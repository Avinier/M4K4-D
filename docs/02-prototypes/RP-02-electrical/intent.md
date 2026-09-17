# RP-02 Intent — Electrical/Control Backbone

| Field | Value |
|---|---|
| Status | Design/gate intent current; Parts 1–4 are complete at design-definition level under `RP02-P1-REG-01`, `RP02-P2-REG-01…03`, `RP02-P3-REG-01/02` and `RP02-P4-REG-01`. Numeric thresholds, remaining component suffixes and every gate outcome remain open; no scored run executed |
| Owner | Project builder |
| Created | 2026-09-08 |
| Revised | 2026-09-16 |
| Governing plan | `../../01-system/risk-prototype-plan.md` v1.12 §RP-02 |
| Electrical baseline inherited | `../../01-system/control-topology-options.md` v0.15 (C2/C3 split, differential production links and C2 display relay selected; C3 suffix corrected to N8; C01 paper candidate named, family unselected); `compute-control-architecture.md` v1.2; `../RP-01-head/decision.md` CTRL-01…CTRL-06; `../../01-system/workbench.md` E-stop and PSU rules |
| Ledger | `../../01-system/power-energy-ledger.md` — the canonical power/energy/thermal budget; RP-02 populates it, it does not own a second copy |
| Feeds | ADR-03 (controller), ADR-06 (battery, rails, charging, isolation, low-energy policy), ADR-12 (internal communication and timebase); `subsystem-interfaces.md` at stage 6 |
| Method | `../../intuition.md` §5.1 — intent before numbers; step 3 electrical toolkit: peak concurrent current × path resistance, energy integration over the mixed-duty cycle, regulator/driver/wire thermal steady state |

## 1. Why RP-02 exists

RP-01 is an object: it has geometry, mass and a centre of mass, and it either fits or it does not. RP-02 is **a set of states and interfaces**. There is no single thing to hold — there is a tree of rails, a handful of boards, a message contract across a moving joint, and a space of concurrent operating conditions. Nothing about it is "does it fit"; everything is "what happens when these five things are true at once."

Every Makad subsystem will work alone. AD-08 says the peaks occur together: three head servos launching a wake rise while the amplifier hits an astromech chirp, the camera streams, the perception loop runs hot and the display transitions. If the rail sags and the C2 brownout detector resets the motion controller mid-slew, that is an unintended reset **and** unsafe motion, and it is invisible to any test that exercises one subsystem at a time. RP-02 is the instrument that makes that failure visible before the enclosure exists.

RP-02 exists to close three architecture decisions. Everything in this folder is justified by one of them. Parts 1–4 now define the state/load, power, compute/control and C0↔C2 interface baselines; closure still requires registered thresholds and physical evidence.

| ADR | What must be true to close it | Where RP-02 produces that |
|---|---|---|
| **ADR-03** controller backbone and compute split | Selected C2/C3 execute trajectories/reflexes, limits, watchdog and command expiry with measured margin; the split survives high-level failure (AD-04) | `compute-control-architecture.md`; `gates.md` G05, G04; `link-contract.md`; `fault-matrix.md` |
| **ADR-12** internal communication and timebase | The link transport, message set, expiry/health semantics and offset-reconciled timebase are chosen and proven on hardware | `link-contract.md`; `../../01-system/timebase.md`; `gates.md` G05 |
| **ADR-06** battery, rails, charging, isolation, low-energy policy | Two halves. **Architecture:** rail topology, protection, chemistry and isolation are decided from a budget *envelope*. **Sizing:** pack capacity and the 20-minute closure need the ledger to mature as real loads arrive | `power-architecture.md`; `gates.md` G01, G06; `../../01-system/power-energy-ledger.md`; `decision.md` closure ladder |

The split row for ADR-06 is the most important line in this folder. It is what stops RP-02 from either claiming closure it has not earned or stalling until the drive exists.

## 2. The two questions

The v1.9 plan asked only a can-question. A can-question is falsifiable but teaches nothing about margin; a how-question is the deliverable but has no failure mode. RP-02 carries both, and keeps them separate.

### 2.1 Design question — the deliverable

