# Makad — MEMORY.md

> **Append-only project decision log.**
> Initialized 2026-08-13 as a reconstruction. Condensed 2026-09-08 (MEM-20260908-02); the verbatim pre-condensation text is preserved at `docs/archive/MEMORY-full-20260908.md`.

`README.md` describes current project truth. This file records how the project got there: decisions, reversals, corrections, and what superseded what. Requirement documents remain the authoritative source for exact wording.

## Rules

1. Never delete or reword an entry. A changed decision gets a new entry whose `Supersedes:` names the old ID; the old entry is untouched.
2. Corrections are appended, never edited in.
3. Every entry carries date-based ID, type, status, and the decision in one or two sentences. Add `Why`, `Consequences`, and `Follow-up` only when they are not obvious from the linked document.
4. Cite the governing document and version; do not restate its content here.
5. Mutable state (open questions, status tables) lives in `README.md`, not here.
6. Types: `DECISION`, `CHANGE`, `CORRECTION`, `REVIEW FINDING`, `VALIDATION`, `BUILD`, `OPEN`. Statuses: `CURRENT`, `PROVISIONAL`, `SUPERSEDED`, `HISTORICAL`. `HISTORICAL` marks an entry whose subject no longer exists (for example a retired exploratory spec) while the recorded intent may live on elsewhere.

Entry format:

```md
### MEM-YYYYMMDD-NN — Title
**Type / Status / Supersedes / Governs:** …

Decision in one or two sentences. Optional Why, Consequences, Follow-up.
```

---

## Era 0 — Reconstructed prehistory (2026-08-03 → 2026-08-13)

All entries below are `Provenance: RECONSTRUCTED` from conversations before any approved foundation existed. The `specsheets/` documents they reference were declared non-binding by MEM-20260813-23 and superseded by the foundation in MEM-20260814-01. The design intents survive where the Status column says so; the spec IDs (SPEC-xx, Cxx-Ryy, OQ-xx) do not.

