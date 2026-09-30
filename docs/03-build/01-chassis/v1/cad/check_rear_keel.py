"""Fast J09/J10 checks for the rear TCRT keel: fastening, cartridge, wear parts, J10-10 route, removal paths.

Run from this folder with the text-to-cad 0.4.28 runtime: python check_rear_keel.py
Writes generated/rear-keel-checks.json.
"""
import itertools
import json
import sys

sys.path.insert(0, ".")
import body_chassis_model as M
from build123d import Location


def _vol(s):
    return 0.0 if s is None else s.volume


def leaves(s):
    k = getattr(s, "children", None)
    return [l for c in k for l in leaves(c)] if k else [s]


def by_label(ss, label):
    return next(s for s in ss if s.label == label)


def moved(s, dx=0.0, dy=0.0, dz=0.0):
    return s.moved(Location((dx, dy, dz)))


frame = M.chassis_frame()
frame_parts = leaves(frame)
crossmember = by_label(frame_parts, "REAR_SKID_CROSSMEMBER")
inserts = [p for p in frame_parts if p.label.startswith("REAR_KEEL_HEATSET_INSERT_")]
keel_group = M.rear_skid_tcrt_module().children[0]
keel_parts = leaves(keel_group)
keel = by_label(keel_parts, "REAR_KEEL_FACETED_BODY")
shoe = by_label(keel_parts, "REAR_KEEL_REPLACEABLE_WEAR_SHOE")
bezel = by_label(keel_parts, "REAR_TCRT_BEZEL_WITH_GUARDS")
shims = [p for p in keel_parts if p.label.startswith("REAR_TCRT_HEIGHT_SHIM_")]
tcrt = by_label(keel_parts, "TCRT5000_REAR_STEP")
joints = by_label(keel_parts, "TCRT_REAR_LEAD_JOINTS_HEATSHRINK")
pigtail = by_label(keel_parts, "TCRT_REAR_J10_10_PIGTAIL")
keel_screws = [p for p in keel_parts if p.label.startswith("REAR_KEEL_M3X30_SCREW_")]
shoe_screw = by_label(keel_parts, "REAR_KEEL_SHOE_M2X6_SCREW")
bezel_screw = by_label(keel_parts, "REAR_TCRT_BEZEL_M2X10_SCREW")
shell = next(l for l in leaves(M.body_shell()) if l.label == "BODY_SHELL")
routes = [p for p in leaves(M.harness_routes()) if p.label.startswith("HARNESS_REAR_TCRT_J10_10")]
R = {}

# Keel parts and the crossmember: every intended contact is surface-only, except
# the TCRT leads inside their solder-joint envelope.
solids = keel_parts + [crossmember, *inserts]
# The one-solid TCRT STEP carries its leads, which the solder joints and heat-shrink wrap;
# the pigtail runs out of the joint envelope.
allowed = {frozenset(("TCRT5000_REAR_STEP", joints.label)), frozenset((joints.label, pigtail.label))}
# Heat-set inserts sit 0.3 mm radially into their O4.0 bores by design.
allowed |= {frozenset(("REAR_SKID_CROSSMEMBER", i.label)) for i in inserts}
clashes = {}
for a, b in itertools.combinations(solids, 2):
    if frozenset((a.label, b.label)) in allowed:
        continue
    v = _vol(a & b)
    if v > 1e-3:
        clashes[f"{a.label} x {b.label}"] = round(v, 3)
R["keel_stack_has_no_clashes"] = (not clashes, clashes)
R["keel_seats_on_crossmember"] = (_vol(keel & crossmember) < 1e-6 and keel.distance_to(crossmember) < 1e-6,)
R["keel_stack_clears_shell"] = (all(_vol(p & shell) < 1e-3 for p in keel_parts), {p.label: round(_vol(p & shell), 3) for p in keel_parts if _vol(p & shell) >= 1e-3})

