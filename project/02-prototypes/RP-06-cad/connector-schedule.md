# RP-06 Connector and Cable-Exit Schedule

| Field | Value |
|---|---|
| Status | **Working schedule, 2026-09-26.** Families and terminations chosen by the builder (below); nothing bought, crimped or bench-proved. Not registered in RP-02 |
| Scope | Every installed body-side connection in body/chassis Layout 02 and the yaw service break. Head-internal connectors stay with head Layout 04 (`head/layout-04/harness.py`) |
| CAD | `body-chassis/layout-02`: group `CONNECTORS_AND_EXITS` (reserves, plus real bodies: `PCB-08` and `PCB-09` boards with their headers, `PCB-05` edge headers, mated Micro-Fit plugs, motor pairs), the C3 carrier `PCB-10` in the electronics group, the re-routed head trunk in `HARNESS_ROUTES`, GH headers on `PCB-06`/`PCB-07`, the rear-panel charge-inlet cut-out and tub window. Cables are not modelled wire by wire; checks listed at the end |
| Sources | RP-02 `board-specs.md` v0.18, `power-implementation-basis.md` §4, `power-component-candidate-screen.md` (`PCD-CON-*`); RP-06 `peripheral-selection.md`; vendor data cited per row |

Grades: `D` vendor data read, `E` estimate, `U` unknown.

## 1. Decisions (builder, 2026-09-26)

| ID | Decision | Consequence |
|---|---|---|
| `CN-01` | **Installed signal connectors are JST GH (1.25 mm, positive latch).** | `PCB-06` mic boards and the `PCB-07` IMU change from JST-SH 4/8 to GH 4/8. GH is 1.0 A per contact at AWG26 (`D`), AWG26–30 only. JST-SH stays bench-only, like Dupont (`PCD-CON-06`). |
| `CN-02` | **The Pololu #4804 0.1" female header is cut off.** The motor pair is re-crimped to a Micro-Fit 3.0 1×2 wire-to-wire pair; the four encoder leads to a GH 4-pin plug. | Motor return never shares a housing with encoder signals. The stock header is friction-only and banned from the installed harness (`power-implementation-basis.md` §4). |
| `CN-03` | **The Pi 5 takes `PB-COMPUTE` through a right-angle USB-C plug pigtail** from `PCB-04`. | There is no PD source, so the Pi needs `usb_max_current_enable=1` in `config.txt` for the full USB budget. The pigtail presents a 56 kΩ Rp on CC (default USB power) so the sink sees attach (`E`; bench it). |
| `CN-05` | **The pack disconnect is a Molex Micro-Fit+ 1×2 wire-to-wire pair, not the Anderson SBS Mini** (builder, 2026-09-26; supersedes `PCD-CON-01` for this pack). It lies in the channel beside the tub (X 27–49), with the ATOF fuse holder moved forward next to it (X 51–75). A 22.6 × 10 mm window in the tub's +Y wall lets the pair slide into the empty tub for unplugging once the hatch is open and the pack is lowered. | Mate and unmate only in `OFF` (43–100 µA, `BA-02`): it is not hot-plug rated. Contact rating ≥ 12 A at AWG16 at 2 circuits to confirm from the Molex terminal specification. Polarized, latched and finger-safe (`power-implementation-basis.md` §4). |
| `CN-06` | **The C3 carrier (`PCB-10`, RP-02 `CCD-HDL-03`) stands vertical on the −Y side wall** (X −14…56, Z 82…125.5), with the DevKitC soldered to it through its own pin headers. Four M2.5 screws go into heat-set inserts in two printed uprights between the −Y rails. | Found by a free-volume scan: the only other space big enough was the air over the Pi cooler. The DevKitC's previous spot put its header pins 8.5 mm into `PCB-04`. The C3 module (carrier + DevKitC) is one replaceable part; the DevKitC USB ports stay reachable from the rear with the panel off. |
| `CN-04` | **Layout rule:** power connectors are right-angle Micro-Fit parts on free board edges; signal connectors are top-entry headers inside the board outline, plugging up into the layer under the compute tray. | Side-entry parts alone need about 80 mm of edge on `PCB-03`, which has 36 mm free. With the rule, every edge fits (§4). |

