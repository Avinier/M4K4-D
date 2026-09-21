# MAKAD — AUDIO ARCHITECTURE DECISION
## 4-Microphone Body-Mounted Array

### DECISION — FROZEN FOR V1

Makad V1 shall use:

\[
\boxed{\textbf{4 digital MEMS microphones}}
\]

mounted in:

\[
\boxed{\textbf{the main body, not the head or ear pods}}
\]

The two external ear pods remain **purely visual/mechanical character elements**.

No microphone, antenna or sensing requirement shall be imposed on the ear pods.

---

# A. Patch to SPEC-04 — Audio / Microphone Subsystem

## A.1 Microphone count

### C4-Rxx — Four-microphone array — MUST

Makad V1 shall use **four digital MEMS microphones** as the primary acoustic capture array.

The array shall support:

- speech capture,
- voice activity detection,
- wake/call detection,
- acoustic echo cancellation support,
- horizontal sound-direction estimation,
- and the directional uncertainty output required by SPEC-11.

A two-microphone primary array is no longer compliant with the intended V1 multimodal speaker-association capability.

---

## A.2 Microphone location

### C4-Rxx — Body-mounted acoustic array — MUST

All four primary microphones shall be mounted in Makad's main body.

They shall not be mounted:

- in the head,
- in the neck,
- or inside the decorative ear pods.

This decision is driven by:

1. increased available acoustic baseline,
2. reduced neck-servo acoustic contamination,
3. fixed loudspeaker-to-microphone geometry for AEC,
4. elimination of head-pose dependence from DOA,
5. elimination of head-rotation DOA smear.

---

## A.3 Ear pods

### C4-Rxx — Ear pods remain visual-only — MUST

Makad's ear pods shall remain mechanical/aesthetic elements only.

The acoustic architecture shall not require wiring or microphone capsules inside them.

This preserves their design freedom and simplifies:

- head assembly,
- head serviceability,
- rotating-head wiring,
- acoustic isolation.

---

# A.4 Array geometry

### C4-Rxx — Non-collinear microphone geometry — MUST

The four microphones shall be arranged in a two-dimensional, non-collinear geometry.

Acceptable candidate geometries include:

- rectangle/square,
- T-shaped geometry,
- another validated asymmetric/non-collinear layout.

A single straight-line four-microphone array shall not be used if it preserves unacceptable front/back ambiguity.

---

### C4-Rxx — Acoustic aperture — MUST

The microphone geometry shall use a substantial fraction of the body width/depth available to it rather than clustering all four capsules unnecessarily close together.

The design objective is to improve TDOA observability and horizontal angular discrimination.

However, maximum spacing shall **not** be pursued blindly.

Final spacing shall be selected after considering:

- usable speech-frequency band,
- spatial ambiguity/aliasing of the selected DOA algorithm,
- body geometry,
- acoustic ports,
- speaker location,
- wheel vibration,
- PCB manufacturability.

Therefore:

\[
\boxed{
\text{large practical aperture}
}
\]

is the design rule rather than:

\[
\boxed{
\text{maximum physically possible spacing at all costs}
}
\]

---

# A.5 Mechanical mounting

### C4-Rxx — Rigid internal array geometry — MUST

The relative position of the four microphones shall remain mechanically fixed after calibration.

Four microphones shall **not** be independently suspended on soft mounts that allow their positions to shift relative to one another.

---

### C4-Rxx — Chassis vibration isolation — MUST

The microphone array shall instead use:

\[
\boxed{
\text{rigid mic PCB/subframe}
\rightarrow
\text{compliant chassis isolation}
}
\]

where practical.

The rigid subassembly preserves calibrated microphone geometry.

The compliant interface reduces structure-borne vibration from:

- drive motors,
- wheel impacts,
- body resonance,
- mechanical actuation.

---

# A.6 Dedicated microphone PCB

### C4-Rxx — Common array PCB — MUST

The four MEMS microphones shall be integrated on a common rigid PCB or equivalently rigid calibrated acoustic subassembly in the final V1 architecture.

The PCB/subassembly shall define:

- microphone positions,
- acoustic-port geometry,
- microphone clock distribution,
- digital capture routing,
- mechanical registration.

Prototype breakout boards may be used during bench development, but they are not the preferred final robot architecture.

---

# A.7 Digital microphone interface

### C4-Rxx — Digital MEMS capture — MUST

The primary array shall use digital MEMS microphone capture.

PDM is the preferred V1 interface unless later electronics integration reveals a compelling reason to select another synchronized digital microphone interface.

