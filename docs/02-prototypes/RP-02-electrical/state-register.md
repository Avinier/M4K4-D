# RP-02 State Register — Registered Concurrent States

| Field | Value |
|---|---|
| Status | **Proposed — no state is registered.** Registration requires a dated builder approval before the first scored run that cites it |
| Owner | Project builder |
| Created | 2026-09-08 |
| Revised | 2026-09-12 |
| Authority | `../../01-system/risk-prototype-plan.md` v1.11 §RP-02 ("every registered concurrent state"); `../../01-system/power-energy-ledger.md` coexistence invariant |
| Load-group codes | `LG-xx` are defined once in `../../01-system/power-energy-ledger.md` §2 and only referenced here |
| Character sources | `../RP-01-head/intent.md` HM-00…HM-18; `../../00-foundation/core-interaction-scenarios.md`; `../../01-system/system-design-brief.md` §6 state dimensions |

This register is RP-02's equivalent of RP-01's storyboard. The storyboard enumerated the motion vocabulary the mechanism must support; this enumerates the **electrical state vocabulary the backbone must survive**. The G02 coexistence invariant is meaningless without it: "peak" would mean whatever happened to be tried.

## 1. Rules

1. **Stable IDs, append-only.** A state, once registered, is never edited. A changed definition gets a new ID or a version suffix (`S04.v2`) and the old one is marked superseded. Unregistered proposals below may be edited freely until registration.
2. **Every state names its load groups and their expected class** — off / idle / average / peak — per group. The ledger turns that into current and energy; this file does not carry numbers.
3. **Every state names the hazard it exposes.** Motion active, hazardous output present, or none. This decides whether a fault injected during the state is a G04 case.
4. **Every state is reachable from a Core scenario or a safety requirement.** A state that serves neither is not registered.
5. **Registration freezes the composition of `MD-01`**, the mixed-duty cycle. After freezing, a changed cycle is `MD-02` with a documented reason.

## 2. State dimensions this register uses

From `system-design-brief.md` §6. A registered state is a point in these dimensions, not a new enum.

| Dimension | Values used here |
|---|---|
| Physical permission | floor · tabletop · motion inhibited · hard stop |
| Interaction phase | asleep · waking · attentive · handling request · returning to idle |
| Energy state | normal · low · critical · charging |
| Subsystem health | available · degraded · unavailable · unsafe |

## 3. Proposed states

Expected class per load group: `–` off, `I` idle/quiescent, `A` average working, `P` peak/transient, `?` depends on later selection. Groups: `LG-01` SBC · `LG-02` C2 · `LG-03` head servos (Y/P/R) · `LG-04` drive · `LG-05` display + light · `LG-06` camera · `LG-07` mics/audio front end · `LG-08` speaker/amp · `LG-10` base MCU/safety sensing.

### 3.1 Lifecycle and rest

| ID | State | Permission / phase / energy | LG-01 | LG-02 | LG-03 | LG-04 | LG-05 | LG-06 | LG-07 | LG-08 | LG-10 | Hazard exposed | Why it is registered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **S00** | Hard stop — E-stop asserted, logic powered | hard stop / any / any | I | I | – | – | I | I | I | – | I | None — motor bus dead; proves logic survives the cut | G01, G04 baseline; `workbench.md` E-stop rule; CON-P02 |
| **S01** | Cold start / boot | inhibited → floor or tabletop / asleep / normal | P (boot) | P (boot) | – → I | – | P (boot) | I | I | – | P | Servo enable during boot before limits are loaded | SC-18 reproducibility; startup order; inrush; G04 "recover only from authorized intent" |
| **S02** | Quiet idle, head down | any / asleep / normal | I | I | I (hold or unpowered per HM-00 result) | – | I (dim) | ? (wake path may need camera) | A (listening for name) | – | I | Minimal; holding torque if not balanced | Largest fraction of `MD-01`; defines the floor of the energy budget |
| **S03** | Attentive idle, procedural aliveness | any / attentive / normal | A | A | A (low amplitude) | – | A | A (streaming) | A | – | I | Motion active, low energy | HM-01 + SC-09; the "resting" state of an awake droid |
| **S15** | Orderly shutdown | any / returning to idle / any | A → – | A → – | A (HM-02 descent) → – | – | A → – | – | – | A (sign-off chirp) → – | – | Descent into rest under falling rails | Shutdown order; must not slew as rails collapse |

### 3.2 Performance peaks (head-dominant)

| ID | State | Permission / phase / energy | LG-01 | LG-02 | LG-03 | LG-04 | LG-05 | LG-06 | LG-07 | LG-08 | LG-10 | Hazard exposed | Why it is registered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **S04** | Wake performance | any / waking / normal | P (perception spin-up) | P | **P** (HM-03 rise, three axes) | – | P (transition) | P (acquisition) | A | **P** (acknowledgement chirp) | I | Fast three-axis motion while every other head load peaks | **The canonical coexistence case.** Scenario 1; SC-21; AD-08 |
| **S05** | Search sweep | any / attentive / normal | P (perception) | A | A→P (HM-04 yaw sectors) | – | A | P | A | I | I | Repeated yaw reversals with camera load | Harness current plus CSI signal integrity across yaw |
| **S06** | Gesture burst | any / handling request / normal | A | P | **P** (HM-06/07/08/09 stitched `MJ5` reversals) | – | A | A | A | A | I | Highest servo current density from reversals | Servo rail transient minimum; C2 loop under bus load |
| **S07** | Startle | any / any / normal | A | P | **P** (HM-15 simultaneous three-axis outbound, 180–250 ms) | – | P | A | A | P | I | Largest simultaneous head transient | Sizes the servo-rail bulk capacitance and conductor drop; combined-load case, not a per-axis peak |

