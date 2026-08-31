# Makad / M4K4-D

> **Current project overview**
>
> Foundation approved: **14 August 2026**
>
> V1 deadline: **5 December 2026**

**Makad**, technical designation **M4K4-D** and commonly shortened to **M4**, is a personal droid. M4 is intended to occupy the kind of companion role R2-D2 occupied for Luke Skywalker: recognizable, attentive, expressive, and full of character.

The central V1 priority is simple:

> **M4 should feel alive.**

Makad's defining advantage is expressiveness. That expression comes from what M4 understands, sees, and hears—and from how convincingly its display, status light, astromech audio, head, wheeled base, and timing communicate one intent.

This README is an orientation document derived from the approved foundation. It does not replace the detailed source documents linked below.

## Project status

| Area | Status |
|---|---|
| Vision | Approved |
| V1 scope | Approved |
| Constraints | Approved; dimensional/packaging target baseline active, some engineering values remain open |
| Success criteria | Approved; numeric thresholds remain open |
| Core interaction scenarios | Approved at scenario level |
| System design brief | Approved |
| System architecture | Not yet defined |
| Engineering budgets | Not yet closed |
| Risk prototypes | Plan approved; execution not yet started |
| Workbench sourcing/readiness | Approved; procurement not yet completed |
| Run identity and evidence storage | Active v1.0 convention; guarded launcher, log schema, and time/video synchronization remain open |
| Exact components and BOM | Not yet selected |
| Integrated CAD | Not frozen |
| Existing `specsheets/` | Exploratory, non-binding reference material |
| Existing `visuals/` | Provisional visual references |

## Approved foundation

- [Vision](docs/00-foundation/vision.md)
- [V1 scope](docs/00-foundation/v1-scope.md)
- [Constraints](docs/00-foundation/constraints.md)
- [Success criteria](docs/00-foundation/success-criteria.md)
- [Core interaction scenarios](docs/00-foundation/core-interaction-scenarios.md)
- [Decision history](MEMORY.md)

## System engineering

- [Canonical engineering intuition guide (all phases)](docs/intuition.md)
- [Approved system design brief](docs/01-system/system-design-brief.md)
- [Approved risk-prototype plan](docs/01-system/risk-prototype-plan.md)
- [Approved workbench sourcing and test-readiness baseline](docs/01-system/workbench.md)
- [Active run-record convention and evidence layout](docs/01-system/run-record-convention.md)
- [Current dimensional and packaging baseline](docs/01-system/dimensional-baseline.md)

## Physical prototype run records

Every bounded physical prototype execution that energizes an actuator, applies representative electrical/mechanical load, or produces decision evidence receives one permanent run ID. Routine assembly, soldering, passive inspection, and unpowered fit checks do not require one unless their result will be cited.

The canonical format is:

```text
RP<prototype>-<gate-and-version-or-EXP>-<exploratory|pilot|scored>-<UTC allocation>-<sequence>
```

For example, `RP01-G03V1-scored-20260822T091530Z-01` identifies one scored RP-01 execution against gate G03 version 1. A retry, power cycle, controlled configuration change, or new trial block receives a new ID. Failed, invalid, unsafe, and aborted runs keep their IDs and evidence; IDs are never renamed, reused, or deleted.

The run record binds that identity to the repository, firmware, software, applied configuration, runtime overrides, rig revision, ballast/geometry, sourced parts, instruments, active limits, readiness checks, raw data, media, derived results, and artifact hashes. Exploratory motion uses an automatically generated `EXP-exploratory` ID rather than bypassing the record. Gate outcomes remain separate because several runs may contribute to one pass/iterate/reject/defer decision.

The operating invariant is:

> **No valid run ID plus no confirmed logger means no actuator enable.**

Until a guarded launcher enforces this in software, the builder applies it as a pre-arm bench check by creating the run directory from [the run-record template](docs/02-prototypes/_templates/run-record.md), filling the pre-run fields, starting the logger, confirming a sample was written with the same ID, and showing or announcing the ID at the start of external video. The launcher, machine-readable logging schema, monotonic timebase, and video-synchronization validation remain required before the first powered scored run.

## Identity and design direction

M4 is a droid, not primarily a desktop assistant, smart speaker, or generic social robot.

The approved visual and physical direction is:

- strongly inspired by Star Wars droids;
- cyberpunk, rugged, scrappy, and characterful;
- mechanical rather than glossy or appliance-like;
- modular and screw-together, with visible fasteners, panels, seams, and service access contributing to the personality;
- approachable without optimizing for minimum size;
- open to substantial redesign from the current renders.

The current physical target is **300 H × 205 W × 180 D mm overall**, with an approximately **95 H × 150 W × 115 D mm nominal head** validated within a **90–100 H × 145–155 W × 110–120 D mm** band, **Ø84 mm wheels**, **170 mm track**, and **110 mm drive-axle-to-front-caster wheelbase**. The head envelope is built outward from the selected 106.1 × 67.8 mm display rather than from the earlier oversized concept-art proportion. The detailed [dimensional and packaging baseline](docs/01-system/dimensional-baseline.md) overrides earlier planning values. Face geometry, shell language, colours, manufacturing tolerances, total mass, exact parts, and internal architecture remain subject to prototype and packaging validation.

## V1 Core

V1 is not complete unless the following outcomes work together as one droid.

### Expression and character

- A high-quality animated face runs on M4's onboard display.
- Powered roll, pitch, and yaw head motion communicate attention and authored expression.
- At least one controllable LED beside the head camera participates in wake, attention, and status behaviours.
- M4 communicates in a custom non-English astromech-style language authored by the builder.
- Idle behaviour makes M4 feel alive without constant manual control.
- Display, LED, astromech audio, head motion, base motion, and timing express the same perceived intent.
- M4 can perform at least one bounded excited spin as a deliberate character action.

### Understanding and perception

- M4 understands natural spoken interaction within the approved V1 scenarios.
- The approved invocation forms are **“M4,” “M4K4,” and “Makad.”**
- M4 visually acquires a nearby person or face and directs attention toward them.
- M4 maintains or reacquires person tracking through the later-defined V1 test cases.
- Detailed intent phrasing and the astromech vocabulary will be designed later; the approved scenario semantics already define what the system must accomplish.

### Mobility and following

- M4 is a battery-powered wheeled floor droid.
- The drive baseline is two independently powered, encoder-equipped wheels plus a front caster and mandatory rear anti-tip skid; exact motors, transmissions, drivers, and control parameters remain engineering decisions.
- In response to “come here,” M4 finds the person, approaches safely, and stops at a bounded distance.
- In response to “follow me,” M4 tracks and follows the selected person through an approved indoor route.
- M4 handles relevant obstacles, stopping, temporary target loss, and unsafe conditions without continuing blindly.
- Movement must remain stable and avoid harmful contact inside the validated operating envelope.

### Utility and entertainment

- M4 can display the current time when asked.
- M4 can create and signal timers.
- M4 can create and signal alarms.
- M4 can start requested Spotify playback through an approved connected integration.
- During music playback, M4 enters an expressive music state; at minimum, its eyes visually “vibe” to the music.

### Operation and construction

- Final V1 runs untethered from an onboard battery; tethered or bench operation is acceptable during development.
- Floor mode is the primary locomotion mode.
- Large-tabletop use is primarily stationary demonstration and development.
- Tabletop mode inhibits ordinary autonomous locomotion by default and provides edge/fall protection whenever movement could occur.
- Plausibly hazardous outputs have an immediately accessible stop or power cutoff and bounded failure behaviour.
- The droid can be assembled, started, demonstrated, inspected, and serviced from project documentation.

## V1 Candidate

- **Spatial/directional hearing:** include it only if a microphone and processing prototype proves that sound direction materially improves an approved interaction.

Core “come here” may initially use invocation detection followed by visual search; direct acoustic localization is not currently required.

### Uncommitted

Capabilities not listed as Core, Target, or Candidate are uncommitted. The project is not maintaining a permanent “never” list at this stage. Arms, manipulation, walking, self-balancing, spherical drive, full-house navigation, SLAM, biometric identity, broad assistant functionality, productionization, and large VLM features are not in the approved V1 plan, but they are not being evaluated as permanent exclusions.

## Approved Core scenarios

The detailed source is [core-interaction-scenarios.md](docs/00-foundation/core-interaction-scenarios.md).

### 1. Wake, socialize, and assist

