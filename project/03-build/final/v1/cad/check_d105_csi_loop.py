"""D-105: the camera ribbon's free loop behind the head, its bracket and both static runs.

Builds the head from 03-head/v1/cad (catalog off) with the D-104 and D-105 droid edits
in the head's local frame (makad-v1.step.py: d104_local, d105_local), and measures:

- the loop: its shape at every pitch of the clamped envelope as a planar elastica
  (ribbon_elastica.py; fixed length, both clamp headings, own weight at three
  stiffnesses), the smallest bend radius against the 15 mm target, the twist from
  roll, and the strip's clearance to the posed head, the bracket and the yaw parts
  at each roll x pitch pose;
- the bracket: on the disc top, clear of the yaw-frame parts and PCB-16, inserts in
  the disc plate, clear of the moving head over the envelope, and clear of the body
  over a full yaw turn (box survey of the body and chassis, as check_d095_mass.py);
- the joiner (a fourth PCB-14 rev A STEP) seated on the cradle, J1's mouth facing the
  loop clamp, J2's facing the static fold reserve;
- the head end: clamp and screws on the rear cover, the cover slot and inserts, the
  slotted roof guide replacing the round one, the inside runs clear of the roll-frame
  parts and, over the envelope, of the pitch- and yaw-frame parts;
- the static FFC reserves on the disc and bracket: clear of the yaw parts, PCB-16,
  the D-104 bundle reserves, and of the moving head;
- cable lengths against the 300 mm standard-mini, and mass and tipping with the
  bracket swept round the yaw axis (check_batch_mass.py's register state).

Run from this folder with the legacy runtime, PYTHONPATH 03-head/v1/cad first.
"""

import json
import math
from pathlib import Path

import numpy as np
from build123d import Compound
from cadgen.step_scene import import_step

import module_checks as C
import check_d095_mass as D
import check_pcb12_fit as F12
import check_pcb16_fit as F16

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PCB14_STEP = ROOT / "04-pcbs" / "pcb-14-yaw-rotor-joiner" / "cad" / "pcb-14-yaw-rotor-joiner-revA.step"
LEG, SADDLE, DISC = "yaw_yoke_leg_-55", "connected_pitch_frame_roll_servo_saddle", "yaw_turntable_disc_flush"
COVER, GUIDE, CRADLE = "removable_octagonal_rear_cover", "CSI_roof_straight_exit_guide", "connected_rolling_cradle_flange_ear_stalks"
OLD = ("pitch_trunnion_D6x12_pin", "pitch_trunnion_bearing_MR106ZZ", "pitch_trunnion_retainer",
       "pitch_trunnion_retainer_M2x4_240", "pitch_trunnion_retainer_M2x4_300", GUIDE)
R_TARGET = 15.0
Q = 4.7e-5                 # N/mm, 0.3 mm FFC with copper (E)
EI = (50.0, 100.0, 200.0)  # N mm^2 (E range)
CF, PETG = 1.55, D.PETG_BODY
STANDARD_MINI_MM = 300.0


