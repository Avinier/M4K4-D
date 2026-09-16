# RP-02 Gate Registrations

| Field | Value |
|---|---|
| Status | **Part-1 case-to-gate coverage approved under `RP02-P1-REG-01` on 2026-09-15.** Candidate numeric metrics/thresholds below remain proposals; no numeric gate is registered and no scored run exists |
| Authority | Gate definitions and registration fields: `../../01-system/risk-prototype-plan.md` v1.12 §RP-02. This file holds the registered numeric versions |
| Sources for thresholds | `intent.md`; `state-register.md`; `load-model.md`; `link-contract.md` §7; `fault-matrix.md` §3; `power-architecture.md` PA-06; registered `power-implementation-basis.md`; derived `power-calculation-ledger.md`; `../../01-system/power-energy-ledger.md`; RP-01 paper P02 sag-floor need |
| Rule | Registration uses the plan's fields — Gate ID, Metric, Threshold, Rationale, Conditions, Repetitions, Instrument, Freeze record (date + builder approval **before** scored data is inspected). A threshold change after results is a new gate version with a documented reason and a fresh test set, never an edit |

## 1. Gates to register

Plan v1.10 keeps six IDs and changes the shape of two.

| Gate | Character | What RP-02 registers here |
|---|---|---|
| **RP02-G01 Protection** | Verification | A reviewed checklist: isolation, fusing/current limiting, conductor/connector sizing assumptions, no exposed unbounded hazardous energy path |
| **RP02-G02 Peak coexistence** | Measurement → **standing invariant** | RP-02 registers the *rehearsal* metric and the rail-excursion definition; the invariant itself and its re-run rule live in the ledger (§2.1 below) |
| **RP02-G03 Runtime** | Measurement → **rehearsal of SC-14** | RP-02 registers the rehearsal on the candidate pack with recorded margin; closure of the 20-minute requirement is SC-14 at integration (§2.2) |
| **RP02-G04 Fault containment** | Verification | Injection campaign per `fault-matrix.md` with zero unbounded outcomes |
| **RP02-G05 Control feasibility** | Measurement | Loop, link and timestamp performance with registered margin against RP-01 and projected base needs |
| **RP02-G06 Serviceability** | Verification | Credible physical paths for isolation, charging, battery removal, measurement points, high-risk module access |

## 2. The two reshaped gates

### 2.1 G02 — what "peak coexistence" means after v1.10

The v1.9 gate ("every registered concurrent state completes without…") is a *moment*; the electrical backbone never has one. Every subsystem that arrives later — drive in RP-03, speaker in RP-05 — reopens it. So the claim is now split:

- **The invariant** (owned by `power-energy-ledger.md` §5): every registered `CC-xx` state vector completes without unintended reset, unsafe motion, rail excursion outside registered component limits, data corruption or thermal-limit violation. Re-run all applicable cases whenever a load profile changes evidence/hardware, a load group is added, or a rail changes.
- **RP-02's registration** is the rehearsal metric any re-run uses: per case, per rail — minimum voltage versus component limit, reset count, CRC errors and temperature. `CC-PEAK-01` is the maximum credible transient; synthetic `ST-01` is a separate robustness test and may require the Phase-C source because the Korad is limited to 5 A.

What a *pass* looks like in `decision.md`: "invariant verified on 2026-xx-xx against ledger vX.Y for the registered non-drive cases (`CC-01`, `CC-02F/T`, `CC-03/03N`, `CC-04…08`, `CC-12A/B`, `CC-13H`, `CC-14…18`) with real head loads; drive-dependent `CC-09/09C/09R`, `CC-10A/B/C`, `CC-11`, `CC-12C`, `CC-13D`, `CC-PEAK-01` and the drive portion of `ST-01` pending RP-03 hardware; re-run due on the next profile/hardware change." Lettered lifecycle cases such as `CC-07D/E` are named individually in the actual record rather than hidden by a range.

`CC-PEAK-01` is the worst currently credible whole-robot transient. `ST-01` deliberately aligns otherwise forbidden peaks. Neither replaces sustained, thermal, accumulated-link-error or state-specific recovery runs.

