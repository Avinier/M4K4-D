# Final v1 — the whole robot

Makad v1 put together: [chassis v1](../../01-chassis/v1/cad/README.md),
[body v1](../../02-body/v1/cad/README.md) and [head v1](../../03-head/v1/cad/README.md).
Each subsystem folder exports only its own parts. This folder is the only
place they are combined. Both entries import the live subsystem sources, so a
subsystem edit shows up here on the next rebuild. From 2026-10-14 the droid's CAD
changes are also made here and nowhere else ([04-pcbs rules](../../04-pcbs/README.md#rules)).
In `makad-v1.step.py`, `DROID_CUTS` cuts material from parts as the droid is built, `DROID_ADDS` adds material to them and `DROID_MOVES` shifts them ([D-063](../../decisions.md#d-063)). An entry is a world-frame box or, since [D-065](../../decisions.md#d-065), a world-frame shape. `PRINT_STATES` lists parts printed in another state than the assembly shows, such as the stretched tyre ([D-070](../../decisions.md#d-070)), and `PRINT_TOOLS` the printed tools that are not robot parts, such as the axle alignment plug ([D-071](../../decisions.md#d-071)); the STL export uses both. Check scripts that build one subsystem tree call `_apply_droid_cuts(tree, strict=False)`, which skips entries for parts outside that tree.
The subsystem checks don't see these changes, so each one has a check script here.

| Path | Role |
|---|---|
| `cad/makad-v1.step.py` | Inspection assembly: `chassis_v1_reference()` and `build_body_assembly()` from body v1, and the head-v1 parts scene with the yaw drive's moving half, placed at `HEAD_ORIGIN_IN_CHASSIS`. Reservations, harness routes and overlays are kept; the head skin and body shell are translucent. The custom boards of the [04-pcbs register](../../04-pcbs/README.md#board-register) are pulled out of the subsystem trees into one top-level `Custom PCBs` group, one subgroup per board, at their installed positions (`CUSTOM_PCBS` in the entry). Their connector and plug reservations stay in the body tree. |
| `cad/makad-v1-presentation.step.py` | The same robot as built: every part opaque and in its real finish colour, reservations and overlays left out (D-050). Use it to judge appearance. |
| `cad/check_pcb15_relief.py` | Measures the PCB-15 seat relief and the moved board slot ([D-059](../../decisions.md#d-059), [D-063](../../decisions.md#d-063)) on the chassis tree, about 40 s. Run it like the builds below |
| `cad/check_pcb15_fit.py` | Places PCB-15's KiCad board STEP in the nose seat and measures it against the seat and the magnet at the cap stop, about 25 s. Run it like the builds below |
| `cad/check_pcb11_socket.py` | Measures the PCB-11 LED socket that `DROID_ADDS` fuses inside the crown ([D-065](../../decisions.md#d-065)). It checks the fusion, the board pocket and shoulder, the light-pipe lip and bore, room for the front parts, clearance to every other head part, the rear wire zone and the board's way in. It builds the head parts only, about 1.5 min. Run it like the builds below |
| `cad/check_pcb05_mount.py` | D-067: measures the PCB-05 fixing the droid edits make: three frame bosses fused into the frame print, open bores with 1 mm walls, screw seats and thread engagement, the spacers clear of the edge connectors, the install slide from the front, and the driver paths from above. Builds the chassis and body trees, about 28 min |
| `cad/check_pcb05_fit.py` | Places PCB-05's KiCad board STEP where the droid has the board and measures it: outline, spacers on the fixing points, connector faces against the CAD headers, parts inside the CAD reserve, every part clear of the droid and of other reserves, J7's clipped tails over the Pi, and the install slide with the real parts. Builds the chassis and body trees, about 8 min |
| `cad/check_pcb06_fit.py` | Places PCB-06's KiCad board STEP on all four shell bosses (two turned over) and measures it: outline and holes against the CAD placeholder, MK1 on the port, the seat, static clearance and the shell's lowering path with datasheet part heights. Builds the body parts only, about 8 min |
| `cad/check_pcb11_fit.py` | Places PCB-11's KiCad board STEP in the D-065 crown socket and measures it: the pocket, the LED on the pipe axis and its clearance to the lip, the back parts against the camera bracket, and every other head part. Builds the head parts only, about 1.5 min |
| `cad/check_wheel_print.py` | D-070: measures the wheel print fixes the droid edits make: the hub-cap pegs moved onto the hub and the cap's flat underside, the cap clear of the rim and screws, the print-orientation overhangs of the rim and cap, one STL per wheel part for both sides, and the tyre's print state (`PRINT_STATES`). Builds the chassis tree, about 1 min. Run it like the builds below |
| `cad/check_axle_stack.py` | D-071: measures the axle-stack fixes the droid edits make: the Ø21 stub flange, a straight key to every housing screw with the stub in, the Ø3.2 housing holes, the set-screw key notch, the alignment plug's fits and its clear face-screw key paths, the print orientations, and (D-072) the M3 × 16 housing-screw tips and insert engagement, and the motor-alignment error budget, with planted cases. Builds the chassis tree twice, about 1.5 min. Run it like the builds below |
| `cad/axle-alignment.step.py` | D-071 view: the left axle at the motor-alignment step (plug and keys in) beside the finished stack. Builds the chassis tree, about 2 min |
| `cad/check_frame_print.py` | D-073, D-074: probes the frame pilots the droid edits resize: J04 rail ends and J11A bosses Ø4.0 (J04 7 mm deep), driver posts Ø3.5, IMU Ø1.6 through the deck; both modules still one solid; the unedited pilots planted. D-074: bed and support area of the three frame prints in their print orientations, and the flat-bottom fills clear of every chassis and body part. Builds the chassis tree twice and the body once, about 15 min. Run it like the builds below |
| `cad/check_frame_assembly.py` | D-075 and the frame page §6: the J13 deck inserts (sockets filled, Ø5.5 pilots, bolt engagement, 45° bosses clear, pin holes through), the rear J04 key walls, and every frame tool path (J04, J11A, J12, J13 including the D-076 hatch notch, J15A, J15B, the post-backing dowel) in the state its step is done in, with planted cases. Builds the chassis tree twice and the body once, about 5 min |
| `cad/chassis-frame.step.py` | Frame print-review view ([04-print frame page](../../../04-print/01-chassis/frame/README.md)): the front module, rear module and hatch with every joint on them, assembled and exploded, one tree group per joint. Builds the chassis tree, about 2 min |
| `cad/check_nose_keel_print.py` | D-077/D-078: final-tree insert pilots, walls and thread engagement; M2 pilots; 1.2 mm shims at the retained sensor datum; shoe roof; real TCRT case support and cradle clearances; PCB-15 slot preservation; valid closed print solids; orientations and planted unedited geometry. `--survey` measures all six bed directions for all seven print types. Add `../../../01-chassis/v1/cad` to `PYTHONPATH` |
| `cad/check_nose_keel_assembly.py` | D-079: final chassis/body tool access and removal per J07–J10 assembly state, keys across corners, all nine insert-iron paths and retained-part blockers. Checks 12 mm lid slide and shortened L-key pod access; body fitted unless stated. Add `../../../01-chassis/v1/cad` to `PYTHONPATH` |
| `cad/nose-keel.step.py` | Nose and keel print-review view ([nose](../../../04-print/01-chassis/nose/README.md) and [keel](../../../04-print/01-chassis/keel/README.md) pages): pod seat, lid, touch cap, keel, wear shoe, TCRT bezel and shims with every J07–J10 joint, assembled and exploded along each fitting direction, one tree group per joint. Builds the chassis tree, about 1 min |
| `cad/export_axle_fab.py` | D-071: writes the non-printed custom axle parts from the final droid geometry to `fab/`: the turned stub `CH-012_stub.step` (axis Z, inboard end at z 0) and the aluminium cap `CH-052_cap.step` and `CH-052_cap.dxf` (laser cut profile). Builds the chassis tree, about 1 min. Run it like the builds below |
| `cad/stub_drawing.py` | D-071: the stub's shop drawing `fab/CH-012_stub_drawing.pdf` (A3, 2:1) from `fab/CH-012_stub.step`. Runs on cadgen 0.6.6's drawing module: `PYTHONPATH=~/.claude/plugins/cache/text-to-cad/cad/0.6.6/packages/cadgen/src` with the legacy venv's Python. Run `export_axle_fab.py` first |
| `fab/` | Fabrication files for parts that are not printed (turned, cut), sent to shops. Generated; regenerate after a change to those parts |
| `cad/check_pcb10_mount.py` | D-068: measures the PCB-10 C3 carrier mounting the droid edits make: the Espressif DevKitC v1.1 in place of the generic STEP, pin-tail reliefs, the top-edge hooks, the 2 mm slide and the approach toward the wall, lower-screw access, the board grown to Z 76 with its three connector rows and the real J10-1 (D-068 amended), and the DevKitC against the frame. Builds the chassis and body trees, about 3 min |
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
