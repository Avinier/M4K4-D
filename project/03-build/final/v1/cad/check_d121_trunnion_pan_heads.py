"""D-121: HD-010 retainer screws as M2 x 3 pan heads in counterbored lugs.

Builds the head parts (catalog off), drops the two D-051 M2 x 4 button heads,
cuts the retainer's lug counterbores and adds the pan-head envelopes from
d121_trunnion_pan_heads, then checks:

- the cut retainer: valid single solid, 0.6 mm under each head, full plate over
  the MR106ZZ outer ring (cut outside the bearing), still on the bearing;
- the heads: seated on the plate, not proud of the -Y leg face, radial room in
  the recess, thread in the insert and tip short of the pocket floor;
- no interference at neutral with any head part;
- a roll x pitch grid of every roll- and pitch-frame part against the heads,
  >= 0.99 mm (D-049 rule), with the old button heads for reference;
- the edits applied through the droid entry to the real head tree;
- mass.

Run from this folder with the legacy runtime; PYTHONPATH = 03-head/v1/cad first,
MAKAD_RELIEF_SERIAL=1 (see ../README.md). About 5 min.
"""
import math
import re
from build123d import Compound, Location
import module_checks as C
import d121_trunnion_pan_heads as D

STEEL, PETG = 7.9e-3, 1.27e-3


