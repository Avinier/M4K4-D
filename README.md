# Makad / M4K4-D

> **Current project overview** — last reconciled **8 September 2026**
>
> Foundation approved: **14 August 2026** · V1 deadline: **5 December 2026** · Roadmap position: **Stage 0/1 — RP-01 head preparation**

**Makad**, technical designation **M4K4-D** and commonly shortened to **M4**, is a personal droid. M4 is intended to occupy the kind of companion role R2-D2 occupied for Luke Skywalker: recognizable, attentive, expressive, and full of character.

The central V1 priority is simple:

> **M4 should feel alive.**

Makad's defining advantage is expressiveness. That expression comes from what M4 understands, sees, and hears, and from how convincingly its display, status light, astromech audio, head, wheeled base, and timing communicate one intent.

This README is the orientation document over the whole repository. It states current truth and links to the documents that own it. [`MEMORY.md`](MEMORY.md) records how that truth changed over time.

## Where the project stands

| Area | Status (2026-09-08) |
|---|---|
| Foundation (vision, scope, constraints, success criteria, scenarios) | Approved. Numeric `SC-TBD`/`CON-TBD` thresholds remain open by design. |
| System design brief | Approved v1.3. Thirteen ADRs defined, none closed. |
| Risk-prototype plan | Approved v1.9. Seven prototypes; **no run has been executed.** |
| Workbench / Stage 0 | Approved; first tools selected and partly ordered. Tool access, E-stop verification, logging schema, monotonic timebase and video sync are still open, so **powered scored testing is blocked.** |
| Run identity | Convention v1.0 active. Guarded launcher not built. |
| Dimensional baseline | v1.8 active: 300 × 205 × 180 mm robot, 95 × 150 × 115 mm nominal head, Ø84 wheels, 170 mm track, 110 mm axle-to-caster, 60 mm neck. |
| Selected components | Display, camera and C2 motion-controller module locked (see below). Servos, SBC, battery, drive motors, harness: open. |
| RP-01 three-axis head | Intent, storyboard and physics framework authored. Concept A credible; Concept B not yet authored. Gates unregistered. Rig not built. First packaging study (`layout-01`) exists. |
| Head mass | Planning lower bound ~490 g at 1.2 mm PLA **before** the C2 assembly; nothing weighed yet. The earlier 250 g target and its inertia/torque proxies are inadmissible. |
| Architecture, budgets, BOM, integrated CAD | Not started; blocked on prototype evidence by design. |
| `specsheets/` | Exploratory, non-binding. |
| `visuals/` | Provisional references; several show superseded details (mouths, ear microphones, yoke-mounted ears). |

### Selected and locked

| Item | Selection | Governing record |
|---|---|---|
| Face display | Waveshare ESP32-S3-LCD-4.3, **no-touch, SKU 30493** — 800×480 IPS with on-board ESP32-S3/LVGL renderer | [`display-candidate-study.md`](docs/01-system/display-candidate-study.md) |
| Head camera | Raspberry Pi Camera Module 3 **Wide**, visible-light, **SC0874** | [`camera-candidate-study.md`](docs/01-system/camera-candidate-study.md) |
| Head motion controller (C2) | Waveshare **ESP32-S3-Zero**, headerless; bench twin ESP32-S3-DevKitC-1-N8R8 | [`control-topology-options.md`](docs/01-system/control-topology-options.md) §6.3 |
| Control split | Body Linux SBC owns behaviour; display ESP32-S3 renders eyes; C2 ESP32-S3 owns trajectories, servo bus, limits, watchdog, E-stop | [`RP-01 decision.md`](docs/02-prototypes/RP-01-head/decision.md) CTRL-01…06 |
| Drive topology | Two encoder wheels + front caster + mandatory rear anti-tip skid | [`dimensional-baseline.md`](docs/01-system/dimensional-baseline.md) |
| RP-01 material and finish | PLA structure and skin (provisional beyond RP-01), real M2 button-heads, nine-step weathered finish | [`material-finish-mass-decision.md`](docs/02-prototypes/RP-01-head/material-finish-mass-decision.md) D-01…08 |
| First head layout choices | Serial body→yaw→pitch→roll; coaxial direct roll on a supported spindle; ears roll with the face; trapezoidal camera crown; external yaw cable loop; C2 on the rolling cradle; A0 balance target | [`cad/head/decisions.md`](docs/02-prototypes/RP-01-head/cad/head/decisions.md) HEAD-CAD-01…07 |

Each lock reopens only through the change-control rule in its governing record.

