# 05 — Harness: connectors, wires and service breaks

| Field | Value |
|---|---|
| Status | Working design, 2026-10-04 ([D-039](../decisions.md#d-039)). Nothing bought, crimped or bench-tested |
| Governs | Every installed cable in the body and chassis, from the pack lead to the yaw junction (PCB-08). Head-internal wiring stays with RP-01 Layout 04 |
| Replaces | RP-06 [connector-schedule.md](../../02-prototypes/RP-06-cad/connector-schedule.md) §3 and §5 for the build. That schedule stays read-only reference; §8 lists the rows changed here |
| Inputs | [04-pcbs/power-boards.md](../04-pcbs/power-boards.md), RP-02 [board-specs.md](../../02-prototypes/RP-02-electrical/board-specs.md), the chassis and body CAD |
| Check | [`check_harness.py`](../01-chassis/v1/cad/check_harness.py) (about 30 s): connector reserves and bodies, edge fit, slide path, NTC break and splices. Result: `generated/harness-checks.json`, **ALL PASS** on 2026-10-04 |
| Evidence labels | `D` vendor data read, `E` estimate, `U` unknown, `W` measured. No `W` value exists yet |

## 1. Decisions

| ID | Decision | Why |
|---|---|---|
| H-01 | **The fused pack feed splits at the fuse** (builder, 2026-10-04). Fuse output and pack negative each fork at a crimped butt splice above the PCB-03 +Y edge. One branch goes to PCB-03 `J3-1` (motors, head), the other to PCB-02 `J2-1` (charger, `OPBUS`). **`W04` and `J2-2` are deleted.** The negative splice is the power star (`PA-15`) | The old path (pack → fuse → PCB-02 on the rear panel → back to PCB-03) had four mated connectors and about 0.5 m of wire. The split halves the pack-to-gate resistance (§6) |
| H-02 | **`J-PK` is the isolator.** Unplug it before mating or unmating `J2-1` or `J3-1`. Every other connector mates and unmates only in `OFF` with the charger unplugged | In `OFF` every body rail is dead (`OPBUS` open, gate open), so a half-mated plug cannot back-power a domain. Only `BATBUS` is live, and it reaches `J2-1`/`J3-1` alone. Micro-Fit parts have no first-mate pins, so the rule is procedural, not mechanical |
| H-03 | **Power and signal never share a housing.** Power is on Micro-Fit+ and Micro-Fit 3.0; signals are on JST GH. The only supplies inside a GH housing are a sensor's own low-current feed (encoder, IMU, nose, TCRT) | `power-implementation-basis.md` §4 and CN-02 |
| H-04 | **Two crimp families, one tool each.** Micro-Fit+ carries only AWG16/18 (Molex 213309-4400). Micro-Fit 3.0 carries only AWG20–24 (one 20–24 AWG tool). **No GH crimping:** every GH cable is a pre-crimped JST GH lead, single-ended where the far end is soldered | A Micro-Fit+ tool covers one gauge pair. AWG20/24 on Micro-Fit+ would need two more tools. GH crimping by hand is unreliable |
| H-05 | **Micro-Fit+ leads use thin-wall wire, UL1061 class (insulation OD ≤ 2.0 mm), not silicone.** This includes the pack lead `W01` | The 206460 16 AWG terminal is specified for 2.00 mm insulation (`D`), and the Molex hand tool for UL1061 wire (`D`). Fine-strand silicone AWG16 is about 2.3–2.6 mm, so the insulation grip would not close |
| H-06 | **`J3-4` and `J8-1` move from Micro-Fit+ to Micro-Fit 3.0.** `J8-1` becomes a 2×3 (43045-0600 class) carrying the pitch/roll pair from `J3-4` and the C2 and display pairs from `J4-2`, all AWG22 | The head trunk's design current is 1.0 A (3.6 A worst stall). Micro-Fit 3.0 at AWG22 carries it, and every head-side power conductor stays on one tool. `J3-4` frees 1.0 mm of PCB-03 −Y edge (margin 0.4 → 1.44 mm) |
| H-07 | **Pack NTC break: a JST SM 2-way wire-to-wire pair**, pre-wired pigtails soldered on, lying in the +Y channel ahead of `J-PK` (X 52–76, Z 41.6–47.4) | GH has no wire-to-wire housing, and the channel holds nothing wider than about 8 mm. The space was freed when the fuse moved up (D-032). The pair's 6.5 × 5.8 mm section passes the 22.6 × 10 mm tub window |
| H-08 | **The body lifts off after 11 plugs (12 with the IMU) are pulled at the body-side boards** (§7.2). There is no separate chassis-body bulkhead connector | The shell must come off to reach the J13 bolts anyway, and that opens access to PCB-02/03 and the C3 carrier. A bulkhead would put two more mated contacts in every chassis lead, including the motor feeds |
| H-09 | **Encoders run from the C3 carrier 3V3, not 5 V** | The MOT3001 Hall board accepts 3.3–5 V (`E`, family data). On 5 V its pulled-up outputs would exceed the ESP32-S3's 3.6 V input limit |

## 2. Power tree as wired

```
 CHASSIS                                                   BODY (frame-mounted)
 cells ─ PCB-01 ─W01─ J-PK ─W03a─ FUSE 15 A ─W03b─ (+)splice ─W03c─ J3-1  PCB-03 ─J3-2/3─W06/07─ #3297 L/R (chassis)
                        │                                 └──────W03d─ J2-1  PCB-02 ─J2-3─W05─ J4-3 PCB-04
                        └────────────W03a−──────────── (−)STAR splice ─W03c/d (−)
 NTC ─W02a─ SM 2p break ─W02b───────────────────────────────────── J2-7  PCB-02 (BQ25798 TS)
```

## 3. Connector families and parts

| Family | Use | Housing | Terminal | Wire | Tool |
|---|---|---|---|---|---|
| Micro-Fit+ 3.0 mm | `J-PK` (wire-to-wire), `J3-1`, `J2-1`, `J3-2`, `J3-3`, `J4-1` (1×2); `J2-3`, `J4-3` (2×2) | Single-row receptacle (215759 series, `D` family) or dual row (206461-0200 for 2×2-class); exact PN at order (`U`) | Female 206460-0041, tin, 16 AWG, 13 A (`D`); 18 AWG sibling; male 215953 series for the `J-PK` plug half (`U`) | AWG16/18 UL1061 | Molex 213309-4400, 16/18 AWG UL1061 (`D`) |
| Micro-Fit 3.0 | `J3-4`, `J4-2`, `J4-4`, `J4-5`, `J5-7`, `J8-1`, `J10-1`, motor inline pairs | 43025 receptacle; 43645/43640 wire-to-wire (`D`) | Female 43030-0007, 20–24 AWG, 8.5 A max (`D`); male 43031 series | AWG22 (motor pairs: the MOT3001's own leads) | Molex 63819-0900 20–24 AWG (`E`, confirm the tool PN) |
| JST GH 1.25 mm | All signals | GHR-xxV-S | Pre-crimped leads (SSHL-002T-P0.2 on AWG28) | AWG28 pre-crimped, double- or single-ended | None. Engineer PA-09 class only for re-pinning |
| JST SM 2.5 mm | Pack NTC break | SMP-02V-BC / SMR-02V-B | Pre-wired pigtail pair | AWG22–26 pigtails, soldered | None |
| JST EH | XC330 yaw servo `J3-5` | ROBOTIS 3-pin cable (vendor) | Vendor | Vendor | None |
| Butt splice | `BATBUS` + and − forks | Insulated 12–10 AWG seamless butt splice: 2 × AWG16 in one end, 1 × AWG16 folded double in the other; adhesive dual-wall heat-shrink over it | — | AWG16 | Ratcheting insulated-terminal crimper |
| USB-C plug | Pi 5 power `W10` | Right-angle, solder type, with a 56 kΩ Rp from CC to VBUS inside the shell (CN-03) | Soldered | AWG18 | Soldering iron |

## 4. Wire list

Lengths are `E`: Manhattan routes through CAD waypoints plus service slack. Cut at the first harness build and record as `W`. "P" means pre-crimped GH; "S" means soldered.

### 4.1 Pack and power

| Cable | From → to | Ends | Conductors | Length | Route |
|---|---|---|---|---|---|
| `W01` pack lead | Pack P+ (cell stack) / TIFPS0629 P− → `J-PK` pack half | S / Micro-Fit+ 1×2 male | 2 × AWG16 UL1061 red/black | 120 | Out through the +Y tub window into the channel |
| `W02a` NTC, pack side | 103AT-2 on the cell → SM 2p plug | S / SM pigtail (S) | 2 × AWG26 | 100 | With `W01`, through the window, forward in the channel |
| `W02b` NTC, body side | SM 2p receptacle → PCB-02 `J2-7` | S / GH 2 (P, single-ended) | 2 × AWG28 | 240 | Up past the fuse, along the +Y side to the PCB-02 top layer |
| `W03a` fused feed + | `J-PK` body half → fuse holder input (front end, X 82) | Micro-Fit+ 1×2 female / crimp onto holder lead | 1 × AWG16 | 110 | Channel, up the front of the fuse bracket |
| `W03a−` pack − | `J-PK` body half → negative star splice | Micro-Fit+ / splice | 1 × AWG16 | 70 | Up beside the bracket |
| `W03b` | Fuse holder output (rear end, X 52) → + splice | Holder lead / splice | 1 × AWG16 | 30 | Straight back |
| `W03c` BATBUS-M | Splices → PCB-03 `J3-1` | Splice / Micro-Fit+ 1×2 | 2 × AWG16 | 60 | Splices to `J3-1` (2.65 mm gap in CAD) |
| `W03d` BATBUS-C | Splices → PCB-02 `J2-1` | Splice / Micro-Fit+ 1×2 | 2 × AWG16 | 220 | Rearward along +Y, across behind PCB-04 to the PCB-02 −Y edge |
| ~~`W04`~~ | Deleted (H-01) | | | | |
| `W05` `OPBUS` + `CHGBUS` | PCB-02 `J2-3` → PCB-04 `J4-3` | Micro-Fit+ 2×2 both ends | 4 × AWG18 | 170 | Under-board slot to the PCB-04 +Y edge |
| `W06`/`W07` `PB-DRIVE-L/R` | PCB-03 `J3-2`/`J3-3` → #3297 `VM`/`GND` pins (power-boards §2.3) | Micro-Fit+ 1×2 / S, with 100 µF + 0.1 µF at `VM` | 2 × AWG18 each | 50 | Edge to the adjacent driver |
| `W08`/`W09` motor L/R | #3297 `AOUT1+BOUT1` / `AOUT2+BOUT2` (bridges paralleled) → MOT3001 motor pair | S at the board / Micro-Fit 3.0 1×2 wire-to-wire at the inline reserve | Driver side 2 × AWG22; motor side the MOT3001's own leads | 230 | Motor connector → across the deck behind the posts (`HARNESS_MOTOR_BRANCH`) → tie bridge (CH-082) → inline pair |
| `W10` `PB-COMPUTE` | PCB-04 `J4-1` → Pi 5 USB-C | Micro-Fit+ 1×2 / right-angle USB-C plug (S) | 2 × AWG18 | 100 | Pi −Y edge, down past the tray (`PI5_POWER_PIGTAIL_DROP`) |
| `W11` `PB-SAFE-BASE` | PCB-04 `J4-4` → C3 `J10-1` | Micro-Fit 3.0 2×1 both ends | 2 × AWG22 | 110 | −Y side up to the carrier front edge |
| `W12` `PB-AUDIO-OUT` | PCB-04 `J4-5` → PCB-05 `J5-7` | Micro-Fit 3.0 2×1 both ends | 2 × AWG22 | 160 | +Y, then forward (BO-006) |
| `W13` `PB-HEAD` pitch/roll | PCB-03 `J3-4` → PCB-08 `J8-1` pins 1/4 | Micro-Fit 3.0 2×1 / one leg of the `J8-1` 2×3 plug | 2 × AWG22 | 160 | −Y riser (`HARNESS_HEAD_RISER_*`) |
| `W14` `PB-SAFE-C2` + `PB-DISPLAY` | PCB-04 `J4-2` → `J8-1` pins 2/5 and 3/6 | Micro-Fit 3.0 2×2 / the other leg of the `J8-1` plug | 4 × AWG22 | 140 | −Y riser, joins `W13` in one sleeve |
| `W15` yaw servo | PCB-03 `J3-5` → XC330-M181 | ROBOTIS 3-pin EH cable | Vendor | 120 | Up to the servo at X −8…26, Y 27…47 |
| `W16` charge inlet | Adapter → PCB-02 USB-C | No cable | — | — | Rear-panel cut-out |

### 4.2 Signals (all GH, AWG28 pre-crimped)

| Cable | From → to | Leads | Length | Notes |
|---|---|---|---|---|
| `W20` | PCB-02 `J2-4` ↔ PCB-04 `J4-6` | GH10, double-ended | 60 | |
| `W21` | `J2-5` ↔ PCB-03 `J3-6` | GH6, double-ended | 110 | |
| `W22` E-stop | XA1E tabs → `J3-7` | GH4, single-ended (S at the switch) | 150 | Two twisted pairs |
| `W23a` | PCB-08 `J8-3` ↔ `J3-8` | GH8, double-ended | 200 | −Y riser |
| `W23b` | `J8-5` ↔ `J2-6` | GH8, double-ended | 160 | −Y riser |
| `W24` head link | PCB-09 `J9-1` ↔ `J8-4` | GH6, double-ended, pairs twisted | 170 | RS-422 |
| `W25` base link | `J9-2` ↔ C3 `J10-2` | GH6, double-ended, pairs twisted | 200 | RS-422 |
| `W26`–`W28` audio | Per [02-body BOM](../02-body/v1/BOM.md) (BO-006) | — | — | Unchanged |
| `W29` IMU | PCB-07 ↔ `J10-7` | GH8 | — | PCB-07 is HOLD; its lead is in the IMU mass row |
| `W30`/`W31` encoders | MOT3001 encoder wires (cut from the vendor cable, ~60 mm kept) → `J10-3`/`J10-4` | GH4, single-ended, soldered to the vendor wires under heat-shrink | 220/230 | Along the deck, up the −Y side |
| `W32`/`W33` driver logic | #3297 `SLP`, `AIN1+BIN1`, `AIN2+BIN2`, `FLT`, `GND` → `J10-5`/`J10-6` | GH6, single-ended (S at the board) | 180/80 | D-038 mapping |
| `W34` nose | GP2Y0A21 (S) and the Hall board pads (S) → `J10-8` | GH5, single-ended | 220 | `HARNESS_NOSE_J10_8_*` route (D-013, D-027) |
| `W36` rear TCRT | TCRT5000 legs (S) → `J10-10` | GH4, 350 mm single-ended (CH-020) | 350 | [rear-tcrt-lead.md](../01-chassis/v1/research/rear-tcrt-lead.md) |
| `W37` CSI | Pi 5 ↔ Camera Module 3 | PCN-36 15-to-22 FFC | — | Unchanged (BA-05) |
| `W38` | PCB-03 → `J10-11` | GH3, double-ended | 90 | |
| `W39` | `J10-12` ↔ `J3-9` | GH4, double-ended | 100 | |

**Pre-crimped GH lead buy list** (lengths rounded up to the stock 50/100/150/200/300 mm, one spare of each):

| Circuits | Double-ended | Single-ended |
|---|---|---|
| GH2 | — | 1 × 300 (`W02b`) |
| GH3 | 1 × 100 (`W38`) | — |
| GH4 | 1 × 150 (`W39`) | 1 × 200 (`W22`), 2 × 300 (`W30`/`W31`); `W36` 350 already on CH-020 |
| GH5 | — | 1 × 300 (`W34`) |
| GH6 | 1 × 150 (`W21`), 1 × 200 (`W24`), 1 × 300 (`W25`) | 1 × 200 (`W32`), 1 × 100 (`W33`) |
| GH8 | 1 × 300 (`W23a`), 1 × 200 (`W23b`) | — |
| GH10 | 1 × 100 (`W20`) | — |

**Wire stock.** AWG16 UL1061 3 m red + 3 m black (needs about 1.0 m). AWG18 UL1061 3 m + 3 m (about 1.1 m). AWG22 stranded 5 m + 5 m (about 1.4 m). AWG26 1 m pair for the NTC. 3:1 adhesive heat-shrink in 3.2/4.8/6.4 mm sizes, and 4 mm braided sleeving for the −Y riser bundle.

## 5. Pinouts

Pin 1 is the housing's marked cavity. On a dual-row Micro-Fit, pins 1…n are the latch row and the second row continues under them. **Rule:** on 2-circuit power, pin 1 is +, pin 2 is the return. On dual-row power, each return sits directly opposite its supply.

### 5.1 Power

| Connector | Pins |
|---|---|
| `J-PK` (Micro-Fit+ 1×2) | 1 PACK+, 2 PACK− |
| `J3-1`, `J2-1` (Micro-Fit+ 1×2) | 1 BATBUS+, 2 PGND (star) |
| `J2-3` ↔ `J4-3` (Micro-Fit+ 2×2) | 1 OPBUS, 2 CHGBUS, 3 OPBUS_RTN, 4 CHGBUS_RTN |
| `J3-2`, `J3-3` (Micro-Fit+ 1×2) | 1 PB-DRIVE+, 2 GND |
| `J4-1` (Micro-Fit+ 1×2) | 1 +5V15_PI, 2 GND |
| `J4-4` ↔ `J10-1`, `J4-5` ↔ `J5-7` (Micro-Fit 3.0 2×1) | 1 +5 V branch, 2 GND |
| `J3-4` (Micro-Fit 3.0 2×1) | 1 +5V_HEAD_PR, 2 GND_HEAD |
| `J4-2` (Micro-Fit 3.0 2×2) | 1 +5V_C2, 2 +5V_DISPLAY, 3 GND_C2, 4 GND_DISPLAY |
| `J8-1` (Micro-Fit 3.0 2×3) | 1 +5V_HEAD_PR, 2 +5V_C2, 3 +5V_DISPLAY, 4 GND_HEAD, 5 GND_C2, 6 GND_DISPLAY |
| Motor inline (Micro-Fit 3.0 1×2 wire-to-wire) | 1 OUT1 (`AOUT1+BOUT1`), 2 OUT2 (`AOUT2+BOUT2`). Set the forward sense in firmware after the first spin |
| NTC break (SM 2p) | 1 TS, 2 TS_RTN (thermistor; polarity-free) |
| `J2-7` (GH2) | 1 TS, 2 TS_RTN |

### 5.2 Signals

Each GH cable puts GND at pin 1 where it carries no supply, and keeps each differential or analog signal next to its return.

| Connector | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| `J2-4` ↔ `J4-6` (`W20`) | GND | +5V_C2 (pull-up supply to PCB-02) | PG_C2 | PG_BASE | SEQ_EN (latch out) | PG_COMPUTE | PG_DISPLAY | PG_AUDIO | spare | GND |
| `J2-5` ↔ `J3-6` (`W21`) | GND | CHARGE_ABSENT | ENERGY_OK | SYSTEM_ARM | MOTOR_PRESENT | GND | | | | |
| `J3-7` (`W22`) | LOOP_IN (NC1) | LOOP_OUT (NC1) | STAT_A (NC2) | STAT_B (NC2) | | | | | | |
| `J3-8` ↔ `J8-3` (`W23a`) | SIG_REF | SERVO_DATA | C2_READY_H | C2_READY_L | E_STOP_STATUS | MOTOR_PRESENT | HEAD_OC | HEAD_PGOOD | | |
| `J2-6` ↔ `J8-5` (`W23b`) | SIG_GND | V_PACK_ANA | SIG_GND | STAT | INT_PB | KILL | CHG_ABSENT_3V3 | spare | | |
| `J9-1` ↔ `J8-4`, `J9-2` ↔ `J10-2` | GND | TX+ | TX− | RX+ | RX− | spare | | | | |
| `J10-3`/`J10-4` (`W30`/`W31`) | GND | +3V3_ENC | ENC_A | ENC_B | | | | | | |
| `J10-5`/`J10-6` (`W32`/`W33`) | SLP | IN1 | IN2 | FLT | GND | spare | | | | |
| `J10-7` (`W29`) | +3V3 | GND | SCLK | MOSI | MISO | CS | INT1 | INT2 | | |
| `J10-8` (`W34`) | +5V (GP2Y) | GND | GP2Y_VO | +3V3 (Hall) | HALL_OUT | | | | | |
| `J10-10` (`W36`) | LED_A | LED_K | TCRT_OUT | GND | | | | | | |
| `J10-11` (`W38`) | ESTOP_N | +3V3 (pull-up ref) | GND | | | | | | | |
| `J10-12` ↔ `J3-9` (`W39`) | GND | C3_READY | MOTOR_PRESENT | GND | | | | | | |
| `J3-5` (EH3, ROBOTIS) | GND | VDD | DATA | | | | | | | |

`J2-4`/`J4-6` signal names follow RP-02 §6.4. The schematic may rename them, but not move a supply onto an end pin. The `W20` +5V_C2 replaces the RP-02 §8 `+5V_C2` line, which had no cable. `J10-8` and `J10-10` are unchanged from [nose-hall-board.md](../01-chassis/v1/research/nose-hall-board.md) and [rear-tcrt-lead.md](../01-chassis/v1/research/rear-tcrt-lead.md); the nose sensor is now the GP2Y0A21YK0F (D-019), not the A41.

**Required at the receiving board (schematic):** a series resistor of 1 kΩ or more on every slow input that crosses a connector (READY, status and ADC lines), and 33–100 Ω on encoder and SPI lines. That keeps any half-mated or unpowered case to a few mA into ESD diodes (`PA-11.6`).

## 6. Calculations (`E`)

Resistance: AWG16 13.2, AWG18 21.0, AWG22 53, AWG28 213 mΩ/m at 20 °C, ×1.16 hot. Micro-Fit+ contact: 10 mΩ maximum (`D`), 2.5 mΩ typical assumed.

| Path | Wire | Contacts | Fuse, holder, splices | Total | Drop |
|---|---|---|---|---|---|
| Pack → PCB-03, split (H-01), typical | 8.7 mΩ | 4 × 2.5 = 10 mΩ | 6.4 mΩ | **25 mΩ** | 0.25 V at 10 A |
| Same, Molex maximum | 8.7 | 4 × 10 = 40 | 6.4 | **55 mΩ** | 0.55 V at 10 A |
| Old route via PCB-02, typical / maximum | — | 8 contacts | — | 44 / 104 mΩ | 0.44 / 1.04 V |
| `W10` Pi feed (AWG18, 100 mm, Micro-Fit+, USB-C) | | | | 18 mΩ | 43 mV at 2.4 A, 90 mV at 5 A; inside the 100 mV steady allowance |
| `W13` body side (AWG22, 2 Micro-Fit 3.0 mates) | | | | 40 mΩ | 40 mV at 1.0 A design, 143 mV at a 3.6 A stall; the 150 mV budget's body share holds at design |

- **Against the ledger.** The 10 mΩ wiring allowance in the pack model (`2·22 + 30 + 10`) was low. With the split, the pack model becomes 44 + ≤ 30 (TIFPS0629 acceptance) + 25 ≈ **99 mΩ** typical. That is still inside the ledger's 80–100 mΩ range, but at its top. RP-02 §8.1 corner D (cold, aged) should be recomputed with the measured path. Measure it (4-wire, 5 A) in Phase C.
- **Currents against ratings.** `BATBUS` peak is about 10.2 A (power-boards §4). `J-PK` and `J3-1` carry all of it, against 13 A per Micro-Fit+ AWG16 contact (`D`). `J2-1` carries `OPBUS` plus charge, about 5.5 A worst. Fuse: 15 A ATOF (CH-029). The drive feeds take 2.4 A, the head trunk 1.0 A (3.6 A worst), and Micro-Fit 3.0 is rated 8.5 A (`D`).
- **Mass.** Conductors about 45 g, plugs, splices, sleeving and ties about 28 g: **about 73 g**. This excludes the pack lead, IMU lead, TCRT lead and audio cables, which have their own mass rows. The `HARNESS_AND_FASTENERS` row is 95 g, which leaves about 22 g for loose fasteners. The register is unchanged; weigh the built harness.

## 7. Service procedures

### 7.1 Pack out

1. Put the robot in `OFF` and unplug the charger.
2. Remove the four J11A screws and lower the hatch with the pack strapped to it.
3. Slide the `J-PK` pair in through the tub window and unplug it.
4. Pull the NTC pair back to the window and unplug it.
5. The pack is free. Refit in reverse: NTC first, then `J-PK`.

### 7.2 Body off the chassis

1. Pack out (7.1), or at least `J-PK` open (H-02).
2. Remove the shell (body README) and the rear service panel.
3. Unplug the 11 chassis leads at the body boards:
   - `J3-1` and `J2-1`: the `BATBUS` branches. Their splices stay with the chassis.
   - `J3-2` and `J3-3`: the drive feeds.
   - `J2-7`: the NTC.
   - `J10-3`, `J10-4`, `J10-5`, `J10-6`, `J10-8`: encoders, driver logic and nose.
   - `J10-10`: rear TCRT.
4. Leave `J10-7` (IMU) to come off with its lead, or unplug it too if PCB-07 is fitted. That makes 12.
5. Undo J13 and lift the body (body README §Body frame/chassis assembly).

Every chassis-side lead carries at least 40 mm of slack at its body-side plug, so the plug can be withdrawn before the body moves. **Check hand and tool reach at the first assembly.** PCB-03's edge plugs sit under the compute tray at Z 64–75 and are reached from ±Y with the shell off.

### 7.3 Head off

Unchanged (connector-schedule §3.4): unplug `J8-1`, `J8-3`, `J8-4`, `J8-5` and the CSI at the Pi, then lift the head with PCB-08.

## 8. Changes to the RP-06 schedule rows

| Row | Was | Now |
|---|---|---|
| `W01` | AWG16 silicone | AWG16 UL1061 (H-05) |
| `W02` | GH2 straight to `J2-7`, break open | `W02a`/`W02b` with the SM 2p break in the channel (H-07) |
| `W03`/`W04` | Fuse on a PCB holder → PCB-02 → `W04` → PCB-03 | Inline holder (D-032), split at splices; `W04` and `J2-2` deleted (H-01) |
| `W06`/`W07` | DRV8874 carrier `VIN` | #3297 `VM` pin (D-038) |
| `W08`/`W09` | #4804 leads | MOT3001 cut lead, Micro-Fit 3.0 inline pair, paralleled outputs |
| `W13`/`W14`, `J8-1` | Micro-Fit+ 1×2 + Micro-Fit 3.0 2×2 into a Micro-Fit+ 2×3 | All Micro-Fit 3.0 AWG22, one 2×3 plug (H-06) |
| `W30`/`W31` | #4804 encoder, Vcc 3.5–20 V | MOT3001 encoder on 3V3 (H-09) |
| `W32`/`W33` | DRV8874 `SLEEP`, `EN/IN1`, `PH/IN2`, `CS`, `FAULT` | DRV8833 `SLP`, `IN1`, `IN2`, `FLT` (D-038) |
| `W34` | GP2Y0A41 + tact switch, PH3 at the sensor | GP2Y0A21 + DRV5055 Hall, soldered at the sensor (D-013, D-019, D-027) |
| `W36` | 5 V/GND/analog/digital breakout | Bare TCRT lead, LED and load on PCB-10 (D-016) |
| §5 items 1, 6, 7, 8 | Open | Closed here: NTC break, pinouts and mating rule, tooling, wire list |

## 9. Open

- [ ] Molex housing and male-terminal part numbers for each Micro-Fit+ position (single-row 215759 receptacle and its plug). Confirm the 63819-0900 tool for 43030/43031. Get quotes; the Molex tools are the main cost.
- [ ] MOT3001 6-wire colour code and encoder supply range on receipt (`U`): meter the cable before cutting it.
- [ ] Received JST SM pair: measure its mated section against the 6.5 × 5.8 mm envelope.
- [ ] Crimp qualification: pull-test three samples per tool and gauge to IPC/WHMA-A-620 Class 2, and section one Micro-Fit+ AWG16 crimp.
- [ ] First harness build: cut-to-length values (`W`), the 4-wire pack → `J3-1` resistance at 5 A, and hand reach for the 12 body-lift plugs. Then weigh the harness against §6.
- [ ] The body model (`02-body/v1/cad/body_v1_model.py`) carries pre-D-031 driver positions and the pre-D-032 fuse envelope. Its PCB-03 edge reserves clash with the stale drivers, and its PCB-04 edge reserves and the `J4-1` plug clash with `BODY_FRAME_MAIN_PRINT` (108 mm³ per reserve, 45.7 mm³ at `J4-1`). These clashes predate D-039 and were confirmed against the HEAD model. The frame/PCB-04 edge clash is real body-v1 geometry and must be fixed before the frame is printed.
- [ ] `body_v1_model.wheel_assembly()` raises `NameError: WHEEL_MODEL` (pre-existing).
