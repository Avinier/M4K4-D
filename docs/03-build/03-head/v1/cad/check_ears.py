"""Ear hardware and neutral-pose removal checks for the head-v1 CAD.

These are rigid, nominal B-rep paths. Printed fits and access for a real
screwdriver still need a physical assembly trial.
"""
import json
import sys
from pathlib import Path

from build123d import Location, export_stl

import layout_model as m

HERE = Path(__file__).resolve().parent
parts = m.build_parts(catalog=False)


def overlap(a, b):
    aa, bb = a.bounding_box(), b.bounding_box()
    if any(tuple(aa.max)[i] <= tuple(bb.min)[i] + 1e-6 or
           tuple(bb.max)[i] <= tuple(aa.min)[i] + 1e-6 for i in range(3)):
        return 0.0
    return sum(max(0, solid.volume) for solid in m.pieces(a.intersect(b)))


results = {}
for sign in (-1, 1):
    prefix = f'ear_{sign}_'
    cap = parts[prefix + 'hollow_removable_cap']['shape']
    rim = parts[prefix + 'ridged_inner_mount']['shape']
    inlays = [parts[prefix + name]['shape'] for name in ('amber_inlay', 'dark_centre')]
    trim = [parts[prefix + name]['shape'] for name in ('trim_slug_stack_max', 'trim_M2x5')]
    cap_screws = [n for n in parts if n.startswith(prefix + 'M2_')]
    hidden_screws = [n for n in parts if n.startswith(prefix + 'hidden_mount_M2_')]
    assert len(cap_screws) == 2 and len(hidden_screws) == 2

    # After removing the two exposed screws, the cap, its glued finish and
    # the installed trim stack travel straight outboard. The two hidden mount
    # screws stay installed during this step.
    cap_blockers = [prefix + 'ridged_inner_mount',
                    'connected_rolling_cradle_flange_ear_stalks',
                    'main_octagonal_skin', *hidden_screws]
    cap_hits = []
    for travel in (0, 1, 3, 6, 10, 20):
        for moving_name, moving in [('cap', cap), ('amber', inlays[0]),
                                    ('centre', inlays[1]), ('trim', trim[0]),
                                    ('trim screw', trim[1])]:
            moved = moving.moved(Location((0, sign * travel, 0)))
            for blocker in cap_blockers:
                volume = overlap(moved, parts[blocker]['shape'])
                if volume > 1e-4:
                    fragments = m.pieces(moved.intersect(parts[blocker]['shape']))
                    bounds = max(fragments, key=lambda s: s.volume).bounding_box()
                    cap_hits.append(dict(travel_mm=travel, moving=moving_name,
                                         blocker=blocker, overlap_mm3=round(volume, 5),
                                         min_xyz=list(bounds.min), max_xyz=list(bounds.max)))

    # Then remove the two hidden mount screws and withdraw the inner ring.
    rim_hits = []
    for travel in (1, 3, 6, 10, 20):
        moved = rim.moved(Location((0, sign * travel, 0)))
        for blocker in ('connected_rolling_cradle_flange_ear_stalks',
                        'main_octagonal_skin'):
            volume = overlap(moved, parts[blocker]['shape'])
            if volume > 1e-4:
                fragments = m.pieces(moved.intersect(parts[blocker]['shape']))
                bounds = max(fragments, key=lambda s: s.volume).bounding_box()
                rim_hits.append(dict(travel_mm=travel, blocker=blocker,
                                     overlap_mm3=round(volume, 5),
                                     min_xyz=list(bounds.min), max_xyz=list(bounds.max)))

    finish_hits = [overlap(cap, shape) for shape in inlays]
    hardware_hits = []
    for cap_name in cap_screws:
        for hidden_name in hidden_screws:
            volume = overlap(parts[cap_name]['shape'], parts[hidden_name]['shape'])
            if volume > 1e-4:
                hardware_hits.append(dict(a=cap_name, b=hidden_name,
                                          overlap_mm3=round(volume, 5)))
    results[str(sign)] = dict(cap_screws=cap_screws, hidden_mount_screws=hidden_screws,
                              cap_solids=len(cap.solids()), rim_solids=len(rim.solids()),
                              cap_valid=cap.is_valid, rim_valid=rim.is_valid,
                              finish_intersections_mm3=finish_hits,
                              hardware_intersections=hardware_hits,
                              cap_withdrawal_hits=cap_hits,
                              inner_mount_withdrawal_hits=rim_hits)

passed = all(d['cap_valid'] and d['rim_valid'] and d['cap_solids'] == d['rim_solids'] == 1
             and not d['cap_withdrawal_hits'] and not d['inner_mount_withdrawal_hits']
             and not d['hardware_intersections']
             and max(d['finish_intersections_mm3']) < 1e-4 for d in results.values())
report = dict(passed=passed, method='Rigid, nominal neutral-pose outboard withdrawal; '
              'two cap screws removed before cap, two hidden mount screws removed before rim.',
              sides=results, limitations=['No wire flex, driver swept volume, press-fit force, '
                                           'insert retention or service-cycle evidence.'])
(HERE / 'generated' / 'ear-service.json').write_text(json.dumps(report, indent=2) + '\n')
if len(sys.argv) > 1:
    mesh_dir = Path(sys.argv[1]).expanduser().resolve()
    mesh_dir.mkdir(parents=True, exist_ok=True)
    for name, part in parts.items():
        if name.startswith('ear_') and any(tag in name for tag in
                                           ('hollow_removable_cap', 'ridged_inner_mount',
                                            'amber_inlay', 'dark_centre')):
            export_stl(part['shape'], mesh_dir / f'{name}.stl',
                       tolerance=.05, angular_tolerance=.1)
print(json.dumps(report, indent=2))
raise SystemExit(0 if passed else 1)
