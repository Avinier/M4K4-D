"""D-068: measure the PCB-10 C3 carrier mounting that the droid edits make.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the chassis and body trees (about 3 min), not the head.

The carrier keeps its two lower M2.5 screws (Z 86). Each printed upright gets a header-row
relief for the DevKitC pin tails and a hook over the board's top edge; the module goes in
2 mm low, slides up under the hooks, then the lower screws go in. The DevKitC is Espressif's
ESP32-S3-DevKitC-1 v1.1, built from Espressif's drawing in makad-v1.step.py. Mated GH plugs
and screws are not on the module while it goes in. The vendor Pi and cooler are tested as boxes.
"""

import importlib.util
from pathlib import Path

from build123d import Axis, Box, Compound, Cylinder, Location, Shape
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.TopAbs import TopAbs_COMPOUND, TopAbs_SOLID
from OCP.TopoDS import TopoDS
from build123d import Solid

import body_v1_model as B

spec = importlib.util.spec_from_file_location("makad_v1_entry", Path(__file__).resolve().with_name("makad-v1.step.py"))
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)
MNT = entry.PCB10_MOUNT

VENDOR = ("C0_RASPBERRY_PI5_EXACT_STEP", "PI5_ACTIVE_COOLER_STEP")
CARRIER = "C3_CARRIER_PCB10_WITH_DEVKITC"
UPRIGHT = "BODY_FRAME_C3_CARRIER_UPRIGHT_"
RESERVE = ("RESERVE", "HARNESS_", "CORRIDOR")
REGION = (-45.0, 80.0, -80.0, -25.0, 60.0, 140.0)
APPROACH = [k * 0.5 for k in range(61)]           # Y offsets from the wall at the low position, 0-30 mm
NEED = 2.5                                        # approach needed: tails (1.5) out of the reliefs, plus margin
DRIVER_R = 2.0                                    # M2.5 driver shank, Ø4
MIN_GAP = 0.3


def _box(shape):
    w = shape.wrapped if hasattr(shape, "wrapped") else shape
    if w is None or w.IsNull():
        return (1e9, 1e9, 1e9, -1e9, -1e9, -1e9)   # empty: hits nothing
    b = Bnd_Box()
    BRepBndLib.Add_s(w, b, False)
    return b.Get()


def _hit(a, b, pad=0.0):
    return not (a[3] + pad <= b[0] or b[3] + pad <= a[0] or a[4] + pad <= b[1] or
                b[4] + pad <= a[1] or a[5] + pad <= b[2] or b[5] + pad <= a[2])


def _place(node, loc):
    """The leaf at its world place, sharing its geometry (TopoDS Moved, no copy)."""
    m = node.wrapped.Moved(loc.wrapped)
    if m.ShapeType() == TopAbs_COMPOUND:
        return Compound(TopoDS.Compound_s(m))
    if m.ShapeType() == TopAbs_SOLID:
        return Solid(TopoDS.Solid_s(m))
    return Shape.cast(m)


def _blk(b):
    return Box(b[3] - b[0], b[4] - b[1], b[5] - b[2]).moved(Location(((b[0] + b[3]) / 2, (b[1] + b[4]) / 2, (b[2] + b[5]) / 2)))


def _leaves(node, loc=Location(), path=()):
    here = loc * node.location
    kids = list(node.children) if getattr(node, "children", None) else []
    name = path + (node.label or "?",)
    if not kids or any(v in (node.label or "") for v in VENDOR):
        yield name, node, loc
        return
    for kid in kids:
        yield from _leaves(kid, here, name)


def _vol(shape):
    return shape.volume if shape is not None and shape.solids() else 0.0