def main():
    entry = C.load_entry()
    import layout_model as m
    import motion_envelope as env
    parts = m.build_parts(catalog=False)
    C.log("head parts built")
    shapes = {n: d["shape"] for n, d in parts.items() if d["kind"] == "physical" and n not in OLD + F12.REMOVED}
    frames = {n: d["frame"] for n, d in parts.items()}
    r = C.Report("check_d105_csi_loop")
    P = entry.D105

    # Droid edits in the head frame (D-102/103/104 and D-105); keep the D-104 parts before for the mass rows.
    d104_before = {n: parts[n]["shape"] for n in (LEG, SADDLE) + OLD[:5]}
    shapes[LEG] = shapes[LEG] - entry.d104_local("leg_cut")
    for sh in entry.d104_local("leg_fill"):
        shapes[LEG] = shapes[LEG] + sh
    shapes[SADDLE] = shapes[SADDLE] - entry.d104_local("boss_cut") + entry.d104_local("boss")
    for sh in entry.pcb12_local("pocket"):
        shapes[CRADLE] = shapes[CRADLE] - sh
    for sh in entry.pcb12_local("boss"):
        shapes[CRADLE] = shapes[CRADLE] + sh
    for sh in entry.pcb16_local("pocket"):
        shapes[DISC] = shapes[DISC] - sh
    cover0 = shapes[COVER]
    shapes[COVER] = cover0 - entry.d105_local("cover_cut")
    for sh in entry.d105_local("disc_pockets"):
        shapes[DISC] = shapes[DISC] - sh
    new_r = {"CSI_LOOP_HEAD_CLAMP": entry.d105_local("head_clamp"), "CSI_LOOP_HEAD_CLAMP_JAW": entry.d105_local("head_jaw"),
             "CSI_ROOF_FFC_GUIDE": entry.d105_local("guide"),
             **{f"CSI_LOOP_HEAD_CLAMP_M2X6_{k}": s for k, s in enumerate(entry.d105_local("head_screws"), 1)}}
    new_y = {"CSI_LOOP_MAST_BASE": entry.d105_local("mast_base"), "CSI_LOOP_MAST_TOP": entry.d105_local("mast_top"),
             **{f"CSI_LOOP_MAST_TUBE_{k}": s for k, s in enumerate(entry.d105_local("tubes"), 1)},
             **{f"CSI_LOOP_MAST_M2X6_{k}": s for k, s in enumerate(entry.d105_local("mast_screws"), 1)}}
    st = import_step(str(PCB14_STEP))
    jloc = entry.d105_joiner_location()
    joiner = {f"CSI_JOINER_{c.label if c.label in ('J1', 'J2') else 'BOARD'}": c.moved(jloc) for c in st.children if c.solids()}
    new_y.update(joiner)
    static_res = dict(entry.d105_local("static_reserves"))
    head_res = dict(entry.d105_local("head_reserves"))
    d104_res = {n: s for n, f, s in entry.d104_local("reserves") if f == "Y"}
    d104_y = {"PITCH_TRUNNION_D104_TUBE_10X1": entry.d104_local("tube"), "PITCH_TRUNNION_D104_TUBE_PLUG": entry.d104_local("plug")}
    s16 = import_step(str(F16.STEP))
    pcb16 = {f"PCB16_{c.label}": c.moved(F16.board_location()) for c in s16.children if c.solids()}
    pcb16.update({f"PCB16_screw_{k}": s for k, s in enumerate(entry.pcb16_local("screws"), 1)})
    pcb16_res = {n: C.blk(b) for n, b in entry.PCB16_RESERVES.items()}
    C.log("D-105 parts built")

    def hits(subject, pool, skip=()):
        sbx = C._box(subject)
        out = []
        for n, s in pool.items():
            if n in skip or not C._hit(sbx, C._box(s)):
                continue
            v = C.common(subject, s)
            if v > 1e-3:
                out.append((n, round(v, 4)))
        return out

    def pose(s, frame, roll, pitch):
        if frame == "R":
            s = s.rotate(m.ROLL_AXIS, roll)
        if frame in "RP":
            s = s.rotate(m.PITCH_AXIS, pitch)
        return s

    yaw_parts = {n: s for n, s in shapes.items() if frames[n] not in ("P", "R")}
    head_movers = {n: (s, frames[n]) for n, s in shapes.items() if frames[n] in ("P", "R")}
    head_movers.update({n: (s, "R") for n, s in new_r.items()})

    # 1. Loop shape over pitch at three stiffnesses.
    pitches = sorted(set(np.round(np.arange(m.PITCH_STOP[0], m.PITCH_STOP[1] + 0.01, 2.0), 3)) | {0.0})
    loops, shape_rows = {}, {}
    for ei in EI:
        sols = {}
        for side in (1, -1):
            guess = None
            for p in sorted([p for p in pitches if p * side >= 0], key=abs):
                pts, th, k, ok = entry.d105_loop(p, q_over_ei=Q / ei, guess=guess)
                sols[p] = (pts, k, ok)
                guess = th if ok else None
        loops[ei] = sols
        shape_rows[ei] = dict(converged=all(v[2] for v in sols.values()),
                              r_min_mm=round(min(1 / v[1] for v in sols.values()), 2),
                              at_pitch=min(sols, key=lambda p: 1 / sols[p][1]),
                              rearmost_x=round(min(v[0][:, 0].min() for v in sols.values()), 1),
                              lowest_z=round(min(v[0][:, 1].min() for v in sols.values()), 1))
    rmin = min(v["r_min_mm"] for v in shape_rows.values())
    free = P["loop"]["length"]
    r.check("loop_bend_radius_at_every_pitch", all(v["converged"] for v in shape_rows.values()) and rmin >= R_TARGET - 0.1,
            target_mm=R_TARGET, by_stiffness_N_mm2=shape_rows, pitches=len(pitches),
            strain_at_r_min=round(P["ribbon"]["t"] / (2 * rmin), 4),
            roll_twist_deg_per_mm=round(2 * m.ROLL_STOP[1] / free, 3),
            note="the head clamp lies on the roll axis heading along it, so roll only twists the free length")

    # 2. Loop strip clearance at each roll x pitch pose (EI 100 shape; roll twists the head end only).
    grid = env.grid_poses(env.load(), [m.ROLL_STOP[0], -10, 0, 10, m.ROLL_STOP[1]], [p for p in pitches if abs(p % 6) < 1e-6 or p in (m.PITCH_STOP[0], m.PITCH_STOP[1])])
    yaw_pool = {**yaw_parts, **new_y, **pcb16}
    loop_hits, nearest, by_pose = [], {}, []
    for roll, pitch in grid:
        p_near = min(loops[100.0], key=lambda q: abs(q - pitch))
        strip = entry.d105_strip(loops[100.0][p_near][0][2:-2])     # the ends sit in the clamps
        sb = C._box(strip)
        worst = (99.0, None)
        for n, (s, f) in head_movers.items():
            ps = pose(s, f, roll, pitch)
            pb = C._box(ps)
            if not C._hit(sb, pb, 6.0):
                continue
            v = C.common(strip, ps) if C._hit(sb, pb) else 0.0
            if v > 1e-3:
                loop_hits.append(dict(pose=(roll, pitch), part=n, mm3=round(v, 4)))
            d = C.distance(strip, ps)
            if d < worst[0]:
                worst = (round(d, 2), n)
        for n, s in yaw_pool.items():
            if n in ("CSI_LOOP_MAST_TOP",):
                continue
            if not C._hit(sb, C._box(s), 6.0):
                continue
            v = C.common(strip, s)
            if v > 1e-3:
                loop_hits.append(dict(pose=(roll, pitch), part=n, mm3=round(v, 4)))
            d = C.distance(strip, s)
            if d < nearest.get(n, (99,))[0]:
                nearest[n] = (round(d, 2), (roll, pitch))
        by_pose.append(((roll, pitch), worst))
    head_worst = min(by_pose, key=lambda x: x[1][0])
    top_gap = round(C.distance(entry.d105_strip(loops[100.0][0.0][0][4:]), new_y["CSI_LOOP_MAST_TOP"]), 3)
    r.check("loop_clear_of_head_bracket_and_yaw_parts", not loop_hits, poses=len(grid), clashes=loop_hits[:20],
            nearest_head=dict(pose=head_worst[0], gap_mm=head_worst[1][0], part=head_worst[1][1]),
            nearest_yaw={k: v for k, v in sorted(nearest.items(), key=lambda kv: kv[1][0])[:6]},
            free_strip_to_bracket_top_mm=top_gap)

    # 3. Bracket on the disc.
    allowed = {"CSI_LOOP_MAST_BASE": (DISC,)}
    channel_ok = ("HARNESS_HEAD_FFC_CHANNEL", "HARNESS_HEAD_CSI_EXIT_UNROUTED", DISC)   # the fold and run start in D-103's CSI exit
    stat = {k: hits(s, {**yaw_parts, **pcb16, **pcb16_res, **d104_res, **d104_y},
                    skip=allowed.get(k, ()) + ((DISC,) if "M2X6" in k else ())) for k, s in new_y.items()}
    stat.update({k: hits(s, {**yaw_parts, **pcb16, **pcb16_res, **d104_res, **d104_y}, skip=channel_ok if ("45_FOLD" in k or "DISC_RUN" in k) else ())
                 for k, s in static_res.items()})
    tube_seat = {k: round(C.common(s, new_y["CSI_LOOP_MAST_BASE"]) + C.common(s, new_y["CSI_LOOP_MAST_TOP"]), 4)
                 for k, s in new_y.items() if "TUBE" in k}
    bearing = round(C.common(new_y["CSI_LOOP_MAST_BASE"], shapes[DISC]), 4)
    floor = min(C._box(p)[2] for p in entry.d105_local("disc_pockets")) - (m.YAW_DISC_TOP_Z - m.YAW_DISC_PLATE)
    r.check("bracket_and_static_runs_on_the_yaw_frame", not any(stat.values()) and all(v < 1e-3 for v in tube_seat.values())
            and floor >= 0.7, clashes={k: v for k, v in stat.items() if v}, base_into_disc_mm3=bearing,
            tubes_into_sockets_mm3=tube_seat, insert_floor_mm=round(floor, 2),
            note="the foot bears on the disc top; the 45-degree fold lies in the channel mouth")

    # 4. Bracket and static runs clear of the moving head over the envelope.
    group = {**new_y, **static_res}
    sweep, near = [], (99.0, None, None)
    for roll, pitch in grid:
        for n, (s, f) in head_movers.items():
            ps = pose(s, f, roll, pitch)
            pb = C._box(ps)
            for k, g in group.items():
                gb = C._box(g)
                if not C._hit(gb, pb, 3.0):
                    continue
                v = C.common(g, ps) if C._hit(gb, pb) else 0.0
                if v > 1e-3:
                    sweep.append(dict(item=k, part=n, pose=(roll, pitch), mm3=round(v, 4)))
                d = C.distance(g, ps)
                if d < near[0]:
                    near = (round(d, 3), f"{k} / {n}", (roll, pitch))
    r.check("bracket_clear_of_moving_head", not sweep, poses=len(grid), clashes=sweep[:20], nearest=near)

    # 5. Bracket over the body through a full yaw turn (body + chassis boxes, conservative).
    ent, tree, leaves = C.droid_tree(entry, with_modules=True)
    ox, oy, oz = entry.HEAD_ORIGIN_IN_CHASSIS
    ax_w, ay_w = ox + m.PITCH_X, oy
    mast_pts = []
    for s in [new_y["CSI_LOOP_MAST_BASE"], new_y["CSI_LOOP_MAST_TOP"]] + [s for k, s in new_y.items() if "TUBE" in k]:
        b = C._box(s)
        mast_pts += [(x, y, b[2]) for x in (b[0], b[3]) for y in (b[1], b[4])]
    r_out = max(math.hypot(x - m.PITCH_X, y) for x, y, _ in mast_pts)
    low_w = min(z for _, _, z in mast_pts) + oz
    worst_body = (-1e9, None)
    for lf in leaves:
        x0, y0, z0, x1, y1, z1 = lf.box
        cx, cy = min(max(ax_w, x0), x1), min(max(ay_w, y0), y1)
        if math.hypot(cx - ax_w, cy - ay_w) > r_out + 1.0:
            continue
        far = max(math.hypot(x - ax_w, y - ay_w) for x in (x0, x1) for y in (y0, y1))
        if far < 63.0:   # inside the disc rim: under the disc, not reached by the arm
            continue
        if z1 > worst_body[0]:
            worst_body = (round(z1, 2), lf.label)
    gap = round(low_w - worst_body[0], 2)
    r.check("bracket_clear_of_body_over_yaw", gap >= 3.0, bracket_lowest_world_z=round(low_w, 2),
            bracket_radius_from_yaw_axis_mm=round(r_out, 1), highest_body_part_in_ring=worst_body, gap_mm=gap,
            method="body and chassis leaf boxes reaching beyond the disc rim (r > 63) inside the bracket radius; any yaw")

    # 6. Joiner in the cradle.
    jb = {k: round(C.common(s, new_y["CSI_LOOP_MAST_TOP"]), 4) for k, s in joiner.items()}
    seat = round(C.distance(joiner["CSI_JOINER_BOARD"], new_y["CSI_LOOP_MAST_TOP"]), 3)
    o, d, n = entry._d105_frame()

    def u_of(shape):
        b = C._box(shape)
        c = ((b[0] + b[3]) / 2, (b[2] + b[5]) / 2)
        return (c[0] - o[0]) * d[0] + (c[1] - o[2]) * d[2]
    r.check("joiner_seated_mouths_facing_the_runs", not any(v > 1e-3 for v in jb.values()) and seat < 0.1
            and u_of(joiner["CSI_JOINER_J1"]) < u_of(joiner["CSI_JOINER_J2"]),
            overlaps_mm3=jb, board_to_cradle_mm=seat, j1_u_mm=round(u_of(joiner["CSI_JOINER_J1"]), 2),
            j2_u_mm=round(u_of(joiner["CSI_JOINER_J2"]), 2), clamp_u=P["clamp"]["u"],
            note="J1 (mouth -u) takes the loop cable 2.5 mm past the clamp; J2 (mouth +u) the static FFC")

    # 7. Head end.
    clamp = new_r["CSI_LOOP_HEAD_CLAMP"]
    r_static = {n: s for n, s in shapes.items() if frames[n] == "R"}
    hr = {k: hits(s, r_static, skip=(COVER,) if "CLAMP" in k else ()) for k, s in {**new_r, **head_res}.items()}
    hr.update({k: hits(s, {kk: vv for kk, vv in new_r.items() if kk != k and "M2X6" not in kk}) for k, s in new_r.items() if "M2X6" in k})
    cover_contact = round(C.distance(clamp, shapes[COVER]), 3)
    slot_left = round(C.common(shapes[COVER], head_res["HARNESS_D105_CSI_ROOF_RUN"]), 4)
    in_floor = round((P["loop"]["head"][1] - P["head_clamp"]["slot_t"] / 2 - P["head_clamp"]["insert_depth"]) - P["head_clamp"]["z"][0], 2)
    jaw_fit = round(C.common(new_r["CSI_LOOP_HEAD_CLAMP"], new_r["CSI_LOOP_HEAD_CLAMP_JAW"]), 4)
    screw_in = [round(C.common(sc, new_r["CSI_LOOP_HEAD_CLAMP_JAW"]), 3) for k, sc in new_r.items() if "M2X6" in k]
    roof = round(C.distance(new_r["CSI_ROOF_FFC_GUIDE"], shapes["main_octagonal_skin"]), 3)
    r.check("head_clamp_cover_slot_and_inside_runs", not any(hr.values()) and cover_contact < 0.05 and in_floor >= 0.7 and jaw_fit < 1e-3,
            clashes={k: v for k, v in hr.items() if v}, clamp_to_cover_mm=cover_contact, cover_left_in_run_mm3=slot_left,
            clamp_insert_floor_mm=in_floor, jaw_into_base_mm3=jaw_fit, guide_to_roof_mm=roof,
            note="the clamp is bonded to the 1.6 mm cover (no cover inserts: the roll servo sweeps behind it); its two M2 pinch the ribbon "
                 "into inserts in its own lower jaw; the round CSI_roof_straight_exit_guide is replaced by a slotted one")
    rel = {**{k: (s, "R") for k, s in head_res.items()}, "CSI_ROOF_FFC_GUIDE": (new_r["CSI_ROOF_FFC_GUIDE"], "R")}
    inside, inside_near = [], (99.0, None, None)
    others = {n: (s, frames[n]) for n, s in shapes.items() if frames[n] in ("P", "Y")}
    for roll, pitch in grid:
        for k, (s, f) in rel.items():
            ps = pose(s, f, roll, pitch)
            pb = C._box(ps)
            for n, (o_, fo) in others.items():
                po = pose(o_, fo, roll, pitch)
                ob = C._box(po)
                if not C._hit(pb, ob, 3.0):
                    continue
                v = C.common(ps, po) if C._hit(pb, ob) else 0.0
                if v > 1e-3:
                    inside.append(dict(item=k, part=n, pose=(roll, pitch), mm3=round(v, 4)))
                dd = C.distance(ps, po)
                if dd < inside_near[0]:
                    inside_near = (round(dd, 3), f"{k} / {n}", (roll, pitch))
    r.check("inside_runs_clear_over_the_envelope", not inside, poses=len(grid), clashes=inside[:20], nearest=inside_near)

    # 8. Cable lengths.
    lp = P["loop"]
    inside_len = (P["cover_slot_z"][1] - lp["head"][1]) + (P["roof_run"]["x"][1] - P["roof_run"]["x"][0]) + 15.0
    loop_cable = 2.5 + (P["clamp"]["u"][1] - P["clamp"]["u"][0]) + lp["length"] + (P["head_clamp"]["x"][1] - P["head_clamp"]["x"][0]) + inside_len
    sr = entry.D105_STATIC_RESERVES
    static_len = 45.0 + (sr["HARNESS_D105_CSI_DISC_RUN"][1] - sr["HARNESS_D105_CSI_ARM_RUN"][0]) + \
        (sr["HARNESS_D105_CSI_CLIMB"][5] - sr["HARNESS_D105_CSI_CLIMB"][4]) + 45.0
    r.check("cable_lengths", loop_cable <= STANDARD_MINI_MM, loop_cable_mm=round(loop_cable, 1),
            standard_mini_mm=STANDARD_MINI_MM, static_ffc_mm_E=round(static_len, 0),
            note="loop cable = joiner mouth to camera exit reserve (+15 mm into the camera); static = PCB-14 board 1 "
                 "to the bracket joiner incl. bore/channel (45, E) and top folds (45, E); slack goes in the roof run")

    # 9. Mass and tipping.
    import body_v1_model as M
    rep95 = {x["check"]: x for x in json.loads((HERE / "check_d095_mass-report.json").read_text())["rows"]}
    repb = {x["check"]: x for x in json.loads((HERE / "check_batch_mass-report.json").read_text())["rows"]}
    removed = {nm for nm, _ in rep95["removed_rows"]["rows"]}
    rows = [(nm, g, tuple(c)) for nm, g, c, _ in M.MASS_ROWS if nm not in removed]
    rows += [(nm, g, tuple(c)) for nm, g, c, _ in rep95["added_rows"]["rows"]]
    rows += [(nm, g, tuple(c)) for nm, g, c, _ in repb["batch_rows"]["rows"]]
    before = D.tip(rows, M)

    def w(c):
        return (c[0] + ox, c[1] + oy, c[2] + oz)
    yaw_rows = []
    for k, s in new_y.items():
        v, c = D.centroid(s)
        rho = CF if "TUBE" in k else (D.STEEL if "M2X6" in k else (1.85 if "BOARD" in k else (1.3 if k.endswith(("J1", "J2")) else PETG)))
        yaw_rows.append((k, v * rho / 1000.0, w(c)))
    # D-104 (hollow trunnion) measured deltas, carried with the head (neutral pose).
    d104_rows = []
    for k, rho in ((LEG, PETG), (SADDLE, PETG)):
        v0, c0 = D.centroid(d104_before[k])
        v1, c1 = D.centroid(shapes[k])
        dv = v1 - v0
        c = tuple((v1 * c1[i] - v0 * c0[i]) / dv for i in range(3)) if abs(dv) > 1e-3 else c1
        d104_rows.append((f"D104_{k}_volume_change", dv * rho / 1000.0, w(c)))
    for k, rho in (("pitch_trunnion_D6x12_pin", D.STEEL), ("pitch_trunnion_retainer", PETG),
                   ("pitch_trunnion_retainer_M2x4_240", D.STEEL), ("pitch_trunnion_retainer_M2x4_300", D.STEEL)):
        v, c = D.centroid(d104_before[k])
        d104_rows.append((f"D104_removed_{k}", -v * rho / 1000.0, w(c)))
    vb, cb = D.centroid(d104_before["pitch_trunnion_bearing_MR106ZZ"])
    d104_rows.append(("D104_removed_MR106ZZ", -1.1, w(cb)))            # E catalogue mass
    vt, ct = D.centroid(entry.d104_local("tube"))
    d104_rows.append(("D104_TUBE_10X1_6063", vt * 2.70 / 1000.0, w(ct)))
    vp, cp = D.centroid(entry.d104_local("plug"))
    d104_rows.append(("D104_TUBE_PLUG", vp * PETG / 1000.0, w(cp)))
    vb2, cb2 = D.centroid(entry.d104_local("bearing"))
    d104_rows.append(("D104_6700_2Z", 2.2, w(cb2)))                    # E catalogue mass
    yaw_rows += [("CSI_LOOP_MAST_INSERTS_M2X3", 4 * 0.10, w((-98.0, 1.0, -36.0))),
                 ("CSI_STATIC_FFC_22W", 0.0048 * static_len, w((-100.0, 28.0, 20.0)))]
    head_rows = []
    for k, s in new_r.items():
        v, c = D.centroid(s)
        head_rows.append((k, v * (D.STEEL if "M2X6" in k else PETG) / 1000.0, w(c)))
    head_rows += [("CSI_LOOP_HEAD_CLAMP_INSERTS", 2 * 0.10, w((-113.4, -1.0, 48.2))),
                  ("CSI_STANDARD_MINI_CABLE", 0.0048 * loop_cable, w((-120.0, -1.0, 70.0)))]
    bal = entry.D105_BALLAST
    bal_row = [("BALLAST_BAR_COPPER_C110_DELTA", M.BALLAST_BAR_G * (bal["density"] / bal["was_density"] - 1.0),
                (sum(M.BALLAST_X) / 2.0, 0.0, sum(M.BALLAST_Z) / 2.0))]
    steel_rows = rows + yaw_rows + head_rows + d104_rows
    now_steel = D.tip(steel_rows, M)
    now_rows = steel_rows + bal_row
    now = D.tip(now_rows, M)
    # The bracket turns with the head: sweep yaw for the bracket and the head together.
    total = now["mass_g"]
    x, y, z = now["com_mm"]
    head_tree = json.loads((M.HEAD_DIR / "mass-placement.json").read_text())
    pitch_w, roll_w, axes = head_tree["working"]["pitch"], head_tree["working"]["roll"], head_tree["axes"]
    pr = (2 * pitch_w["mass_g"] * math.hypot(pitch_w["center_mm"][0] - axes["pitch_x"], pitch_w["center_mm"][2] - axes["pitch_z"])
          + 2 * roll_w["mass_g"] * math.hypot(roll_w["center_mm"][1] - axes["roll_y"], roll_w["center_mm"][2] - axes["roll_z"])) / total
    th_h = math.atan2(M.HEAD_LOCAL_COM[1], M.HEAD_LOCAL_COM[0] - M.HEAD_LOCAL_YAW[0])
    r_h = math.hypot(M.HEAD_LOCAL_COM[0] - M.HEAD_LOCAL_YAW[0], M.HEAD_LOCAL_COM[1])
    yawed = [(g, math.atan2(c[1] - ay_w, c[0] - ax_w), math.hypot(c[0] - ax_w, c[1] - ay_w)) for _, g, c in yaw_rows + head_rows + d104_rows]

    def sweep(xc, zc, tot):
        best = (1e9, None)
        for psi in np.arange(0, 360, 2.0):
            ps = math.radians(psi)
            dx = M.HEAD_MASS_G * r_h * (math.cos(th_h + ps) - math.cos(th_h))
            dx += sum(g * rr * (math.cos(th + ps) - math.cos(th)) for g, th, rr in yawed)
            a = 9.81 * (xc + dx / tot - pr) / (zc + pr)
            if a < best[0]:
                best = (round(a, 4), float(psi))
        return best
    worst = sweep(x, z, total)
    worst_steel = sweep(now_steel["com_mm"][0], now_steel["com_mm"][2], now_steel["mass_g"])
    d105_g = round(sum(g for _, g, _ in yaw_rows + head_rows), 2)
    d104_g = round(sum(g for _, g, _ in d104_rows), 2)
    r.check("mass_and_tipping", now["a_tip"] >= D.A_TIP_MIN and worst[0] >= D.A_TIP_MIN * 1.015,
            d105_added_g=d105_g, bracket_g=round(sum(g for _, g, _ in yaw_rows), 2), d104_net_g=d104_g,
            d104_rows=[(k, round(g, 3), [round(v, 1) for v in c]) for k, g, c in d104_rows],
            ballast=dict(material=bal["material"], added_g=round(bal_row[0][1], 2),
                         worst_yaw_a_tip_with_steel_bar=worst_steel[0], neutral_with_steel_bar=round(now_steel["a_tip"], 4)),
            margin_pct=round(100 * (worst[0] / D.A_TIP_MIN - 1), 2),
            rows=[(k, round(g, 3), [round(v, 1) for v in c]) for k, g, c in yaw_rows + head_rows],
            a_tip_neutral=round(now["a_tip"], 4), a_tip_neutral_before=round(before["a_tip"], 4),
            worst_yaw_a_tip=worst[0], at_yaw_deg=worst[1], d095_worst_before=round(before["worst_pose_a_tip"], 4),
            minimum=round(D.A_TIP_MIN, 4),
            note="worst pose: head pitch/roll offsets as check_d095_mass.tip (head working masses from mass-placement.json, not re-solved), "
                 "with the head, the D-104 deltas and the yaw-carried bracket swept together over yaw")
    r.finish()


if __name__ == "__main__":
    main()
