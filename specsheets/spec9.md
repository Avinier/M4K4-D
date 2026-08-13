# MAKAD — SPEC-09 v1.1 FREEZE CANDIDATE
## Person / Face Detection, Temporal Tracking, Attention Targeting & Social-Gaze Geometry

---

# 1. Scope of this specification

SPEC-09 defines the perception and tracking layer that converts Makad's moving-camera imagery into a **stable, timestamped, uncertainty-aware human attention target** usable by the eyes, head, behaviour system and later mobile base.

The subsystem shall answer:

> **Who is visible, which person is Makad attending to, where is that person relative to Makad at the time of observation, and how certain are we about that estimate?**

SPEC-09 covers:

- person detection;
- face detection/localisation;
- face/person association;
- coarse face orientation estimation;
- temporal multi-person tracking;
- short-term track IDs;
- track lifecycle management;
- attention target selection;
- externally commanded target selection;
- attention-hint input from other modalities;
- target and anchor hysteresis;
- short occlusion handling;
- reacquisition;
- calibrated social-gaze anchor generation;
- moving-camera ego-motion compensation;
- target bearing estimation;
- coarse range use for parallax compensation;
- bearing uncertainty estimation;
- camera/joint timestamp alignment requirements;
- observation freshness;
- prediction and filtering;
- detector duty-cycling;
- perception telemetry and deterministic/reproducible offline replay;
- false-lock behaviour around photographs, displays and mirrors;
- interfaces required by gaze, audio and behaviour systems.

SPEC-09 does **not** define:

- camera/lens electrical selection — SPEC-08;
- neck mechanics or servo control — SPEC-02;
- eye-expression rendering — SPEC-01;
- general object/scene understanding — SPEC-10;
- high-level social-event interpretation — SPEC-11;
- complete behaviour arbitration — SPEC-20;
- collision avoidance — SPEC-18;
- autonomous person-following locomotion — SPEC-19;
- named face recognition;
- biometric identity;
- full-body human pose estimation;
- eye-gaze estimation;
- SLAM;
- safety-grade human distance.

The fundamental separation remains:

\[
\boxed{
\text{Detection}
\neq
\text{Tracking}
\neq
\text{Attention selection}
\neq
\text{Gaze geometry}
\neq
\text{Motor control}
}
\]

---

# 2. Existing Makad decisions that constrain this spec

## 2.1 Moving camera

Makad's camera is rigidly mounted in the moving head.

Raw image motion therefore contains both:

\[
\text{target motion}
+
\text{camera ego-motion}
\]

and cannot be interpreted as target motion alone.

---

## 2.2 Full camera transform

SPEC-08 requires the calibrated camera transform to include both:

\[
R
\quad\text{and}\quad
t
\]

rather than rotation alone.

This is required because camera translation relative to the neck reference centre creates significant close-range parallax.

---

## 2.3 Coarse range is permitted

A coarse target range estimate may be used for gaze geometry.

It may originate from:

- apparent face size;
- body size;
- bounding-box geometry;
- future non-safety range sensing.

This remains categorically different from collision-avoidance depth.

---

## 2.4 Existing camera/gaze targets

Provisional inherited targets include approximately:

- 70–90° horizontal camera FOV;
- ≥720p-class capture;
- ≥30 FPS camera acquisition;
- ~60 px minimum useful face width at the intended maximum social distance;
- ≤250 ms active-mode person acquisition;
- ≤100 ms established visual-target perception latency;
- normal-motion image-quality requirements established by SPEC-08.

SPEC-09 shall not independently redefine these.

---

## 2.5 Distributed gaze

Makad's social gaze is distributed across:

\[
\text{animated eyes}
\rightarrow
\text{physical head}
\rightarrow
\text{body/base when necessary}
\]

SPEC-09 provides target state.

It does not directly command actuators.

---

## 2.6 Physical joint state is authoritative

Camera geometry shall use measured physical neck pose rather than assuming commanded pose equals actual pose.

This creates a direct accuracy interface with SPEC-02.

---

# 3. Engineering reasoning / architecture

# 3.1 Perception chain

The intended architecture is:

```text
CAMERA FRAME + EFFECTIVE CAPTURE TIME
              │
              ↓
      PERSON / FACE DETECTION
              │
              ↓
       FACE LANDMARKS / ORIENTATION
              │
              ↓
   EGO-MOTION-AWARE ASSOCIATION
              │
              ↓
     TEMPORAL PERSON TRACKER
       ├── Track A
       ├── Track B
       └── Track C
              │
              ↓
     ATTENTION TARGET SELECTION
       ↑                ↑
 behaviour command   attention hint
                     audio/other cue
              │
              ↓
       SOCIAL GAZE ANCHOR
              │
              ↓
       PIXEL → CAMERA RAY
              │
              ↓
  COARSE RANGE + PARALLAX MODEL
              │
              ↓
 CAPTURE-TIME CAMERA→NECK TRANSFORM
              │
              ↓
 FILTERED / PREDICTED TARGET BEARING
              │
              ↓
      BEARING + UNCERTAINTY
              │
       ┌──────┴──────┐
       ↓             ↓
      EYES           HEAD
                      │
                      ↓
                BASE REQUEST LATER
```

---

# 3.2 Coordinate-frame convention

Makad shall adopt one explicit coordinate convention across perception and motion.

## Body/head frames

Right-handed:

- \(+X\): forward;
- \(+Y\): left;
- \(+Z\): upward.

## Camera optical frame

Right-handed optical convention:

- \(+Z_c\): forward through optical axis;
- \(+X_c\): image right;
- \(+Y_c\): image down.

Every transform shall explicitly state:

\[
{}^A T_B
\]

as:

> pose of frame \(B\) expressed in frame \(A\).

No subsystem may silently use a different axis or handedness convention.

---

# 3.3 Detection is not temporal tracking

A neural detector operating independently on frames will naturally produce:

- box jitter;
- missed detections;
- confidence variation;
- identity switching;
- unstable gaze.

Therefore detector output shall enter a temporal tracker before becoming a gaze target.

A likely architecture is:

\[
f_\text{camera}\approx30\text{ Hz}
\]

\[
f_\text{detector}\approx10\text{ Hz TARGET}
\]

while temporal prediction/tracking operates at:

\[
f_\text{track}\ge15\text{ Hz MUST}
\]

and preferably close to camera rate.

The detector is therefore **not required to sit on the established-gaze critical path for every frame**.

---

# 3.4 Capture-time pose and clock synchronization

Merely recording timestamps is insufficient.

If camera and neck state differ in time by:

\[
\Delta t
\]

while the head rotates at:

\[
\omega
\]

the resulting angular error is approximately:

\[
\Delta \theta_\text{time}
\approx
\omega\Delta t
\]

At:

\[
\omega=150^\circ/s
\]

a timestamp error of:

\[
10\text{ ms}
\]

causes:

\[
1.5^\circ
\]

of apparent bearing error.

That alone consumes the entire C9-R34 target.

A provisional timing allocation of:

\[
0.3^\circ
\]

therefore requires approximately:

\[
\Delta t
\le
\frac{0.3^\circ}{\omega}
\]

giving:

- at 60°/s → **5 ms**;
- at 100°/s → **3 ms**;
- at 150°/s → **2 ms**.

The correct requirement is therefore not simply:

> “timestamps exist.”

It is:

\[
\boxed{
|\Delta t|_{95}\,|\omega|
\le0.3^\circ
}
\]

for operating conditions where the high-accuracy bearing target is claimed.

---

# 3.5 Camera timestamps require calibration

Many commodity camera timestamps correspond to:

- host arrival;
- driver dequeue;
- USB packet completion;

rather than actual exposure time.

SPEC-09 therefore requires an **effective exposure timestamp**.

This may be achieved using:

1. hardware timestamps/strobe if supported; or
2. empirical exposure-to-system-clock calibration.

For empirical calibration, a repeated visual/electrical event can be recorded to estimate:

- fixed timestamp offset;
- offset variance/jitter;
- outliers.

Subtracting a constant mean delay is useful only if the remaining jitter satisfies the timing error budget.

---

# 3.6 Rolling shutter

Clock synchronization alone does not solve rolling-shutter distortion.

During rolling-shutter exposure, different image rows correspond to different times.

If full-frame readout time is:

\[
t_r
\]

and head angular velocity is:

\[
\omega
\]

the top-to-bottom pose difference may approach:

\[
\Delta\theta_{RS}
\approx
\omega t_r
\]

At fast expressive head speeds this may become several degrees.

Therefore final camera validation must establish:

- global vs rolling shutter;
- effective frame readout time;
- whether face localisation remains inside the bearing-error budget during head motion.

If not, one of the following must occur:

- tracking-mode head slew rate is limited;
- exposure/readout configuration changes;
- row-time compensation is introduced;
- bearing uncertainty is increased during the slew;
- a more appropriate camera is selected.

---

# 3.7 Social gaze anchor

The centre of a full person box is socially unacceptable.

The centre of a face box is also not necessarily correct.

A chin-to-forehead face box typically places the eyes above its geometric centre, and detector bounding-box conventions differ between models.

Therefore target priority shall be:

\[
\boxed{
\text{eye landmark midpoint}
}
\]

when reliable landmarks exist.

Fallback:

\[
\boxed{
\text{detector-specific calibrated face-box offset}
}
\]

followed only then by an upper-body/head-region fallback.

The offset must be measured for the selected detector.

---

# 3.8 Anchor hysteresis

Target identity hysteresis and gaze-anchor hysteresis are separate problems.

If a weak face detector alternates:

```text
eye anchor
→ body fallback
→ eye anchor
→ body fallback
```

the same person can produce an obvious vertical twitch.

The system must therefore retain the higher-quality anchor briefly through intermittent landmark/face loss before falling back.

---

# 3.9 Ego-motion compensation

When the head rotates, the expected visual location of a stationary target changes.

The tracker shall use known camera motion to predict this change.

Conceptually:

\[
\text{predicted observation}
=
f(
\text{previous bearing},
\text{camera motion},
\text{range uncertainty}
)
\]

and association shall use residual error after that prediction.

The requirement is **ego-motion-compensated association**.

It is intentionally implementation-neutral.

Valid implementations may perform association using:

- bearing-space gating; or
- camera-motion-predicted image-space gating.

A literal bearing-space tracker is therefore **not mandated**.

---

# 3.10 Large head slews

A high-speed head movement should not automatically destroy a stable track.

During a commanded or measured slew, the tracker should propagate the target using:

- camera kinematics;
- previous target state;
- bounded target-motion prediction.

Confidence/uncertainty may temporarily widen.

Only genuinely uninformative frames should be rejected.

---

# 3.11 Coarse range and parallax uncertainty

For target ray:

\[
\mathbf r_c
\]

and estimated target distance:

\[
\hat z
\]

the approximate point is:

\[
\mathbf p_c=\hat z\mathbf r_c
\]

and:

\[
\mathbf p_n=
{}^nR_c\mathbf p_c+
{}^n\mathbf t_c
\]

The resulting neck-relative direction is:

\[
\mathbf r_n=
\frac{\mathbf p_n}
{\|\mathbf p_n\|}
\]

For small offsets, range-induced angular error can be approximated by:

\[
\Delta\theta
\approx
b
\left|
\frac{1}{z}
-
\frac{1}{\hat z}
\right|
\]

where \(b\) is the relevant camera-to-reference-centre translation.

Example:

\[
b=50\text{ mm},
\quad
z=0.50\text{ m},
\quad
\hat z=0.65\text{ m}
\]

gives approximately:

\[
\Delta\theta\approx1.32^\circ
\]

Thus a poor range prior can consume nearly the complete 1.5° target.

This creates a real CAD trade:

\[
\boxed{
\text{smaller camera/neck offset}
\quad\text{or}\quad
\text{better range estimate}
}
\]

The final system shall quantify both.

---

# 3.12 Bearing error budget

C9-R34's 1.5° aggregate target shall not exist without subsystem ownership.

The provisional planning budget is:

| Contributor | Provisional allocation | Primary owner |
|---|---:|---|
| Gaze-anchor / landmark localisation | 0.6° | SPEC-09 |
| Camera intrinsics/distortion residual | 0.2° | SPEC-08 |
| Camera/neck extrinsic calibration | 0.3° | SPEC-08/09 integration |
| Physical neck-pose knowledge | 0.5° | SPEC-02 |
| Camera↔pose temporal alignment | 0.3° | SPEC-08/09 integration |
| Range/parallax residual | 0.6° | SPEC-09 + CAD geometry |
| Tracking/filter/prediction residual | 0.4° | SPEC-09 |

For approximately independent zero-mean residuals:

\[
\sigma_\text{combined}
\approx
\sqrt{
\sum_i\sigma_i^2
}
\]

These allocations combine to approximately:

\[
1.22^\circ
\]

leaving integration margin beneath the approximately 1.5° target.

These are **planning allocations**, not permission to leave systematic biases uncorrected.

Systematic errors shall be calibrated out wherever practical.

The final authority remains the measured end-to-end bearing test.

If CAD or prototypes show that one contributor cannot meet its allocation, the error budget shall be consciously rebalanced rather than silently exceeded.

---

# 3.13 Bearing uncertainty

A target bearing shall not be represented as equally trustworthy in every frame.

The system must distinguish:

### Existence confidence

> How likely is this actually a human/person track?

from:

### Association confidence

> How likely is this observation part of the same existing track?

from:

### Bearing uncertainty

> How uncertain are yaw/pitch estimates?

A useful output is:

\[
\Sigma_{\theta}
=
\begin{bmatrix}
\sigma^2_\text{yaw} & \sigma_{\text{yaw,pitch}} \\
\sigma_{\text{yaw,pitch}} & \sigma^2_\text{pitch}
\end{bmatrix}
\]

A simpler V1 implementation may expose independent yaw and pitch standard deviations if covariance proves unnecessary.

This allows the gaze controller to respond differently:

- low uncertainty → decisive physical head movement;
- moderate uncertainty → cautious motion;
- high uncertainty → eye-only adjustment or wait.

