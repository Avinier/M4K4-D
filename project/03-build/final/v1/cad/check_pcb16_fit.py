"""PCB-16 rev A: the head junction on the yaw disc (D-103).

Places the KiCad STEP (core and the two FH34SRJ) flat on the disc top in the
head's local frame, with the D-103 droid edits applied (M2 insert pockets in the
disc, two M2 x 4 button screws) and the head FFC / bundle reserves from
makad-v1 (PCB16_RESERVES). Head parts are built from 03-head/v1/cad (catalog off).

- core, both ZIFs and their mouths where the FFC reserves end;
- board, parts, screws and every reserve clear of the yaw-frame parts (the
  board's underside bears on the disc; the leg foot and its screws are near);
- all of it under the head's sweep floor (Z -30.5) and clear of the pitch- and
  roll-frame parts over a roll x pitch grid clamped onto the motion envelope;
- the FFC reserves: the lower FFC rises into J1, the upper rises, runs over J1's
  closed body and drops into J2; the reserves touch only the intended parts;
- insert pockets in the disc plate leave a floor; screws fully in the inserts;
- conductor 1: on the head FFC's -X edge in the channel (D-101); with each ZIF
  at 0 deg its contact 22 is at -X, so contact m carries conductor 23-m, as the
  schematic and netlist audit assume.

Run from this folder with the legacy runtime, PYTHONPATH 03-head/v1/cad first.
"""

import sys
from pathlib import Path

from build123d import Compound, Location, Plane
from cadgen.step_scene import import_step

import module_checks as C

ROOT = Path(__file__).resolve().parents[3]
STEP = ROOT / "04-pcbs" / "pcb-16-head-junction" / "cad" / "pcb-16-head-junction-revA.step"
BOARD = ROOT / "04-pcbs" / "pcb-16-head-junction" / "design" / "pcb-16-head-junction.kicad_pcb"
sys.path.insert(0, str(ROOT / "04-pcbs" / "tools"))
import kfile as K  # noqa: E402

DISC_TOP = -34.5
SWEEP_FLOOR = -30.5
J1_MOUTH_Y, J2_MOUTH_Y = 36.0, 43.4


def board_location():
    """KiCad STEP -> head-local: X = x - 142.4, Y = 150 + y, Z = -34.5 + z."""
    return Plane(origin=(-142.4, 150.0, DISC_TOP), x_dir=(1, 0, 0), z_dir=(0, 0, 1)).location


def box6(shape):
    return tuple(round(v, 3) for v in C._box(shape))