The earlier family leads stand, except the pack connector (`PCD-CON-01`, replaced by `CN-05`): Micro-Fit+ for high-current internal power (`PCD-CON-03`), Micro-Fit 3.0 for low-current power (`PCD-CON-02`), USB-C for the charge inlet (`PCD-CON-05`). XT30 and Dupont stay rejected (`PCD-CON-06/07`).

## 2. Families

| Family | Part series | Use | Rating used | Geometry basis |
|---|---|---|---|---|
| SBS Mini | Anderson `B02265G1` red + `261G3-LPBK` contacts | **Not used** (`CN-05`): it fits nowhere near the tub | 31 A at AWG14 (UL, `D`) | About 22 × 13 × 14 mm mated, `U` (drawing behind an Anderson login) |
| Micro-Fit+ | Molex, 3.0 mm, dual row, right-angle; wire-to-wire for the pack | Pack disconnect (`CN-05`), `BATBUS`, `OPBUS`/`CHGBUS`, `PB-DRIVE`, `PB-HEAD` trunk, `PB-COMPUTE` | up to 13.5 A per contact, exact terminal open (`D` family) | Width 3.0 × columns + 5.3 mm (`E`, drawing not fetched) |
| Micro-Fit 3.0 | Molex 43045 (right-angle header), 43025 receptacle; 43640/43645 for wire-to-wire | `PB-SAFE-C2`, `PB-DISPLAY`, `PB-SAFE-BASE`, `PB-AUDIO-OUT`, motor pair | 10 mΩ contact (`D`) | Width 3.0 × columns + 4.26 mm, header depth 10.0 mm (`D`, Molex drawing via the KiCad fab outline) |
| JST GH | SMxxB-GHS-TB (side), BMxxB-GHS-TBT (top), GHR-xxV-S | All signals | 1.0 A per contact at AWG26 (`D`) | Header width 1.25 n + 3.25, 4.25 mm tall (`D`, JST catalogue); side-entry STEPs from step.parts |
| JST EH | B3B-EH-A / EHR-03 | XC330 yaw servo only (vendor-fixed) | Per ROBOTIS | ROBOTIS e-manual (`D`); width `E` |
| JST PH | S3B-PH on the sensor / PHR-3 | GP2Y0A41SK0F only (vendor-fixed) | — | Existing reserve |
| USB-C | Vertical-mount 16-pin receptacle on `PCB-02` (part open); right-angle plug for the Pi | Charge inlet; Pi power | 3 A default, PD negotiated by `STUSB4500` | Envelope `E`; GCT USB4105 rejected: its mouth lies in the vertical board's plane and cannot face the panel |
| FFC | Raspberry Pi PCN-36 15-to-22 (11.5 mm wide) | CSI | — | `BA-05` |

## 3. Schedule

Connector IDs are `J<board>-<n>` on boards (`J2` = `PCB-02`, `J3` = `PCB-03`, `J4` = `PCB-04`, `J5` = `PCB-05`, `J8` = `PCB-08` yaw junction, `J9` = `PCB-09` C0 link adapter, `J10` = `PCB-10` C3 carrier); `J-PK` is the pack disconnect. `W` numbers are cables.

### 3.1 Pack and power distribution

