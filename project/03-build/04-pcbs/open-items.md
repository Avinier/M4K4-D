# 04 — PCB open items

This page tracks the open work on the custom boards that has no other home. Each row names what closes it. Tick a row and add the date and evidence when it closes; do not delete it. Decisions still go in the [ledger](../decisions.md).

Other board items stay where they were raised:
- PCB-01/03/04 and the TIFPS0629: [power-boards.md §5](power-boards.md#5-open);
- the board register's "work still required" column: [README](README.md#board-register).

## Charge path: PCB-13 inlet and the PCB-02 charger ([D-040](../decisions.md#d-040), [charge-path.md](charge-path.md))

| ID | Item | Kind | Blocks | Closed when |
|---|---|---|---|---|
| CP-OI-01 | **PCB-13 schematic and layout** from charge-path §3. Footprints: GCT USB4140 land pattern (plated slots for the four stakes), TVS2200 DRV (SON-6), STUSB4500 QFN-24. Outline 28 × 15 mm, M2 holes Ø2.2 at Y ±11 on the receptacle line, all parts but J1 on the +X face, ≤ 2.0 mm tall | Design | Fab, NVM, bench | Schematic, BOM and layout committed; outline and holes match `PCB13_BOARD`/`PCB13_SCREW_YZ` in `body_v1_model.py` |
| CP-OI-02 | **PCB-02 charger block schematic** from charge-path §4: `J2-8`, 50 V input capacitors, `VAC`/`ACDRV` straps, `D+`–`D−` tie, `BATP` 100 Ω Kelvin to `J2-1`, `PROG` 8.2 k, `ILIM_HIZ` 10 k/6.8 k, `TS` 8.45 k/324 k + 10 nF, both NTC leads to the BQ25798 ground pad, `SDRV` 1 nF, `CE` 10 k | Design | PCB-02 fab | Captured in the PCB-02 schematic and cross-checked against §4 row by row |
| CP-OI-03 | **ST part ratings from ST's own PDFs:** ESDA25W (standoff, breakdown, capacitance) and STL6P3LLH6 (`RDS(on)` at −4.5/−10 V, `VGS` ±20 V). Only distributor summaries were read | Datasheet | CP-OI-01 | Values confirmed or the parts replaced; charge-path §3 labels updated to `D` |
| CP-OI-04 | **India sourcing:** USB4140-GF-0170-C, TVS2200DRVR, STUSB4500QTR, BQ25798RQMR, STL6P3LLH6, ESDA25W, Würth 74437346022. The Evelta MUP-U23007-01 is SMT-only, with no shell stakes, so it is not a drop-in | Sourcing | Order | Supplier, price and stock recorded in BO-015/CH-041; spares for one rework |
| CP-OI-05 | **STUSB4500 NVM image and programming jig** (charge-path §8): image file with checksum, a pogo jig on the PCB-13 test pads, the read-back log format | Design, tooling | Fitting PCB-13 | Image committed beside charge-path.md; one board programmed and read back byte-identical (CP-01) |
| CP-OI-06 | **`VAC_OVP` default.** The BQ25798 REG10 field says "POR: 11b" (7 V), but the register reset value 85h means 26 V. If 7 V is real, 9/15 V charging cannot start | Bench (CP-04) | First charge | REG10 read on the bench header shows `VAC_OVP` = 00b. If not, stop and raise a decision |
| CP-OI-07 | **Bench tests CP-01 to CP-14** (charge-path §9), in order: PCB-13 alone, then PCB-13 + PCB-02 on a supply with a 10 kΩ NTC stand-in, then the real pack after the TIFPS0629 acceptance | Bench | Charge release | Each row recorded as `W` with its log; failures raised as decisions |
| CP-OI-08 | **Charging in a hot room.** With the 0–50 °C `TS` window, JEITA drops the charge voltage to 8.0 V above about 35 °C on the cell. That is roughly 85–90% full (`E`) | Decision | — | After CP-12 in a warm room: accept, or reopen `PA-09` for a charger host that can move T3 |
| CP-OI-09 | **PCB-02 mounting in CAD.** The board floats in `body_v1_model.py`. The rear lower cross rail (X −36…−28, Z 61–69) is directly behind it | CAD | PCB-02 layout (hole positions) | Standoffs and inserts modelled; PCB-02 clashes and `check_charge_inlet.py` still pass |
| CP-OI-10 | **Adapter and cable (BO-016):** buy one ≥ 30 W BIS-registered PD adapter with a 15 V ≥ 1.5 A PDO and a 3 A C-to-C cable; confirm the PDO list with a PD tester | Purchase | CP-02, CP-12 | PDO list and CRS number recorded in BO-016 |
| CP-OI-11 | **Plug-fit samples:** three overmolds (slim, 12 × 6 class, chunky braided) against a printed panel-pad coupon | Print, bench (CP-14) | Panel release | All three seat fully, none rubs; pocket size kept or changed by decision |
| CP-OI-12 | **Pull and wrench test** on a printed pad with PCB-13 fitted: 20 N axial, 10 N side (`E` loads) | Bench (CP-13) | Panel release | No pad crack, no board movement, `VSNK` stays up |
| CP-OI-13 | **Chassis-model copy of the body** (`01-chassis/v1/cad/body_chassis_model.py`) still has the old PCB-02 receptacle and its `charge_inlet_is_cut_through_rear_panel` row in `check_layout.py` | CAD housekeeping | — | Copy updated to PCB-13, or the row retired with a note that body v1 governs |
| CP-OI-14 | **Full `body-v1.step` rebuild and viewer review** of the inlet, pocket and `W16` route. Not run after D-040; only the targeted checks were | CAD | Panel print release | STEP rebuilt, snapshot saved in `02-body/v1/cad/snapshots/` |
| CP-OI-15 | **PCB-02 area.** RP-02 sized PCB-02 at 2.5–2.8× its placeholder (board-specs §10.4). D-040 moves the receptacle, STUSB4500, input switch and protection off it | Layout | PCB-02 layout | Layout fits the 50 × 36 mm box with the D-040 content, or the box grows by decision |