def main():
    entry = C.load_entry()
    import layout_model as m
    import motion_envelope as env
    parts = m.build_parts(catalog=False)
    C.log("head parts built")
    shapes = {n: d["shape"] for n, d in parts.items() if d["kind"] == "physical"}
    frames = {n: d["frame"] for n, d in parts.items()}
    disc = "yaw_turntable_disc_flush"
    for sh in entry.pcb16_local("pocket"):
        shapes[disc] = shapes[disc] - sh
    screws = entry.pcb16_local("screws")
    reserves = {n: C.blk(b) for n, b in entry.PCB16_RESERVES.items()}
    r = C.Report("check_pcb16_fit")

    scene = import_step(str(STEP))
    kids = {c.label: c for c in scene.children if c.solids()}
    loc = board_location()
    placed = {n: c.moved(loc) for n, c in kids.items() if n in ("J1", "J2")}
    core = [c for n, c in kids.items() if n not in ("J1", "J2")]
    assert len(core) == 1
    board = core[0].moved(loc)
    bb = C._box(board)
    j1, j2 = C._box(placed["J1"]), C._box(placed["J2"])
    r.check("board_and_zifs_placed", abs(bb[2] - DISC_TOP) < 0.02 and abs(bb[0] + 62.4) < 0.02 and abs(bb[3] + 26.0) < 0.02
            and abs(bb[1] - 35.5) < 0.02 and abs(bb[4] - 54.0) < 0.02
            and abs(j1[1] - J1_MOUTH_Y) < 0.05 and abs(j2[1] - J2_MOUTH_Y) < 0.05
            and abs((j1[0] + j1[3]) / 2 + 42.4) < 0.05,
            core=box6(board), J1=box6(placed["J1"]), J2=box6(placed["J2"]))

    items = {"board": board, **placed, **{f"screw_{k}": s for k, s in enumerate(screws, 1)}}

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

    static = {n: s for n, s in shapes.items() if frames[n] not in ("P", "R")}
    st = {k: hits(s, static, skip=(disc,) if k == "board" or k.startswith("screw") else ()) for k, s in items.items()}
    st.update({k: hits(s, static) for k, s in reserves.items()})
    gaps = {k: round(C.distance(s, shapes["yaw_yoke_leg_55"]), 3) for k, s in items.items()}
    r.check("clear_of_yaw_frame_parts", not any(st.values()), clashes={k: v for k, v in st.items() if v},
            gap_to_leg_mm=gaps, board_on_disc_overlap_mm3=round(C.common(board, shapes[disc]), 4))

    tops = {k: round(C._box(s)[5], 3) for k, s in {**items, **reserves}.items() if not k.startswith("screw")}
    screw_top = max(C._box(s)[5] for s in screws)
    r.check("under_the_sweep_floor", max(tops.values()) <= SWEEP_FLOOR and screw_top <= SWEEP_FLOOR,
            sweep_floor_z=SWEEP_FLOOR, highest=max(tops, key=tops.get), tops=tops, screw_head_top=round(screw_top, 3))

    poses = env.grid_poses(env.load(), [m.ROLL_STOP[0], -10, 0, 10, m.ROLL_STOP[1]],
                           [m.PITCH_STOP[0], -15, 0, 15, 30, m.PITCH_STOP[1]])
    group = Compound(children=list(items.values()) + list(reserves.values()))
    gbox = C._box(group)
    movers = {n: s for n, s in shapes.items() if frames[n] in ("P", "R")}
    sweep_hits, nearest = [], (99.0, None, None)
    for roll, pitch in poses:
        for n, s in movers.items():
            ps = s.rotate(m.ROLL_AXIS, roll) if frames[n] == "R" else s
            ps = ps.rotate(m.PITCH_AXIS, pitch)
            pb = C._box(ps)
            if not C._hit(gbox, pb, 3.0):
                continue
            v = C.common(group, ps)
            if v > 1e-4:
                sweep_hits.append(dict(pose=(roll, pitch), part=n, mm3=round(v, 4)))
            d = C.distance(group, ps)
            if d < nearest[0]:
                nearest = (round(d, 3), n, (roll, pitch))
    r.check("clear_of_moving_head_over_envelope", not sweep_hits, poses=len(poses), clashes=sweep_hits[:20],
            nearest=nearest)

    # FFC reserves: each ends at its mouth and touches only its own ZIF.
    rise1, rise2 = reserves["HARNESS_HEAD_FFC_STRAIGHT_INTO_J1"], reserves["HARNESS_HEAD_FFC_RISE_TO_PCB16_J2"]
    bend1 = reserves["HARNESS_HEAD_FFC_RISE_TO_PCB16_J1"]
    over, drop = reserves["HARNESS_HEAD_FFC_RAISED_OVER_J1"], reserves["HARNESS_HEAD_FFC_DROP_TO_PCB16_J2"]
    ffc_vs = {k: [(z, round(C.common(s, items[z]), 4)) for z in ("board", "J1", "J2") if C.common(s, items[z]) > 1e-4]
              for k, s in (("bend_J1", bend1), ("straight_J1", rise1), ("rise_J2", rise2), ("over_J1", over), ("drop_J2", drop))}
    over_gap = round(C._box(over)[2] - j1[5], 3)
    r.check("ffc_paths_into_the_mouths", not any(ffc_vs.values()) and over_gap >= 0.04
            and abs(C._box(rise1)[4] - J1_MOUTH_Y) < 0.01 and abs(C._box(drop)[4] - J2_MOUTH_Y) < 0.01,
            overlaps=ffc_vs, raised_run_above_J1_mm=over_gap,
            note="S-bends are enclosing boxes (E: about R 3 mm; 1 mm straight into J1, none into J2), as PCB-08's stepped probe")

    floor = min(C._box(p)[2] for p in entry.pcb16_local("pocket"))
    disc_bottom = C._box(shapes[disc])[2]
    plate_bottom = m.YAW_DISC_TOP_Z - m.YAW_DISC_PLATE
    shank_in = [round(C.common(s, p), 3) for s, p in zip(screws, entry.pcb16_local("pocket"))]
    r.check("inserts_in_the_disc_plate", floor - plate_bottom >= 0.7 and all(v > 0 for v in shank_in),
            pocket_floor_z=round(floor, 2), plate_bottom_z=plate_bottom, floor_left_mm=round(floor - plate_bottom, 2),
            disc_bottom_z=round(disc_bottom, 2), shank_in_pocket_mm3=shank_in)

    b = K.Board(BOARD)
    xw = lambda ref, n: round(b.pad(ref, n)["at"][0] - 142.4, 3)
    ok = all(xw(ref, 22) < xw(ref, 1) for ref in ("J1", "J2"))
    r.check("conductor_1_lands_on_contact_22", ok, j1_contact22_x=xw("J1", 22), j1_contact1_x=xw("J1", 1),
            rule="head FFC conductor 1 on its -X edge (D-101) meets contact 22 at -X: contact m = conductor 23-m")
    r.finish()


if __name__ == "__main__":
    main()