---

# 3.14 Face orientation is useful, but not eye gaze

A landmark-capable face pipeline can often estimate coarse face yaw/pitch with little extra computational cost.

SPEC-09 shall therefore expose a coarse estimate such as:

- facing Makad;
- turned left;
- turned right;
- looking/downward head orientation;
- unknown.

However:

\[
\boxed{
\text{head orientation}
\neq
\text{eye gaze}
}
\]

and:

\[
\boxed{
\text{face directed toward Makad}
\neq
\text{proven mutual eye contact}
}
\]

Makad may use face orientation as a social-attention cue but shall not represent it internally as precise eye-gaze detection.

---

# 3.15 Attention hints

Other modalities may know approximately where Makad should look before vision has selected a person.

Example:

\[
\text{sound DOA}
\rightarrow
\text{approximate bearing}
\rightarrow
\text{visual acquisition bias}
\]

SPEC-09 shall therefore accept an attention hint equivalent to:

```text
attention_hint:
    bearing
    angular_uncertainty
    source
    timestamp
    validity
```

An attention hint may:

- bias candidate selection;
- define an acquisition region;
- accelerate reacquisition.

It shall not itself invent a visual human track.

---

# 3.16 Audio-visual association ownership

Matching:

> “this sound bearing”

to:

> “this visual person track”

is a cross-modal attention decision.

SPEC-09 shall expose sufficient candidate-track geometry.

The audio subsystem shall expose sound-direction information.

**SPEC-20 / central attention arbitration is assigned ownership of audio-visual association** unless later architecture work justifies extracting it into a dedicated fusion module.

This dependency is now explicitly named rather than left ownerless.

---

# 3.17 Default target-selection policy

SPEC-20 will ultimately own behaviourally meaningful attention.

However SPEC-09 requires deterministic behaviour before SPEC-20 exists.

Default V1 policy:

1. retain currently selected valid target;
2. if no target exists, select the confirmed person whose gaze anchor lies closest to the current camera optical axis;
3. use detection/track confidence as a tie-breaker;
4. prefer a plausible face-bearing track over a body-only candidate when otherwise comparable;
5. do not continuously rescore and switch while the selected target remains valid.

This is a fallback policy, not Makad's final social-attention intelligence.

---

# 3.18 Track-capacity overflow

The currently selected attention target shall be **pinned**.

If track capacity is exceeded, eviction shall occur among non-selected tracks according to criteria such as:

- staleness;
- low confidence;
- short lifetime;
- weak association.

A newly appearing person shall never evict Makad's current interaction partner solely because capacity was reached.

---

# 3.19 Active and idle vision modes

Running a full detector continuously may waste:

- compute;
- power;
- thermal headroom.

SPEC-09 therefore supports at least:

### ACTIVE TRACKING

Used during interaction or after an attention cue.

Target:

\[
f_\text{detector}\approx10\text{ Hz or higher}
\]

### IDLE PRESENCE MODE

Lower-rate human-presence scanning.

Initial TARGET:

\[
2-5\text{ Hz}
\]

or equivalent low-power strategy.

The ≤250 ms acquisition requirement applies to ACTIVE mode.

Idle acquisition may be slower.

Initial TARGET:

\[
\boxed{\le1.0\text{ s}}
\]

from a person becoming visually observable until promotion to active tracking.

Audio or another attention cue may immediately wake ACTIVE mode.

---

# 3.20 Photographs, screens and mirrors

A normal face detector may detect:

- posters;
- photographs;
- phone/tablet screens;
- television faces;
- mirrors.

These shall be considered **known false-lock classes**.

Camera-motion parallax alone is **not considered a reliable liveness discriminator**.

A face displayed on a flat screen can exhibit camera-motion geometry consistent with the physical screen depth.

A mirror can be even more ambiguous.

V1 therefore does not promise robust real-person liveness detection.

Instead:

- these cases shall be tested;
- their behaviour shall be documented;
- they shall never feed safety-critical reasoning;
- inexpensive heuristics may be used if validated;
- stronger anti-spoof/liveness methods remain optional later work.

---

# 3.21 Reproducible offline replay

Tracking development must not require a human subject for every filter change.

Validation recordings shall therefore support offline replay of:

- raw frames;
- effective camera timestamps;
- timestamped neck-state data;
- calibration data;
- configuration/model version.

The replay system should reproduce outputs deterministically where the backend permits.

Bit-identical GPU inference is **not universally guaranteed** because some accelerated kernels are nondeterministic.

Therefore the requirement is:

\[
\boxed{
\text{reproducible within defined numerical/track-state tolerances}
}
\]

with deterministic execution enabled when technically available.

---

# 3.22 Camera-data privacy

Persistent raw-video logging shall **not** be required for normal Makad operation.

Default normal-operation telemetry should consist primarily of derived metadata.

Raw frames may be recorded during:

- explicit engineering validation;
- debugging;
- user-authorised dataset collection.

Such recording should be:

- opt-in;
- local by default;
- bounded in retention;
- visibly distinguishable from ordinary operation in the software/debug state.

Precise product privacy policy remains outside this subsystem spec, but the architecture shall not require cloud video retention.

---

# 3.23 Nominal Validation Envelope

The phrase **“nominal conditions”** shall mean the following unless a particular requirement defines a different envelope.

### Lighting

Indoor illumination at the subject approximately:

\[
\boxed{100-1000\text{ lux TARGET}}
\]

without extreme direct backlighting or camera saturation.

### Target size

Face width:

\[
\boxed{\ge60\text{ px}}
\]

when face-specific performance is claimed.

### Image position

For the 1.5° precision target:

central useful calibrated FOV, initially defined as approximately the central 80% of image width/height after distortion handling.

Detection may operate outside this region without being required to satisfy maximum bearing accuracy.

### Human movement

Standing, seated, normal head motion and ordinary indoor walking.

### Camera motion

The tracker shall remain operational during the intended head-motion envelope.

The tightest absolute-bearing target may be relaxed during extreme expressive slews if the reported bearing uncertainty correctly reflects the degradation.

### Scene

Ordinary indoor backgrounds, including furniture and moderate clutter.

The NVE is a validation definition, not a claim that Makad fails immediately outside it.

---

# 4. Formal requirements

## Detection and tracking

### C9-R01 — Human detection — MUST

Detect human/person candidates in the validated operating envelope.

Each detection shall provide at minimum:

- image location;
- confidence;
- frame/effective-capture timestamp.

---

### C9-R02 — Face localisation — MUST

Where a sufficiently visible face exists, localise the face separately from the full person.

---

### C9-R03 — Face/person association — MUST

Associate a valid face detection with the corresponding temporal person track.

---

### C9-R04 — Coarse face orientation — MUST

Where suitable facial landmarks are available, expose a coarse head/face-orientation estimate and confidence.

This is not eye-gaze estimation.

---

### C9-R05 — No biometric identity requirement — MUST

Named face recognition, biometric enrolment and long-term human identity are not required by SPEC-09.

---

### C9-R06 — Nominal Validation Envelope — MUST