1. M4 is stationary in an idle/head-down state.
2. A person calls “M4,” “M4K4,” or “Makad.”
3. M4 wakes as one coordinated performance: powered roll/pitch/yaw head rise and orientation, animated eyes, camera-side LED, astromech acknowledgement, face acquisition, and attentive gaze.
4. A natural greeting such as “Hi, how are you?” produces an in-character response using eyes, head movement, LED, chirps/beeps, and deliberate timing.
5. The person can request the time, set a timer, set an alarm, or request Spotify playback.
6. M4 confirms the request visibly and in character, performs it, and returns to an appropriate attentive or idle state.
7. During playback, M4 visually vibes to the music.

### 2. Come here and follow me

1. M4 begins on an approved indoor floor and may initially be looking elsewhere.
2. The person invokes M4 and says “come here.”
3. M4 acknowledges, searches for and acquires the person, turns toward them, approaches safely, and stops at the approved distance.
4. The person says “follow me.”
5. M4 follows the selected person through the approved route while maintaining distance and handling obstacles or temporary target loss.
6. When continuing safely is impossible, M4 stops and communicates the problem rather than moving blindly.
7. M4 performs an approved excited spin and settles back into an attentive state.

## Success definition

V1 succeeds when M4 delivers these interactions as a convincing, repeatable droid encounter on battery power—not as a sequence of manually rescued subsystem demos.

The approved validation categories include:

- recognizable droid identity;
- fluid onboard display expression;
- controlled roll/pitch/yaw head motion;
- coherent cross-channel timing;
- natural-language understanding;
- authored astromech communication;
- named wake and status-light behaviour;
- face acquisition, tracking, loss handling, and reacquisition;
- time, timer, alarm, and Spotify functions;
- safe floor movement, approach, following, obstacle handling, and expressive spin;
- tabletop movement inhibition and edge/fall protection;
- untethered battery operation;
- controlled stopping and bounded failure;
- physical robustness, serviceability, reproducible startup, and documented learning.

The exact numeric pass thresholds remain engineering work. They must be selected before final validation, not rewritten afterward to fit the result.

## Confirmed constraints

| Constraint | Current decision |
|---|---|
| V1 deadline | **5 December 2026** |
| Weekly project time | Approximately **60–80 hours** |
| Cost policy | No fixed ceiling yet; cost the complete architecture, prototypes, tools, sourcing, shipping, replacements, and contingency, then review substitutions/cuts before major procurement |
| Primary environment | Normal indoor floors |
| Interaction/following envelope | Single household room; interaction approximately 0.3–2.0 m, “come” from approximately 1–2 m, stop approximately 0.6–0.9 m away, follow up to approximately 3 m at no more than approximately 0.5 m/s |
| Tabletop environment | Large tables; stationary by default, with only explicitly enabled low-speed test/calibration movement inside a marked validated circular footprint |
| Final power | Onboard battery, untethered; initial mixed-duty runtime at least **20 minutes** |
| Cloud access | Reliable network/cloud may be assumed for Core connected features; no duplicate offline feature implementation is required |
| Recording | Allowed; active sensors/services must remain stoppable |
| Lighting baseline | Normal household lighting |
| Construction | Modular, screw-together, and serviceable |
| Fabrication | Several 3D printers available; exact machine/material chosen per part |
| Current electrical tools | Soldering, bench supply, multimeter, oscilloscope, and logic analyser are not yet established as available |
| External fabrication | Laser cutting, CNC, and machining access not yet confirmed |

Safety work is proportional to actual hazards rather than generic product-certification bureaucracy. Real risks—mobile contact, tabletop falls, pinch points, battery faults, heat, instability, and uncontrolled motion after a failure—must be addressed. Where harm or damage is plausible, safety overrides expression.

## Engineering principles

1. **Approved outcomes before architecture.** Design the system around the approved Core scenarios.
2. **Architecture before final parts.** Use candidate parts for risk prototypes, but close coupled mechanical, electrical, compute, perception, internal-communication, external-network, sourcing, timing, and thermal budgets before final component selection.
3. **Prototype risk before CAD freeze.** Test the uncertain mechanisms and perception/control loops before packaging hardens around them.
4. **Measure physics.** Torque, inertia, backlash, speed, stopping distance, stability, power, heat, latency, and failure timing need evidence rather than invented precision.
5. **Preserve coherent fallbacks.** Candidate features and implementation options need clean removal plans, but fallback paths must not quietly lower Core quality. Powered roll is Core and is not a fallback decision.
6. **Make failure explicit.** Ambiguity, target loss, service timeout, sensor failure, and low battery must produce named states and bounded behaviour.
7. **Keep character and control connected.** Expression is not a post-processing layer; timing and motion quality affect architecture and component choices.

