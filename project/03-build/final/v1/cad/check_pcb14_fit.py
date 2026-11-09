"""PCB-14 rev A: three real joiner boards in the yaw rotor (D-052, D-101).

Places the KiCad STEP (board core, J1 lower and J2 upper FH34SRJ with the
detailed drawing-based models) three times at the D-101 4.5 mm pitch and
measures them against the robot:

- the static droid tree (chassis + body with every droid edit, bought modules);
- the yaw moving half (hub, rotor) with the D-101 droid edits: posts rebuilt
  for the new slots, placeholders moved;
- the head disc from 03-head/v1/cad/yaw-yoke.step (D-052 build; the bore and
  pilot are measured, not assumed).

Checks: core and ZIF placement, every board clear of the robot and of each
other, tabs in their slots and captured under the hub shoulder, the rotor's
rise into the hub with the boards on it, both ZIFs inside the disc bore,
opened actuators (Hirose: back flip, 90 deg; 3.45 mm open depth; height
3.4 mm and 1.8 mm behind the body, E, as PCB-08) clear of the next board, a
lifting-tool column over every upper actuator, both FFC exits (head FFCs up
the bore and flat in the disc channel; cassette tails into the lower mouths),
the drum-core fold (D-052 method, planes at -4.5/0/+4.5), and the conductor-1
frame: cassette conductor 1 at the lower ZIF's -X end, straight through to
the upper ZIF's contact 22, so the head FFC carries conductor 1 on its -X edge.

Paper geometry for the cables (0.3 mm FFC, square corners, E). Run from this
folder with the legacy runtime and the PYTHONPATH in ../README.md.
"""

import math
import sys
from pathlib import Path

import numpy as np
from build123d import Compound, Location, Plane
from cadgen.step_scene import import_step

import module_checks as C
from check_pcb08_ffc_fold import pcb14_w, seg

ROOT = Path(__file__).resolve().parents[3]
STEP = ROOT / "04-pcbs" / "pcb-14-yaw-rotor-joiner" / "cad" / "pcb-14-yaw-rotor-joiner-revA.step"
DISC_STEP = ROOT / "03-head" / "v1" / "cad" / "yaw-yoke.step"
sys.path.insert(0, str(ROOT / "04-pcbs" / "tools"))
import kfile as K  # noqa: E402
BOARD = ROOT / "04-pcbs" / "pcb-14-yaw-rotor-joiner" / "design" / "pcb-14-yaw-rotor-joiner.kicad_pcb"

AX = 16.0                                   # BODY_AXIS_X
Y0 = (-5.725, -1.225, 3.275)                # D-101 back faces (makad-v1 PCB14_BOARD_Y0)
T = 0.8
SLOT_C = 0.425                              # FH34SRJ slot centre above the board face (model)
FFC_T, FFC_HW = 0.3, 5.75                   # generic 22-way 0.5 mm FFC
MOUTH_LO, MOUTH_UP = 134.40, 150.20         # layout_pcb14 PLACE (entry faces)
REAR_LO, REAR_UP = 138.20, 146.40           # body rear faces
ACT_H, ACT_BEHIND, ACT_IN, ACT_HX = 3.4, 1.8, 1.0, 6.0   # opened actuator envelope (E)
BAND_Z = (121.35, 132.85)                   # YAW_FFC_BAND_Z
DRUM_R = 11.0
CHANNEL_FLOOR, DISC_TOP = 153.5, 155.0
HEAD_LAYER_Z = {3: 153.7, 2: 154.1, 1: 154.5}   # head FFCs flat in the channel; board 3 lowest
SKIP = ("PCB14_", "YAW_ROTOR_FFC_")


def board_location(y0, core_zmin):
    """KiCad STEP -> world: x -> -X, y -> +Z, z -> +Y (layout_pcb14 docstring)."""
    return Plane(origin=(116.0, y0 - core_zmin, 242.3), x_dir=(-1, 0, 0), z_dir=(0, 1, 0)).location