# J09A: screws in clear holes, thread engagement in the inserts, insert walls.
eng = {}
for screw in keel_screws:
    sb = screw.bounding_box()
    ins = min(inserts, key=lambda i: (i.bounding_box().center() - sb.center()).length)
    ib = ins.bounding_box()
    eng[screw.label] = round(min(sb.max.Z, ib.max.Z) - max(sb.min.Z, ib.min.Z), 2)
R["keel_screws_engage_inserts_5mm"] = (all(v >= 5.0 for v in eng.values()), eng)
tips = {s.label: round(s.bounding_box().max.Z, 2) for s in keel_screws}
R["keel_screw_tips_inside_clearance"] = (all(t <= M.REAR_KEEL_TOP_Z + 9.5 for t in tips.values()), tips)
# Crossmember body faces (the tie lug widens its bounding box).
fx0, fx1 = M.SKID_ROOT_DATUM[0] - 8.0, M.SKID_ROOT_DATUM[0] + 8.0
walls = {i.label: round(min(i.bounding_box().min.X - fx0, fx1 - i.bounding_box().max.X), 2) for i in inserts}
R["crossmember_insert_wall_ge_1p5"] = (all(w >= 1.5 for w in walls.values()), walls)
tool = {}
for screw in keel_screws:
    c = screw.bounding_box().center()
    key = M._z_cylinder(M.REAR_KEEL_COUNTERBORE_RADIUS - 0.25, -30.0, screw.bounding_box().min.Z, c.X, c.Y)  # hex key + fingers straight up
    hit = {p.label: round(_vol(key & p), 3) for p in (keel, shoe, bezel, *shims) if _vol(key & p) > 1e-3}
    tool[screw.label] = hit
R["keel_screws_drivable_from_below_keel_on"] = (not any(tool.values()), tool)

# J09B: shims clear the sensor and its leads; the bezel carries the sensor at the datum.
R["height_shims_clear_tcrt"] = (all(_vol(s & tcrt) < 1e-6 for s in shims), {s.label: round(_vol(s & tcrt), 3) for s in shims})
tb = tcrt.bounding_box()
ledge = _vol(bezel & M._block(tb.min.X, tb.max.X, tb.min.Y, tb.max.Y, M.TCRT_OPTICAL_FACE_Z - 0.5, M.TCRT_OPTICAL_FACE_Z))
R["tcrt_face_on_bezel_ledge"] = (abs(tb.min.Z - M.TCRT_OPTICAL_FACE_Z) < 1e-3 and ledge > 1e-3 and _vol(bezel & tcrt) < 1e-6, round(tb.min.Z, 3), round(ledge, 3))
shim_range = [M.REAR_TCRT_BELLY_Z - n * M.REAR_TCRT_SHIM_T for n in range(M.REAR_TCRT_SHIMS_RANGE[0], M.REAR_TCRT_SHIMS_RANGE[1] + 1)]
R["j09_height_range_pm2"] = (min(shim_range) <= M.TCRT_OPTICAL_FACE_Z - 2.0 and max(shim_range) >= M.TCRT_OPTICAL_FACE_Z + 2.0, shim_range)
# Sensor, joints and lead move together with the shims; they must clear the
# keel at both ends of the range (the flexible lead takes up the travel).
stack = [tcrt, joints, pigtail]
ends = {}
for face in (min(shim_range), max(shim_range)):
    dz = face - M.TCRT_OPTICAL_FACE_Z
    ends[face] = round(sum(_vol(moved(p, dz=dz) & keel) for p in stack), 3)
R["sensor_stack_clears_keel_across_j09_range"] = (all(v < 1e-3 for v in ends.values()), ends)
R["guard_lips_below_face_above_shoe"] = (M.SKID_SHOE_BOTTOM_Z < bezel.bounding_box().min.Z < tcrt.bounding_box().min.Z, round(bezel.bounding_box().min.Z, 2))