The working sequence is:

**approved scenarios → approved system brief → prototype plan plus provisional budgets/trade studies → risk-prototype evidence → evidence-backed ADRs and system architecture → final component selection → BOM → integrated CAD → build and integration → validation**

## Current engineering phase

The foundation phase is complete. The project is now entering system architecture and risk reduction.

The approved architecture input is the [Makad V1 System Design Brief](docs/01-system/system-design-brief.md). The approved [Risk-Prototype Plan](docs/01-system/risk-prototype-plan.md) turns its seven risk questions into procedures, measurements, and evidence gates. The approved [workbench baseline](docs/01-system/workbench.md) defines the initial tool sourcing list and powered-test readiness gate; its purchases have not yet been completed, and prices/stock are rechecked at purchase time.

The architecture/prototype priority is deliberately weighted toward mechanical engineering, firmware, sourcing, and natural motion:

1. **Three-axis head mechanism and firmware:** powered roll/pitch/yaw load paths, torque, support, sensing, backlash, noise, wiring, control, and natural trajectories.
2. **Electrical/control backbone and peak power:** controller boundaries, stop/watchdog paths, rails, representative concurrent loads, brownout, and thermal behaviour.
3. **Mobile base:** drive trade study, low-speed quality, stability, braking, obstacles, tabletop edges, and expressive spin.
4. **Coordinated motion:** natural head–body–wheel composition, scheduling, interruption, feedback, and settling.
5. **Interaction pipeline:** invocation aliases, natural-language latency, cloud/service failure, timers/alarms, and cancellation behaviour.
6. **Physical layout and sourcing:** component availability, alternatives, cost, lead time, serviceability, camera/display/light/audio placement, and manufacturability.
7. **Tracking/following and remaining software integration:** person acquisition, selection, loss/reacquisition, bounded following, audio processing, display UI, and connected utilities.

Exact components and integrated CAD should not be frozen until these risks and budgets are sufficiently understood.

## Open engineering decisions

- final visual detailing, manufacturing tolerances, and total mass; current target proportions/dimensions live in the dimensional baseline;
- exact drive motors, transmissions, drivers, wheel/caster parts, skid construction, encoder parts, and control parameters;
- roll/pitch/yaw actuation, sensing, transmission, support, wiring, range, and control;
- camera, display, speaker, microphone, and status-light hardware;
- person localization, tracking, selection, loss, and reacquisition policy;
- final tolerances and pass criteria within the approved household interaction/following envelope;
- complete natural-language intent set and accepted phrasing;
- astromech vocabulary, grammar, synthesis, and behaviour pairings;
- display layouts for time, timer, alarm, and music;
- Spotify authentication and playback-control path;
- compute split, internal communication, and cloud/network degradation behaviour;
- charging method, regulation, low-battery state, and whether runtime should increase beyond the initial 20-minute requirement;
- exact tabletop test/calibration radius, speed, and mode selection;
- electrical-tool acquisition/borrowing plan;
- first complete sourced cost range and affordability review;
- quantitative success thresholds.

## Document authority

Use project documents in this order:

1. **Approved foundation documents** define the product identity, V1 scope, constraints, scenarios, and success conditions.
2. **Approved human-reviewed system and subsystem documents** define how the approved outcomes will be engineered; draft system documents guide work only after their status and open review decisions are checked, and they cannot silently change V1 scope.
3. **Approved component, material, and assembly records** define selections and physical implementation.
4. **BOM and procurement records** summarize selected items and sourcing status.
5. **CAD, software, and firmware** implement the approved decisions.
6. **README.md** provides the current orientation and must be corrected if it conflicts with an authority above it.
7. **MEMORY.md** is the append-only decision history explaining how the project changed.
8. **`specsheets/`** contains exploratory starting material and is non-binding unless a specific item is explicitly reviewed and adopted later.
9. **`visuals/`** contains inspiration and historical references, not frozen engineering truth.

No old requirement number, architecture, metric, or component becomes authoritative merely because it appears in a specification-style document.

## One-sentence definition

**M4K4-D is a rugged personal floor droid whose understanding, perception, animated face, astromech voice, expressive head and wheeled movement coordinate convincingly enough that M4 feels attentive, responsive, and alive.**