def box6(shape):
    return tuple(round(v, 3) for v in C._box(shape))


def blk(x0, x1, y0, y1, z0, z1):
    return C.blk((x0, x1, y0, y1, z0, z1))


def max_r(shape):
    b = C._box(shape)
    return max(math.hypot(x - AX, y) for x in (b[0], b[3]) for y in (b[1], b[4]))


def main():
    entry, _tree, leaves = C.droid_tree()
    import body_v1_model as B
    assert abs(B.BODY_AXIS_X - AX) < 1e-9
    moving_tree = entry._apply_droid_cuts(Compound(children=B.yaw_drive_moving_parts()), strict=False)
    moving = [C.Leaf(p, C.place(n, l), False) for p, n, l in C._leaves(moving_tree)]
    disc_scene = import_step(str(DISC_STEP))
    disc_src = max((c for c in disc_scene.children if c.solids()), key=lambda c: C.volume(c))
    disc = C.Leaf(("HEAD", "yaw_turntable_disc_flush"), disc_src.moved(Location(B.HEAD_ORIGIN_IN_CHASSIS)), False)
    world = leaves + moving + [disc]
    hub = C.find(moving, "YAW_HUB_DRIVEN_GEAR_M1_Z37")
    rotor = C.find(moving, "YAW_ROTOR_CLAMP_DRUM_AND_STOP_DOG")
    r = C.Report("check_pcb14_fit")

    # Disc as built: bore radius and pilot bottom from the solid.
    db = C._box(disc.shape)
    probe = [k * 0.05 for k in range(180, 240)]
    bore_r = next(rr for rr in probe if C.common(blk(AX - rr, AX + rr, -0.05, 0.05, 152.0, 153.0), disc.shape) > 1e-6) - 0.05
    pilot_bottom = min(z for z in [144.0 + 0.05 * k for k in range(40)]
                       if C.common(blk(AX + 11.0, AX + 12.5, -0.5, 0.5, z, z + 0.05), disc.shape) > 1e-6)
    r.check("disc_bore_and_pilot_as_d052", abs(bore_r - 10.5) < 0.06 and abs(pilot_bottom - 144.4) < 0.06,
            bore_r=round(bore_r, 3), pilot_bottom_z=round(pilot_bottom, 3), disc_box=[round(v, 2) for v in db])

    # The three boards.
    scene = import_step(str(STEP))
    parts = {c.label: c for c in scene.children if c.solids()}
    core = next(c for name, c in parts.items() if name not in ("J1", "J2"))
    cb = C._box(core)
    boards = []
    for k, y0 in enumerate(Y0, start=1):
        loc = board_location(y0, cb[2])
        boards.append({name: p.moved(loc) for name, p in (("core", core), ("J1", parts["J1"]), ("J2", parts["J2"]))})
    b1 = C._box(boards[0]["core"])
    r.check("board_core_placed", abs(b1[0] - (AX - 13.6)) < 0.02 and abs(b1[3] - (AX + 13.6)) < 0.02
            and abs(b1[2] - 133.9) < 0.02 and abs(b1[5] - 150.7) < 0.02 and abs(b1[1] - Y0[0]) < 0.01
            and abs((b1[4] - b1[1]) - (cb[5] - cb[2])) < 0.01,
            core=box6(boards[0]["core"]), core_thickness=round(cb[5] - cb[2], 3))
    j1, j2 = C._box(boards[0]["J1"]), C._box(boards[0]["J2"])
    r.check("zif_bodies_placed", abs(j1[2] - MOUTH_LO) < 0.02 and abs(j1[5] - REAR_LO) < 0.15
            and abs(j2[5] - MOUTH_UP) < 0.02 and abs(j2[2] - REAR_UP) < 0.15
            and abs((j1[0] + j1[3]) / 2 - AX) < 0.02 and abs(j1[4] - (Y0[0] + T + 1.0)) < 0.15,
            J1=box6(boards[0]["J1"]), J2=box6(boards[0]["J2"]),
            note="KiCad places components on the core face; ZIF top 1.0 mm above it")

    # Clearance to the robot, the moving half and the disc.
    for k, bd in enumerate(boards, start=1):
        for name, part in bd.items():
            hits = C.clashes(part, world, skip=SKIP)
            gap, near = C.min_gap(part, world, skip=SKIP)
            r.check(f"board{k}_{name}_clear", not hits, clashes=hits, nearest=near, min_gap=round(gap, 3))
    pair_hits = [(i + 1, j + 1, round(C.common(a, b), 4))
                 for i in range(3) for j in range(i + 1, 3)
                 for a in boards[i].values() for b in boards[j].values() if C.common(a, b) > 1e-4]
    face_gap = min(Y0[k + 1] - (Y0[k] + T + 1.0) for k in range(2))
    r.check("boards_clear_of_each_other", not pair_hits, overlaps=pair_hits, zif_top_to_next_board_mm=round(face_gap, 3))

    # Tabs: in their slots (0.1 a side), on the 0.4 floor, captured by the shoulder.
    tab_gaps = [round(C.distance(bd["core"], rotor.shape), 3) for bd in boards]
    capture = min(math.hypot(13.6, abs(y)) for y0 in Y0 for y in (y0, y0 + T)) - B.YAW_GEAR_BORE_RADIUS
    r.check("tabs_in_slots_and_captured", all(g < 0.12 for g in tab_gaps) and capture >= 0.4
            and B.YAW_HUB_SHOULDER[2] - 143.0 >= 0.9,
            board_to_rotor_gap=tab_gaps, shoulder_overhang_mm=round(capture, 3),
            lift_gap_mm=round(B.YAW_HUB_SHOULDER[2] - 143.0, 2))
    # The rotor ring screws to the hub spigot (face contact by design); the posts must stand clear.
    posts = entry.pcb14_posts()
    post_gap = C.distance(posts, hub.shape)
    r.check("rebuilt_posts_clear_hub", C.common(rotor.shape, hub.shape) < 1e-4 and post_gap > 0.5
            and C.common(posts, rotor.shape) > 0.99 * C.volume(posts),
            posts_to_hub_mm=round(post_gap, 3), rotor_hub_overlap_mm3=round(C.common(rotor.shape, hub.shape), 4),
            post_to_spigot_mm=round(B.YAW_HUB_SPIGOT[0] - math.hypot(15.2, 6.9), 2))

    # Assembly: the rotor carrying the boards rises into the hub from 15 mm below.
    lift = [("rotor", rotor.shape)] + [(f"board{k}_{n}", p) for k, bd in enumerate(boards, 1) for n, p in bd.items()]
    # D-052 bench order: bearing in the housing, clamp ring, hub; then the rotor from below.
    cartridge = [lf for lf in world if lf.label.startswith(("YAW_HUB", "YAW_BEARING", "YAW_CARTRIDGE_HOUSING"))]
    first = C.sweep(lift, cartridge, (0, 0, -1), [0.5 * k for k in range(1, 31)])
    r.check("rotor_with_boards_rises_into_hub", first is None and len(cartridge) >= 4, first_hit_going_down=first,
            cartridge=[lf.label for lf in cartridge], note="bench cartridge only; the disc goes on at D-052 step 5")

    # Bore: the head unplugs through the disc's bore with the disc on.
    zone = blk(AX - 20, AX + 20, -20, 20, pilot_bottom, 160.0)
    bore_parts = [C.common(bd["core"], zone) for bd in boards]
    board_r = max(math.hypot(7.25, abs(y)) for y0 in Y0 for y in (y0, y0 + T))
    upper_r = max(max_r(bd["J2"]) for bd in boards)
    r.check("upper_zifs_and_boards_inside_disc_bore", board_r < bore_r - 1.0 and upper_r < bore_r - 1.0
            and all(v > 0 for v in bore_parts),
            board_corner_r=round(board_r, 3), upper_zif_r=round(upper_r, 3), bore_r=round(bore_r, 3))

    # Opened actuators: each ZIF's back flip at 90 deg, next to the next board's back.
    act_hits, act_gaps = [], []
    for k, (bd, y0) in enumerate(zip(boards, Y0), start=1):
        face = y0 + T
        for name, rear, sign in (("J1", REAR_LO, 1), ("J2", REAR_UP, -1)):
            z0, z1 = sorted((rear - sign * ACT_IN, rear + sign * ACT_BEHIND))
            env = blk(AX - ACT_HX, AX + ACT_HX, face, face + ACT_H, z0, z1)
            hits = C.clashes(env, world, skip=SKIP)
            hits += [(f"board{j}", round(C.common(env, boards[j - 1]["core"]), 4)) for j in range(1, 4)
                     if j != k and C.common(env, boards[j - 1]["core"]) > 1e-4]
            act_hits += [(f"board{k}_{name}", h) for h in hits]
            nxt = Y0[k] - (face + ACT_H) if k < 3 else bore_r - max_r(env)
            act_gaps.append((f"board{k}_{name}", round(nxt, 3)))
    r.check("opened_actuators_clear", not act_hits and min(g for _, g in act_gaps) >= 0.25,
            clashes=act_hits, clearance_to_next_board_or_bore=act_gaps,
            envelope_E=dict(height=ACT_H, behind_rear=ACT_BEHIND, into_body=ACT_IN, half_x=ACT_HX))
    # A spudger column down to every upper actuator's centre, between the boards.
    col_hits = []
    for k, y0 in enumerate(Y0, start=1):
        ffc = y0 + T + SLOT_C
        col = blk(AX - 1.5, AX + 1.5, ffc + FFC_T / 2 + 0.2, min(y0 + T + ACT_H, (Y0[k] if k < 3 else 9.0) - 0.2),
                  REAR_UP + ACT_BEHIND, DISC_TOP + 2.0)
        col_hits += [(k, h) for h in C.clashes(col, world, skip=SKIP)]
        col_hits += [(k, f"board{j}") for j in range(1, 4) if C.common(col, boards[j - 1]["core"]) > 1e-4]
    r.check("upper_actuator_tool_column_open", not col_hits, clashes=col_hits,
            note="3 mm wide tool column, beside the head FFC, from the disc top to the opened actuator")

    # Cable exits. Head FFCs: rise in their plane, turn +Y and lie flat in the channel.
    exits, exit_hits = {}, []
    for k, y0 in enumerate(Y0, start=1):
        yp, zl = y0 + T + SLOT_C, HEAD_LAYER_Z[k]
        exits[f"head{k}_rise"] = blk(AX - FFC_HW, AX + FFC_HW, yp - FFC_T / 2, yp + FFC_T / 2, MOUTH_UP, zl + FFC_T / 2)
        exits[f"head{k}_flat"] = blk(AX - FFC_HW, AX + FFC_HW, yp + FFC_T / 2, 14.0, zl - FFC_T / 2, zl + FFC_T / 2)
        exits[f"tail{k}"] = blk(AX - FFC_HW, AX + FFC_HW, yp - FFC_T / 2, yp + FFC_T / 2, BAND_Z[1], MOUTH_LO)
    for name, solid in exits.items():
        hits = C.clashes(solid, world, skip=SKIP)
        hits += [(f"board{j}", round(C.common(solid, bd[p]), 4)) for j, bd in enumerate(boards, 1) for p in bd
                 if C.common(solid, bd[p]) > 1e-4]
        hits += [(other, round(C.common(solid, s2), 4)) for other, s2 in exits.items()
                 if other != name and other[:5] != name[:5] and C.common(solid, s2) > 1e-4]
        exit_hits += [(name, h) for h in hits]
    r.check("ffc_exits_clear", not exit_hits, clashes=exit_hits,
            head_layers_z=HEAD_LAYER_Z, channel_floor=CHANNEL_FLOOR, disc_top=DISC_TOP,
            head_stack_top_below_disc_top=round(DISC_TOP - (max(HEAD_LAYER_Z.values()) + FFC_T / 2), 2),
            tail_length_mm=round(MOUTH_LO - BAND_Z[1], 2))

    # Drum-core fold (D-052 method): slit at 0 deg, fan-out S-bend to each plane, one 45 deg fold up.
    fold_hits, folds = [], {}
    for k, y0 in enumerate(Y0, start=1):
        yp = y0 + T + SLOT_C
        folds[f"fold{k}"] = blk(AX - FFC_HW, AX + FFC_HW, yp - FFC_T, yp + FFC_T, *BAND_Z)      # doubled at the crease
        zm, h = (BAND_Z[0] + BAND_Z[1]) / 2, BAND_Z[1] - BAND_Z[0]
        folds[f"fanout{k}"] = seg((AX + DRUM_R - 0.05, 0.0, zm), (AX + FFC_HW + 0.15, yp, zm), FFC_T, (0, 0, 1), h)
    for name, solid in folds.items():
        hits = C.clashes(solid, world, skip=SKIP)
        hits += [(other, round(C.common(solid, s2), 4)) for other, s2 in folds.items()
                 if other[-1] != name[-1] and name.startswith("fold") and other.startswith("fold")
                 and C.common(solid, s2) > 1e-4]
        fold_hits += [(name, h) for h in hits]
    planes = [y0 + T + SLOT_C for y0 in Y0]
    fold_r = math.hypot(FFC_HW + 0.15, max(abs(p) for p in planes) + FFC_T)
    run, off = DRUM_R - (FFC_HW + 0.15), max(abs(p) for p in planes)
    s_bend = (run ** 2 + off ** 2) / (4.0 * off)
    r.check("drum_core_fold", not fold_hits and fold_r <= DRUM_R - 1.0 and s_bend >= 2.5,
            clashes=fold_hits, planes_y=[round(p, 3) for p in planes], fold_square_r=round(fold_r, 2),
            fold_to_drum_bore_mm=round(DRUM_R - fold_r, 2), fanout_s_bend_radius_E=round(s_bend, 2),
            note="fan-out is a straight slab from the slit (R11, Y 0) to the fold edge in each plane, not a bent surface")

    # Conductor 1: from the cassette convention through the drum fold and the board.
    b = K.Board(BOARD)
    world_x = lambda ref, n: round(116.0 - b.pad(ref, n)["at"][0], 3)
    t14, w14 = pcb14_w((0, 0, -1))                     # conductor 1 on the cassette TOP edge
    lower_ok = np.allclose(t14, [0, 0, 1]) and np.allclose(w14, [1, 0, 0]) and world_x("J1", 1) < AX
    straight = all(abs(world_x("J1", n) - world_x("J2", 23 - n)) < 1e-6 for n in range(1, 23))
    # Head side: up out of the upper mouth, a bend about X to +Y keeps w along +X.
    r.check("conductor_1_frame", lower_ok and straight and world_x("J2", 22) < AX and world_x("J2", 1) > AX,
            lower_travel=np.round(t14, 3).tolist(), lower_w_1_to_22=np.round(w14, 3).tolist(),
            j1_contact1_x=world_x("J1", 1), j2_contact22_x=world_x("J2", 22), j2_contact1_x=world_x("J2", 1),
            pcb12_input="head FFC conductor 1 (= cassette conductor 1) on its -X edge: upper ZIF contact 22; "
                        "travelling +Y in the disc channel at yaw 0, conductor 1 is on the -X side")
    r.finish()


if __name__ == "__main__":
    main()
