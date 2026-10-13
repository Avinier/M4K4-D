# Final v1 — the whole robot

Makad v1 put together: [chassis v1](../../01-chassis/v1/cad/README.md),
[body v1](../../02-body/v1/cad/README.md) and [head v1](../../03-head/v1/cad/README.md).
Each subsystem folder exports only its own parts. This folder is the only
place they are combined. It holds no geometry of its own: both entries import
the live subsystem sources, so a subsystem edit shows up here on the next rebuild.

| Path | Role |
|---|---|
| `cad/makad-v1.step.py` | Inspection assembly: `chassis_v1_reference()` and `build_body_assembly()` from body v1, and the head-v1 parts scene with the yaw drive's moving half, placed at `HEAD_ORIGIN_IN_CHASSIS`. Reservations, harness routes and overlays are kept; the head skin and body shell are translucent. |
| `cad/makad-v1-presentation.step.py` | The same robot as built: every part opaque and in its real finish colour, reservations and overlays left out (D-050). Use it to judge appearance. |
| `cad/finish_colours.py` | The finish palette and part-label rules the presentation entry paints with ([print guide §4](printguide.md#4-colour-scheme)). Add a rule when a printed part is added or renamed. |
| `printguide.md` | Print guide: material, colour and mass of every printed part, for a realistic finished CAD (draft). |
| `cad/snapshots/` | Whole-robot review images. Files named `head-v1-integrated-*` and `head-v1-presentation-*` came from the head folder before this split; they show the same assembly. |

The two `.step` files are about 0.5 GB each, ignored by Git, and regenerated
from source. Build from `cad/` with the project's legacy CAD runtime
(Python 3.13, `cadgen==0.4.28`):

```sh
CAD_PY=/Users/avinier/.codex/runtimes/text-to-cad/0.4.28/venv/bin/python
CAD_GEN=/Users/avinier/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen
# The head source needs its own folder on the path and a serial relief pool;
# without them a build can stall at 0 % CPU.
export MAKAD_RELIEF_SERIAL=1 PYTHONPATH=../../../03-head/v1/cad:../../../02-body/v1/cad
rtk proxy "$CAD_PY" "$CAD_GEN" makad-v1.step.py --write
rtk proxy "$CAD_PY" "$CAD_GEN" makad-v1-presentation.step.py --write
```

The fit, clearance and mass checks stay with the subsystem that owns each
interface. For example, the head-to-body yaw stage is checked by body v1's
`check_yaw_stage.py`, and the head checks by `03-head/v1/cad/run_checks.py`.
This CAD is a geometry and packaging handoff. It is not a fabrication release
or physical proof.
