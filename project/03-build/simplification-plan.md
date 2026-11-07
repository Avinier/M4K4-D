# Simplification plan: minimal safety, off-board charging, bought modules

| Field | Value |
|---|---|
| Status | **PLAN, 2026-11-06.** Builder decisions D1–D6 and sub-decisions Q1–Q9 taken (§6); this page reviews them and maps every change they cause. The changes are applied level by level; §7 tracks which levels are done |
| Ledger entry | **[D-093](decisions.md#d-093)**, written 2026-11-06 (Level 0 done; the PCB-09 branch is merged to `main`) |
| Print state | Nothing is printed: [04-print](../04-print/README.md) phase 0 (access) is still open. Every CAD change below lands before any part is printed |

---

## 1. The decisions (builder, 2026-11-06)

| # | Decision | Review |
|---|---|---|
| D1 | **Minimal, scrappy safety** for the v1 desk robot. No permit chains, latching e-fuses, hold-up, sequencing or arm latch. Replaces RP-02 `BD-01` ("custom PCBs; breakout modules bench-only") | **Sound.** [constraints.md](../00-foundation/constraints.md) already says safety must be "proportional to Makad's plausible hazards, not … a generic product-certification exercise". The real hazards (cell fire, shorts, a runaway base) stay covered: see §3 |
| D2 | **Charge the pack outside the robot** with a bought balance charger | **Sound.** It closes foundation item CON-TBD-09 ("charging method and whether operation while charging is allowed"): an off-board balance charger, with no operation while charging. CON-10 (battery-powered, untethered, ≥ 20 min) is unaffected. The only physical risk is fitting the balance lead in the pack channel (§5 R3) |
| D3 | **PCB-03, PCB-04 and PCB-07 are bought** | **Sound.** They are the hardest power board, the second-largest and a HOLD board. Watch: the bays' volume, the yaw rail's margin and USB back-feed from the C3 (§5) |
| D4 | **PCB-02 is bought**: the simplified charging leaves only the on/off latch and pack sense | **Sound.** It is not one module but three jobs: on/off → pushbutton power switch module; pack sense → monitor module; charger → gone (D2). It discards the most work (D-082 to D-091 and the routing), but also the riskiest bring-up |
| D5 | **PCB-05 bought; PCB-06 bought too** | **Sound. Q6 chose 4 I²S mics on two lanes, which keeps the spatial-hearing candidate.** It removes the WLCSP assembly with X-ray. PCB-09 needs no re-spin: its `J9-3` already carries the I²S signals a bought amp and I²S mics need. You lose PCB-05's job as the audio wiring hub, which becomes a small perfboard hub or splices. Its SDI0/SDI1 lanes carry the four mics as two stereo pairs, as PCB-05 did. Spatial hearing (`CAND-01`, [v1-scope.md](../00-foundation/v1-scope.md)) stays possible |
| D6 | **PCB-13 is gone** | Follows from D2 |

---

## 2. Board outcome

| Board | Before | After | Work left |
|---|---|---|---|
| PCB-01 | Bought TIFPS0629 | **Unchanged.** Now the main safety device | §3 bench acceptance (power-boards §3) |
| PCB-02 charger, latch, sense | Routed | **Bought modules** (switch + monitor) | — |
| PCB-03 motor gate, head/yaw rails | Not started | **Bought modules** (two buck-boosts) | — |
| PCB-04 branch converters | Not started | **Bought modules**: 2 × S13V30F5 5 V buck-boost (D-094) | — |
| PCB-05 audio front end | Rev A | **Bought** MAX98357A breakout (BO-007 promoted) | — |
| PCB-06 ×4 mics | Rev A | **Bought**: 4 I²S mic breakouts on two lanes (Q6) | — |
| PCB-07 base IMU | HOLD | **Bought** SPI 6-axis breakout | — |
| PCB-13 charge inlet | Rev A | **Deleted** | — |
| PCB-08 yaw junction | Not started | **Custom, simpler**: drops the permit/status sideband, **gains the yaw servo plug** (was PCB-03 `J3-5`) | Design |
| PCB-09 C0 link adapter | Rev A (branch) | **Kept, no change**; merge the branch | Procure |
| PCB-10 C3 carrier | Rev A | **Kept, no re-spin.** `J10-12` unused; its watchdog + AND gate become the motor kill | Procure |
| PCB-11 status LED | Rev A | **Kept** | Procure |
| PCB-12 C2 head carrier | Not started | **Custom, simpler** (no watchdog, `ARM_REQ` or READY pair). The Waveshare board doesn't fit the C2 bay (D-094) | Design |
| PCB-14 ×3 yaw joiners | HOLD | **Kept custom** (passive; ZIF pick still open) | Design |
| PCB-15 nose Hall | Rev A | **Kept** | Procure |

**Count:** 14 custom designs → **7** (PCB-08, 09, 10, 11, 12, 14, 15), or 6 if Q5 picks the Waveshare board. 4 are already designed; **3 are left to design** (08, 12, 14). All 7 go on one fab order ([D-064](decisions.md#d-064) batch). What's left to bring up is medium risk (PCB-09, 10, 12) or low (08, 11, 14, 15).

**Interface rule.** Boards already designed keep their connectors. Each bought module gets a soldered pigtail ending in the connector the board expects. No designed board is re-spun.

---

## 3. System architecture after the change

### Power tree

```
 CHASSIS                                     BODY
 cells ─ PCB-01 (TIFPS0629) ─W01─ J-PK ─ FUSE 15 A ─ splice ─┬─ CHARGE PORT (rear panel, unswitched)
   │                                                         └─ PUSHBUTTON POWER SWITCH ─ INA226 shunt ─ switched bus
   └─ balance lead (B−, mid, B+) ─ break ─────────────────────── BALANCE PORT (rear panel)

 switched bus ─┬─ #3297 L / R drive (VM: SMBJ8.5A + 100 µF + 0.1 µF each)
               ├─ buck-boost → 5.5 V head pitch/roll (W13 → J8-1)
               ├─ buck-boost → 11.1 V yaw (→ PCB-08 → W15)
               ├─ buck-boost 5 V 3 A → Pi 5 (W10 USB-C; a non-PD Pi 5 assumes 3 A)
               └─ buck-boost 5 V → C3 (W11, via a diode), amp (W12), C2 + display (W14 → J8-1)
```

### Modes

`OFF` and `ON` only. Charging happens only in `OFF`. That is an operating rule, not enforced in hardware.

### Safety kept

| Hazard | Cover |
|---|---|
| Cell over-charge, over-discharge, over-current, short circuit, imbalance | TIFPS0629 ([D-019](decisions.md#d-019)), plus the external charger's own balance and limits |
| Wiring fault | 15 A ATOF fuse (CH-029) |
| Cell over-temperature | Bourns AC72ABD in the cell strap (CH-024) |
| Power off | The mushroom (BO-018) on the power switch cuts the whole switched bus; `J-PK` is the isolator for service |
| Runaway base when C3 hangs | **Already on PCB-10**: TPS3436 watchdog → `C3_READY` → U4 74LVC1G08 holds both DRV8833 `nSLEEP` low. U4 is fed locally on PCB-10, so it works without PCB-03 |
| DRV8833 over-voltage on regeneration | SMBJ8.5A + bulk at each `VM` (power-boards §2.2) |
| Driver over-current | DRV8833 chopping and trip |
| Servo overload | Feetech's own protection, plus firmware torque/current limits |
| Deep discharge before the pack trips | Firmware, reading the monitor |

### Safety dropped

The motor gate and surge stopper, the permit chain and arm latch (`SYSTEM_ARM`, `PERMIT_OK`, `ARM_REQ`), `ENERGY_OK`, `CHARGE_ABSENT`, the e-fuses, hold-up and sequencing, the head/yaw current comparators, the C2 watchdog and the pack NTC.

---

## 4. Impact by project area

### 4.1 Foundation and system ledgers (`00-foundation`, `01-system`)

| Document | Change |
|---|---|
| [constraints.md](../00-foundation/constraints.md) | Close CON-TBD-09 and its checklist item: off-board balance charger; no operation while charging |
| [success-criteria.md](../00-foundation/success-criteria.md) | SC-TBD-10 (battery): low-battery behaviour is now firmware stop + shutdown; recharge expectation is an off-board charge |
| [power-energy-ledger.md](../01-system/power-energy-ledger.md) | Retire `PB-CHARGE-IN` and `PB-CHARGE-LOGIC`. `PB-SAFE-C2` and the others lose their own-protection wording. Redo the OFF budget: TIFPS0629 + the power switch's OFF draw only. BQ25798, LTC2954 and LTC4368 are gone. Redo converter efficiencies with module figures and recheck the 20 min runtime |
| [mass-envelope-ledger.md](../01-system/mass-envelope-ledger.md) | Module masses replace custom-board estimates |
| [candidate-sourcing-matrix.md](../01-system/candidate-sourcing-matrix.md) | PCB-05/06/07 rows point to the bought parts |

These are system records, outside `03-build`. The [03-build rule](README.md) says `03-build` wins on disagreement, so updating them is housekeeping, not a blocker.

### 4.2 Decisions ledger ([decisions.md](decisions.md))

**New: D-093.** It covers D1–D6, the board outcome (§2) and the architecture (§3).

| Decision | Fate |
|---|---|
| RP-02 `BD-01`, `BD-05`, `BD-07`, `BD-09`, `BD-11`, `BD-13`; `brownout-restart-contract.md` | Superseded for the build |
| RP-02 `BD-10` (watchdog) | Kept on PCB-10, dropped from PCB-12 |
| [D-019](decisions.md#d-019) TIFPS0629 | Kept |
| [D-034](decisions.md#d-034) speaker | Kept (bought part) |
| [D-035](decisions.md#d-035) bench amp breakout (BO-007) | **Promoted**: the breakout is now the installed amplifier |
| [D-036](decisions.md#d-036) PDM mic IC, [D-037](decisions.md#d-037) mic mounting, [D-066](decisions.md#d-066) L/R straps and sound-hole ring, [D-067](decisions.md#d-067) PCB-05 | **Superseded.** Mic port positions in the shell stay as a starting point (§4.6) |
| [D-038](decisions.md#d-038) power-board deltas | Superseded except the DRV8833 facts and the `VM` TVS/bulk (§2.1–2.2) and the TIFPS0629 acceptance (§3) |
| [D-040](decisions.md#d-040) charge path, [D-069](decisions.md#d-069) PCB-13 | Superseded |
| [D-041](decisions.md#d-041) power button | **Amended**: the mushroom drives the power switch module; no `LTC2954` |
| [D-046](decisions.md#d-046)/[D-047](decisions.md#d-047) servo rails | Amended: bought modules; yaw at 11.1 V (Q8) |
| [D-064](decisions.md#d-064) design-then-procure | Kept; the batch is 7 boards |
| [D-073](decisions.md#d-073)/[D-074](decisions.md#d-074)/D-092 PCB-09 | Kept |
| [D-082](decisions.md#d-082) fresh-arm | Superseded |
| [D-083](decisions.md#d-083) to [D-091](decisions.md#d-091) PCB-02 | Superseded |
| [D-068](decisions.md#d-068) PCB-10 | Kept; amend the note that `J10-12` mates PCB-03 |

### 4.3 PCB work area ([04-pcbs](04-pcbs/README.md))

| Item | Change |
|---|---|
| [README](04-pcbs/README.md) board register | Rows 02, 03, 04, 05, 06, 07 and 13 → "Bought / superseded by D-093"; rows 08 and 12 rescoped |
| [workflow.md](04-pcbs/workflow.md) tracker | 7 rows remain; the design batch is PCB-08, 12, 14 |
| [power-boards.md](04-pcbs/power-boards.md) | Banner: superseded except §2.1–2.2 and §3 |
| [charge-path.md](04-pcbs/charge-path.md) | Banner: superseded |
| [open-items.md](04-pcbs/open-items.md) | CP-OI-01 to -15 closed as "superseded by D-093", not deleted |
| `pcb-02`, `03`, `04`, `05`, `06`, `07`, `13` folders | README banner "Superseded by D-093". **Keep the KiCad files**: they are reference for a v2 with in-robot charging or custom audio |
| `pcb-08` README | New inputs: yaw servo plug (`+11V1_YAW`, GND, `SERVO_DATA`); remove the `W23a`/`W23b` sideband and `ARM_REQ` |
| `pcb-12` README | Remove the TPS3436 watchdog and the D-082 `ARM_REQ` section |
| `pcb-10` README | Note `J10-12` unused and the new `W11` diode (§5 R4) |
| Branch `pcb-09-c0-link-adapter` | Merge to `main` |

### 4.4 Harness ([05-harness](05-harness/README.md))

**Power**

| Wire | After |
|---|---|
| `W01`, `W03a`, `W03a−`, `W03b` | Unchanged |
| `W02a`/`W02b` NTC + SM 2p break | **Deleted**. The balance lead takes its route |
| **New** balance lead | Cells → a break near `J-PK` → rear-panel balance port |
| `W03c` (→ PCB-03 `J3-1`) | Removed; the drive feeds now leave the switched bus |
| `W03d` (→ PCB-02 `J2-1`) | **Route reused**: splice → rear area → power switch input and charge port |
| **New** charge lead | Unswitched side → rear-panel charge port |
| `W05` `OPBUS`/`CHGBUS` | Replaced by the switched-bus distribution (splice or small bus bar) |
| `W06`/`W07` | From the switched bus to the #3297 `VM`, with the TVS and bulk kept |
| `W10`, `W11`, `W12`, `W13`, `W14` | From modules, same far-end connectors. `W11` gets a series Schottky (R4) |
| `W15` yaw servo | From PCB-08, not PCB-03 |
| `W16` charge inlet | Deleted |

**Signals**

| Wire | After |
|---|---|
| `W20`, `W21`, `W23b`, `W39` | **Deleted** |
| `W23a` | **Deleted**; `SERVO_DATA` for yaw now stays on PCB-08 |
| `W40` power button | To the power switch's button input |
| `W43` sideband FFC | Fewer conductors; reassign at PCB-08/12 design |
| `W26` audio (`J9-3` GH10) | **Changed**: `J9-3` → a small audio hub (perfboard or splices) → amp breakout and the four mic breakouts. BCLK, LRCLK, 3V3 and GND go to every mic, with a 33–100 Ω series resistor per clock branch at the hub (as PCB-05 had); SDI0 from the front pair, SDI1 from the rear pair; SDO0 and `AMP_SD` go to the amp |
| `W27` mic leads | **Changed**: 6 wires per I²S mic (VDD, GND, SCK, WS, SD, L/R strap) instead of the PDM GH4 |
| `W28` speaker | To the breakout's screw terminal |
| **New** I²C to the monitor | Monitor → the Pi (Q2) |
| `W24`, `W25`, `W29`–`W37`, `W41`, `W42` | Unchanged (`W29` to the bought IMU) |

**Also**

- The body-lift plug count (H-08, §7.2) is **11 after pack removal** in the [D-096 harness](05-harness/README.md#72-body-off-chassis-rear-panel-off): four power and seven signal breaks. It does not drop as initially expected because both S18 outputs cross the joint.
- The Micro-Fit+ positions shrink: recheck the crimp-tool buy (§9).
- The GH buy list loses GH10 ×1, GH8 ×2, GH4 ×1 and the GH2 NTC lead.

### 4.5 Chassis (`01-chassis`, [04-print/01-chassis](../04-print/01-chassis/README.md))

| Item | Change |
|---|---|
| Pack build (CH-022, CH-025, CH-026) | Add a 3-wire balance lead off the cell straps; drop the 103AT NTC |
| Pack channel (H-07, X 52–76) | The balance break must fit the ≈ 8 mm channel (R3). **D-095:** the channel is 13.5 mm wide at the break (8 mm was the NTC reserve); a JST PA 3P wire-to-wire pair sits there with the body-side loop beside it |
| IMU mount J15A ([joint-register](01-chassis/v1/joint-register.md#j15a--imu-board-to-deck)) | The 16 × 20 mm PCB-07 and its two M2 holes become a bought breakout (≈ 25 × 18 mm class). **Option A:** a small printed adapter on the existing J15A holes, so no frame change. **Option B:** move the holes before the frame is printed (phase 1) |
| Driver boards (J15B) | Unchanged; the TVS and 100 µF are soldered at `VM` |
| Chassis model copies (`body_chassis_model.py`, `check_layout.py`) | Already stale (CP-OI-13); leave them, `final/v1` governs |

### 4.6 Body (`02-body`, CAD edits in `final/v1/cad`)

| Area | Change |
|---|---|
| PCB-02 place (behind the rear panel) | Remove the board and the D-083 frame mount; place the power switch, monitor and charge splice |
| PCB-03 bay (above the tub) | Remove the placeholder; place two buck-boost modules. Re-check the −Y head riser and `HARNESS_*` reserves |
| PCB-04 bay (under the compute tray, 70 × 44, Z 60–77) | Remove the placeholder; place 2–4 bucks. Keep the D-072 underside keep-out over the motor cable reserves |
| PCB-05 place (above the Pi, three M2 SMT spacers on frame bosses, D-067) | Swap to the amp breakout. Reuse one or two of the D-067 frame bosses with a printed adapter, or move the amp near the speaker |
| Mic bosses (D-037, BO-013/014) and sound-hole rings (D-066) on the shell | Keep all four D-037 port positions (Q6); redesign the bosses for the I²S breakout's outline and port |
| Rear panel | Remove the PCB-13 pad and USB4140 pocket (`PCB13_RELIEF`); add the charge port and balance port cut-outs. The mushroom well (D-041) is unchanged |
| Enclosure fan vs mic ports (D-043) | Re-check once the mic positions are final |
| Mass | New mass rows and a re-run of the CoM / `a_tip` check (D-026 margin 1.763 against 1.582) |

### 4.7 Head (`03-head`)

| Item | Change |
|---|---|
| [Head BOM](03-head/v1/BOM.md) yaw rail note (BO-043) | "Second LTC3119 on PCB-03" → bought buck-boost at 11.1 V; servo current limit below the module's 2 A |
| PCB-12 | Simplified scope, or the Waveshare board in the C2 tray (Q5) |
| `J8-1` head trunk | Unchanged pinout; the supplies now come from modules |
| [feetech-migration-status.md](feetech-migration-status.md) | Update the rail lines |

### 4.8 Final CAD ([final/v1/cad](final/v1/README.md))

| File | Change |
|---|---|
| `makad-v1.step.py` | Remove `PCB02_MOUNT` and its edge rails/standoffs, `PCB05_MOUNT` bosses/spacers/cuts, `PCB13_RELIEF` and the `J5-7` relocation entries. Change the "Custom PCBs" group (lines for PCB-02/03/04/05/06/07/13) into a new "Bought modules" group with each module's STEP or box |
| `pcb_integration.py`, `check_pcb_integration.py` | Drop the 05/06/13 boards |
| Retire | `check_pcb02_back_face.py`, `check_pcb02_j9_courtyard.py`, `check_pcb02_mount.py`, `check_pcb05_fit.py`, `check_pcb05_mount.py`, `check_pcb06_fit.py`, `check_pcb13_fit.py`, `check_pcb13_relief.py`; body `check_charge_inlet.py` |
| Replace | `check_mic_mounts.py` → the new breakout bosses |
| New targeted checks | Module bay fit (PCB-03/04 bays), rear-panel ports, balance-lead channel, amp and mic mounts, IMU adapter |
| Keep | `check_power_button.py` and every PCB-09/10/11/15 check |

### 4.9 Print ([04-print](../04-print/README.md))

| Item | Change |
|---|---|
| [Frame README](../04-print/01-chassis/frame/README.md) J15A row | IMU breakout adapter or new holes (§4.5) |
| Frame README line on the body frame and PCB-02 | The PCB-02 edge frame is gone |
| [04-print README](../04-print/README.md) `DROID_ADDS` PCB-05 example | Update when the bosses change |
| Phase 3 (skins) | The shell mic bosses and rear panel change before printing; no reprint cost |

### 4.10 BOM ([BOM.csv](BOM.csv))

| Rows | Change |
|---|---|
| CH-041, CH-042, CH-043, BO-002, BO-005, BO-012, BO-015, BO-016, BO-017, CH-025 | **Retired** (D-093) |
| BO-003 MAX98357A IC, BO-004 ADAU7002, BO-013/014 mic mounting | Retired or replaced by the breakout rows |
| BO-007 MAX98357A breakout | **Promoted** from bench to installed |
| CH-021 | Bought SPI IMU breakout |
| CH-046 IDEC E-stop | Retire if still open (dead since D-041) |
| CH-083, CH-086 | Rescoped (§4.3) |
| **New** | Pushbutton power switch; 2 buck-boosts; Pi buck; 1 shared 5 V buck; INA226/219; 2S balance charger; charge port (XT30-class panel pair); balance port and break; 4 I²S mic breakouts with an L/R select pin (INMP441 class); audio hub perfboard; Schottky for `W11`; 2 × SMBJ8.5A + 2 × 100 µF if not already listed |
| Unchanged | CH-017, CH-023, CH-024, CH-027–CH-029, BO-001, BO-018, CH-044, CH-045, CH-064, CH-084, CH-085, BO-062 |

### 4.11 Firmware and software

`04-software` is empty, so these become its first requirements.

| Job | Was | Now |
|---|---|---|
| Low battery | `ENERGY_OK` comparator | The Pi reads the monitor: stop motion at 6.0 V (RP-02 soft-critical), shut down before the TIFPS0629 under-voltage trip |
| Power-off | `LTC2954` `INT` → orderly shutdown | Q1. With a plain toggle, use a read-only or overlay root filesystem on the Pi |
| Power-up | `SEQ_EN` latch | None; everything starts together (test N7) |
| Motor permission | Permit chain | C3 `nSLEEP` + the PCB-10 watchdog/AND gate (already designed) |
| Servo overload | `HEAD_OC` comparator | Feetech limit registers and load reads |
| Audio | Custom 5-pin I²S0 overlay with two capture lanes (PCB-09 notes) | **Still needed (Q6: 4 mics).** Define a five-pin I²S0 group on GPIO 18–22, keep GPIO 23/24 out of it, and bind one clock with four capture channels on SDI0/SDI1 plus SDO0 playback (PCB-09 README, audio overlay row). This is the main software risk of the audio path |

### 4.12 Tests

| Retired | Kept |
|---|---|
| CP-01 to CP-14, PB-01 to PB-06, CP-OI-05 NVM jig, the PCB-02/03/04 truth-table, fault, inrush, regeneration, start-up, hold-up, breaker and back-feed tests, brownout-contract tests, PCB-05 two-lane PDM bench, PCB-06 array tap and boss coupon | TIFPS0629 acceptance (two units), MOT3001 R/L on receipt, PCB-09/10/11/15 bench, the speaker/cavity listen |

**New tests.** This table is the bench register: the pass criteria below are what gets followed. Other pages ([module-selection.md](module-selection.md) §3) cite test IDs, not their own versions.

| # | Test | Setup | Pass |
|---|---|---|---|
| N1 | Power switch (M1) | Switch installed in its CAD position inside the closed body, shell on; bench supply or pack at 7.4 V **and the 6.0 V low-pack corner**; thermocouple on the switch board and current/voltage scope | (a) On from the mushroom, off from the OFF input (firmware pulse). (b) 10 A for 10 s. (c) A realistic duty cycle for 30 min: drive, head and Pi loads as in a demo, with peaks logged. (d) OFF current recorded. (e) Screen repeated **13 A and 16 A, ≤2 s pulses** at the measured duty interval; record switch voltage drop and temperature, including after the 30 min warm-up. This is a candidate peak test, not an approved current budget. **Board temperature stays below 70 °C** in all fitted-body cases |
| N2 | Module capacity (M2, M4, M5) | Each module at 6.0 V and 8.4 V in, inside the body, on its real lead | (a) Output at no load and at its design load. (b) **M2 head rail:** both head servos stalled at once with the Feetech protection current set; record each servo's set limit; the rail stays ≥ 5.23 V at the servo terminals and the module doesn't thermal-limit for the time the servos take to trip. (c) **M5 shared 5 V:** simultaneous power-up of C3, amp, C2 and display, then full-volume audio with the display on; stays ≥ 4.75 V at each load |
| N3 | Yaw rail (M3) | Pack at 6.0 V and at 8.4 V; servo current limit set below the module's measured capability | (a) Sustained yaw load (continuous back-and-forth sweeps for 10 min): rail holds 11.1 V ±4 % and the module doesn't thermal-limit. (b) Stall and a hard stop at full speed: **< 12.6 V at the servo terminals** at every instant (scope) |
| N4 | Drive `VM` | Both #3297 boards on the switched bus, real motors, SMBJ8.5A + 100 µF + 0.1 µF at each `VM` | Both motors released at the chopping limit (permit loss and `nSLEEP` low): **`VM` peak < 11.8 V** on a scope |
| N5 | Charge in place | Robot `OFF`; charger on rear ports; use a current-limited cell simulator for balance fault injection | Full balance charge completes; cells end within charger balance band; nothing in body gets warm. On the simulator, verify reversed/mis-seated plug prevention, each open balance tap, main-lead disconnect, adjacent balance-pin short and proposed cell-end fuse operation; no uncontrolled charger output or unprotected AWG24 fault |
| N6 | Low battery | Pack drawn down under a demo load, with pack/cell and **post-switch module-input** voltage logged | Firmware stops motion at its defined **loaded-voltage** threshold and shuts down before TIFPS0629 under-voltage trip. Inject the measured peak demand near the threshold; no protection-board trip, Pi blackout or unintended restart. Define the 6.0 V observation point before using it as a test condition |
| N7 | Start together | Robot on from `OFF`, 20 cycles | Pi, C2, C3 and display start cleanly every time |
| N8 | C3 supply and back-feed (M13 Schottky) | Schottky in `W11` | (a) **Loaded:** C3 running with its peripherals, robot `ON` at 6.0 V pack: DevKitC 5 V pin ≥ 4.5 V and its 3.3 V rail in tolerance. (b) **Back-feed:** service USB on the DevKitC with the robot `OFF`: the switched bus and the M5 output stay at 0 V |
| N9 | Audio | Amp, four mics, audio hub with 100 kΩ SD pull-downs | Speaker plays while all four mics capture on I²S0, each mic in its own channel (tap each mic) |
| N10 | IMU | Adafruit LSM6DSOX on `J10-7` | SPI WHO_AM_I and data read at C3 |
| N11 | Mic array timing | Four mics in their shell bosses | A clap from known directions gives consistent inter-mic delays across the four channels |
| N12 | Pi supply voltage (M4) | Scope or logging meter **at the Pi's USB-C input**; pack at 6.0 V and 8.4 V | (a) M4 output at no load ≥ 4.90 V at the module, else reject that unit; a shorter `W10` cannot fix a low module. (b) **≥ 4.80 V at the Pi** through boot and through a CPU stress run with the camera and fan on, with no dip below 4.80 V. (c) `vcgencmd get_throttled` shows no under-voltage, now or since boot. **The 5.1 V recommendation:** Raspberry Pi recommends a 5.1 V supply to cover cable drop; M4 is a 5.0 V part, and the Pi flags under-voltage at 4.63 V ±5 % (up to about 4.86 V). M4 is accepted only if N12 passes; if it fails, choose a ≥ 3 A regulator settable to 5.1–5.2 V, by decision |

### 4.13 Memory and housekeeping

Update the memories for the PCB workflow tracker, the power distribution design, the power-board deltas and the Print guide, and add one for D-093.

---

## 5. Risks the decisions introduce

| # | Risk | Mitigation |
|---|---|---|
| R1 | **Power switch current.** The HP (#2813, D-094) is rated "16 A continuous at 12 V without exceeding 150 °C"; the MP is 6 A continuous. Peak pack current is about 10.2 A, the average far lower | HP chosen; **open as a thermal check**: test N1 in the closed body |
| R2 | **Yaw rail margin.** A fixed 12 V ±4 % module reaches 12.48 V against the ST3215-HS 12.6 V maximum | Adjustable buck-boost set to 11.1 V (Q8); servo current limit below 2 A |
| R3 | **Balance lead in the pack channel.** H-07: the channel holds nothing wider than about 8 mm; a JST-XH 3P housing is about 10 mm | Narrower break (2.0 mm pitch or soldered pigtails) or a re-route; CAD check before the frame print. **Closed in CAD (D-095):** JST PA 2.0 mm wire-to-wire break, `check_balance_channel.py` |
| R4 | **C3 USB back-feed.** PCB-10's DevKitC feeds `VCC_5V` from USB through its diodes, then out `J10-1` into `W11` (PCB-10 README). A bought buck's output may conduct back to its input and wake the switched bus | Series Schottky in `W11`; test N8 |
| R5 | **Hard power-off on the Pi.** Without the `LTC2954` interrupt, a press may cut the Pi mid-write | Q1, plus an overlay root filesystem |
| R6 | **More volume and wire.** Modules are larger than custom parts, and the hub boards (PCB-04, PCB-05) become splices | Bay fit checks in CAD before ordering; one splice point per rail |
| R7 | **India stock for Pololu.** The distributors listed are Fab.to.Lab and MG Super Labs; stock is patchy and TME is an import (D-066) | Check stock before freezing the CAD; for each module, name a second-source part with the same footprint class |
| R8 | **Custom I²S overlay** for four capture channels on two lanes (Q6) is not written yet. The kernel path exists: Raspberry Pi's I2S white paper (RP-009699) shows RP1 multi-lane I²S through `rpi-simple-soundcard`, used by the HiFiBerry DAC8x and ADC8x (8-channel capture, Pi 5 only). Their overlay muxes GPIO 18–27, which would take `AMP_SD` (23) and `FAN_EN` (24), so Makad needs its own GPIO 18–22 pin group and a 4-in/2-out channel setup | Adapt the DAC8x/ADC8x overlay (about a day). Prove it on the bench with loose breakouts before the shell bosses are printed. Fallback: the front pair on SDI0 alone, with a stock 2-channel path |
| R9 | **I²S clock fan-out** to five loads over ~200 mm leads | Series resistor per clock branch at the hub; short, twisted clock/ground pairs; test N9 |

---

## 6. Sub-decisions (builder, 2026-11-06)

| # | Question | Decision |
|---|---|---|
| Q1 | Power button | **Press-to-on; firmware off.** The button is also read by a GPIO; firmware shuts the Pi down, then drives the switch's OFF input. `J-PK` stays the hard isolator |
| Q2 | Who reads the monitor | **The Pi** |
| Q3 | Number of 5 V bucks | **Two:** the Pi alone; one shared by C3, amp, C2 and display |
| Q4 | Pack NTC | **Dropped**; the AC72ABD breaker stays |
| Q5 | PCB-12 | **Fit-check the Waveshare ESP32 Servo Driver first**; design the simpler custom carrier only if it doesn't fit. **Result (D-094): doesn't fit (65 × 30 mm against an 18 × 23.5 mm bay); custom carrier** |
| Q6 | Microphones | **4 I²S mics on two lanes** (SDI0 front pair, SDI1 rear pair). Keeps `CAND-01` spatial hearing; needs the custom overlay (R8) and an audio hub (R9) |
| Q7 | Charge connection | **Rear-panel charge port + balance port** (XT30-class + 3-pin) |
| Q8 | Yaw rail | **Adjustable buck-boost at 11.1 V** |
| Q9 | IMU mount | **Printed adapter on the existing J15A holes**; no frame change |

## 7. Levels of work

The changes are applied in these levels. Q1–Q9 are decided (§6).

| Level | What | Kind | Depends on | Status |
|---|---|---|---|---|
| 0 | **Decisions:** [D-093](decisions.md#d-093) in the ledger; PCB-09 branch merged to `main` | Record | — | **Done 2026-11-06** |
| 1 | **Architecture docs:** superseded banners on [power-boards.md](04-pcbs/power-boards.md) and [charge-path.md](04-pcbs/charge-path.md); CP-OI-01 to -15 closed as superseded in [open-items.md](04-pcbs/open-items.md) | Doc cleanup | — | **Done 2026-11-06** |
| 2 | **Board docs:** [04-pcbs](04-pcbs/README.md) register and [workflow](04-pcbs/workflow.md) tracker; superseded banners on PCB-02, 03, 04, 05, 06, 07, 13; new inputs in the PCB-08, 10, 12 READMEs (§4.3) | Doc cleanup | — | **Done 2026-11-06** |
| 3 | **Modules:** pick each part, check India stock, get dimensions and STEPs (§2, risks R1, R2, R7) | New design | — | **Done 2026-11-07**: [D-094](decisions.md#d-094), [module-selection.md](module-selection.md) |
| 4 | **CAD** in `final/v1/cad`: module bays, rear-panel ports, balance-lead channel, mic and amp mounts, IMU adapter; targeted checks; mass/CoM (§4.5–4.8) | New design | 3 | **Done 2026-11-07**: [D-095](decisions.md#d-095); outlines of M6, M8, M9 unmeasured |
| 5 | **Harness:** rewrite [05-harness](05-harness/README.md) power tree, wire list, pinouts, service procedures and buy list (§4.4) | New design | 3, 4 | **Topology documented; electrical HOLD 2026-11-07**: [D-096](decisions.md#d-096). ~16 A coincident low-pack demand exceeds the assumed 13 A connector rating and R010 shunt minimum; cut lengths, PNs and break/star CAD fit also open |
| 6 | **BOM:** retire, promote and add rows (§4.10) | Records | 3 | Waits |
| 7 | **Other docs:** foundation CON-TBD-09, the power/energy and mass ledgers, head BOM yaw-rail note, print READMEs, final v1 README (§4.1, 4.7, 4.9) | Doc cleanup | 3–6 | Waits |
| 8 | **Firmware requirements** in `04-software`: low-battery stop, button-off, servo limits, the four-mic overlay (§4.11) | Software | — | Can start any time |
| 9 | **Custom boards:** design PCB-08, PCB-12 (after the Waveshare fit check) and PCB-14; one fab order for all seven | New design | 4, 5 | Waits |
| 10 | **Bench:** TIFPS0629 acceptance, the four-mic overlay on loose breakouts (before the shell is printed), tests N1–N11 (§4.12) | Physical | Parts in hand | Waits |

---

## 8. Background: how we got here

### Board count before this plan (2026-11-06)

| State | Boards |
|---|---|
| Designed, rev A | PCB-05, 06, 09 (branch), 10, 11, 13, 15 |
| In progress | PCB-02: routed, ERC/DRC clean, 10 A path sized; populated-STEP fit and outputs open |
| Not started | PCB-03, 04, 07, 08, 12, 14 |

### Why there were so many boards

RP-02 `BD-01` chose custom PCBs because its spec asks for behaviour no module gives: a hardware permit chain with an LTC4368 surge stopper, latching e-fuses with hold-up and sequencing, a hostless JEITA charger, watchdogs on both carriers, a fresh-arm latch and an `ENERGY_OK` comparator. That is close to industrial safety, for a ~1 kg desk robot with 1.8 A-stall gearmotors, small servos, a fused 2S1P pack and a bought pack protection board.

### Risk sits in complexity, not count

| Risk | Boards (before) |
|---|---|
| Very high | PCB-02, PCB-03 |
| High | PCB-04, PCB-05 (WLCSP + X-ray) |
| Medium | PCB-09, 10, 12, 13 (PD NVM jig) |
| Low | PCB-06, 08, 11, 14, 15 |

After D1–D6, every very-high and high board is bought, and so is PCB-13.

---

## Sources

- [Pololu S18V20F12](https://www.pololu.com/product/2577): 12 V ±4 %, 2.9–32 V input, 2 A typical
- [Pololu Big Pushbutton Power Switch, MP](https://www.pololu.com/product/2812): 4.5–40 V, about 8 A continuous
- [Pololu power switch distributors](https://www.pololu.com/product/2808/distributors)
- [Elecrow ICM-42688-P breakout](https://www.elecrow.com/icm-42688-p-ultra-low-power-imu-breakout.html)
- [Zbotic – Waveshare ESP32 Servo Driver Expansion Board](https://zbotic.in/product/waveshare-esp32-servo-driver-expansion-board-built-in-wi-fi-and-bluetooth/)
- [Robu 2S Type-C charger module](https://robu.in/product/2s-8-4v-2a-18650-lithium-battery-charger-module-type-c) (not used: no NTC or JEITA)