| ID | Type | Decision or finding | Status now |
|---|---|---|---|
| MEM-20260803-01 | CHANGE | AURA (manipulation-heavy assistant) collapses toward a small companion robot where expression, perception and integration are the hard problem. | Superseded by MEM-20260807-01 |
| MEM-20260807-01 | DECISION | Project becomes **Makad** ("monkey"); feeling alive is a first-class goal; hackable maker platform, not a sealed toy. | Current; identity refined by MEM-20260814-01 |
| MEM-20260807-02 | DECISION | Mechanical droid visual language: sharp-ish corners, pseudo sheet-metal panels, screw-together, visible camera, `MAKAD` branding, monkey-like side ears. | Current |
| MEM-20260807-03 | DECISION | Hardware first, software later. | Clarified by MEM-20260813-13 |
| MEM-20260808-01 | CHANGE | Wheels become an official capability; BB-8 as expressive reference but no spherical mechanism. | Current |
| MEM-20260808-02 | DECISION | Differential drive with passive support; no self-balancing. | Current; exact topology fixed in MEM-20260825-01 |
| MEM-20260809-01 | DECISION | Face is **eyes only, no mouth**, circular identity, dot-matrix/phosphor aesthetic, procedural animation. Later concept art showing a mouth is non-canonical. | Current |
| MEM-20260809-02 | DECISION | Eye parameters expand beyond x/y/radius: closure, blink, widen, squint, asymmetric lids, lid angle, brightness, sleep/wake. | Current |
| MEM-20260809-03 | DECISION | Head motion is an engineering subsystem: torque, backlash, closed-loop, structural support, repeatability. | Current |
| MEM-20260809-04 | REVIEW FINDING | Backlash is proportional to expressive scale; a 2° deadband is enormous against a 4° move. Small-reversal tests become neck validation. | Current; now the ≤0.50°/≤0.25° complete-output targets in `storyboard.md` |
| MEM-20260809-05 | DECISION | Freeze a 20-point functional list; sequence functionality → requirements → specs → architecture → budgets → parts → BOM → CAD. | List superseded by MEM-20260814-01; sequencing retained via MEM-20260813-13 |
| MEM-20260810-01 | DECISION | Neck: yaw + pitch MUST, roll TARGET, yaw→pitch→roll order, measured joint pose feeds perception. | Roll classification superseded by MEM-20260814-03; order carried into Concept A |
| MEM-20260810-02 | VALIDATION | Small-motion acceptance becomes quantitative: ±4° reversals, ≤1° lost motion pass, ≤0.5° target, ~240 fps video as independent measure. | Provisional; evolved into `storyboard.md` §2.4–2.5 |
| MEM-20260810-03 | DECISION | Attention model: eyes signal first, head establishes gaze, base handles large reorientation. | Current |
| MEM-20260810-04 | CHANGE | Real-time speech input stays; ordinary English output becomes optional; droid voice is the primary channel. | Current; astromech output is Core (SCOPE-06) |
| MEM-20260810-05 | REVIEW FINDING | Tonal chirps are poor AEC excitation; barge-in during motion makes echo cancellation harder, not just more important. | Current |
| MEM-20260810-06 | REVIEW FINDING | Partial or stale recognition must never cause irreversible motion; utterance IDs and cancellation semantics required. | Current |
| MEM-20260810-07 | DECISION | Perception is layered temporal tracking (tracks, loss, reacquisition, uncertainty, moving-camera compensation); track ID is not identity. | Current |
| MEM-20260810-08 | DECISION | Observations bind to capture-time head pose, not processing-time pose. | Provisional |
| MEM-20260811-01 | REVIEW FINDING | Two ear microphones have front/back ambiguity and cannot support audio/visual association. | Resolved by MEM-20260811-02; sharpened by MEM-20260813-19 |
| MEM-20260811-02 | DECISION | **Four synchronized MEMS microphones in the body**, non-collinear, none in head or ears; ear pods visual-only. | Current (`dimensional-baseline.md`) |
| MEM-20260811-03 | DECISION | Capture, playback, fusion and expression share one timing reference. | Sharpened by MEM-20260813-19 |
| MEM-20260811-04 | REVIEW FINDING | Presence needs explicit ambiguity, staleness, handle-swap and session semantics; unknown is a valid output. | Current |
| MEM-20260811-05 | DECISION | Procedural aliveness (continuous, low-amplitude) is separated from authored performances (recognizable transients). | Current |
| MEM-20260812-01 | REVIEW FINDING | Reaction latency dominates stopping distance: `d_available > v·t_latency + v²/(2·a_brake) + d_margin`; obstacle/cliff safety runs on the low-level controller with ≤50 ms detection-to-decel. | Current |
| MEM-20260812-02 | CHANGE | IMU promoted toward MUST for slip, lift, tip and odometry failure detection. | Current; base-frame IMU deferred to RP-03 (MEM-20260831-02) |
| MEM-20260812-03 | REVIEW FINDING | Body yaw turns the mic array into a rotating frame; locomotion must publish timestamped yaw. | Current |
| MEM-20260812-04 | REVIEW FINDING | Drivetrain vibration reaches all mics coherently; beamforming does not fix it, isolation and inhibit do. | Current |
| MEM-20260812-05 | DECISION | Audio may request a locomotion inhibit during active listening, separate from safety inhibit. | Current |
| MEM-20260812-06 | DECISION | Minimum controllable speed, reversal deadband and backlash are expressive-quality motor criteria. | Current |
| MEM-20260812-07 | DECISION | Startle begins with deceleration to stop; no blind fast reverse. | Current |
| MEM-20260812-08 | REVIEW FINDING | Drive must resist head reaction torque at zero commanded velocity. | Current |
| MEM-20260812-09 | REVIEW FINDING | Body footprint should stay inside the swept circle about the axle midpoint; head-height sweep needs its own limit. | Provisional |
| MEM-20260812-10 | REVIEW FINDING | Low-level obstacle recovery: stop, bounded slow reverse, turn, resume; must not depend on high-level AI. | Provisional |
| MEM-20260812-11 | CHANGE | Procedural layer may use the base for micro-motion only, summed before safety clamping. | Historical spec; intent current |
| MEM-20260812-12 | DECISION | Procedural base motion is discrete micro-moves with dwell, not continuous sub-threshold drift. | Current |
| MEM-20260812-13 | DECISION | Procedural base random walk must be spatially bounded (return bias or displacement window). | Current |
| MEM-20260812-14 | DECISION | Proximity suppresses procedural base motion before the safety clamp becomes visible behaviour. | Current |
| MEM-20260813-01 | CHANGE | Base becomes a full authored-performance channel; drive layer keeps execution and safety. | Provisional per MEM-20260813-14 |
| MEM-20260813-02 | DECISION | Geared base has ~150–400 ms perceptible onset; cannot share a clock edge with display/audio/neck. | Provisional |
| MEM-20260813-03 | DECISION | Reaction performances lead with display/audio, then neck, then base. | Current |
| MEM-20260813-04 | DECISION | Base-yaw gaze compensation (geometric) and acceleration-to-pitch expression (tunable) are separate couplings. | Current |
| MEM-20260813-05 | DECISION | Planned base motion can be anticipated by the neck; external/safety motion can only be reacted to. | Current |
| MEM-20260813-06 | DECISION | A base veto degrades only the base track of a performance. | Current |
| MEM-20260813-07 | DECISION | Sustained authored base velocity below the validated minimum is non-conforming. | Current |
| MEM-20260813-08 | DECISION | Five base performances carried: curious approach, turn-toward-caller, excited spin, side-to-side, startle; side-to-side is highest risk. | Current |
| MEM-20260813-09 | OPEN | Open follow-ups recorded by OQ ID. | Historical; OQ register retired by MEM-20260814-02 |
| MEM-20260813-10 | DECISION | `README.md` (current truth) and `MEMORY.md` (append-only history) introduced. | Current |
| MEM-20260813-11 | REVIEW FINDING | README reconciled against the exploratory spec map. | Historical |
| MEM-20260813-12 | CHANGE | Governance corrected: supersession is append-only, pre-08-13 entries marked reconstructed, mutable registers moved out. | Current; rules above |
| MEM-20260813-13 | CORRECTION | Cut line is 3–4 months (4–5 belonged to AURA). "Hardware first" means the difficulty budget goes to mechanics/electronics/integration, not that parts precede requirements. | Current; supersedes MEM-20260807-03 |
| MEM-20260813-14 | CORRECTION | SPEC-13/SPEC-16 amendment application was unverified. | Historical; specs non-binding |
| MEM-20260813-15 | DECISION | Affect state modulates; performances are bounded acts. No central `current_emotion` enum. | Current |
| MEM-20260813-16 | DECISION | VLM protocol is a caller-driven registry starting empty; VLM inclusion in V1 open. | Historical; VLM uncommitted per `v1-scope.md` |
| MEM-20260813-17 | REVIEW FINDING | Procedural-layer math corrections (summed-coordinate saturation, stable stimulus classes). | Historical spec |
| MEM-20260813-18 | DECISION | Compensation removes unintended lag so authors can specify intentional lag; 80–170 ms onset offsets per fast link. | Provisional |
| MEM-20260813-19 | CORRECTION | Mic chain: ≥90% audio/visual association at ≥40° separation → σₐ ≤13–15° → ≥4 non-collinear mics; capture and playback need a shared word clock. | Current; supersedes MEM-20260811-01/-03 |
| MEM-20260813-20 | DECISION | Ball/dual passive support preferred; holonomic drive rejected for V1. | Support type superseded by MEM-20260825-01 (front caster + rear skid); holonomic rejection current |
| MEM-20260813-21 | CHANGE | Mutable registers moved to README. | Historical |
| MEM-20260813-22 | CORRECTION | OQ mapping for reconciliation traceability. | Historical |
| MEM-20260813-23 | CORRECTION | **`specsheets/` and `visuals/` are exploratory and non-binding.** Only the concept, name, broad intent and a provisional visual anchor were established. | Current |