Requirements referring to nominal/validated conditions shall use §3.23 unless explicitly stated otherwise.

---

### C9-R07 — Minimum face-size target — TARGET

Reliable face-specific tracking shall target operation with visible face width approximately:

\[
\ge60\text{ px}
\]

pending camera/detector benchmarking.

---

### C9-R08 — Active acquisition latency — MUST

In ACTIVE mode, a newly visible person satisfying the validation envelope shall normally become a confirmed candidate track within:

\[
\boxed{\le250\text{ ms}}
\]

---

### C9-R09 — Idle acquisition — TARGET

In IDLE presence mode, a newly visible person should trigger active visual tracking within approximately:

\[
\boxed{\le1.0\text{ s}}
\]

under nominal conditions.

---

### C9-R10 — Established tracking rate — MUST

Selected-target state shall update at:

\[
\boxed{\ge15\text{ Hz}}
\]

under representative operating load.

TARGET:

\[
\approx30\text{ Hz}
\]

---

### C9-R11 — Detector refresh — TARGET

Active human/face detection should achieve approximately:

\[
\ge10\text{ Hz}
\]

while lighter temporal tracking may run more frequently.

---

## Time and coordinate integrity

### C9-R12 — Effective capture timestamps — MUST

Every observation used for gaze control shall have an effective image-capture timestamp rather than relying only on host arrival time.

---

### C9-R13 — Camera↔joint-state temporal alignment — MUST

Residual temporal alignment error shall satisfy:

\[
\boxed{
|\Delta t|_{95}\,|\omega|
\le0.3^\circ
}
\]

for motion conditions where the high-accuracy bearing target is claimed.

At 150°/s this implies approximately:

\[
|\Delta t|_{95}\le2\text{ ms}
\]

unless the system deliberately widens uncertainty or relaxes gaze accuracy during that motion.

Both mean offset and residual jitter shall be measured.

---

### C9-R14 — Pose interpolation — MUST

Camera transforms shall use measured neck pose corresponding to effective image capture time.

Interpolation between timestamped joint states shall be supported where required.

---

### C9-R15 — Rolling-shutter characterisation — MUST

If the selected camera uses rolling shutter, effective frame/row readout timing shall be characterised.

If rolling-shutter motion error materially exceeds the gaze-bearing error budget, the architecture shall mitigate or explicitly degrade uncertainty/accuracy during affected motions.

---

### C9-R16 — Coordinate-frame convention — MUST

All SPEC-09 transforms shall use the frame conventions defined in §3.2.

Frame IDs and units shall be explicit in software interfaces.

---

## Temporal tracks

### C9-R17 — Persistent temporal tracks — MUST

Human observations shall be associated across frames into short-term persistent tracks.

Each active track shall expose at least:

- track ID;
- person box;
- face box where available;
- gaze anchor;
- track state;
- confidence;
- timestamp;
- observation age.

---

### C9-R18 — Track lifecycle — MUST

Tracks shall distinguish states equivalent to:

- tentative;
- confirmed;
- temporarily occluded;
- lost.

---

### C9-R19 — Short occlusion tolerance — TARGET

Confirmed tracks should survive brief missing observations for approximately:

\[
0.3-0.7\text{ s}
\]

before being irrecoverably declared lost.

Final timing shall be empirically tuned.

---

### C9-R20 — Reacquisition — MUST

A briefly occluded target reappearing consistently with the predicted track shall preferentially reacquire the previous temporary identity.

No biometric recognition is required.

---

### C9-R21 — Multiple-person tracking — MUST

At least two simultaneously visible people shall be representable as independent tracks.

TARGET:

\[
\ge3
\]

under normal indoor conditions.

---

### C9-R22 — Selected-target protection — MUST

Track-capacity overflow shall never evict the currently selected valid attention target solely to admit a new candidate.

---

## Attention selection

### C9-R23 — Candidate versus selected target — MUST

The subsystem shall distinguish:

- visible candidate tracks;
- selected attention track.

---

### C9-R24 — Target-lock hysteresis — MUST

Small detection-confidence variations shall not change the selected person.

Switching requires:

- explicit selection command;
- target invalidation/loss;
- higher-level attention arbitration.

---

### C9-R25 — Default selection policy — MUST

When no external behaviour preference exists:

1. retain an existing valid target;
2. otherwise select the confirmed human whose gaze anchor is nearest the camera optical axis;
3. resolve close ties using track quality/confidence.

---

### C9-R26 — External selection contract — MUST

The behaviour system shall be able to:

- select a track by current track ID;
- clear selection;
- request acquisition near a bearing/attention hint.

A command referring to a track that has become invalid before execution shall return an invalid/stale-target result rather than silently selecting another person.

---

### C9-R27 — Attention-hint input — MUST

SPEC-09 shall accept a time-bounded external attention hint containing at minimum:

- bearing;
- angular uncertainty;
- source;
- timestamp/age.

Hints may bias acquisition but shall not constitute visual proof that a person exists.

---

## Gaze anchor

### C9-R28 — Landmark-derived gaze anchor — MUST

Where valid eye landmarks are available, the preferred social-gaze anchor shall be derived from the eye region rather than the raw face-box centre.

---

### C9-R29 — Calibrated fallback anchor — MUST

Where landmarks are unavailable but a face remains valid, fallback anchor position shall use a detector-specific empirically calibrated face-box fraction.

A generic assumption of face-box centre is insufficient.

---

### C9-R30 — Upper-body fallback — MUST

When the face is temporarily unavailable but the person remains confidently tracked, a stable estimated head/upper-body anchor may be used.

---

### C9-R31 — Anchor hysteresis — MUST

Intermittent face/landmark loss shall not cause frame-by-frame switching between face and body anchors.

Anchor transitions shall use persistence/hysteresis.

---

## Geometry and ego motion

### C9-R32 — Camera-ray representation — MUST

Selected targets shall be expressible as calibrated camera-frame rays, not only pixels.

---

### C9-R33 — Ego-motion-compensated association — MUST

Temporal association during head/body movement shall predict the effect of measured camera motion before deciding whether visual displacement represents target movement.

This may operate in bearing space or motion-predicted image space.

---

### C9-R34 — Full camera transform — MUST

Transformation from camera coordinates shall use full calibrated translation and rotation.

---

### C9-R35 — Coarse range prior — MUST where geometrically required

Where camera translation materially affects reference-frame bearing, coarse range shall be used for parallax compensation.

---

### C9-R36 — Range uncertainty propagation — MUST

Range estimation shall expose uncertainty sufficient to estimate its contribution to angular bearing uncertainty.

If predicted parallax uncertainty alone threatens the bearing budget, the system shall either:

- widen target-bearing uncertainty;
- improve range estimation;
- reduce the relevant camera/neck offset through CAD;
- restrict the high-accuracy operating envelope.

---

### C9-R37 — Non-safety range classification — MUST

Range generated by this perception layer shall be explicitly treated as approximate/non-safety data.

---

## Accuracy and latency

### C9-R38 — Aggregate target-bearing accuracy — TARGET

Under the Nominal Validation Envelope and central useful FOV:

\[
\boxed{
95^\text{th}\text{-percentile absolute bearing error}
\le1.5^\circ
}
\]

TARGET.

Minimum acceptable V1:

\[
\boxed{\le3^\circ}
\]

The provisional error allocations in §3.12 shall be used during subsystem design.

---

### C9-R39 — Stationary target jitter — TARGET

For a settled stationary target:

\[
\boxed{\le0.5^\circ\ RMS}
\]

unintended filtered bearing variation per relevant axis.

---

### C9-R40 — No raw-box servo control — MUST

Raw detector box positions shall never directly control neck actuators.

---

### C9-R41 — Established perception latency — MUST

Under ACTIVE tracking:

\[
\boxed{
t_\text{target published}
-
t_\text{effective capture}
\le100\text{ ms}
}
\]

at the 95th percentile under representative Makad compute load.

Detector refresh does not need to block every established track update.

---

### C9-R42 — Per-stage latency instrumentation — MUST

The perception pipeline shall expose timing for at least:

- camera capture/readout/availability;
- detector/tracker processing;
- landmarks/anchor;
- transforms;
- filtering/prediction;
- publication/IPC.

Initial planning allocation:

| Stage | Planning budget |
|---|---:|
| Frame availability / transport | ≤35 ms |
| Tracker / landmarks | ≤30 ms |
| Geometry / filtering | ≤10 ms |
| Scheduling / IPC | ≤15 ms |
| Integration reserve | ≥10 ms |

These are planning allocations and may be rebalanced provided C9-R41 remains satisfied.

---

### C9-R43 — System-visible reaction owner — MUST dependency

The complete:

\[
\text{image capture}
\rightarrow
\text{visible physical head response}
\]

latency is **not owned by SPEC-09**.

It shall be owned by the eventual **Makad Master System Timing / Integration Budget**, combining:

- SPEC-09 perception latency;
- behaviour/gaze arbitration;
- communications;
- SPEC-02 actuator/control latency;
- mechanical rise time.

SPEC-09 shall publish sufficient timestamps for that total to be measured.

---

## Motion and prediction

### C9-R44 — Head-motion robustness — MUST

Normal programmed Makad head movement shall not by itself create persistent target loss or self-excited visual tracking oscillation.

---

### C9-R45 — Kinematic prediction through slews — MUST

During known head motion, the tracker shall predict expected target observation from camera kinematics rather than simply treating all camera motion as degraded target motion.

---

### C9-R46 — Bounded target-motion prediction — TARGET

For smoothly moving people, short-term target angular velocity may be estimated to compensate pipeline delay.

---

### C9-R47 — Prediction decay — MUST

Prediction shall decay or terminate rapidly after observations become unavailable.

The system shall not generate indefinitely confident extrapolated human positions.

---

### C9-R48 — Motion-quality degradation — MUST

Blur, rolling-shutter distortion, poor lighting or other image-quality failures shall reduce bearing confidence/increase uncertainty rather than masquerade as accurate measurements.

---

## Confidence and output contract

### C9-R49 — Confidence semantics — MUST

At minimum, the architecture shall distinguish:

- person/existence confidence;
- track/association quality;
- angular bearing uncertainty.

One undifferentiated “confidence” number is insufficient.

---

### C9-R50 — Bearing uncertainty output — MUST

The selected-target output shall expose yaw/pitch uncertainty, either as:

- covariance; or
- independent angular uncertainty values for V1.

---

### C9-R51 — Gaze output interface — MUST

Selected-target state shall expose at minimum:

- selected track ID;
- target bearing;
- bearing uncertainty;
- existence confidence;
- track state;
- observation timestamp;
- observation age;
- target-visible state.

Optional useful values include:

- target angular velocity;
- coarse range + uncertainty;
- face orientation;
- bounding boxes.

---

### C9-R52 — Lost-target state — MUST

Lost/stale targets shall produce an explicit lost state.

SPEC-09 shall not autonomously initiate uncontrolled head scanning.

---

### C9-R53 — Face/head orientation output — MUST

When reliable, coarse face yaw/pitch or orientation category shall be exposed with confidence.

It shall not be labelled as eye gaze.

---

### C9-R54 — Eye/head shared target — MUST

Animated eyes and physical head gaze shall ultimately reference the same selected human target.

---

### C9-R55 — Joint-limit exposure — MUST

If the target lies outside the useful head tracking envelope, that condition shall be exposed so another subsystem may decide whether body/base rotation is appropriate.

---

## Compute, replay and privacy

### C9-R56 — Compute coexistence — MUST

V1 performance requirements shall hold while representative Makad subsystems are simultaneously operating.

---

### C9-R57 — Replaceable perception backend — TARGET

Detector/tracker implementation should be replaceable without rewriting gaze-control logic.

---

### C9-R58 — Duty-cycled operation — MUST

The architecture shall support at least:

- active tracking mode;
- lower-compute idle presence mode.

---

### C9-R59 — Diagnostic telemetry — MUST

Logs shall include enough data to reconstruct perception decisions, including:

- timestamps;
- track IDs;
- detection/association confidence;
- selected target;
- anchor type;
- anchor coordinates;
- bearing;
- bearing uncertainty;
- coarse range where used;
- neck pose used;
- latency stages;
- track switches/loss/reacquisition.

---

### C9-R60 — Raw-frame logging policy — MUST

Normal operation shall not require persistent raw-video recording.

Raw-frame recording for engineering purposes shall be explicit and local by default.

---

### C9-R61 — Offline replay — MUST

Recorded engineering sessions shall support offline replay using:

- raw frames;
- effective capture timestamps;
- joint-state history;
- calibration;
- software/model configuration.

Replays shall be deterministic where technically supported and otherwise reproducible within documented tolerances.

---

### C9-R62 — Degraded/fault state — MUST

If tracking cannot be trusted because of:

- unavailable camera;
- stale frames;
- failed temporal calibration;
- invalid extrinsics/intrinsics;
- unavailable joint state;
- processing overload;

closed-loop gaze output shall enter a degraded/fault state.

---

### C9-R63 — Appearance-coverage validation — MUST

Validation shall include human subjects/test imagery spanning representative variation in:

- skin tone;
- glasses;
- facial hair;
- head coverings;
- hair styles;
- lighting direction/intensity.

Because the prototype sample size will be small, the team shall report observed failures rather than make unjustified statistical fairness claims.

---

### C9-R64 — Screen/photo/mirror handling — MUST validation item

Photographs, displays and mirrors shall be explicitly treated as known challenging false-lock cases and included in validation.

Robust liveness rejection is not a V1 requirement.

---

# 5. Interfaces and dependencies

## SPEC-01 — Animated Face

Consumes:

- selected target;
- target bearing;
- target uncertainty;
- attention state.

Eye animation may respond faster than the head but must not silently select a different person.

---

## SPEC-02 — Head Mechanics & Control

Must provide:

- timestamped measured physical joint state;
- sufficiently accurate pose knowledge;
- neck kinematic model;
- joint limits;
- motion state.

### Derived SPEC-02 interface requirement

The provisional bearing budget allocates approximately:

\[
0.5^\circ
\]

to uncertainty in physical neck-pose knowledge.

This is not automatically equivalent to actuator command repeatability; it refers to how accurately SPEC-09 knows the **actual camera-bearing pose** at exposure time.

---

## SPEC-06 / Audio Perception

Future sound-localisation output may produce:

- sound bearing;
- uncertainty;
- timestamp.

SPEC-09 accepts this as an attention hint.

---

## SPEC-08 — Camera

Must provide/allow determination of:

- frames;
- intrinsics;
- distortion parameters;
- camera-to-head extrinsics;
- effective capture timestamps;
- exposure/readout characteristics;
- camera health.

### Derived CAD requirement

Final CAD must measure:

\[
{}^n\mathbf t_c
\]

rather than treating camera offset as negligible.

If that translation makes range/parallax error dominate C9-R38, either CAD geometry or the range estimator must change.

---

## SPEC-10 — General Visual Understanding

General object/scene perception shall not block the real-time human-gaze path.

---

## SPEC-11 — Social Event Detection

May consume:

- human track appeared/disappeared;
- track count;
- face orientation;
- target state.

SPEC-11 owns social interpretation, not basic tracking.

---

## SPEC-19 — Perception-Controlled Locomotion

May later consume:

- target bearing;
- bearing uncertainty;
- target visibility;
- head-envelope saturation;
- coarse target motion.

SPEC-09 does not issue wheel commands.

---

## SPEC-20 — Central Behaviour / Attention Arbitration

Owns final social significance such as:

- who Makad wants to attend to;
- switching interaction partners;
- audio-visual cue association;
- response to someone speaking/calling;
- behaviour-driven target changes.

SPEC-09 supplies tracks and deterministic fallback behaviour.

---

## MASTER SYSTEM SPEC

The consolidated Makad master specification shall own the complete:

\[
\text{perception}
\rightarrow
\text{decision}
\rightarrow
\text{motor}
\rightarrow
\text{visible response}
\]

latency budget.

---

# 6. Quantities still requiring CAD / prototype / component validation

The following remain deliberately unresolved.

## 6.1 Camera-to-neck translation

Full vector:

\[
{}^n\mathbf t_c
\]

must come from CAD/measurement.

Once known, it determines how demanding the range prior must be.

---

## 6.2 Range estimator accuracy

Final requirement shall follow from:

\[
\Delta\theta
\approx
b
\left|
\frac1z-\frac1{\hat z}
\right|
\]

and the allocated parallax-error budget.

---

## 6.3 Camera timing characteristics

Need measurement of:

- exposure timing;
- host timestamp offset;
- jitter distribution;
- rolling-shutter readout time.

---

## 6.4 Detector/tracker backend

Not frozen.

---

## 6.5 Landmark backend

Not frozen.

---

## 6.6 Calibrated gaze-anchor offset

Must be measured for the actual detector if landmark fallback is used.

---

## 6.7 Occlusion and anchor hysteresis timing

Prototype tuning required.

---

## 6.8 Filter/predictor parameters

Prototype tuning required against both:

- jitter;
- latency.

---

## 6.9 Face-orientation accuracy

Final useful bins/thresholds require validation with the selected landmark model.

---

## 6.10 Idle detection rate

Final duty cycle depends on:

- compute;
- power;
- temperature;
- active-wake latency.

---

## 6.11 Maximum simultaneous tracks

Architecture shall support multiple people but final resource limit depends on compute benchmarking.

---

## 6.12 High-speed tracking envelope

Need integrated testing to determine at what combination of:

- head angular velocity;
- exposure;
- rolling shutter;
- timing jitter;

the 1.5° target must temporarily be relaxed.

---

# 7. Acceptance tests

## C9-T01 — Active human acquisition

Run at least 20 representative acquisition trials under the NVE.

### Pass

At least 18/20 valid trials produce a confirmed track within:

\[
250\text{ ms}
\]

---

## C9-T02 — Eye-line gaze-anchor calibration

For the selected detector/landmark system, present frontal and mildly rotated faces at known positions.

Compare:

- face-box centre;
- chosen gaze anchor;
- measured eye-line position.

### Pass

The selected anchor is calibrated to the eye region rather than merely lying somewhere within the face box.

Angular anchor bias shall remain compatible with the C9-R38 budget.

---

## C9-T03 — Face-loss / body-track continuity

Track a person while they turn their face sideways/away and back.

### Pass

Body-track continuity prevents unnecessary person loss where the human remains visually trackable.

---

## C9-T04 — Camera↔pose temporal alignment test

Generate repeated, measurable motion or visual/electrical timing events.

Estimate effective camera exposure timing relative to the joint-state clock across at least:

\[
100
\]

samples.

Record:

- mean offset;
- standard deviation;
- 95th-percentile residual;
- outliers.

### Pass

After fixed-offset correction:

\[
|\Delta t|_{95}|\omega|
\le0.3^\circ
\]

for the validated tracking-motion envelope.

A mean-only result does not pass.

---

## C9-T05 — Rolling-shutter motion test

Observe a stationary calibrated target while moving the head at several angular velocities.

### Pass

The resulting row/readout-related bearing error is either:

- inside the allocated error budget; or
- correctly reflected by increased uncertainty/degraded-state handling.

---

## C9-T06 — Aggregate bearing accuracy

Place a known target at multiple:

- yaw angles;
- pitch angles;
- distances;
- head poses.

### V1 pass

\[
95^\text{th}\text{ percentile error}\le3^\circ
\]

### TARGET

\[
95^\text{th}\text{ percentile error}\le1.5^\circ
\]

through the central useful FOV.

---

## C9-T07 — Error-budget attribution

For C9-T06 failures, separately quantify where practical:

- anchor bias;
- intrinsic/extrinsic calibration;
- pose error;
- timing error;
- parallax/range error;
- tracker/filter residual.

### Pass

A missed total bearing target can be assigned to measurable contributors rather than remaining unexplained.

---

## C9-T08 — Stationary-target jitter

Track a stationary target for at least 30 s after settling.

### TARGET

\[
\le0.5^\circ\ RMS
\]

per relevant axis.

---

## C9-T09 — Moving-person tracking

Track a person walking laterally at ordinary indoor speed.

### Pass

Track identity and bearing evolve continuously through the majority of the traverse without rapid ID switching.

---

## C9-T10 — Ego-motion association test

Keep a person physically stationary.

Move Makad's head through representative yaw/pitch trajectories.

### Pass

Known camera motion does not cause persistent track loss or false target-motion estimation.

This test shall include a faster slew, not only slow tracking movement.

---

## C9-T11 — Close-range parallax test

At several known ranges and camera/head poses, compare:

1. rotation-only geometry;
2. full transform;
3. full transform + configured range prior.

### Pass

The implemented full geometry reduces close-range systematic bearing error as predicted.

Reported uncertainty shall increase when the range prior becomes insufficient.

---

## C9-T12 — Two-person lock test

Select Person A.

Allow Person B to:

- move;
- approach image centre;
- become larger;
- temporarily have greater detector confidence.

### Pass

Person A remains selected while valid.

