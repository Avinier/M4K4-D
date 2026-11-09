"""Probe the routed PCB-08 STEP and conservative through-hole tails.

The KiCad STEP has a board core, J2/R1, and conservative closed-body J3/J4
envelopes. J1 and J5 bodies still prevent a populated fit release; J6 is a
pair of solder pads whose wire ends are represented by the tail probe.
"""

import sys
from pathlib import Path

from build123d import Location
from cadgen.step_scene import import_step

import module_checks as C
from check_pcb08_zif_stepped import face_boxes

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "04-pcbs" / "tools"))
import kfile as K  # noqa: E402


STEP = "../../../04-pcbs/pcb-08-yaw-junction/cad/pcb-08-yaw-junction-revA.step"
EXPECTED = {"J1", "J2", "J3", "J4", "J5", "R1"}
BOARD = ROOT / "04-pcbs" / "pcb-08-yaw-junction" / "design" / "pcb-08-yaw-junction.kicad_pcb"


def box6(shape):
    b = shape.bounding_box()
    return tuple(round(v, 3) for v in (b.min.X, b.min.Y, b.min.Z,
                                        b.max.X, b.max.Y, b.max.Z))


def xy_overlaps(a, b):
    return a[0] < b[3] and b[0] < a[3] and a[1] < b[4] and b[1] < a[4]


def tail_boxes(underside):
    """Conservative drilled-pad tails: J1 5 mm; J5/J6 3.5 mm.

    XY uses a conservative square around the pad (max pad dimension plus
    0.2 mm). This includes J1's two unnetted plastic/retention pegs.
    """
    b = K.Board(BOARD)
    for ref in ("J1", "J5", "J6"):
        protrusion = 5.0 if ref == "J1" else 3.5
        for p in b.fp(ref)["pads"]:
            if p["kind"] != "thru_hole":
                continue
            x, y = p["at"][0] - 100, 100 - p["at"][1]
            radius = max(p["size"]) / 2 + 0.1
            yield (f"{ref}.{p['num']}", (x-radius, y-radius, underside-protrusion,
                                          x+radius, y+radius, underside))


