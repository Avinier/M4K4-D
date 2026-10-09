"""Screw-stack audit: what each modeled screw passes through, from the B-rep.

For every modeled screw the shank axis is sampled from the head seat to the tip.
At each station, rings just outside the shank (r 1.05), inside a Ø3.2 insert
pocket (r 1.35) and outside it (r 1.8) are tested against the same-frame
printed parts and purchased references. Each station is then classified as:

  clearance  shank free, plastic within r 1.35 (Ø2.3 clearance bore)
  insert     free to r 1.35, plastic at r 1.8 (Ø3.2 heat-set pocket)
  plastic    plastic at r 1.05 (screw cuts printed material)
  metal      inside a purchased reference (tapped servo/coupling hole)
  air        no material round the shank

Engagement is the insert length occupied by the shank, capped at the selected
insert length. Any plastic station is a failure unless the joint is declared
thread-forming. M2 only; the M3 hub screws are checked by check_integration.py.
"""
import json, math, sys
from pathlib import Path
from build123d import Vector
import layout_model as m
import details as d
from inspection_scene import group_for

HERE = Path(__file__).parent
STEP = .2
INSERT = d.M2_INSERT
# Declared plastic-thread joints: the screw is meant to form its own thread.
THREAD_FORMING = {}
# Screws into purchased parts (tapped metal): the servo case holes.
INTO_METAL = ()
METAL = ('STS3045M', 'coupler', 'horn')


def axis_of(shape):
    """Shank axis from the long bounding-box side; head end has the wider section."""
    bb = shape.bounding_box()
    size = [bb.size.X, bb.size.Y, bb.size.Z]
    k = max(range(3), key=lambda i: size[i])
    lo, hi = list(bb.min), list(bb.max)
    centre = [(lo[i] + hi[i]) / 2 for i in range(3)]
    def wide(t):
        p = list(centre); p[k] = t
        q = list(p); q[(k + 1) % 3] += 1.3
        return shape.is_inside(Vector(*q))
    a, b = lo[k] + 1., hi[k] - 1.
    head_at_low = wide(a) and not wide(b)
    head_at_high = wide(b) and not wide(a)
    assert head_at_low != head_at_high, f'ambiguous head end: {shape.label}'
    direction = [0, 0, 0]; direction[k] = 1 if head_at_low else -1
    start = list(centre); start[k] = lo[k] if head_at_low else hi[k]
    return k, Vector(*start), Vector(*direction), size[k]


def ring(point, k, r, n=6):
    u, v = (k + 1) % 3, (k + 2) % 3
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        p = [point.X, point.Y, point.Z]; p[u] += r * math.cos(t); p[v] += r * math.sin(t)
        out.append(Vector(*p))
    return out


def inside(points, solids):
    return sum(any(s.is_inside(p) for s in solids) for p in points) >= len(points) / 2


def classify(name, shape, plastics, metals):
    k, start, direction, length = axis_of(shape)
    seat = None
    stations = []
    t = .1
    while t < length - .05:
        p = start + direction * t
        # The head seat is the first station whose shank section is Ø2.
        if seat is None:
            if not shape.is_inside(p + Vector(*[1.3 if i == (k + 1) % 3 else 0 for i in range(3)])):
                seat = t
            t += STEP; continue
        near_p = [s for s in plastics if _near(s, p)]
        near_m = [s for s in metals if _near(s, p)]
        if near_m and inside(ring(p, k, .5, 3), near_m):
            c = 'metal'
        elif near_p and inside(ring(p, k, 1.05), near_p):
            c = 'plastic'
        elif near_p and inside(ring(p, k, 1.35), near_p):
            c = 'clearance'
        elif near_p and inside(ring(p, k, 1.8), near_p):
            c = 'insert'
        else:
            c = 'air'
        stations.append((round(t - seat, 2), c))
        t += STEP
    runs = []
    for s, c in stations:
        if runs and runs[-1]['class'] == c:
            runs[-1]['to'] = round(s + STEP, 2)
        else:
            runs.append(dict(**{'class': c}, **{'from': s, 'to': round(s + STEP, 2)}))
    total = lambda c: round(sum(r['to'] - r['from'] for r in runs if r['class'] == c), 2)
    tip = runs[-1]['class'] if runs else None
    # A pocket is only fully measured when the shank runs out of it.
    pockets = [i for i, r in enumerate(runs) if r['class'] == 'insert']
    pocket = round(runs[pockets[0]]['to'] - runs[pockets[0]]['from'], 2) if pockets else 0.
    through = bool(pockets) and pockets[0] < len(runs) - 1
    return dict(axis='XYZ'[k], seat=[round(v, 2) for v in tuple(start + direction * (seat or 0))],
                shank_mm=round(length - (seat or 0), 2), runs=runs,
                insert_mm=min(total('insert'), INSERT['length']), pocket_mm=pocket if through else None,
                plastic_mm=total('plastic'), metal_mm=total('metal'), tip=tip)