### Immediate next work

Ordered by the risk-prototype plan's open-inputs list and the intuition guide:

1. **Per-axis mass tree and A0 coordinates** from `layout-01`, replacing the 35 g actuator allowance with real housings and making M008 explicit.
2. **Concept B** for the mechanism comparison (the parallel pitch/roll alternative is the named candidate).
3. **Torque, RMS and modal screen** per axis from the mass tree, then a servo family shortlist.
4. **Register RP-01 gates** (thresholds frozen before any scored run).
5. **Stage 0 closure:** verify tools and E-stop, implement the logging schema, monotonic timebase and video-sync method, and the run generator/guarded launcher. This is software work and should not wait on hardware.
6. **First weigh-ins** when the display and camera samples arrive (M001, M004, finish coupon).

## Documents

### Approved foundation

- [Vision](docs/00-foundation/vision.md)
- [V1 scope](docs/00-foundation/v1-scope.md)
- [Constraints](docs/00-foundation/constraints.md)
- [Success criteria](docs/00-foundation/success-criteria.md)
- [Core interaction scenarios](docs/00-foundation/core-interaction-scenarios.md)

### System engineering

- [Engineering intuition guide (method, all phases)](docs/intuition.md)
- [System design brief](docs/01-system/system-design-brief.md)
- [Risk-prototype plan](docs/01-system/risk-prototype-plan.md)
- [Workbench and test-readiness baseline](docs/01-system/workbench.md)
- [Run-record convention](docs/01-system/run-record-convention.md) and [run-record template](docs/02-prototypes/_templates/run-record.md)
- [Dimensional and packaging baseline](docs/01-system/dimensional-baseline.md)
- Living ledgers: [mass/envelope](docs/01-system/mass-envelope-ledger.md), [candidate sourcing matrix](docs/01-system/candidate-sourcing-matrix.md)
- Studies: [control topology](docs/01-system/control-topology-options.md), [display](docs/01-system/display-candidate-study.md), [display shopping brief](docs/01-system/display-shopping-brief.md), [camera](docs/01-system/camera-candidate-study.md), [head harness routing](docs/01-system/head-harness-routing-study.md)

### RP-01 — three-axis head

Folder: [`docs/02-prototypes/RP-01-head/`](docs/02-prototypes/RP-01-head/)

- [Intent](docs/02-prototypes/RP-01-head/intent.md) — authored head vocabulary (HM-00…HM-18) with eye/audio placeholders
- [Storyboard](docs/02-prototypes/RP-01-head/storyboard.md) — keyframes, profile laws (`MJ5`, `MS7`, `TRACK`, `BRAKE`), per-axis peak speed/acceleration, hysteresis and modal targets
- [Physics](docs/02-prototypes/RP-01-head/physics.md), [gates](docs/02-prototypes/RP-01-head/gates.md), [rig](docs/02-prototypes/RP-01-head/rig.md), [decision](docs/02-prototypes/RP-01-head/decision.md)
- [Material/finish/mass decision](docs/02-prototypes/RP-01-head/material-finish-mass-decision.md) and [payload mass capture](docs/02-prototypes/RP-01-head/payload-mass-capture.md)
- Concepts: [comparison](docs/02-prototypes/RP-01-head/concepts/comparison.md), [Concept A](docs/02-prototypes/RP-01-head/concepts/elevated-ear-pivot-serial-gimbal.md), [servo mechanism recommendation](docs/02-prototypes/RP-01-head/concepts/servo-mechanism-recommendation.md)
- CAD: [entry point](docs/02-prototypes/RP-01-head/cad/README.md), [decisions](docs/02-prototypes/RP-01-head/cad/head/decisions.md), [requirements](docs/02-prototypes/RP-01-head/cad/head/requirements.md), [packaging estimates](docs/02-prototypes/RP-01-head/cad/head/packaging-estimates.md), [pre-layout brief](docs/02-prototypes/RP-01-head/cad/head/pre-layout-brief.md), [layout-01 study](docs/02-prototypes/RP-01-head/cad/head/layout-01/brief.md)

Root `cad/`, `docs/03-architecture/` and `docs/04-bom/` are reserved for later stages and must stay empty until then.

## Repository layers

```
docs/00-foundation/     WHAT M4 must be              approved, the test oracle
docs/01-system/         HOW we will find out          approved instruments and living ledgers
docs/02-prototypes/     EVIDENCE                      RP-XX folders, runs, decisions
docs/03-architecture/   COMMITMENTS                   ADRs, budgets, interfaces   (stage 6, empty)
docs/04-bom/            PURCHASES                     final selection, sourcing   (stage 7, empty)
cad/                    GEOMETRY                      integrated CAD, frozen last (stage 7, empty)
docs/archive/           superseded verbatim documents
MEMORY.md               append-only history of how every decision changed
README.md               this orientation
```

