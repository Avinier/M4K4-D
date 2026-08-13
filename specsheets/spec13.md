# SPEC-13 — TRACKED AMENDMENT
## Gaze-Target Channel Distribution: Eyes → Neck → Base

**Base document:** current SPEC-13 — Behaviour Coordination & Performance Scheduling, including the mobile-base amendment.

**Editing rule:** this is a tracked amendment, not a regenerated SPEC-13.

All existing identifiers survive:

- **C13-R01 through C13-R80 — retained**
- **C13-T01 through C13-T42 — retained**

New requirements append from **C13-R81**.

New acceptance tests append from **C13-T43**.

---

# 1. Changelog

## Added requirements

- **C13-R81** — Gaze-distribution ownership boundary
- **C13-R82** — Single redundant gaze objective
- **C13-R83** — Cheapest-sufficient-channel policy
- **C13-R84** — Eye/neck fast inner loop
- **C13-R85** — Base slow outer loop
- **C13-R86** — Prohibition on direct bearing→base closure
- **C13-R87** — Eye→neck handoff
- **C13-R88** — Neck neutral-reference definition
- **C13-R89** — Neck→base hysteretic handoff
- **C13-R90** — Listening-state-dependent neck envelope
- **C13-R91** — Deferred-unwind release
- **C13-R92** — Extended-deflection mechanical/stability bound
- **C13-R93** — Rotating-frame bearing consistency
- **C13-R94** — Performance precedence and gaze-distribution handback
- **C13-R95** — Distribution-base veto semantics
- **C13-R96** — Procedural-idle composition during distribution
- **C13-R97** — Swept-envelope clearance for recruited base yaw

## Amended requirements

- **C13-R07** — insert gaze-target distribution into the shared stage.
- **C13-R69** — clarify that distribution-recruited base yaw remains a SPEC-16-vetoable request.
- **C13-R73** — clarify yaw ownership now that gaze distribution can recruit the base.
- **C13-R77** — extend listening motion inhibit from authored base tracks to distribution-recruited base motion.

## Added tests

- **C13-T43** — Ownership-boundary / SPEC-20 separation
- **C13-T44** — Cheapest-sufficient-channel distribution
- **C13-T45** — Inner/outer-loop convergence
- **C13-T46** — Direct target-bearing→base prohibition audit
- **C13-T47** — Eye→neck handoff
- **C13-T48** — Neck→base hysteresis / boundary dwell
- **C13-T49** — Listening inhibit and deferred body unwind
- **C13-T50** — Extended-deflection limit validation
- **C13-T51** — Rotating-frame bearing / clean termination
- **C13-T52** — Performance override and handback
- **C13-T53** — Distribution-base veto
- **C13-T54** — Procedural idle/headroom during gaze distribution
- **C13-T55** — Swept-envelope clearance of recruited base rotation

## Status-changed

**None.**

Status continues to express confidence, not importance.

## Removed

**None.**

---

# 2. Scope-boundary amendment

Add to SPEC-13 scope:

> **SPEC-13 owns HOW an already-selected gaze target bearing is distributed across rendered eye offset, neck yaw and base yaw.**
>
> SPEC-13 does **not** own WHETHER a target should be:
>
> - attended to,
> - ignored,
> - followed,
> - approached,
> - abandoned,
> - replaced by another target.
>
> Those decisions belong to behaviour arbitration in **SPEC-20**.
>
> SPEC-16 C16-R74 explicitly declines ownership of this channel-arbitration problem and delegates it to SPEC-13.
>
> SPEC-13 receives an authorised target/bearing objective and realizes it. It does not select the objective.

### SPEC-20 stub

> **SPEC-20 shall determine target selection and attention/follow/approach policy; SPEC-13 shall only distribute the resulting authorised bearing across gaze channels.**

---

# 3. Engineering-reasoning addition

## 3.1 One objective, three redundant channels

Horizontal attention now has three actuated representations:

\[
\theta_{target}
\rightarrow
\begin{cases}
\theta_{eye}\\
\theta_{neck}\\
\theta_{base}
\end{cases}
\]

All three can contribute to placing the attended target on Makad's effective forward/gaze axis.

This makes the system **redundantly actuated**.

Without a distribution rule:

- eyes can attempt to null target error;
- neck can independently attempt to null the same target error;
- base can independently attempt to null the same target error.

That is not three layers of intelligence.

