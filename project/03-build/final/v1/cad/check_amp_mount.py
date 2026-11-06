"""D-095: the MAX98357A amp and the perfboard audio hub on the bracket fused to the front +Y post.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md; about 2 min.
Measures: the frame still one solid with the bracket fused in, the amp on its cradle pads with the
rim clear, hub screw engagement, every part clear of the robot and of the speaker's acoustic
cavity, and the shell lowering over the bracket.
"""

import module_checks as C

OWN = ("M8 amplifier", "M13 audio hub")


def main():
    entry, tree, leaves = C.droid_tree()
    a, h, cr = entry.AMP, entry.HUB, entry.CRADLE
    r = C.Report("check_amp_mount")
    frame = C.find(leaves, "BODY_FRAME_MAIN_PRINT").shape
    r.check("frame_one_solid_with_bracket", len(frame.solids()) == 1, solids=len(frame.solids()))
    bracket = entry._blk(*a["bracket"])
    r.check("bracket_in_frame", C.frac_inside(bracket, frame) > 0.98, fraction=C.frac_inside(bracket, frame))
    post = C.blk((60.0, 68.0, 59.0, 69.0, 100.0, 123.0))
    fused = C.common(entry._blk(a["bracket"][0], a["bracket"][1], 58.5, a["bracket"][3], a["bracket"][4], a["bracket"][5]), frame)
    r.check("bracket_fused_to_post", C.frac_inside(post, frame) > 0.9 and fused > 0, post_fraction=C.frac_inside(post, frame), root_mm3=fused)

    amp = C.find(leaves, "M8_MAX98357A_BOARD_UNMEASURED")
    pad_top = a["bracket"][1] + cr["pad"]
    ov = C.common(amp.shape, frame)
    r.check("amp_on_cradle_pads", abs(amp.box[0] - pad_top) < 0.02 and ov < 1e-3, board_back_x=amp.box[0], pad_top_x=pad_top, overlap_mm3=ov)
    hx = a["bracket"][0] - h["boss"][1]
    tip = hx - h["board"][2] + h["screw"]
    r.check("hub_screw_engagement", tip - hx >= 2.0 and tip <= a["bracket"][0] + 1.5 - 0.2, engaged=tip - hx, tip_x=tip)

    subjects = [lf for lf in C.own(leaves, *OWN) if C.is_part(lf.path)]
    for lf in subjects:
        skip = OWN + (("BODY_FRAME_MAIN_PRINT",) if any(k in lf.label for k in ("SCREW", "BOARD", "PERFBOARD")) else ())
        hits = C.clashes(lf.shape, leaves, skip=skip)
        gap, near = C.min_gap(lf.shape, leaves, skip=skip)
        r.check(f"clear_{lf.label}", not hits and gap >= 0.2, clashes=hits, min_gap=gap, nearest=near)
    cavity = C.find(leaves, "SPEAKER_ACOUSTIC_CAVITY_KEEP_OUT").shape
    worst = min(C.distance(lf.shape, cavity) for lf in subjects)
    r.check("speaker_cavity_clear", worst >= 1.0, min_gap=worst)
    shell = C.find(leaves, "BODY_SHELL")
    group = [(lf.label, lf.shape) for lf in subjects] + [("bracket", bracket)]
    hit = C.sweep(group, [shell], (0, 0, -1), [1.0 * k for k in range(0, 81, 2)])
    r.check("shell_lowers_over_bracket", hit is None, first_hit=hit)
    r.finish()


if __name__ == "__main__":
    main()