### 2.2 G03 — what "runtime" means after v1.10

SC-14 already says "the integrated droid completes at least 20 minutes of representative mixed-duty untethered operation." A bench rig with substitute drive cannot close that. RP-02's job is **early warning with margin**: run the frozen `MD-01` on the candidate pack in Phase C, integrate energy per group, and report the margin against the 20-minute floor and the SC-TBD-10 reserve. If the margin is negative or thin, the design changes *now* — servo class, head mass, pack — while there is calendar left. If it is comfortable, ADR-06 sizing gets a bounded input.

`Defer` is unavailable and CON-10 cannot be weakened; a negative rehearsal is an `iterate` on the design, never a threshold change.

## 3. Candidate registrations — not registered

Every number below is a candidate awaiting a dated builder approval. Registering one means copying its row into §4 with the freeze record filled in.

### RP02-G01 Protection — candidate checklist

| Item | Pass condition | Method |
|---|---|---|
| Main isolation | One physical action at the selected retained pack connector/isolation device removes the pack from everything; reachable without tools; visible | Review + demonstration |
| System motor-arm | `PB-MOTOR` is off in system `OFF`, boot inhibit and `CHARGE`, independent of E-stop release state | Demonstration across the registered power-state matrix |
| E-stop | Latching hardware stage dominates the motor-arm command; assertion removes `PB-MOTOR` while safety supervision stays up (`OM-04`); release does not restore motion authorization or an old command | Demonstration under `CC-06`, later `CC-10A`, including F-12/F-13 |
| Pack protection | Complete retained pack assembly has documented protection, cell matching/retention and assembly-level current/temperature limits | Datasheet + assembly review |
| Main protection | Rating is within downstream conductor/connector limits; non-trip envelope clears `CC-PEAK-01` and the registered admissible `ST-01`; branch faults coordinate before main/pack protection | Ledger + applicable time-current, I²t or current-limit curves |
| Branch protection | Every registered final `PB-*` branch has an identified protective element or a justified bounded upstream limit; a branch fault is contained before main/pack protection where selectivity is required | Ledger + fault-current and protection-coordinate analysis |
| Conductor sizing | Every conductor is rated above the maximum energy its upstream protection can pass; `PB-HEAD-Y/P/R` load-end drop stays within the registered servo-family limit during `CC-06` | Calculation + load-end measurement |
| Connectors | No power connector can mate reversed; current/voltage/temperature rating covers the protected branch; yaw-boundary connector's mated resistance is recorded | Review + measurement |
| Returns and back-power | Star/paired return intent is preserved; no signal, telemetry, programming or charge path back-powers an off branch | Schematic walk + partial-power injection |
| No unbounded path | Walk the tree: every node between an energy source and a load has a fuse, e-fuse, current limiter or documented bounded source upstream | Review with `power-architecture.md` and `power-branch-contracts.md` |
| Repetitions | Review once per rig revision; E-stop demonstration every session | — |

### RP02-G02 rehearsal — candidate metrics

| Metric | Candidate threshold | Instrument |
|---|---|---|
| Rail minimum margin, per rail per case | `V_min − V_UVLO(component) ≥ 0.25 V` on `PB-COMPUTE` and applicable safety branches; head-axis terminal voltage ≥ family minimum with drop ≤ 3 % (PA-06). C01's 3.7 V is a sensitivity endpoint, not the sag floor | INA226 at max rate; oscilloscope for `CC-06/CC-PEAK-01/ST-01`; resolution stated |
| Unintended resets | 0 across all repetitions of every registered state | Reset-reason logs |
| CRC errors on the SBC↔C2 link | ≤ registered rate from F-04 | `HEARTBEAT` counters |
| Temperatures | ≤ SC-TBD-12 values once registered; until then, record and flag > 60 °C on any touchable surface | Thermistors |
| Brownout order | Under the preregistered slow path, new peaks stop at `EN-02`, non-safety demand sheds at `EN-03`, and motor permission/local enables are inactive before safety-control validity is lost; under the fast path, hardware/local inhibit does not wait for the SBC | Time-correlated source/rail, `ENERGY_OK`, gate/enable, PG/reset and motor-bus capture per `brownout-restart-contract.md` §8 |
| Recovery after energy loss/reset | 0 old actions replayed and 0 motor re-enables without the required fresh mode/arm/enable/action sequence | Epoch/session/action logs plus motor-arm and driver-enable probes |
| Repetitions | ≥3 per registered `CC`; `CC-03/05/06` ≥10 events per registered motion variant | — |