It is three controllers fighting over one error signal.

The required architecture is therefore:

```text id="gaze_distribution_arch"
SPEC-20:
"Attend to target T"
          │
          ↓
consistent target bearing
          │
          ↓
┌───────────────────────────────┐
│ SPEC-13 GAZE DISTRIBUTION     │
│                               │
│ FAST INNER LOOP               │
│ target bearing → eyes + neck  │
│                               │
│ SLOW OUTER LOOP               │
│ neck deflection → base yaw    │
└───────────────────────────────┘
          │
          ↓
   channel implementations
```

The existing neck architecture already established the conceptual hierarchy:

> eyes signal attention first; head establishes physical gaze; body/base handles large orientation changes.

This amendment makes the control law behind that statement explicit.

---

## 3.2 Channel-cost ordering

Distribution is biased toward the cheapest channel capable of carrying the required bearing.

| Channel | Approximate onset | Acoustic cost | Safety interaction | Available during active audio capture | Distribution role |
|---|---:|---|---|---|---|
| **Rendered eye offset** | Near-zero relative to mechanical channels; actual display latency remains governed by SPEC-01 | None | None | **Yes** | First / cheapest |
| **Neck yaw** | ~100 ms **PROVISIONAL** | Some actuator/mechanical noise | No locomotion safety interaction | **Yes** | Fast physical follow |
| **Base yaw** | ~150–400 ms **PROVISIONAL** | High: drivetrain noise couples into body-mounted microphone array | Requires swept-envelope clearance under **C16-R60** | **No** while listening-motion inhibit is active | Slow whole-body recentering |

SPEC-16 already treats body rotation as both a safety-envelope and audio-state problem: its current amendment lineage requires rotational swept-envelope coverage and a locomotion motion-inhibit interface separate from the safety inhibit.

The resulting default cost order is:

\[
\boxed{
Eyes
<
Neck
<
Base
}
\]

This is not merely a latency ordering.

It captures:

- actuation cost,
- acoustic contamination,
- safety interaction,
- interruption of listening.

---

## 3.3 Two distinct reasons for body rotation

Base yaw can occur for two fundamentally different reasons.

### Tracking-driven recruitment

Cheaper gaze channels have accumulated enough neck deflection that whole-body recentering is warranted.

### Expressive/performance intent

An authored performance intentionally wants a body turn even though the target could physically be served by neck yaw alone.

These MUST remain distinct.

A dramatic turn can therefore recruit the body because:

> "turn the whole creature"

is the expressive action.

That is different from:

> "the neck is running out of comfortable yaw."

---

## 3.4 Inner-loop / outer-loop structure

The oscillation failure described in SPEC-16 §8.11 occurs if both neck and base close directly on target bearing:

```text id="bad_loop"
target is left
    ↓
neck turns left
    ↓
base also sees target left
    ↓
base turns left
    ↓
neck compensates right
    ↓
base reacts again
    ↓
hunt / oscillate
```

SPEC-13 therefore uses different error signals.

### Fast inner loop

Rendered eyes and neck consume:

\[
e_{target}
=
\theta_{target}
\]

in the current compensated gaze frame.

They track the target directly.

### Slow outer loop

The base does **not** consume target-bearing error.

It consumes:

\[
\boxed{
e_{base}
=
\theta_{neck}
-
\theta_{neutral}
}
\]

Its objective is:

> unwind persistent neck yaw deflection.

As the base turns toward the head:

\[
|\theta_{neck}-\theta_{neutral}|
\downarrow
\]

so:

\[
|e_{base}|
\downarrow
\]

and the body turn naturally terminates.

No special target-acquired stop condition is needed.

---

# 4. Existing requirements amended

## C13-R07 — Evaluation order — MUST — AMENDED

Replace the current shared-stage ordering with:

\[
\boxed{
Affect
\rightarrow
Target\ Gaze\ Distribution
\rightarrow
\left[
Base\text{-}acceleration\ neck\ coupling
+
Authored\ Performance
\right]
\rightarrow
Arbitration
\rightarrow
Reserved\ Clamp
\rightarrow
SPEC\text{-}12
\rightarrow
Full\ Clamp
}
\]

Target gaze distribution includes:

- rendered eye offset;
- neck yaw;
- any recruited outer-loop base yaw.

It belongs to the **affect-and-gaze portion** of the stage and therefore exists beneath authored performance tracks.

