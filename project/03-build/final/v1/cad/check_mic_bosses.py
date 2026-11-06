"""D-095 (D-093 Q6): the four INMP441 mics in their redesigned shell bosses at the D-037 ports.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 3 min.
Replaces body check_mic_mounts.py for the final droid (the body source still has the PCB-06 bosses).
Measures per mic: the boss inside the shell's outer envelope (skin unchanged), the board in its
pocket with room all round, the gasket in its pocket, the port open to the outside, the pilot depth
and skin beyond it, screw engagement, the washer's worst-case overlap on the board edge, nothing
inboard of |Y| 68.5, every part clear of the robot, and the shell lowering past the frame.
"""

import module_checks as C

OWN = ("M9 microphones",)


def main():
    entry, tree, leaves = C.droid_tree()
    import body_v1_model as B
    m = entry.MIC
    r = C.Report("check_mic_bosses")
    shell = C.find(leaves, "BODY_SHELL").shape
    outer = B._shell_outer()
    r.check("shell_one_solid", len(shell.solids()) == 1, solids=len(shell.solids()))
    raw = B.body_shell()
    out_raw = C.volume(raw) - C.common(raw, outer)
    out_now = C.volume(shell) - C.common(shell, outer)
    r.check("no_new_material_outside_skin", out_now - out_raw < 0.01, outside_mm3_source=out_raw, outside_mm3_droid=out_now)

    bw, bh, bt = m["board"]
    pw, ph = m["pocket"]
    f, floor = m["seat"], entry.MIC_FLOOR
    for x, y, z, name in B.MICROPHONE_PORTS:
        s = 1 if y > 0 else -1
        board = C.find(leaves, f"M9_INMP441_{name}_BOARD_UNMEASURED").shape
        gasket = C.find(leaves, f"M9_INMP441_{name}_GASKET").shape
        ov, gap = C.common(board, shell), C.distance(board, shell)
        lateral = min((pw - bw) / 2, (ph - bh) / 2)
        r.check(f"{name}_board_in_pocket", ov < 1e-3 and lateral >= 0.4, overlap_mm3=ov, lateral_clearance=lateral, floor_contact_gap=gap)
        r.check(f"{name}_gasket_in_pocket", C.common(gasket, shell) < 1e-3, overlap_mm3=C.common(gasket, shell))
        iv = C.ray(shell, (x, 0.0, z), (0, s, 0))
        through = [seg for seg in iv if seg[1] > floor - 0.05]
        r.check(f"{name}_port_open_to_outside", not through, material_beyond_floor=through)
        # Pilots: Ø1.6 x 4.0 from the seat, at least 0.8 mm of shell beyond.
        for du in (-m["screw_u"], m["screw_u"]):
            iv = C.ray(shell, (x + du, 0.0, z), (0, s, 0))
            pilot_end = f + m["pilot"][1]
            skin = max(seg[1] for seg in iv)
            hole = [seg for seg in iv if seg[0] < pilot_end - 0.05 and seg[1] > f + 0.05 and seg[0] > f + 0.05]
            r.check(f"{name}_pilot_{du:+.1f}", skin - pilot_end >= 0.8 and not hole, pilot_end_abs_y=pilot_end, shell_outer_abs_y=skin, material_in_pilot=hole)
        tip = f - m["washer"][1] + m["screw_len"]
        r.check(f"{name}_screw_engagement", tip - f >= 3.0 and tip <= f + m["pilot"][1] - 0.2, engaged=tip - f, tip_abs_y=tip)
        reach = m["screw_u"] - m["washer"][0]
        worst = bw / 2 - lateral - reach
        r.check(f"{name}_washer_overlap_worst_case", worst >= 0.3, overlap_mm=worst, washer_inner_reach=reach)
        group = [lf for lf in leaves if f"_{name}_" in lf.label and lf.label.startswith("M9_")]
        inboard = min(abs(lf.box[4] if s > 0 else lf.box[1]) for lf in group)
        r.check(f"{name}_nothing_inboard_of_68p5", inboard >= 68.5, innermost_abs_y=inboard)
        for lf in group:
            if not C.is_part(lf.path):
                continue
            skip = OWN + (("BODY_SHELL",) if any(k in lf.label for k in ("SCREW", "WASHER", "BOARD", "GASKET")) else ())
            hits = C.clashes(lf.shape, leaves, skip=skip)
            gap, near = C.min_gap(lf.shape, leaves, skip=skip)
            r.check(f"clear_{lf.label}", not hits and gap >= 0.2, clashes=hits, min_gap=gap, nearest=near)

    # The shell with the mics on it lowers onto the body frame: mic parts swept up from final.
    on_shell = [(lf.label, lf.shape) for lf in leaves if lf.label.startswith("M9_") and C.is_part(lf.path)]
    frame_side = [lf for lf in leaves if "BODY_SHELL" not in lf.label]
    hit = C.sweep(on_shell, frame_side, (0, 0, 1), [1.0 * k for k in range(1, 81, 2)], skip=OWN)
    r.check("shell_lowering_with_mics", hit is None, first_hit=hit)
    fan = C.find(leaves, "ENCLOSURE_FAN_3010_REAR_THREE_SPOKE_MOTOR_SUPPORT")
    rear = [C.find(leaves, f"M9_INMP441_REAR_L_BOARD_UNMEASURED")]
    r.check("rear_left_mic_to_fan_d043", True, distance_mm=C.distance(rear[0].shape, fan.shape), note="report only; D-043 re-check")
    r.finish()


if __name__ == "__main__":
    main()