No exact microphone model is selected by this requirement.

---

# A.8 Audio clock architecture

### C4-Rxx — Shared audio hardware timebase — MUST

Microphone capture and loudspeaker playback shall derive from a common or coherently disciplined hardware audio timebase.

For a PDM implementation this means, where practicable:

- all microphones share a defined PDM clock architecture,
- PDM capture timing is generated from the primary audio clock tree,
- playback I²S/codec timing derives from the same oscillator/clock domain or from a synchronously related clock,
- capture and playback sample counters can be related without long-term asynchronous drift.

This requirement is about **shared sample-time reference**, not necessarily one literal electrical clock signal for every interface.

---

### C4-Rxx — Capture/playback timestamp coherence — MUST

AEC and downstream fusion shall be able to determine the temporal relationship between:

- captured microphone samples,
- transmitted speaker samples.

Unbounded drift between independent capture and playback clock domains is not acceptable.

---

# A.9 USB microphone arrays

### C4-Rxx — No USB array in final V1 architecture — MUST

The final Makad V1 microphone array shall not depend on a generic asynchronous USB microphone array.

USB audio devices may be used for temporary laboratory experiments.

They shall not define the final architecture because they may introduce:

- an independent audio clock,
- host buffering uncertainty,
- additional transport jitter,
- poorer capture/playback clock coupling,
- unnecessary dependency on USB scheduling.

---

# A.10 AEC geometry

### C4-Rxx — Fixed acoustic echo path geometry — MUST

Makad's primary speaker and microphone array shall both be fixed to the main body such that their relative geometry does not change during normal head movement.

This removes head pose as a variable in the primary loudspeaker-to-microphone echo path.

The AEC system shall still accommodate:

- changing room reflections,
- body movement through the environment,
- nonlinear speaker behaviour,

but shall not be forced to track continuous head-induced speaker/microphone geometry changes.

---

# A.11 Direction estimate output

### C4-Rxx — DOA output — MUST

The audio subsystem shall expose a horizontal body-frame direction estimate where directional evidence is valid.

Example conceptual output:

```text
bearing_azimuth
capture_timestamp
direction_quality
direction_uncertainty
audio_window_start
audio_window_end
```

The exact API is deferred.

---

# A.12 Directional uncertainty

### C4-Rxx — Directional uncertainty output — MUST

SPEC-04 shall provide SPEC-11 with uncertainty/quality accompanying every DOA estimate.

A bare:

```text
bearing = +22°
```

is insufficient.

The output shall provide information equivalent to:

```text
bearing = +22°
uncertainty = ±...
```

or:

```text
bearing = +22°
quality = HIGH / MODERATE / LOW / INVALID
```

Preferably both.

---

# A.13 Derived acoustic performance

SPEC-11 requires useful discrimination between two candidate speakers separated by approximately:

\[
40^\circ
\]

For Gaussian-equivalent combined error:

\[
P(correct)
=
\Phi
\left(
\frac{20^\circ}{\sigma_{total}}
\right)
\]

A 90% correct-association design point requires approximately:

\[
\sigma_{total}
\lesssim15.6^\circ
\]

With visual-bearing error and remaining fusion error consuming part of that budget, the acoustic subsystem shall target:

\[
\boxed{
\sigma_a\le13^\circ
}
\]

---

### C4-Rxx — Installed DOA angular accuracy — MUST

For the validated normal stationary interaction environment, the **installed four-microphone system** shall target an equivalent horizontal directional standard deviation of:

\[
\boxed{
\sigma_a\le13^\circ
}
\]

for speech-like sources within the specified usable interaction region.

This is a derived requirement from SPEC-11 speaker-association performance.

It applies to the completed:

- microphone array,
- body shell,
- acoustic ports,
- electronics,
- signal-processing pipeline,

not to microphone datasheet performance in isolation.

Testing shall separately report:

- median absolute azimuth error,
- 68th-percentile absolute error,
- 90th-percentile absolute error,
- front/back classification errors,
- invalid/ambiguous estimate rate.

If real error distributions are strongly non-Gaussian, percentile metrics shall take precedence over pretending the system has a perfect Gaussian \(\sigma\).

---

# A.14 Body-motion interference

### C4-Rxx — Drive-noise quality gating — MUST

DOA confidence shall account for body-drive interference including:

- wheel motors,
- drivetrain vibration,
- wheel impacts,
- body resonance.

Precise DOA is not required while the acoustic environment is known to be heavily corrupted by locomotion.

---

### C4-Rxx — Base-rotation smear — MUST