Procedural idle remains downstream of distribution and continues receiving the reserved headroom defined by C13-R11/C13-R13.

---

## C13-R69 — Channel safety authority — MUST — AMENDED

Retain existing text.

Add:

A base-yaw request created by gaze-target distribution has the same safety authority as any other SPEC-13 base request:

\[
\boxed{
SPEC\text{-}16\ safety
>
SPEC\text{-}13\ gaze\ distribution
}
\]

Distribution MUST NOT assume that requested body yaw executed.

Safety veto, obstacle/cliff inhibit, motion inhibit or locomotion fault may prevent it.

Failure to execute base yaw invokes C13-R95.

---

## C13-R73 — Base yaw versus linear-acceleration pitch separation — MUST — AMENDED

Retain the existing linear-acceleration→expressive-pitch rule.

Replace the base-yaw paragraph with:

### Base yaw

Base yaw participates in the gaze solution only through the distribution architecture defined by C13-R81–C13-R89.

During a base turn, neck yaw counter-rotation/recentring is part of geometric gaze preservation.

The outer-loop base objective is neck-yaw deflection relative to its neutral reference—not target bearing directly.

This remains distinct from expressive pitch coupling caused by linear acceleration.

Therefore:

\[
a_{linear}
\rightarrow
\Delta pitch_{expressive}
\]

while:

\[
\theta_{neck}-\theta_{neutral}
\rightarrow
\omega_{base,gaze}
\]

and no linear-acceleration term may create expressive gaze yaw.

---

## C13-R77 — Listening motion inhibit — MUST — AMENDED

Retain existing performance-track requirements.

Add:

While listening-motion inhibit is active, **gaze-distribution-recruited base yaw is also unavailable**.

Distribution MUST then use C13-R90–C13-R92:

- allow additional neck yaw within the extended legal envelope;
- hold attention using eyes + neck;
- defer body recentering until the inhibit clears.

The base MUST NOT rotate solely to improve gaze while active capture prohibits locomotion.

---

# 5. New formal requirements

## C13-R81 — Gaze-distribution ownership boundary — MUST

SPEC-13 MUST own allocation of an authorised target bearing across:

- eye offset;
- neck yaw;
- base yaw.

SPEC-13 MUST NOT decide:

- whether the target deserves attention;
- whether it should be followed;
- whether Makad should approach it;
- whether it should replace another target.

Those policies remain SPEC-20 responsibilities.

This requirement is the SPEC-13 counterpart to **C16-R74**.

---

## C13-R82 — Single redundant gaze objective — MUST

Eye, neck and distribution-recruited base yaw MUST be treated as coordinated actuators serving one gaze objective.

They MUST NOT run independent target-bearing controllers whose outputs compete to null the same target error.

There MUST be exactly one SPEC-13 gaze-distribution authority for the authorised bearing.

---

## C13-R83 — Cheapest-sufficient-channel policy — MUST

For ordinary gaze tracking, SPEC-13 MUST bias allocation toward the lowest-cost sufficient channel:

\[
\boxed{
Eyes
\rightarrow
Neck
\rightarrow
Base
}
\]

The base MUST be recruited by the gaze-distribution mechanism only when:

1. cheaper channels have reached the configured escalation condition; or
2. an authored performance separately requests whole-body orientation for expressive intent.

Condition 2 is **not** tracking escalation.

A performance may intentionally turn the body even when neck range alone could carry the bearing.

---

## C13-R84 — Fast inner gaze loop — MUST

Rendered eyes and neck yaw MUST form the fast inner gaze loop.

Their control input is the compensated target bearing.

They MAY share/partition the target bearing according to the existing eye→neck handoff.

They MUST continue target tracking while base recentering occurs.

---

## C13-R85 — Slow outer base loop — MUST

Distribution-recruited base yaw MUST form a slower outer loop.

Its control error MUST be:

\[
\boxed{
e_{base}
=
\theta_{neck}
-
\theta_{neutral}
}
\]

not target bearing.

The base objective is to reduce persistent neck deflection toward the configured neutral region.

As the base rotates and the inner gaze loop maintains fixation, neck deflection SHOULD naturally decay and terminate the body manoeuvre.

---

## C13-R86 — No direct target-bearing→base closure below SPEC-20 — MUST

No controller below the SPEC-20 behaviour layer may command distribution-driven base rotation directly from target-bearing error.

