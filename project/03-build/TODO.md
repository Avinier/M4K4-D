# 03-build TODO

| Field | Value |
|---|---|
| Status | **Open.** Started 2026-11-08 for D-093 procurement |
| Register | [BOM.csv](BOM.csv) is the parts record; this list only tracks actions. Tick a box here, then update the row's `procurement` / `received_measurements` |
| Plan | [simplification-plan.md §7](simplification-plan.md#7-levels-of-work) |

## Order

- [ ] **CH-103 balance-tap fuse card — design selected ([D-115](decisions.md#d-115)), do not order yet.** Three 0466001.NRHF fuses on a 1.8 mm card on the BMS; CH-106 has the relief pocket (re-exported). Next: check the received TIFPS0629 pad positions, lay out the card, then run N5 with it potted. Order 3 fuses + 2 spares once the layout is fixed
- [ ] **BO-068 DIN 9021 M2 washers (Ø6), 8.** Clamp the INMP441 edges under the BO-013 screws. Skip if they came with the screw order
- [ ] **CH-110 non-screw items:** 4 × M2 × 5 F-F round standoffs (S13V30F5 modules) and VHB foam tape. Skip if already in hand

## Order after the 05-harness review (part B)

- [ ] CH-101 XT30U female panel port + XT60→XT30 lead for the PD60
- [ ] CH-102 JST PA 3P balance break (PAP-03V-S / PALR-03VF, pre-crimped SPHD/SPAL AWG24) + JST XH 3P rear balance port (XHP-3, pre-crimped SXH AWG24)
- [ ] HN-006 tub pair: 2 × WAGO 221-415 ([D-113](decisions.md#d-113)); four rear splices still to select
- [ ] CH-099 shunt: Littelfuse WPC2512QLR004FWR 4 mΩ 3 W ([D-112](decisions.md#d-112))
- [ ] Micro-Fit+ 2-way pairs for `J-BAT` and `J-CHASSIS` (206460/215953 series, AWG16); exact gender/key/PN open
- [ ] Micro-Fit 3.0 2-way pairs for `J-S18-H` and `J-S18-Y` (43030/43025 + 43031/43020)
- [ ] Crimp tools (Molex 213309-4400 MF+, 63819-0900 MF3; check PN) or professionally terminated pairs
- [ ] AWG16 UL1061 red/black wire; rated multi-wire AWG16 splices (charge splice, rear ± star, tub branch)
- [ ] Sample each connector first: confirm mate/key, pull-test three per wire/contact combination ([05-harness §9](05-harness/README.md#9-open-and-acceptance))

## On receipt (ordered 2026-11-08)

- [ ] Record seller, price and exact article in `BOM.csv` for CH-021, CH-096–CH-100, CH-104, CH-105, CH-109, CH-110, BO-007, BO-013, BO-016, BO-066, BO-067
- [ ] CH-099 INA226: record the received shunt marking, resistance, power rating, trace layout and I²C address. **Do not install an R010/≥1 W board in the full switched-bus path.** Screen a lower-value shunt/module (5 mΩ ≥2 W is a candidate, not selected), measure current peaks with an independent current probe, then choose the value with range and thermal margin and calibrate against a meter. An R010 board may be used only on an isolated, current-limited bench load below its measured limits
- [ ] CH-100: note whether the ISDT PD60 or a fallback charger arrived; set LiPo 4.20 V/cell, never LiHV
- [ ] BO-016 adapter: BIS CRS number on the label and a 15 V PDO
- [ ] Measure outlines of M6 (CH-099), M8 (BO-007) and M9 (BO-066) and compare with the D-095 UNMEASURED envelopes
- [ ] CH-039 (old 2 × M2 × 5 IMU screw row): check whether CH-110 covers it, then retire or order

## Feetech release order (moved from the retired feetech-migration-status.md, 2026-10-07)

Bench protocol: [03-head/v1/feetech-bench-protocol.md](03-head/v1/feetech-bench-protocol.md). Some steps may already be closed by D-048/D-049/D-095; tick them against `decisions.md`.

- [ ] Verify the provisional yaw packaging against the received ST3215-HS
- [ ] Complete the cradle, BO-056 hub, compute tray and PCB-09 source integration
- [ ] Redesign the head mounts/horns against the received STS3045M horn, coupler and thread fits
- [ ] Solve the head mass/axes and verify all mechanical clearances
- [ ] Regenerate body/chassis stability and §11.3/P07
- [ ] Run B1–B6, then freeze the electrical/firmware thresholds from those results
- [ ] Add the yaw servo to the AR-61 mic noise test (gate 3.10)

## D-107 physical integration (current)

CAD/electrical implementation is recorded in [d107-execution.md](final/v1/d107-execution.md). Before release: receive and measure the slim HDMI plugs, B0091 adapters, GH/Micro-Fit housings and gauge-compatible contacts; verify all cavity and servo pin orders; identify D1 power inlet (K3) and PCB11 LED driver (K2); run C0–C4 camera gates, head-link/servo-bus/rail checks, strain-relief pull checks and first-hour wear inspection. The moved servo-wire anchor has at least1.54mm nominal screw clearance in the CAD sweep; verify actual wire dress before motion. Weigh printed parts and the cable; confirm tipping. No board, cable or print has been ordered by this work.

Whole STEP topology follow-up: both unchanged wheel-arch pods are valid in source but fail STEP round trip; the purchased ST3215-HS case has an already-documented invalid solid. D107 geometry passes. Evidence: [full validity](final/v1/cad/d107-assembly-validity.json), [independent reproduction](final/v1/cad/d107-unchanged-topology.json). Resolve before treating the whole robot as a clean fabrication solid set.


D1072026-11-14 corrections are implemented; fabrication stays HOLD: buy/measure HDMI before closed inserts, verify two150mm static FPCs/contact dress, tape clamp to6.8±0.05mm, confirm >=35µm finished inner copper with fab, qualify solid PETG support roots and100N first-print proof. Weigh actual cable/robot and validate tipping: original-register all10g-in-head sensitivity gives2.38%, below3% buffer, though moving-frame sensitivity gives3.47%. Retain camera C0–C4, N2(b) temperature/voltage, first-motion/wear and existing contact/driver/inlet gates. [Record](final/v1/d107-corrections.md).

Camera chain review: [verification](final/v1/d107-camera-verification.md) fails3/5 additional checks. Correct the head HDMI plug approach, replace the head's five ribbon slabs with a credible continuous cable, and dress the body ribbon's65.035mm surplus before camera release. The jacket-stripped HDMI section has no manufacturer qualification; bench-test the received cable through motion before printing or ordering closed inserts.

## D-109 body harness (current)

CAD Levels 0–6 done ([review](05-harness/body-design-review.md)). Remaining:

- [x] Service sweeps (10/13): tray, panel, body lift and PCB-08 pass
- [x] Shell lift: W27 shell-dressed (16/16, service 13/13)
- [ ] Shell mock-up: adhesive cable clips on PETG and W27 dress, before printing the shell
- [x] Body wires vs head harness, HDMI and camera FPC (31/31)
- [x] Tie lugs: none qualify; frame runs tie to each other/module cradles, shell runs use adhesive clips
- [x] J10-1 lead exit: the J101 box is its own lead reserve
- [ ] 2-way header at the button buffer for the W40 mushroom lead
- [ ] Adhesive cable clips for the shell-dressed W27 (about 12)
- [ ] Order samples: Molex C-Grid III 2×3 latching headers/housings ×4 + spares, Micro-Fit 3.0 1×6 inline pair with AWG26–28 contacts, 2-way speaker inline pair
- [ ] Weigh the built harness; re-run `MAKAD_D109_MASS=1 check_d107_mass.py`; keep copper ballast until steel shows ≥ 3 %
- [x] Rebuild `makad-v1.step` (inspection)
- [x] Rebuild the presentation STEP