### 3.3 Interaction and audio

| ID | State | Permission / phase / energy | LG-01 | LG-02 | LG-03 | LG-04 | LG-05 | LG-06 | LG-07 | LG-08 | LG-10 | Hazard exposed | Why it is registered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **S08** | Spoken request round-trip | any / handling request / normal | P (capture, cloud, utility view) | A | A (attentive corrections) | – | P (utility view) | A | P | P (response) | I | Cloud timeout during motion | SC-06/SC-22; SC-TBD-14 timeout registration; network loss injection point |
| **S09** | Music vibe | any / attentive / normal | A | A | A (small sustained motion) | – | P (eye vibe) | A | A (capture during playback) | **P sustained** | I | Sustained audio peak plus simultaneous capture | SC-23; ADR-11 evidence; longest-duration LG-08 peak in `MD-01` |

### 3.4 Locomotion (floor only; RP-03 loads)

| ID | State | Permission / phase / energy | LG-01 | LG-02 | LG-03 | LG-04 | LG-05 | LG-06 | LG-07 | LG-08 | LG-10 | Hazard exposed | Why it is registered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **S10** | Base acceleration / reversal | floor / any / normal | A | A | A | **P** (two motors from rest, reversal) | A | A | A | I | P | Motor stall transient on the motor bus shared with servos | Drive inrush versus servo rail; `≤2.0 m/s²` caster-lift limit stays in force |
| **S11** | Come / follow | floor / handling request / normal | **P** (tracking loop) | A | A (`TRACK` corrections) | A | A | P | A | A | P | Sustained compute peak plus continuous motion | Scenario 2; SC-24; the longest sustained multi-group average |
| **S12** | Excited spin | floor / handling request / normal | A | A | A | **P** (sustained max) | P | A | A | P | P | Maximum drive current for the spin duration | SC-25; bounded spin envelope |
| **S17** | Tabletop mode | tabletop / any / normal | A | A | A | **– (inhibited)** | A | A | A | A | P (edge sensing) | Locomotion must stay inhibited under every other load | AD-07; SC-13; a permission state, registered so inhibit is tested under load |

### 3.5 Composite and energy states

| ID | State | Definition | Hazard exposed | Why it is registered |
|---|---|---|---|---|
| **S13** | Maximum safe concurrency | The registered worst credible composite: S07 startle **during** S09 playback **during** S10 base reversal, with perception at S11 load and the display transitioning. Composed from registered states; not a new load profile | Everything at once | **The transient anchor of the G02 invariant.** Passing S13 covers only simultaneous peak rail/current behaviour; sustained, thermal, protocol and state-specific behaviours still require their individual states. If S13 cannot be produced on the rig, that is recorded, not assumed |
| **S14** | Low-energy operation | Energy state `low`: registered inhibitions apply (candidate: base motion inhibited, gesture amplitude reduced, audio level capped) while visible/audible response is retained | Motion after the threshold crossing | SC-TBD-10 reserve and low-battery behaviour; ADR-06 policy |
| **S16** | Critical / charging | Energy state `critical` (orderly shutdown forced) and `charging` (all hazardous outputs inhibited; display may show state) | Motion while charging | G06 charging path; battery gate; SC-TBD-10 |

## 4. `MD-01` — proposed mixed-duty cycle (not frozen)

CON-10 requires 20 minutes of *representative mixed-duty* operation. Without a frozen recipe the requirement is trivially met by a dim, idle droid. This proposal is for the builder to approve, adjust and freeze; its proportions are authored from the two Core scenarios, not measured.

| Segment | State | Count / duration | Rationale |
|---|---|---|---|
| Quiet idle | S02 | 4 min total, split across the cycle | A droid on a desk spends real time asleep |
| Attentive idle | S03 | **8 min 34 s total** | Awake, alive, not performing; includes the time needed to make the proposed cycle exactly 20 minutes |
| Wakes | S04 | 6 events × 1 s, plus 2 searches × 3 s in S05 (**12 s total**) | Scenario 1 repeated; the coexistence case must recur, not happen once |
| Gesture bursts | S06 | 12 events, **20 s total** | Yes/no/laugh/wobble spread through the interactions |
| Startles | S07 | 2 events, **1 s total** | Rare, but the largest head transient must be inside the cycle |
| Spoken requests | S08 | 4 round-trips, **40 s total** | Time, timer, alarm, Spotify start |
| Music | S09 | 3 min continuous | Sustained audio peak inside the cycle |
| Base motion | S10 + S11 | 3 min total including 2 come approaches and 1 follow route of ~3 m at ≤0.5 m/s, with ≥6 accelerations/reversals | Scenario 2 |
| Spin | S12 | 1 event, **3 s** | SC-25 |
| Shutdown | S15 | 1, **10 s**, at the end | Orderly, on the energy remaining |
| **Total** | | **20 min elapsed**; S13 is produced by overlap within the listed time and adds no duration | |

Freeze fields when registered: exact ordering, the overlap that produces S13, servo family and load configuration, and the instrument that logs per-group current at ≥ the transient-resolving rate.

## 5. Not states

- **Individual subsystem bring-up** (a servo on the bench, the display alone) is exploratory work under `EXP` run IDs. It populates ledger rows; it does not close any G02 claim.
- **Fault conditions** are not states. They are injected *into* a state and live in `fault-matrix.md`; the state names the hazard the fault would expose.
- **Charging while operating** is not registered for V1. If ADR-06 selects onboard charging, `S16` splits.

## 6. Registration record

*(none yet)* — each registration will record: state ID, version, dated builder approval, the ledger revision it was registered against, and the run IDs that later cite it.