### RP02-G03 rehearsal — candidate metrics

| Metric | Candidate threshold | Instrument |
|---|---|---|
| `MD-01` completion on the candidate pack | Completes; `EN-03` is not reached before scheduled `EV-14` | INA226 at input, 10 Hz |
| Energy margin | `(E_pack,usable / E_MD01) − 1 ≥ registered reserve`; candidate reserve 25% | Integration of `i_in · v_in`; `E_pack,usable = E_pack,nominal · DoD_usable · η_system` |
| Reserve | Per SC-TBD-10 once registered; candidate additive reserve `r = 25%`, using the convention in `power-calculation-ledger.md` | — |
| Repetitions | 2 full cycles on the same pack state; pack rested between | — |

### RP02-G04 Fault containment — candidate metrics

Per `fault-matrix.md` §3: time-to-`BRAKE` ≤ 200 ms (heartbeat-mediated) or ≤ 1 tick (local detection); **0** obsolete commands executed; health correct within 2 heartbeat periods; **0** motion after recovery without a fresh enable; ≥ 5 repetitions per row in ≥ 2 states.

### RP02-G05 Control feasibility — candidate metrics

| Metric | Candidate threshold | Why | Instrument |
|---|---|---|---|
| C2 trajectory loop rate and jitter | ≥ 200 Hz sustained with the servo bus and link active; jitter p99 ≤ 10 % of period | HM-08 7°/100 ms pulses; `physics.md` peak accelerations | GPIO tick on the logic analyzer, cross-checked with the self-report |
| Servo bus update rate | ≥ 100 Hz sync write + read, three axes | Family-defined; measured, not assumed | Bus decode on the analyzer |
| Link round-trip p95 | ≤ 5 ms at 921 600 baud | `TRACK` feel; RP-05 tightens | `TIME_SYNC` round-trip statistics |
| Timestamp reconciliation error p95 | ≤ 1 ms | Per-axis event alignment for RP-01 combined reversals | `sync_edge` versus `c2_tick` on the analyzer (`timebase.md` §6) |
| Link CRC error rate across the flexing harness | Registered from measurement under `CC-04` search sweeps; candidate acceptance ≤1 per 10⁵ frames | F-04; harness signal integrity | `crc_err_count` |
| Heartbeat-timeout-to-brake | ≤ 200 ms | SC-15 | F-01 timing |
| Margin | Every metric reports measured / threshold as a ratio; ADR-03 closes only with ≥ 1.5× on loop rate and ≤ 0.5× on latency figures | "with registered margin" is in the plan's wording | — |
| Repetitions | ≥ 10 min continuous capture per configuration; ≥ 3 configurations (rendering off/on on the display board is *not* required — C2 is a separate board — but link load high/low and servo bus active/idle are) | — | — |

### RP02-G06 Serviceability — candidate checklist

| Path | Pass condition |
|---|---|
| Isolation | Selected main pack isolation action is reachable with the shell on and requires no tools |
| Charging connection | Keyed low-voltage DC charge input reachable with shell on; strain relief/polarity protection documented; pack remains separately removable for service |
| Battery removal | Pack out and in without disturbing unrelated assemblies; documented procedure with time |
| Measurement points | `PB-MAIN` voltage/current plus registered branch source/load-end points are accessible without disassembly beyond a service panel |
| High-risk module access | The named high-risk module (SC-17 — candidate: the C2 assembly, because of CAD-04a flashing and the moving harness) replaceable without destructive disassembly |
| Repetitions | Procedure performed twice by the builder, timed |

## 4. Registered gates

*(none yet)*