Prohibited structure:

\[
\theta_{target}
\rightarrow
base\ yaw\ controller
\]

Required tracking structure:

\[
\theta_{target}
\rightarrow
eyes/neck
\]

then:

\[
\theta_{neck}-\theta_{neutral}
\rightarrow
base
\]

An authored SPEC-13 performance may still command an explicit body-turn track because its objective is expressive body orientation rather than target-bearing closure.

---

## C13-R87 — Eye→neck handoff — MUST

The eye→neck handoff MUST use the **existing SPEC-12 eye-offset ceiling** as its escalation boundary.

SPEC-13 MUST consume that ceiling as an inherited configuration value.

It MUST NOT define a second competing numeric eye-offset limit.

Once the rendered eye contribution reaches the permitted eye-only region, additional required bearing MUST recruit neck yaw according to the gaze controller.

### Traceability note

The exact C12 requirement ID containing the current eye-offset ceiling is not present in the accessible consolidated artifacts.

The synchronized SPEC-12 stub pass MUST insert that existing C12 ID.

No C12 identifier is invented here.

---

## C13-R88 — Neck neutral reference — MUST

Base-distribution error MUST be measured relative to a configurable neck-yaw neutral reference:

\[
\boxed{
\theta_{neutral}
}
\]

rather than assuming:

\[
\theta_{neutral}=0^\circ
\]

The reference MAY be biased by mechanical calibration, pose configuration or validated character posture.

The base therefore need not unwind the neck to exact geometric centre.

---

## C13-R89 — Neck→base hysteretic handoff — MUST

Normal base recruitment MUST use separate neck-deflection thresholds:

\[
\theta_{engage}
\]

and:

\[
\theta_{disengage}
\]

with:

\[
\boxed{
|\theta_{engage}|
>
|\theta_{disengage}|
}
\]

A minimum dwell:

\[
T_{reengage}
\]

MUST also be enforced before a recently disengaged base loop can re-engage.

Therefore:

- engage outer-loop base yaw only after neck deflection exceeds \(\theta_{engage}\);
- continue unwinding until neck deflection falls below \(\theta_{disengage}\);
- prohibit immediate re-engagement for \(T_{reengage}\).

All three values are:

> **PROVISIONAL — pending simulator and integrated observer tuning.**

---

## C13-R90 — Listening-state-dependent neck envelope — MUST

The permitted gaze neck-yaw envelope MUST be state-dependent.

### Normal operation

Base recruitment occurs at C13-R89's normal threshold.

### Listening-motion inhibit active

SPEC-13 MUST permit neck yaw to continue beyond the normal base-recruitment threshold, up to a separately validated extended listening envelope:

\[
\boxed{
|\theta_{neck}-\theta_{neutral}|
\le
\theta_{listen,max}
}
\]

because the base is unavailable.

The resulting visible behaviour is intentionally:

> Makad turns and holds its head farther toward the speaker while listening, then uses the body to unwind the head after listening ends.

\(\theta_{listen,max}\) is:

> **PROVISIONAL — pending mechanical/stability and observer validation.**

---

## C13-R91 — Deferred body-unwind release — MUST

When listening-motion inhibit clears while neck deflection still exceeds the normal base-recruitment condition, SPEC-13 MUST begin the deferred outer-loop body unwind subject to normal SPEC-16 clearance.

The resulting base-yaw request MUST be slew-limited.

Clearing the inhibit MUST NOT cause:

- a step in base yaw command;
- a snap in neck command;
- an instantaneous attempt to force the neck back to neutral.

---

## C13-R92 — Extended-deflection mechanical and stability bound — MUST

The extended listening neck envelope from C13-R90 MUST remain inside:

1. SPEC-02 mechanical yaw limits;
2. cable/service limits;
3. any applicable SPEC-16 stability envelope affected by head orientation and centre-of-mass projection.

Audio-capture policy MUST NOT authorize a neck posture that violates physical or stability constraints.

---

## C13-R93 — Consistent target-bearing frame during body rotation — MUST

The target bearing consumed by gaze distribution MUST remain expressed in a consistent compensated frame throughout a base-yaw manoeuvre.

SPEC-13 MUST consume the body-yaw/body-yaw-rate information published under **SPEC-16 C16-R91** through the appropriate perception/audio-visual compensation path.

During base rotation, SPEC-13 MUST NOT consume a bearing that is known to be:

- stale relative to current body yaw;
- uncompensated for the rotating body/camera frame;
- expressed in an ambiguous pre-turn frame.

The underlying compensation algorithm remains owned by the relevant perception/audio-visual specification.

SPEC-13 only requires a valid compensated bearing.

---

## C13-R94 — Performance precedence and handback — MUST

Gaze distribution operates beneath performance tracks.

If an active authored performance contains an absolute base-pose/body-orientation track, that performance MUST override distribution-recruited base yaw for the affected quantity.

The inner eye/neck gaze solution MAY continue where compatible with the authored performance.

When the performance releases base control:

- gaze distribution MUST resume from the **current measured base and neck pose**;
- it MUST NOT resume from the pre-performance pose;
- it MUST NOT issue a discontinuous catch-up command.

Handback MUST therefore be bumpless/slew-limited.

---

## C13-R95 — Base-veto behaviour during gaze distribution — MUST

Distribution-recruited base yaw is subject to the same execution veto sources as authored base tracks:

- safety clamp;
- obstacle/cliff inhibit;
- listening motion inhibit;
- locomotion fault.

If the recruited body turn is vetoed:

1. SPEC-13 MUST NOT abandon the authorised gaze target solely because the base is unavailable;
2. the inner eye/neck loop MUST continue;
3. neck yaw MAY remain at the best legal extended deflection permitted by current state;
4. the base request MUST remain withdrawn while veto persists.

If later conditions permit a body unwind, it may resume under normal hysteresis and slew rules.

---

## C13-R96 — Procedural-idle composition during gaze distribution — MUST

SPEC-12 procedural idle MUST remain active during gaze-target distribution.

The gaze-distribution result MUST enter the same pre-procedural reserved-envelope clamp already defined by C13-R11/C13-R13.

SPEC-12 may then add its legal procedural micro-contribution.

Therefore distribution MUST NOT consume the procedural headroom merely because:

- neck yaw is near its gaze limit;
- base recentering is active;
- the target is held for a long duration.

Procedural idle remains downstream of distribution.

---

## C13-R97 — Swept-envelope clearance for recruited base yaw — MUST

A base-yaw manoeuvre recruited by gaze distribution MUST remain subject to the rotational swept-envelope clearance required by **SPEC-16 C16-R60**.

SPEC-13 MUST treat the base request as unavailable until/while SPEC-16 denies the required rotational clearance.

Gaze urgency MUST NOT bypass this constraint.

On denial, C13-R95 applies.

---

# 6. Interface amendments

Add:

| Interface | Direction | Meaning |
|---|---|---|
| Authorised gaze target/bearing | SPEC-20 / perception → SPEC-13 | Target already selected; SPEC-13 distributes it |
| Eye-offset ceiling | SPEC-12 → SPEC-13 | Existing inherited eye→neck handoff threshold |
| Measured neck yaw | SPEC-02 → SPEC-13 | Outer-loop base error source |
| Configured neck neutral reference | calibration/config → SPEC-13 | Centre of outer-loop unwind |
| Base yaw request | SPEC-13 → SPEC-16 | Slow outer-loop recenter request |
| Motion inhibit | SPEC-16/audio → SPEC-13 | Temporarily removes base from gaze distribution |
| Base safety/veto status | SPEC-16 → SPEC-13 | Causes neck-held degradation |
| Body yaw + yaw rate | SPEC-16 C16-R91 → perception/distribution | Rotating-frame compensation input |
| Swept-envelope clearance/veto | SPEC-16 C16-R60 → SPEC-13 | Gates recruited body rotation |

---

# 7. Quantities requiring validation

Add:

| Quantity | Status | Validation |
|---|---|---|
| Eye→neck ceiling | **Inherited from SPEC-12** | Do not duplicate |
| Normal neck→base engage threshold \(\theta_{engage}\) | **PROVISIONAL** | Simulator + observer + mechanical test |
| Base disengage threshold \(\theta_{disengage}\) | **PROVISIONAL** | Hysteresis test |
| Re-engagement dwell \(T_{reengage}\) | **PROVISIONAL** | Boundary-target test |
| Neck neutral reference \(\theta_{neutral}\) | Configurable | Calibration / character-pose tuning |
| Listening extended yaw \(\theta_{listen,max}\) | **PROVISIONAL** | Neck mechanics + COM/stability + observer test |
| Base recenter slew | **PROVISIONAL** | Integrated neck/base observer test |
| Target-bearing freshness tolerance during rotation | Owned by perception timing contract | Cross-spec validation |

