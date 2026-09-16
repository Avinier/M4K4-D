# RP-02 Decision

| Field | Value |
|---|---|
| Status | **Open — no gate outcome and no ADR closed. Raspberry Pi 5 2 GB is selected as `LG-01`; purchase and measured evidence remain open.** Part 1 is registered under `RP02-P1-REG-01`, topology under `RP02-P2-REG-01`, and implementation basis/SBC selection under `RP02-P2-REG-02` |
| Created | 2026-09-08 |
| Revised | 2026-09-16 |
| Design question | What compute/controller split, internal link, rail and protection topology, and energy source lets Makad run representative head, drive, display, camera, audio and compute loads concurrently — and with what measured margin? |
| Gate question | Does that design sustain every registered state and the registered mixed-duty cycle for at least 20 minutes without unsafe motion, unintended reset, rail excursion, data staleness or thermal violation — and does every injected fault produce a bounded state? |
| Feeds | ADR-03, ADR-06, ADR-12; power/energy, thermal, internal-communication and compute-coexistence budget rows; `subsystem-interfaces.md` |
| Rule | A negative runtime or coexistence result is an `iterate` on the design or a `reject` of a candidate — never a threshold change. CON-10's 20 minutes cannot be weakened; `Defer` is unavailable for Core outcomes. Failed runs stay cited here |
| Remaining-open index | Folder-wide list lives in [`../openitems.md`](../openitems.md), including final wire/fuse/converter/pack ratings. This file remains the RP-02 decision record. |

## Inherited locked decisions

Nothing in RP-02 reopens these; RP-02 measures them.

| Decision | Locked input | Source |
|---|---|---|
| CTRL-01…CTRL-06 | ESP32-S3 motion firmware; C2 separate from the display board; C2 = Waveshare ESP32-S3-Zero; bench twin DevKitC-1-N8R8; no runtime head IMU | `../RP-01-head/decision.md` |
| Display | SKU 30493 renders locally; receives semantic face state | display study; MEM-20260902-01 |
| Camera | Camera Module 3 Wide SC0874, CSI to the SBC | camera study |
| Placement | SBC, mics, speaker, battery in the body; battery low and forward of the axle | dimensional baseline v1.10 |
| E-stop | Motor bus, not logic | `workbench.md` |

## Inherited RP-01 paper state — not locked

These are current inputs. They are not SKU freezes, purchases, or `W` mass.

| Input | Current value | Source |
|---|---|---|
| Layout 03 paper demand | Nominal D/E tree ~362/436/509 g at M008=20 g; controlling peaks 0.0953 / 0.0560 / 0.1099 N·m pitch/roll/yaw. Complete-head `W` still waits on M008 | `../RP-01-head/fullproofmath.md`; physics.md |
| C01 paper candidate | XC330-M288-T, proposed 5 V, paper approval OPEN; **not a family freeze**. Layout 03 already uses matching 23 g housings | `../RP-01-head/actuator-screen-01.md` |

## RP-02 Part-1 builder decisions — 2026-09-15

| ID | Decision | Architectural consequence |
|---|---|---|
| SD-01 | Camera off in quiet sleep | Wake/acquire timing includes camera startup; `CC-02F/T` use `LP-06-OFF` |
| SD-02 | Head-servo torque off in sleep; head rests down | RP-01 must prove a safe passive rest; idle load cannot include guessed hold current |
| SD-03 | Floor/table mode manually selected in the control app for V1 | Selection is session-scoped and locally enforced; boot/reset/app-link loss returns to motion inhibit |
| SD-04 | Display on while charging | External AC-to-DC adapter plus chemistry-specific onboard charge/power path is required; only display/minimum supervision remain on; all motors, camera and normal interaction/audio stay off |

## RP-02 Part-2 architecture decision — 2026-09-16

`RP02-P2-REG-01` registers `PA-01…16` and the `PB-*` branch set in `power-architecture.md`. It fixes four failure-consequence domains, independent C2 and base-safety supplies, contained application branches, restricted charge-mode power, a common-reference star return, true `OFF/OPERATE/CHARGE` control, and battery-only motor energy behind both the system motor-arm gate and dominant hardware E-stop. It does not select a battery, charger, converter, protection device, connector, conductor, or numeric rating.

`RP02-P2-REG-02` registers the voltage-domain, grounding, connector, conductor-calculation, terminal-drop, protection-coordination, branch-local-capacitance and circuit-sequencing basis in `power-implementation-basis.md`. It also selects Raspberry Pi 5 2 GB as `LG-01` with a dedicated 5.1 V nominal, 5 A-capable `PB-COMPUTE` interface. Selection is not purchase authorization and does not convert load estimates into measured evidence.

