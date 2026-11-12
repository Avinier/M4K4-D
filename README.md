# Makad / M4K4-D

> **Current project overview**: last reconciled **12 November 2026**
>
> Foundation approved: **14 August 2026** · V1 deadline: **5 December 2026**

**Makad**, technical designation **M4K4-D** and commonly shortened to **M4**, is a personal droid. M4 is intended to occupy the kind of companion role R2-D2 occupied for Luke Skywalker: recognizable, attentive, expressive, and full of character.

The central V1 priority is simple:

> **M4 should feel alive.**

Makad's defining advantage is expressiveness. That expression comes from what M4 understands, sees, and hears, and from how convincingly its display, status light, astromech audio, head, wheeled base, and timing communicate one intent.

## Authority

- [`project/00-foundation`](project/00-foundation/) is the product-intent authority.
- [`project/03-build`](project/03-build/README.md) governs every engineering decision, part selection, BOM change and CAD edit from 2026-09-28. Its ledger is [`decisions.md`](project/03-build/decisions.md) and its parts register is [`BOM.csv`](project/03-build/BOM.csv).
- [`project/01-system`](project/01-system/) and [`project/02-prototypes`](project/02-prototypes/) are read-only engineering reference. Where they disagree with `03-build`, `03-build` wins.

[`MEMORY.md`](MEMORY.md) is a short chronological log of the project's turning points.

## Current design

M4 is a battery-powered floor droid with a three-axis head, an animated face, a camera-side status light, body-mounted hearing and speech, and a two-wheel base. The head carries the display, camera, status light and C2 motion controller. The body carries the yaw stage, four I²S microphones, the speaker, main compute and the bought power modules; the chassis carries the battery, drive and floor sensors. Floor mode is primary; tabletop mode inhibits locomotion by default.

Drive geometry is Ø84 mm wheels on a ~170 mm track with a front ball caster and a mandatory rear anti-tip keel ([dimensional baseline](project/01-system/dimensional-baseline.md) v1.15). The whole robot is modelled in [`project/03-build/final/v1`](project/03-build/final/v1/README.md); subsystem CAD lives in [01-chassis](project/03-build/01-chassis/), [02-body](project/03-build/02-body/) and [03-head](project/03-build/03-head/).

### Selected components

States follow the [BOM](project/03-build/BOM.csv): selected parts are settled but not yet measured or bench-proven.

