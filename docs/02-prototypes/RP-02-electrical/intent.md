# RP-02 Intent — Electrical/Control Backbone

| Field | Value |
|---|---|
| Status | Draft — design and gate questions authored; no state, threshold or candidate is registered; no run executed |
| Owner | Project builder |
| Created | 2026-09-08 |
| Governing plan | `../../01-system/risk-prototype-plan.md` v1.11 §RP-02 |
| Electrical baseline inherited | `../../01-system/control-topology-options.md` v0.10 (C2 selected, UART/USB link and timebase recommended); `../RP-01-head/decision.md` CTRL-01…CTRL-06; `../../01-system/workbench.md` E-stop and PSU rules |
| Ledger | `../../01-system/power-energy-ledger.md` — the canonical power/energy/thermal budget; RP-02 populates it, it does not own a second copy |
| Feeds | ADR-03 (controller), ADR-06 (battery, rails, charging, isolation, low-energy policy), ADR-12 (internal communication and timebase); `subsystem-interfaces.md` at stage 6 |
| Method | `../../intuition.md` §5.1 — intent before numbers; step 3 electrical toolkit: peak concurrent current × path resistance, energy integration over the mixed-duty cycle, regulator/driver/wire thermal steady state |

## 1. Why RP-02 exists

RP-01 is an object: it has geometry, mass and a centre of mass, and it either fits or it does not. RP-02 is **a set of states and interfaces**. There is no single thing to hold — there is a tree of rails, a handful of boards, a message contract across a moving joint, and a space of concurrent operating conditions. Nothing about it is "does it fit"; everything is "what happens when these five things are true at once."

Every Makad subsystem will work alone. AD-08 says the peaks occur together: three head servos launching a wake rise while the amplifier hits an astromech chirp, the camera streams, the perception loop runs hot and the display transitions. If the rail sags and the C2 brownout detector resets the motion controller mid-slew, that is an unintended reset **and** unsafe motion, and it is invisible to any test that exercises one subsystem at a time. RP-02 is the instrument that makes that failure visible before the enclosure exists.

RP-02 exists to close three architecture decisions. Everything in this folder is justified by one of them.

| ADR | What must be true to close it | Where RP-02 produces that |
|---|---|---|
| **ADR-03** controller backbone and compute split | The selected C2 executes trajectories, limits, watchdog and command expiry with measured margin; the split survives high-level failure (AD-04) | `gates.md` G05, G04; `link-contract.md`; `fault-matrix.md` |
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
| Head motion controller | **C2: Waveshare ESP32-S3-Zero**, headerless; bench twin ESP32-S3-DevKitC-1-N8R8; one firmware target, pin map in one header | control study v0.10 §6.3; CTRL-04/06 |
| C2 responsibilities | Instantiates `MJ5`/`MS7`/`TRACK`/`BRAKE`, synchronizes yaw/pitch/roll, owns servo bus, limits, watchdog, E-stop/fault, command expiry | CTRL-03 |
| C2 pin constraints | E-stop/fault off GPIO0/3/45/46; GPIO21 is WS2812; native-USB flashing only (CAD-04a) | MEM-20260907-04 |
| Display | Waveshare ESP32-S3-LCD-4.3 no-touch SKU 30493; own ESP32-S3/LVGL renderer; receives semantic face state, never raster | display study; MEM-20260902-01 |
| Camera | Raspberry Pi Camera Module 3 Wide SC0874, 2-lane CSI-2, powered from the SBC camera port | camera study |
| Compute placement | Body-mounted Linux SBC (unselected); mics, speaker, battery body-mounted; head carries display, camera, light, C2 | dimensional baseline v1.10 |
| Link recommendation | UART/USB serial, Vector-style; not CAN, micro-ROS or I²C across joints; semantic command surface | control study §3, §7 |
| Timebase recommendation | One master, timestamp-at-source, serial round-trip offset reconciliation; not PTP/NTP | control study §5 → `timebase.md` |
| Head load | Layout 03 nominal D/E tree ~362/436/509 g roll/pitch/yaw at M008=20 g, with ~499–524 g complete C2 sensitivity; substitute each servo candidate for the two 23 g references — this sets servo class, which sets the servo rail | dimensional baseline v1.10; RP-01 physics |
| Servo family | **Unselected.** XC330 is a packaging reference only (5 V class, `D` stall ≈1.8 A per unit — verify against eManual before use) | RP-01 decision; sourcing matrix |
| E-stop rule | Cuts the **motor bus, not logic power**; latching mushroom plus a physically yankable XT60 | workbench.md |
| PSU rule | Korad KA3005D: set current limit to expected draw plus margin before first power-up; **5 A ceiling** | workbench.md |
| Battery placement and mass row | Low and forward of the drive axle; ledger row 150–500 g; chemistry undecided | mass ledger v0.13; dimensional baseline |
| Harness partition | Camera CSI on its own controlled route; power + semantic link as a segmented branch; servo power/bus sized for peak and separated from camera strain relief; demateable boundary at yaw (CAD-05) | harness study |