`power-calculation-ledger.md` v0.1 derives the presently possible voltage-drop, conductor/contact heat, converter-loss, source-current, `MD-01` energy and fuse-coordination results. `power-component-candidate-screen.md` v0.1 applies those contracts to manufacturer-sourced `PCD-*` candidates and records leads, holds and rejections. `brownout-restart-contract.md` v1.0 is registered as `RP02-P2-REG-03` and freezes the `BR-*` slow/fast energy-loss paths, threshold ownership, reset-safe defaults, fresh-intent recovery and sizing/verification method. Installed path lengths, converter maps, protection curves, pack impedance, timing and `W` load profiles still control final ratings and numeric thresholds; registration does not convert those open inputs into selections or evidence.

## Gate outcomes

| Gate | Outcome | Evidence (run IDs) | Notes |
|---|---|---|---|
| RP02-G01 Protection | | | Verification; per rig revision |
| RP02-G02 Peak coexistence | | | Record registered `CC` cases/profile revisions verified, pending cases, `CC-PEAK-01`/`ST-01` coverage and re-run trigger |
| RP02-G03 Runtime | | | Recorded as a rehearsal with margin; SC-14 closes the requirement at integration |
| RP02-G04 Fault containment | | | Verification; zero unbounded outcomes across the campaign |
| RP02-G05 Control feasibility | | | Measurement with margin ratios |
| RP02-G06 Serviceability | | | Verification; timed procedures |

## ADR closure ladder

This is the folder's purpose. Each row closes independently and says what it is waiting on.

| ADR | Half | Closes when | Waiting on | Status |
|---|---|---|---|---|
| **ADR-03** controller backbone | — | G05 with margin on the Zero (or the twin with the pin-map header noted) **and** G04 on the SBC↔C2 link with real servos | Named servo load for the bus (C01 as reference, or later selected family); Phase B | Open |
| **ADR-12** internal communication and timebase | — | `link-contract.md` v1.0 implemented at both ends; G05 link and timestamp metrics met; `timebase.md` validated per its §6 | Phase A for loopback and DevKitC-1; Phase B for the flexing-harness CRC measurement | Open |
| **ADR-06** battery, rails, isolation, low-energy policy | **Architecture** | Registered `PA-01…16` and `RP02-P2-REG-02` basis implemented; G01 passed on the rig; chemistry chosen from the ledger's envelope; G06 paths credible on the body layout | Topology/basis registered; still waits on servo voltage, remaining power components and RP-06 body layout | Open — topology/basis fixed, implementation/evidence pending |
| **ADR-06** | **Sizing** | Ledger `W` rows cover every load group; trip-wire evaluated against the candidate pack; G03 rehearsal margin recorded | RP-03 drive `W` rows; Phase C battery gate | Open — **expected to close after RP-03, not in stage 2**; RP-02 records it as *bounded, not sized* |

## Candidate register

Candidates are recorded so selection happens from evidence. **Only the Raspberry Pi 5 2 GB row is selected; no purchase is authorized by this file.**

