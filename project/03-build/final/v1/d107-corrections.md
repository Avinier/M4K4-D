# D107 functional corrections — 2026-11-14

Brief: address the builder review without changing subsystem CAD, interfaces, or measured motion envelope. Keep the established electrical pin maps and steel ballast. Rebuild final inspection/presentation and PCB08 outputs once corrected sources pass checks. Do not print or order.

Plan before edits:
- Replace the 2×2 PCB08 hanger and 4×4 strain-relief hanger with a broad shared vertical web, stiff fore/rear cradle beams, and a second upper tie to the existing rear crossrail. Preserve plug withdrawal, PCB service, Pi/CSI access and the full yaw-stop sweep.
- Screen nominal50N connector insertion and40N cable pull, with a100N proof case, from measured CAD minimum sections and attachment intersections. PETG strength/elastic modulus are explicit E assumptions; the screen is not FEA or print qualification. Actual first-print proof loads remain required.
- Add an annular liner flange seated on the rotor’s upper face, inside the hub’s clear bore, to prevent dropping onto the Pi. Verify bearing land, allowable axial travel and removal order.
- Specify a150mm15-way head camera FFC and a separately sized22-to15 Pi-side FPC. Measure routed, straight and insertion/slack budgets; do not rely on the kit’s60mm15-way ribbons.
- Widen the head-rail and yaw-return copper. Maintain separate nets and no shared ground plane; audit finished copper widths/layers and35µm inner copper requirement, also screen17.5µm as an explicit adverse scenario. Re-run DRC, net audits and exports.
- Move the roll-wire anchor and enforce at least1mm nominal clearance from the screw over0.5° roll increments, while checking all other obstacles and minimum bend radius. Retain physical cable-dress qualification.
- Keep HDMI passage unqualified until the actual cable is measured. Size the head clamp using tape and record actual diameter. Update current plan dimensions and restore original CSV quoting on unchanged rows.

Sources and final measurements follow below.

## Corrected design and proof conditions

The PCB08 cradle has a9.6×18mm broad hanger and a second upper tie into the rear crossrail, with deeper front/rear beams. Its actual root intersection with the unedited frame is107.64mm²; the measured weaker-axis section modulus is158.86mm³. The rear beam is2.35×10mm and the side stops3.85mm thick. The body saddle has a6.4×9.4mm guaranteed gusset throat below the conservative rotating envelope. The final FPC passes below the front beam in a clearance slot; the rear portion runs atY−39. All changes remain in final-assembly helper/table geometry.

[Functional screen](cad/check_d107_functional-report.json):50N connector force gives7.55MPa at the hanger,9.53MPa at the rear beam;40N cable pull gives4.97MPa at the hanger and5.52MPa at the saddle gusset. Edge-stop bearing/bending stay below7.79MPa. This uses **E20MPa printed-PETG material credit with factor2 at service load**, with solid roots/beams. It is a simplified beam/section calculation, not FEA, measured print strength, fatigue or connector/FR4 qualification. Layer adhesion, print orientation, notches and creep are not established by CAD. The actual process must demonstrate that credit; do not substitute ordinary sparse infill at the structural roots.

Before production use, fixture the actual frame at its normal mounts. With the keeper fitted and a sacrificial board/housing fixture that does not load solder joints, apply100N slowly in each relevant connector insertion/removal direction at the board connector midplane (no impact); hold10s. Separately pull the tied dummy bundle100N in the adverse saddle direction (13mm lever), hold10s. Inspect roots, beams, keeper and screw under load and after unloading: no cracking, layer opening, loss of retention or permanent set. The100N hand stress case reaches19.06MPa at the rear beam against the assumed20MPa credit; the proof is mandatory. Support real housings during first mating. The head camera cradle’s existing two2×8mm supports are unchanged.

The rotor liner retains0.2mm radial running clearance, with an OD24.8 flange at worldZ137…138 resting on the rotor top. CAD gives102.92mm² bearing land and51.46mm³ obstruction to a0.5mm downward translation. This establishes positive downward capture, not snap retention; removal is upward after the disc bushing. First print must verify the seating surfaces and the Ø18 passage.

The servo roll-frame anchor moves from(−25.8,−9.5,46) to(−28,−12,46). At0.5° roll steps over±21°, the loop clears the PCB12 screw by at least1.5418mm (worst16.5°), versus0.1794mm before. The full head checks also cover frame, PCB, branch and bend clearance. Actual ties and flexible-wire dressing still need a slow first sweep and wear inspection.

## Bought ribbons and receipt gates

