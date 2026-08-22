# Makad Engineering Intuition Guide

| Field | Value |
|---|---|
| Status | Canonical methodological guide |
| Version | 1.0 |
| Owner | Project builder |
| Approved | 2026-08-22 |
| Scope | How to think and work through every project phase: foundation (00) → system (01) → prototypes (02) → architecture (03) → BOM (04) → CAD/build |
| Authority | This guide governs *method and reasoning*. It cannot override the approved foundation documents, the system design brief, the risk-prototype plan, the workbench baseline, or the run-record convention. Where this guide and an approved phase document conflict, the phase document wins and this guide must be corrected. |

---

## 1. The one model behind everything

**Every phase of this project is the same activity at a different altitude: retiring uncertainty in order, and never letting a downstream artifact harden around an upstream guess.**

The order is always: **intent → numbers → understanding → competing options → evidence → closed decision.** Only the subject changes:

| Altitude | Uncertainty being retired | Closed by |
|---|---|---|
| Foundation (00) | *What should M4 be?* | Approved vision, scope, scenarios, constraints, success criteria |
| System (01) | *What must we find out, and how, before designing?* | Approved brief, risk-prototype plan, workbench, run conventions |
| Prototypes (02) | *Which mechanisms/topologies/policies actually work?* | Gate results + evidence packets per RP |
| Architecture (03) | *What is Makad, engineering-wise?* | 13 closed ADRs + engineering budgets |
| BOM (04) | *Exactly which parts, from where, at what cost?* | Committed BOM + procurement records |
| CAD/build | *Exactly what geometry?* | Integrated CAD freeze → build → validation |

Two consequences fall out of this model and recur in every phase:

1. **An artifact is only as trustworthy as the layer above it.** CAD made before prototype evidence is fiction with fillets. A BOM made before ADRs close is shopping, not engineering. A prototype run before its intent is quantified measures nothing in particular.
2. **Each layer answers its own question and no other.** The foundation says *what*, never *how*. Prototypes produce *evidence*, never commitments. Architecture makes *commitments*, never purchases. Violating the layering in either direction — down (premature freeze) or up (a spec quietly rewriting scope) — is how projects rot. The project's own history caught both failure modes already (MEM-20260813-23, MEM-20260814-02).

A compact image that holds across the whole repo: **prototypes are the lab notebook, architecture is the published paper, BOM and CAD are what you're allowed to build only from the paper.** The notebook is messy, chronological, append-only; the paper is clean, current, and cites the notebook by run ID; the factory floor never reads the raw notebook.

---

## 2. The repository as a map of the model

```
docs/00-foundation/     WHAT M4 must be              — approved, the test oracle
docs/01-system/         HOW we will find out          — approved instruments
docs/02-prototypes/     EVIDENCE                      — RP-XX folders, runs, decisions
docs/03-architecture/   COMMITMENTS                   — ADRs, budgets, interfaces   (stage 6)
docs/04-bom/            PURCHASES                     — final selection, sourcing   (stage 7)
cad/                    GEOMETRY                      — integrated CAD, frozen last (stage 7)
MEMORY.md               append-only history of how every decision above changed
README.md               current orientation over all of it
```

Directionality rules:

- **Information flows down** (foundation constrains everything; prototype evidence feeds architecture; architecture authorizes BOM and CAD).
- **Citations flow up** (a CAD feature cites an ADR; an ADR cites run IDs; a run cites its preregistered gate; a gate cites a success criterion; a success criterion cites a scenario).
- **Nothing skips a layer.** A part may not be purchased because a prototype "showed it works"; the result must pass through an ADR first. A scenario may not be weakened because a prototype failed; that requires an explicit foundation review (Core-failure rule).

`specsheets/` and `visuals/` sit outside this chain deliberately: exploratory reference, binding on nothing.

---

## 3. Phase 00 — Foundation: authoring intent

**Status: approved and complete. Its role now is oracle, not workspace.**

### How to think about it

The foundation is the project's ground truth for *what*, written before any *how* existed. Its central intellectual move was refusing to let capability lists grow freely: everything funnels through one priority ("M4 should feel alive") and two Core scenarios that translate that feeling into observable behaviour. When a downstream question seems open-ended, the resolution is almost always to re-read the scenario and ask: *what does this moment of the encounter actually require?*

### The skills this phase exercised (and still requires when reopened)

