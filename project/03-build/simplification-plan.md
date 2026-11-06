# Simplification plan: minimal safety and off-board charging

| Field | Value |
|---|---|
| Status | **PLAN, 2026-11-06.** Nothing in the ledger, BOM, CAD, harness or board folders has been changed yet. Each level below is reviewed with the builder and then applied |
| Builder decisions (2026-11-06) | **1. Minimal, scrappy safety for the v1 desk robot.** No industrial-style permit chains, latching e-fuses, hold-up or sequencing. This replaces RP-02 `BD-01` ("custom PCBs; breakout modules bench-only"). **2. The pack is charged outside the robot** by a bought balance charger. There is no in-robot charger and no USB-C inlet |
| Ledger entry | To be written as the next free D-number (D-093; D-092 is used on the unmerged `pcb-09-c0-link-adapter` branch) once Level 0 is approved |
| Why | 14 custom boards, each needing fab, assembly, bring-up and possible revisions, is too slow for v1. Most of the count and almost all the bring-up risk come from the RP-02 safety architecture, not from the robot's needs |

---

## Background: how we got here

### Board count before this plan (2026-11-06)

There were 14 custom boards (PCB-01 is the bought TIFPS0629). On `main`, 6 were designed at rev A. PCB-09 was finished on the unmerged branch.

| State | Boards |
|---|---|
| Designed, rev A | PCB-05, 06, 09 (branch), 10, 11, 13, 15 |
| In progress | PCB-02: routed, ERC/DRC clean, 10 A path sized; populated-STEP fit and outputs open |
| Not started | PCB-03, 04, 07, 08, 12, 14 |

### Why there were so many boards

RP-02 decision `BD-01` chose custom PCBs because its spec asks for behaviour that bought modules can't give:

- a 6-FET hardware permit chain with an LTC4368 surge stopper (`BD-07`);
- latching e-fuses, hold-up capacitors and power-good sequencing on every branch (`BD-11`);
- a hostless I²C charger with JEITA temperature limits (`BD-09`, D-040);
- watchdogs on both MCU carriers (`BD-10`, D-068);
- an arm latch with fresh-arm edges (D-082) and an `ENERGY_OK` comparator.

That is close to industrial-safety level. The robot is a ~1 kg desk robot with two 1.8 A-stall gearmotors, small Feetech servos, a fused 2S1P pack and a bought pack protection board. Keep the spec and you have to keep the boards. Relax the spec and most of the boards become modules.

### Risk is in complexity, not count

Bring-up time scales with board complexity. Ranked by bring-up risk:

| Risk | Boards |
|---|---|
| Very high | PCB-02 (119 parts, QFN charger, 10 A path, CP-OI-06 could block charging), PCB-03 (two LTC3119s losing ~3 W, surge stopper, regeneration clamp) |
| High | PCB-04 (five converters, e-fuses, hold-up), PCB-05 (WLCSP assembly needing X-ray) |
| Medium | PCB-12, PCB-09, PCB-10, PCB-13 (PD NVM image and programming jig) |
| Low | PCB-06, PCB-11, PCB-15, PCB-08, PCB-14 (passive or a few parts) |

The two decisions remove both very-high boards, one high board and one medium board.

---

## Level 0 — Decisions and governance

### New ledger entry (D-093, to write)

**Minimal-safety power architecture and off-board charging.** It replaces RP-02 `BD-01` for the build. Bought modules may be installed in the robot. A custom board is made only where nothing bought fits the geometry or the interface.

### Decisions superseded or amended

