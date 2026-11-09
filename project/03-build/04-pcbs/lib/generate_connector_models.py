"""Detailed STEP models for the PCB-08/PCB-14 connectors that KiCad's 3D library lacks.

Drawn from the vendors' customer drawings, in KiCad model coordinates: origin
at the footprint origin on the board top, +Z up, and +Y = -footprint Y (KiCad
footprints are Y-down, models Y-up). Each model is a coloured assembly:
housing, contacts or pins, and the metal retention parts. Outer sizes follow
the drawings; small features without a dimension (cavity chamfers, latch
detail, actuator profile) are representative, so use these for review and
fit, not for tooling.

- Hirose FH34SRJ-22S-0.5SH(99), FH34 catalogue: 13 x 3.8 x 1.0 mm back-flip
  ZIF, 0.5 mm pitch, cable entry at -Y (footprint +Y), contact 1 at +X.
- Molex Micro-Fit 3.0 43045-0621, SD-43045-008 rev H6: 2 x 3 right-angle
  through-hole header, 12.65 wide, 13.67 deep including the 1.40 front lip,
  7.40 high; tails 3.18 below the board; press-fit retention clips.
- Molex Mini-SPOX 5267-03A (22-03-5035), 52670001-SD rev B1: 9.9 x 4.9 mm,
  5.9 high, 1.0 floor, 0.7 walls; pins 3.5 above the floor and 3.5 below.

Run with the project's build123d runtime: writes the .step files next to the
footprints in fh34.pretty/ and pcb08.pretty/.
"""

from pathlib import Path

from build123d import Box, Color, Compound, Cylinder, Location, export_step

HERE = Path(__file__).parent
BLACK = Color(0.07, 0.07, 0.08)
BEIGE = Color(0.86, 0.80, 0.64)
NATURAL = Color(0.95, 0.93, 0.87)
TIN = Color(0.78, 0.78, 0.80)
GOLD = Color(0.85, 0.66, 0.24)


def box(x0, x1, y0, y1, z0, z1):
    return Box(x1 - x0, y1 - y0, z1 - z0).moved(Location(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)))


def part(shape, label, color):
    shape.label, shape.color = label, color
    return shape


def assembly(name, children):
    a = Compound(children=children)
    a.label = name
    return a


def fh34srj_22():
    """Back-flip ZIF. Body x -6.5..6.5, y -1.9..1.9 (entry face at -1.9), z 0..1.0."""
    housing = box(-6.5, 6.5, -1.9, 0.6, 0.0, 0.8)
    housing -= box(-5.75, 5.75, -2.0, 0.2, 0.25, 0.6)              # 11.5 mm FFC slot, 0.35 high
    housing += box(-6.5, -5.9, -1.9, 1.9, 0.0, 1.0)                 # side posts carry the actuator pivots
    housing += box(5.9, 6.5, -1.9, 1.9, 0.0, 1.0)
    housing += box(-5.9, 5.9, 0.6, 1.9, 0.0, 0.3)                   # rear floor under the contact tails
    actuator = box(-5.9, 5.9, 0.15, 1.9, 0.55, 1.0)                 # closed, lying flat over the rear
    actuator -= box(-5.0, 5.0, 1.5, 2.0, 0.85, 1.1)                 # finger lip
    contacts = []
    for k in range(22):
        x = 5.25 - 0.5 * k                                         # contact 1 at +X, as the footprint
        contacts.append(box(x - 0.1, x + 0.1, -0.2, 1.9, 0.3, 0.42))   # beam in the slot
        contacts.append(box(x - 0.1, x + 0.1, 1.0, 1.9, 0.0, 0.3))     # tail down to the pad
    tabs = [box(6.05, 6.45, -1.9, -1.3, 0.0, 0.9), box(-6.45, -6.05, -1.9, -1.3, 0.0, 0.9)]
    return assembly("Hirose FH34SRJ-22S-0.5SH(99)", [
        part(housing, "FH34SRJ housing", BEIGE),
        part(actuator, "FH34SRJ back-flip actuator (closed)", BLACK),
        part(Compound(children=contacts), "FH34SRJ contacts x22", GOLD),
        part(Compound(children=tabs), "FH34SRJ solder tabs", TIN),
    ])