- **Character-first specification.** Intent is authored in experiential terms ("wakes as one coordinated performance") before being quantified. Numbers invented without authored intent behind them are either too soft or falsely precise.
- **Scope as a boundary, not a wishlist.** Core / Target / Candidate / uncommitted is a commitment hierarchy. Core cannot be quietly deferred; Candidates must carry clean removal plans; uncommitted items are not silently promoted.
- **Success criteria written before results exist.** Thresholds get selected before validation and are never rewritten to fit an outcome — the project-level version of preregistration.

### When this phase reopens

Only under the Core-failure rule: a Core prototype outcome that cannot be met by iteration or alternative architecture forces an explicit foundation review — a deliberate, recorded scope decision, never an engineering workaround. If you ever find yourself "reinterpreting" a scenario to make a gate passable, stop: that is a foundation change wearing a disguise.

---

## 4. Phase 01 — System: designing the instruments

**Status: approved. Brief, risk-prototype plan, workbench baseline, and run-record convention exist.**

### How to think about it

Phase 01 does not design Makad. It designs **the program that will make designing Makad safe**: which uncertainties exist, which are dangerous, in what order to attack them, what evidence counts, and what discipline keeps a solo builder honest.

The three load-bearing ideas:

1. **Risk-first ordering.** The prototype sequence is sorted by (uncertainty × consequence), weighted toward the builder's weakest domains (mechanics, firmware, sourcing) and away from comfortable ones (CV, software). When tempted to reorder work, the question is never "what do I feel like building?" but "which unretired uncertainty could invalidate the most downstream work?"
2. **Preregistration is the solo builder's reviewer.** With no colleague to challenge your conclusions, thresholds frozen *before* data plus retained failed runs are the only defense against self-deception. Gate versions change only with a documented reason and a fresh test set.
3. **Identity before energy.** No valid run ID plus no confirmed logger means no actuator enable. This is not bureaucracy; it is the guarantee that a number cited in an ADR six weeks later means what it claims.

### Proportionality (the approved way to stay fast)

The plan's ceremony has two tiers, and using the light one aggressively is compliance, not deviation:

- **Exploratory** (`EXP-exploratory` IDs): most bench hours. Auto-generated identity, minimal ceremony, learning-oriented.
- **Scored**: the handful of runs where a gate actually closes. Full preregistration, evidence packet, readiness checklist.

Rule of thumb: writing more than about one gate-registration record per week means scored theater is being performed on exploratory work. Conversely, citing an exploratory run in an ADR means it should have been scored — go back and score it properly.

### Calendar defense

The deadline (5 Dec 2026) is a constraint with the same authority as any other. Time boxes are real: an iteration beyond the box requires evidence the remaining problem is localized. Fill hardware lead-time gaps with software-side prototypes (RP-05 class work). No week from Stage 0 onward should end with more new markdown than new measurements or hardware progress.

---

## 5. Phase 02 — Prototypes: producing evidence

**This is the current phase. Prototypes are decision instruments, not partial droids.**

Folder convention: `docs/02-prototypes/RP-XX-<name>/` — number for run-ID traceability, name for humans:

```
RP-01-head/
  intent.md           motion storyboard + quantification table
  physics.md          torque/inertia/resonance analysis + assumptions
  concepts/           the ≥2 candidates + comparison matrix
  rig.md              fixture, instrumentation, stop/safety
  gates.md            preregistered thresholds (from the RP plan's G01…G06)
  runs/               one directory per run ID, per run-record convention
  decision.md         pass/iterate/reject outcome; cites runs; feeds ADRs
```

What a prototype folder may **never** contain: a "final" anything. Concept CAD, rig CAD, mass blockouts, candidate sourcing rows — all welcome as working evidence. Frozen geometry and committed purchases live two layers down and one phase later.

### 5.1 The universal six-step loop

Every RP runs the same loop. The content changes; the shape never does.

**Step 1 — State the intent in character terms (no numbers).**
What must Makad *do or feel like*, in plain language. RP-01: "startle — fast recoil then freeze," "curious tilt," "settle without wobble." RP-03: "approach with hesitation," "spin that ends crisply." RP-05: "answers fast enough to feel attentive." This is authored, creative work — animation thinking. If it's vague, everything downstream inherits the vagueness.

**Step 2 — Quantify the intent (a separate pass).**
Convert each named behaviour into numbers an equation can eat: amplitude, duration, time-to-peak → peak velocity and **peak acceleration**; precision class; settle time; latency budgets; load states; staleness bounds. Keep passes 1 and 2 separate or you will unconsciously soften the intent to make the numbers easy.