def _near(s, p, pad=2.):
    bb = s.bounding_box()
    return all(tuple(bb.min)[i] - pad <= tuple(p)[i] <= tuple(bb.max)[i] + pad for i in range(3))


def main():
    parts = m.build_parts(catalog=False, reliefs='--fast' not in sys.argv)
    screws = {n: x for n, x in parts.items()
              if group_for(n, x) == 'fasteners' and '_M2' in n and x['kind'] == 'physical'}
    out, failures = {}, []
    for n, x in sorted(screws.items()):
        frame = x['frame']
        same = {k: v for k, v in parts.items() if v['frame'] == frame and v['kind'] == 'physical'
                and group_for(k, v) != 'fasteners'}
        metals = [v['shape'] for k, v in same.items() if any(t in k for t in METAL)]
        plastics = [v['shape'] for k, v in same.items() if not any(t in k for t in METAL)]
        r = classify(n, x['shape'], plastics, metals)
        forming = any(n.startswith(p) for p in THREAD_FORMING)
        metal = n.startswith(INTO_METAL)
        r['joint'] = 'thread-forming' if forming else 'tapped metal' if metal else 'heat-set insert'
        problems = []
        if r['joint'] == 'heat-set insert':
            if r['plastic_mm'] > STEP + 1e-6: problems.append(f"shank cuts plastic for {r['plastic_mm']} mm")
            if r['insert_mm'] + 1e-6 < INSERT['min_engagement']:
                problems.append(f"insert engagement {r['insert_mm']} < {INSERT['min_engagement']} mm")
            # One sample step of tolerance on the measured pocket length.
            if r['pocket_mm'] is not None and r['pocket_mm'] + STEP < INSERT['length']:
                problems.append(f"pocket {r['pocket_mm']} mm in plastic, shorter than the {INSERT['length']} mm insert")
        elif r['joint'] == 'tapped metal':
            if r['metal_mm'] < 2: problems.append(f"thread in metal {r['metal_mm']} mm")
            if r['plastic_mm'] > STEP + 1e-6: problems.append(f"shank cuts plastic for {r['plastic_mm']} mm")
        r['problems'] = problems
        out[n] = r
        if problems: failures.append(n)
        print(f"{n:42s} {r['joint']:16s} ins {r['insert_mm']:4.1f} pla {r['plastic_mm']:4.1f} "
              f"met {r['metal_mm']:4.1f} tip {r['tip']:9s} {'; '.join(problems)}", flush=True)
    report = dict(method=__doc__.strip().splitlines()[0], insert=INSERT, sample_step_mm=STEP,
                  screws=out, failures=failures, passed=not failures,
                  limitations=['Nominal B-rep only: no insert knurl, thread pitch, preload, '
                               'pull-out or print tolerance. Driver access is not checked here.'])
    (HERE / 'generated' / 'fastener-stack.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS' if not failures else f'FAIL: {len(failures)} screws')
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
