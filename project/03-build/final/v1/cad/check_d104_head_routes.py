"""D-104: the head wire bundle through a hollow -Y trunnion, and its routes.

Builds the head parts from 03-head/v1/cad (catalog off) with the D-102/D-103/D-104
droid edits applied in the head's local frame (makad-v1.step.py: d104_local, the
PCB-12 bosses, the PCB-16 pockets), places PCB-12 and PCB-16 rev A as their fit
checks do, and measures:

- the -Y leg: tube bore and cable channel cut, the D-051 recess filled; the
  channel's designed walls (0.8 mm across, 1.0 mm outboard) lie inside the leg as
  drawn before the cut, away from the intended mouths;
- the trunnion: tube in the pad bore, the window on the channel, the 6700-2Z on
  the tube and in the grown boss, the boss clear of the stop dowel and the leg;
- every new part and yaw-carried reserve clear of the yaw-frame parts and of
  PCB-16 at the neutral pose, except where the bundle is meant to be;
- a roll x pitch grid clamped onto the motion envelope: yaw-carried items against
  the pitch- and roll-frame parts and PCB-12; pitch-frame items (boss, bearing,
  servo branch, PCB-12 branch) against the yaw- and roll-frame parts and PCB-12;
  the roll-frame branch against the yaw- and pitch-frame parts;
- the tube's insertion path from outside the leg and the bundle sizes against the
  reserves.

Run from this folder with the legacy runtime, PYTHONPATH 03-head/v1/cad first.
"""

import math

from build123d import Compound
from cadgen.step_scene import import_step

import module_checks as C
import check_pcb12_fit as F12
import check_pcb16_fit as F16

LEG, SADDLE, DISC = "yaw_yoke_leg_-55", "connected_pitch_frame_roll_servo_saddle", "yaw_turntable_disc_flush"
CRADLE = "connected_rolling_cradle_flange_ear_stalks"
OLD = ("pitch_trunnion_D6x12_pin", "pitch_trunnion_bearing_MR106ZZ", "pitch_trunnion_retainer",
       "pitch_trunnion_retainer_M2x4_240", "pitch_trunnion_retainer_M2x4_300")
BUNDLE = dict(rows=2, width_mm=6.0, thickness_mm=2.2,
              wires="2 x AWG24 silicone (+6V3_HEAD_PR, GND_HEAD; OD 1.4 E), 11 x AWG30 silicone (OD 0.8 E)")