def main():
    tree = entry._apply_droid_cuts(Compound(children=[B.build_body_assembly(), B.chassis_v1_reference()]), strict=False)
    # OCC-level placement: Moved() shares the geometry, so the vendor STEPs cost nothing until
    # they are boxed; build123d moved() on every leaf copies them and stalls.
    every = [(path, _place(node, loc)) for path, node, loc in _leaves(tree)
             if node.wrapped is not None and not node.wrapped.IsNull()]
    labels = [p[-1] for p, _ in every]
    near = [(p, s) for p, s in every if _hit(_box(s), (*REGION[0::2], *REGION[1::2]))]

    ok = True

    def report(name, passed, detail):
        nonlocal ok
        ok &= bool(passed)
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}", flush=True)

    def solid(shape, path):
        return _blk(_box(shape)) if any(v in "/".join(path) for v in VENDOR) else shape

    own = [(p, s) for p, s in near if CARRIER in p and not p[-1].startswith(UPRIGHT)]
    ups = {p[-1]: s for p, s in near if p[-1].startswith(UPRIGHT)}
    others = [(p, solid(s, p)) for p, s in near if CARRIER not in p]
    fixed = [(p, s) for p, s in others if not any(r in p[-1] for r in RESERVE)] + [((k,), s) for k, s in ups.items()]
    reserves = [(p, s) for p, s in others if any(r in p[-1] for r in RESERVE)]
    part = {p[-1]: s for p, s in own}

    # 1. The generic DevKitC and the upper screws are gone; Espressif's v1.1 is in.
    gone = [l for l in labels if l in ("C3_ESP32_S3_DEVKITC_STEP", "C3_DEVKIT_HEADER_ROW_1", "C3_DEVKIT_HEADER_ROW_2")
            or l.startswith(("C3_CARRIER_M25_SCREW_HEAD_2", "C3_CARRIER_M25_SCREW_HEAD_4"))]
    v11 = [l for l in labels if l.startswith("C3_DEVKITC_V11_")] + [p[-2] for p, _ in every if "C3_DEVKITC_V11_PINS" in p[-2]][:2]
    screws = sorted(l for l in labels if l.startswith("C3_CARRIER_M25_SCREW_HEAD_"))
    report("DevKitC replaced, upper screws deleted", not gone and len(v11) >= 6 and screws == ["C3_CARRIER_M25_SCREW_HEAD_1", "C3_CARRIER_M25_SCREW_HEAD_3"],
           f"left over {gone or 'none'}; v1.1 parts {sorted(set(v11))}; screws {screws}")

    board = part["C3_CARRIER_PCB10_BOARD"]
    pcb = part["C3_DEVKITC_V11_PCB"]
    pb = _box(pcb)
    report("DevKitC v1.1 outline", abs((pb[3] - pb[0]) - 62.74) < 0.01 and abs((pb[5] - pb[2]) - 25.40) < 0.01,
           f"PCB X {pb[0]:.2f}..{pb[3]:.2f}, Z {pb[2]:.2f}..{pb[5]:.2f}, underside Y {pb[1]:.2f}")

    # 2. Pin tails clear the uprights, installed and through the slide.
    pins = [s for p, s in own if any("C3_DEVKITC_V11_PINS" in n for n in p)]
    slide = MNT["slide"]
    worst = min((pin.moved(Location((0, 0, dz))).distance(u), dz, k)
                for dz in (-slide, -slide / 2, 0.0) for pin in pins for k, u in ups.items() if _hit(_box(pin), _box(u), pad=4.0))
    report("pin tails clear the uprights (reliefs)", worst[0] >= MIN_GAP,
           f"{len(pins)} pins, nearest {worst[0]:.2f} mm ({worst[2]}, slide {worst[1]:+.1f})")

    # 3. Hooks: gaps to the board, engagement, clearance to the DevKitC.
    bb = _box(board)
    rows = []
    for k, u in ups.items():
        lip = u & _blk((bb[0], bb[4], bb[5] - 3.0, bb[3], bb[4] + 3.0, bb[5]))
        lb = _box(lip)
        bridge = u & _blk((bb[0], bb[1] + 0.05, bb[5], bb[3], bb[4] - 0.05, bb[5] + 3.0))   # over the edge only
        rb = _box(bridge)
        dk = min(u.distance(s) for p, s in own if any("C3_DEVKITC_V11" in n for n in p) and _hit(_box(s), _box(u), pad=3.0))
        rows.append((k, lb[1] - bb[4], rb[2] - bb[5], bb[5] - lb[2], dk, _vol(u & board)))
    good = all(abs(g - 0.1) < 0.01 and abs(o - 0.1) < 0.01 and e >= 1.8 and d >= MIN_GAP and v < 1e-6 for _, g, o, e, d, v in rows)
    report("hooks over the top edge", good, "; ".join(
        f"{k[-1]}: lip gap {g:.2f}, over the edge {o:.2f}, engagement {e:.2f}, to DevKitC {d:.2f}, overlap {v:.3f}"
        for k, g, o, e, d, v in rows))

    # 4. Install: the module (board, DevKitC, headers; no plugs or screws) sits 2 mm low against
    #    the wall and slides up 2 mm under the hooks. Before that it must come in toward the wall:
    #    the frame's front upper cross rail (Z 126) stops it being lowered from above, so it comes
    #    in from inboard. Measure how far out it is clear at the low position, and what stops it.
    module = [s for p, s in own if not any(x in p[-1] for x in ("MATED_PLUG", "M25_SCREW"))]

    def clashes_at(dy, dz):
        found = {}
        for m in module:
            mm = m.moved(Location((0.0, dy, dz)))
            mb = _box(mm)
            for p, f in fixed:
                if _hit(mb, _box(f)):
                    v = _vol(mm & f)
                    if v > 1e-4:
                        found[p[-1]] = max(v, found.get(p[-1], 0.0))
        return found

    slide_hits = {}
    for f in (1.0, 0.75, 0.5, 0.25, 0.0):
        slide_hits.update(clashes_at(0.0, -slide * f))
    report("2 mm slide up under the hooks", not slide_hits,
           "clear" if not slide_hits else "; ".join(f"{k} {v:.3f} mm3" for k, v in sorted(slide_hits.items())))
    depth, stop = None, {}
    for dy in APPROACH:
        stop = clashes_at(dy, -slide)
        if stop:
            break
        depth = dy
    report(f"approach toward the wall at the low position (need {NEED} mm)", depth is not None and depth >= NEED,
           f"clear to {depth} mm out; " + ("clear to 30 mm" if not stop else "then hits " + "; ".join(
               f"{k} {v:.2f} mm3" for k, v in sorted(stop.items()))))

    # 5. Lower screws: a Ø4 driver from each head out to Y -30, plugs off. The module goes in
    #    before the compute tray (assembly order, D-068), so the tray and its fixings are left
    #    out of the pass test; the free reach with the tray in is reported for service.
    tray = ("COMPUTE_TRAY", "TRAY_")
    rows = []
    for k in (1, 3):
        head = _box(part[f"C3_CARRIER_M25_SCREW_HEAD_{k}"])
        x, z = (head[0] + head[3]) / 2, (head[2] + head[5]) / 2

        def driver(y_end):
            return Cylinder(DRIVER_R, y_end - head[4]).rotate(Axis.X, 90).moved(Location((x, (head[4] + y_end) / 2, z)))

        obst = [(p[-1], s) for p, s in fixed] + [(p[-1], s) for p, s in own if "MATED_PLUG" not in p[-1] and "M25_SCREW" not in p[-1]]
        tool = driver(-30.0)
        tb = _box(tool)
        near_tool = [(l, s) for l, s in obst if _hit(tb, _box(s), pad=3.0)]
        d = min(((tool.distance(s), l) for l, s in near_tool if not l.startswith(tray)), default=(99.0, "none"))
        reach = 0.0
        for y_end in [head[4] + 0.5 * i for i in range(1, 51)]:
            if any(_vol(driver(y_end) & s) > 1e-4 for l, s in near_tool):
                break
            reach = y_end - head[4]
        rows.append((k, x, z, d, reach))
    report("lower screws reachable before the compute tray", all(r[3][0] >= 0.2 for r in rows),
           "; ".join(f"screw {k} at ({x:.0f}, {z:.0f}): driver {d[0]:.2f} mm from {d[1]}; reach with the tray in {r:.1f} mm"
                     for k, x, z, d, r in rows))

    # 6. D-068 amended: the board grown to Z 76, the GH headers and plugs in their three rows and the real
    #    J10-1 Micro-Fit, against every fixed part (the board bears on the uprights by design).
    bb = _box(board)
    j101 = _box(part["C3_J10_1_MICROFIT3_2P_RA_HEADER"])
    conn = [(p[-1], s) for p, s in own if p[-1].startswith("C3_J10_") or p[-1] == "C3_CARRIER_PCB10_BOARD"]
    worst = []
    for l, s in conn:
        sb = _box(s)
        for p, f in fixed:
            if (l == "C3_CARRIER_PCB10_BOARD" and p[-1].startswith(UPRIGHT)) or not _hit(sb, _box(f), pad=2.0):
                continue
            worst.append((s.distance(f), l, p[-1]))
    worst.sort()
    report("grown board, connectors and plugs clear of fixed parts",
           abs(bb[2] - 76.0) < 0.01 and abs((j101[5] - j101[2]) - 9.655) < 0.01 and abs(j101[2] - 78.6) < 0.01 and (not worst or worst[0][0] >= MIN_GAP),
           f"board Z {bb[2]:.2f}..{bb[5]:.2f}; J10-1 housing X {j101[0]:.2f}..{j101[3]:.2f}, Z {j101[2]:.2f}..{j101[5]:.2f}; nearest: "
           + ("; ".join(f"{l} {d:.2f} to {o}" for d, l, o in worst[:3]) or "nothing within 2 mm"))

    # 7. Installed: DevKitC and hooks against everything else; reserves reported.
    dev = [(p[-1], s) for p, s in own if any("C3_DEVKITC_V11" in n for n in p)]
    hard, soft = [], []
    for l, s in dev:
        sb = _box(s)
        for p, f in fixed:
            if p[-1].startswith(UPRIGHT) or not _hit(sb, _box(f), pad=3.0):
                continue
            hard.append((s.distance(f), l, p[-1]))
        for p, f in reserves:
            if _hit(sb, _box(f), pad=3.0):
                soft.append((s.distance(f), l, p[-1]))
    hard.sort()
    soft.sort()
    report("DevKitC v1.1 clear of fixed parts", not hard or hard[0][0] >= MIN_GAP,
           "; ".join(f"{l} {d:.2f} to {o}" for d, l, o in hard[:3]) or "nothing within 3 mm")
    print("INFO  reserves near the DevKitC: " + ("; ".join(f"{l} {d:.2f} to {o}" for d, l, o in soft[:4]) or "none"))

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