Because the microphone array is body-fixed, head angular velocity no longer affects acoustic-array orientation.

However, Makad's **base angular velocity** rotates the entire microphone array.

For a DOA analysis window \(T_w\):

\[
\Delta\theta_{array}
=
\omega_{base}T_w
\]

shall be considered when deciding whether directional evidence remains valid.

At sufficiently high body rotation rates, the DOA estimate shall be:

- uncertainty-widened,
- quality-degraded,
- or invalidated.

---

# B. Patch to SPEC-11

## B.1 Replace existing §2.4 audio statement

### OLD CONCEPT

SPEC-11 treated directional uncertainty/quality as though it were already guaranteed by SPEC-04.

### REPLACEMENT

SPEC-04 supplies the acoustic evidence consumed by SPEC-11.

Following the SPEC-11 design review, SPEC-04 is now explicitly required to provide:

- voice activity,
- wake/call evidence,
- body-frame horizontal DOA,
- DOA uncertainty/quality,
- acoustic-window capture timing,
- AEC/self-audio state,
- audio health.

Directional uncertainty was **not an existing guaranteed interface** before SPEC-11.

It is a **new derived requirement imposed by SPEC-11 on SPEC-04**.

---

# B.2 Remove head-mounted-array assumptions

All SPEC-11 reasoning implying that the microphone array rotates with the head shall be removed.

In particular, audio DOA shall no longer require:

- microphone-to-head transform,
- neck capture-time pose,
- head angular velocity compensation,
- \(\omega_{head}\sigma_t\) acoustic-bearing error,
- head-rotation integration-window smear.

The visual camera path still requires capture-time head pose because the camera remains head-mounted.

---

# B.3 New coordinate relationship

Audio DOA is already expressed in Makad's body frame:

\[
\alpha_{audio}^{body}
\]

Visual person bearing from SPEC-09 is transformed into body frame using capture-time head pose:

\[
\beta_i^{camera}
\rightarrow
\beta_i^{body}
\]

Association therefore compares:

\[
\alpha_{audio}^{body}
\]

against:

\[
\beta_i^{body}
\]

No audio-side neck transform is required.

---

# B.4 Revise cross-modal timing model

The previous association uncertainty included:

\[
(\omega_{head}\sigma_t)^2
\]

because the microphone array was assumed to move with the head.

That term is removed.

A more appropriate model is now:

\[
\sigma_{assoc}^2
=
\sigma_a^2
+
\sigma_v^2
+
\sigma_{motion}^2
+
\sigma_{sync}^2
\]

where:

- \(\sigma_a\) = installed acoustic bearing uncertainty,
- \(\sigma_v\) = visual body-frame bearing uncertainty,
- \(\sigma_{motion}\) = source/base motion during the temporal separation of measurements,
- \(\sigma_{sync}\) = residual temporal-registration contribution.

Head movement only affects the **visual transformation**, which SPEC-08/09 already owns.

---

# B.5 Relax but retain AV temporal registration

The old ≤10 ms requirement existed largely to constrain rapidly changing head orientation on both modalities.

That is no longer necessary.

However:

\[
\boxed{
\text{audio/video synchronization is still required}
}
\]

because a human can move between the acoustic and visual observations, and Makad's base may also move.

Therefore SPEC-11 shall retain a cross-modal time-alignment requirement, but it no longer needs to carry the old head-motion-derived ≤10 ms hard budget.

### Revised requirement

### C11-Rxx — AV capture-time registration — MUST

Audio and visual observations used in direct association shall be mapped to a common monotonic robot timebase.

The residual differential capture-time uncertainty shall be measured and included in fusion quality.

### TARGET

Normal V1 operation should aim for approximately:

\[
\boxed{\le20\,ms}
\]

differential uncertainty where the camera timestamp architecture permits it.

If temporal uncertainty becomes large enough that moving sources could invalidate association, SPEC-11 shall degrade the result instead of forcing a binding.

The final validated threshold shall be set using measured camera timestamp behaviour and moving-speaker tests.

---

# B.6 Remove old head-rotation acoustic test

Any acceptance test whose purpose was:

> rotate the head and verify microphone-array DOA compensation

is deleted.

Head rotation no longer changes microphone-array orientation.

---

# B.7 Replace it with base-rotation test

### C11-Txx — Body-rotation DOA test

Use a stationary sound source.

Measure DOA while Makad's mobile base/body rotates through representative angular rates.

### PASS

The system either:

- preserves validated directional accuracy,
- increases reported uncertainty,
- or invalidates DOA

as body-rotation smear increases.