---

## C9-T13 — Anchor hysteresis test

Operate near the face/landmark detection threshold so face landmarks intermittently appear/disappear.

### Pass

The physical gaze anchor does not repeatedly jump between eye-line and torso fallback.

---

## C9-T14 — Short occlusion

Briefly occlude the selected target within configured persistence duration.

### Pass

Track enters occluded/predicted state and preferentially reacquires the target.

---

## C9-T15 — Long disappearance

Remove target beyond the lost timeout.

### Pass

Track becomes LOST and prediction does not continue indefinitely.

---

## C9-T16 — Track-capacity overflow

Fill the tracker to its configured track capacity while one track is selected.

Introduce additional people/candidates.

### Pass

The selected target is not evicted solely because capacity was exceeded.

---

## C9-T17 — Attention-hint acquisition

Begin without a selected visual target.

Provide an attention hint near one of multiple candidate people.

### Pass

The hint appropriately biases acquisition without itself creating a fake person track.

---

## C9-T18 — Stale track-selection command

Obtain a track ID, allow it to die, then issue selection for that old ID.

### Pass

The system returns invalid/stale target and does not silently substitute a different human.

---

## C9-T19 — Face-orientation test

Present a person facing:

- approximately toward Makad;
- left;
- right;
- downward/away.

### Pass

The coarse orientation output changes meaningfully and reports uncertainty/unknown where inappropriate.

No eye-gaze claim is made.

---

## C9-T20 — False-lock media test

Present:

- printed face;
- face on phone/tablet;
- television/video face;
- mirror reflection;
- real nearby person.

### Requirement

Record detector/tracker behaviour for each.

### Pass

V1 need not reject all spoof cases.

However:

- failures must be documented;
- none may be interpreted as safety-critical human ranging;
- persistent false-lock behaviour must be understood before final demonstration.

---

## C9-T21 — Empty-scene false-track test

Operate for at least 10 minutes in a representative empty room.

### Pass

No false detection remains a confirmed persistent human attention target for more than approximately 1 s.

---

## C9-T22 — Observation-age / stale-data test

Introduce deliberate perception delay or pause input.

### Pass

Observation age rises and closed-loop gaze becomes degraded/inhibited rather than following stale measurements.

---

## C9-T23 — Latency decomposition test

Measure the distribution of each C9-R42 pipeline stage under representative load.

### Pass

Overall established perception latency satisfies:

\[
P95\le100\text{ ms}
\]

and no unexplained timing segment remains.

---

## C9-T24 — Compute coexistence

Run representative simultaneous:

- vision;
- face animation;
- audio capture;
- audio processing;
- head communication;
- behaviour logic.

### Pass

Tracking-rate and latency MUST requirements remain satisfied without persistent thermal/compute saturation.

---

## C9-T25 — Idle duty-cycle test

Operate in IDLE presence mode.

Measure:

- detector rate;
- compute utilisation;
- wake latency;
- transition to ACTIVE tracking.

### TARGET

Person acquisition from idle:

\[
\le1.0\text{ s}
\]

under the NVE.

---

## C9-T26 — Offline replay

Record a complete validation sequence containing:

- raw video;
- calibrated timing;
- joint states;
- target switches;
- occlusion.

Replay without a person physically present.

### Pass

The processing pipeline reproduces track state and numerical outputs within documented deterministic/reproducibility tolerances.

---

## C9-T27 — Appearance-coverage test

Repeat representative human acquisition/tracking tests using subjects/test material varying:

- skin tone;
- glasses;
- facial hair;
- head coverings;
- lighting.

### Pass

Observed failures are recorded and no obvious category is systematically excluded from the tested operating envelope without documentation.

No statistically unsupported population-level fairness claim shall be made.

---

## C9-T28 — Raw-frame privacy/default test

Operate Makad normally with engineering recording disabled.

### Pass

Persistent raw camera frames are not written merely because the person tracker is operating.

---

## C9-T29 — Coordinate-frame unit test

Inject synthetic known rays/transforms for:

- centre;
- left;
- right;
- above;
- below.

### Pass

All frame conversions produce expected sign and direction under the §3.2 convention.

This test should run automatically in software CI/replay tooling.

---

# 8. Internal consistency / design review

## 8.1 Timestamp existence was not enough

The earlier spec correctly demanded capture-time pose but did not define whether the two time domains were aligned accurately enough.

That left a hidden error potentially larger than the complete gaze budget.

The specification now owns:

\[
|\Delta t|_{95}|\omega|\le0.3^\circ
\]

rather than merely “timestamps shall exist.”

---

## 8.2 Rolling shutter remains a possible budget killer

Even after clock calibration, a rolling-shutter camera can encode multiple camera poses into one frame during fast head motion.

This can become more important than neural-network localisation accuracy.

Therefore camera selection later cannot be based on resolution/FPS alone.

---

## 8.3 Eye-line anchoring is required

A face box is a region detector, not a gaze target.

The earlier test could have passed while Makad systematically stared several degrees too low.

Eye landmarks or detector-specific calibration now close that gap.

---

## 8.4 The 1.5° target now has owners

The earlier aggregate target was not actionable.

The provisional error budget now provides interfaces to:

- SPEC-02;
- SPEC-08;
- CAD;
- SPEC-09 itself.

These allocations should **not** be treated as immutable numbers.

Their purpose is to make integration failure diagnosable.

---

## 8.5 Camera offset may force a mechanical change

At close range, a 50 mm offset combined with a mediocre monocular range estimate can consume most of the total bearing target.

Therefore:

> “we'll fix it in software”

is not automatically acceptable.

Once CAD exposes actual camera-to-neck translation, the project must consciously choose among:

- reducing the offset;
- improving coarse range;
- relaxing near-field accuracy;
- accepting wider bearing uncertainty.

This decision cannot be deferred beyond early CAD.

---

## 8.6 Ego-motion association is required, but implementation remains open

The stronger claim:

> “association must happen in bearing space”

would unnecessarily constrain implementation.

An image-space tracker that predicts the next pixel region from known camera motion can be equally valid.

The real invariant is:

\[
\boxed{\text{association after ego-motion prediction}}
\]

---

## 8.7 Face orientation is worth adding

This is high-value social information with low architectural cost if landmarks are already present.

However it must not become an unjustified eye-contact detector.

Makad may infer:

> “the person's face is oriented toward me”

but not:

> “the person's eyes are definitely looking at me.”

---

## 8.8 Confidence needed to become uncertainty

One scalar detector confidence cannot tell the head controller how aggressively it should move.

Explicit angular uncertainty closes the perception-control interface much more cleanly.

It also naturally supports expressive behaviour:

\[
\text{uncertain}
\rightarrow
\text{small/cautious gaze response}
\]

without inventing separate behavioural hacks.

---

## 8.9 Anchor hysteresis is separate from person hysteresis

Maintaining the same track does not prevent the desired point *inside that person* from changing.

Both levels therefore require continuity logic.

---

## 8.10 Audio attention has a defined entry point

The visual tracker now supports:

\[
\text{attention hint}
=
\{\text{bearing, uncertainty, source, time}\}
\]

