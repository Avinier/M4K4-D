"""PCB-12 rev A: the C2 carrier in the head's roll-carried frame (D-102).

Places the KiCad STEP (core, the ESP32-S3-Zero vendor model, both transceivers,
both buffers, three GH headers and the passives) at its head-local position
and measures it against the head parts with the D-102 droid edits applied
(C2 tray and its screws removed, two crossbar bosses with M2 insert pockets,
two M2 x 4 button screws), built from 03-head/v1/cad (catalog off):

- core and Zero placement: the Zero model on its old seat;
- every board part and each mated GH plug envelope (header footprint, 9 mm
  rearward) clear of the head at the neutral pose;
- screws through the board holes, heads clear of the Zero, bosses on the
  board's back face and fused to the crossbar, clear of the display frame;
- the C2 service reserves (USB-C plug and withdrawal, BOOT/RESET rear access)
  free of board parts and plugs;
- a roll x pitch grid clamped onto the motion envelope (as check_layout.py):
  the board and plugs (roll frame) against the pitch- and yaw-frame parts.

Run from this folder with the legacy runtime; PYTHONPATH = 03-head/v1/cad first
(see ../README.md). About 5 min.
"""

import itertools
import sys
from pathlib import Path

from build123d import Compound, Location, Plane
from cadgen.step_scene import import_step

import module_checks as C

ROOT = Path(__file__).resolve().parents[3]
STEP = ROOT / "04-pcbs" / "pcb-12-c2-head-carrier" / "cad" / "pcb-12-c2-head-carrier-revA.step"
BOARD = ROOT / "04-pcbs" / "pcb-12-c2-head-carrier" / "design" / "pcb-12-c2-head-carrier.kicad_pcb"
sys.path.insert(0, str(ROOT / "04-pcbs" / "tools"))
import kfile as K  # noqa: E402

F_FACE_X = -25.0
PLUG_DEPTH = 9.0          # GH mated plug and wire bend behind the header face (E)
REMOVED = ("C2_removable_open_rear_tray", "C2_tray_M2_-39", "C2_tray_M2_-19")
OWN = ("C2_ESP32_S3_Zero_23_5x18_footprint", "C2_installed_components_reserve")
SERVICE = ("C2_USB_C_installed_plug_reserve", "C2_USB_C_withdrawal_BOOT_RESET_service_reserve",
           "C2_BOOT_RESET_rear_tool_access_reserve")


def board_location(core_t):
    """KiCad STEP -> head-local: x -> -Y, y -> +Z, z -> -X; F face at X -25.0."""
    return Plane(origin=(F_FACE_X + core_t, 71.0, 139.75), x_dir=(0, -1, 0), z_dir=(-1, 0, 0)).location


def box6(shape):
    return tuple(round(v, 3) for v in C._box(shape))