# Removal paths (straight 20 mm pulls, 1 mm steps).
def sweep(parts, against, dx=0.0, dz=0.0, steps=20):
    worst = 0.0
    for i in range(1, steps + 1):
        f = i / steps
        for p in parts:
            m = moved(p, dx=dx * f, dz=dz * f)
            for a in against:
                worst = max(worst, _vol(m & a))
    return round(worst, 3)

swap = (sweep([bezel, *shims, bezel_screw], [keel], dz=-20.0), sweep([tcrt, joints], [keel], dz=-20.0))
R["sensor_and_lead_drop_out_below_keel_on"] = (max(swap) < 1e-3, *swap)
R["shoe_slides_out_forward"] = (sweep([shoe], [keel], dx=20.0) < 1e-3, sweep([shoe], [keel], dx=20.0))
keel_module = [p for p in keel_parts if p not in keel_screws and p is not pigtail]
others = [crossmember, *inserts, shell] + [p for p in frame_parts if p.label.startswith(("CHASSIS_RAIL", "CHASSIS_DECK", "BATTERY", "BALLAST"))]
R["keel_drops_30mm_clear"] = (sweep(keel_module, others, dz=-30.0, steps=10) < 1e-3, sweep(keel_module, others, dz=-30.0, steps=10))

# J10-10 route and disconnect point.
names = [r.label for r in routes]
R["pigtail_leaves_through_keel_top"] = (_vol(pigtail & keel) < 1e-3 and pigtail.bounding_box().max.Z > M.REAR_KEEL_TOP_Z, round(_vol(pigtail & keel), 3))
R["j10_10_route_modelled"] = ({"HARNESS_REAR_TCRT_J10_10_SERVICE_LOOP", "HARNESS_REAR_TCRT_J10_10_RISER"} <= set(names), names)
loop = by_label(routes, "HARNESS_REAR_TCRT_J10_10_SERVICE_LOOP").bounding_box()
R["service_loop_ge_30mm"] = (loop.size.Y + 2 * loop.size.Z >= 30.0, round(loop.size.Y + 2 * loop.size.Z, 1))
obstacles = [p for p in frame_parts] + [shell, keel]
for fn in ("electronics", "body_primary_frame", "body_panels", "body_audio", "body_chassis_mount_hardware", "sensors"):
    obstacles += leaves(getattr(M, fn)())
skip = ("C3_GH_PLUG_LAYER", "C3_J10_10_GHR04_MATED_PLUG", "")
route_hits = {}
for r in routes:
    rb = r.bounding_box()
    for o in obstacles:
        if o.label in skip:
            continue
        ob = o.bounding_box()
        if ob.min.X > rb.max.X or ob.max.X < rb.min.X or ob.min.Y > rb.max.Y or ob.max.Y < rb.min.Y or ob.min.Z > rb.max.Z or ob.max.Z < rb.min.Z:
            continue
        v = _vol(r & o)
        if v > 1e-3:
            route_hits[f"{r.label} x {o.label}"] = round(v, 3)
R["j10_10_route_clear"] = (not route_hits, route_hits)
lug = M.REAR_CROSSMEMBER_TIE_LUG
riser = by_label(routes, "HARNESS_REAR_TCRT_J10_10_RISER").bounding_box()
R["strain_relief_lug_beside_riser"] = (0.0 <= lug[0] - riser.max.X <= 1.0 and riser.min.Y <= lug[2] and lug[3] <= riser.max.Y, round(lug[0] - riser.max.X, 2))

# Mass inputs for the MASS_ROWS entry (hand-kept register).
printed = {p.label: round(p.volume / 1000.0, 3) for p in (keel, shoe, bezel, *shims)}
R["_volumes_cm3"] = (True, printed)
cg = keel.center()
R["_keel_body_centroid"] = (True, [round(v, 2) for v in (cg.X, cg.Y, cg.Z)])

out = {k: {"pass": bool(v[0]), "detail": v[1:]} for k, v in R.items()}
with open("generated/rear-keel-checks.json", "w") as f:
    json.dump(out, f, indent=2, default=str)
for k, v in R.items():
    print("PASS" if v[0] else "FAIL", k, *v[1:])