---

## Era 1 — Foundation approval (2026-08-14)

### MEM-20260814-01 — Human-reviewed V1 foundation approved
**Type / Status / Governs:** DECISION / CURRENT / `docs/00-foundation/` v1.0

Makad (M4K4-D, "M4") is a personal droid whose V1 objective is to feel alive. Core: expressive head, animated face, camera-side LED, natural-language in and astromech out, face tracking, wheeled floor locomotion, come/follow, obstacle and tabletop protection, time/timer/alarm/Spotify, modular screw-together build. Deadline **5 December 2026**. Following and sustained tracking are Core, not Targets. Closes the follow-up in MEM-20260813-23.

### MEM-20260814-02 — README reconciled with the foundation
**Type / Status:** CHANGE / CURRENT

README rewritten as an orientation document derived from the foundation. The exploratory spec map, speculative numeric constraints and OQ register no longer appear as current authority.

### MEM-20260814-03 — Powered roll, pitch and yaw are all Core
**Type / Status / Supersedes / Governs:** CHANGE / CURRENT / roll-as-Target in MEM-20260814-01 and MEM-20260810-01 / foundation v1.1

A two-axis head is not a V1-complete fallback. The three-axis head and its firmware become the first risk prototype.

### MEM-20260814-04 — Planning constraints reset
**Type / Status / Supersedes / Governs:** CHANGE / CURRENT / budget, runtime and framing parts of -01/-02 / `constraints.md` v1.1, `system-design-brief.md` v0.2