| Item | Selection | Record |
|---|---|---|
| Face display | Waveshare ESP32-S3-LCD-4.3, **no-touch, SKU 30493**: 800×480 IPS with on-board ESP32-S3/LVGL renderer | [display study](project/01-system/display-candidate-study.md) |
| Head camera | Raspberry Pi Camera Module 3 **Wide**, **SC0874**; ribbon crosses pitch and roll in a free loop behind the head | [D-105](project/03-build/decisions.md#d-105) |
| Main compute (C0) | **Raspberry Pi 5, 2 GB** with the official Active Cooler, on PCB-09 (2 × RS-422 link adapter) | [D-048](project/03-build/decisions.md#d-048), [04-pcbs](project/03-build/04-pcbs/README.md) |
| Head motion controller (C2) | Waveshare **ESP32-S3-Zero** on the custom PCB-12 carrier | [D-102](project/03-build/decisions.md#d-102) |
| Base controller (C3) | Espressif **ESP32-S3-DevKitC-1 v1.1** on the custom PCB-10 carrier | [04-pcbs](project/03-build/04-pcbs/README.md) |
| Head actuators | Yaw: **Waveshare ST3215-HS** at 11.1 V. Pitch and roll: **Feetech STS3045M** at 6.3 V. Candidates until bench tests B1–B6 | [D-046](project/03-build/decisions.md#d-046)–[D-049](project/03-build/decisions.md#d-049) |
| Drive | **ThinkRobotics MOT3001-6V230RPM** encoder gearmotors (received), two DRV8833 carriers, printed PETG/TPU wheels, Pololu #2691 ball caster | [D-003](project/03-build/decisions.md#d-003) |
| Battery | **2S1P Samsung INR18650-25R** (7.2 V, 18 Wh) with a bought TIFPS0629 protection board and copper ballast; charged off-board (ISDT PD60) | [D-093](project/03-build/decisions.md#d-093) |
| Power | Pololu #2813 pushbutton switch, two S18V20ALV servo rails, two S13V30F5 5 V rails, INA226 monitor | [D-094](project/03-build/decisions.md#d-094), [module selection](project/03-build/module-selection.md) |
| Audio and IMU | Visaton K 50 WP speaker, MAX98357A amp, 4 × INMP441 mics, Adafruit LSM6DSOX base IMU | [D-094](project/03-build/decisions.md#d-094) |
| Control split | C0 owns semantic behaviour; D1 renders eyes; C2 owns head trajectory and local safety; C3 owns base loops and local hazards. Links are differential UART; C2 relays face/light state locally | [control topology](project/01-system/control-topology-options.md) |

## Current build state

The design is ahead of the physical robot. The whole-robot CAD is integrated and checked; first parts have arrived; nothing is printed, wired or running.

| Area | State (2026-11-12) |
|---|---|
| CAD | Chassis, body and head v1 are integrated in `final/v1` with targeted checks. Tipping margin a_tip 1.670 neutral / 1.646 worst pose against 1.582 ([D-095](project/03-build/decisions.md#d-095)); camera-loop ballast keeps the worst-yaw margin above 1.5% ([D-105](project/03-build/decisions.md#d-105)). Not yet a fabrication release for body and head. |
| Electrical | D-093 replaced the custom power boards with bought modules. The [harness](project/03-build/05-harness/README.md) topology is drawn but on **electrical HOLD** ([D-096](project/03-build/decisions.md#d-096)). Custom boards: PCB-09 rev B routed; PCB-10/11/15 rev A; PCB-08/12/14/16 rev A drafts, not ordered. |
| Procurement | Modules and small parts ordered 2026-11-08; deliveries logged in [BOM-deliveries.md](project/03-build/BOM-deliveries.md). Open actions in [TODO.md](project/03-build/TODO.md). |
| Printing | Chassis print package exported to [04-print](project/04-print/README.md); body and head prints not started. |
| Software / firmware | [Firmware requirements](project/03-build/04-software/firmware-requirements.md) recorded; timebase, link contract and behaviour are specified more than implemented. |
| Physical tests | None run. Bench register N1–N12 and actuator tests B1–B6 are open. |

`visuals/` are provisional references; several show superseded details (mouths, ear microphones, yoke-mounted ears).

## Immediate next work

- **Receive and measure** the ordered parts; record them in the BOM and correct dependent CAD.
- **Run the bench tests**: power switch, servo and 5 V rails (N1–N12), Feetech actuators (B1–B6), pack protection acceptance.
- **Clear the harness HOLD** from measured peaks, then build and test the harness.
- **Finish the custom boards** (PCB-08, 12, 14, 16) and order all of them together.
- **Print and assemble the chassis**, then body and head, through [04-print](project/04-print/README.md).
- **Implement firmware and software** on the same timeline: C2/C3, C0 behaviour and perception, the serial link and face rendering.

## Documents

### Product intent: authoritative

- [Vision](project/00-foundation/vision.md)
- [V1 scope](project/00-foundation/v1-scope.md)
- [Constraints](project/00-foundation/constraints.md)
- [Success criteria](project/00-foundation/success-criteria.md)
- [Core interaction scenarios](project/00-foundation/core-interaction-scenarios.md)

### Build: governing

- [03-build overview](project/03-build/README.md): status, file map and build rules
- [Decisions ledger](project/03-build/decisions.md), [BOM](project/03-build/BOM.csv), [simplification plan](project/03-build/simplification-plan.md)
- [Whole robot (final v1)](project/03-build/final/v1/README.md) and its [print guide](project/03-build/final/v1/printguide.md)
- [Custom PCBs](project/03-build/04-pcbs/README.md), [harness](project/03-build/05-harness/README.md)
- [Printing](project/04-print/README.md)

### Engineering reference (read-only)

- [Dimensional and packaging baseline](project/01-system/dimensional-baseline.md)
- Ledgers: [mass/envelope](project/01-system/mass-envelope-ledger.md), [power/energy/thermal](project/01-system/power-energy-ledger.md), [candidate sourcing](project/01-system/candidate-sourcing-matrix.md)
- Studies: [control topology](project/01-system/control-topology-options.md), [display](project/01-system/display-candidate-study.md), [camera](project/01-system/camera-candidate-study.md), [head harness](project/01-system/head-harness-routing-study.md), [timebase](project/01-system/timebase.md)
- [System design brief](project/01-system/system-design-brief.md), [risk-prototype plan](project/01-system/risk-prototype-plan.md), [workbench](project/01-system/workbench.md), [run-record convention](project/01-system/run-record-convention.md)
- Risk prototypes: [head](project/02-prototypes/RP-01-head/), [electrical](project/02-prototypes/RP-02-electrical/README.md), [locomotion](project/02-prototypes/RP-03-locomotion/README.md), [coordination](project/02-prototypes/RP-04-coordination/README.md), [interaction](project/02-prototypes/RP-05-interaction/README.md), [CAD layouts](project/02-prototypes/RP-06-cad/README.md), [following](project/02-prototypes/RP-07-following/README.md)
- Earlier memory logs: [`archive/`](archive/)

## Repository

```
project/00-foundation/   product intent and constraints      authoritative
project/01-system/       system studies and ledgers          reference
project/02-prototypes/   risk prototypes and early CAD       reference
project/03-build/        decisions, BOM, CAD, PCBs, harness  governs
project/04-print/        print lab, workflow, STL exports
visuals/                 provisional renders
archive/                 earlier memory logs
MEMORY.md                chronological log of turning points
README.md                this orientation
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

V1 is not complete unless the following outcomes work together as one droid. Exact wording lives in [`v1-scope.md`](project/00-foundation/v1-scope.md) (SCOPE-01…21).

**Expression and character** — animated face on the onboard display; powered roll, pitch and yaw head motion; at least one controllable LED beside the camera; a builder-authored non-English astromech language; idle aliveness without manual control; display, LED, audio, head, base and timing express one intent; at least one bounded excited spin.

**Understanding and perception** — natural spoken interaction within the approved scenarios; invocation forms **"M4," "M4K4," and "Makad"**; visual acquisition of a nearby person or face; tracking maintained or reacquired through later-defined test cases.

**Mobility and following** — battery-powered wheeled floor droid; "come here" finds, approaches and stops at a bounded distance; "follow me" tracks the selected person through an approved indoor route; obstacles, stopping, target loss and unsafe conditions are handled without continuing blindly.

**Utility and entertainment** — display the time; create and signal timers and alarms; start Spotify playback through an approved integration; eyes "vibe" to music.

**Operation and construction** — untethered on onboard battery for at least 20 minutes; floor mode primary; tabletop mode inhibits locomotion by default and protects edges; accessible stop or cutoff with bounded failure; assembled, started, demonstrated, inspected and serviced from documentation.

**Candidate:** spatial/directional hearing, included only if it materially improves an approved interaction. Everything else is uncommitted; there is no permanent "never" list.

## Approved Core scenarios

Source: [`core-interaction-scenarios.md`](project/00-foundation/core-interaction-scenarios.md).

**1. Wake, socialize, assist.** M4 idles head-down. A person calls its name. M4 wakes as one coordinated performance: three-axis head rise, eyes, camera-side LED, astromech acknowledgement, face acquisition and gaze. A greeting produces an in-character response. The person can request the time, a timer, an alarm, or Spotify playback; M4 confirms visibly, performs it, and vibes during music.

**2. Come here and follow me.** On an approved floor, the person invokes M4 and says "come here." M4 acknowledges, searches, acquires, turns, approaches safely and stops approximately 0.6–0.9 m away. "Follow me" makes M4 follow through an approved route of up to about 3 m at no more than about 0.5 m/s while handling obstacles and target loss. When continuing is unsafe, M4 stops and says so. M4 performs an excited spin and settles.

## Success definition

V1 succeeds when M4 delivers these interactions as a convincing, repeatable droid encounter on battery power, not as a sequence of manually rescued subsystem demos. The validation categories and open thresholds are in [`success-criteria.md`](project/00-foundation/success-criteria.md) (SC-01…25).
