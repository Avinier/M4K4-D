# Makad V1 Scope

| Field | Value |
|---|---|
| Status | Approved |
| Version | 1.1 |
| Owner | Project builder |
| Last reviewed | 2026-08-14 |
| Depends on | `vision.md` |

## Scope rule

V1 is the first integrated version of Makad that delivers the approved droid experience within the four-month project window. It is not an exercise in minimizing physical size, cost, or capability. Size, mass, and expenditure may increase when the improvement is justified by expressiveness, reliability, fabrication practicality, or learning value.

This document defines outcomes. Mechanisms, dimensions, architectures, and exact components remain later engineering decisions unless explicitly stated.

The scope labels mean:

- **Core** — V1 is not complete without it.
- **Target** — actively design and prototype toward it, but it may be cut without invalidating V1.
- **Candidate** — evaluate only after the Core path is credible; inclusion requires evidence and schedule capacity.
- **Uncommitted** — not part of the current plan and not permanently rejected.

## Core V1 outcomes

| ID | Outcome | What counts at scope level |
|---|---|---|
| SCOPE-01 | Droid identity | Makad presents a consistent M4K4-D visual, audio, and behavioural character informed by the approved vision. |
| SCOPE-02 | High-quality display expression | An onboard display presents a continuously animated default face with convincing idle and reactive expression, and can temporarily present approved utility information. Exact display and rendering implementation remain open. |
| SCOPE-03 | Three-axis expressive head | The physical head provides powered roll, pitch, and yaw. All three axes contribute to authored attention and expression, and their trajectories coordinate with display and body motion. Exact mechanism and ranges remain engineering decisions. |
| SCOPE-04 | Person/face tracking | Makad can visually acquire a nearby person/face, direct attention toward them, and maintain or reacquire that attention as they move within the approved environment. |
| SCOPE-05 | Natural-language understanding | Makad accepts natural spoken interaction with sufficient latency and reliability for the approved scenarios. It is not limited to rigid button input or a tiny command grammar. |
| SCOPE-06 | Astromech communication | Makad responds through a custom non-English astromech-style language authored by the builder, using coordinated droid sounds and behaviour. Ordinary English speech output is not a V1 requirement. |
| SCOPE-07 | Idle aliveness | When powered but not engaged, Makad shows bounded, non-repetitive signs of life without manual control. |
| SCOPE-08 | Integrated behaviour | At least three recognizable authored behaviours across the approved scenarios coordinate perception, display, sound, head motion, timing, and available base motion as one action. |
| SCOPE-09 | Wheeled locomotion | Makad moves using a powered wheeled base. Exact drive architecture is deliberately deferred to system engineering. |
| SCOPE-10 | Floor operation | The primary locomotion environment is a normal indoor floor. Makad can perform the approved movement scenarios without uncontrolled contact or instability. |
| SCOPE-11 | Tabletop protection | Makad can be placed on a large tabletop for mostly stationary demonstrations. Tabletop mode inhibits ordinary locomotion by default and includes edge/fall protection for any permitted movement or unintended activation. |
| SCOPE-12 | Collision avoidance and bounded contact | Makad detects relevant obstacles and stops or redirects before harmful contact in the approved operating envelope. “Collision-proof” is treated as a design goal, not an absolute guarantee. |
| SCOPE-13 | Battery operation | The final integrated droid operates untethered from an onboard battery for its approved demonstration and runtime. USB or bench power remains acceptable during development. |
| SCOPE-14 | Controlled failure and stop | Plausibly hazardous outputs have a clear stop/power cutoff, bounded motion, and predictable failure behaviour. |
| SCOPE-15 | Repeatable build | The physical and software system can be assembled, started, demonstrated, and serviced using project documentation. |
| SCOPE-16 | Named wake interaction | From an idle/head-down state, Makad recognizes the approved name forms “M4,” “M4K4,” and “Makad,” then performs a coordinated wake response. Exact wake-word technology remains open. |
| SCOPE-17 | Camera-side status light | At least one controllable LED beside the head camera participates in wake, attention, and status behaviours. Exact colour, optics, and animation remain open. |
| SCOPE-18 | Core utility interactions | Through natural language, Makad can display the current time, create a timer, and create an alarm. Detailed intent coverage and GUI design are deferred. |
| SCOPE-19 | Music interaction | Makad can start requested Spotify playback through an approved connected integration and expressively “vibe” during playback using at least its eyes. Exact musical synchronization remains open. |
| SCOPE-20 | Come and follow | On the floor, Makad can respond to “come here” by finding and approaching the speaker/person, and to “follow me” by following them through the approved indoor test environment while applying obstacle and distance constraints. |
| SCOPE-21 | Expressive base gesture | Makad can perform at least one bounded excited spin as a deliberate character action inside its validated floor-motion envelope. |