> What compute/controller split, internal link, rail and protection topology, and energy source lets Makad run representative head, drive, display, camera, audio and compute loads concurrently — and what is the measured margin of that design against each registered state?

The answer is a design (`power-architecture.md`, `link-contract.md`) plus a populated ledger with a margin column. "Margin" is a number per state per rail, not an adjective.

### 2.2 Gate question — the falsifier

> Does that design sustain every registered concurrent state and the registered mixed-duty cycle for at least 20 minutes without unsafe motion, unintended reset, rail excursion outside component limits, data staleness or thermal violation — and does every injected fault produce a bounded state?

The gate question is what `Reject` is reachable from. CON-10's 20 minutes cannot be weakened and `Defer` is unavailable for Core outcomes, so a miss forces a design change — lighter head, lower-draw servo class, different pack — never a threshold change.

### 2.3 Which gates are which

| Character | Gates | What closes them |
|---|---|---|
| **Verification** — a property holds or it does not; margin language does not apply | G01 protection, G04 fault containment, G06 serviceability | A reviewed checklist (G01, G06) or an injection campaign with zero unbounded outcomes (G04) |
| **Measurement** — the number and its headroom are the deliverable | G05 control feasibility; the G02 coexistence invariant; the G03 runtime rehearsal | Registered metric, frozen threshold, recorded margin |

G02 and G03 changed shape in plan v1.10. See `gates.md` §2 for what RP-02 records against them and where their genuine closure lives.

## 3. Traceability

| Kind | IDs |
|---|---|
| Architecture drivers | AD-04 safety survives high-level failure; AD-08 peak loads occur concurrently; AD-09 cloud bounded; AD-10 battery-powered and serviceable; AD-11 failures diagnosable |
| ADRs | ADR-03, ADR-06, ADR-12 (closes); ADR-10, ADR-11 (informs timeout and audio-power evidence) |
| Success criteria | SC-14 battery operation; SC-15 controlled stop and failure; SC-16 physical robustness; SC-17 serviceability; SC-18 reproducibility |
| Open thresholds | SC-TBD-10 battery reserve/low-energy behaviour; SC-TBD-11 endurance duty cycle; SC-TBD-12 thermal limits; SC-TBD-14 cloud-dependency timeout |
| Constraints | CON-03 honest costing; CON-07 tool availability; CON-10 ≥20 min untethered; CON-11 safety independent of network; CON-P02 accessible cutoff; CON-P04 explicit timeouts; CON-P05 power/heat/wiring estimates before CAD freeze |
| Budgets (`system-design-brief.md` §7) | Power and energy; thermal; internal communication; compute (coexistence portion); timing and latency (stop path portion) |

## 4. Inputs inherited — do not re-derive

