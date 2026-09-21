# Makad / M4K4-D

> **Current project overview** — last reconciled **21 September 2026**
>
> Foundation approved: **14 August 2026** · V1 deadline: **5 December 2026**

**Makad**, technical designation **M4K4-D** and commonly shortened to **M4**, is a personal droid. M4 is intended to occupy the kind of companion role R2-D2 occupied for Luke Skywalker: recognizable, attentive, expressive, and full of character.

The central V1 priority is simple:

> **M4 should feel alive.**

Makad's defining advantage is expressiveness. That expression comes from what M4 understands, sees, and hears, and from how convincingly its display, status light, astromech audio, head, wheeled base, and timing communicate one intent.

`00-foundation` is the product-intent authority. Documents under `01-system` and `02-prototypes` are engineering reference. Design, sourcing, CAD, software, and hardware proceed together.

This README orients the repository around the current design, current build state, and immediate next work. [`MEMORY.md`](MEMORY.md) is a short chronological log of later consequential discoveries and decisions.

## Current design

M4 is a battery-powered floor droid with a three-axis head, an animated face, a camera-side status light, body-mounted hearing and speech, and a two-wheel base. The head carries the display, camera, status light, C2 motion controller, and local structure. The body carries four PDM microphones, the speaker, battery, and main compute. Floor mode is primary; tabletop mode inhibits locomotion by default.

The current physical target is **300 × 205 × 180 mm**, with Layout 03 producing a provisional **304 mm** neutral stack (140 mm body-top datum + 60 mm neck + 104 mm crown-inclusive head). Drive geometry is Ø84 mm wheels, 170 mm track, 110 mm axle-to-front-support, and a mandatory rear anti-tip skid. Front support is a Ø1″ ball transfer; a swivel caster remains a comparison article on the same mount.

Working geometry lives in [`docs/02-prototypes/RP-06-cad/`](docs/02-prototypes/RP-06-cad/README.md): head [Layout 03](docs/02-prototypes/RP-06-cad/head/layout-03/README.md) and body/chassis [Layout 02](docs/02-prototypes/RP-06-cad/body-chassis/layout-02/README.md).

### Selected components

| Item | Selection | Record |
|---|---|---|
| Face display | Waveshare ESP32-S3-LCD-4.3, **no-touch, SKU 30493** — 800×480 IPS with on-board ESP32-S3/LVGL renderer | [`display-candidate-study.md`](docs/01-system/display-candidate-study.md) |
| Head camera | Raspberry Pi Camera Module 3 **Wide**, visible-light, **SC0874** | [`camera-candidate-study.md`](docs/01-system/camera-candidate-study.md) |
| Head motion controller (C2) | Waveshare **ESP32-S3-Zero**, headerless; bench twin ESP32-S3-DevKitC-1-N8R8 | [`control-topology-options.md`](docs/01-system/control-topology-options.md) §6.3 |
| Main compute (C0) | **Raspberry Pi 5, 2 GB** with official Pi 5 Active Cooler; storage and power-entry implementation still open | [`compute-control architecture`](docs/02-prototypes/RP-02-electrical/compute-control-architecture.md) |
| Base controller (C3 prototype) | **Espressif ESP32-S3-DevKitC-1-N8**, selected over N8R8 to preserve GPIO35–37 | same, CA-03 |
| Control split | C0 owns semantic behaviour; D1 renders eyes; C2 owns head trajectory and local safety; C3 owns base loops and local hazards. Production links are differential UART; C2 relays face/light state locally | same |
| Drive topology | Two encoder wheels + **front ball transfer** + mandatory rear anti-tip skid | [`dimensional-baseline.md`](docs/01-system/dimensional-baseline.md) v1.12 |
| Head construction | PLA structure and skin (provisional beyond first head), real M2 button-heads, nine-step weathered finish | [`material-finish-mass-decision.md`](docs/02-prototypes/RP-01-head/material-finish-mass-decision.md) |
| Head layout | Serial body→yaw→pitch→roll; coaxial direct roll on a supported spindle; ears roll with the face; trapezoidal camera crown; external yaw cable loop; C2 on the rolling cradle; A0 balance target | [`head/decisions.md`](docs/02-prototypes/RP-06-cad/head/decisions.md) |