No external rubric. No fixed spend ceiling; cost the complete picture first (CON-TBD-13). Untethered runtime ≥20 min. Household envelope: interaction 0.3–2.0 m, come from 1–2 m stopping 0.6–0.9 m away, follow ≤3 m at ≤0.5 m/s. Tabletop stationary by default. Cloud may be assumed for Core; physical safety may not depend on it. Priority order: sourcing, three-axis head, electrical/control, locomotion, coordination, then CV/audio/display.

### MEM-20260814-05 — System design brief approved
**Type / Status / Governs:** DECISION / CURRENT / `system-design-brief.md` v1.0

Fixes system boundary, responsibility model, 13 architecture drivers, information contracts, failure model, 15 budget categories, ADR-01…ADR-13 and the seven-prototype portfolio. Selects no component, mechanism or threshold.

---

## Era 2 — System instruments (2026-08-17 → 2026-08-22)

### MEM-20260817-01 — Risk-prototype plan approved
**Type / Status / Governs:** DECISION / CURRENT / `risk-prototype-plan.md` v1.0

RP-01…RP-07 with roadmap, dependency order, preregistered thresholds, minimum evidence packet, pass/iterate/reject/defer and Core-failure rule. Powered scored tests blocked until a reviewed workbench gate exists.

### MEM-20260817-02 — Workbench baseline approved
**Type / Status / Supersedes / Governs:** DECISION / CURRENT / workbench-as-proposed in -01 / `workbench.md` v1.0, plan v1.1

Tool classes, buy/defer order, E-stop rule (cut motor bus, not logic), scored-test readiness checklist, battery gate. Approval is not purchase.

### MEM-20260822-01 — Immutable run identity for every physical execution
**Type / Status / Governs:** DECISION / CURRENT / `run-record-convention.md` v1.0, `_templates/run-record.md`

`RP<nn>-<gate|EXP>-<class>-<UTC>-<seq>`; allocated before the run, never renamed or deleted, failed runs retained. **No valid run ID plus no confirmed logger means no actuator enable.** Log schema, monotonic timebase and video sync remain open.

### MEM-20260822-02 — Engineering intuition guide adopted
**Type / Status / Governs:** DECISION / CURRENT / `docs/intuition.md` v1.0

Method guide for all phases: retire uncertainty in order; six-step prototype loop; `docs/02-prototypes/RP-XX-<name>/` skeleton; ADRs/budgets in a future `docs/03-architecture/`, BOM in `docs/04-bom/`, integrated CAD in root `cad/`. Methodological authority only; phase documents win on conflict.

### MEM-20260822-03 — Planning time boxes removed
**Type / Status / Supersedes / Governs:** CHANGE / CURRENT / time-box provisions in MEM-20260817-01 / plan v1.2

Per-prototype day counts were invented precision. Iteration discipline is enforced by the gate-review rule instead. (This entry was originally numbered MEM-20260822-02, duplicating the guide-adoption entry; renumbered by MEM-20260908-02.)

---

## Era 3 — Baselines and component locks (2026-08-25 → 2026-09-02)

### MEM-20260825-01 — 300 mm geometry and drive topology adopted
**Type / Status / Governs:** DECISION / PARTIALLY SUPERSEDED / `dimensional-baseline.md` v1.0, `constraints.md` v1.2

300 H × 205 W × 180 D mm; Ø84 wheels, 170 mm track, 110 mm axle-to-caster; two encoder wheels + front caster + mandatory rear skid; 140 mm body-top datum, 60 mm neck allocation; body-mounted mics, speaker, battery and primary electronics. Also adopted a ~250 g head target with ~0.001 kg·m² and ~0.2 N·m proxies. Head envelope superseded by MEM-20260830-01; head mass and proxies superseded by MEM-20260831-01 and MEM-20260902-01. Drive, placement and datum decisions remain current.

### MEM-20260825-02 — Battery sign, clearance and skid geometry corrected
**Type / Status / Governs:** CORRECTION / CURRENT / baseline v1.1, plan v1.3

Battery goes **low and forward** of the axle. CoM target `x=+25 mm, h=124 mm` gives caster-lift threshold `a_tip ≈ 2.0 m/s²`, which governs before traction. Shell clearance 25–35 mm. Skid at 70 mm reach must be ≤14 mm high (`h/d < 0.20`). CoM must be recomputed under the heavier head.