## 5. Scope

### 5.1 RP-02 owns

- the **registered state set** (`state-register.md`) and the proposed mixed-duty cycle awaiting freeze;
- the **candidate power architecture** (`power-architecture.md`) as an ADR-06 input, evidence class `E`;
- the **link contract** (`link-contract.md`) as a versioned interface specification that outlives the prototype;
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
- authorize any purchase — candidates are recorded in `decision.md` with explicit *not selected* status until an ADR cites evidence.

## 6. Phase ladder

Phase is a status field per document, not a directory. Artifacts mature at different rates and a directory split would invite "finishing Phase A" as a unit.

| Phase | Needs | Can produce | Cannot produce |
|---|---|---|---|
| **A — paper and on-hand hardware** | Nothing purchased beyond `workbench.md`; DevKitC-1 twin; display sample when it arrives; Korad PSU | State register; ledger `D`/`E` rows; power architecture candidate; link contract v0.x on a loopback and on DevKitC-1↔laptop; timebase implementation and offset measurement; G01 and G06 paper review; fault matrix rows; gate registrations | Any `W` row for a load that does not exist; G02 composite peaks; G03 |
| **B — representative loads** | RP-01 servo family selected (or a reference unit), an SBC candidate, camera, amp/speaker candidate; characterized substitutes for drive | Per-group `W` rows; G05 on real servo bus; G04 injection campaign on real link; G02 rehearsal at head-plus-compute concurrency; conductor/regulator thermal | Drive `W` rows; composite peak above the Korad 5 A ceiling without a second source |
| **C — onboard energy** | `workbench.md` battery gate satisfied (written procedure, bag, balance charger); candidate pack | G03 rehearsal with margin; ADR-06 sizing input; charging and isolation paths for G06 | SC-14 closure (integrated droid only) |

## 7. Relationship to RP-01

The dependency is circular and should be named rather than hidden. RP-01's complete mass cannot close because M008 is `U` until the installed C2 assembly is weighed; C2's timing and electrical validity is RP02-G05. RP-01's first scored run needs the timebase and logging schema that RP-02 builds. RP-01's servo selection sets RP-02's servo rail voltage and the largest transient on the tree.

The resolution: RP-02's Phase A work runs now and **unblocks** RP-01's scored runs; RP-02's scored gates that need representative loads follow RP-01's selections. Neither prototype waits for the other to finish.

## 8. Evidence rules carried in from day one

The 490 g correction happened because an `E`-class planning value was treated as a target until confirmed geometry collapsed it. Power budgets are *more* prone to this — datasheet idle figures are quotable and optimistic.

1. **Evidence classes are the mass ledger's**, reused unchanged: `W` measured in the exact recorded state; `D` datasheet; `E` estimate from calculation or analogy; `U` unknown or unselected, never entered as zero.
2. **A substitute load needs an equivalence record** stating what it reproduces (average current, a stall step) and what it does not (inductive kick, regenerative current, thermal mass). Without the record it is not admissible against a gate.
3. **Thresholds freeze before data.** SC-TBD-10/11/12/14 receive gate-registration records with a dated builder approval before any scored run.
4. **Transient claims need a transient instrument.** G02's "rail excursion" is a millisecond event; `workbench.md` item 6 applies — an instrument on the bench must resolve the threshold, or the run is exploratory.
5. **Every state, fault and gate has a stable ID.** IDs are append-only; a changed definition gets a new version, never an edit.