Still open: servos, battery, drive motors/drivers, production camera interconnect, harness/carriers, storage, audio SKUs, status-LED optic, and most power hardware. XC330-M288-T is a paper candidate (C01), not a selected servo.

## Current build state

The design is far ahead of the physical robot. Head and body CAD exist; electrical and locomotion behaviour are specified on paper; no integrated article has been built, weighed, or run.

| Area | State (2026-09-21) |
|---|---|
| Foundation | Approved. Some numeric thresholds remain open. |
| Geometry | Head Layout 03 is the 1:1 packaging direction (104 × 150 × 115 mm; ~499–524 g complete D/E tree, nominal 509 g). Body/chassis Layout 02 live-imports that head. Two retainer-screw collisions, hard-stop margin, pitch/roll stiffness, bearing SKU, balance trim, and CAD/firmware sign mapping are still open. Not a fabrication release. |
| Head mechanism | Concept A (elevated-ear serial gimbal) is the path. External rigid-body demand is calculated; nothing is weighed; actuator-internal inertia is not included. |
| Electrical / control | States, power topology, compute split, and C0↔C2 message/recovery design are written. Host codec work is exploratory. Pack sizing still needs drive measurements. |
| Locomotion | Two-wheel + ball + skid is the V1 type. Concept A chassis/sensing is retained; caster is the comparison swap. Motors, hubs, drivers, and sensors are not frozen. Layout 02 currently packages one guarded rear TCRT channel, which does not yet match the fuller stop-path sensing in the control design. |
| Interaction / following | Audio-path requirements and following architecture are documented. No SKU, corpus, or physical test. |
| Software / firmware | Timebase, link contract, C2/C3 firmware, and C0 behaviour are specified more than implemented. |
| Physical hardware | Selected display, camera, C2, Pi 5, and cooler are locked on paper. First weigh-ins wait on samples. No head, chassis, or electrical rig has been built. |

`visuals/` are provisional references; several show superseded details (mouths, ear microphones, yoke-mounted ears).

## Immediate next work

Sourcing, CAD, software, and hardware proceed together. The useful next work is:

- **Finish the current head CAD** so it can be printed: remove the two retainer-screw collisions; stiffen or verify the pitch frame and roll saddle; move hard stops beyond usable travel; select a bearing; add physical balance trim and explicit CAD/firmware sign mapping.
- **Choose and source remaining parts** as packaging needs them — head servos, wheels/hubs/motors, ball transfer, battery and power hardware, audio, status LED, connectors — and replace CAD envelopes with real geometry.
- **Keep the whole-robot model current** in RP-06: accept or recover the 4 mm stack over 300 mm; reconcile Layout 02's rear-only cliff channel with the base safety design.
- **Implement firmware and software** on the same timeline: C2/C3, C0 behaviour and perception, the serial link and timebase, and face rendering on the display.
- **Build and measure** as parts arrive: weigh display, camera, C2, prints, and finish coupons; print the head and chassis; stand up a protected bench and start moving hardware.

## Documents

### Product intent — authoritative

- [Vision](docs/00-foundation/vision.md)
- [V1 scope](docs/00-foundation/v1-scope.md)
- [Constraints](docs/00-foundation/constraints.md)
- [Success criteria](docs/00-foundation/success-criteria.md)
- [Core interaction scenarios](docs/00-foundation/core-interaction-scenarios.md)

### Current engineering

- [Dimensional and packaging baseline](docs/01-system/dimensional-baseline.md)
- Working CAD: [RP-06-cad](docs/02-prototypes/RP-06-cad/README.md) — [head Layout 03](docs/02-prototypes/RP-06-cad/head/layout-03/README.md), [body/chassis Layout 02](docs/02-prototypes/RP-06-cad/body-chassis/layout-02/README.md)
- Ledgers: [mass/envelope](docs/01-system/mass-envelope-ledger.md), [power/energy/thermal](docs/01-system/power-energy-ledger.md), [candidate sourcing](docs/01-system/candidate-sourcing-matrix.md)
- Studies: [control topology](docs/01-system/control-topology-options.md), [display](docs/01-system/display-candidate-study.md), [camera](docs/01-system/camera-candidate-study.md), [head harness](docs/01-system/head-harness-routing-study.md)

### Research and history

These folders are engineering reference. They do not set how work proceeds.