| Input | Value | Source |
|---|---|---|
| Head motion controller | **C2: Waveshare ESP32-S3-Zero**, headerless; bench twin ESP32-S3-DevKitC-1-N8R8; one firmware target, pin map in one header | control study v0.15 §6.3; CTRL-04/06 |
| C2 responsibilities | Instantiates `MJ5`/`MS7`/`TRACK`/`BRAKE`, synchronizes yaw/pitch/roll, owns servo bus, limits, watchdog, E-stop/fault, command expiry | CTRL-03 |
| C2 pin constraints | E-stop/fault off GPIO0/3/45/46; GPIO21 is WS2812; native-USB flashing only (CAD-04a) | MEM-20260907-04 |
| Display | Waveshare ESP32-S3-LCD-4.3 no-touch SKU 30493; own ESP32-S3/LVGL renderer; receives semantic face state, never raster | display study; MEM-20260902-01 |
| Camera | Raspberry Pi Camera Module 3 Wide SC0874, 2-lane CSI-2, powered from the SBC camera port | camera study |
| Compute placement | **Selected Raspberry Pi 5 2 GB**, body-mounted; mics, speaker and battery body-mounted; head carries display, camera, light and C2 | `RP02-P2-REG-02`; dimensional baseline v1.10 |
| Link architecture | Framed UART over full-duplex differential signalling for C0↔C2/C3; C2 relays semantic display state over head-local RS-485; TTL is bench-only and USB service-only; no CAN, micro-ROS or I²C across joints | `RP02-P3-REG-01`; control study §3, §7 |
| Timebase recommendation | One master, timestamp-at-source, serial round-trip offset reconciliation; not PTP/NTP | control study §5 → `timebase.md` |
| Head load | Layout 03 nominal D/E tree ~362/436/509 g roll/pitch/yaw at M008=20 g, with ~499–524 g complete C2 sensitivity. **Paper demand complete 2026-09-13** (`fullproofmath.md`): controlling physical-law peaks pitch 0.0953 N·m at 57.8°/s, roll 0.0560 N·m at 70.2°/s, yaw 0.1099 N·m at 90.5°/s. Complete-head `W` mass still waits on M008 weigh-in | dimensional baseline v1.10; RP-01 physics; `fullproofmath.md` |
| Servo family | **Unselected.** First named paper candidate is ROBOTIS **XC330-M288-T** (C01, SKU 902-0173-000), 5 V class, Dynamixel Protocol 2.0 TTL; paper approval OPEN; yaw fails the rapid envelope at the 3.7 V sensitivity endpoint. Layout 03 already uses 23 g XC330 housings, so C01 adds zero mass to the paper tree. Not a SKU freeze. eManual `D`: stall 1.80 A at 5.0 V | `../RP-01-head/actuator-screen-01.md`; RP-01 `gates.md` paper P01–P06 |
| E-stop rule | System motor-arm plus dominant latching hardware E-stop cut the battery-only motor path, not safety supervision; retained-pack isolation remains separately accessible; exact switching device and connector are open | `power-architecture.md` PA-13/14; workbench.md |
| PSU rule | Korad KA3005D: set current limit to expected draw plus margin before first power-up; **5 A ceiling** | workbench.md |
| Battery placement and mass row | Low and forward of the drive axle; ledger row 150–500 g; chemistry undecided | mass ledger v0.13; dimensional baseline |
| Harness partition | Camera CSI on its own controlled route; power + semantic link as a segmented branch; servo power/bus sized for peak and separated from camera strain relief; demateable boundary at yaw (CAD-05) | harness study |

## 5. Scope

### 5.1 RP-02 owns

- the **reader-first operating-situation map** (`operating-situations.md`), audited against all approved foundation/system situations and grouping mode, energy, behaviour, person continuity, per-action lifecycle, health, events, loads, cases, faults and evidence under recognisable conditions;
- the **operating-state model** (`state-register.md`): modes/permissions, energy/health overlays, behavioural states, transitions, qualification concurrency, forbidden combinations and the proposed mixed-duty cycle;
- the **coverage proof** (`state-coverage-matrix.md`): requirement-to-vector-to-case-to-load-to-fault-to-evidence traceability;
- the **named load-profile contract** (`load-model.md`), which binds those cases to reproducible waveforms/duties without duplicating the numeric ledger;
- the **candidate power architecture** (`power-architecture.md`) as an ADR-06 input, evidence class `E`;
- the **link contract** (`link-contract.md`) as a versioned interface specification that outlives the prototype;
- the **compute/control ownership baseline** (`compute-control-architecture.md`) and its component/sourcing screen, including C0 process containment, C2/C3 authority, physical-link choice, watchdog layers and boot/arm/recovery;
- the **fault-injection matrix** (`fault-matrix.md`) and its required observables;
- the **bench rig** (`rig.md`), including which loads are real and which are characterized substitutes;
- **gate registrations** G01, G04, G05, G06 and the recorded rehearsals against the G02 invariant and the G03/SC-14 runtime requirement;
- **populating** `power-energy-ledger.md` from `D` rows to the first `W` rows;
- the **ADR closure ladder** in `decision.md`.

### 5.2 RP-02 does not

- duplicate `control-topology-options.md` — RP-02 closes it, it does not copy it;
- hold a second budget — the ledger in `01-system/` is the only power/energy record; the moment there are two, one is wrong;
- close SC-14 — the 20-minute untethered run of the *integrated droid* is a stage-7 validation; RP-02 rehearses it on the rig and records margin;
- select servos (RP-01), drive motors (RP-03), microphones or the speaker (RP-05/RP-06);
- write display firmware or define face assets;
- authorize any purchase — architecture selections and implementation leads are recorded with their evidence obligations, but purchase remains a separate builder action and ADR closure still requires the registered gates.