---

# 8. New acceptance tests

## C13-T43 — Ownership-boundary test

Provide SPEC-13 with several already-selected target-bearing commands.

Separately vary SPEC-20 decisions:

- attend;
- ignore;
- follow;
- approach.

### Pass

SPEC-13 only distributes bearings that SPEC-20 has authorised.

No SPEC-13 gaze-distribution state machine independently decides to:

- select another target;
- approach;
- follow;
- ignore.

---

## C13-T44 — Cheapest-sufficient-channel distribution

Place a stationary target at progressively larger horizontal bearings.

### Pass

Observed recruitment proceeds in order:

1. eye offset;
2. neck yaw;
3. base yaw only after the neck escalation condition.

For a bearing fully serviceable by eyes/neck, base rotation does not occur unless a separate authored performance explicitly requests expressive whole-body orientation.

---

## C13-T45 — Inner/outer-loop convergence

Place a stationary target far enough off-axis to recruit the base.

Record:

- compensated target bearing;
- eye offset;
- neck yaw;
- base yaw;
- \(e_{base}\).

### Pass

- eyes/neck track target directly;
- base rotation correlates with neck deflection, not raw target-bearing error;
- as the base turns, neck deflection falls;
- base rotation terminates without persistent hunting.

---

## C13-T46 — Direct target-bearing→base prohibition audit

Inspect runtime control/dataflow and inject a changing target-bearing signal while holding neck-deflection input constant.

### Pass

No distribution base-yaw controller below SPEC-20 responds directly to raw target-bearing error.

Base recruitment depends on the neck-deflection outer-loop state.

Authored body-turn performances remain separately identifiable.

---

## C13-T47 — Eye→neck handoff

Sweep a target from centre outward through the existing SPEC-12 eye-only region.

### Pass

- eye contribution reaches the inherited SPEC-12 ceiling;
- further required bearing recruits neck yaw;
- SPEC-13 contains no second conflicting numeric eye-offset ceiling.

---

## C13-T48 — Neck→base hysteresis boundary

Place a target at a bearing that produces neck yaw near \(\theta_{engage}\).

Introduce only small target/bearing perturbations around the boundary.

Hold for an extended interval.

### Pass

The base does **not** repeatedly:

```text id="boundary_twitch"
engage
→ disengage
→ engage
→ disengage
```

Base engagement follows:

- \(\theta_{engage}\);
- \(\theta_{disengage}\);
- \(T_{reengage}\).

---

## C13-T49 — Listening inhibit and deferred unwind

Place an active speaking target sufficiently off-axis that normal operation would recruit base yaw.

Activate listening-motion inhibit.

### Pass during capture

- base remains stationary;
- eyes + neck retain gaze;
- neck may exceed the normal base-recruitment threshold;
- neck remains inside \(\theta_{listen,max}\).

Clear the inhibit.

### Pass after capture

- base begins a slew-limited body unwind;
- neck progressively recentres;
- no release snap occurs.

---

## C13-T50 — Extended-deflection limits

Command the largest legal listening-state neck deflection across relevant body/base poses.

### Pass

It remains within:

- SPEC-02 mechanical/cable limits;
- applicable SPEC-16 stability envelope.

Any more restrictive physical constraint becomes the effective \(\theta_{listen,max}\).

---

## C13-T51 — Rotating-frame bearing / clean termination

Place a stationary target far enough off-axis to recruit body yaw.

Execute the body turn while target tracking remains active.

Record:

- body yaw/yaw rate;
- compensated target bearing;
- neck yaw;
- base-yaw command.

### Pass

- bearing remains consistent across the manoeuvre;
- stale/uncompensated bearing updates are rejected or not consumed;
- neck deflection decays;
- body rotation terminates cleanly;
- no systematic overshoot/hunting occurs because the target bearing rotated with the body frame.

---

## C13-T52 — Performance override and handback

Recruit base yaw through ordinary gaze distribution.

While tracking, start a performance containing an absolute base-orientation track.

### Pass

During performance:

- authored base orientation has precedence.

At performance release:

- distribution resumes from current measured base/neck pose;
- target fixation resumes/continues;
- no command snaps toward the pre-performance pose.