- **HD-026:**150mm15-way1.0mm-pitch standard head camera ribbon. The111.198mm routed path plus10mm total socket insertion and15mm service allowance needs136.198mm; reserve13.802mm. The63.361mm straight span already exceeds the kit’s60mm ribbon.
- **HD-027:**150mm15-way1.0mm to22-way0.5mm Pi5 camera FPC (Arducam B0210-class). Routed59.965mm plus the same25mm allowances leaves65.035mm. Dress excess as a static fold clear of nearby parts; the geometry shows the routed free-span envelope, not every millimetre of stock.
- The [official B0091 kit page](https://www.arducam.com/arducam-csi-hdmi-cable-extension-module-15pin-60mm-fpc-cable-raspberry-pi-camera-specific-pack-2-1-set.html) lists60mm15pin and73mm22pin ribbons; they are spares here. [Arducam’s cable table](https://docs.arducam.com/Camera-Extension-Solution/MIPI-Camera-Cable/) lists the150mm15-to22 B0210 class. No price/stock or received pin/contact orientation is claimed. Verify continuity, contact faces, stiffeners and latch dress before C0–C4 camera acceptance.
- HDMI passage remains **unqualified**. The16×7mm assumed plug diagonal17.464mm has only0.268mm radial reserve insideØ18. Buy the cable first and measure full housing, latch and boot. If it fails, unplug at the head, or separately design/verify split inserts for the bareØ21 bore; split geometry is not released here.
- Hard clamp bore7.2mm with two0.25mm silicone pads gives6.7mm softID. Repack/tape to6.8±0.05mm at the grip. If the bare bundle exceeds6.85mm, revise pads/clamp instead of crushing the camera pairs. Verify actual grip without transferring pull to sockets.

## Copper and fabrication

PCB08 now has a solid isolated +6V3_HEAD_PR fill on In1 and GND_HEAD fill on In2, solid pad connections, and1.5mm outer yaw supply/return tracks. Other returns remain separate. DRC has0 errors,0 unconnected and0 parity differences, with the same six library warnings. The [filled-copper audit](../../04-pcbs/pcb-08-yaw-junction/design/power-copper-audit.json) checks actual filled polygons, net separation, copper thickness and widths. Filled areas are664.78/670.85mm².

At35µm copper and60°C, the0.1mm resistor-sheet screen predicts positive/return resistance2.013/2.708mΩ:11.33mV total drop and0.0272W copper loss at2.4A. It excludes barrels, solder and contacts and predicts no temperature. A17.5µm adverse calculation doubles resistance/loss; it is **not an accepted fab substitution**. Require written>=35µm finished inner copper and verify closed-body PCB temperature and terminal voltage under N2(b).

## Mass and records

The larger supports, liner flange, Pi ribbon and added copper are included in the new ledger. Steel remains selected. Nominal moving-frame margin4.5922%; original D095 register calculation3.4707%. Adding all10g at the head adapter gives moving-frame3.4683% but original-register2.3844%. The latter freezes the source-head radii and treats delta centroids as stationary; it is reproduced transparently, not renamed as a new conservative calculation. It clears the1.5% operating minimum but **does not clear the3% restoration buffer** in this adverse placement. Received mass/dress and physical tipping remain HOLD. The builder’s earlier3.2% sensitivity used a different cable-mass placement; do not quote it as this all-in-head case.

Plan§3 now states clampZ6, opening34×30.2 and finishedØ18 passage versus bareØ21. Nine unchanged BOM rows have their original quoting restored exactly: CH-044, BO-022, BO-023, BO-058, BO-063, HN-011, CH-087, CH-088, CH-095. No procurement, printing or powered tests were performed.

## Camera harness drawing correction —2026-11-14

The camera signal goes through a short static15-way ribbon to the B0091 board in the head, an HDMI cable (stripped to inner pairs through the moving neck), the second B0091 board in the body, and a separate static15-to22 FPC into the Pi5. None of the flat CSI ribbon crosses the yaw/neck joint. W47’s twelve electrical wires fan out after the head clamp to PCB12, servo and display; the camera pairs continue separately to the head B0091’s HDMI plug.

The `W47_LEAD_HEAD_CAMERA_HDMI` drawing used to end about3.1mm beyond its modeled plug. Its terminal now enters the plug envelope at head-local(−67,15.5,75), with24.835mm³ nominal interface overlap. The neck checker explicitly verifies this intentional connection while still testing the lead against other head parts. The B0091 board/plug solids remain E placement envelopes.

The body Pi FPC’s six disjoint rectangular plates are replaced with one valid, continuous0.3mm-thick mitered ribbon envelope, tapered between the15-way and22-way ends. The body checker tests the actual solid against the imported Pi solid, avoiding false hits from the single ribbon’s overall bounding box. This establishes routed space and CAD continuity; the received cable’s exact fold, stiffener/contact orientation and spare-length dressing remain physical checks.

The buying register now lists **HD-023 one B0091 adapter-pair kit**, **HD-028 one slim HDMI cable**, and **HD-026/HD-027 two installed150mm ribbons** separately. The kit’s short included ribbons are spares. No part was purchased.
