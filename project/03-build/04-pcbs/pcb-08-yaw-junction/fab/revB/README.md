# PCB-08 rev B — draft fabrication package

**HOLD: do not order.** D-107 electrical outputs; received-part, populated bench, DFM/stack-up and D-064 batch release gates remain in the [board record](../../README.md#before-ordering--physical-acceptance).

- Board34×25mm, 1.6mm, **four layers**, **>=35µm finished copper on every layer, including inner layers** (written fab confirmation;17.5µm is not an approved substitution). F.Cu components; In1 isolated solid +6V3_HEAD_PR fill, In2 isolated solid GND_HEAD fill, solid pad connections; yaw supply/return1.5mm outer tracks; B.Cu signal routes. No ground planes bond the three returns.
- ENIG preferred; top SMD J2/J4/R1; THT J1/J3/J5; W17 on J6 by hand. Genuine Micro-Fit contacts must match both AWG22 and AWG26.
- Gerbers include F/In1/In2/B copper, both mask/paste/silk and Edge.Cuts. Drill is Excellon mm. The zip includes the Gerber job and drills. All use world(−22,−46) as plot/drill/placement origin.
- `*-bom.csv` and `*-pos.csv` omit J6/TP1/TP2 (bare copper). `*-cpl-jlcpcb.csv` uses the same placement frame. Confirm the opposed Micro-Fit mouths in the fab preview.
- `../../cad/pcb-08-yaw-junction-revB.step` has both Micro-Fits, both GH headers, SPOX and R1. J6's absent library wire model is intentionally not a populated part.
- ERC0/0; pin audit12/12; W47/PCB-12 audit5/5; parity DRC0 errors/0 unconnected/0 parity. Six deliberate library-copy warnings are explained in the board record.

Reproduce with `design/export_revB.py` after the saved board passes checks. Rev A is historical and must not be mixed with this package. Source hashes and final integration evidence accompany the execution record.

The [power copper audit](../../design/power-copper-audit.json) is a resistance/loss screen, not a temperature qualification. N2(b) must measure closed-body PCB temperature under actual current/duty before release.