### MEM-20260829-01 — Face display and head camera locked *(backfilled 2026-09-08)*
**Type / Status / Governs:** DECISION / CURRENT / `display-candidate-study.md` v0.5, `camera-candidate-study.md` v0.2, plan v1.6–1.7

On 2026-08-29 the builder dropped the AMOLED requirement and locked the **Waveshare ESP32-S3-LCD-4.3 no-touch, SKU 30493** (800×480 IPS, on-board ESP32-S3/LVGL renderer, ~106.1 × 67.8 mm) and the **Raspberry Pi Camera Module 3 Wide, SC0874** (IMX708, 102° horizontal). Head-local rasterization (D2) follows from the display; the body SBC sends semantic face state. Supplier, production moving CSI interconnect (H1/H2/H3 in `head-harness-routing-study.md`) and installed masses stay open. Reopening either requires a recorded hard failure. These locks were recorded in the studies at the time but received no log entry until MEM-20260908-01.

### MEM-20260830-01 — Head envelope rebuilt from the selected display
**Type / Status / Supersedes / Governs:** CORRECTION / CURRENT / 100 × 180 × 130 mm head in MEM-20260825-01 / baseline v1.7

Nominal complete head **95 H × 150 W × 115 D mm**, validated within 90–100 × 145–155 × 110–120; core 95 × 125–130 × 110–115. Optical aperture ~95 × 54 inside a 110–115 × 60–65 bezel. Side pods integrate pivots and add only 8–12 mm per side.

### MEM-20260831-01 — RP-01 material/finish locked; 250 g head rejected
**Type / Status / Supersedes / Governs:** DECISION + CORRECTION / CURRENT FOR RP-01 / 250 g, 0.001 kg·m², 0.2 N·m in MEM-20260825-01 / `material-finish-mass-decision.md`, `payload-mass-capture.md`

D-01…D-08: all RP-01 structure and skin in PLA (provisional beyond the prototype), real visible M2 button-heads, nine-step chipped-paint finish, integral cosmetic seams, 0.3–0.5 mm panel offsets. Planning build-up **~490 g at 1.2 mm walls before M008**, a lower bound, not a target. Requires full-width rear window mask, display flashing path and a separable yaw-plane harness boundary (CAD-01…CAD-06). Every actuator conclusion based on the old mass is reopened.

### MEM-20260831-02 — ESP32-S3 motion firmware; Nano and IMU to the bench
**Type / Status / Supersedes / Governs:** DECISION / CURRENT FOR RP-01 / Nano-as-installed-controller path / `control-topology-options.md` v0.7

Motion firmware targets ESP32-S3 from the start. Nano 33 BLE Sense is a bench instrument only. Stationary RP-01 has no runtime head IMU (servo encoders give joint angle); a locomotion IMU belongs on the base. Official SKU 30493 schematic audit: only GPIO6 is cleanly exposed, so **C1 (motion on the display board) fails the pin screen**; C2 (separate ESP32-S3) becomes the active path.

### MEM-20260902-01 — C2 selected; display and motion roles separated
**Type / Status / Governs:** DECISION / CURRENT FOR RP-01 / control study v0.8, baseline v1.8, ledger v0.11, `RP-01-head/decision.md`

Display ESP32-S3 renders eyes. Separate C2 ESP32-S3 instantiates the registered `MJ5`/`MS7`/`TRACK`/`BRAKE` laws, synchronizes yaw/pitch/roll, owns the servo bus, limits, watchdog, E-stop and command expiry. Smart servos close only local loops. System baselines now carry ~490 g pre-M008 plus C2. C1 reopens only via display-carrier change control.

---

## Era 4 — Head layout preparation (2026-09-07 →)

### MEM-20260907-01 — CAD records created; first-layout construction choices
**Type / Status / Governs:** DECISION + ORGANIZATION / CURRENT FOR FIRST RP-01 LAYOUT / `RP-01-head/cad/head/decisions.md`, `requirements.md`, `packaging-estimates.md`

HEAD-CAD-01/02/04/05: integral rib/backplate with removable carrier, rear cover, ear shells, servo mounts and bearing cartridge; coaxial direct 1:1 roll on an independently supported spindle with XC330 as a size reference; solid yaw spindle with an external guided service loop; C2 removable on the rolling cradle. CAD-01…CAD-06 relocated unchanged. Folder lives at `docs/02-prototypes/RP-01-head/cad/`; root `cad/` stays reserved for integrated CAD.