def main():
    entry = C.load_entry()
    import layout_model as m
    import motion_envelope as env
    parts = m.build_parts(catalog=False)
    C.log("head parts built")
    shapes = {n: d["shape"] for n, d in parts.items()
              if d["kind"] == "physical" and n not in OLD + F12.REMOVED}
    frames = {n: d["frame"] for n, d in parts.items()}
    r = C.Report("check_d104_head_routes")
    px, pz = m.PITCH_X, m.PITCH_Z
    D = entry.D104

    # Droid edits in the head frame (cuts before adds, as _cut_parts).
    leg0, saddle0 = shapes[LEG], shapes[SADDLE]
    leg = leg0 - entry.d104_local("leg_cut")
    for sh in entry.d104_local("leg_fill"):
        leg = leg + sh
    saddle = saddle0 - entry.d104_local("boss_cut") + entry.d104_local("boss")
    shapes[LEG], shapes[SADDLE] = leg, saddle
    for sh in entry.pcb12_local("pocket"):
        shapes[CRADLE] = shapes[CRADLE] - sh
    for sh in entry.pcb12_local("boss"):
        shapes[CRADLE] = shapes[CRADLE] + sh
    for sh in entry.pcb16_local("pocket"):
        shapes[DISC] = shapes[DISC] - sh
    tube, plug, brg = entry.d104_local("tube"), entry.d104_local("plug"), entry.d104_local("bearing")
    channel, bore = entry.d104_local("channel"), entry.d104_local("pad_bore")
    reserves = entry.d104_local("reserves")
    res = {n: (f, s) for n, f, s in reserves}

    # PCB-12 (roll frame) and PCB-16 (yaw frame) as their fit checks place them.
    s12 = import_step(str(F12.STEP))
    k12 = {c.label: c for c in s12.children if c.solids()}
    refs = {"U1", "U2", "U3", "U4", "U5", "J1", "J2", "J3", "C1", "C3", "C4", "C5",
            "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R9", "R10"}
    core12 = [c for n, c in k12.items() if n not in refs]
    loc12 = F12.board_location(C._box(core12[0])[5] - C._box(core12[0])[2])
    pcb12 = {f"PCB12_{n}": c.moved(loc12) for n, c in k12.items()}
    s16 = import_step(str(F16.STEP))
    pcb16 = {f"PCB16_{c.label}": c.moved(F16.board_location()) for c in s16.children if c.solids()}
    pcb16.update({f"PCB16_screw_{k}": s for k, s in enumerate(entry.pcb16_local("screws"), 1)})
    C.log("boards placed")

    # 1. Leg edits.
    v0, v1 = C.volume(leg0), C.volume(leg)
    fill = sum(C.volume(s) for s in entry.d104_local("leg_fill"))
    left_in_channel = C.common(leg, channel)
    left_in_bore = C.common(leg, bore)
    r.check("leg_bore_and_channel_cut_recess_filled", left_in_channel < 1e-3 and left_in_bore < 1e-3 and fill > 50,
            leg_volume_before_mm3=round(v0, 1), after_mm3=round(v1, 1), d051_recess_filled_mm3=round(fill, 1),
            leg_left_in_channel_mm3=round(left_in_channel, 4), leg_left_in_bore_mm3=round(left_in_bore, 4))

    # 2. Channel walls: grow each run by the designed wall and measure what leaves the
    # pre-cut leg (with the D-051 recess filled). Mouths are trimmed off each run.
    c = D["channel"]
    x0, x1 = px + c["dx"] - c["w"] / 2, px + c["dx"] + c["w"] / 2
    solid_leg = leg0
    for sh in entry.d104_local("leg_fill"):
        solid_leg = solid_leg + sh
    wall_x, wall_out, wall_in = 0.8, 1.0, 1.0
    knee = (px + c["dx"], pz + c["knee_dz"])
    runs = {
        "vertical": C.blk((x0 - wall_x, x1 + wall_x, c["y"][0] - wall_out, c["y"][1] + wall_in,
                           c["bottom_z"] + 3.5, knee[1])),
        "diagonal": entry._xz_bar(knee, (px + 0.55 * (knee[0] - px), pz + 0.55 * (knee[1] - pz)),
                                  c["w"] + 2 * wall_x, c["y"][0] - wall_out, c["y"][1] + wall_in),
        "tunnel": C.blk((x0 - wall_x, x1 + wall_x, D["tunnel"]["y"][0] - wall_out, D["tunnel"]["y"][1] - 0.6,
                         D["tunnel"]["z"][0] - 0.6, D["tunnel"]["z"][1] + 1.0)),
    }
    outside = {k: round(C.volume(s) - C.common(s, solid_leg), 3) for k, s in runs.items()}
    r.check("channel_walls_inside_the_leg", all(v < 0.05 for v in outside.values()),
            designed_walls_mm=dict(across=wall_x, outboard=wall_out, inboard=wall_in, tunnel_floor_over_key_socket=0.6),
            grown_volume_outside_leg_mm3=outside,
            note="tunnel mouth (inner face), the knee-to-axis run's last 45 % (pad, tube window) are left out")
    key = entry.D104["tunnel"]["z"][0] - (m.YAW_DISC_TOP_Z + m.fe.LEG_KEY["h"] + m.fe.LEG_KEY["top_clear"])
    r.check("tunnel_over_the_key_socket", key >= 0.5, floor_over_socket_mm=round(key, 2),
            key_screws_clear_mm=round(C.distance(C.blk(entry.D104_Y_RESERVES["HARNESS_D104_RISER"]), leg), 3))

    # 3. Trunnion.
    tb_leg = C.common(tube, leg)
    window = C.common(tube, channel)
    brg_hits = dict(tube=round(C.common(brg, tube), 4), saddle=round(C.common(brg, saddle), 4),
                    leg=round(C.common(brg, leg), 4))
    seat_gap = round(C.distance(brg, saddle), 3)
    pin = C.blk((px + D["stop_pin"]["dx"] - 1, px + D["stop_pin"]["dx"] + 1, -54, -46, pz - 1, pz + 1))
    boss = entry.d104_local("boss")
    boss_leg_gap = round(C.distance(boss, leg), 3)
    r.check("hollow_trunnion_fits", tb_leg < 1e-3 and window < 1e-3 and not any(v > 1e-3 for v in brg_hits.values())
            and seat_gap < 0.1 and boss_leg_gap >= 0.5,
            tube_in_leg_overlap_mm3=round(tb_leg, 4), tube_window_left_in_channel_mm3=round(window, 4),
            bearing_overlaps_mm3=brg_hits, bearing_to_seat_mm=seat_gap, boss_to_leg_mm=boss_leg_gap,
            boss_to_stop_dowel_region_mm3=round(C.common(boss, pin), 4),
            tube_inboard_end_y=D["tube"]["y"][1], bearing=D["bearing"])

    # 4. Neutral pose, yaw-carried.
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

    yaw_pool = {n: s for n, s in shapes.items() if frames[n] not in ("P", "R")}
    yaw_pool.update(pcb16)
    yitems = {"tube": tube, "plug": plug, **{n: s for n, (f, s) in res.items() if f == "Y"}}
    allowed = {"tube": (LEG,), "plug": ("tube",), "HARNESS_D104_LEG_CHANNEL": (LEG,),
               "HARNESS_D104_TUBE_BORE": (), "HARNESS_D104_DISC_RUN": (), "HARNESS_D104_DISC_CROSS": (),
               "HARNESS_D104_RISER": (), "HARNESS_D104_TUNNEL_ENTRY": ()}
    neutral = {k: hits(s, yaw_pool, skip=allowed.get(k, ())) for k, s in yitems.items()}
    disc_gap = round(C.distance(C.blk(entry.D104_Y_RESERVES["HARNESS_D104_DISC_RUN"]), pcb16["PCB16_J1"]), 3) \
        if "PCB16_J1" in pcb16 else None
    r.check("yaw_items_clear_at_neutral", not any(neutral.values()), clashes={k: v for k, v in neutral.items() if v},
            disc_run_to_pcb16_J1_mm=disc_gap, sweep_floor_z=m.SWEEP_FLOOR_Z if hasattr(m, "SWEEP_FLOOR_Z") else -30.5)

    # 5. Motion grid.
    poses = env.grid_poses(env.load(), [m.ROLL_STOP[0], -10, 0, 10, m.ROLL_STOP[1]],
                           [m.PITCH_STOP[0], -15, 0, 15, 30, m.PITCH_STOP[1]])

    def pose(s, frame, roll, pitch):
        if frame == "R":
            s = s.rotate(m.ROLL_AXIS, roll)
        if frame in "RP":
            s = s.rotate(m.PITCH_AXIS, pitch)
        return s

    groups = {
        "Y": {**yitems},
        "P": {"boss": boss, "bearing": brg, **{n: s for n, (f, s) in res.items() if f == "P"}},
        "R": {n: s for n, (f, s) in res.items() if f == "R"},
    }
    pools = {f: {n: s for n, s in shapes.items() if frames[n] == f} for f in ("Y", "P", "R")}
    pools["Y"].update(pcb16)
    pools["R"].update(pcb12)
    pools["P"][SADDLE] = saddle
    pools["Y"][LEG] = leg
    # Joint pairs: the bearing turns on the tube; the bundle leaves the tube bore inside the boss.
    joint = {("bearing", "tube"), ("tube", "bearing"), ("HARNESS_D104_TUBE_BORE", "boss"),
             ("HARNESS_D104_TUBE_BORE", "bearing")}
    sweep, nearest = [], {}
    for fa, items in groups.items():
        for fb, pool in pools.items():
            if fb == fa:
                continue
            for roll, pitch in poses:
                for ka, sa in items.items():
                    pa = pose(sa, fa, roll, pitch)
                    ba = C._box(pa)
                    for kb, sb in pool.items():
                        if (ka, kb) in joint:
                            continue
                        pb = pose(sb, fb, roll, pitch)
                        bb = C._box(pb)
                        if not C._hit(ba, bb, 2.0):
                            continue
                        v = C.common(pa, pb)
                        if v > 1e-3:
                            sweep.append(dict(item=ka, part=kb, pose=(roll, pitch), mm3=round(v, 4)))
                        elif C._hit(ba, bb):
                            d = C.distance(pa, pb)
                            if d < nearest.get(ka, (99,))[0]:
                                nearest[ka] = (round(d, 3), kb, (roll, pitch))
            C.log(f"sweep {fa} vs {fb} done")
    # Same-frame clearance for the moving items.
    same = {k: hits(s, pools["P"], skip=(SADDLE,) if k in ("boss", "bearing") else ())
            for k, s in groups["P"].items()}
    same.update({k: hits(s, pools["R"]) for k, s in groups["R"].items()})
    worst = {}
    for c_ in sweep:
        key_ = (c_["item"], c_["part"])
        if c_["mm3"] > worst.get(key_, {"mm3": 0})["mm3"]:
            worst[key_] = c_
    r.check("clear_over_the_motion_envelope", not sweep and not any(same.values()), poses=len(poses),
            clashes=sorted(worst.values(), key=lambda x: -x["mm3"])[:25], same_frame=dict((k, v) for k, v in same.items() if v),
            nearest=nearest)

    # 6. Insertion and bundle size.
    path = entry._y_cyl(D["tube"]["r"], -75.0, -58.0)
    ins = hits(path, yaw_pool)
    rows = BUNDLE["width_mm"], BUNDLE["thickness_mm"]
    fits = dict(channel=(c["w"], c["y"][1] - c["y"][0]), tunnel=(c["w"], D["tunnel"]["z"][1] - D["tunnel"]["z"][0]),
                tube_bore_diag=2 * D["tube"]["r_in"], ribbon_diag=round(math.hypot(*rows), 2))
    ok = rows[0] <= fits["channel"][0] - 0.3 and rows[1] <= fits["channel"][1] - 0.3 and fits["ribbon_diag"] <= fits["tube_bore_diag"] - 1.0
    r.check("tube_inserts_from_outside_and_bundle_fits", not ins and ok, insertion_path_clashes=ins,
            bundle=BUNDLE, fits_mm=fits,
            branches={n: dict(frame=f, radius=rad) for n, (f, rad, _) in entry.D104_BRANCHES.items()})
    r.finish()


if __name__ == "__main__":
    main()
