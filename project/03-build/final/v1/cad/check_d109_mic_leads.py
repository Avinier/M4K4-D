"""D-109 F2: shell-dressed W27 leads ride with the shell.

Rows per mic: the dressed lead clears the shell skin and the mic parts at the
installed pose; translated with the shell through its whole vertical travel (0..140 mm
in 5 mm steps, D-037: the shell lifts vertically) it meets no fixed part.
"""

import json
from pathlib import Path

import module_checks as C
from chassis_harness import _tube

HERE = Path(__file__).resolve().parent
R = 1.2
MOVES_WITH_SHELL = ("BODY_SHELL", "M9_", "HARNESS_", "D109_", "REAR_SERVICE_PANEL", "POWER_BUTTON", "M12_XT30", "M12_JST_XHP")


def main():
    _, _, leaves = C.droid_tree()
    shell = C.find(leaves, "BODY_SHELL")
    mics = [lf for lf in leaves if lf.label.startswith("M9_") and "PIGTAIL" not in lf.label]
    fixed = [lf for lf in leaves if not lf.label.startswith(MOVES_WITH_SHELL)
             and not any(k in lf.label for k in ("RESERVE", "KEEP_OUT", "ENVELOPE"))]
    r = C.Report("check_d109_mic_leads")
    for name, d in json.loads((HERE / "d109-mic-leads.json").read_text()).items():
        t = _tube(d["points"], R)
        run = _tube(d["points"][1:], R)    # exit segments run in the droid-cut boss notch; the pigtail stub stays in its pocket
        # piecewise throughout: whole-tube Booleans read 0 for a lead 12 mm inside the shell (2026-11-17)
        skin = C.piece_common(run, shell.shape)
        frame_hits = C.piece_clashes(run, fixed, min_vol=0.05, parts_only=False)
        r.check(f"{name} lead clear of the shell skin", skin < 0.05,
                overlap=round(skin, 3), gap=C.min_gap(run, [shell], reach=2.0, parts_only=False))
        r.check(f"{name} lead clear of the frame and fixed parts", not frame_hits, hits=frame_hits[:6])
        hits = [h for h in C.piece_clashes(t, mics, min_vol=0.05, parts_only=False)
                if not h[0].endswith(("_BOARD_UNMEASURED",))]
        r.check(f"{name} lead clear of mic parts", not hits, hits=hits)
        # adhesive cable clips (bought, E 6 x 3.2 x 4.8 around the lead) at the clip points ride too
        from build123d import Compound
        # clip: 6 mm long, 0.4 mm strap inboard of the lead, base from the lead to the skin
        sg = lambda y: 1 if y > 0 else -1
        clips = [C.blk((x - 3, x + 3, *sorted((y - sg(y) * (R + 0.4), y + sg(y) * (R + 0.6))), z - R - 0.4, z + R + 0.4))
                 for x, y, z in d["clips"]]
        rider = Compound(children=[t, *clips])
        r.check(f"{name} clips clear of the shell skin", all(C.common(c, shell.shape) < 0.3 for c in clips),
                clips=len(clips), note="clip base bonds to the skin: <= 0.3 mm3 contact allowed")
        first = None
        for dz in range(0, 141, 5):
            hits = [h for part in (*C._solids(t), *clips) for h in C.clashes(C.moved(part, (0, 0, dz)), fixed, min_vol=0.05, parts_only=False)]
            if hits:
                first = (dz, hits[:4])
                break
        r.check(f"{name} lead rides with the shell (0-140 mm)", first is None, first_hit=first)
    r.finish()


if __name__ == "__main__":
    main()
