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
| `cad/pcb_integration.py` | Replaces the six completed boards (nine installed instances) with their rev-A KiCad STEP inputs after droid edits and grouping. Keeps mounting hardware, plugs and cable reserves; omits layout-marked DNP components. Placement datums come from the existing board fit scripts. PCB-09 remains provisional |
| `cad/check_pcb_integration.py` | Checks board/component counts, installed core datums, duplicate placeholder removal, static board-to-board and board-to-robot interferences. Writes `cad/pcb-integration-report.json`; own fixing/plug contacts and PCB-05 spacer/boss contact are excluded explicitly. Existing fit scripts own tolerance and installation-sweep checks |
| `cad/pcbs-integrated.step.py` | Focused review of the nine completed KiCad boards at the same world placements, without the robot or provisional PCB-09 |
| `cad/check_pcb10_jp1_relief.py` | D-068 follow-up: reproduces JP1’s interference with upright 1, proves the local pocket is material removal only, checks remaining material, geometry validity and the sampled installation motion; writes `cad/pcb10-jp1-relief-report.json` |
| `cad/check_pcb_integration_delta.py` | Compares every exported occurrence before/after the JP1 cut; requires the upright to be the sole geometry change with all placements fixed, then combines the full baseline static matrix with the targeted corrected-upright check |
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
| `cad/check_frame_print.py` | D-075, D-076: probes the frame pilots the droid edits resize: J04 rail ends and J11A bosses Ø4.0 (J04 7 mm deep), driver posts Ø3.5, IMU Ø1.6 through the deck; both modules still one solid; the unedited pilots planted. D-076: bed and support area of the three frame prints in their print orientations, and the flat-bottom fills clear of every chassis and body part. Builds the chassis tree twice and the body once, about 15 min. Run it like the builds below |
| `cad/check_frame_assembly.py` | D-077 and the frame page §6: the J13 deck inserts (sockets filled, Ø5.5 pilots, bolt engagement, 45° bosses clear, pin holes through), the rear J04 key walls, and every frame tool path (J04, J11A, J12, J13 including the D-078 hatch notch, J15A, J15B, the post-backing dowel) in the state its step is done in, with planted cases. Builds the chassis tree twice and the body once, about 5 min |
| `cad/chassis-frame.step.py` | Frame print-review view ([04-print frame page](../../../04-print/01-chassis/frame/README.md)): the front module, rear module and hatch with every joint on them, assembled and exploded, one tree group per joint. Builds the chassis tree, about 2 min |
| `cad/check_nose_keel_print.py` | D-079/D-080: final-tree insert pilots, walls and thread engagement; M2 pilots; 1.2 mm shims at the retained sensor datum; shoe roof; real TCRT case support and cradle clearances; PCB-15 slot preservation; valid closed print solids; orientations and planted unedited geometry. `--survey` measures all six bed directions for all seven print types. Add `../../../01-chassis/v1/cad` to `PYTHONPATH` |
| `cad/check_nose_keel_assembly.py` | D-081: final chassis/body tool access and removal per J07–J10 assembly state, keys across corners, all nine insert-iron paths and retained-part blockers. Checks 12 mm lid slide and shortened L-key pod access; body fitted unless stated. Add `../../../01-chassis/v1/cad` to `PYTHONPATH` |
| `cad/nose-keel.step.py` | Nose and keel print-review view ([nose](../../../04-print/01-chassis/nose/README.md) and [keel](../../../04-print/01-chassis/keel/README.md) pages): pod seat, lid, touch cap, keel, wear shoe, TCRT bezel and shims with every J07–J10 joint, assembled and exploded along each fitting direction, one tree group per joint. Builds the chassis tree, about 1 min |
| `cad/export_axle_fab.py` | D-071: writes the non-printed custom axle parts from the final droid geometry to `fab/`: the turned stub `CH-012_stub.step` (axis Z, inboard end at z 0) and the aluminium cap `CH-052_cap.step` and `CH-052_cap.dxf` (laser cut profile). Builds the chassis tree, about 1 min. Run it like the builds below |
| `cad/stub_drawing.py` | D-071: the stub's shop drawing `fab/CH-012_stub_drawing.pdf` (A3, 2:1) from `fab/CH-012_stub.step`. Runs on cadgen 0.6.6's drawing module: `PYTHONPATH=~/.claude/plugins/cache/text-to-cad/cad/0.6.6/packages/cadgen/src` with the legacy venv's Python. Run `export_axle_fab.py` first |
| `fab/` | Fabrication files for parts that are not printed (turned, cut), sent to shops. Generated; regenerate after a change to those parts |
| `cad/pcb09-inputs.step.py` | D-074 focused review: updated PCB-09 core, vendor Pi header and numbered stock socket land markers. Orange overlay highlights the strip extension; this is not a KiCad layout. Build with the legacy runtime like the other entries |
| `cad/check_pcb09_inputs.py` | PCB-09 lesson-1 survey: measures the current board and Pi header, checks all 40 numbered socket lands and an intentionally mirrored case, screens socket edge margin, SOIC/socket copper and GH courtyards, and probes both board faces against the current body/chassis with droid edits. Records open findings in the [board report](../../04-pcbs/pcb-09-c0-link-adapter/mechanical-audit.json); verifies the D-074 strip extension and plants the old failing outline. This is not a release/DRC or insertion pass. Run like the checks below |
| `cad/check_pcb10_mount.py` | D-068: measures the PCB-10 C3 carrier mounting the droid edits make: the Espressif DevKitC v1.1 in place of the generic STEP, pin-tail reliefs, the top-edge hooks, the 2 mm slide and the approach toward the wall, lower-screw access, the board grown to Z 76 with its three connector rows and the real J10-1 (D-068 amended), and the DevKitC against the frame. Builds the chassis and body trees, about 3 min |
| `cad/finish_colours.py` | The finish palette and part-label rules the presentation entry paints with ([print guide §4](printguide.md#4-colour-scheme)). Add a rule when a printed part is added or renamed. |
| `printguide.md` | Print guide: material, colour and mass of every printed part, for a realistic finished CAD (draft). |
| `cad/snapshots/` | Whole-robot review images. Files named `head-v1-integrated-*` and `head-v1-presentation-*` came from the head folder before this split; they show the same assembly. |

## PCB geometry in the whole-robot assembly

The final assembly now calls `pcb_integration.replace_completed_boards()` after applying the droid edits and grouping the custom PCBs. The presentation entry uses the same source. Replacement is confined to this folder; subsystem CAD and released KiCad layouts stay unchanged.

| Board | Geometry installed by the final source | Kept from the CAD installation |
|---|---|---|
| [PCB-05](../../04-pcbs/pcb-05-audio-front-end/README.md) | Rev-A board, fitted components, seven headers and three real spacers; six DNP options omitted | Seven mated plugs; frame bosses and screws remain in their existing assembly groups |
| [PCB-06 ×4](../../04-pcbs/pcb-06-pdm-mic/README.md) | Four copies of the rev-A board/microphone/passives, in the fit check's alternating orientations | Four gaskets, sixteen screw pieces and four pigtail reserves |
| [PCB-10](../../04-pcbs/pcb-10-c3-carrier/README.md) | Rev-A carrier including the DevKitC v1.1 and headers; six DNP options omitted; no second CAD DevKitC | Ten mated plugs, two lower screws (four pieces), existing printed uprights/hooks, including the D-068 JP1 pin relief |
| [PCB-11](../../04-pcbs/pcb-11-status-led/README.md) | Rev-A board, LED, capacitor and resistor in the head's world frame | D-065 crown socket and light pipe |
| [PCB-13](../../04-pcbs/pcb-13-charge-inlet/README.md) | Rev-A board, USB receptacle and fitted circuit | Two mounting screws, D-069 panel relief |
| [PCB-15](../../04-pcbs/pcb-15-nose-hall/README.md) | Rev-A board and fitted parts at the D-063 mid-plane | Seat relief and the magnet/cap mechanism |
| [PCB-09](../../04-pcbs/pcb-09-c0-link-adapter/README.md) | **Provisional placeholder** with the approved strip extension; not a released/populated KiCad board | Socket height, retention, populated fit and routing remain open |

The imported assembly keeps KiCad reference designators, so components remain identifiable. DNP flags are read from the matching `.kicad_pcb`; their optional models are not shown as populated parts. The board STEP files remain in their revision folders under `04-pcbs`, referenced by path rather than copied into the final folder.

**Verification (2026-11-01).** The first combined static check found one interference: PCB-10 JP1’s tails against upright 1 (0.5524 mm³). The [local relief check](cad/pcb10-jp1-relief-report.json) reproduces it, then verifies zero corrected overlap, ≥1.05 mm sampled installation clearance, one valid upright solid, 4.6 mm back material, ≥1.92 mm nominal side strips below the junction with the existing header-row groove and 1.95 mm to the lower screw bore. The released boards and their placements are unchanged. Both robot exports have been rebuilt with this correction. [Final integration verification](cad/pcb-integration-report.json) passes: nine installed boards, no board-to-board interference, and the sole reported robot interference corrected. This combines the [full pre-fix static matrix](cad/pcb-integration-before-relief.json) with an exported-occurrence delta check and the targeted corrected-upright check; it is not a second full-matrix run. All 2,237 occurrence placements remain fixed and 2,236 occurrences are physically unchanged. The nose seat’s render hash also changed, but [exact BRep equivalence](cad/pcb-seat-equivalence.json) confirms identical geometry (identical retained BRep object and zero Boolean difference in both directions).

Reviewed the [whole-robot context snapshot](cad/snapshots/pcbs-integrated-context.png) and the focused boards from [one side](cad/snapshots/pcbs-integrated-only_20261101T063017Z.png) and the [opposite side](cad/snapshots/pcbs-integrated-opposite_20261101T063217Z.png). The [opaque presentation snapshot](cad/snapshots/pcbs-integrated-presentation.png) was also reviewed. The context image emphasizes all custom PCB groups, including unfinished placeholders; the focused scene contains only the six completed designs / nine installed boards.

[PCB model placement readback](cad/pcb-transform-readback.json) checks all 158 populated model groups (nine cores and 149 component groups) against direct OCC transforms. [Geometry validation](cad/pcb-geometry-validation.json) reports zero failures across the focused scene’s 166 leaf occurrences (valid topology, closed solids and positive volume; exhaustive Boolean self-intersection testing was skipped). Fresh PCB-11 socket/light-pipe and PCB-15 full-travel magnet checks pass. The remaining per-board installation/tolerance checks retain their earlier recorded results; they were not all rerun here. Physical received-board and harness acceptance remain open.

**CAD replacement is complete. Physical integration remains open.** Procurement, received-board dimensions, harness dressing and the existing stage-3 bench/assembly items remain open. PCB-09 remains provisional.

The new placement helper copies only a component branch’s wrappers and shares OCC geometry, avoiding the legacy `moved()` parent-copy trap. Intersection checks use world-frame `BRepAlgoAPI_Common`: a planted JP1 collision demonstrates that Python’s nested-Compound Boolean operator can otherwise miss it. The whole-robot source-level inspection/snapshot helpers also showed the legacy parent-copy cost; the focused scene was inspected with the legacy CLI and the whole STEP was rendered with the current artifact-based runtime.

After changing a released board STEP or its layout DNP flags, rebuild both final entries with `--force` and rerun the integration check. The legacy source-closure cache does not make those external inputs authoritative by itself; the integration report records their hashes.

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