def main():
    entry = C.load_entry()
    import layout_model as m
    import feetech as fe
    import motion_envelope as env
    from inspection_scene import parts_scene
    parts = m.build_parts(catalog=False)
    C.log("head parts built")
    r = C.Report("check_d121_trunnion_pan_heads")
    shapes = {n: d["shape"] for n, d in parts.items() if d["kind"] == "physical"}
    frames = {n: d["frame"] for n, d in parts.items()}
    old = {n: shapes.pop(n) for n in list(shapes) if any(re.fullmatch(p, n) for p in D.REMOVES)}
    plate_old = shapes["pitch_trunnion_retainer"]
    plate = plate_old - D.counterbore_tool()
    shapes["pitch_trunnion_retainer"] = plate
    new = {f"pan_{k:g}": s for k, s in D.screws().items()}
    r.check("removed_button_heads", len(old) == 2, removed=sorted(old))
    r.check("parts_valid_single_solids",
            all(s.is_valid and len(s.solids()) == 1 for s in [plate, *new.values()]),
            plate=[bool(plate.is_valid), len(plate.solids())],
            screws={k: [bool(s.is_valid), len(s.solids())] for k, s in new.items()})

    # --- Retainer -------------------------------------------------------------
    T = fe.TRUNNION
    under_head = D.SEAT_Y - D.FLOOR_Y
    r.check("plate_under_head_mm", abs(under_head) >= .6 - 1e-6, thickness=round(-under_head, 3))
    axis_to_cut = T["screw_r"] - D.CB_R
    r.check("cut_outside_bearing_outer_ring", axis_to_cut >= T["bearing"]["D"] / 2 + .5,
            axis_to_cut=axis_to_cut, bearing_R=T["bearing"]["D"] / 2)
    brg = shapes["pitch_trunnion_bearing_MR106ZZ"]
    r.check("retainer_still_on_bearing", C.distance(plate, brg) < 1e-3, gap=C.distance(plate, brg))
    removed = PETG * (C.volume(plate_old) - C.volume(plate))
    r.check("counterbore_material_small", 0 < removed < .05, removed_g=removed)

    # --- Heads ------------------------------------------------------------------
    seated = [C.distance(s, plate) for s in new.values()]
    inter = [C.common(s, plate) for s in new.values()]
    r.check("heads_seated_on_plate", max(seated) < 1e-3 and max(inter) < 1e-3, gaps=seated, overlap_mm3=inter)
    head_min_y = min(C._box(s)[1] for s in new.values())
    below = head_min_y - D.LEG_FACE_Y
    r.check("heads_below_leg_face_mm", below >= .1 - 1e-6, below=round(below, 3), leg_face_y=D.LEG_FACE_Y)
    leg = shapes["yaw_yoke_leg_-55"]
    room = min(C.distance(s, leg) for s in new.values())
    r.check("head_radial_room_in_recess_mm", room >= .3, nearest_leg=round(room, 3))
    insert_end = D.FLOOR_Y + 3.0
    tip = D.SEAT_Y + D.SCREW_LEN
    engagement = min(tip, insert_end) - D.FLOOR_Y
    pocket_floor = D.FLOOR_Y + T["insert_pocket"]
    r.check("thread_in_insert_mm", engagement >= 2.4 - 1e-6, engagement=round(engagement, 3),
            note="fastener-stack min_engagement 2.4 (1.2 d)")
    r.check("tip_short_of_pocket_floor_mm", pocket_floor - tip >= .5, margin=round(pocket_floor - tip, 3),
            note="covers the +/-0.24 length tolerance")

    # --- Static interference at neutral ------------------------------------------
    clashes = []
    for k, s in new.items():
        for n, t in shapes.items():
            if C._hit(C._box(s), C._box(t)) and C.common(s, t) > 1e-3:
                clashes.append((k, n, round(C.common(s, t), 4)))
    r.check("no_interference_at_neutral", not clashes, clashes=clashes)

    # --- Motion: roll/pitch parts against the yaw-carried heads -----------------------
    heads = Compound(children=list(new.values()))
    buttons = Compound(children=list(old.values()))
    movers = {n: t for n, t in shapes.items() if frames[n] in ("R", "P")}
    poses = env.grid_poses(env.load(), [m.ROLL_STOP[0], -10, 0, 10, m.ROLL_STOP[1]],
                           [m.PITCH_STOP[0], -15, 0, 15, m.PITCH_STOP[1]])
    worst, worst_old, hits = (99., None, None), (99., None, None), []
    hb = C._box(heads)
    for roll, pitch in poses:
        for n, t in movers.items():
            mv = t.rotate(m.ROLL_AXIS, roll) if frames[n] == "R" else t
            mv = mv.rotate(m.PITCH_AXIS, pitch)
            if not C._hit(hb, C._box(mv), 3.):
                continue
            if C._hit(hb, C._box(mv)) and C.common(heads, mv) > 1e-3:
                hits.append(((roll, pitch), n))
            d = C.distance(heads, mv)
            if d < worst[0]:
                worst = (round(d, 3), n, (roll, pitch))
            d0 = C.distance(buttons, mv)
            if d0 < worst_old[0]:
                worst_old = (round(d0, 3), n, (roll, pitch))
    r.check("roll_pitch_grid_vs_heads", not hits and worst[0] >= .99, poses=len(poses), clashes=hits[:10],
            nearest_within_3mm=worst, d051_button_heads_were=worst_old)

    # --- Through the droid entry ---------------------------------------------------
    head = Compound(label="Head v1", children=[*parts_scene(parts).children]).moved(Location(entry.HEAD_ORIGIN_IN_CHASSIS))
    tree = entry._apply_droid_cuts(Compound(label="t", children=[head]), strict=False)
    leaves = {}

    def walk(n, loc):
        here = loc * n.location
        kids = list(n.children) if getattr(n, "children", None) else []
        if not kids:
            leaves[n.label] = n
        for k in kids:
            walk(k, here)
    walk(tree, Location())
    want = {f"D121_TRUNNION_RETAINER_M2X3_PAN_{d:g}" for d in T["screw_deg"]}
    cut_ok = abs(C.volume(leaves.get("pitch_trunnion_retainer", plate_old)) - C.volume(plate)) < 1e-3
    r.check("droid_entry_applies_d121", want <= set(leaves) and not (set(old) & set(leaves)) and cut_ok,
            missing=sorted(want - set(leaves)), still_present=sorted(set(old) & set(leaves)), retainer_cut=cut_ok)

    # --- Mass ------------------------------------------------------------------------
    g_new = STEEL * sum(C.volume(s) for s in new.values())
    g_old = STEEL * sum(C.volume(s) for s in old.values())
    r.check("mass_delta_small", abs(g_new - g_old - removed) <= .5, pan_g=g_new, button_g=g_old,
            plate_removed_g=removed, delta_g=g_new - g_old - removed)
    r.finish()


if __name__ == "__main__":
    main()