## 6. Phase ladder

Phase is a status field per document, not a directory. Artifacts mature at different rates and a directory split would invite "finishing Phase A" as a unit.

| Phase | Needs | Can produce | Cannot produce |
|---|---|---|---|
| **A — paper and on-hand hardware** | Nothing purchased beyond `workbench.md`; DevKitC-1 twin; display sample when it arrives; Korad PSU | Registered state/power/compute-control baselines; ledger `D`/`E` rows; link contract v0.3 first on TTL loopback then differential breakouts; timebase implementation and offset measurement; G01 and G06 paper review; F-01…30 harness; gate registrations | Any `W` row for a load that does not exist; production-link qualification from TTL alone; G02 composite peaks; G03 |
| **B — representative loads** | A named RP-01 servo load (C01 as reference unit, or a later selected family), selected Raspberry Pi 5 2 GB, selected camera, amp/speaker candidate; characterized substitutes for drive. C01 purchase is not a family freeze | Per-group `W` rows; G05 on real servo bus; G04 injection campaign on real link; G02 rehearsal at head-plus-compute concurrency; conductor/regulator thermal | Drive `W` rows; composite peak above the Korad 5 A ceiling without a second source; collapsed PA-04 rail voltage (needs family selection) |
| **C — onboard energy** | `workbench.md` battery gate satisfied (written procedure, bag, balance charger); candidate pack | G03 rehearsal with margin; ADR-06 sizing input; charging and isolation paths for G06 | SC-14 closure (integrated droid only) |

## 7. Relationship to RP-01

The dependency is circular and should be named rather than hidden. The two closures are different objects:

- RP-01's **complete-head `W` mass** (M900 / the physical ledger) cannot close while M008 is `U`. The installed C2 assembly — board + mount + connectors + assigned local harness — has not been weighed. That is unchanged.
- Layout 03 **paper demand does not wait on that weigh-in.** The mechanical-demand and 1,560-case sensitivity calculation is complete as of 2026-09-13 (`fullproofmath.md`), using M008=20 g `E` plus the 10/20/35 g sweep. Paper physics can screen a candidate; it cannot accept M900.
- C2's timing and electrical validity is still RP02-G05. RP-01's first scored run still needs the timebase and logging schema that RP-02 builds.
- RP-01's servo **selection** still sets RP-02's servo-rail voltage and the largest transient on the tree. The family is still unselected. The first named paper candidate is XC330-M288-T (C01) at a proposed 5 V nominal; paper approval is OPEN. That is a leading PA-04 working assumption, not a collapse. RP-01 paper gate P02 explicitly needs the loaded servo-terminal sag floor from this rail.

The resolution: RP-02's Phase A work runs now and **unblocks** RP-01's scored runs; Phase B may use C01 as a named reference load without treating a purchase as a family freeze; scored gates that need the frozen rail follow RP-01's selection. Neither prototype waits for the other to finish.

## 8. Evidence rules carried in from day one

The 490 g correction happened because an `E`-class planning value was treated as a target until confirmed geometry collapsed it. Power budgets are *more* prone to this — datasheet idle figures are quotable and optimistic.

1. **Evidence classes are the mass ledger's**, reused unchanged: `W` measured in the exact recorded state; `D` datasheet; `E` estimate from calculation or analogy; `U` unknown or unselected, never entered as zero.
2. **A substitute load needs an equivalence record** stating what it reproduces (average current, a stall step) and what it does not (inductive kick, regenerative current, thermal mass). Without the record it is not admissible against a gate.
3. **Thresholds freeze before data.** SC-TBD-10/11/12/14 receive gate-registration records with a dated builder approval before any scored run.
4. **Transient claims need a transient instrument.** G02's "rail excursion" is a millisecond event; `workbench.md` item 6 applies — an instrument on the bench must resolve the threshold, or the run is exploratory.
5. **Every state, fault and gate has a stable ID.** IDs are append-only; a changed definition gets a new version, never an edit.