Sources when the robot doesn't exist: reference footage scrubbed frame-by-frame (R2-D2, BB-8, EVE at 24 fps gives real amplitudes and timings); human/animal data (head-plus-gaze saccades peak ~300–600°/s; conversational response tolerance ~200–1000 ms); acted mockups on 240 fps phone video. These are hypotheses — they become the preregistered thresholds, and the rig later says whether they were achievable *and whether achieving them reads as intended*.

**Step 3 — Do the physics on paper.**
A spreadsheet and an afternoon eliminates most candidates for free. The paper stage answers *what class of solution can possibly work*; only the rig answers *does this specific device behave*. Know which question you're asking.

Mechanical toolkit (RP-01/RP-03 core):

- **τ = J·α + m·g·d·sin(θ) + τ_friction** per axis. Compute **peak** (worst instant — usually direction reversal at max CoM offset) against the actuator's peak rating, and **RMS over a representative cycle** against its thermal rating.
- **Parallel axis theorem: J_axis = J_com + m·d².** For a small head on an offset pivot the m·d² term often dominates — moving the axis toward the CoM buys more than a bigger servo.
- **Gravity compensation is a design variable.** Pitch axis through the CoM (or a counterweight behind the display) sends holding torque to ~zero: smaller, quieter, cooler actuators, no idle buzz — all directly serving aliveness.
- **Reflected inertia: J/N² through ratio N; keep load/rotor under ~10×.** The most predictive paper number for crisp-vs-sloppy motion. Only computable when rotor inertia is published (Dynamixel-class yes; sealed hobby servos no — then the check moves to the rig and is *not* considered passed).
- **Resonance: f_n ≈ (1/2π)·√(K/J_eff).** Motor and head are two inertias joined by compliant printed structure; low f_n means every fast move ends in visible ringing that no controller tuning rescues. Fix order: stiffen structure → reduce m·d² → raise ratio → filter.
- **Backlash is quantity #5 and no equation predicts it.** Reversal deadband comes from geartrain, spline fit, horn attachment. A 2° deadband is enormous when the intended move is 4° (MEM-20260809-04). Paper checklist item when comparing concepts; measured quantity on the rig.
- **3-DOF coupling, the cheap way:** compute each axis at the worst-case configuration of the other two rather than full Newton–Euler.

Electrical toolkit (RP-02): peak concurrent current × path resistance = brownout math; energy integration over the mixed-duty cycle against the 20-minute floor; thermal steady state on regulators, drivers, wires.

Safety toolkit (RP-03): the stopping inequality `d_available > v·t_latency + v²/(2·a_brake) + d_margin` — latency dominates braking at Makad speeds (MEM-20260812-01).

Perception/interaction toolkit (RP-05/RP-07): think in **distributions and staleness**, never averages. A 95th-percentile latency and an observation-age bound; "usually works" is not a number.

**Step 4 — Generate competing concepts (minimum two).**
The first idea only proves itself by beating something. Concepts are sketches, napkin geometry, and a filled comparison of the step-3 quantities — still not CAD. Credibility requires: a load path (never a servo horn cantilever alone), an actuator class with a sourcing path, a cable route, a service/assembly story, and step-3 numbers clearing step-2 requirements with margin.

**Step 5 — Build the ugly rig and measure.**
Open frame, ballast at the representative CoM, guarded, instrumented, deliberately unpretty — a polished prototype is a slower decision instrument. The rig measures what paper cannot: backlash and small-reversal behaviour under load; ringing (was the f_n estimate right?); what a sealed hobby servo actually does; noise character; cable survival; thermal drift; fastener loosening; and for behaviour prototypes, whether the result *reads* as alive to a blinded observer. Everything under the run-record convention.

**Step 6 — Close the decision; only then let geometry harden.**
Gates produce pass/iterate/reject; `decision.md` records it citing run IDs; ADR inputs and budget rows (measured value + uncertainty + margin) get updated; downstream assumptions rechecked. For mechanical prototypes, *this* is the moment detailed CAD becomes transcription instead of speculation.

### 5.2 The loop applied per prototype

