"""D-074 review: current PCB-09 core and the numbered socket land screen.

Uses the project's legacy gen_step runtime, as the final assembly does. This is
an inspection scene, not a KiCad board export: the gold lands are markers, and
the orange overlay highlights the added strip. The Pi header is vendor geometry.
The final socket body, circuit parts, drill holes and mounting are not designed.
"""

import importlib.util
from pathlib import Path
import sys

from build123d import Color, Compound, Cylinder, Location

spec = importlib.util.spec_from_file_location("makad_v1_entry", Path(__file__).with_name("makad-v1.step.py"))
entry = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = entry
spec.loader.exec_module(entry)

import body_v1_model as B
from module_checks import _box


def gen_step():
    adapter = entry._apply_droid_cuts(Compound(children=[B._c0_link_adapter()]), strict=False)
    core = next(n for n in adapter.children[0].children if n.label == "C0_LINK_ADAPTER_PCB09_BOARD")
    core.color = Color(0.12, 0.39, 0.24, 1)
    header = next(s for s in B.raspberry_pi5().solids()
                  if abs((_box(s)[3]-_box(s)[0])-50.8) < 0.001
                  and abs((_box(s)[4]-_box(s)[1])-5.0) < 0.001)
    header.label, header.color = "Pi_40_pin_header_reference", Color(0.32, 0.34, 0.37, 1)
    hb = _box(header)
    x1 = (hb[0]+hb[3])/2-19*2.54/2
    y1 = (hb[1]+hb[4])/2-2.54/2
    overlay = entry._blk(-4.7, 36., 20.9, 22.4, 108.001, 108.021)
    overlay.label, overlay.color = "D074_added_strip_highlight_only", Color(0.95, 0.48, 0.12, 1)
    lands = []
    for n in range(1, 41):
        x, y = x1+((n-1)//2)*2.54, y1+((n-1)%2)*2.54
        land = Cylinder(0.85, 0.035).moved(Location((x, y, 108.045)))
        land.label = f"Socket_land_marker_pin_{n:02d}"
        land.color = Color(0.96, 0.79, 0.22, 1) if n != 1 else Color(0.90, 0.25, 0.16, 1)
        lands.append(land)
    return {"shape": Compound(label="PCB09_D074_input_review_NOT_A_BOARD_RELEASE",
                               children=[core, header, overlay, *lands])}
