"""D-120 roll output: Probots 25T horn + turned hub collar in place of the goBILDA coupler.

Builds the head parts (catalog off), drops the coupler and its M4 clamp, cuts the
spindle's rear flat and adds the D-120 parts from d120_roll_horn_hub, then checks:

- interface facts: horn on the spline (0.3 off the boss, engagement), the centre
  screw unchanged and passing the collar bore, M2 screw thread and tips, M2 heads
  beside the horn hub, spindle in the bore, set screws on the flat;
- no interference at neutral with any head part except the designed contacts;
- a roll sweep (stop to stop, 1.5 deg) of the new parts against every pitch-frame
  part: >= 0.99 mm (D-049 rule) except the horn hub's designed 0.3 mm boss gap;
  a roll x pitch grid against the yaw-frame parts;
- straight hex-key paths to both set screws from +Y at neutral;
- the edits applied through the droid entry to the real head tree;
- mass against the coupler and clamp.

Run from this folder with the legacy runtime; PYTHONPATH = 03-head/v1/cad first,
MAKAD_RELIEF_SERIAL=1 (see ../README.md). About 5 min.
"""
import re
from build123d import Compound, Location
import module_checks as C
import d120_roll_horn_hub as D

STEEL, ALU = 7.9e-3, 2.70e-3


