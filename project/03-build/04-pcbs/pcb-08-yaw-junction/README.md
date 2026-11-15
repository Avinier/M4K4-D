# PCB-08 — Yaw junction, rev B (D-107)

The stationary body junction for W47: three power pairs pass from J8-1 to J8-9; the C0 head link and servo bus leave on J8-10. The B0091 camera link bypasses this board. Rev A and its FFC fab package are historical and must not be ordered.

| Stage | State / evidence |
|---|---|
| Design | Rev B electrical draft: [design](design/), Nightly ERC 0 errors/0 warnings; exported pin audit 12/12 and W47/PCB-12 audit 5/5; DRC 0 errors, 0 unconnected, 0 parity differences, six explained library-copy warnings |
| Procure | **HOLD — do not order.** D-064 batch, received-cable checks, populated bench gates and fab DFM remain open |
| Integrate | Rev B STEP selected by final/v1/cad/pcb_integration.py. Body/plug/mount checks: `check_d107_body.py`; whole-robot check: `check_pcb_integration.py`. First real board and mount fit remain open |

## Frozen interfaces

KiCad reference designators differ from harness names. Use marked contact numbers, never visual left-to-right guesses.

| KiCad | Harness | Part / pin order |
|---|---|---|
| J1 | J8-1 input | Molex 43045-0621 Micro-Fit 3.0 2×3 RA: 1 +6V3_HEAD_PR, 2 +5V_C2, 3 +5V_DISPLAY, 4 GND_HEAD, 5 GND_C2, 6 GND_DISPLAY |
| J3 | J8-9 W47 power | Same header and **same numbered map as J1**; mouth +X, opposed to J1's −X mouth |
| J2 | J8-4 W24 | JST BM06B-GHS-TBT GH6: 1 LINK_GND, 2 C0TX+, 3 C0TX−, 4 C2TX−, 5 C2TX+, 6 isolated |
| J4 | J8-10 W47 signals | GH6: 1 GND_SIG, 2 C0TX+, 3 C0TX−, 4 C2TX−, 5 C2TX+, 6 SERVO_DATA |
| J5 | J8-8 yaw | Molex 22-03-5035 / 5267-03A: 1 GND_SIG, 2 +11V1_YAW, 3 SERVO_DATA; match received Feetech lead |
| J6 | W17 solder pads | 1 +11V1_YAW, 2 GND_SIG; strain relieve before pads |
| R1 | ground option | 0Ω 0805 from LINK_GND to GND_SIG; ferrite/resistor fallback needs bench evidence |

The three power returns stay separate on PCB-08. GND_SIG includes the yaw return, so the accepted W24/yaw loop and its ground-current/common-mode checks from D-100 remain. PCB-12 joins its local grounds through R1/R7/R10; W47 J8-9.4 and J8-10.6 branch to PCB-12 J2 in the head. Only three conductors cross the roll joint.

## Envelope and routing amendment

The six real connector courtyards do not fit the proposed 32×21 mm core. Rev B is **34×25×1.6 mm**, world X−22…12, Y−46…−21, Z112…113.6. The old FFC extension to X20 is removed. All parts are on the top. Placement is read back from the saved board, and the populated STEP is checked against the Pi's real face bounds and the complete edited body.

Rev B uses **four layers with at least35µm FINISHED copper on every layer**. Dedicated solid +6V3_HEAD_PR and GND_HEAD fills on In1/In2 carry the head rail with solid pad connections, around the1.0mm seed tracks. Other power returns remain separate; there is no shared ground plane. C2/display branches remain0.5mm; yaw supply and return are1.5mm outer tracks; signals0.2mm. The nominal stack is0.035/0.20/0.035/1.06/0.035/0.20/0.035mm. Obtain written fab confirmation of finished inner copper:17.5µm is not an accepted substitution.

[Power copper audit](design/power-copper-audit.json) measures the actual filled copper and solves a0.1mm resistor sheet with equipotential PTH disks. At35µm/60°C it predicts about11.33mV total drop and0.0272W loss for the2.4A head rail, excluding barrels, contacts and solder. Half-thickness inner copper doubles both. This is an electrical screen, not thermal qualification; N2(b) must measure terminal voltage and PCB temperature in the closed body.

PCB-08 seats in a droid-owned edge cradle, with a removable front keeper and one M2×4 screw. It does not gain unreviewed mounting holes. The corrected cradle has a broad9.6×18mm web, deep beams and second upper tie into the frame. The first actual solid-root PETG print must pass100N connector-direction proof without cracking or permanent set; the hand screen is not a strength certification. Remove plugs and keeper before board removal; the CAD assembly check owns the removal path.

The six DRC warnings are `lib_footprint_mismatch` on J2/J4/J5/R1/TP1/TP2: their board copies deliberately put silk/reference graphics on Fab (and use the recorded model copies). The [pad audit](design/footprint-pad-audit.json) confirms all nine footprint land patterns match their libraries. No clearance or connection violation is waived. J6 is bare copper; KiCad's named wire model is absent and is not required to represent a populated component.

## Reproduce

Use the project Python for generators and KiCad **10.99 Nightly** for all electrical outputs. The documented headless kfile workflow is used; no autorouter.

```sh
rtk proxy .venv/bin/python project/03-build/04-pcbs/pcb-08-yaw-junction/design/build_schematic.py
rtk proxy .venv/bin/python project/03-build/04-pcbs/pcb-08-yaw-junction/design/layout_pcb08.py
rtk proxy .venv/bin/python project/03-build/04-pcbs/pcb-08-yaw-junction/design/export_revB.py
rtk proxy .venv/bin/python project/03-build/04-pcbs/pcb-08-yaw-junction/design/audit_netlist.py
rtk proxy .venv/bin/python project/03-build/04-pcbs/pcb-08-yaw-junction/design/audit_w47.py
```

ERC is run separately with `kicad-cli sch erc --severity-all`. The export script refuses electrical errors, then exports the netlist, schematic PDF, STEP, Gerbers, drill, BOM and placements. All fab coordinates use the same bottom-left origin, world(−22,−46). Review [fab/revB](fab/revB/README.md); [fab/revA](fab/revA/README.md) remains the superseded record.

## Before ordering / physical acceptance

- Verify genuine connector contacts for **AWG22 and AWG26** in the Micro-Fit plug; a contact for 20–24AWG must not be assumed suitable for AWG26. Buy compatible pre-crimped GH leads.
- Confirm J5/servo cavity order and conductor ratings against received parts. Trim conductive THT tails to ≤1.5 mm below the board and recheck clearance.
- Confirm first printed cradle, keeper and body strain relief; connector mating and head removal with the received housings, through the Ø18 liner.
- N2(b): terminal voltage under the 2.4A head allowance and low pack; review M2's 6.3V setpoint after removing the ribbon loss. Retain minimum terminal target5.23V.
- Measure W24 ground current at yaw stall, common-mode voltage with simultaneous display/servo load, and bus edges at J8-8.
- Complete fab DFM/stack-up acceptance and the six-board D-064 batch release. PCB-12 still has K2 LED-driver and received Zero/B5 gates. K3 D1 power inlet remains open.
- Camera C0–C4 and first-hour wear checks are in [the D-107 plan](../../head-umbilical-plan.md); they cannot be closed by CAD.
