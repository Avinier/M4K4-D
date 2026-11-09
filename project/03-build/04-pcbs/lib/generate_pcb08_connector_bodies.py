"""Generate conservative closed-body STEP envelopes for PCB-08 J1 and J5.

KiCad's released 3D library has no model for either part. Each body is a
box: XY is the stock footprint's F.Fab outline (which already includes the
retention clips and housing flanges, so it is larger than the housing), and
the height is the housing height from the Molex customer drawing. KiCad
models use +Y up where footprints use +Y down, so the Fab Y range is negated.
Tails below the board are not modelled here; check_pcb08_step_fit.py adds
them as tail envelopes.

- J1, Micro-Fit 3.0 43045-0621 (SD-43045-008 rev H6): 12.65 wide, 12.24 long,
  housing 7.40 above the PCB; tails 3.18 below a 1.57 board, clip 4.60 +/- 0.30.
- J5, Mini-SPOX 5267-03A / 22035035 (52670001-SD rev B1): 9.9 +/- 0.2 long,
  4.9 deep, 5.9 above the PCB; tails 3.5 +/- 0.6 below.

Run with the project's build123d runtime.
"""

from pathlib import Path

from build123d import Box, Location, export_step

HERE = Path(__file__).parent
BODIES = {
    # name: (Fab x0, x1, y0, y1 in footprint coordinates, height)
    "Molex_Micro-Fit_3.0_43045-0621_2x03-1MP_P3.00mm_Horizontal": (-4.36, 10.36, -9.42, 4.25, 7.40),
    "Molex_SPOX_5267-03A_1x03_P2.50mm_Vertical": (-2.95, 7.95, -3.60, 2.31, 5.90),
}

for name, (x0, x1, y0, y1, h) in BODIES.items():
    body = Box(x1 - x0, y1 - y0, h).moved(Location(((x0 + x1) / 2, -(y0 + y1) / 2, h / 2)))
    body.label = f"{name} closed-body envelope (Molex drawing height, Fab outline)"
    out = HERE / "pcb08.pretty" / f"{name}.step"
    export_step(body, str(out))
    print(out.name)
