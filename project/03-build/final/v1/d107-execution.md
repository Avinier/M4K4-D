# D107 execution record — corrected2026-11-14

The [plan](../../head-umbilical-plan.md) Levels3–6 and the builder’s four functional corrections are implemented in final-assembly CAD and PCB08 rev B. The [correction record](d107-corrections.md) gives load assumptions, proof procedure, sources and receipt gates. Hardware remains **HOLD**. No procurement, print qualification, powered thermal/camera test or measured mass is claimed.

## Current implementation

- Removed cassette stator/ribbons, four PCB14s, PCB16, D104 hollow leg/trunnion and D105 mast/long loop. Restored D051 solid pivot, bearing, retainer and leg; retained steel ballast. Six custom boards remain:08/09 rev B and10/11/12/15 rev A. Head/body subsystem CAD sources are untouched; all mechanical edits are final-assembly-owned.
- W47 carries twelve individual wires plus stripped HDMI pairs through the yaw axis. The95mm nominalØ7 neck span reaches a split clamp at head-local(−50.4,0,6), through a34×30.2mm lower-skin opening. The jaw has twoM2×8, twoM2×3 inserts and0.25mm silicone pads. Repack/tape the bundle to6.8±0.05mm; revise an oversize clamp fit instead of crushing pairs.
- PCB08 now hangs from a9.6×18mm web with deep front/rear beams and a second upper rear-crossrail connection. Its body saddle has a6.4×9.4mm gusset throat. The keeper/M2×4 provides rigid capture in six directions. Simplified section/load checks assume20MPa printed-PETG credit with factor2 at50N connector/40N cable service loads; these are not measured strength or FEA. Solid roots and100N first-print proof are mandatory.
- The rotor liner has an OD24.8 flange at worldZ137…138 seated on the rotor top, with102.92mm² bearing land. It cannot drop onto the Pi. Remove the disc bushing before lifting the liner. Both inserts give a finishedØ18 passage inside the bareØ21 bore.
- HD-023 is one B0091 kit for both adapters; HD-028 is the separately counted slim HDMI cable. The adapters retain their documented25.2×27.83×12.62mm envelopes and2.5mm ties. HD-026 is a separate150mm15-way head ribbon; HD-027 is a separate150mm15-to22 Pi5 FPC. The kit’s60mm15-way ribbon fails the63.36mm straight span and111.20mm routed head run. Pi route59.97mm; both budgets include10mm socket insertion and15mm service. Actual contact faces, bends and excess-length dress remain U.
- The servo roll-frame anchor is(−28,−12,46), with a30mm free loop. Actual securing/dressing of flexible leads remains a first-motion gate. The CAD loop clears the PCB12 screw by1.5418mm across85 roll positions at0.5° spacing, replacing the former0.1794mm rub zone.

## Electrical and fabrication evidence

J3/J8-9 Micro-Fit2×3 mirrors J1/J8-1 pin for pin. J4/J8-10 GH6 is GND_SIG,C0TX+,C0TX−,C2TX−,C2TX+,SERVO_DATA. Yaw J8-8, W17 and R1 remain. The three power returns remain separate on PCB08; PCB12’s local bonds are unchanged.

Rev B is34×25×1.6mm, four layers with **>=35µm finished copper including inner layers**. Dedicated solid +6V3_HEAD_PR In1 and GND_HEAD In2 fills connect pads solidly around the1mm seed tracks. Yaw supply/return use1.5mm outer tracks. No shared ground plane is introduced. Require written fab copper confirmation;17.5µm is not an approved substitution.

| Evidence | Result |
|---|---|
| ERC |0 errors /0 warnings |
| Saved-board parity DRC |0 errors /0 unconnected /0 parity differences; same6 library-copy warnings |
| Exported net audit |12/12,32 connected pins,0 manifest differences |
| W47/PCB12 audit |5/5 |
| Reproducible pad audit |9/9 library land patterns match after rotation normalization |
| Filled copper audit |PASS; positive/return664.78/670.85mm²; separate nets, solid connections,35µm inner stack,1.5mm yaw paths |
| Resistance/loss screen |At35µm/60°C,2.013/2.708mΩ positive/return;11.33mV and0.0272W total at2.4A, excluding barrels/contacts/solder |

The resistor-sheet result is not a temperature prediction. N2(b) must measure actual closed-body PCB temperature and terminal voltage. The17.5µm adverse scenario doubles loss and remains unapproved. Gerbers, drill, placements, BOM, schematic/netlist and STEP were regenerated in [fab/revB](../../04-pcbs/pcb-08-yaw-junction/fab/revB/README.md); rev A is historical. Reproduce using `layout_pcb08.py`, `export_revB.py`, `audit_netlist.py`, `audit_w47.py`, `audit_pads.py` and `audit_power_copper.py` in the design directory.

## Targeted CAD evidence

| Report | Current result |
|---|---|
| [Neck](cad/check_d107_neck-report.json) |13/13;45 poses, full paths, internal leads and static head ribbon |
| [Body](cad/check_d107_body-report.json) |31/31; populated rev B, five plugs, frame/mounts, wires, Pi FPC and service |
| [Seating](cad/check_d107_seating-report.json) |7/7; includes liner flange downward capture and continuousØ18 bore |
| [Controller hardware](cad/check_d107_controller_mount-report.json) |2/2;85 roll positions;1.5418mm screw minimum, no position below1mm |
| [Functional](cad/check_d107_functional-report.json) |9/9; actual frame roots/sections, load screens, board capture and bought ribbon reach |
| [Mass](cad/check_d107_mass-report.json) |3/3 numerical criteria; sensitivity below3% in the original register is explicitly OPEN, not a release pass |
| [PCB12](cad/check_pcb12_fit-report.json) |7/7; existing land/interface/service/motion checks |