| RP | Step 1 intent (examples) | Key step-2/3 quantities | Concepts compared | Rig measures | Closes into |
|---|---|---|---|---|---|
| **RP-01 head** | startle, wake rise, curious tilt, tracking correction, settle | α_peak per move; m, d, J per axis; f_n; backlash budget | joint order, actuation class, support/bearing scheme | reversal deadband, repeatability, ringing, camera shake, noise, endurance | ADR-02/03 evidence |
| **RP-02 backbone** | never browns out mid-performance; 20 min untethered; safe under single failures | concurrent peak current, rail droop, Wh budget, stop-path latency | compute/controller split, rail topology | transients, thermals, watchdog independence, restart behaviour | ADR-06/12 evidence |
| **RP-03 base** | hesitant approach, crisp spin, tiny wiggles, never lurches or falls | min controllable speed, reversal deadband, stopping inequality, stability margin | drive geometry, support/caster type, sensing arrangement | slow-speed quality, stopping, edges, tabletop denial | ADR-04/07 evidence |
| **RP-04 coordination** | one readable performance, not three actuators firing | onset offsets per channel (80–170 ms class), interruption latency, settle | scheduling/composition models vs. independent baseline | phase alignment, degradation, observer coherence | ADR-05 evidence |
| **RP-05 interaction** | feels attentive; fails visibly and in character | per-stage latency distributions, wake accuracy, cancellation latency | pipeline/lifecycle architectures | end-to-end distributions, failure states, barge-in | ADR-10/11 evidence |
| **RP-06 layout** | looks like Makad, serviceable, everything obtainable | mass/CoM/envelope with margins, viewing/coverage geometry, landed cost | physical layouts from sourced parts | legibility, occlusion, contamination, service paths | ADR-01/08/11 evidence; binding envelopes |
| **RP-07 following** | comes when called, follows like a pet, never continues blindly | acquisition time, staleness bound, distance-band control | tracking/selection policies, compute placement | continuity, identity switches, loss→stop behaviour | ADR-09 evidence |

Geometry closes only where the uncertainty was geometric; everything else closes into budgets and architecture. Individual prototypes are followed not by "more individual testing" but by RP-04/RP-07 — which exist because individually-passing subsystems still fail together.

### 5.3 Beginner's concept map (learn per prototype, not upfront)