| Decision | Candidates | What is fixed for comparison | What decides it |
|---|---|---|---|
| Servo family | C01 XC330-M288-T (5 V TTL Dynamixel 2.0, paper OPEN); faster XC330-M181-T named as yaw comparison if sag/speed conflict unresolved; other families still admissible | Direct 1:1; Layout 03 23 g housings already match C01 | RP-01 paper P01–P06 then scored G01–G06; **this row is not selected** |
| **Main SBC (LG-01) — SELECTED 2026-09-16** | **Raspberry Pi 5, 2 GB**, selected under `RP02-P2-REG-02`. Same BCM2712, ISP and libcamera path as larger variants; the selected IMX708 camera has the supported CSI stack. Pi 5 4 GB remains the change-controlled fallback only if measured memory proves insufficient. | Must drive selected CM3 Wide over CSI; body-mounted; UART pairs for C2/display; 22-to-15-pin CSI cable, active cooler and dedicated 5.1 V nominal / 5 A-capable `PB-COMPUTE` | RP-07 profiling and thermal work now validate the selection and size its converter; **purchase remains separately authorized by the project builder** |
| Battery chemistry | Retained protected pack module using a suitable cylindrical or pouch-cell construction; exact chemistry/construction open. The historical loose-cell holder is a planning case only, not an architecture assumption | Placement low and forward; mass row 150–500 g; handling rules in `workbench.md`; complete assembly must satisfy `PB-MAIN` | Ledger composite peak and energy; G06 charging/removal paths; solo-builder risk |
| Pack configuration | 2S (regulated servo rail or direct for 6–7.4 V servos); 3S (12 V servo class) | Coupled to RP-01 servo family (PA-04). C01 points at 5 V class → 2S + motor-domain buck is the leading working assumption | RP-01 actuator selection, then ledger |
| Servo-rail conversion | Direct from pack; high-current buck on the motor domain | Rig socket accommodates both | Servo voltage window; measured `CC-06` transient with each |
| Compute-rail converter | `PCD-CVT-01` Murata OKL-T/6-W12P-C lead; `PCD-CVT-02` OKR-T/6-W12-C through-hole comparison; Pololu fixed-output modules are bench-only/rejected by use | Own 5.1 V nominal / 5 A-capable converter, never shared with motor domain (PA-05) | 6.0 V low-line step/thermal/ripple evidence and Pi power-entry method during `CC-06/CC-PEAK-01/ST-01` |
| C2/display conversion | `PCD-CVT-06` TPS630701 production lead; `PCD-CVT-07/-08` Pololu S13V10F5/S13V15F5 bench leads | Separate converters/protection/returns; 5 V class; C2 independent of display | Startup/current-limit, source transfer, quiescent, power-good and cross-branch fault evidence |
| Branch protection | `PCD-PRO-01` TPS25982 high-current lead; `PCD-PRO-02` TPS25947 low-current/reverse-blocking lead; `PCD-PRO-03` ATOF main-fuse family | Drop allocations, latch/retry policy and source-adjacent passive clearing path remain fixed requirements | Hot resistance, inrush/fault curves, path `I²t`, and upstream/downstream selectivity |
| Pack/internal connectors | `PCD-CON-01` SBS Mini pack lead; Micro-Fit 3.0 low-current and Micro-Fit+ high-current internal leads | Pack and charge cannot mate; positive retention; exact terminals/gauges count | Exact assembly, hot four-wire resistance, crimp pull, temperature-rise and motion/service evidence |
| E-stop/motor-arm hardware | `PCD-EST-01` IDEC XW1E 2NC operator lead; `PCD-EST-02` LTC4368-1 + external MOSFET engineering lead | E-stop contacts command a fail-open low-energy loop and never carry `PB-MOTOR`; release cannot re-arm | FET/shunt/SOA, regenerative signed current, hardwire truth table and F-12/F-13 evidence |
| Link transport | 3.3 V UART at 921 600 (primary); USB-CDC on native USB (fallback) | Same framing either way | G05 CRC error rate across the flexing harness; flashing-path conflict (CAD-04a) |
| Base/drive MCU | Same family as C2 (ESP32-S3) preferred; on-SBC RT thread rejected by AD-04 unless proven | Added in RP-03 | RP-03; heterogeneity caution in the control study |
| Microphone front end (LG-07) | **Suggested addition (2026-09-14 review):** a Raspberry Pi has one I2S port and no native 4-channel PDM capture, so four synchronized PDM MEMS mics need a codec HAT (AC108-class, I2S TDM, kernel-driver risk on current Pi 5 kernels) or a USB array (XMOS-class, no kernel driver, onboard DOA/beamforming — would also supply CAND-01 spatial hearing). Neither is selected | Body-mounted, non-collinear geometry per dimensional baseline | RP-05; sourcing matrix row; selected Pi 5 audio-input constraints |
| SBC ↔ display link topology | Two UART pairs across the yaw boundary (link-contract v0.2 baseline); **suggested alternative (2026-09-14 review):** SBC ↔ C2 only, with C2 relaying `FACE_STATE`/`LIGHT_STATE` to the display over a short in-head UART, removing two conductors from the moving harness and putting face and motion on one head-local timebase | Same framing either way; display's RS-485/UART pins per the schematic audit | G05 CRC measurement across the flex; whether C2-as-relay complicates fault containment (F-xx re-run) |
| Charging input/power path | USB-C inlet + `PCD-CHG-01` STUSB4500QTR PD sink + `PCD-CHG-02` BQ25798 charger/NVDC path is the leading architecture; adapter and exact implementation remain open | Display + minimum supervision on; motors/camera/normal SBC/audio off; AC mains never enters Makad | Chemistry/pack selection, PDO/NVM audit, pack-absent/depleted and CC-15 thermal/load tests, G06 |
| Low-energy thresholds | Loaded-source assertion/clear thresholds plus conservative energy estimate; coulomb counting is supplementary | Must satisfy `BR-08/10`, assert before the `V_SRC_SAFE` reaction margin is consumed and never restore an old arm/action | Selected pack/converters/controllers, path resistance, stop profile and `W` source/load captures; then preregistration |

## Conclusion

*(per ADR: pass / iterate / reject; selected candidates; budget rows updated with measured value, uncertainty and margin; downstream assumptions changed; re-run obligations created)*