def main():
    entry = C.load_entry()
    import layout_model as m
    import feetech as fe
    import motion_envelope as env
    from inspection_scene import parts_scene
    parts = m.build_parts(catalog=False)
    C.log("head parts built")
    r = C.Report("check_d120_roll_coupler")
    shapes = {n: d["shape"] for n, d in parts.items() if d["kind"] == "physical"}
    frames = {n: d["frame"] for n, d in parts.items()}
    old = {n: shapes.pop(n) for n in list(shapes) if any(re.fullmatch(p, n) for p in D.REMOVES)}
    shapes["rolling_spindle_6mm"] = shapes["rolling_spindle_6mm"] - D.spindle_flat_tool()
    new = {"horn": D.horn(), "collar": D.collar()}
    new.update({f"m2_{k:g}": s for k, s in D.horn_screws().items()})
    new.update({f"set_{i}": s for i, s in enumerate(D.set_screws(), 1)})
    r.check("removed_coupler_and_clamp", len(old) == 2, removed=sorted(old))
    r.check("new_parts_valid_single_solids", all(s.is_valid and len(s.solids()) == 1 for s in new.values()),
            parts={k: [bool(s.is_valid), len(s.solids())] for k, s in new.items()})

    # --- Interface facts --------------------------------------------------
    boss_top = fe.ROLL_CASE_BOTTOM_X + fe.BOSS_TOP
    spline_top = fe.ROLL_CASE_BOTTOM_X + fe.SPLINE_TOP
    r.check("horn_hub_to_boss_mm", abs(D.HORN_HUB_X - boss_top - .3) < 1e-6, gap=D.HORN_HUB_X - boss_top)
    eng = spline_top - D.HORN_HUB_X
    r.check("horn_spline_engagement_mm", eng >= 2.9, engagement=eng, goBILDA_was=2.9)
    cs = C._box(shapes["roll_coupler_centre_M3x5"])
    r.check("centre_screw_seat_on_horn_web", abs(cs[0] + 3 - D.HORN_DISC_X[1]) < 1e-6 or abs(cs[3] - 3 - D.HORN_DISC_X[1]) < 1e-6,
            seat_x=D.HORN_DISC_X[1], screw_box_x=(cs[0], cs[3]))
    r.check("centre_screw_thread_in_output_mm", abs(spline_top - cs[0] - 3.8) < .05, thread=spline_top - cs[0])
    r.check("centre_screw_head_passes_collar_bore", D.COLLAR["bore_r"] - 2.75 >= .2, radial_gap=D.COLLAR["bore_r"] - 2.75)
    m2_tip = D.HORN_DISC_X[0] + D.M2X6
    r.check("m2_thread_in_flange_mm", m2_tip - D.HORN_DISC_X[1] >= 3.5 and m2_tip <= D.FLANGE_FRONT_X + 1e-6,
            thread=m2_tip - D.HORN_DISC_X[1], tip_x=m2_tip, flange_front_x=D.FLANGE_FRONT_X)
    hub_gap = fe.HORN["pcd_r"] - 1.75 - fe.HORN["hub_r"]
    r.check("m2_heads_beside_horn_hub_mm", hub_gap >= .2, radial_gap=hub_gap,
            note="E: Probots hub diameter not published; measure <= 10.4 mm on receipt")
    head_to_case = D.HORN_DISC_X[0] - 1.3 - (fe.ROLL_CASE_BOTTOM_X + fe.CASE_H)
    r.check("m2_heads_above_case_top_mm", head_to_case >= .99, gap=head_to_case)
    sp = C._box(shapes["rolling_spindle_6mm"])
    r.check("spindle_in_collar_bore_mm", D.COLLAR_X[1] - sp[0] >= 8.5, engagement=D.COLLAR_X[1] - sp[0])
    fx0, fx1 = D.SPINDLE_FLAT["x"]
    margins = [min(x - 1.5 - fx0, fx1 - (x + 1.5)) for x in D.COLLAR["set_x"]]
    rear_bearing_face = min(fe.ROLL_BEARING_X) - 2.5
    r.check("set_screws_on_flat", min(margins) >= .4 and fx1 <= D.COLLAR_X[1] - .3 and fx1 <= rear_bearing_face - 2,
            screw_edge_margins=margins, flat_x=(fx0, fx1), flat_end_inside_collar=D.COLLAR_X[1] - fx1,
            flat_to_rear_bearing=rear_bearing_face - fx1)
    tips = [C.distance(s, shapes["rolling_spindle_6mm"]) for s in D.set_screws()]
    outer = [C._box(s)[4] for s in D.set_screws()]
    r.check("set_screw_tips_on_flat_and_recessed", max(tips) < 1e-3 and max(outer) <= m.ROLL_Y + D.COLLAR["shaft_r"] - .3,
            tip_gaps=tips, recess=[m.ROLL_Y + D.COLLAR["shaft_r"] - o for o in outer])

    # --- Static interference at neutral ------------------------------------
    servo = shapes["roll_STS3045M_reference"] - m.axial(fe.HORN["bore_r"] + .01, 10., (boss_top + 5, m.ROLL_Y, m.ROLL_Z))
    pool = dict(shapes, roll_STS3045M_reference=servo)
    allowed = {("horn", "roll_coupler_centre_M3x5"), ("collar", "rolling_spindle_6mm")} | \
              {(k, "rolling_spindle_6mm") for k in new if k.startswith("set_")}
    clashes, nearest = [], (99., None, None)
    for k, s in new.items():
        for n, t in pool.items():
            if not C._hit(C._box(s), C._box(t), 3.):
                continue
            v = C.common(s, t) if C._hit(C._box(s), C._box(t)) else 0.
            if v > 1e-3 and (k, n) not in allowed:
                clashes.append((k, n, round(v, 4)))
            if (k, n) not in allowed and frames.get(n) != "R":
                d = C.distance(s, t)
                if d < nearest[0]:
                    nearest = (round(d, 3), k, n)
    inner = [(a, b, round(C.common(new[a], new[b]), 4)) for a in new for b in new if a < b
             and C._hit(C._box(new[a]), C._box(new[b])) and C.common(new[a], new[b]) > 1e-3]
    r.check("no_interference_at_neutral", not clashes and not inner, clashes=clashes, between_new_parts=inner,
            nearest_non_roll_part=nearest)

    # --- Motion -------------------------------------------------------------
    movers = Compound(children=list(new.values()))
    rolls = [m.ROLL_STOP[0] + 1.5 * i for i in range(int(round((m.ROLL_STOP[1] - m.ROLL_STOP[0]) / 1.5)) + 1)]
    p_parts = {n: t for n, t in pool.items() if frames[n] == "P"}
    hub_only = Compound(children=[new["horn"]])
    worst, hits, boss = (99., None, None), [], 99.
    for roll in rolls:
        mv = movers.rotate(m.ROLL_AXIS, roll)
        for n, t in p_parts.items():
            if not C._hit(C._box(mv), C._box(t), 2.):
                continue
            if C._hit(C._box(mv), C._box(t)) and C.common(mv, t) > 1e-3:
                hits.append((roll, n))
            if n == "roll_STS3045M_reference":
                boss = min(boss, C.distance(hub_only.rotate(m.ROLL_AXIS, roll), t))
                rest = Compound(children=[s for k, s in new.items() if k != "horn"]).rotate(m.ROLL_AXIS, roll)
                d = C.distance(rest, t)
            else:
                d = C.distance(mv, t)
            if d < worst[0]:
                worst = (round(d, 3), n, roll)
    r.check("roll_sweep_vs_pitch_frame", not hits and worst[0] >= .99 and boss >= .29, poses=len(rolls),
            clashes=hits[:10], nearest=worst, horn_to_servo_min=round(boss, 3))
    poses = env.grid_poses(env.load(), [m.ROLL_STOP[0], -10, 0, 10, m.ROLL_STOP[1]],
                           [m.PITCH_STOP[0], -15, 0, 15, m.PITCH_STOP[1]])
    y_parts = {n: t for n, t in pool.items() if frames[n] == "Y"}
    yw, yhits = (99., None, None), []
    for roll, pitch in poses:
        mv = movers.rotate(m.ROLL_AXIS, roll).rotate(m.PITCH_AXIS, pitch)
        for n, t in y_parts.items():
            if C._hit(C._box(mv), C._box(t), 3.):
                if C._hit(C._box(mv), C._box(t)) and C.common(mv, t) > 1e-3:
                    yhits.append(((roll, pitch), n))
                d = C.distance(mv, t)
                if d < yw[0]:
                    yw = (round(d, 3), n, (roll, pitch))
    r.check("roll_pitch_grid_vs_yaw_frame", not yhits and yw[0] >= .99, poses=len(poses), clashes=yhits[:10],
            nearest_within_3mm=yw)

    # --- Set-screw key paths -------------------------------------------------
    blocked = []
    for x in D.COLLAR["set_x"]:
        path = m.block(x - 1.5, x + 1.5, m.ROLL_Y + D.COLLAR["shaft_r"] + .05, m.ROLL_Y + 60., m.ROLL_Z - 1.5, m.ROLL_Z + 1.5)
        for n, t in pool.items():
            if C._hit(C._box(path), C._box(t)) and C.common(path, t) > 1e-3:
                blocked.append((x, n))
    r.check("set_screw_key_paths_clear_from_plus_y", not blocked, blocked=blocked, path="3 x 3 mm, collar face to +60 mm")

    # --- Through the droid entry ---------------------------------------------
    head = Compound(label="Head v1", children=[*parts_scene(parts).children]).moved(Location(entry.HEAD_ORIGIN_IN_CHASSIS))
    tree = entry._apply_droid_cuts(Compound(label="t", children=[head]), strict=False)
    labels = set()

    def walk(n):
        kids = list(n.children) if getattr(n, "children", None) else []
        if not kids:
            labels.add(n.label)
        for k in kids:
            walk(k)
    walk(tree)
    want = {"D120_ROLL_HORN_25T_PROBOTS", "D120_ROLL_HUB_COLLAR_6061"} | \
           {f"D120_ROLL_HORN_TO_HUB_M2X6_{d:g}" for d in fe.HORN["holes_deg"]} | {"D120_ROLL_HUB_SET_M3X3_1", "D120_ROLL_HUB_SET_M3X3_2"}
    r.check("droid_entry_applies_d120", want <= labels and not (set(old) & labels),
            missing=sorted(want - labels), still_present=sorted(set(old) & labels))

    # --- Mass ------------------------------------------------------------------
    g_new = ALU * (C.volume(new["horn"]) + C.volume(new["collar"])) + \
        STEEL * sum(C.volume(s) for k, s in new.items() if k.startswith(("m2_", "set_")))
    g_old = ALU * C.volume(old["roll_coupler_goBILDA_4001_0025_0006"]) + STEEL * C.volume(old["roll_coupler_clamp_M4x10"])
    g_flat = 7.85e-3 * C.common(parts["rolling_spindle_6mm"]["shape"], D.spindle_flat_tool())
    delta = g_new - g_old - g_flat
    r.check("mass_delta_small", abs(delta) <= 3., new_g=g_new, coupler_and_clamp_g=g_old, flat_removed_g=g_flat,
            delta_g=delta, collar_g=ALU * C.volume(new["collar"]))
    r.finish()


if __name__ == "__main__":
    main()