def main():
    entry = C.load_entry()
    import layout_model as m
    import motion_envelope as env
    parts = m.build_parts(catalog=False)
    C.log("head parts built")
    shapes = {n: d["shape"] for n, d in parts.items()}
    frames = {n: d["frame"] for n, d in parts.items()}
    kinds = {n: d["kind"] for n, d in parts.items()}
    cradle = "connected_rolling_cradle_flange_ear_stalks"
    old_cradle_v = C.volume(shapes[cradle])
    for sh in entry.pcb12_local("pocket"):
        shapes[cradle] = shapes[cradle] - sh
    for sh in entry.pcb12_local("boss"):
        shapes[cradle] = shapes[cradle] + sh
    screws = entry.pcb12_local("screws")
    r = C.Report("check_pcb12_fit")

    scene = import_step(str(STEP))
    kids = {c.label: c for c in scene.children if c.solids()}
    refs = {"U1", "U2", "U3", "U4", "U5", "J1", "J2", "J3", "C1", "C3", "C4", "C5",
            "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R9", "R10"}
    core = [c for name, c in kids.items() if name not in refs]
    assert len(core) == 1, [c.label for c in core]
    core = core[0]
    cb = C._box(core)
    core_t = cb[5] - cb[2]
    loc = board_location(core_t)
    placed = {name: c.moved(loc) for name, c in kids.items() if name in refs}
    board = core.moved(loc)
    bb = C._box(board)
    r.check("board_core_placed", abs(bb[1] + 44) < 0.02 and abs(bb[4] + 14) < 0.02 and abs(bb[2] - 8) < 0.02
            and abs(bb[5] - 51.5) < 0.02 and abs(bb[0] - F_FACE_X) < 0.02,
            core=box6(board), core_thickness=round(core_t, 3), missing_parts=sorted(refs - placed.keys()))
    zb, seat = C._box(placed["U1"]), C._box(shapes["C2_ESP32_S3_Zero_23_5x18_footprint"])
    r.check("zero_model_on_its_seat",
            all(abs((zb[i] + zb[i + 3]) / 2 - (seat[i] + seat[i + 3]) / 2) < 0.3 for i in (1, 2))
            and abs(zb[3] - F_FACE_X) < 0.1 and abs(zb[0] - seat[0]) < 1.6,
            zero_model=box6(placed["U1"]), seat_placeholder=[round(v, 2) for v in seat],
            note="vendor model board bottom on the carrier copper (KiCad sets models about 0.085 mm off the core); USB-C up")

    # Mated plug envelopes behind each GH header (rear, -X).
    b = K.Board(BOARD)
    plugs = {}
    for ref in ("J1", "J2", "J3"):
        hb = C._box(placed[ref])
        plugs[ref] = C.blk((F_FACE_X - PLUG_DEPTH, F_FACE_X, hb[1], hb[4], hb[2], hb[5]))

    others = {n: s for n, s in shapes.items()
              if n not in REMOVED + OWN and kinds[n] == "physical"}
    pcb_parts = {"board": board, **placed, **{f"{k}_plug": p for k, p in plugs.items()}}

    def hits(subject, pool, skip=()):
        sbx = C._box(subject)
        out = []
        for n, s in pool.items():
            if n in skip or not C._hit(sbx, C._box(s)):
                continue
            v = C.common(subject, s)
            if v > 1e-4:
                out.append((n, round(v, 4)))
        return out

    static = {k: hits(s, others, skip=(cradle,) if k == "board" else ()) for k, s in pcb_parts.items()}
    bad = {k: v for k, v in static.items() if v}
    r.check("board_parts_and_plugs_clear_at_neutral", not bad, clashes=bad,
            note="the board's back face bears on the two bosses (checked below), so the cradle is skipped for the core")

    # Screws, holes and bosses.
    zero_seat = shapes["C2_ESP32_S3_Zero_23_5x18_footprint"]
    screw_hits = [(k, hits(sc, {**others, "board": board, "zero": zero_seat, **placed}, skip=(cradle,)))
                  for k, sc in enumerate(screws, 1)]
    head_gap = min(C.distance(sc, zero_seat) for sc in screws)
    pad_gap = min(C.distance(sc, placed["U1"]) for sc in screws)
    r.check("screws_through_holes_clear_of_zero", all(not h for _, h in screw_hits) and head_gap > 0.2,
            clashes=screw_hits, head_to_zero_seat_mm=round(head_gap, 3), head_to_zero_model_mm=round(pad_gap, 3))
    boss_gap = min(C.distance(bs, board) for bs in entry.pcb12_local("boss"))
    boss_hits = [hits(bs, {n: s for n, s in others.items() if n != cradle}) for bs in entry.pcb12_local("boss")]
    frame_gap = min(C.distance(bs, shapes["display_rear_frame"]) for bs in entry.pcb12_local("boss"))
    r.check("bosses_on_board_and_crossbar", boss_gap < 0.15 and C.volume(shapes[cradle]) > old_cradle_v
            and not any(boss_hits) and frame_gap >= 0.05,
            boss_to_board_back_mm=round(boss_gap, 3), cradle_volume_added_mm3=round(C.volume(shapes[cradle]) - old_cradle_v, 2),
            boss_clashes=boss_hits, boss_to_display_frame_mm=round(frame_gap, 3))

    serv = {n: [(k, round(C.common(shapes[n], s), 4)) for k, s in pcb_parts.items()
                if k != "U1" and C.common(shapes[n], s) > 1e-4] for n in SERVICE}
    r.check("c2_service_reserves_free", not any(serv.values()), overlaps=serv,
            note="USB-C plug/withdrawal and the BOOT/RESET rear access; the Zero itself owns them")

    # Motion: roll x pitch grid; the board and plugs ride the roll frame.
    def pose(s, frame, roll, pitch):
        if frame == "R":
            s = s.rotate(m.ROLL_AXIS, roll)
        if frame in "RP":
            s = s.rotate(m.PITCH_AXIS, pitch)
        return s

    poses = env.grid_poses(env.load(), [m.ROLL_STOP[0], -15, 0, 15, m.ROLL_STOP[1]],
                           [m.PITCH_STOP[0], -15, 0, 15, m.PITCH_STOP[1]])
    movers = Compound(children=list(pcb_parts.values()) + screws)
    supports = {n: s for n, s in others.items() if frames[n] in ("P", "Y")}
    sweep_hits, worst = [], (99.0, None, None)
    for roll, pitch in poses:
        mv = pose(movers, "R", roll, pitch)
        for n, s in supports.items():
            ps = pose(s, frames[n], roll, pitch)
            if C._hit(C._box(mv), C._box(ps)):
                v = C.common(mv, ps)
                if v > 1e-4:
                    sweep_hits.append(dict(pose=(roll, pitch), part=n, mm3=round(v, 4)))
            if C._hit(C._box(mv), C._box(ps), 3.0):
                d = C.distance(mv, ps)
                if d < worst[0]:
                    worst = (round(d, 3), n, (roll, pitch))
    r.check("roll_pitch_sweep_clear", not sweep_hits, poses=len(poses), clashes=sweep_hits[:20],
            nearest_support=worst, supports=sorted(supports))
    r.finish()


if __name__ == "__main__":
    main()