### MEM-20260907-02 — Ears follow the rolling face
**Type / Status / Supersedes:** DECISION / CURRENT FOR FIRST RP-01 LAYOUT / open ear ownership in -01 and the 09-05 yaw-yoke cover proposal

HEAD-CAD-03: both cosmetic ears attach to the rolling cradle and move with yaw, pitch and roll. Mass membership updated without adding a second ear allowance. Pre-layout brief prepared; no CAD modelled yet.

### MEM-20260907-03 — A0 selected as the first-layout balance target
**Type / Status:** DECISION / CURRENT FOR FIRST RP-01 LAYOUT

HEAD-CAD-07: pitch axis through the pitch-carried CoM, roll near the rolling assembly's CoM. A1/A2 are fallback sensitivity cases. No preload or spring selected.

### MEM-20260907-04 — C2 module selected: Waveshare ESP32-S3-Zero
**Type / Status / Clarifies / Governs:** DECISION / CURRENT FOR RP-01 / MEM-20260902-01 / control study v0.9 §6.3, CTRL-04/06, sourcing matrix v0.17, CAD-04a

Headerless ESP32-S3FH4R2, 19 exposed GPIO, 23.5 × 18 mm; ~17 clean pins against a 12-signal future-ready screen. Bench twin ESP32-S3-DevKitC-1-N8R8 (not installed, same firmware). Rejected: XIAO ESP32S3 (pins), DevKitC as installed (size), Waveshare/SB servo boards (wrong family or pre-decides servo bus). Constraints: keep E-stop/fault off GPIO0/3/45/46; GPIO21 is the WS2812; no USB-UART bridge so the sealed head needs a C2 flashing path (CAD-04a). **M008 stays unknown until the installed assembly is weighed.** Purchase, servo family and RP02-G05 remain open.

### MEM-20260907-05 — Camera crown selected *(backfilled 2026-09-08)*
**Type / Status / Governs:** DECISION / CURRENT FOR FIRST RP-01 LAYOUT / HEAD-CAD-06

Builder selected a local trapezoidal upward shell protrusion at the camera, continuous with the face bezel, instead of solving the display/camera height stack by depth staggering. Crown dimensions and the resulting total head height against the 90–100 mm band are open; layout-01 trials Z=109 mm. Recorded in `decisions.md` on 2026-09-07; log entry added by MEM-20260908-01.

### MEM-20260907-06 — Layout-01 packaging study produced *(backfilled 2026-09-08)*
**Type / Status / Governs:** BUILD / PROVISIONAL / `RP-01-head/cad/head/layout-01/`

First build123d packaging study of the A0 / rolling-ear / coaxial-roll arrangement with imported camera and XC330 reference geometry. Fit checker shows zero overlaps across 56 roll/pitch poses **after** neck reliefs were cut into skin and ears (31 hits before). Provisional per-axis sets from the spatial ledger: roll ~392–417 g, pitch ~452–477 g, yaw ~523–548 g across C2 scenarios of 10/20/35 g. Not fabrication CAD, not swept clearance, not a servo pass.

---

## Era 5 — Log maintenance (2026-09-08)

### MEM-20260908-01 — Missing entries backfilled
**Type / Status:** CORRECTION / CURRENT

The 2026-08-29 display and camera locks, the 2026-09-07 camera-crown decision and the layout-01 study had been recorded in their documents but never in this log. Entries MEM-20260829-01, MEM-20260907-05 and MEM-20260907-06 were added with their original decision dates and marked backfilled.

### MEM-20260908-02 — Log condensed; verbatim archive retained
**Type / Status / Supersedes:** CHANGE / CURRENT / the verbose format of all prior entries

The builder judged the log bloated. Every entry ID, date, type, status and supersession link was retained; bodies were condensed to the decision and its governing document. Era 0 reconstructed entries were tabulated with a "status now" column because their spec references are retired. The duplicate ID MEM-20260822-02 was resolved by renumbering the time-box entry to MEM-20260822-03. The pre-condensation file is preserved unchanged at `docs/archive/MEMORY-full-20260908.md`. Rule 1 is unbroken: no decision was deleted or reworded in substance.

---

## Era 6 — Electrical/control backbone preparation (2026-09-08 →)

### MEM-20260908-03 — RP-02 reframed: design question plus gate question; G02/G03 reshaped
**Type / Status / Supersedes / Governs:** DECISION + CHANGE / CURRENT / the v1.9 RP-02 decision question and the v1.9 shape of RP02-G02 and RP02-G03 / `risk-prototype-plan.md` v1.10 §RP-02 and approval note