Information flows down; citations flow up; nothing skips a layer. A part is never bought because a prototype "showed it works"; it passes through an ADR first.

## Physical prototype run records

Every bounded physical execution that energizes an actuator, applies representative load, or produces decision evidence receives one permanent run ID:

```text
RP<prototype>-<gate-and-version-or-EXP>-<exploratory|pilot|scored>-<UTC allocation>-<sequence>
```

IDs are allocated before the run and never renamed, reused or deleted; failed and aborted runs keep their evidence. The operating invariant is:

> **No valid run ID plus no confirmed logger means no actuator enable.**

Until a guarded launcher enforces this, the builder applies it as a pre-arm bench check from the [run-record template](docs/02-prototypes/_templates/run-record.md). Detail is in the [run-record convention](docs/01-system/run-record-convention.md).

## Identity and design direction

M4 is a droid, not a desktop assistant, smart speaker, or generic social robot. The approved direction is:

- strongly inspired by Star Wars droids;
- cyberpunk, rugged, scrappy, and characterful;
- mechanical rather than glossy or appliance-like;
- modular and screw-together, with visible fasteners, panels, seams, and service access as part of the personality;
- eyes only on the face, no mouth;
- approachable without optimizing for minimum size;
- open to substantial redesign from the current renders.

Face geometry, shell language, colours, tolerances, total mass and internal architecture remain subject to prototype and packaging validation. Four PDM microphones, the speaker, battery and main compute are body-mounted; the head carries only the display, camera, status light, C2 controller and local structure.

## V1 Core

V1 is not complete unless the following outcomes work together as one droid. Exact wording lives in [`v1-scope.md`](docs/00-foundation/v1-scope.md) (SCOPE-01…21).

**Expression and character** — animated face on the onboard display; powered roll, pitch and yaw head motion; at least one controllable LED beside the camera; a builder-authored non-English astromech language; idle aliveness without manual control; display, LED, audio, head, base and timing express one intent; at least one bounded excited spin.

**Understanding and perception** — natural spoken interaction within the approved scenarios; invocation forms **"M4," "M4K4," and "Makad"**; visual acquisition of a nearby person or face; tracking maintained or reacquired through later-defined test cases.

**Mobility and following** — battery-powered wheeled floor droid; "come here" finds, approaches and stops at a bounded distance; "follow me" tracks the selected person through an approved indoor route; obstacles, stopping, target loss and unsafe conditions are handled without continuing blindly.

**Utility and entertainment** — display the time; create and signal timers and alarms; start Spotify playback through an approved integration; eyes "vibe" to music.

**Operation and construction** — untethered on onboard battery for at least 20 minutes; floor mode primary; tabletop mode inhibits locomotion by default and protects edges; accessible stop or cutoff with bounded failure; assembled, started, demonstrated, inspected and serviced from documentation.

**Candidate:** spatial/directional hearing, included only if a prototype proves sound direction materially improves an approved interaction. Everything else is uncommitted; there is no permanent "never" list.

## Approved Core scenarios

Source: [`core-interaction-scenarios.md`](docs/00-foundation/core-interaction-scenarios.md).

**1. Wake, socialize, assist.** M4 idles head-down. A person calls its name. M4 wakes as one coordinated performance: three-axis head rise, eyes, camera-side LED, astromech acknowledgement, face acquisition and gaze. A greeting produces an in-character response. The person can request the time, a timer, an alarm, or Spotify playback; M4 confirms visibly, performs it, and vibes during music.

**2. Come here and follow me.** On an approved floor, the person invokes M4 and says "come here." M4 acknowledges, searches, acquires, turns, approaches safely and stops approximately 0.6–0.9 m away. "Follow me" makes M4 follow through an approved route of up to about 3 m at no more than about 0.5 m/s while handling obstacles and target loss. When continuing is unsafe, M4 stops and says so. M4 performs an excited spin and settles.

## Success definition

V1 succeeds when M4 delivers these interactions as a convincing, repeatable droid encounter on battery power, not as a sequence of manually rescued subsystem demos. The validation categories and open thresholds are in [`success-criteria.md`](docs/00-foundation/success-criteria.md) (SC-01…25). Thresholds are selected before final validation and never rewritten afterward to fit the result.