def microfit_43045_0621():
    """2 x 3 right-angle header. Pads 1-3 at y 0, 4-6 at y -3 (model Y); mating face at y +9.42."""
    x0, x1 = 3.0 - 12.65 / 2, 3.0 + 12.65 / 2
    front, rear, h = 9.42, -4.25, 7.40
    housing = box(x0, x1, rear, front, 0.0, h)
    rows = {"A": 2.2, "B": 5.2}                                    # cavity centres: lower row -> pads 1-3
    for z in rows.values():
        for x in (0.0, 3.0, 6.0):
            housing -= box(x - 1.2, x + 1.2, front - 6.0, front + 0.1, z - 1.2, z + 1.2)
            housing -= box(x - 1.2, x - 0.6, front - 6.0, front + 0.1, z + 0.6, z + 1.2)   # polarising corner
    housing -= box(1.4, 4.6, front - 3.0, front + 0.1, h - 0.6, h + 0.1)                 # latch window on top
    ramp = box(2.0, 4.0, front - 2.6, front - 1.2, h - 0.6, h - 0.15)                    # latch ramp in the window
    housing -= box(x0 - 0.1, x1 + 0.1, front - 1.4, front + 0.1, -0.1, 0.5)              # front lip clears the board edge
    pins = []
    for row, z in rows.items():
        y_tail = 0.0 if row == "A" else -3.0
        for x in (0.0, 3.0, 6.0):
            pins.append(box(x - 0.32, x + 0.32, front - 6.0, front - 1.0, z - 0.32, z + 0.32))  # mating pin
            pins.append(box(x - 0.32, x + 0.32, y_tail - 0.32, y_tail + 0.32, -3.18, 0.0))     # tail below the board
    clips = [box(x - 0.8, x + 0.8, 4.32 - 0.15, 4.32 + 0.15, -2.0, 0.6) for x in (-2.15, 8.15)]
    return assembly("Molex Micro-Fit 3.0 43045-0621", [
        part(housing + ramp, "Micro-Fit 43045 housing", BLACK),
        part(Compound(children=pins), "Micro-Fit pins x6", TIN),
        part(Compound(children=clips), "Micro-Fit press-fit retention clips", TIN),
    ])


def minispox_5267_03a():
    """Vertical 3-way header. Pads at x 0, 2.5, 5 on y 0; locking ramp on the +Y wall."""
    x0, x1, y0, y1, h = -2.45, 7.45, -2.31, 2.59, 5.9
    housing = box(x0, x1, y0, y1, 0.0, h)
    housing -= box(x0 + 0.7, x1 - 0.7, y0 + 0.7, y1 - 0.7, 1.0, h + 0.1)                 # open top, 1.0 floor
    housing -= box(1.25, 3.75, y0 - 0.1, y0 + 0.75, 3.4, h + 0.1)                        # polarising slot in the -Y wall
    ramp = box(0.5, 4.5, y1, 3.6, 2.4, h - 0.6) + box(0.5, 4.5, y1, 3.2, h - 0.6, h)     # locking ramp
    pins = [Cylinder(0.32, 8.0).moved(Location((x, 0.0, 1.0 + 3.5 - 4.0))) for x in (0.0, 2.5, 5.0)]
    return assembly("Molex Mini-SPOX 5267-03A", [
        part(housing + ramp, "Mini-SPOX 5267 housing", NATURAL),
        part(Compound(children=pins), "Mini-SPOX pins x3 (3.5 above floor, 3.5 below board)", TIN),
    ])


MODELS = {
    HERE / "fh34.pretty" / "Hirose_FH34SRJ-22S-0.5SH_1x22_P0.50mm.step": fh34srj_22,
    HERE / "pcb08.pretty" / "Molex_Micro-Fit_3.0_43045-0621_2x03-1MP_P3.00mm_Horizontal.step": microfit_43045_0621,
    HERE / "pcb08.pretty" / "Molex_SPOX_5267-03A_1x03_P2.50mm_Vertical.step": minispox_5267_03a,
}

if __name__ == "__main__":
    for out, build in MODELS.items():
        model = build()
        bb = model.bounding_box()
        export_step(model, str(out))
        print(f"{out.name}: x {bb.min.X:.2f}..{bb.max.X:.2f}  y {bb.min.Y:.2f}..{bb.max.Y:.2f}  z {bb.min.Z:.2f}..{bb.max.Z:.2f}")
