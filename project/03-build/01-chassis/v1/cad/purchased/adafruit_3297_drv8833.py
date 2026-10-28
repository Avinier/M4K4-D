"""Build adafruit_3297_drv8833.step from Adafruit's own board file.

Adafruit publishes no STEP for #3297. Its PCB repository does publish the Eagle
board (adafruit/Adafruit-DRV8833-Motor-Driver-Breakout-PCB, commit dda79a8,
"Adafruit DRV8833.brd"). The outline, holes and part placements below are
copied from that file in Eagle millimetres. Component bodies use the nominal
package sizes (HTSSOP-16, 1206, 0805, SOT-23), except the 3.5 mm terminal
block's 8.5 mm height, which is an estimate. Headers are not fitted (#3297 ships
them loose); their through-holes are modeled.

Frame: Eagle X/Y, PCB bottom at Z 0, parts on top.
Run with the text-to-cad 0.4.28 runtime: python adafruit_3297_drv8833.py
"""
from pathlib import Path

from build123d import Box, Color, Compound, Cylinder, Location, Pos, RectangleRounded, Rot, export_step, extrude

PCB_T = 1.6
OUTLINE = (-2.286, 15.494, -1.27, 24.13)  # layer 20, 2.54 mm corner arcs
CORNER_R = 2.54
MOUNT_HOLES = [(12.954, 21.59), (12.954, 1.27)]  # MOUNTINGHOLE_2.5_PLATED
HEADER_HOLES = (
    [(0.254, 11.43 + d) for d in (-8.89, -6.35, -3.81, -1.27, 1.27, 3.81, 6.35, 8.89)]  # JP5 1x8
    + [(12.954, y + d) for y in (6.35, 11.43, 16.51) for d in (-1.27, 1.27)]  # JP2-JP4 1x2
)
PCB_BLUE = Color(0.07, 0.12, 0.30)
BLACK = Color(0.10, 0.10, 0.11)
TAN = Color(0.62, 0.50, 0.33)
TIN = Color(0.78, 0.78, 0.80)
TB_GREEN = Color(0.13, 0.45, 0.25)


def _body(sx, sy, sz, x, y, rot, label, color, z0=PCB_T):
    """Package body centred on its Eagle origin; rot is the Eagle R angle."""
    if rot in (90, 270):
        sx, sy = sy, sx
    part = Box(sx, sy, sz).moved(Location((x, y, z0 + sz / 2.0)))
    part.label, part.color = label, color
    return part


def build():
    x0, x1, y0, y1 = OUTLINE
    board = extrude(RectangleRounded(x1 - x0, y1 - y0, CORNER_R), PCB_T).moved(Location(((x0 + x1) / 2.0, (y0 + y1) / 2.0, 0.0)))
    for x, y in MOUNT_HOLES:
        board -= Cylinder(1.25, 3 * PCB_T).moved(Location((x, y, PCB_T / 2.0)))
    for x, y in HEADER_HOLES + [(7.112 - 1.8, 20.32), (7.112 + 1.7, 20.32)]:  # headers, then J1 pins
        board -= Cylinder(0.5, 3 * PCB_T).moved(Location((x, y, PCB_T / 2.0)))
    board.label, board.color = "ADAFRUIT_3297_PCB", PCB_BLUE

    parts = [board]
    # U1 DRV8833PWPR HTSSOP-16 at (6.858, 9.144) R90: 5.0 x 4.4 x 1.2 body, leads to 6.4 across.
    parts.append(_body(5.0, 4.4, 1.2, 6.858, 9.144, 90, "U1_DRV8833PWP_HTSSOP16", BLACK))
    for side in (-1.0, 1.0):
        parts.append(_body(4.9, 1.0, 0.25, 6.858 + side * 2.7, 9.144, 90, f"U1_LEADS_{'A' if side < 0 else 'B'}", TIN))
    for name, (x, y) in (("R1", (6.096, 2.921)), ("R2", (6.096, 0.508))):
        parts.append(_body(3.2, 1.6, 0.55, x, y, 0, f"{name}_0R2_1206", BLACK))
    for name, x, y, rot, h in (("C1", 2.413, 21.971, 90, 1.25), ("C2", 4.445, 5.207, 0, 1.25),
                               ("C3", 4.064, 14.986, 270, 0.85), ("C4", 5.969, 14.986, 270, 1.25)):
        parts.append(_body(2.0, 1.25, h, x, y, rot, f"{name}_0805", TAN))
    parts.append(_body(2.9, 1.3, 1.0, 9.144, 15.113, 0, "Q1_DMG3415U_SOT23", BLACK))
    # J1 3.5 mm 2-way terminal block at (7.112, 20.32) R180: 7.0 x 7.0 footprint, wire entries on the +Y board edge.
    tb = Box(7.0, 7.0, 8.5).moved(Location((7.112 - 0.1, 20.32 + 0.1, PCB_T + 4.25)))
    for px in (7.112 - 1.8, 7.112 + 1.7):
        tb -= Cylinder(1.3, 2.0).moved(Location((px, 20.32, PCB_T + 8.5)))
        tb -= Box(2.8, 3.0, 2.8).moved(Location((px, 20.32 + 0.1 + 3.5 - 1.4, PCB_T + 3.0)))
    tb.label, tb.color = "J1_VMOTOR_TERMINAL_BLOCK_3P5MM", TB_GREEN
    parts.append(tb)
    return Compound(label="ADAFRUIT_3297_DRV8833", children=parts)


if __name__ == "__main__":
    out = Path(__file__).with_suffix(".step")
    export_step(build(), str(out))
    print(out)