RP-02 now carries a *design* question (what split, link, rail/protection topology and energy source, with what measured margin) and a separate *gate* question (does it sustain every registered state and `MD-01` for ≥20 min without unsafe motion, reset, rail excursion, staleness or thermal violation, and does every fault bound). G01/G04/G05/G06 stay pass/fail properties. **G02 becomes a standing coexistence invariant with a re-run rule** owned by the power/energy ledger; **G03 becomes a rehearsal with recorded margin**, the 20-minute requirement closing at SC-14. ADR-06 closure is split into an architecture half (stage 2) and a sizing half (after RP-03/RP-05 `W` rows).

**Why**
- A can-question is falsifiable but teaches nothing about margin; a how-question has no failure mode. RP-02 needs both.
- G02/G03 needed loads that do not exist at stage 2, reopen with every later subsystem, and G03 duplicated SC-14.

### MEM-20260908-04 — RP-02 folder created; ledger and timebase placed in `01-system/`
**Type / Status / Governs:** ORGANIZATION + BUILD / CURRENT / `docs/02-prototypes/RP-02-electrical/`, `docs/01-system/power-energy-ledger.md` v0.1, `docs/01-system/timebase.md` v0.1

`RP-02-electrical/` opened with `intent.md`, `state-register.md` (S00…S17 and a proposed `MD-01`, none registered), `power-architecture.md` (PA-01…PA-10, class `E`), `link-contract.md` v0.1, `fault-matrix.md` (F-01…F-16), `rig.md`, `gates.md` (candidates only), `decision.md` (ADR closure ladder, candidate register with nothing selected) and `runs/`. Deliberately not a mirror of `RP-01-head/`. Under the rule that kept the RP-01 CAD sources in place, the power/energy/thermal ledger and the monotonic timebase strategy live in `01-system/` because they serve every prototype; RP-02 populates and validates them. No run, registration, selection or purchase.

**Consequences**
- The ledger's `E` envelope already shows the composite peak (≈5.5–9.5 A at 2S) exceeds the Korad KA3005D's 5 A, so S13 composite rehearsals need the candidate pack or a second supply.
- RP-02 Phase A (state register, ledger seeding, link contract and timebase on the DevKitC-1 twin) is live now and unblocks RP-01's first scored run; Phase B waits on RP-01's servo family and an SBC candidate; Phase C on the battery gate.

---

## Era 7 — Layout 02 logging and Layout 03 pass (2026-09-09)

### MEM-20260909-01 — Layout 02 per-part dimensions log
**Type / Status / Governs:** BUILD / CURRENT FOR LAYOUT 02 / `RP-01-head/cad/head/layout-02/dimensions.md`

Generated axis-aligned bounding boxes, axis datums and yoke-length segments for every named Layout 02 solid at neutral pose, from the parametric model. Not a fabrication drawing, not a freeze, and not Layout 03 geometry. Refresh with `write_dimensions.py`. Mass/CoM remain in `mass-placement.json`.

### MEM-20260909-02 — Layout 03 pass opened
**Type / Status / Governs:** DECISION / CURRENT FOR NEXT CAD PASS / `RP-01-head/cad/head/layout-03-brief.md`, HEAD-CAD-09

After reviewing Layout 02, the next CAD pass is Layout 03: faceted rear-side taper aft of the ears; visible-yoke length versus stiffness without dropping A0 or lengthening the legs; ear/yoke shroud solved on that shell. Layout 02 remains the current 1:1 model until the pass is generated. Display/C2 seats and pitch-servo recentring are not in this pass.

### MEM-20260909-03 — Layout 03 inspection tree: physics, harness, annotations
**Type / Status / Clarifies / Governs:** DECISION / CURRENT FOR NEXT CAD PASS / MEM-20260909-02 / HEAD-CAD-10, `layout-03-brief.md`

Layout 03 STEP must be a labelled occurrence tree with four top groups — physical, physics, harness, annotations — so each can be hidden as a whole and by named subgroup. Physics shows joint axes, origin triad, estimated roll/pitch/complete CoMs, gravity and the camera FOV cone, driven from A0 and the mass tree. Harness is trial centreline-and-jacket geometry partitioned by function, posed with the joint it rides; not a cable SKU or flex certification. Annotations show each named part’s global XYZ in the head-layout frame and its bounding-box size, generated from the dimensions script. Default: physical/physics/harness on, annotations off. Overlay solids are not PLA mass.