---

## C13-T53 — Distribution-base veto

Recruit a body turn toward a stationary off-axis target.

Apply in separate runs:

- obstacle/safety veto;
- listening-motion inhibit;
- locomotion fault simulation.

### Pass

In each case:

- base request is withdrawn/vetoed;
- target is not abandoned solely because the base cannot move;
- eyes/neck continue tracking within legal range;
- neck holds the best legal extended deflection.

---

## C13-T54 — Procedural idle during gaze distribution

Hold a target off-axis long enough to recruit neck/base gaze distribution while SPEC-12 procedural life remains enabled.

### Pass

- procedural layer continues evaluating;
- legal micro-offsets remain present;
- pre-procedural arbitration respects reserved headroom;
- post-procedural clamp does not begin routinely firing because gaze distribution consumed the reserve.

---

## C13-T55 — Swept-envelope clearance

Place a target such that gaze distribution requests body yaw.

Run once with valid rotational clearance and once with a SPEC-16 C16-R60 clearance veto.

### Pass

Clear case:

- recruited base recentering proceeds.

Vetoed case:

- body rotation does not proceed;
- eyes/neck retain target as permitted;
- C13-R95 degradation occurs;
- no gaze request bypasses SPEC-16 safety.

---

# 9. Design-review additions

## 9.1 Redundant actuators require one allocation authority

Eye, neck and base yaw are not three independent trackers.

They are three ways of serving one horizontal-attention objective.

Allowing separate controllers to close directly on the same bearing creates a mechanically valid but systemically unstable architecture.

The key distinction is therefore:

\[
\boxed{
\text{eyes/neck close on target bearing}
}
\]

while:

\[
\boxed{
\text{base closes on neck deflection}
}
\]

---

## 9.2 The outer-loop structure removes the oscillation mechanism

The base does not need to know whether the target is "still left."

It only needs to know whether Makad's head is persistently turned left relative to its preferred neutral orientation.

When the body follows:

- gaze keeps target fixation;
- head naturally recentres;
- base error automatically disappears.

This is why an explicit "stop rotating when target is centred" condition is unnecessary and undesirable.

---

## 9.3 Biological resemblance is structurally useful

The sequence resembles biological gaze coordination:

1. fast visual shift;
2. head follows;
3. larger body orientation follows;
4. eyes/head recentre as the slower body catches up.

The resemblance is not decorative.

The same hierarchical timing is what prevents large slow actuators from corrupting the fast attention signal, which is also why it tends to read as natural.

---

## 9.4 Whole-body expression is not the same as tracking necessity

A dramatic body turn can be expressive even when the neck could physically maintain fixation.

Therefore:

> "base is expensive; use it last"

applies to **tracking-driven distribution**.

It does not prohibit an authored performance from deliberately using the body.

That separation avoids turning a control-efficiency rule into an animation restriction.

---

## 9.5 Listening produces a deliberate asymmetric pose

Motion inhibit creates a state in which Makad may be looking strongly sideways with its head while its body remains forward.

That is expected.

Forcing the head back toward centre would sacrifice attention exactly while the person is speaking.

The correct sequence is:

```text id="listening_gaze"
speaker off-axis
    ↓
eyes + head turn
    ↓
base desired but inhibited
    ↓
hold larger head yaw
    ↓
capture ends
    ↓
body turns
    ↓
head recentres
```

---

## 9.6 Base yaw uniquely perturbs its own sensing frame

Eye animation does not move the camera or microphone array.

Neck yaw moves the camera, but not the body-mounted microphone array.

Base yaw rotates:

- camera support frame;
- body;
- microphone array;
- DOA coordinate frame.

It is therefore the attention channel most capable of corrupting the sensory bearing that caused its own command.

C13-R93 prevents this loop from consuming uncompensated/stale bearings.

---

# 10. SPEC-16 cross-spec resolution register