- [System design brief](docs/01-system/system-design-brief.md), [risk-prototype plan](docs/01-system/risk-prototype-plan.md), [workbench](docs/01-system/workbench.md), [run-record convention](docs/01-system/run-record-convention.md)
- Head: [`RP-01-head/`](docs/02-prototypes/RP-01-head/)
- Electrical: [`RP-02-electrical/`](docs/02-prototypes/RP-02-electrical/README.md)
- Locomotion: [`RP-03-locomotion/`](docs/02-prototypes/RP-03-locomotion/README.md)
- Coordination: [`RP-04-coordination/`](docs/02-prototypes/RP-04-coordination/README.md)
- Interaction: [`RP-05-interaction/`](docs/02-prototypes/RP-05-interaction/README.md)
- Following: [`RP-07-following/`](docs/02-prototypes/RP-07-following/README.md)
- Earlier memory log: [`archive/MEMORY-20260921.md`](archive/MEMORY-20260921.md)

## Repository

```
docs/00-foundation/     product intent and constraints     authoritative
docs/01-system/         engineering reference
docs/02-prototypes/     studies, calculations, and working CAD
docs/archive/           superseded documents
archive/                prior process log
MEMORY.md               chronological build and decision log
README.md               this orientation
```

## Identity and design direction

M4 is a droid, not a desktop assistant, smart speaker, or generic social robot. The approved direction is:

- strongly inspired by Star Wars droids;
- cyberpunk, rugged, scrappy, and characterful;
- mechanical rather than glossy or appliance-like;
- modular and screw-together, with visible fasteners, panels, seams, and service access as part of the personality;
- eyes only on the face, no mouth;
- approachable without optimizing for minimum size;
- open to substantial redesign from the current renders.

## V1 Core

V1 is not complete unless the following outcomes work together as one droid. Exact wording lives in [`v1-scope.md`](docs/00-foundation/v1-scope.md) (SCOPE-01…21).

**Expression and character** — animated face on the onboard display; powered roll, pitch and yaw head motion; at least one controllable LED beside the camera; a builder-authored non-English astromech language; idle aliveness without manual control; display, LED, audio, head, base and timing express one intent; at least one bounded excited spin.

**Understanding and perception** — natural spoken interaction within the approved scenarios; invocation forms **"M4," "M4K4," and "Makad"**; visual acquisition of a nearby person or face; tracking maintained or reacquired through later-defined test cases.

**Mobility and following** — battery-powered wheeled floor droid; "come here" finds, approaches and stops at a bounded distance; "follow me" tracks the selected person through an approved indoor route; obstacles, stopping, target loss and unsafe conditions are handled without continuing blindly.

**Utility and entertainment** — display the time; create and signal timers and alarms; start Spotify playback through an approved integration; eyes "vibe" to music.

**Operation and construction** — untethered on onboard battery for at least 20 minutes; floor mode primary; tabletop mode inhibits locomotion by default and protects edges; accessible stop or cutoff with bounded failure; assembled, started, demonstrated, inspected and serviced from documentation.

**Candidate:** spatial/directional hearing, included only if it materially improves an approved interaction. Everything else is uncommitted; there is no permanent "never" list.

## Approved Core scenarios

Source: [`core-interaction-scenarios.md`](docs/00-foundation/core-interaction-scenarios.md).

**1. Wake, socialize, assist.** M4 idles head-down. A person calls its name. M4 wakes as one coordinated performance: three-axis head rise, eyes, camera-side LED, astromech acknowledgement, face acquisition and gaze. A greeting produces an in-character response. The person can request the time, a timer, an alarm, or Spotify playback; M4 confirms visibly, performs it, and vibes during music.

**2. Come here and follow me.** On an approved floor, the person invokes M4 and says "come here." M4 acknowledges, searches, acquires, turns, approaches safely and stops approximately 0.6–0.9 m away. "Follow me" makes M4 follow through an approved route of up to about 3 m at no more than about 0.5 m/s while handling obstacles and target loss. When continuing is unsafe, M4 stops and says so. M4 performs an excited spin and settles.

## Success definition

V1 succeeds when M4 delivers these interactions as a convincing, repeatable droid encounter on battery power, not as a sequence of manually rescued subsystem demos. The validation categories and open thresholds are in [`success-criteria.md`](docs/00-foundation/success-criteria.md) (SC-01…25).