| Cable | Function | From → to | Connectors | Conductors | Route / exit | CAD |
|---|---|---|---|---|---|---|
| `W01` | Pack lead | `PCB-01` → pack disconnect `J-PK` | Soldered on `PCB-01`; Micro-Fit+ 1×2 wire-to-wire, pack half | 2 × AWG16 silicone, about 120 mm with service slack | Through the +Y tub window into the channel | `PACK_DISCONNECT_MICROFIT_PLUS_1X2_MATED_ENVELOPE`, service slide path |
| `W02` | Pack NTC | `PCB-01` 103AT-2 → `PCB-02` | GH 2 plug → `J2-7` (top-entry); an inline break at the pack is open (§5) | 2 × AWG28 | With `W01`/`W03` | Top-layer reserve |
| `W03` | Fused pack feed | `J-PK` body half → ATOF holder → `PCB-02` | Micro-Fit+ 1×2 body half; ATO FLR PCB holder; Micro-Fit+ 1×2 → `J2-1` | 2 × AWG16 | Channel (pair X 27–49, fuse X 51–75), then `HARNESS_BATTERY_TRUNK` | Pair and fuse holder modelled; `J2-1` edge reserve |
| `W04` | `BATBUS` | `PCB-02` `J2-2` → `PCB-03` `J3-1` | Micro-Fit+ 1×2 both ends | 2 × AWG16 | Under-board slot, Z 56–63 | Edge reserves |
| `W05` | `OPBUS` + `CHGBUS` | `PCB-02` `J2-3` → `PCB-04` `J4-3` | Micro-Fit+ 2×2 both ends | 4 × AWG18 | Under-board slot to `PCB-04` +Y | Edge reserves |
| `W06`/`W07` | `PB-DRIVE-L/R` | `PCB-03` `J3-2`/`J3-3` → DRV8874 carrier `VIN`/`GND` | Micro-Fit+ 1×2; soldered at the carrier with 100 µF + 0.1 µF | 2 × AWG18 each | Edge to the adjacent carrier | Edge reserves |
| `W08`/`W09` | Motor L/R | Carrier `OUT1/OUT2` → #4804 red/black | Soldered at the carrier; Micro-Fit 3.0 1×2 wire-to-wire (43645/43640) at the motor lead | Motor's own leads | Pigtail reserve over the cap, then outboard of the carrier | `MOTOR_x_INLINE_MICROFIT3_1X2_RESERVE` |
| `W10` | `PB-COMPUTE` | `PCB-04` `J4-1` → Pi 5 USB-C | Micro-Fit+ 1×2; right-angle USB-C plug | 2 × AWG18 (5 A, ≤ 100 mV) | Pi −Y edge at X −10, down past the tray to `PCB-04` −Y | Plug and drop reserves |
| `W11` | `PB-SAFE-BASE` | `PCB-04` `J4-4` → C3 carrier `J10-1` | Micro-Fit 3.0 2×1 both ends | 2 × AWG22 | `PCB-04` −Y, up the −Y side to the carrier's front edge | Both edge reserves |
| `W12` | `PB-AUDIO-OUT` | `PCB-04` `J4-5` → `PCB-05` `J5-7` | Micro-Fit 3.0 2×1 both ends | 2 × AWG22 | `PCB-04` +Y, then forward | Edge reserve |
| `W13` | `PB-HEAD` pitch/roll + yaw branch | `PCB-03` `J3-4` → yaw junction `J8-1` | Micro-Fit+ 1×2 | 2 × AWG20 | −Y riser | Edge reserve, riser |
| `W14` | `PB-SAFE-C2` + `PB-DISPLAY` | `PCB-04` `J4-2` → yaw junction `J8-1` | Micro-Fit 3.0 2×2 | 2 × AWG24 + 2 × AWG24 | −Y riser | Edge reserve, riser |
| `W15` | Yaw servo | `PCB-03` `J3-5` → XC330-M181 | JST EH 3 (B3B-EH-A top entry), ROBOTIS 3-pin cable | VDD, GND, bus `DATA` (AWG21 per ROBOTIS) | Up to the servo at X −8…26, Y 27…47 | Top-layer reserve |
| `W16` | Charge inlet | External adapter → `PCB-02` | USB-C receptacle on `PCB-02`'s back face, through a 13.2 × 7.2 mm rear-panel cut-out | — | Rear panel, Y 0, Z 64 | Receptacle, cut-out, outside plug corridor |

### 3.2 Safety and control signals (all JST GH unless stated)