| Interaction | SPEC-16 requirement | SPEC-13 requirement(s) | Resolution |
|---|---|---|---|
| **Channel-arbitration ownership** | **C16-R74** | **C13-R81, C13-R82, C13-R83** | SPEC-16 does not choose eyes vs neck vs base. SPEC-13 owns distribution of an authorised gaze target. |
| **Head/base oscillation identified in SPEC-16 §8.11** | **C16-R74** | **C13-R84, C13-R85, C13-R86** | Eyes/neck close on target bearing; base closes only on neck deflection from neutral. |
| **Listening motion inhibit** | **C16-R109** | **C13-R77, C13-R90, C13-R91, C13-R95** | Base becomes unavailable during capture; neck uses an extended legal envelope and body unwind is deferred. |
| **Rotational swept envelope** | **C16-R60** | **C13-R97, C13-R95** | Distribution-recruited body yaw remains subject to normal rotational-clearance veto. |
| **Rotating body frame** | **C16-R91** | **C13-R93, C13-T51** | Distribution consumes only a bearing compensated consistently with published body yaw/yaw rate. |

---

# 11. Required stub pointers

## SPEC-16 C16-R74

> **Gaze-target allocation across rendered eyes, neck yaw and base yaw is owned by SPEC-13 C13-R81–C13-R86; SPEC-16 does not perform channel arbitration.**

## SPEC-16 §8.11 / C16-R74

> **The head/base oscillation case is resolved normatively by SPEC-13 C13-R84–C13-R86: the fast loop closes on target bearing and the slow base loop closes on neck deflection.**

## SPEC-16 C16-R109

> **Listening-state gaze degradation and deferred body unwind are defined by SPEC-13 C13-R90/C13-R91/C13-R95.**

## SPEC-16 C16-R60

> **Base yaw recruited for gaze recentering remains subject to this swept-envelope requirement; see SPEC-13 C13-R97.**

## SPEC-16 C16-R91

> **SPEC-13 C13-R93 requires gaze distribution to consume a consistently compensated bearing throughout body rotation.**

## SPEC-20 future gaze-policy section

> **SPEC-20 owns whether a target is attended to, followed or approached. Once authorised, channel allocation is delegated to SPEC-13 C13-R81–C13-R97.**

## SPEC-12 eye-offset-ceiling section

> **The existing eye-only/eye-offset ceiling is consumed by SPEC-13 C13-R87 as the eye→neck escalation boundary; SPEC-13 shall not define a duplicate value.**

---

# 12. Final decisions introduced by this amendment

**DECIDED**

- SPEC-13 owns **how** an authorised gaze bearing is distributed.
- SPEC-20 owns **whether** Makad attends, follows or approaches.
- Eye offset, neck yaw and base yaw are one redundant gaze system.
- Ordinary tracking uses cheapest-sufficient-channel ordering:
  \[
  Eyes\rightarrow Neck\rightarrow Base
  \]
- Whole-body expressive intent is a separate reason to use the base.
- Eyes + neck are the fast loop and consume target-bearing error.
- Base yaw is the slow outer loop.
- Base distribution error is:
  \[
  \theta_{neck}-\theta_{neutral}
  \]
  not target bearing.
- Direct target-bearing→base tracking below SPEC-20 is prohibited.
- Eye→neck escalation reuses SPEC-12's existing eye-offset ceiling.
- Neck neutral reference is configurable rather than hard zero.
- Neck→base recruitment uses engage/disengage hysteresis plus re-engagement dwell.
- Base is unavailable for gaze recentering during listening-motion inhibit.
- Neck gets a larger legal listening envelope while the base is inhibited.
- Body recentering occurs after capture with a slew-limited unwind.
- Extended neck deflection remains subject to mechanical and stability limits.
- Rotating-body gaze uses consistently compensated bearings tied to C16-R91 state.
- Absolute performance base tracks override distribution while active.
- Handback resumes from current measured pose without snapping.
- A base veto does not automatically abandon the attended target.
- Procedural idle remains downstream of gaze distribution with reserved headroom.
- Distribution-recruited base rotation remains subject to C16-R60 swept-envelope safety.

**PROVISIONAL**

- neck→base engage threshold;
- neck→base disengage threshold;
- re-engagement dwell;
- extended listening yaw envelope;
- deferred body-unwind slew;
- neck onset ~100 ms;
- base onset 150–400 ms.

**INHERITED / NOT DUPLICATED**

- SPEC-12 eye-offset ceiling.

**DEFERRED TO SPEC-20**

- target selection;
- attend versus ignore;
- follow policy;
- approach policy;
- replacing/abandoning targets.

**NO CHANGE**

- no runtime `current_emotion`;
- affect and performances remain separate;
- perceived-time performance authoring remains intact;
- SPEC-12 retains procedural ownership;
- SPEC-16 retains low-level base safety/control ownership.