**For RP-01 (start here):**
- Peak vs. RMS torque — [Motion Control Tips](https://www.motioncontroltips.com/how-to-calculate-continuous-and-peak-torque-values-for-servo-applications/)
- Inertia about an axis, parallel axis, worked examples — [Control Engineering](https://www.controleng.com/how-to-size-servo-motors-advanced-inertia-calculations/)
- Reflected inertia and the ~10× ratio — [PDH gearhead-selection course](https://pdhonline.com/courses/m298/m298content.pdf)
- Mechanical resonance and why controllers can't fix it — [George Ellis, Control Engineering](https://www.controleng.com/how-to-work-with-mechanical-resonance-in-motion-control-systems/)
- Mass/CoM/inertia straight out of CAD with real densities — [Fusion 360 physical properties](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-Find-Mass-Properties-in-Fusion-360.html)
- Inertia-tensor sanity checks and physical meaning — [Gazebo inertia tutorial](https://classic.gazebosim.org/tutorials?cat=build_robot&tut=inertia)

**Foundations, for depth:**
- Rigid-body inertia, principal axes — [Modern Robotics §8.2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/8-2-dynamics-of-a-single-rigid-body-part-1-of-2/)
- Each joint carries everything above it — [Peter Corke, Robot Academy](https://robotacademy.net.au/lesson/forces-acting-on-robot-links/)
- Configuration-dependent multi-body coupling — [MIT OCW 2.12 Ch. 7 (Asada)](https://ocw.mit.edu/courses/2-12-introduction-to-robotics-fall-2005/c7caaa2376b8ec01e270328a3b80b029_chapter7.pdf)

**Closest published analogues:**
- "Adam" humanoid head (MDPI 2024): 1.05 kg head, 70 mm CoM offset, torque peaking 325 N·mm at reversal, ~zero as CoM crosses pivot — RP-01's calculation done end-to-end: [paper](https://www.mdpi.com/2571-5577/7/3/42)
- Spring gravity compensation for social-robot necks — holding torque is a choice, not a fact: [Adascalitei et al.](http://robotica-management.uem.ro/fileadmin/Robotica/2013_1/2013_1_Pag_03_Adascalitei.pdf)

---

## 6. Phase 03 — Architecture: converting evidence into commitments

**Opens at roadmap stage 6, but provisional option studies may run alongside prototypes; commitments may not.**

### What lives here

- **ADRs (Architecture Decision Records), ADR-01…ADR-13.** One significant decision each: the question, options considered, evidence (cited by run ID), the choice, the reasons, and the *revisit trigger* — the named future condition under which the decision must be re-examined. An ADR answers, forever, "why did we do it this way?"
- **`system-architecture.md`** — the selected system: boundaries, responsibilities, control/safety topology.
- **`engineering-budgets.md`** — every budget row as *measured value + uncertainty + margin*, never a bare number.
- **`physical-architecture.md`** — binding envelopes, masses, placements exported from RP-06.
- **`subsystem-interfaces.md`** — timing, freshness, command semantics between subsystems, exported from RP-04/RP-05 measurements.

### How to think about it

**Prototypes and architecture differ as question and answer, and as history and truth.** Evidence folders are immutable — failed runs stay forever, like MEMORY.md. Architecture is current truth — an ADR is superseded by a new version when new evidence lands, with the old version preserved. The mapping is many-to-many (RP-01 feeds four ADRs; ADR-12 draws on three prototypes), which is why neither folder can live inside the other.

Discipline rules:

1. **Every load-bearing claim cites a run ID.** "The head uses concept B because `RP01-G03V1-scored-…` showed X" — not "because it worked well."
2. **Uncertainty travels with the number.** A budget row without a measurement condition and margin is an invitation to false precision.
3. **Provisional is a real status.** ADRs close provisionally as prototypes pass and finalize at stage 6; the status must be visible so downstream work knows what it may rely on.
4. **Safety-critical, mechanically coupled, and packaging-critical choices cannot close on paper alone** — they require the relevant passed evidence, per the RP plan's closeout rules.

---

## 7. Phase 04 — BOM: converting commitments into purchases

**Opens at stage 7, after ADRs and budgets close. Fed continuously before that by the candidate sourcing matrix — candidates, not commitments.**

### How to think about it

A BOM row is a *decision with money attached*, and its epistemics differ from everything upstream: prototype evidence was measured by you, but availability, lead time, and landed cost are **external facts that decay**. Prices and stock are rechecked at purchase time, never trusted from a weeks-old matrix row.

Discipline rules, inherited from RP-06's sourcing gate and the constraints doc:

1. **Landed cost or it isn't a cost.** Unit price + shipping + customs/GST + replacements + the tools the part demands.
2. **Every architecture-critical part has a verified source and at least one acceptable substitute** — or an explicitly accepted, written single-source risk.
3. **Lead time is a schedule input.** Indian sourcing realities belong in the calendar, not in the hope column. Long-lead items are identified early through the continuous matrix even though commitment waits for stage 7.
4. **Quantity includes spares** for parts that prototyping showed are fragile or consumable.
5. **The complete cost picture precedes major procurement** (CON-TBD-13): total the architecture, prototypes, tools, shipping, replacements, and contingency first; then review substitutions or cuts deliberately — no invented ceiling, no drip-spend that forecloses options silently.
6. **A part may enter the BOM only via an ADR or budget that authorizes it.** "RP-01 showed this servo works" is evidence, not authorization; it must pass through ADR-02/03 first.

---

## 8. CAD and build: transcription, freeze, and change control

**The integrated CAD freeze is a single event at stage 7, downstream of everything.**

### How to think about it

By the time integrated CAD begins, every hard question already has a measured answer: actuator envelopes, bearing seats, load paths, cable clearances, service access, mass targets, mic-array geometry, display/camera placement. **CAD is transcription of decisions, not a design activity.** If modeling a region requires inventing an answer, that's a signal an upstream decision is missing — go close it, don't improvise it in the sketch.

Working rules:

1. **Model with real physics from day one.** Correct material densities; override density on lumps (battery, motors) to match datasheets; read m, CoM, and the full inertia tensor from the CAD and check them against `physical-architecture.md` envelopes continuously. Sanity-check tensors (positive diagonals, triangle inequality).
2. **The mass ledger is the head-CAD blocker by design.** If CAD mass properties drift outside the RP-01-validated envelope, RP-01's conclusions no longer apply — the plan requires a rerun (RP06-G04). This is the layering enforcing itself.
3. **Design for the approved construction language:** modular, screw-together, visible fasteners, serviceable panels — identity and serviceability are the same requirement here. The named high-risk module must be replaceable without destructive disassembly (RP06-G06).
4. **Print-aware, not print-driven.** Orientation, tolerances, and printer/material choice per part matter, but geometry serves the mechanism evidence first and the printer second.
5. **After the freeze, changes are controlled.** A post-freeze geometry change that touches mass, CoM, clearances, or any budget must name the ADRs and budget rows it perturbs — and gets a MEMORY entry if it changes a decision. "Just a small tweak" to a head shell is a mass-property change wearing a disguise.
6. **Build and integration inherit run discipline.** Powered integration milestones are runs like any other: identity, logging, evidence. Validation against the success criteria uses thresholds selected *before* final validation, never fitted afterward.

---

## 9. Cross-phase invariants

These hold everywhere, at every altitude:

1. **The traceability chain must be walkable in both directions:** scenario → success criterion → gate → run → decision → ADR → budget → BOM row → CAD feature → validated behaviour. Any artifact that cannot name its parent is an orphan and binds nothing.
2. **History is append-only; truth is current.** MEMORY/runs/superseded ADR versions never change; README/ADRs/budgets always reflect now. Never blend the two in one document.
3. **Preregister, then look.** Thresholds, observer protocols, and pass criteria are chosen before results exist — at every scale from a bench run to final V1 validation.
4. **Failures are evidence.** Failed runs, rejected candidates, and superseded decisions stay visible. Deleting a failure deletes the reason the current answer is trusted.
5. **Ceremony proportional to consequence.** Exploratory work is light; scored/committing work is rigorous. Both directions of mismatch are errors.
6. **Character and control stay connected.** Backlash, latency, onset timing, and settling are *expressive quality* metrics, not just engineering metrics. Numeric gates exist because the numbers serve a feeling; the blinded-observer checks are as real as the torque margins.
7. **Safety overrides expression, locally and always.** Stop paths, watchdogs, and inhibits are independent of high-level intelligence and network; no performance may bypass them.
8. **The calendar is a constraint document.** Time boxes bound iteration; lead times shape sequencing; markdown does not outrun measurement.

---

## 10. Anti-patterns (each caught at least once in this project's history)

1. **CAD first.** Modeling the shell, then cramming motors in — the character dies in the backlash. (MEM-20260809-03/04)
2. **Blending intent and quantification.** "Reasonable" numbers with no authored intent behind them: too soft or falsely precise.
3. **Trusting a datasheet for what it doesn't say.** A stall-torque number says nothing about deadband, resolution, or thermal endurance. An uncomputable paper check is not a passed check — it moves to the rig.
4. **One candidate.** The first idea only proves itself by beating something.
5. **Averages instead of distributions.** "Usually responds in 400 ms" hides the 2 s tail that kills aliveness.
6. **Moving thresholds after seeing results.** A miss is an iterate/reject, never a redefinition of success.
7. **Polishing the rig.** Pretty prototypes are slow decision instruments.
8. **Skipping the "does it read as alive" check.** Passing numeric gates isn't the goal; the numbers serve a feeling.
9. **Spec-shaped documents impersonating decisions.** Writing something in requirement language does not make it approved. (MEM-20260813-23)
10. **Documentation as displacement activity.** A beautiful docs tree with zero energized actuators is only appropriate for as long as the phase says so.
11. **Layer-skipping.** Buying parts from prototype results without an ADR; weakening a scenario because a gate failed; freezing one subsystem's geometry before its neighbours' physics exist.
12. **"Just a small tweak" after freeze.** Every post-freeze geometry change is a mass/clearance/budget change until shown otherwise.

---

## 11. Where the project stands, and what's next

Current position: foundation and system phases approved; Stage 0 (workbench purchase, stop/isolation verification) incomplete; RP-01 unblocked on paper work but blocked on scored testing until the readiness gate passes.

Immediate order of attack (per the RP plan's open-inputs checklist):

1. **Motion storyboard** (`RP-01-head/intent.md`) — 8–12 named moves, then the quantification table: move × (amplitude, duration, α_peak, precision class, settle). Becomes RP-01's registered motion cases.
2. **Mass/envelope blockout** — dumb solids with real densities for display, camera, servos, wiring; read m, CoM, tensor per candidate axis placement; feed the ledger.
3. **Torque spreadsheet** (`physics.md`) — peak + RMS per axis per concept, reflected inertia where computable, f_n estimate, backlash checklist.
4. **Two mechanism concepts** (`concepts/`) compared on those numbers → what goes on the rig.
5. In parallel: complete workbench purchases, and knock out the logging schema + monotonic timebase + video-sync method (software, your home turf, ~days) so process infrastructure never blocks hardware.

Iterate on CoM placement before iterating on servo choice — it's the cheaper lever, and it decides whether Makad hums quietly or buzzes while pretending to sleep.
