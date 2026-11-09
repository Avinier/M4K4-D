"""Generate a conservative closed-state FH34SRJ-22S body STEP.

The solid uses Hirose's published 13 x 3.8 x 1.0 mm envelope and the
footprint origin at board top. It includes the closed actuator within that
envelope; the opened actuator and mated FFC remain separate CAD probes.
Run with the project's build123d/CAD Python runtime.
"""

from pathlib import Path

from build123d import Box, Location, export_step

NAME = "Hirose_FH34SRJ-22S-0.5SH_1x22_P0.50mm"
OUT = Path(__file__).parent / "fh34.pretty" / f"{NAME}.step"

body = Box(13.0, 3.8, 1.0).moved(Location((0, 0, 0.5)))
body.label = "FH34SRJ-22S closed housing and actuator envelope"
export_step(body, str(OUT))
print(OUT)