| Decision | What it set | Fate |
|---|---|---|
| RP-02 `BD-01` | Custom power boards; modules bench-only | **Replaced** by D-093 |
| RP-02 `BD-05` | LTC3119 buck-boost for the head rail | **Superseded**: bought buck-boost module |
| RP-02 `BD-07` | LTC4368 motor gate, shunt, FETs | **Superseded**: no gate. The fuse plus the Level 1 kill path |
| RP-02 `BD-09` | Hostless charger control | **Superseded**: off-board charging |
| RP-02 `BD-10` | Carrier watchdog block | **Kept on PCB-10** (already designed). **Dropped from PCB-12** |
| RP-02 `BD-11` | `TPS630701` + `TPS259474L` e-fuses, `SYS` gate, sequencing latch | **Superseded**: bought buck modules, no sequencing |
| RP-02 `BD-13` | Per-axis protection layers | **Superseded**: Feetech's own overload/temperature protection and firmware limits |
| RP-02 `brownout-restart-contract.md` | Hold-up, thresholds, restart contract | **Retired for the build**; firmware low-battery cut-off instead (Level 5) |
| [D-019](decisions.md#d-019) | TIFPS0629 as PCB-01 | **Kept.** It is now the main safety device, so its bench acceptance matters more |
| [D-038](decisions.md#d-038) | Power-board build deltas | **Mostly superseded**: keep only the DRV8833 facts and the TVS/bulk at `VM` (Level 1) |
| [D-040](decisions.md#d-040) | Charge path: PCB-13 + PCB-02 charger block | **Superseded** |
| [D-041](decisions.md#d-041) | Mushroom = `LTC2954` power button, motor stop via `INT` | **Amended**: the mushroom stays (BO-018) and drives the bought pushbutton power switch |
| [D-064](decisions.md#d-064) | Design every board, then procure together | **Kept, smaller batch**: only PCB-08, PCB-12 and PCB-14 are left to design |
| [D-069](decisions.md#d-069) | PCB-13 inputs | **Superseded** (board deleted) |
| [D-082](decisions.md#d-082) | Fresh-arm, `PERMIT_OK`, `ARM_REQ` | **Superseded**: no arm latch |
| [D-083](decisions.md#d-083)–[D-091](decisions.md#d-091) | PCB-02 mount and layout | **Superseded**; the work is archived, not deleted |
| [D-047](decisions.md#d-047), D-046 | Yaw and head servo rails | **Amended**: rails come from bought modules (Level 3) |

### Housekeeping

- Merge `pcb-09-c0-link-adapter` to `main` anyway. PCB-09 is kept (Level 2).
- Archive the PCB-02 and PCB-13 KiCad work in their folders with a "Superseded by D-093" banner. Don't delete it: it is reference if v2 brings charging back inside.
- Update memory: the PCB workflow tracker and `power-distro-working-design` memories go stale after D-093.

---

## Level 1 — System architecture

### Power tree after the change

```
 CHASSIS                                    BODY
 cells ─ PCB-01 (TIFPS0629) ─W01─ J-PK ─ FUSE 15 A ─ splice ─┬─ CHARGE PORT (rear panel, unswitched)
   │                                                         └─ PUSHBUTTON POWER SWITCH (module) ── switched bus
   └─ balance lead (3 wires) ─ break ─────────────────────────── BALANCE PORT (rear panel)
                                                                    │
 switched bus ─┬─ #3297 L / R (drive, via VM with TVS + 100 µF each)
               ├─ buck-boost module → 5.5 V head pitch/roll
               ├─ buck-boost module → 11.1–12 V yaw servo
               ├─ buck module 5.1 V 5 A → Pi 5 (USB-C, W10)
               └─ buck module(s) 5 V → C3 carrier, audio, C2, display
```

### Modes

| Before | After |
|---|---|
| `OFF`, `CHARGE`, `OPERATE`, plus arm/permit states | **`OFF` and `ON` only** |
| Charging allowed only with motors blocked by `CHARGE_ABSENT` | **Charge only in `OFF`** (operating rule, not enforced in hardware) |

### Safety functions kept

| Function | Where |
|---|---|
| Cell over-voltage, under-voltage, over-current, short circuit, balancing | PCB-01 TIFPS0629 (D-019), §3 acceptance still required |
| Wiring protection | 15 A ATOF fuse (CH-029) |
| Cell over-temperature | Bourns AC72ABD in the cell strap (CH-024) |
| Hard power off | The mushroom on the pushbutton power switch, which cuts the whole switched bus |
| Motor stop on a hung base MCU | **Already on PCB-10**: the TPS3436 watchdog drops `BASE_READY`, and the 74LVC1G08 AND gate holds both DRV8833 `nSLEEP` low (power-boards §2.4) |
| DRV8833 over-voltage on regeneration | SMBJ8.5A TVS + 100 µF + 0.1 µF soldered at each #3297 `VM` (power-boards §2.2, cheap, kept) |
| Driver over-current | The DRV8833's own chopping and over-current trip |
| Servo overload | Feetech's own protection, plus torque/current limits in firmware |
| Low battery | **Firmware** (Level 5), reading a bought current/voltage monitor |

### Safety functions dropped

The motor gate and surge stopper, the permit chain and arm latch, `ENERGY_OK`/`PERMIT_OK`/`CHARGE_ABSENT`, the e-fuses, hold-up and sequencing, the head/yaw current comparators, the C2 watchdog and the pack NTC to a charger.

---

## Level 2 — Board by board

| Board | Before | After | Design work left |
|---|---|---|---|
| PCB-01 | Bought TIFPS0629 | **Unchanged** | Bench acceptance (power-boards §3) |
| **PCB-02** charger, latch, sense | Routed, not released | **Deleted.** Latch → pushbutton power switch module; charger → off-board; pack sense → monitor module; comparators → firmware | — |
| **PCB-03** motor gate, head and yaw rails | Not started | **Deleted.** Head rail and yaw rail → buck-boost modules; drive feeds wired straight from the switched bus; TVS/bulk at `VM`. The yaw servo plug moves to PCB-08 | — |
| **PCB-04** five branch converters | Not started | **Deleted.** 2–4 buck modules (Level 3) | — |
| PCB-05 audio front end | Rev A | **Kept by default.** Optional swap to breakouts (Level 10 Q6) | Procure |
| PCB-06 ×4 mics | Rev A | **Kept by default**; goes with PCB-05 | Procure |
| **PCB-07** base IMU | HOLD | **Deleted**; a bought SPI IMU breakout on `J10-7` | — |
| PCB-08 yaw junction | Not started | **Kept custom, simpler.** Loses the permit and status sideband; **gains the yaw servo plug** (`+12V_YAW`, GND, `SERVO_DATA`) that was `J3-5` on PCB-03 | Design |
| PCB-09 C0 link adapter | Rev A (branch) | **Kept**; merge the branch | Procure |
| PCB-10 C3 carrier | Rev A | **Kept, no re-spin.** `J10-12` (`C3_READY`/`MOTOR_PRESENT` to PCB-03) is left unconnected. Its watchdog and AND gate become the motor kill | Procure |
| PCB-11 status LED | Rev A | **Kept** | Procure |
| PCB-12 C2 head carrier | Not started | **Simplified**: ESP32-S3-Zero, servo bus half-duplex, head-link RS-422 and display link. **No watchdog, no `ARM_REQ`, no READY pair.** Or the bought Waveshare ESP32 Servo Driver if it fits the head (Level 10 Q5) | Design, or a fit check |
| **PCB-13** charge inlet | Rev A | **Deleted.** Its rear-panel pad takes the charge and balance ports | — |
| PCB-14 ×3 yaw rotor joiners | HOLD | **Kept custom.** Passive; nothing bought fits the clock spring. Still needs the ZIF ≤ 2.0 mm tall pick | Design |
| PCB-15 nose Hall | Rev A | **Kept** | Procure |

**Result:** custom designs drop from 14 to 9. Three are left to design (PCB-08, 12, 14), all low or medium complexity. Five boards are deleted: 02, 03, 04, 07, 13.

### Rule for interfaces

Boards already designed keep their connectors. Bought modules get soldered pigtails ending in the connector the board expects. For example, the 5 V module feeding PCB-10 gets a Micro-Fit 3.0 2×1 lead to `J10-1`, and the module feeding PCB-05 gets one to `J5-7`. No designed board is re-spun.

---

## Level 3 — Bought modules

Part classes, not orders. Stock and prices are checked at Level 3 review. Pololu has India distributors listed (Fab.to.Lab, MG Super Labs), but stock is patchy. TME counts as an import ([D-066](decisions.md#d-066)).

| Function | Replaces | Candidate class | Notes |
|---|---|---|---|
| Power on/off latch | PCB-02 `LTC2954` | Pololu Big Pushbutton Power Switch (HP/MP class) | Must carry ~10–11 A peak at 6.0–8.4 V (power-boards §4). Current rating and OFF current are `U` until read from Pololu's page. The mushroom (BO-018) wires to its button input |
| Head pitch/roll 5.5 V | PCB-03 LTC3119 #1 | Pololu adjustable buck-boost (S18V20ALV class, 4–12 V), set to 5.5 V | Check the current against the 2.8 A aligned-stall allowance; a 2 A module may need a 3 A class part |
| Yaw servo rail | PCB-03 LTC3119 #2 | Pololu S18V20F12 (12 V ±4 %, 2.9–32 V in, 2 A typical) **or** the adjustable S18V20ALV set to 11.1 V | The 12 V part's high corner is 12.48 V against the ST3215-HS 12.6 V maximum: almost no room for regeneration. **Prefer 11.1 V adjustable** (power-boards §4A already found ~2.5× torque margin there). 2.4 A locked rotor exceeds 2 A: set the servo's current limit in firmware |
| Pi 5 | PCB-04 compute branch | 5.1 V, ≥ 5 A buck with EN (Pololu D36V50F5 / D24V50F5 class) | Feeds the existing `W10` USB-C plug with its 56 kΩ Rp |
| C3, audio, C2, display | PCB-04 four branches | One or two 5 V 2.5–3 A bucks (Pololu D36V28F5 class) | Consolidating saves space; separate outputs only where the harness already splits them (Level 10 Q3) |
| Pack voltage/current | PCB-02 pack sense, PCB-03 INA2181 | INA226 or INA219 breakout on the switched bus, I²C | Put it after the switch so it draws nothing in `OFF` |
| Base IMU | PCB-07 | **SPI** 6-axis breakout at 3.3 V (LSM6DSOX / ISM330DHCX class) | Must match the `J10-7` SPI pinout PCB-10 already has (+3V3, GND, SCLK, MOSI, MISO, CS, INT1, INT2). ICM-42688 breakouts are scarce in India (Elecrow ~$88). BNO085 needs RST/WAKE pins `J10-7` doesn't have |
| Charger | PCB-02 BQ25798, PCB-13 | 2S balance charger with a Li-ion 4.20 V/cell mode (not LiHV), 1–2 A | Outside the robot. Does not read the 103AT NTC |
| Optional all-in-one | PCB-03/04 partly | FPV-drone power distribution board with BECs and a current sensor | Option only; most BECs can't give the Pi its 5 A |

---

## Level 4 — Harness ([05-harness](05-harness/README.md))

### Power wires

| Wire | Before | After |
|---|---|---|
| `W01`, `W03a`, `W03a−`, `W03b` | Pack → `J-PK` → fuse → splices | **Unchanged** |
| `W02a`/`W02b` NTC + SM 2p break | NTC to PCB-02 `J2-7` | **Deleted** (or kept as an optional firmware temperature input, Level 10 Q4). Its route is reused for the balance lead |
| **New** balance lead | — | 3 wires from the cells (B−, mid, B+) to a break near `J-PK`, then on to the rear-panel balance port. **CAD check:** H-07 says the channel holds nothing wider than about 8 mm; a JST-XH 3P housing is about 10 mm wide. Use a narrower break or re-route |
| `W03c` BATBUS-M → PCB-03 `J3-1` | | **Rerouted**: the motor branch now leaves the **switched** bus, not the splice |
| `W03d` BATBUS-C → PCB-02 `J2-1` | | **Reused route**: splice → rear area → power-switch input and the charge port |
| `W05` `OPBUS`/`CHGBUS` | PCB-02 → PCB-04 | **Replaced** by the switched-bus distribution (a splice or small bus bar). `CHGBUS` is gone |
| `W06`/`W07` drive feeds | PCB-03 → #3297 `VM` | From the switched bus; TVS + 100 µF + 0.1 µF still at `VM` |
| `W10` Pi, `W11` C3, `W12` audio | PCB-04 → board | Module → board, same far-end connectors |
| `W13` head pitch/roll, `W14` C2/display | PCB-03/04 → `J8-1` | Modules → `J8-1`, same 2×3 plug |
| `W15` yaw servo | PCB-03 `J3-5` | **From PCB-08**, with 12 V from the yaw module |
| `W16` charge inlet | PCB-13 → `J2-8` | **Deleted** |
| **New** charge lead | — | Unswitched bus → rear-panel charge port (XT30-class), AWG16–18 |

### Signal wires

| Wire | Before | After |
|---|---|---|
| `W20` | PCB-02 ↔ PCB-04 power-good/sequencing | **Deleted** |
| `W21` | PCB-02 ↔ PCB-03 permit | **Deleted** |
| `W23a` | PCB-08 ↔ PCB-03: `SERVO_DATA`, C2 READY pair, `HEAD_OC`, `HEAD_PGOOD`, `MOTOR_PRESENT` | **Deleted.** `SERVO_DATA` stays on PCB-08 for the yaw plug |
| `W23b` | PCB-08 ↔ PCB-02: `V_PACK_ANA`, `STAT`, `INT_PB`, `KILL`, `CHG_ABSENT`, `ARM_REQ` | **Deleted** |
| `W39` | PCB-10 `J10-12` ↔ PCB-03 | **Deleted** |
| `W40` power button | Mushroom → PCB-02 `J2-9` | Mushroom → power-switch module button input |
| `W43` sideband FFC | Permit and status signals | Fewer conductors used; reassign at PCB-08/12 design |
| **New** I²C to the monitor | — | Monitor module → Pi or C3 (Level 10 Q2) |
| `W24`, `W25`, `W29`–`W37`, `W41`, `W42` | | **Unchanged** (`W29` now to the bought IMU) |

### Effects

- Body-lift plug count (H-08, §7.2) drops: `J2-1`, `J2-7` and `J3-1` go away and are replaced by the switched-bus leads. Recount at Level 6.
- Micro-Fit+ positions and their tooling shrink. Recheck the crimp-tool buy list (§9).
- GH lead buy list: GH10 ×1, GH8 ×2 and GH4 ×1 drop out.

---

## Level 5 — Firmware takes over

| Job | Was hardware on | Now |
|---|---|---|
| Low-battery stop and shutdown | `ENERGY_OK` comparator (PCB-02) | Read the monitor: stop motion at the RP-02 soft-critical 6.0 V, orderly shutdown before the TIFPS0629 under-voltage trip. Thresholds are re-registered from RP-02 §8.1 |
| Orderly shutdown on a button press | `LTC2954` `INT` → C2 | Depends on Level 10 Q1. With a plain toggle switch, a press cuts power at once, so the Pi needs a read-only or overlay root filesystem |
| Power-up order | `SEQ_EN` latch | None. Everything comes up together; check that the Pi and C2 tolerate it at Level 9 |
| Motor permission | Permit chain | C3 `nSLEEP` plus the existing watchdog/AND gate on PCB-10 |
| Head and yaw overload | `HEAD_OC` comparator | Feetech current/torque limit registers and present-load reads |
| Charging state | `STAT`, `CHG_ABSENT` | None. Charging happens in `OFF` |

---

## Level 6 — CAD ([final/v1/cad](final/v1/README.md))

All edits go in `makad-v1.step.py`, never in subsystem sources ([D-063](decisions.md#d-063) rules).

| Area | Change |
|---|---|
| PCB-02 location (behind the rear panel) | Remove the board and its D-083 mount; place the power-switch module, the monitor and the charge-path splice there |
| PCB-03 bay (above the tub) | Remove the placeholder; place the head and yaw buck-boost modules. They are larger than the custom layout's parts would have been. Re-check the −Y head riser and the motor cable reserves |
| PCB-04 bay (under the compute tray, 70 × 44 mm, Z 60–77) | Remove the placeholder; place 2–4 buck modules. Keep the D-072 underside keep-out over the motor cable reserves |
| PCB-07 | Swap the 16 × 20 mm placeholder for the chosen breakout's outline and holes |
| PCB-08 | Room for the moved yaw servo plug |
| PCB-12 | The simplified carrier, or the Waveshare board in the head pocket |
| Rear panel | Fill or reshape the PCB-13 USB4140 pocket and pad; add the charge port and balance port cut-outs |
| Pack channel | Route the balance lead and its break (the 8 mm channel limit, Level 4) |
| Mass | Update the hand-kept mass rows. Modules plus pigtails differ from the custom estimates; re-run the CoM and `a_tip` check (D-026 margin 1.763 against 1.582) |
| Checks | New targeted checks for each bay's fit and clearance. Retire `check_pcb13_*` and the PCB-02 mount checks |

---

## Level 7 — BOM ([BOM.csv](BOM.csv))

| Row | Change |
|---|---|
| CH-041 PCB-02, CH-042 PCB-03, CH-043 PCB-04, BO-015 PCB-13 | **Retired** (superseded by D-093) |
| CH-021 PCB-07 | Becomes the bought IMU breakout |
| BO-016 PD adapter and cable, BO-017 inlet screws | **Retired** |
| CH-025 pack NTC | Retired, or kept optional (Level 10 Q4) |
| CH-046 IDEC E-stop | Already dead since D-041; retire if still open |
| CH-086 PCB-12 | Updated scope (no watchdog), or the Waveshare board |
| CH-083 PCB-08 | Updated scope (adds the yaw servo plug) |
| CH-023, CH-024, CH-027–CH-029, BO-018 | Unchanged |
| **New** | Pushbutton power switch; head buck-boost; yaw buck-boost; Pi buck; 1–2 small bucks; INA226/219 monitor; 2S balance charger; charge port (XT30-class panel pair); balance port and break; 2 × SMBJ8.5A + 2 × 100 µF if not already listed |

---

## Level 8 — Documents to update

| Document | Change |
|---|---|
| [decisions.md](decisions.md) | D-093 (Level 0) |
| [04-pcbs/README.md](04-pcbs/README.md) | Register: rows 02, 03, 04, 07, 13 superseded; 08 and 12 rescoped |
| [04-pcbs/workflow.md](04-pcbs/workflow.md) | Tracker table; the design batch is PCB-08, 12, 14 |
| [04-pcbs/power-boards.md](04-pcbs/power-boards.md) | Banner: superseded by D-093 except §2.1–2.2 (DRV8833 and the `VM` TVS) and §3 (TIFPS0629 acceptance) |
| [04-pcbs/charge-path.md](04-pcbs/charge-path.md), [open-items.md](04-pcbs/open-items.md) | Charge path superseded; close CP-OI-01 to -15 as "superseded", don't delete |
| `pcb-02`, `pcb-03`, `pcb-04`, `pcb-07`, `pcb-13` folders | README banner "Superseded by D-093"; keep the files |
| `pcb-08`, `pcb-12` READMEs | New inputs (Levels 2 and 4) |
| [05-harness/README.md](05-harness/README.md) | Power tree, wire list, pinouts, service procedures, buy list (Level 4) |
| [final/v1/README.md](final/v1/README.md) | Custom PCBs group and the new bought-module group |

---

## Level 9 — Tests

### Retired

CP-01 to CP-14 (charge path), PB-01 to PB-06 (power button on the `LTC2954`), PCB-02/03/04 truth-table, fault, inrush, regeneration, start-up, hold-up, breaker and back-feed tests, the brownout-contract tests, and the STUSB4500 NVM image and jig (CP-OI-05).

### Kept

The TIFPS0629 acceptance (power-boards §3, two units), MOT3001 winding R and L on receipt, and the bench tests of every kept board (PCB-05/06 audio, PCB-10, PCB-11, PCB-15).

### New

| Test | Pass |
|---|---|
| Power switch | Turns on and off from the mushroom; carries 10 A without overheating; OFF current recorded |
| Each module | Output voltage at no load and full load, at 6.0 V and 8.4 V input; enable works if used |
| Yaw rail | Voltage at the servo terminals stays below 12.6 V through a stall and a fast stop |
| Drive `VM` | Bus peak stays below 11.8 V when both motors are released at the chopping limit |
| Charging in place | A full balance charge through the rear ports in `OFF`; cells end within the charger's balance band; nothing warm in the body |
| Low battery | Firmware stops motion and shuts down before the TIFPS0629 under-voltage trip |
| Power-up together | Pi, C2, C3 and display start cleanly with no sequencing, 20 cycles |
| IMU | SPI read at the C3 on `J10-7` |

---

## Level 10 — Open sub-decisions (for the builder)

| # | Question | Recommendation |
|---|---|---|
| Q1 | Button behaviour: toggle (a press cuts power at once) or press-to-on with firmware-driven off (button also read by a GPIO; firmware pulses the switch's OFF input after an orderly shutdown) | Press-to-on, firmware off. Keep the hard cut-off as unplugging `J-PK`, or a long hold if the chosen switch supports it |
| Q2 | Who reads the voltage/current monitor: the Pi or C3 | The Pi (it owns shutdown). C3 only if PCB-10 has a free I²C pair |
| Q3 | How many 5 V buck modules | Two: Pi alone; one shared for C3, audio, C2 and display. Four only if the harness split forces it |
| Q4 | Keep the pack NTC as a firmware temperature input | Drop it; the AC72ABD breaker stays |
| Q5 | PCB-12: simplified custom carrier or the Waveshare ESP32 Servo Driver (₹1,375 at Zbotic, plain ESP32, larger) | Fit-check the Waveshare board in the head first; design the custom one only if it doesn't fit |
| Q6 | PCB-05/06: keep rev A or swap to breakouts (MAX98357A + I2S mics, or a USB mic array) | Decide after checking how many I2S mic lanes the Pi 5 can capture; the WLCSP assembly is the main reason to swap |
| Q7 | Charge port: main + balance (XT30 + 3-pin), or balance-lead-only charging at under 1 A | Main + balance: faster, and every hobby charger supports it |
| Q8 | Yaw rail: fixed 12 V or adjustable set to 11.1 V | 11.1 V |

---

## Sources

- [Pololu S18V20F12](https://www.pololu.com/product/2577): 12 V ±4 %, 2.9–32 V input, 2 A typical
- [Pololu power switch distributors](https://www.pololu.com/product/2808/distributors)
- [Elecrow ICM-42688-P breakout](https://www.elecrow.com/icm-42688-p-ultra-low-power-imu-breakout.html)
- [Zbotic – Waveshare ESP32 Servo Driver Expansion Board](https://zbotic.in/product/waveshare-esp32-servo-driver-expansion-board-built-in-wi-fi-and-bluetooth/)
- [Robu 2S Type-C charger module](https://robu.in/product/2s-8-4v-2a-18650-lithium-battery-charger-module-type-c) (not used: no NTC or JEITA)