### MEM-20260909-04 — Layout 03 is the last packaging/detailing pass; Concept A only
**Type / Status / Clarifies / Governs:** DECISION / CURRENT FOR RP-01 / MEM-20260909-02 / `layout-03-brief.md`, `RP-01-head/decision.md`

Builder: Layout 03 is the intended last RP-01 head packaging and detailing pass. Camera–display board gap **3 mm** (Layout 02’s 1 mm is not the finished stack). Include C2 removable tray and CAD-04a flashing, insert/captive-nut pockets, named bearing seats, coupling fastening and hard stops. **Concept B will not be authored**; RP-01 proceeds on Concept A. This does not freeze a servo SKU, certify optics, or pass gates.

### MEM-20260909-05 — No shroud; yoke by judgment; layered taper feasible-or-keep; look into vignetting
**Type / Status / Clarifies / Governs:** DECISION / CURRENT FOR NEXT CAD PASS / MEM-20260909-02 / HEAD-CAD-09, `layout-03-brief.md`

Builder: Layout 03 does not add a yoke shroud; ear/yoke combined-motion clearance remains. Visible yoke length (below the head) is chosen for stiffness, look-up and cable loop without dropping A0. The head shell must be judged as a layered/tapered shape against [`visuals/mvp-updated-after-spechseet.png`](docs/../visuals/mvp-updated-after-spechseet.png) (appearance only; not ear mics); **reject only if way worse than Layout 02**; cosmetic layering after that call. **Look into vignetting** (FOV cone + written clearance report).

### MEM-20260909-05 — No shroud; yoke by judgment; layered taper feasibility; look into vignetting
**Type / Status / Clarifies / Governs:** DECISION / CURRENT FOR NEXT CAD PASS / MEM-20260909-02 / HEAD-CAD-09, `layout-03-brief.md`

Builder: do not add a yoke shroud; ear/yoke clearance still required. Visible yoke length is chosen by the modeller (stiffness, look-up, cable loop, stack); do not drop A0. The head may be layered and tapered per `visuals/mvp-updated-after-spechseet.png` (non-binding; no ear mics). Feasibility first — reject only if way worse than Layout 02; aesthetics after. Layout 03 must look into vignetting (FOV cone + clear/hit report).

### MEM-20260909-06 — Preserve head modularity and easy disassembly in Layout 03
**Type / Status / Clarifies / Governs:** DECISION / CURRENT FOR NEXT CAD PASS / HEAD-CAD-01, MEM-20260909-02 / `layout-03-brief.md`, CON-P01

Builder: Layout 03 must keep the head practical and modular. It should stay fairly simple to disassemble and to remove components (display, camera, C2, ears, servos, bearing cartridge). Layered/tapered appearance lives on the existing service parts; a scheme that traps hardware or needs destructive disassembly is way worse than Layout 02 and is rejected.

### MEM-20260909-07 — Layout 03 helmet taper checked at 104 mm rear
**Type / Status / Clarifies / Governs:** VALIDATION + CHANGE / CURRENT FOR LAYOUT 03 / MEM-20260909-02, HEAD-CAD-09 / `layout-03/brief.md`, `layout-03/review/verification.md`

The first Layout 03 stern (122 × 82 mm) was a conservative keep-the-hardware choice, not a proven maximum. The shell now keeps the 130 mm ear belt through X−78, deepens upper shoulders to 24 mm, and narrows to 104 mm at X−115 (Z10…84), with rear M2 lands at Y±44. Combined roll/look-up required clipping an unused pitch-servo adapter corner; the 56-pose grid, jackets, optics, hard stops and C2/camera extraction then passed. Estimated complete mass is 6.34 g below Layout 02. Not a fabrication release, servo freeze or optical certification.

### MEM-20260910-01 — Layout 03 camera, C2 and insert retention modelled
**Type / Status / Clarifies / Governs:** CHANGE + VALIDATION / CURRENT FOR LAYOUT 03 / MEM-20260909-07, HEAD-CAD-01, HEAD-CAD-09 / `layout-03/review/verification.md`

The accepted 104 mm packaging is unchanged. The camera bracket now C-channels the Module 3 PCB and sits 0.10 mm from the imported rear shield; the C2 tray gains rear-edge jaws and USB-end corner caps so the board lifts with the tray; front/rear Ø3.2 insert pockets open through the receiver faces. Display, servo-SKU, shaft and harness retention remain open. Not a fabrication release.