Neck bundle Y/P/R gaps are6.0652/4.2553/3.6833mm; opening margin4.6101mm;95mm span versus70.6785mm longest chord; minimum candidate bend9.5234mm. Solver residual8.9697 is recorded: force/torque estimates are not an equilibrium certificate. Head camera/clamp to pitch/yaw minimum2.1397mm. The hard jaw is intentionally near the bundle; silicone grip is physical acceptance. These nominal/discrete checks do not certify tolerance, flex equilibrium, fatigue or actual cable life.

PCB08 removal: shell and rear panel off; release harness slack; unplug all five; remove M2×4 and keeper; tilt front15°, slide+Y6mm, withdraw−X60mm. Micro-Fit demating reserves6mm straight pull. Common body bundle clears mounts by0.5mm; the FPC passes below the reinforced front beam in its slot and around the rear beam atY−39.

The16×7mm HDMI envelope is arithmetic only: diagonal17.464mm versusØ18,0.268mm radial reserve. **Buy and measure the entire plug/latch/boot before printing closed inserts.** If it fails, unplug at the head or separately design/check split inserts for the bareØ21 bore. No split-insert design is released here.

## Mass method and open sensitivity

The ledger starts at D095 before D104/105 and includes larger supports, liner flange, Pi FPC and added fill copper. No removed assembly is subtracted twice. Estimated total2655.04g, neutral CoM(18.651,0.788,110.152)mm. Actual signed frame centroids swept at1° pitch/roll to hard stops and full360° yaw give1.6549m/s² versus1.5823 minimum:4.5922% margin; steel retained. Copper comparison6.1546%.

The unchanged original D095 register algorithm gives3.4707%. Adding all10g at the head adapter gives3.4683% in the moving-frame sweep but **2.3844% in the original register**, below the3% restoration buffer (above1.5% operating minimum). That old calculation freezes source-head radii and treats deltas as stationary; both outputs are retained with their limitations. This all-in-head placement differs from the builder’s earlier cable-distribution estimate. Weigh/dress actual cable and validate tipping before release. The mass script’s PASS does not assert every method/scenario clears3%.

## Export verification and visual review

The exported STEP board matrix passes for six installed custom boards with zero cross-board collisions and zero static board/robot intersections. Readback confirms twelve individual W47 branches, no obsolete cassette/PCB14/PCB16/D104/D105 labels and the33.2mm head retaining tie.

Both inspection and presentation STEP exports were rebuilt with `--force` from corrected sources on2026-11-14. Fresh exported-board matrix, validity/readback, image review and final hashes are recorded in the [completion manifest](cad/d107-completion.json). Full validity checks3933 leaf occurrences /3803 prototypes; every corrected D107 part passes topology/closure/positive-volume checks. The full assembly retains three pre-existing topology findings outside D107: two wheel-arch STEP round trips and the vendor yaw-servo case, independently reproduced in [unchanged topology evidence](cad/d107-unchanged-topology.json). These prevent claiming a clean whole-robot topology release; Boolean self-intersection is skipped.

The separate chassis-harness source commit on2026-11-15 advanced `makad-v1.step.py` after those exports. Treat the recorded hashes and full-assembly readback as the D107 review baseline; regenerate the whole-robot STEPs before any later integrated release.

Reviewed close-up support views: [above](cad/snapshots/d107-supports.png), [below](cad/snapshots/d107-supports-under.png). The reinforced roots, deeper board beams and retained populated board are present in the rebuilt inspection STEP.

Review snapshots: [iso](cad/snapshots/d107-iso.png), [opposite](cad/snapshots/d107-opposite.png), [top](cad/snapshots/d107-top.png), [front](cad/snapshots/d107-front.png), [umbilical](cad/snapshots/d107-umbilical.png), [PCB08](cad/snapshots/d107-pcb08-revB.png). The full-scene section renderer previously exceeded its JavaScript stack limit; a focused view plus exact geometric checks supplies the internal evidence.

Live CAD Viewer: [inspection](http://127.0.0.1:3247/?file=final/v1/cad/makad-v1.step), [presentation](http://127.0.0.1:3247/?file=final/v1/cad/makad-v1-presentation.step), [PCB08 rev B](http://127.0.0.1:3247/?file=04-pcbs/pcb-08-yaw-junction/cad/pcb-08-yaw-junction-revB.step).

## Remaining physical gates

Printed process strength and100N proof; keeper/insert/tie retention; actual HDMI housing and camera-board geometry; static FPC contact/pin mapping and excess dress; taped clamp grip; genuine gauge-compatible contacts/crimps and cavity order; actual servo-loop anchoring/dress and wear; complete head removal/twist; camera C0–C4; bus/link and ground-current checks; N2(b) voltage/temperature; K2 LED driver, K3 display inlet; received masses and physical tipping. Nine unchanged BOM rows have their original quoting restored. Nothing was ordered, printed or powered by this work.


**Camera drawing follow-up,2026-11-14:** [Camera harness map](../../05-harness/README.md#camera-signal-path-and-head-fan-out) clarifies the two static CSI ribbons and moving HDMI pairs. The earlier plug-overlap and one-solid claims are insufficient: the independent [camera verification](d107-camera-verification.md) fails 3/5 new geometry/stock-dress checks. The head lead enters the plug from below, the head FFC is five slabs, and the body FFC omits 65.035 mm of selected stock length. The previous clearance rows and completion manifest do not qualify the camera harness. HD-023/026/027/028 remain unpurchased and release stays HOLD.
