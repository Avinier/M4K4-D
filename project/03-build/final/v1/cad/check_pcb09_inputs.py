"""PCB-09 lesson-1 survey; records findings, not a board release/DRC pass.

Run with the legacy runtime and PYTHONPATH documented in ../README.md.
Uses the current body + chassis with droid edits, plus the nightly stock lands.
No robot geometry is changed. --output writes the inspectable survey JSON.
"""

import argparse
import importlib.util
import json
import math
import re
from pathlib import Path

from build123d import Compound

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("makad_v1_entry", HERE / "makad-v1.step.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)

import body_v1_model as B
from module_checks import _box, _hit, _leaves

LIB = Path("/Applications/KiCad-nightly/KiCad.app/Contents/SharedSupport/footprints")
SOCKET = "Connector_PinSocket_2.54mm.pretty/PinSocket_2x20_P2.54mm_Vertical.kicad_mod"
SOIC = "Package_SO.pretty/SOIC-8_3.9x4.9mm_P1.27mm.kicad_mod"
GH6 = "Connector_JST.pretty/JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical.kicad_mod"
GH10 = "Connector_JST.pretty/JST_GH_BM10B-GHS-TBT_1x10-1MP_P1.25mm_Vertical.kicad_mod"
EDGE = 0.3
STRIP_PROPOSED_Y1 = 22.4  # D-074 approved edge; asserted against the droid edit


def pads(path):
    return [(n, *map(float, xy.split()), *map(float, wh.split()))
            for n, xy, wh in re.findall(
                r'\(pad "([^\"]*)"[^\n]*\n\s*\(at ([^)]+)\)\n\s*\(size ([^)]+)\)',
                path.read_text())]


def courtyard(path):
    points = []
    for block in re.findall(r'\(fp_line\s.*?\(layer "F.CrtYd"\)\s*\)', path.read_text(), re.S):
        block = block.split("(fp_line")[-1]
        points += [tuple(map(float, p)) for p in re.findall(
            r'\((?:start|end) ([-\d.]+) ([-\d.]+)\)', block)]
    return (min(x for x, y in points), min(y for x, y in points),
            max(x for x, y in points), max(y for x, y in points))


def xy_rect(box):
    x0, x1, y0, y1, _, _ = box
    return x0, y0, x1, y1


def supported(pad, rectangles, extra=0):
    _, x, y, w, h = pad
    # Bounding rectangles are conservative for round/rounded pads. Here all
    # failing socket disks actually cross the straight +Y strip edge.
    return all(any(a <= px <= c and b <= py <= d for a, b, c, d in rectangles)
               for px in (x-w/2-extra, x+w/2+extra)
               for py in (y-h/2-extra, y+h/2+extra))


def disk_rect_hit(cx, cy, radius, x, y, w, h):
    dx, dy = max(abs(cx-x)-w/2, 0), max(abs(cy-y)-h/2, 0)
    return dx*dx + dy*dy < radius*radius - 1e-8


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print("Building body and chassis with current droid edits...", flush=True)
    robot = entry._apply_droid_cuts(Compound(children=[entry.chassis_v1_reference(),
                                                     entry.build_body_assembly()]), strict=False)
    parts = [("/".join(p), entry._shifted(n, loc), _box(n.wrapped.Moved(loc.wrapped)))
             for p, n, loc in _leaves(robot)]
    get = lambda label: next(n for p, n, b in parts if p.endswith(label))
    core = get("C0_LINK_ADAPTER_PCB09_BOARD")
    # Read the standalone vendor Pi (no parent-tree deepcopy). Select its header
    # by its 50.8 x 5 mm geometry rather than relying on a vendor solid index.
    pi = B.raspberry_pi5()
    candidates = [s for s in pi.solids() if
                  abs((_box(s)[3]-_box(s)[0])-50.8) < 0.001 and
                  abs((_box(s)[4]-_box(s)[1])-5.0) < 0.001]
    assert len(candidates) == 1, "Pi vendor header changed; re-establish the datum"
    header = candidates[0]
    hb = _box(header)
    x1 = (hb[0]+hb[3])/2 - 19*2.54/2
    y1 = (hb[1]+hb[4])/2 - 2.54/2
    # Official Pi top-view pin numbering: pin 1 is the inner row at the end
    # away from USB/Ethernet (world -X). Pin 2 is outboard, toward +Y.
    lands = pads(LIB/SOCKET)
    assert len(lands) == 40
    placed = [(n, x1+y, y1-x, w, h) for n, x, y, w, h in lands]
    expected = {str(n): (x1+((n-1)//2)*2.54, y1+((n-1)%2)*2.54) for n in range(1, 41)}
    assert all(math.dist((x, y), expected[n]) < 1e-6 for n, x, y, w, h in placed)
    # A wrong row reflection must fail the numbered mating-grid check.
    wrong = [(n, x1+y, y1+x) for n, x, y, w, h in lands]
    mirrored_errors = [n for n, x, y in wrong if math.dist((x, y), expected[n]) > 0.01]
    assert len(mirrored_errors) == 20
    original = [xy_rect(b) for b in (B.C0_LINK_ADAPTER_STRIP, B.C0_LINK_ADAPTER_BRIDGE,
                                  B.C0_LINK_ADAPTER_BOX)]
    actual = [tuple(r) for r in original]
    growth = next(value for pattern, value in entry.DROID_ADDS
                  if pattern == r"C0_LINK_ADAPTER_PCB09_BOARD")
    assert abs(growth[3]-STRIP_PROPOSED_Y1) < 1e-9
    actual[0] = (*actual[0][:3], growth[3])
    proposed = actual
    outside = [n for n, *v in placed if not supported((n, *v), actual)]
    edge_fail = [n for n, *v in placed if not supported((n, *v), actual, EDGE)]
    planted = [n for n, *v in placed if not supported((n, *v), original, EDGE)]
    assert planted == [str(n) for n in range(2, 33, 2)]
    assert not outside and not edge_fail
    assert all(supported(p, proposed, EDGE) for p in placed)
    old_core = B._c0_link_adapter().children[0]
    assert len(core.solids()) == 1
    # D-092 adds two standoff tabs and the bay extension beyond the D-074 growth; count only D-074's here.
    tabs = sum((x1-x0)*(y1-y0)*1.6 for x0, x1, y0, y1 in
               (*entry.PCB09_MOUNT["tabs"], entry.PCB09_MOUNT["bay_extension"]))
    added = core.volume-old_core.volume-tabs
    assert abs(added-40.7*1.5*1.6) < 1e-4
    # Check a real SOIC-8 at the old SOIC-14 placeholder's centre. A roundrect
    # contains a full-height central rectangle (corner radius = 0.15 mm), so
    # disk hits against that rectangle are definite copper collisions.
    collisions = {}
    head_box = _box(get("C0_THVD1451_HEAD_LINK_SOIC14"))
    cx, cy = (head_box[0]+head_box[3])/2, (head_box[1]+head_box[4])/2
    for angle in (0, 90):
        hit = []
        for un, ux, uy, uw, uh in pads(LIB/SOIC):
            # Convert library y-down to world y-up, then rotate in world XY.
            x, y = (ux, -uy) if angle == 0 else (uy, ux)
            w, h = (uw-0.3, uh) if angle == 0 else (uh, uw-0.3)
            for sn, sx, sy, sw, sh in placed:
                if disk_rect_hit(sx, sy, sw/2, cx+x, cy+y, w, h):
                    hit.append({"soic_pad": un, "header_pin": sn})
        collisions[str(angle)] = hit
    assert all(collisions.values()), "Revisit the old head-IC placement finding"
    gh6, gh10 = courtyard(LIB/GH6), courtyard(LIB/GH10)
    j2 = _box(get("C0_J9_2_JST_GH_BM06B_HEADER"))
    j3 = _box(get("C0_J9_3_JST_GH_BM10B_HEADER"))
    row_pitch = j3[1]-j2[1]
    # Same orientation/family and identical library Y extents: model-minimum
    # separation is footprint-origin separation, without guessing an origin.
    assert abs(gh6[1]-gh10[1]) < 1e-9 and abs(gh6[3]-gh10[3]) < 1e-9
    probes = {
        "original_core": old_core, "current_core": core,
        "above_strip": entry._blk(-4.7,36,16.3,22.4,108.001,128),
        "below_strip": entry._blk(-4.7,36,16.3,22.4,96.4,106.399),
        "above_bay": entry._blk(36,66,22.5,39,108.001,128),
        "below_bay": entry._blk(36,66,22.5,39,96.4,106.399),
    }
    hits = {}
    for tag, probe in probes.items():
        found = []
        pb = _box(probe)
        for path, part, box in parts:
            if "C0_LINK_ADAPTER" in path or "C0_GPIO_" in path or not _hit(pb, box):
                continue
            common = probe & part
            volume = 0 if common is None else sum(s.volume for s in common.solids())
            if volume > 0.001:
                found.append({"part": path, "volume_mm3": volume, "bbox": _box(common)})
        hits[tag] = found
        print(f"{tag}: {len(found)} intersecting solids/reserves", flush=True)
    assert not hits["current_core"], "Extended core clashes with the current body/chassis"
    fan = _box(get("C0_LINK_ADAPTER_J94_FAN_XH2_PLUG_RESERVE"))
    base = _box(get("C0_THVD1451_BASE_LINK_SOIC14"))
    result = {
        "status": "D-074 strip extension verified; other mechanical inputs OPEN",
        "scope": "static body/chassis geometry; no head build, motion sweep, final footprints or insertion proof",
        "core_bbox": _box(core), "core_volume_mm3": core.volume,
        "outline_rectangles_xy": actual, "plate_z": B.C0_LINK_ADAPTER_PLATE_Z,
        "added_core_volume_mm3": added, "core_solid_count": len(core.solids()),
        "pi_header_bbox": hb,
        "pin_centres": {n: [x, y] for n, x, y, w, h in placed},
        "socket_footprint": str(LIB/SOCKET), "socket_pad_size_mm": [1.7, 1.7],
        "socket_pad_diameter_source": "nightly stock footprint; final socket MPN not selected",
        "mirrored_numbering_errors_detected": mirrored_errors,
        "socket_pads_outside_existing_core": outside,
        "socket_pads_failing_0p3_edge": edge_fail,
        "planted_original_strip_edge_failures": planted,
        "required_strip_y1_for_copper_edge_mm": y1+2.54+0.85+EDGE,
        "extended_strip_y1_mm": STRIP_PROPOSED_Y1,
        "socket_pad_edge_screen": "all 40 pass at 0.3 mm",
        "head_soic8_at_old_centre": {"centre": [cx, cy], "definite_copper_hits": collisions},
        "gh_row_pitch_mm": row_pitch, "gh_courtyard_height_mm": gh6[3]-gh6[1],
        "gh_courtyard_overlap_mm": gh6[3]-gh6[1]-row_pitch,
        "base_ic_box_overlaps_fan_connector_reserve": _hit(base, fan),
        "core_and_face_probe_intersections": hits,
        "header_tip_to_core_bottom_mm": B.C0_LINK_ADAPTER_PLATE_Z[0]-hb[5],
        "socket_installed_height": "OPEN: body box is not a selected mating socket",
        "board_retention": "OPEN: no dedicated PCB-09 fixings in the current model",
    }
    text = json.dumps(result, indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
        print(f"Survey saved: {args.output}", flush=True)
    else:
        print(text)
    print("Survey completed; OPEN findings are not DRC or release passes.", flush=True)


if __name__ == "__main__":
    main()