It shall not continue producing narrow high-confidence DOA estimates once the validated regime has been exceeded.

---

# B.8 Speaker-association acoustic requirement

SPEC-11 shall now explicitly depend on:

\[
\boxed{
4\text{-microphone body array}
}
\]

with an installed design requirement of approximately:

\[
\boxed{
\sigma_a\le13^\circ
}
\]

for the validated stationary interaction case.

This replaces the earlier loose ±15–30° hypothesis.

The ±15–30° figure is no longer an acceptable design assumption.

Actual characterization still determines whether the finished hardware passes.

---

# C. Cross-spec consequences now frozen

## Head

- Camera remains in head.
- No microphone required in head.
- No microphone wires cross the neck joint.
- Ear pods remain visual.
- Head acoustic contamination from neck servos is substantially reduced as an architecture concern.

---

## Body

The body must reserve physical space for:

- four microphone acoustic ports,
- rigid array PCB/subframe,
- mechanical isolation interface,
- digital routing,
- speaker-to-array geometry.

Microphone placement therefore becomes a **body CAD constraint**.

---

## Speaker

The body speaker remains fixed relative to the microphone array.

This becomes the preferred AEC geometry.

---

## Electronics

The audio electronics architecture shall support:

- four synchronized digital microphone channels,
- speaker playback,
- common/related hardware audio clock domain,
- coherent sample timing,
- no final USB-array dependency.

---

## SPEC-11

Speaker association becomes substantially cleaner:

```text
BODY-FIXED MIC ARRAY
        │
        │ DOA already in body frame
        ▼
     SPEC-11
        ▲
        │ visual bearing transformed
        │ to body frame using
        │ capture-time head pose
        │
    SPEC-09
```

The camera remains mechanically dynamic.

The acoustic array becomes mechanically static relative to Makad's body.

That asymmetry is desirable.

---

# D. Final decisions carried forward

### DECIDED

1. Makad V1 uses **4 MEMS microphones**.

2. The microphones are mounted in the **body**.

3. Head-mounted microphones are removed from the architecture.

4. Ear-pod microphones are removed from the architecture.

5. Ear pods remain exactly what they should be: **visual character elements**.

6. The four microphones use a **non-collinear 2-D layout**.

7. Body size is deliberately used to obtain a wider useful acoustic aperture.

8. Final spacing is optimized rather than blindly maximized.

9. The microphones use a **rigid calibrated array PCB/subframe**.

10. That whole assembly may be compliantly isolated from body/drivetrain vibration.

11. Individual microphones shall not float independently on compliant mounts.

12. The final array uses synchronized digital MEMS capture.

13. PDM is the preferred interface.

14. Capture and playback use a common/coherently related **hardware audio timebase**.

15. Final V1 does not depend on a generic USB microphone array.

16. Body speaker + body microphone geometry is fixed for AEC.

17. SPEC-04 must expose **DOA uncertainty/quality**, not merely a bearing.

18. Installed horizontal DOA performance carries a derived:

\[
\boxed{\sigma_a\le13^\circ}
\]

design requirement for the validated speaker-association environment.

19. SPEC-11 no longer transforms acoustic DOA through head pose.

20. SPEC-11 no longer includes head angular velocity in acoustic DOA uncertainty.

21. Head-rotation acoustic smear disappears.

22. Base/body rotation can still smear DOA and remains quality-gated.

23. Cross-modal audio/video timestamping remains required, but the old head-motion-driven ≤10 ms requirement is relaxed.

24. Approximately ≤20 ms differential AV capture-time uncertainty becomes the initial TARGET pending real camera timing characterization.

25. SPEC-11 §2.4 must explicitly state that directional uncertainty is a **new requirement imposed on SPEC-04**, not something SPEC-04 had already guaranteed.

---

## Final sensor geometry

```text
                    ┌───────────────┐
                    │     HEAD      │
                    │               │
 visual ear pod  ◄──┤   DISPLAY     ├──► visual ear pod
                    │    CAMERA     │
                    │               │
                    └──────┬────────┘
                           │
                        NECK
                           │
          ┌────────────────┴────────────────┐
          │              BODY               │
          │                                 │
          │       M1                M2       │
          │                                 │
          │            SPEAKER              │
          │                                 │
          │       M3                M4       │
          │                                 │
          │    compute / audio / power      │
          └─────────────────────────────────┘
```

Exact M1–M4 locations are not yet frozen.

Their design rule is:

\[
\boxed{
\text{wide + non-collinear + rigidly calibrated + acoustically clean}
}
\]

subject to body CAD and prototype characterization.