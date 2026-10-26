# Final v1 — the whole robot

Makad v1 put together: [chassis v1](../../01-chassis/v1/cad/README.md),
[body v1](../../02-body/v1/cad/README.md) and [head v1](../../03-head/v1/cad/README.md).
Each subsystem folder exports only its own parts. This folder is the only
place they are combined. Both entries import the live subsystem sources, so a
subsystem edit shows up here on the next rebuild. From 2026-10-14 the droid's CAD
changes are also made here and nowhere else ([04-pcbs rules](../../04-pcbs/README.md#rules)).
In `makad-v1.step.py`, `DROID_CUTS` cuts material from parts as the droid is built, `DROID_ADDS` adds material to them and `DROID_MOVES` shifts them ([D-063](../../decisions.md#d-063)). An entry is a world-frame box or, since [D-065](../../decisions.md#d-065), a world-frame shape. Check scripts that build one subsystem tree call `_apply_droid_cuts(tree, strict=False)`, which skips entries for parts outside that tree.
The subsystem checks don't see these changes, so each one has a check script here.

| Path | Role |
|---|---|
| `cad/makad-v1.step.py` | Inspection assembly: `chassis_v1_reference()` and `build_body_assembly()` from body v1, and the head-v1 parts scene with the yaw drive's moving half, placed at `HEAD_ORIGIN_IN_CHASSIS`. Reservations, harness routes and overlays are kept; the head skin and body shell are translucent. The custom boards of the [04-pcbs register](../../04-pcbs/README.md#board-register) are pulled out of the subsystem trees into one top-level `Custom PCBs` group, one subgroup per board, at their installed positions (`CUSTOM_PCBS` in the entry). Their connector and plug reservations stay in the body tree. |
| `cad/makad-v1-presentation.step.py` | The same robot as built: every part opaque and in its real finish colour, reservations and overlays left out (D-050). Use it to judge appearance. |
| `cad/check_pcb15_relief.py` | Measures the PCB-15 seat relief and the moved board slot ([D-059](../../decisions.md#d-059), [D-063](../../decisions.md#d-063)) on the chassis tree, about 40 s. Run it like the builds below |
| `cad/check_pcb15_fit.py` | Places PCB-15's KiCad board STEP in the nose seat and measures it against the seat and the magnet at the cap stop, about 25 s. Run it like the builds below |
| `cad/check_pcb11_socket.py` | Measures the PCB-11 LED socket that `DROID_ADDS` fuses inside the crown ([D-065](../../decisions.md#d-065)). It checks the fusion, the board pocket and shoulder, the light-pipe lip and bore, room for the front parts, clearance to every other head part, the rear wire zone and the board's way in. It builds the head parts only, about 1.5 min. Run it like the builds below |
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