| Cable | Function | From → to | Connectors | Conductors | CAD |
|---|---|---|---|---|---|
| `W20` | Branch enables and power-good, sequencing latch | `PCB-02` `J2-4` ↔ `PCB-04` `J4-6` | GH 10 both ends | `EN_*`, `PG_*`, latch, 2 × GND | Top layers |
| `W21` | Permit logic | `PCB-02` `J2-5` ↔ `PCB-03` `J3-6` | GH 6 | `CHARGE_ABSENT`, `ENERGY_OK`, `SYSTEM_ARM`, `MOTOR_PRESENT`, 2 × GND | Top layers |
| `W22` | E-stop | IDEC XA1E tabs → `PCB-03` `J3-7` | Soldered at the switch; GH 4 | NC1 loop pair, NC2 status pair | Top layer; switch keep-out existing |
| `W23` | Head sideband | Yaw junction `J8-3` → `PCB-03` `J3-8`; `J8-5` → `PCB-02` `J2-6` | Two GH 8 cables (the PCB-03 set and the PCB-02 set) | `C2_READY_H/L`, `E_STOP_STATUS`, `MOTOR_PRESENT`, `HEAD_OC`, `HEAD_PGOOD`, servo `DATA` + ref; `STAT`, `INT_PB`, `KILL`, `V_PACK_ANA`, `CHG_ABSENT_3V3`, signal GND | Riser, top layers |
| `W24` | Head link (C0 ↔ C2 RS-422) | `J9-1` ↔ `J8-4` | GH 6 | TX±, RX± twisted pairs, reference, spare | Headers and plugs modelled on both boards |
| `W25` | Base link (C0 ↔ C3 RS-422) | `J9-2` ↔ `J10-2` | GH 6 | TX±, RX±, reference, spare | Both ends reserved |
| `W26` | Audio host | `J9-3` ↔ `PCB-05` `J5-1` | GH 10 (top entry on `PCB-09`, side entry on `PCB-05`'s rear edge) | BCLK, LRCLK, SDI0, SDI1, SDO0, `AMP_SD`, 3V3, 2 × GND, spare | Headers and plugs modelled |
| `W27` | Microphones (× 4) | `PCB-06` ↔ `PCB-05` `J5-2…5` | GH 4 (side entry on `PCB-05`'s ±Y edges) | 3V3, GND, CLK, DATA | Headers and plugs modelled at both ends |
| `W28` | Speaker | K 50 WP tabs → `PCB-05` `J5-6` | Soldered; GH 2 | 2 × AWG26 (0.7 A crest, `E`) | Header and plug modelled |
| `W29` | IMU (SPI) | `PCB-07` ↔ `J10-7` | GH 8 | 3V3, GND, SCLK, MOSI, MISO, CS, INT1, INT2 | GH header modelled; plug reserve |
| `W30`/`W31` | Encoders L/R | #4804 green/blue/yellow/white → `J10-3`/`J10-4` | GH 4 plug re-crimped on the motor lead | GND, Vcc (3.5–20 V, `D`), A, B | Carrier plug layer |
| `W32`/`W33` | DRV8874 logic L/R | DRV carrier pins → `J10-5`/`J10-6` | Soldered at the DRV carrier; GH 6 | `SLEEP`, `EN/IN1`, `PH/IN2`, `CS`, `FAULT`, GND | Carrier plug layer |
| `W34` | Nose pod (front range + touch cap) | GP2Y0A41SK0F and the tact switch → `J10-8` | JST PH 3 (vendor) at the sensor, switch soldered; one GH 5 at the carrier | Vcc, GND, Vo, switch pair | `GP2Y_JST_PH3_PLUG_RESERVE`; carrier header modelled. `W35` merged into this cable 2026-09-26 to free a carrier slot |
| `W36` | Rear TCRT | Keel cartridge → `J10-10` | GH 4 (breakout unselected) | 5 V, GND, analog, digital | `TCRT_REAR_GH4_PLUG_RESERVE` |
| `W38` | E-stop status to C3 | `PCB-03` → `J10-11` | GH 3 | status, 3V3 pull-up reference, GND | Carrier plug layer |
| `W39` | Base readiness | `J10-12` ↔ `PCB-03` `J3-9` | GH 4 | `C3_READY`, `MOTOR_PRESENT`, 2 × GND | Top layers |
| `W37` | CSI | Pi 5 rear FPC socket (X 26–29) ↔ Camera Module 3 | 22-pin FPC at the Pi; PCN-36 FFC | 11.5 mm FFC | `HARNESS_CSI_*`: down the Ø18 plate bore, then beside the cooler |

Vendor-fixed and service-only connections are not installed harness: the Pi cooler fan (on-board JST SH), the DevKitC USB ports (service, behind the rear panel), and the C2 USB-C (head service path).

### 3.3 C3 carrier (`PCB-10`)

The board is 70 × 43.5 mm and stands vertical at Y −58.4…−56.8, 1.6 mm inboard of the −Y rails.

- **Parts.** The DevKitC-1-N8 is soldered on the +Y face through its two 22-pin headers, with a 2.5 mm plastic gap. Under it are the base-link THVD1451, the TPS3436 watchdog and the `READY` AND gate. The `BASE_READY` N-FET stages gate the two DRV8874 `SLEEP` lines, and test points sit on every rail and link pair (RP-02 `CCD-HDL-03`, `board-specs.md` §7).
- **Mounting.** Four M2.5 screws go into heat-set inserts in two 8 × 7.6 mm printed uprights between the lower and upper −Y rails, at X −12…−4 and 20…28.
- **Connectors.** Signal headers are top-entry GH in the 14.2 mm band below the DevKitC. Ten real JST BM headers sit in two rows (`C3_GH_ROWS`) that keep clear of the four M2.5 screws: `J10-2…8` and `J10-10…12`; `J10-9` was dropped when the touch switch joined `J10-8`. `J10-1` (`PB-SAFE-BASE`) is a right-angle Micro-Fit 3.0 on the front edge, exiting +X.
- **Service.** The DevKitC's USB-C ports face −X, with a service corridor to X −40 (rear panel off).

### 3.4 Yaw service break

The clock-spring's stationary end lands on a small junction board (`PCB-08`, 32 × 21 mm plate at X −22…10, Y −44…−23, Z 112, reserve to Z 125.5) under the adapter plate on −Y, clear of the cooler-headroom prism. To remove the head, unplug the body-side cables at `PCB-08` and the CSI FFC at the Pi, then lift the head, clock-spring and junction board together through the Ø90 shell opening. `PCB-08` connectors: `J8-1` Micro-Fit+ 2×3 (the three power pairs: separate contacts and returns in one shell, `power-implementation-basis.md` §4), `J8-3` and `J8-5` GH 8 sideband, and `J8-4` GH 6 head link, all top-entry. The Micro-Fit+ exits −X, then runs down the riser. The head-side conductor gauges stay as `board-specs.md` §9.2 sets them.

## 4. Edge fit (CAD check `edge_power_connectors_fit_free_board_edges`)

| Edge | Free length | Connectors | Needed | Margin |
|---|---:|---|---:|---:|
| `PCB-03` +Y (X 19–37) | 18.0 | `J3-2`, `J3-1` Micro-Fit+ 1×2 | 17.6 | **0.4** |
| `PCB-03` −Y (X 19–37) | 18.0 | `J3-3`, `J3-4` Micro-Fit+ 1×2 | 17.6 | **0.4** |
| `PCB-04` −Y (X −14–15) | 29.0 | `J4-1` Micro-Fit+ 1×2, `J4-2` Micro-Fit 3.0 2×2, `J4-4` Micro-Fit 3.0 2×1 | 27.8 | 1.2 |
| `PCB-04` +Y (X −14–15) | 29.0 | `J4-3` Micro-Fit+ 2×2, `J4-5` Micro-Fit 3.0 2×1 | 19.6 | 9.4 |
| `PCB-02` −Y (Z 60–94) | 34.0 | `J2-1`, `J2-2` Micro-Fit+ 1×2, `J2-3` Micro-Fit+ 2×2 | 29.9 | 4.1 |

The free lengths are what the DRV8874 carriers, the body mount doglegs and the DevKitC leave. The `PCB-03` margins rest on the estimated Micro-Fit+ width. If the Molex drawing shows it wider than 8.5 mm per 1×2, one `PCB-03` power connector must move to the top layer as a vertical Micro-Fit+ header, or the DRV feeds become soldered pigtails.

## 5. Open items

1. **Pack disconnect (resolved as `CN-05`; still to prove).** Confirm the Micro-Fit+ wire-to-wire outline (22 × 8.3 × 10 mm mated is `E`) and the terminal rating at 2 circuits and AWG16, then bench the service move: hatch open, pack lowered on its lead, pair slid through the tub window and unplugged. The window removes 22.6 mm of the +Y tub wall's side support, so check the pack retention foam. The pack NTC (`W02`) needs its own break at the pack, such as a GH 2 inline pair beside `J-PK`; it isn't modelled yet.
2. **C3 carrier (resolved as `CN-06`; still to prove).** The lugs are printed features on the rails and aren't load-checked. The board outline is a proposal pending the RP-03 pin map freeze. `W11` and `W25`–`W39` now run the length of the −Y side, so measure the lengths once the harness is drawn.
3. **The Pi header connection is measured but very tight.** The yaw servo overhangs the GPIO header's outer edge from Z 104. The CAD models three parts:
   - A standard 8.5 mm 2 × 20 socket, with its top at Z 106.4, clears the servo by 0.6 mm.
   - The C0 link adapter (`PCB-09`: two THVD1451, `J9-1…3`) is a 4.6 mm strip over the socket (Y ≤ 26.9), 0.1 mm clear of the servo. A bridge past X 26 joins it to the board's wide part beside the servo.
   - All three reserves are checked.

   0.1 mm is below any print or assembly tolerance. Fit the real board, socket and servo on the bench before committing. If they don't fit, a flat flex from a socket, or moving the servo about 1.5 mm +Y (it sits on the pinion mesh), are the fallbacks.
4. **Micro-Fit+ and Micro-Fit 3.0 heights and plug protrusion are estimates.** Only widths are checked. The `PCB-03` edge reserve is 10.4 mm tall.
5. **Vertical USB-C inlet part not chosen.** The CAD uses an 8.94 × 3.26 mm envelope with the mouth 1.05 mm behind the panel's inner face. Choose a part and check the plug's overmold against the 13.2 × 7.2 mm cut-out.
6. **Pin-outs and partial-mating order** (`power-implementation-basis.md` §4: no power through a signal pin on partial mating) are not assigned. Assign them with the schematics.
7. **Crimp tooling.** GH (`SSHL-002T-P0.2`), Micro-Fit and Micro-Fit+ terminals and the SBS Mini contacts each need their own crimp tool. The SBS Mini tool part number is still open (`board-specs.md` §10.4).
8. **Harness lengths, mass and bend radii** are not a wire list. The `HARNESS_AND_FASTENERS` mass row (95 g) is unchanged.

## 6. CAD checks added (Layout 02)

- `connector_reserves_clear_of_real_hardware`: every connector and cable-exit reserve against all real parts. `_OPEN` clashes are reported, not counted.
- `connector_reserves_do_not_overlap_each_other`
- `edge_power_connectors_fit_free_board_edges` (§4)
- `head_trunk_and_csi_avoid_tray_pi_cooler_and_yaw_stage`: replaces `HARNESS_HEAD_VERTICAL`, which ran through the compute tray and the Pi cooler.
- `charge_inlet_is_cut_through_rear_panel`
- `pack_disconnect_is_placed_and_serviceable_through_tub_window`
- `c3_carrier_holds_devkitc_clear_of_everything`
- `c3_carrier_gh_headers_fit_two_rows`
- `connector_bodies_clear_of_hardware_and_each_other`
- `mated_plugs_sit_inside_their_reserves`
- `signal_connectors_are_latching_jst_gh`