## V1 Targets

No V1 Targets are currently approved. Powered neck roll was promoted to the Core three-axis expressive-head requirement in version 1.1.

## V1 Candidates

| ID | Capability | Inclusion gate |
|---|---|---|
| CAND-01 | Spatial/directional hearing | A microphone and processing prototype proves that sound direction materially improves an approved interaction. |

Cloud-backed natural-language understanding and the approved time/timer/alarm/Spotify interactions are part of Core. Spatial hearing is distinct from ordinary microphone capture and remains a Candidate; “come here” may initially use wake detection followed by visual search rather than direct acoustic localization.

## Explicit output-language decision

Makad may understand natural human speech, including English, but its character output is an authored astromech language rather than ordinary spoken English. The language vocabulary, acoustic grammar, meanings, and behaviour pairings will be designed by the builder.

Temporary diagnostic audio, development prompts, or an external debug interface do not redefine Makad's in-character voice.

## Operating modes

### Floor mode

- Primary mode for locomotion.
- Allows only the movement envelope validated for indoor floors.
- Obstacle detection, stopping, stability, and recovery behaviour are active.

### Tabletop mode

- Intended mainly for stationary demonstrations and development.
- Ordinary autonomous locomotion is inhibited by default.
- Any deliberately enabled test/calibration movement remains low-speed and inside a marked, separately validated circular footprint around the robot.
- Come/follow behaviour and the excited spin are not permitted in tabletop mode.
- Edge/fall detection remains active whenever motion could occur.

The method used to select or verify operating mode is an architecture decision still to be made.

## Uncommitted capabilities

There is currently no permanent “outside V1 forever” list. Arms, manipulation, walking, self-balancing, spherical drive, full-house navigation, SLAM, biometric identity, broad assistant functions, productionization, and large VLM features are **not in the approved V1 plan**, but this foundation does not evaluate or reject their value for later versions.

## Scope-change rule

A capability moves among **Core**, **Target**, **Candidate**, and **Uncommitted** only through a human-reviewed edit to this document and a corresponding decision entry in `MEMORY.md`. A detailed specsheet cannot promote itself into V1 scope.

Targets and Candidates must have time boxes, evidence gates, and clean removal/fallback plans. Cutting one must leave a coherent droid rather than a visibly broken promise in the Core encounter.

## Open implementation decisions

- [ ] Select the wheeled drive architecture after locomotion requirements and prototypes exist.
- [ ] Select and validate the roll/pitch/yaw joint arrangement, actuation, support, sensing, wiring, and control using a representative head/load prototype.
- [ ] Define the detailed natural-language intent set and acceptable phrasing after the Core scenario semantics are stable.
- [ ] Define the first astromech vocabulary and the behaviours it must express.
- [ ] Set the exact radius and speed of the permitted tabletop test/calibration footprint after stopping tests.
- [ ] Select the person-localization and following architecture, including loss and reacquisition behaviour.
- [ ] Define Spotify authentication, playback control, and failure behaviour.

### Review notes

Approved by the project builder on 2026-08-14. Version 1.1 makes powered roll, pitch, and yaw Core. Time, timer, alarm, Spotify playback, and come/follow behaviours remain Core; broader general utility remains uncommitted.