def main():
    shape = import_step(STEP)
    parts = {c.label: c for c in shape.children if c.solids()}
    core = next(c for name, c in parts.items() if name not in EXPECTED)
    core_z = core.bounding_box().max.Z - core.bounding_box().min.Z
    # KiCad --user-origin 0x0mm: STEP X=KiCad X, Y=-KiCad Y. Nominal 1.6 mm
    # board is centred on the CAD reserve's Z 112.0..113.6 interval.
    loc = Location((-100, 100, 112.0 + (1.6 - core_z) / 2))
    _entry, _tree, leaves = C.droid_tree()
    r = C.Report("check_pcb08_step_fit")
    board = core.moved(loc)
    bb = board.bounding_box()
    r.check("board_outline_matches_cad",
            abs(bb.min.X + 22) < 0.01 and abs(bb.max.X - 20) < 0.01
            and abs(bb.min.Y + 44) < 0.01 and abs(bb.max.Y + 23) < 0.01,
            bounds=box6(board), core_thickness=round(core_z, 3))
    skip = ("YAW_JUNCTION",)
    for label, part in (("board", board), ("J2", parts["J2"].moved(loc)),
                        ("J3", parts["J3"].moved(loc)),
                        ("J4", parts["J4"].moved(loc)),
                        ("R1", parts["R1"].moved(loc))):
        hits = C.clashes(part, leaves, skip=skip)
        # min_gap compares leaf bounding boxes, so the large Pi vendor wrapper
        # reports a false nearest distance; the face survey below handles Pi.
        gap, near = C.min_gap(part, leaves,
                              skip=skip + ("C0_RASPBERRY_PI5_EXACT_STEP",))
        r.check(label + "_external_clearance", not hits,
                clashes=hits, nearest_non_pi=near,
                min_non_pi_gap=round(gap, 3), bounds=box6(part))
    j2 = parts["J2"].moved(loc)
    reserve = C.find(leaves, "YAW_JUNCTION_J8_4_JST_GH_BM06B_HEADER").box
    jb = j2.bounding_box()
    r.check("j2_centered_on_mated_plug_datum",
            abs((jb.min.X + jb.max.X) / 2 - (reserve[0] + reserve[3]) / 2) < 0.02
            and abs((jb.min.Y + jb.max.Y) / 2 - (reserve[1] + reserve[4]) / 2) < 0.02,
            actual=box6(j2), reserve=reserve)
    for ref, x0, x1 in (("J3", 15.7, 19.5), ("J4", 5.86, 9.66)):
        zif = parts[ref].moved(loc)
        zb = zif.bounding_box()
        r.check(ref.lower() + "_closed_body_matches_stepped_probe",
                abs(zb.min.X-x0) < 0.02 and abs(zb.max.X-x1) < 0.02
                and abs(zb.min.Y+40) < 0.02 and abs(zb.max.Y+27) < 0.02
                and abs((zb.max.Z-zb.min.Z)-1.0) < 0.02,
                bounds=box6(zif))

    pi = C.find(leaves, "C0_RASPBERRY_PI5_EXACT_STEP")
    faces = face_boxes(pi.shape)
    board_xy = (bb.min.X, bb.min.Y, bb.min.Z, bb.max.X, bb.max.Y, bb.max.Z)
    under_board = [f for f in faces if xy_overlaps(f, board_xy)]
    highest = max((f[5] for f in under_board), default=None)
    r.check("pi_faces_surveyed_under_whole_board", bool(under_board),
            face_count=len(under_board), highest_face_z=highest,
            board_underside_face_gap=None if highest is None else round(bb.min.Z-highest, 3),
            note="broad Pi bounding-box gap is not a local underside clearance")
    riser = [C.find(leaves, "HARNESS_HEAD_RISER_UPPER_" + suffix)
             for suffix in ("RISE", "TO_J1")]
    lower_riser = C.find(leaves, "HARNESS_HEAD_RISER_LOWER")
    j1_plug = C.find(leaves, "YAW_JUNCTION_J8_1_MICROFIT3_6P_MATED_PLUG")
    route_clashes = [hit for segment in riser for hit in
                     C.clashes(segment.shape, leaves, skip=("HARNESS", "YAW_JUNCTION"))]
    r.check("head_riser_route_reaches_j1_without_solid_clash",
            C.common(lower_riser.shape, riser[0].shape) > 1e-4
            and C.common(riser[0].shape, riser[1].shape) > 1e-4
            and C.common(riser[1].shape, j1_plug.shape) > 1e-4
            and not route_clashes,
            solid_clashes=route_clashes)
    pi_hits, riser_hits, riser_gaps = [], [], []
    for name, tail in tail_boxes(bb.min.Z):
        local = [f for f in faces if xy_overlaps(f, tail)]
        top = max((f[5] for f in local), default=None)
        if top is not None and top >= tail[2]:
            pi_hits.append((name, round(top-tail[2], 3), tuple(round(v, 2) for v in tail)))
        tail_shape = C.blk((tail[0], tail[3], tail[1], tail[4], tail[2], tail[5]))
        for segment in riser:
            if C.common(tail_shape, segment.shape) > 1e-4:
                riser_hits.append((name, segment.label))
            riser_gaps.append((C.distance(tail_shape, segment.shape), name, segment.label))
    r.check("through_hole_tails_clear_pi_faces", not pi_hits,
            protrusion_mm={"J1": 5.0, "J5": 3.5, "J6": 3.5}, collisions=pi_hits)
    min_riser_gap, near_tail, near_segment = min(riser_gaps)
    r.check("through_hole_tails_clear_head_riser_reserve",
            not riser_hits and min_riser_gap >= 0.5,
            reserve_segments={s.label: s.box for s in riser}, collisions=riser_hits,
            min_clearance_mm=round(min_riser_gap, 3), nearest_tail=near_tail,
            nearest_segment=near_segment, required_mm=0.5)
    missing = sorted(EXPECTED - parts.keys())
    r.check("populated_models_present", not missing, missing=missing,
            note="J3/J4 use conservative closed-body envelopes; J1/J5 stock model files are unavailable; J6 has wire-tail envelopes")
    r.finish()


if __name__ == "__main__":
    main()
