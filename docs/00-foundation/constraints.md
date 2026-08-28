# Makad V1 Constraints

| Field | Value |
|---|---|
| Status | Approved |
| Version | 1.2 |
| Owner | Project builder |
| Last reviewed | 2026-08-25 |
| Depends on | `vision.md`, `v1-scope.md` |
| Current physical targets | `../01-system/dimensional-baseline.md` |

## Purpose

This document records the real boundaries inside which V1 must be designed. Unknowns remain visible instead of becoming invented requirements.

## Confirmed project constraints

| ID | Constraint | Consequence |
|---|---|---|
| CON-01 | The V1 deadline is **5 December 2026**. | Planning must preserve integration, validation, and redesign time before this fixed date. |
| CON-02 | The builder can dedicate approximately 60–80 hours per week. | The project can be ambitious, but workload estimates must still include learning, sourcing, failed prototypes, and integration. |
| CON-03 | No fixed project budget ceiling is approved at this stage. Components, prototype replacements, tools, shipping, fabrication, and contingency shall be costed honestly before major procurement. | Architecture and sourcing begin with a complete cost range; expensive choices are then justified, substituted, or cut through review rather than designed to an invented ceiling. |
| CON-04 | The learning priority is physical robotics: mechanics, electronics, sensing, control, and integration. | Familiar software/AI work must not consume the schedule merely because it is easier to add. |
| CON-05 | The builder is learning hardware/mechatronics and CAD through the project. | Mechanisms need realistic fabrication, assembly, calibration, and debugging plans. |
| CON-06 | Several 3D printers are accessible, but the exact machine, build volume, and materials will vary. | Every fabricated part must be checked against the selected printer and material before release. |
| CON-07 | Soldering equipment, a bench supply, multimeter, oscilloscope, and logic analyser are not currently established as available. | The plan must identify which tools are mandatory, then budget for purchase, borrowing, lab access, or an alternate test method before the relevant work begins. |
| CON-08 | Laser cutting, CNC, machining, and other external fabrication access are not confirmed. | Core mechanical design cannot depend on these processes until access, price, and lead time are verified. |
| CON-09 | Primary locomotion occurs on normal indoor floors. Large-tabletop use is stationary by default; only explicitly enabled low-speed test/calibration motion is allowed inside a marked, validated circular footprint. | Floor and tabletop modes require different movement permissions. Come/follow and excited-spin behaviour remain floor-only. |
| CON-10 | Final V1 operation is battery-powered and untethered. The initial runtime requirement is **at least 20 minutes** of representative mixed-duty operation. | Battery, charging, regulation, peak current, runtime, thermal behaviour, and accessible power isolation are system-level budgets. Runtime may be increased after representative power and mass measurements. |
| CON-11 | Reliable network and cloud access may be assumed for the full Core interaction set; no duplicate offline implementation of language, time, or Spotify capability is required. | External dependencies still need explicit timeout, failure indication, and recovery. Physical stop, motion inhibition, obstacle/edge protection, and bounded controller failure must remain effective without the network. |
| CON-12 | Normal household lighting is the baseline visual environment. | Vision must be validated in representative indoor lighting rather than ideal studio conditions only. |
| CON-13 | There is no special project-level prohibition on camera or microphone recording. | Recording and cloud use are permitted; the selected power/sensor controls must make active operation clear and allow it to be stopped. |
| CON-14 | The current physical target is **300 H × 205 W × 180 D mm overall**, governed in detail by `docs/01-system/dimensional-baseline.md`; total mass remains architecture-derived. | Packaging, stability, transport, fabrication, and operating-envelope checks must preserve this baseline or trigger an explicit revision before CAD freeze. |
| CON-15 | The existing `specsheets/` content is exploratory and non-binding. | Every architecture, metric, interface, and part choice must be reconsidered before adoption. |
| CON-16 | Existing renders are provisional visual references. | They guide character direction but do not determine dimensions or internal architecture. |
| CON-17 | Requirements precede final component selection and CAD freeze. | No component is selected merely because an old document names it. |
| CON-18 | V1 is a serious prototype, not a consumer product. | Reliability must support repeated testing and demonstration; certification and production readiness are not implied. |
| CON-19 | The initial interaction/following envelope is a single indoor household room: ordinary interaction from approximately 0.3–2.0 m, “come here” from approximately 1–2 m with a 0.6–0.9 m stopping distance from the person, and following over a route up to approximately 3 m at a slow walking speed no greater than approximately 0.5 m/s. | Early perception and locomotion work can use a bounded representative case: a level indoor floor, one gentle turn, representative furniture/box/person obstacles, no stairs, and no requirement for room-to-room navigation. Exact validation tolerances remain prototype-derived. |