This is enough for:

\[
\text{sound}
\rightarrow
\text{turn}
\rightarrow
\text{visual acquisition}
\]

without hard-wiring audio logic into the vision subsystem.

---

## 8.11 Audio-visual association now has an owner

Central attention arbitration / SPEC-20 owns eventual matching of cross-modal cues to visual tracks.

That decision is now carried forward explicitly.

---

## 8.12 Photos/screens cannot be solved cheaply by parallax alone

The earlier proposed discriminator was too optimistic.

A flat display at a physical depth can generate perfectly plausible camera-motion parallax.

A mirror can generate even more convincing geometry.

V1 therefore tests and documents these cases instead of claiming unsolved liveness detection.

---

## 8.13 Offline replay is essential, but bit-identical output is too strict

Requiring the ability to replay sessions is absolutely correct.

Requiring universal bit-identical inference across GPU/accelerator backends is not.

The engineering requirement is **reproducible track behaviour and bounded numerical differences**, with deterministic kernels/configuration used where available.

---

## 8.14 Duty cycling changes the acquisition requirement

The original ≤250 ms target cannot simultaneously describe:

- an always-hot tracker; and
- a low-power sleeping detector.

These are now separated:

- ACTIVE → ≤250 ms;
- IDLE → ≤1 s TARGET.

---

## 8.15 Validation diversity must avoid fake statistics

The robot needs to work across ordinary variation in human appearance.

However a college prototype with a handful of participants cannot honestly establish population-level fairness metrics.

The correct requirement is diverse validation plus explicit failure reporting.

---

## 8.16 Stationary-head testing remains deliberately valuable

A large subset of SPEC-09 can still be validated with:

- fixed camera/head;
- recorded video;
- offline replay.

This preserves fast iteration and avoids tying human perception development to the mobile-base build.

However **not every V1 acceptance test can be stationary**, because:

- timestamp alignment;
- ego-motion compensation;
- parallax;
- rolling shutter;

fundamentally require camera/head motion.

This is intentional.

The **mobile base**, however, remains completely unnecessary for SPEC-09 acceptance.

---

# 9. Final decisions carried forward

## DECIDED — MUST-HAVE

1. Person detection and temporal person tracking are separate layers.

2. Faces are associated with person tracks rather than existing as unrelated targets.

3. No biometric identity or named face recognition is required.

4. Coarse face/head orientation shall be available where landmarks permit.

5. Face orientation is not eye-gaze estimation.

6. Multiple humans must be representable.

7. Attention target selection is distinct from visibility.

8. Existing valid target receives selection hysteresis.

9. Track-capacity overflow cannot evict the selected target.

10. A deterministic default selection policy exists before SPEC-20.

11. Behaviour may explicitly select a current track ID.

12. Stale selection commands fail explicitly.

13. Attention hints can bias visual acquisition.

14. SPEC-20 owns eventual audio-visual association.

15. Eye landmarks are the preferred social gaze anchor.

16. Detector-specific calibrated face-box position is the fallback.

17. Face/body anchor switching requires hysteresis.

18. Raw detector centres never directly drive motors.

19. All gaze geometry uses an explicitly defined coordinate convention.

20. Camera observations require effective capture timestamps.

21. Camera and joint-state timing alignment has a quantitative angular-error requirement.

22. Fixed timestamp offset and residual jitter must both be measured.

23. Rolling shutter must be characterised.

24. Measured neck pose must correspond to image capture time.

25. Tracking must compensate known camera ego-motion.

26. Ego-motion compensation may be implemented in bearing or predicted image space.

27. Large head slews should be predicted through rather than automatically treated as target motion.

28. Full 6-DOF camera transform is retained.

29. Coarse range is allowed and required where parallax matters.

30. Range uncertainty must propagate into bearing uncertainty.

31. Coarse range remains explicitly non-safety data.

32. The 1.5° target now has a provisional error budget and subsystem ownership.

33. Separate existence confidence, association quality and bearing uncertainty are required.

34. Bearing uncertainty is part of the gaze-controller interface.

35. Established perception latency remains ≤100 ms P95.

36. Latency must be instrumented by stage.

37. Complete capture→visible-head-response latency belongs to the Master System Integration Budget.

38. Active and idle vision modes are required.

39. Active person acquisition remains ≤250 ms.

40. Offline frame + joint-state replay is required.

41. Normal operation shall not require persistent raw-video storage.

42. Screens, photos and mirrors are explicit known false-lock classes.

43. V1 does not promise anti-spoof/liveness recognition.

44. Representative appearance variation must be included in validation.

45. SPEC-09 remains independent of wheel/mobile-base completion.

---

## TARGET / PROVISIONAL

- ~60 px minimum useful face width;
- ≥10 Hz active detector refresh;
- ~30 Hz target updates;
- ≤1.0 s idle-mode person acquisition;
- 0.3–0.7 s occlusion persistence;
- ≥3 simultaneous person tracks;
- ≤1.5° P95 absolute bearing error;
- ≤0.5° RMS stationary bearing jitter;
- provisional error allocations in §3.12;
- bounded target-motion prediction;
- replaceable perception backend;
- coarse face-orientation accuracy;
- exact detector duty cycle.

---

## MUST BE RESOLVED DURING CAD / CAMERA PROTOTYPING

1. Actual camera-to-neck translation vector.

2. Required accuracy of coarse range from the resulting parallax geometry.

3. Camera timestamp semantics.

4. Exposure-to-host timing offset and jitter.

5. Rolling-shutter readout behaviour.

6. Whether the 1.5° target remains feasible during fast head motion.

7. Real physical neck-pose knowledge accuracy from SPEC-02.

These quantities are now **architecture-affecting**, not things that may be casually deferred until final integration.

---

## EXPLICITLY DEFERRED

- named-person recognition;
- biometric re-identification;
- precise eye-gaze estimation;
- robust presentation-attack/liveness detection;
- full-body pose estimation;
- gesture recognition;
- general object understanding — SPEC-10;
- social-event interpretation — SPEC-11;
- safety depth — SPEC-18;
- autonomous person following — SPEC-19;
- final social attention policy — SPEC-20;
- SLAM.

---

# SPEC-09 final design principle

Makad's perception chain is now:

\[
\boxed{
\begin{aligned}
&\text{observe people}\\
\rightarrow\;&\text{maintain temporally coherent tracks}\\
\rightarrow\;&\text{select one attention target}\\
\rightarrow\;&\text{anchor gaze near the eyes}\\
\rightarrow\;&\text{compensate camera ego-motion}\\
\rightarrow\;&\text{transform using capture-time physical pose}\\
\rightarrow\;&\text{correct parallax using uncertain coarse range}\\
\rightarrow\;&\text{publish bearing + uncertainty}\\
\rightarrow\;&\text{coordinate expressive eyes and physical head}
\end{aligned}
}
\]

The defining property is not merely:

> **Makad can detect a human.**

It is:

> **Makad can maintain a geometrically and temporally coherent belief about the human it is attending to—even while Makad itself moves—and can communicate both that estimate and how much it trusts it to the rest of the robot.**