## Proportionate safety constraint

Safety work should be proportional to Makad's plausible hazards, not treated as a generic product-certification exercise. There is no reason to add safety bureaucracy for behaviour that cannot cause meaningful harm.

The project must nevertheless address real risks created by:

- a mobile robot contacting people, pets, furniture, or cables;
- falling from a tabletop or raised surface;
- pinch points in the neck or drivetrain;
- unstable or uncontrolled motion;
- battery faults, short circuits, charging, and peak current;
- hot components or enclosure surfaces;
- a failed cloud, controller, sensor, or communication path leaving motion active.

Where an identified behaviour or component can cause harm or damage, safety takes priority over expressive behaviour.

## Design constraints approved in review

| ID | Constraint | Reason |
|---|---|---|
| CON-P01 | Use modular, screw-together construction with service access. Visible fasteners and panels are part of M4's personality. | Iteration, debugging, serviceability, and visual identity. |
| CON-P02 | Provide an immediately accessible physical power cutoff or equivalent hard stop for hazardous outputs. | Safe prototype testing and recovery. |
| CON-P03 | Network and cloud services may be required by Core behaviours. | Full cloud access is available and natural-language understanding is Core. |
| CON-P04 | Every required network service must have explicit timeout and degradation behaviour. | Service loss must not produce uncontrolled motion or an indefinite broken state. |
| CON-P05 | Major CAD freezes only after mass, volume, heat, power, wiring, stability, and moving-clearance estimates exist. | Avoid enclosure-driven rework and unstable packaging. |
| CON-P06 | Targets and Candidates have time boxes and removal/fallback plans. | Preserve a coherent Core while still pursuing the intended ambitious vision. |
| CON-P07 | Fallbacks should preserve the best possible version of the vision, not become the default implementation target. | Risk management must not quietly lower the intended quality bar. |

## Values still requiring a decision or measurement

| ID | Open value | Current planning value |
|---|---|---|
| CON-TBD-03 | Available electrical tools and acquisition plan | Not yet established |
| CON-TBD-04 | External fabrication access | Not yet established |
| CON-TBD-06 | Maximum acceptable mass | To be derived and approved; moderate weight is acceptable |
| CON-TBD-09 | Charging method and whether operation while charging is allowed | Not yet selected |
| CON-TBD-13 | First complete project cost range | Produce from candidate components, prototype quantities, tools, fabrication, shipping, replacements, and contingency before major procurement |
| CON-TBD-14 | Exact tabletop test/calibration footprint | Set radius, speed, stopping margin, and edge-test geometry after the locomotion prototype |

## Engineering decision order

1. Use the approved foundation and Core scenarios as the requirements anchor.
2. Establish the electrical-tool plan and begin a sourcing/availability/cost survey for every prototype-critical component class.
3. Prototype the powered roll/pitch/yaw head mechanism and motion firmware with a representative load.
4. Establish the electrical/control backbone and test representative concurrent peak loads.
5. Prototype wheeled locomotion, low-speed quality, stopping, stability, obstacle handling, and tabletop-edge protection.
6. Prototype natural coordinated head–body–wheel motion and the scheduling/firmware behaviour that composes it.
7. Validate wake/interaction latency, then person tracking/following and audio/display integration against the bounded household envelope.
8. Close the architecture and mechanical, electrical, power, compute, internal-communication, external-network, perception, timing, sourcing, cost, and schedule budgets from evidence.
9. Select final components and build the procurement BOM.
10. Freeze integrated CAD only after the relevant prototype, sourcing, and budget gates pass.

## Open implementation decisions

- [ ] Establish the electrical-tool acquisition/borrowing plan.
- [ ] Produce the first complete component, prototype, tool, fabrication, shipping, replacement, and contingency cost range.
- [ ] Select the charging method and whether operation while charging is allowed.
- [ ] Set the exact tabletop test/calibration footprint after stopping tests.
- [ ] Validate the approved dimensional baseline and derive the maximum acceptable total mass during architecture/layout work.

### Review notes

Approved by the project builder on 2026-08-14. Version 1.1 removed the fixed budget ceiling, established an initial 20-minute untethered runtime, defined a bounded household interaction/following envelope, limited tabletop motion, and prioritized three-axis mechanical/firmware prototyping. Version 1.2 adopts the 2026-08-25 dimensional baseline while leaving maximum total mass architecture-derived. The fixed V1 deadline remains 5 December 2026.
