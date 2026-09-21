# MAKAD — SPEC-10
# Visual Novelty, Object Understanding & Semantic Perception
## Revised Final Specification

> **Design principle:** **Notice, then optionally name.**  
> Makad should react quickly to visual change without needing to understand it semantically. Semantic interpretation is slower, optional, behaviour-driven, and subordinate to real-time perception.

---

# 1. Scope of this specification

SPEC-10 defines Makad's **non-human visual novelty and semantic-understanding layer**.

It contains two deliberately different perception paths.

### Path A — visual novelty

Answers:

> **"Did something visually interesting just happen?"**

Examples:

- an object appears;
- an object disappears;
- something changes;
- something moves;
- Makad looks away, looks back, and the scene is different.

The output is an **attention-level perceptual event**, not an actuator command.

---

### Path B — semantic inspection

Answers:

> **"What is the thing Makad is currently looking at?"**

The canonical V1 interaction is **show-and-tell**:

1. a person presents an object;
2. Makad orients toward it;
3. Makad captures a suitable image;
4. Makad immediately enters an expressive "examining/thinking" state;
5. semantic inference occurs;
6. Makad receives a structured interpretation or explicit failure/uncertainty result.

Semantic inference is:

**trigger-driven → asynchronous → slow-path → lower priority than SPEC-09.**

---

## 1.1 Explicitly outside SPEC-10

SPEC-10 does not own:

- human detection/tracking;
- human target selection;
- real-time gaze control;
- face identification;
- person identity;
- persistent object identity;
- remembered object locations;
- SLAM;
- semantic mapping;
- room inventories;
- manipulation perception;
- grasp estimation;
- safety-grade obstacle ranging;
- safety-grade metric depth;
- autonomous navigation perception;
- continuous VLM scene narration;
- arbitrary pointing/reference resolution;
- OCR/general text reading;
- camera-history recording;
- long-term visual memory.

Persistent entity/object memory belongs to the later memory architecture.

---

# 2. Existing Makad decisions that constrain SPEC-10

## 2.1 SPEC-08 owns the camera

SPEC-10 shall use the common camera acquisition architecture.

It shall inherit rather than redefine:

- camera intrinsics;
- distortion treatment;
- frame timestamps;
- exposure metadata where available;
- camera extrinsics;
- image coordinate conventions;
- calibration data;
- camera/head transform.

There shall not be a second independent camera stack for semantic vision.

---

## 2.2 SPEC-09 owns the hard real-time visual loop

SPEC-09 remains responsible for:

**camera → human detection/tracking → target selection → gaze geometry → attention/gaze**

with its existing real-time timing requirements.

SPEC-10 shall never weaken those requirements.

When resources are insufficient:

> **SPEC-10 loses resources before SPEC-09 does.**

---

## 2.3 Shared capture-time geometry remains mandatory

SPEC-09 already established that directional observations must use the physical camera/head state corresponding to **image capture time**, not inference-completion time.

SPEC-10 inherits the same timestamp-synchronization requirement and shall not introduce a weaker timing standard.

Likewise, objects and novelty regions requiring a bearing shall use the same:

**pixel → camera ray → capture-time pose → neck/Makad frame**

pipeline used by SPEC-09.

---

## 2.4 SPEC-09's ego-motion model is inherited

SPEC-10 shall not create an independent optical-flow-based interpretation of Makad's own head motion.

The baseline compensation mechanism shall inherit SPEC-09's **kinematic feedforward** model.

Optical flow may later supplement it, but it shall not replace the shared kinematic model as the source of expected camera motion.

---

## 2.5 Coarse range remains non-safety information

Where camera translation relative to the neck pivot requires approximate depth/range for geometric correction, SPEC-10 may use the same coarse-range mechanism permitted by SPEC-09.

Such range remains:

**interaction geometry only — never collision/safety depth.**

---

## 2.6 Actual neck pose is a required perception input

SPEC-02 already requires measured physical neck pose to be available to perception.

SPEC-10 depends on:

- measured yaw;
- measured pitch;
- measured roll if present;
- timestamps;
- preferably estimated angular velocity.

Commanded servo angle alone is insufficient.

---

## 2.7 SPEC-10 creates an explicit build-order dependency

Unlike much of SPEC-09, several important SPEC-10 tests require the camera itself to move.

Therefore full novelty validation cannot happen before Makad has:

1. a controllable neck prototype;
2. timestamped physical joint-state measurements;
3. a candidate camera mounted approximately in its intended geometry.

This creates the following development milestone:

> **Prototype SPEC-10 novelty as soon as the neck mule can perform controlled representative motion, and do so before final camera and compute-platform lock.**

Waiting until final integration would be too late.

---

# 3. Engineering reasoning / architecture

# 3.1 Two paths remain fundamental

SPEC-10 is not one giant computer-vision pipeline.

```text
                        CAMERA
                           │
                ┌──────────┴───────────┐
                │                      │
                ▼                      ▼
        LIGHTWEIGHT NOVELTY      SEMANTIC INSPECTION
                │                      │
                │                      │
        provisional hint         triggered request
                │                      │
        confirmed hint           quality-gated frame
                │                      │
                ▼                      ▼
          attention system        local / remote
                                       │
                                       ▼
                               structured result
                                       │
                                       ▼
                                  behaviour
```

The novelty path exists primarily for **aliveness**.

The semantic path exists for **understanding on demand**.

---

# 3.2 Novelty needs a real latency architecture

The previous version left three independent variables unresolved:

- processing frequency;
- temporal persistence;
- cooldown.

Those parameters directly combine into reaction latency.

They therefore cannot be tuned independently without an end-to-end requirement.

SPEC-10 now uses a **two-stage novelty event**.

---

## Stage 1 — provisional novelty

A single sufficiently strong observation may produce:

`NOVELTY_PROVISIONAL`

This event is:

- low confidence;
- short lived;
- cheap;
- suitable for subtle behavioural acknowledgement.

The attention system may allow it to cause something like an **eyes-only glance**.

A provisional event shall not by itself authorize a full head turn.

### End-to-end latency

From the first camera frame containing usable evidence of the change to publication of the provisional attention hint:

\[
\boxed{T_{provisional} \leq 150\text{ ms}}
\]

---

## Stage 2 — confirmed novelty

Persistence or repeated evidence promotes the same visual episode to:

`NOVELTY_CONFIRMED`

A confirmed event may be allowed by the attention arbiter to trigger:

- physical head orientation;
- curious posture;
- chirp;
- further inspection.

### End-to-end latency

From the first usable camera frame containing the change to publication of the confirmed event:

\[
\boxed{T_{confirmed} \leq 400\text{ ms}}
\]

---

## Why the split exists

A one-frame false positive now costs Makad perhaps:

> a tiny eye flick.

It does **not** cost:

> a pointless mechanical head turn.

That converts the false-positive/latency tradeoff into two much easier decisions.

---

# 3.3 Derived novelty-processing cadence

For provisional latency:

\[
T_{provisional}
=
T_{wait}
+
T_{process}
+
T_{publish}
\]

To remain within 150 ms, the lightweight novelty path shall have:

\[
T_{wait} \leq 100\text{ ms}
\]

which implies an active evaluation cadence of at least approximately:

\[
\boxed{10\text{ Hz}}
\]

or another event-driven architecture providing an equivalent worst-case evaluation interval.

The remaining:

\[
\boxed{\leq50\text{ ms}}
\]

is allocated to:

- geometric compensation;
- change analysis;
- event formation;
- IPC/publication.

This is a much stronger compute constraint than simply saying "lightweight."

---

# 3.4 Eyes hide perception latency

This architecture deliberately matches Makad's established eye/head behaviour hierarchy:

**eyes signal attention first → physical head follows if warranted.**

SPEC-10 therefore does not need to eliminate all temporal validation.

Instead:

```text
visual change
    ↓
≤150 ms
    ↓
eyes notice
    ↓
additional evidence
    ↓
≤400 ms total
    ↓
head may follow
```

The character animation and perception architecture now reinforce each other.

---

# 3.5 Novelty cannot depend only on adjacent frames

Adjacent-frame novelty misses one of Makad's most important behaviours.

Example:

1. Makad looks at an empty desk.
2. Makad looks toward the user.
3. The user places a mug on the desk.
4. Makad later looks back.

The object never "appeared" between two frames viewing the desk.

It appeared while the desk was out of view.

Therefore SPEC-10 requires **pose-keyed visual reference memory**.

---

# 3.6 Pose-keyed reference frames

The novelty subsystem shall maintain a small cache of reference observations indexed primarily by measured head/camera pose.

Conceptually:

```text
reference_cache[
    quantized_yaw,
    quantized_pitch,
    quantized_roll
] → reference observation
```

When Makad returns to a previously observed viewing direction:

1. obtain capture-time physical head pose;
2. retrieve the nearest appropriate reference observation;
3. geometrically align the views where required;
4. compare current visual content against the prior view.

This supports:

> **look away → environment changes → look back → notice**

without requiring continuous observation of the change.

---

# 3.7 Kinematic ego-motion compensation

For camera rotation, the baseline frame warp shall derive from the same kinematic motion estimate used by SPEC-09.

For approximately pure camera rotation:

\[
H = K R K^{-1}
\]

where:

- \(K\) is the calibrated camera intrinsic matrix;
- \(R\) is the predicted relative camera rotation between captures.

This allows a previous view to be warped into the expected current view cheaply.

---

## 3.7.1 Important failure case: parallax

Makad's camera does not necessarily rotate about its optical centre.

Neck motion therefore creates some camera translation.

Residual parallax scales approximately with:

\[
\frac{\|\Delta t\|}{Z}
\]

where:

- \(\Delta t\) is relative camera translation;
- \(Z\) is object range.

Therefore kinematic homography compensation becomes weakest for **near objects**.

Ironically, that is exactly where show-and-tell occurs.

Consequently:

- pose-keyed comparisons should preferentially compare frames captured at closely matching physical poses;
- large-pose-difference homography comparisons shall not be treated as reliable close-range novelty evidence;
- coarse range may be used where already available;
- persistent close-range residuals shall not automatically become confirmed novelty.

---

# 3.8 Reference cache is not object memory

The reference cache exists only to answer:

> **"Does this view differ from the previous accepted appearance of this view?"**

It shall not create:

- named objects;
- persistent identities;
- object-location histories;
- semantic maps.

This remains perception infrastructure, not SPEC-20 memory.

---

# 3.9 Novelty event semantics

SPEC-10 shall support the following coarse visual-change categories:

- `appeared`
- `disappeared`
- `changed`
- `moved`
- `unknown_change`

`unknown_change` exists because reliably distinguishing motion from disappearance+appearance may not always be possible without stronger object correspondence.

The system shall prefer `unknown_change` over inventing precision.

---

# 3.10 Event coalescing is not habituation

SPEC-10 and the future behaviour/habituation layer must have a hard boundary.

### SPEC-10 event coalescing

Means:

> "Do not emit the same underlying visual episode repeatedly."

Example:

the same mug appearing should not create twenty identical novelty messages across twenty frames.

### SPEC-11 habituation / interest decay

Means:

> "This event is real, but Makad no longer finds it interesting."

SPEC-10 shall not reduce perceptual event validity merely because Makad has seen similar events many times.

Perception decides:

> **did it happen?**

Behaviour decides:

> **do I still care?**

---

# 3.11 Canonical V1 inspection geometry

"Show me this" needs a computable interpretation.

V1 therefore adopts a **centre-presentation convention**.

### Presentation zone

The intended object's visual centre should lie approximately within:

\[
u \in [0.30W, 0.70W]
\]

\[
v \in [0.30H, 0.70H]
\]

where \(W,H\) are image dimensions.

This corresponds to the central 40% of the image along each dimension.

---

### Default semantic crop

The initial semantic ROI shall be:

\[
u \in [0.20W,0.80W]
\]

\[
v \in [0.20H,0.80H]
\]

providing a margin around the presentation zone.

This gives V1 an explicit crop contract without requiring a separate class-agnostic object detector.

---

## 3.11.1 Why this is preferable for V1

The human performs most of the segmentation by:

> holding the thing up in front of Makad.

Makad does not need to solve arbitrary referring expressions just to demonstrate useful visual understanding.

---

# 3.12 Crop policy

The remote semantic path shall use the default inspection crop when that crop contains sufficient information.

A full frame may be sent only when:

- the behaviour explicitly requires scene context;
- or the semantic backend determines that the inspection crop is insufficient and policy allows a wider retry.

A class-agnostic objectness/segmentation stage is therefore **not a V1 prerequisite**.

It remains a possible later TARGET.

---

# 3.13 Pixels-on-target is a camera requirement

Near focus alone is insufficient.

For an object of physical width \(w\) at distance \(d\):

\[
\theta =
2\tan^{-1}\left(\frac{w}{2d}\right)
\]

For a representative:

\[
w=0.06\text{ m}, \qquad d=0.40\text{ m}
\]

the angular width is approximately:

\[
\boxed{\theta \approx 8.6^\circ}
\]

With calibrated horizontal focal length \(f_x\), the projected width is approximately:

\[
N_{px}
=
2f_x\tan\left(\frac{\theta}{2}\right)
\]

For intuitive comparison, with a roughly 70° horizontal FOV:

- a 1280-pixel-wide image gives roughly 150–160 pixels across such an object;
- a 640-pixel-wide image gives only roughly 75–80 pixels.

Therefore camera FOV, image width and semantic recognition performance are coupled.

SPEC-08 cannot lock the lens/camera merely because the object is "in focus."

---

# 3.14 Semantic pixels-on-target threshold

Define:

\[
N_{semantic}
\]

as the minimum projected target width required for acceptable semantic performance.

Unlike the geometry above, \(N_{semantic}\) depends on the actual semantic backend.

It shall therefore be established experimentally using the Makad object benchmark by progressively reducing effective object resolution.

Before final SPEC-08 camera lock, the candidate camera shall demonstrate:

\[
\boxed{
N_{object}(0.4\text{ m})
\geq
N_{semantic}
}
\]

for representative small show-and-tell objects.

This becomes a **component-selection gate**, not a generic future tuning parameter.

---

# 3.15 Semantic capture and motion

Slow inference does not require Makad to remain motionless.

The correct sequence is:

```text
orient / settle sufficiently
        ↓
capture candidate frames
        ↓
choose acceptable frame
        ↓
release motion restriction
        ↓
Makad resumes expressive "thinking"
        ↓
semantic inference continues
```

Makad only needs a sufficiently stable **capture opportunity**.

It does not need to freeze for two seconds while a VLM thinks.

---

# 3.16 Frame-quality gate

Semantic inference shall not consume arbitrarily bad frames.

The capture-quality system shall calculate at least:

### Blur metric

A focus/sharpness metric based on spatial high-frequency content, initially:

\[
Q_{blur} = \operatorname{Var}(\nabla^2 I)
\]

i.e. variance of Laplacian or equivalent.

Absolute thresholds depend strongly on:

- camera;
- resolution;
- exposure;
- preprocessing.

Therefore SPEC-08 camera validation shall establish an acceptable sharp-frame baseline.

The runtime gate shall compare against that calibrated baseline rather than using an arbitrary internet threshold.

---

### Exposure metric

For the semantic ROI:

\[
f_{clip}
=
\frac{
N_{dark-clipped}+N_{bright-clipped}
}{
N_{ROI}
}
\]

shall be measured.

The final acceptable clipping threshold shall be determined using the Makad camera/object benchmark.

---

### Motion state

Capture shall also consider measured head angular velocity.

A candidate frame taken during a high-speed neck movement shall be penalized or rejected when motion blur is expected.

---

# 3.17 Semantic acquisition is bounded

After a semantic request has entered its capture phase:

- maximum reacquisition attempts: **3**
- maximum total frame-acquisition window: **750 ms**

If no suitable source frame is obtained:

`epistemic_outcome = unusable_image`

The subsystem shall not loop indefinitely waiting for perfection.

Major gaze reorientation should normally occur **before** the semantic request enters capture.

---

# 3.18 Semantic result preserves spatial context

The semantic result shall retain the location of what was inspected.

At capture time, SPEC-10 shall calculate and attach:

- source ROI;
- source capture timestamp;
- ROI-centre camera ray;
- capture-time neck/Makad-frame bearing;
- angular ROI extent where practical;
- coarse range used for geometry, if any.

This enables later behaviour such as:

> Makad names an object and then keeps looking toward the same thing.

The bearing should not need to be reconstructed seconds after inference completion.

---

# 3.19 Semantic output has two orthogonal outcome axes

The previous single failure enumeration incorrectly mixed:

> **"I cannot tell what this is"**

with:

> **"the network is down."**

SPEC-10 shall separate them.

---

## Epistemic outcome

Describes the visual knowledge result.

Examples:

- `identified`
- `uncertain`
- `ambiguous_target`
- `unknown`
- `unusable_image`

---

## System outcome

Describes whether the computation itself succeeded.

Examples:

- `ok`
- `offline`
- `timeout`
- `cancelled`
- `privacy_blocked`
- `resource_rejected`
- `backend_error`

Thus:

```text
system_outcome = ok
epistemic_outcome = unknown
```

means:

> the visual system worked correctly but could not identify the object.

While:

```text
system_outcome = offline
epistemic_outcome = null
```

means:

> Makad could not access the requested backend.

Behaviour can react differently to each.

---

# 3.20 Local versus remote semantic path

V1 architecture remains backend-independent.

### Open-vocabulary backend

A remote VLM is acceptable and likely useful for V1 show-and-tell.

### Local closed-set backend

Remains a TARGET if a real Makad behaviour requires specific known classes.

The architecture shall not require both before the capability is considered functional.

---

# 3.21 "Preemptible inference" is removed

SPEC-10 shall **not assume** that inference already executing on:

- GPU;
- NPU;
- DSP;
- accelerator

can be interrupted.

Often it cannot.

Instead the architecture distinguishes:

### request cancellation

Makad can decide a semantic result is no longer needed.

from:

### hardware execution preemption

which may be impossible.

Therefore accelerator safety must be handled **before scheduling the work**.

---

# 3.22 Shared accelerator occupancy contract

Define:

\[
J_{9,shared}
\]

as the maximum additional scheduling delay that SPEC-09 can tolerate from another workload while still satisfying its finalized real-time latency/jitter requirements.

For any non-preemptible semantic operation sharing SPEC-09's accelerator:

\[
\boxed{
T_{nonpreemptible}
\leq
J_{9,shared}
}
\]

shall hold.

The actual numeric value shall be inherited from the finalized SPEC-09 timing budget during master-spec consolidation.

This is not a free SPEC-10 TARGET.

It is a **cross-spec derived constraint**.

If the candidate semantic model cannot satisfy it, one of the following must happen:

1. semantic inference runs remotely;
2. semantic inference runs on a separate accelerator;
3. semantic work is segmented/chunked sufficiently;
4. semantic inference is blocked while SPEC-09 tracking requires the device.

"Thread priority" is not an acceptable fix for a non-preemptible accelerator operation.

---

# 3.23 Memory bandwidth is also shared

Accelerator occupancy is only half the problem.

A semantic model can degrade SPEC-09 by saturating:

- DRAM bandwidth;
- shared cache;
- memory controller;
- thermal envelope.

Therefore coexistence validation must measure SPEC-09 performance during the **actual semantic memory load**, not merely confirm that its process has a higher scheduler priority.

---

# 3.24 Privacy architecture

Remote visual inference is not equivalent to ordinary local camera operation.

SPEC-10 therefore introduces a single architecture concept:

# Visual Uplink Gate

All outbound network transmission containing camera-derived visual data shall pass through one controlled uplink mechanism.

No semantic backend shall directly upload camera images independently.

The Visual Uplink Gate owns:

- privacy-mode checking;
- image/crop authorization;
- transfer state;
- remote-analysis indication;
- logging of backend/version;
- completion/failure state.

---

# 3.25 Global local-only mode

Makad shall expose a global mode equivalent to:

`visual_cloud_enabled = false`

When local-only mode is active:

> **no camera-derived image data may leave the device.**

This policy overrides:

- semantic routing;
- behaviour requests;
- novelty events;
- backend preferences.

A fresh/default privacy configuration should begin in local-only mode until remote visual inference is intentionally enabled.

---

# 3.26 Privacy indication uses Makad's own expression language

Remote visual transmission shall not silently occur.

When the Visual Uplink Gate is actively transmitting/awaiting a remote visual request, Makad shall display a distinct **uplink visual state using its existing eye display**.

It shall:

- preserve the eyes-only face rule;
- not require text;
- not require a generic cloud icon;
- be visually distinguishable from ordinary idle/thinking expressions.

Possible implementation:

- distinctive eye pulse;
- brightness pattern;
- animation cadence;
- colour alteration if the final display supports colour.

The exact artwork belongs to the face/behaviour implementation.

The existence of a distinct state does not.

---

## 3.26.1 Indicator coupling

The uplink indicator shall be asserted by the **same Visual Uplink Gate that performs the transfer**.

It shall become active before camera-derived payload transmission begins and shall remain active until that remote visual operation finishes or fails.

A separate unrelated UI call is insufficient.

This prevents future code from accidentally uploading an image while forgetting to activate the indicator.

---

# 3.27 No cloud inference from novelty alone

A novelty event may trigger:

- eyes;
- head orientation;
- local curiosity behaviour.

It may not by itself authorize remote transmission.

A separate behaviour/semantic request must cross the privacy gate.

---

# 3.28 Reproducibility is a first-class requirement

SPEC-10 contains several interacting novelty thresholds and temporal policies.

Manual room testing is too slow for tuning.

Therefore the novelty system requires deterministic offline replay.

---

## Required replay recording

Record at minimum:

- image/frame data used by novelty;
- camera capture timestamps;
- measured yaw/pitch/roll;
- joint-state timestamps;
- camera exposure/gain metadata where available;
- calibration version;
- novelty configuration;
- relevant attention-state metadata.

The recording must preserve the camera/joint temporal relationship.

A frame recording without joint-state timing is insufficient.

---

## Replay requirement

Given the same recording, calibration and configuration, the novelty path shall reproduce the same event sequence and timestamps within the pipeline's defined deterministic granularity.

For the lightweight novelty path, fixed-input replay should be deterministic enough for automated regression tests.

Remote VLM outputs are explicitly exempt from bit-identical replay.

---

# 3.29 Semantic backends require version traceability

Every semantic result shall record where practical:

- provider;
- model identifier;
- immutable model version if exposed;
- API/version identifier;
- relevant inference configuration;
- request date/time.

If a provider exposes only a mutable model alias, that backend shall be marked as **not fully reproducible**.

The Makad object benchmark must be executable again whenever:

- model/backend configuration changes;
- a local model changes;
- a remote model version changes;
- a meaningful perception regression is suspected.

---

# 4. Formal requirements

## 4.1 Governing principles

The following are architectural principles rather than ordinary pass/fail feature requirements:

### P10-01 — Behaviour bounded

Semantic recognition exists because a Makad behaviour consumes the result.

### P10-02 — Notice before naming

Novelty detection shall not depend on semantic classification.

### P10-03 — Current observation is not memory

A visual result describes the captured observation and does not establish persistent object identity.

### P10-04 — Human social attention outranks incidental object curiosity

Unless behaviour explicitly overrides it, active human interaction remains higher priority than object novelty.

These principles are intentionally removed from the MUST count.

---

# 4.2 Critical architecture requirements

## C10-R01 — MUST — Shared camera pipeline

SPEC-10 shall consume the common SPEC-08 camera acquisition pipeline and shall not open a competing independent camera stream.

---

## C10-R02 — MUST — Shared perception geometry

All physical bearings generated by SPEC-10 shall use the same geometry implementation and conventions as SPEC-09.

---

## C10-R03 — MUST — Capture-time physical pose

Directional results shall use physical camera/head state corresponding to image capture time.

SPEC-10 inherits SPEC-09's finalized timestamp-synchronization requirement.

---

## C10-R04 — MUST — Shared kinematic ego-motion model

Expected image motion caused by commanded/measured head motion shall use SPEC-09's kinematic feedforward model as the baseline mechanism.

---

## C10-R05 — MUST — No direct actuation

SPEC-10 shall publish perception events/attention hints only.

No bounding box, novelty region or semantic ROI may directly command a motor.

---

## C10-R06 — MUST — SPEC-09 compute protection

SPEC-10 shall not cause SPEC-09 to violate its finalized latency, jitter or tracking requirements.

---

## C10-R07 — MUST — Shared accelerator occupancy bound

Any non-preemptible SPEC-10 work scheduled on a hardware accelerator shared with SPEC-09 shall satisfy:

\[
T_{nonpreemptible}\leq J_{9,shared}
\]

or shall not be scheduled while the real-time SPEC-09 workload requires that accelerator.

---

## C10-R08 — MUST — Memory/thermal coexistence

SPEC-10 shall also be limited where required to prevent shared memory-bandwidth or thermal contention from violating SPEC-09 requirements.

---

# 4.3 Novelty requirements

## C10-R09 — MUST — Local novelty

Basic novelty detection shall function without internet access.

---

## C10-R10 — MUST — Evaluation interval

While novelty monitoring is active, eligible novelty evaluations shall occur with a maximum nominal interval of:

\[
\boxed{\leq100\text{ ms}}
\]

or equivalent event-driven latency.

---

## C10-R11 — MUST — Provisional novelty latency

A qualifying visual change shall produce a provisional novelty event within:

\[
\boxed{\leq150\text{ ms}}
\]

of the first usable camera frame containing the change.

---

## C10-R12 — MUST — Confirmed novelty latency

A visual change satisfying the confirmation policy shall produce a confirmed novelty event within:

\[
\boxed{\leq400\text{ ms}}
\]

of the first usable evidence frame.

---

## C10-R13 — MUST — Two-tier novelty output

Novelty events shall explicitly indicate:

- `provisional`
- or `confirmed`.

---

## C10-R14 — MUST — Pose-keyed reference cache

Novelty shall support comparison against previously observed views indexed by physical camera/head pose rather than relying exclusively on adjacent-frame differences.

---

## C10-R15 — MUST — Look-away/look-back novelty

A scene change occurring while the changed region is outside Makad's current FOV shall remain detectable when Makad subsequently returns to a sufficiently similar prior viewing pose.

---

## C10-R16 — MUST — Egomotion robustness

Normal Makad head motion shall not systematically become confirmed environmental novelty.

---

## C10-R17 — MUST — Global disturbance rejection

The novelty system shall reject or reduce responses to:

- global exposure changes;
- camera gain transitions;
- broad illumination changes;
- expected full-frame displacement from head motion.

---

## C10-R18 — MUST — Novelty event contract

Every novelty event shall expose at minimum:

- `episode_id`;
- `phase = provisional | confirmed`;
- `event_kind`;
- source timestamp;
- source ROI;
- novelty strength/quality;
- physical bearing where valid;
- event age/expiry;
- confidence/validity state.

`event_kind` shall support:

- `appeared`;
- `disappeared`;
- `changed`;
- `moved`;
- `unknown_change`.

---

## C10-R19 — MUST — Attention hint

Qualified novelty events shall be representable through the common Makad `attention_hint` architecture.

---

## C10-R20 — MUST — Provisional/confirmed behavioural distinction

The attention interface shall preserve sufficient information for behaviour to allow:

- provisional event → subtle/eyes-only acknowledgement;
- confirmed event → possible physical head attention.

SPEC-10 does not itself command those motions.

---

## C10-R21 — MUST — Event coalescing

Repeated frames representing the same underlying visual episode shall be coalesced under the same episode rather than generating a new novelty event on every frame.

This is duplicate suppression only.

It shall not implement long-term interest/habituation.

---

## C10-R22 — TARGET — Human-region suppression

Where SPEC-09 human masks/tracks are available, SPEC-10 should suppress duplicate novelty events already explained by ordinary tracked human motion.

---

# 4.4 Semantic inspection requirements

## C10-R23 — MUST — Trigger-driven semantic inference

Computationally expensive semantic interpretation shall run only in response to an explicit semantic/behaviour request.

---

## C10-R24 — MUST — Defined V1 inspection region

V1 shall use the centre-presentation convention defined in §3.11.

The default semantic crop shall be the central 60% × 60% of the image unless another explicitly selected ROI is available.

---

## C10-R25 — MUST — Ambiguous target

If the semantic input contains multiple plausible intended objects and the target cannot be determined reliably:

`epistemic_outcome = ambiguous_target`

shall be permitted.

---

## C10-R26 — MUST — Close-range semantic compatibility

SPEC-08 camera selection shall demonstrate usable semantic imaging at the intended show-and-tell region including approximately:

\[
\boxed{0.4\text{ m}}
\]

---

## C10-R27 — MUST — Pixels-on-target gate

Before camera lock, the candidate camera/FOV/resolution combination shall demonstrate:

\[
N_{object}(0.4\text{ m})\geq N_{semantic}
\]

for representative small handheld objects.

---

## C10-R28 — MUST — Frame-quality measurements

Semantic candidate images shall be evaluated using at minimum:

- a calibrated blur/sharpness metric;
- ROI exposure/clipping metric;
- head-motion state.

---

## C10-R29 — MUST — Bounded capture

A semantic request entering frame-acquisition state shall terminate that phase within:

\[
\boxed{\leq750\text{ ms}}
\]

with no more than:

\[
\boxed{3}
\]

reacquisition attempts.

Failure shall produce `unusable_image`.

---

## C10-R30 — TARGET — Burst-based source-frame selection

Where compute/buffering permits, the system should select the best image from a short capture burst rather than trusting a single arbitrary frame.

---

## C10-R31 — MUST — Bearing retention

Every semantic result associated with a spatial target shall retain the capture-time bearing and ROI of the inspected region.

---

## C10-R32 — MUST — Backend-independent semantic result

Makad behaviour shall consume a common semantic result contract rather than provider-specific VLM responses.

---

## C10-R33 — MUST — Open-vocabulary path

V1 shall contain at least one usable open-vocabulary semantic path.

A remote VLM is acceptable.

---

## C10-R34 — TARGET — Local closed vocabulary

A local recognizer may be implemented for a small behaviour-relevant vocabulary if useful.

---

## C10-R35 — TARGET — Semantic backend routing

Where multiple backends exist, routing may consider:

- network availability;
- privacy mode;
- workload;
- vocabulary;
- requested behaviour;
- backend capability.

---

# 4.5 Semantic state and uncertainty

## C10-R36 — MUST — Early processing state

After a semantic request is accepted, behaviour shall receive a processing state rapidly enough to begin the thinking animation.

Target:

\[
\boxed{\leq150\text{ ms}}
\]

from request acceptance.

This does not constrain inference completion.

---

## C10-R37 — MUST — Orthogonal result taxonomy

Semantic output shall contain separate:

- `system_outcome`;
- `epistemic_outcome`.

---

## C10-R38 — MUST — Explicit uncertainty

Semantic output shall support:

- identified;
- uncertain;
- ambiguous;
- unknown.

It shall not force a label.

---

## C10-R39 — MUST — No fake calibrated confidence

Uncalibrated VLM self-confidence shall not be exposed as though it were calibrated perception probability.

Categorical confidence may be used instead.

---

## C10-R40 — MUST — Behaviour-accessible hedging

The behaviour layer shall be able to distinguish a confident semantic result from a weak/uncertain one and react differently.

---

# 4.6 Request scheduling

## C10-R41 — MUST — Bounded semantic queue

V1 semantic inference shall support at most one active inference request and a bounded number of pending requests.

An unlimited queue is prohibited.

---

## C10-R42 — MUST — Stale result rejection

Every semantic inference shall carry an interaction/request identifier.

A result from a cancelled or superseded interaction shall not automatically trigger behaviour.

---

## C10-R43 — MUST — Cancellation without preemption assumption

Semantic requests may be cancelled logically.

The architecture shall not assume cancellation can interrupt an already running accelerator kernel/model execution.

---

# 4.7 Privacy requirements

## C10-R44 — MUST — Visual Uplink Gate

All outbound camera-derived visual data shall pass through one privacy-aware network transfer mechanism.

---

## C10-R45 — MUST — Global local-only mode

When local-only mode is enabled, no camera-derived visual payload may leave Makad.

---

## C10-R46 — MUST — Novelty cannot authorize upload

A novelty event alone shall never authorize cloud image transfer.

---

## C10-R47 — MUST — Uplink indication

Every remote visual operation shall activate a distinct Makad eye/display state indicating remote visual processing.

---

## C10-R48 — MUST — Indicator-transfer coupling

The indication shall be controlled by the same Visual Uplink Gate performing the remote transfer and shall activate before outbound image data begins.

---

## C10-R49 — MUST — Minimum-necessary visual payload

For V1 show-and-tell, the default centre inspection crop shall be used rather than a full room frame whenever sufficient.

---

## C10-R50 — MUST — No persistent image storage by default

Semantic-request source images shall not enter long-term storage by default.

---

## C10-R51 — MUST — No raw-image operational logs

Normal runtime logs shall not contain raw camera frames unless explicit development image logging has been enabled.

---

# 4.8 Reproducibility and observability

## C10-R52 — MUST — Novelty replay recording

The development/validation system shall be able to record synchronized:

- camera frames;
- frame timestamps;
- measured joint state;
- joint timestamps;
- camera metadata;
- calibration identifier;
- novelty configuration.

---

## C10-R53 — MUST — Deterministic novelty replay

The novelty pipeline shall support deterministic offline replay sufficiently stable for regression testing of event generation.

---

## C10-R54 — MUST — Backend/version logging

Semantic logs shall record:

- backend/provider;
- model name;
- version where available;
- API/configuration information sufficient to identify the evaluated setup.

---

## C10-R55 — MUST — Runtime health

SPEC-10 shall expose:

- novelty active/inactive;
- novelty event rate;
- semantic queue state;
- backend;
- backend/version;
- remote/local path;
- inference latency;
- resource rejection;
- timeout;
- cancellation;
- error state.

---

## C10-R56 — MUST — Failure isolation

SPEC-10 process/backend/network failure shall not stop:

- SPEC-08 camera acquisition;
- SPEC-09 human tracking;
- gaze control;
- motor control.

---

# 4.9 Evaluation

## C10-R57 — MUST — Makad-specific object benchmark

Semantic evaluation shall use approximately:

\[
\boxed{30}
\]

physical objects representative of Makad's real environment.

---

## C10-R58 — MUST — Real operating conditions

The benchmark shall include:

- Makad's camera;
- actual/candidate mount geometry;
- approximately 0.4 m presentation;
- multiple orientations;
- realistic indoor lighting;
- handheld presentation;
- some object motion;
- representative head movement where relevant.

---

## C10-R59 — MUST — Error taxonomy in evaluation

Evaluation shall separately record:

1. useful/correct answer;
2. acceptable uncertainty/refusal;
3. confidently wrong answer;
4. system failure.

A generic accuracy percentage is insufficient.

---

## C10-R60 — MUST — Benchmark rerunnability

The 30-object suite shall be rerunnable on demand after backend/model/camera/configuration changes.

---

# 5. Interfaces and dependencies

# 5.1 SPEC-08 — Camera

SPEC-10 imposes **two** camera-selection gates:

### Optical focus

Representative objects must be sufficiently sharp around the 0.4 m interaction region.

### Semantic sampling

Representative small objects must provide sufficient pixels-on-target:

\[
N_{object}\geq N_{semantic}
\]

These requirements must be checked together with SPEC-09's wider human-tracking FOV requirement before lens/camera lock.

This is a genuine cross-spec tradeoff:

> wider FOV helps human coverage but reduces pixels-per-degree for small objects.

---

# 5.2 SPEC-09 — Human tracking/gaze

SPEC-10 requires:

- shared capture-time geometry;
- shared kinematic camera-motion model;
- attention-hint interface;
- real-time compute/jitter budget;
- optional person masks/tracks.

SPEC-10 shall not alter SPEC-09 merely because a semantic model is computationally expensive.

---

# 5.3 SPEC-02 — Neck mechanism

Full SPEC-10 novelty validation requires:

- working powered roll/pitch/yaw motion;
- measured roll state;
- measured physical pose;
- pose timestamps;
- representative camera mounting.

This makes the moving neck mule a prerequisite for meaningful novelty validation.

---

# 5.4 Behaviour / attention system

SPEC-10 publishes:

```text
novelty_provisional
novelty_confirmed
attention_hint
semantic_processing
semantic_result
semantic_system_failure
```

Behaviour determines:

- eye flick;
- head turn;
- ignore;
- curiosity;
- semantic inspection;
- chirp;
- hedging;
- request for another view.

---

# 5.5 SPEC-11 boundary

SPEC-10 performs **event coalescing**.

SPEC-11 performs **interest/habituation**.

No long-duration "I've seen this too often" decay belongs in SPEC-10.

---

# 5.6 Compute architecture

Compute selection must explicitly benchmark simultaneous:

- SPEC-09 tracking;
- novelty at ≥10 Hz equivalent;
- semantic preprocessing;
- local semantic inference if implemented;
- audio;
- normal Makad control.

Important resources include:

- accelerator occupancy;
- DRAM bandwidth;
- CPU utilization;
- memory pressure;
- thermals.

---

# 5.7 Privacy / networking

All camera-derived remote traffic shall pass through the Visual Uplink Gate.

Backend libraries shall not own unrestricted direct image-upload paths.

---

# 6. Quantities still requiring validation

The list is now much shorter.

## 6.1 \(J_{9,shared}\)

This is not independently tuneable by SPEC-10.

It must be copied/derived from final SPEC-09 real-time jitter headroom during consolidation.

---

## 6.2 Pose-cache angular bin/tolerance

Needs testing against:

- neck repeatability;
- camera FOV;
- scene distance;
- registration quality.

Too narrow → cache misses.

Too wide → excessive registration/parallax error.

---

## 6.3 Reference-background replacement policy

Need determine how long a changed scene must remain stable before it becomes the new accepted reference.

This affects duplicate-event generation but must remain separate from behavioural habituation.

---

## 6.4 Blur calibration threshold

Calibrate from accepted/rejected source frames with the final candidate camera.

---

## 6.5 Exposure clipping threshold

Calibrate using the actual Makad object test set and indoor lighting.

---

## 6.6 \(N_{semantic}\)

Must be measured for the selected semantic backend by testing reduced effective pixels-on-target.

This value must be known **before camera/FOV lock**.

---

## 6.7 Final semantic timeout

Ordinary semantic inference may take seconds.

The timeout should be selected from actual backend latency distributions rather than guessed.

---

## 6.8 Local recognition vocabulary

Only required if real behaviours justify it.

---

# 7. Acceptance tests

# C10-T01 — Shared camera/geometry inspection

Verify architecturally and through logs that SPEC-10:

- uses the common camera acquisition path;
- uses the common geometry implementation;
- consumes capture-time physical joint state.

**Pass:** no duplicate camera ownership or independently defined coordinate transform exists.

---

# C10-T02 — Provisional novelty latency

Introduce a clear new object while recording camera timestamps and novelty-event timestamps.

Measure:

\[
T =
t_{provisional}
-
t_{first\ usable\ evidence}
\]

**Pass:**

\[
\boxed{T\leq150\text{ ms}}
\]

for the required latency percentile established for Makad's real-time event tests.

---

# C10-T03 — Confirmed novelty latency

Repeat C10-T02 and measure confirmed-event publication.

**Pass:**

\[
\boxed{T\leq400\text{ ms}}
\]

for qualifying persistent novelty.

---

# C10-T04 — Provisional false-positive behaviour

Create brief one-frame/transient disturbances.

**Pass:**

Transient evidence may produce a provisional event but shall not automatically become a confirmed event or full head-attention command.

---

# C10-T05 — Moving-camera compensation

Use a static room.

Command representative neck:

- yaw;
- pitch;
- combined movement.

**Pass:**

Makad's own motion does not systematically produce confirmed novelty.

---

# C10-T06 — Look-away / object-appears / look-back

1. View an empty desk at pose A.
2. Turn Makad to pose B.
3. Place an object on the desk.
4. Return to approximately pose A.

**Pass:**

The pose-keyed reference mechanism detects the changed scene.

Provisional and confirmed latency budgets apply from the first usable returned-view frame.

---

# C10-T07 — Look-away / object-disappears / look-back

1. Establish a stable reference containing an object.
2. Look away.
3. Remove the object.
4. Return.

**Pass:**

A disappearance/change event is generated without requiring the removal itself to have been visible.

---

# C10-T08 — Pose-cache false-change test

Return repeatedly to approximately the same reference pose without changing the scene.

**Pass:**

Normal neck repeatability and registration error do not repeatedly create confirmed novelty.

---

# C10-T09 — Global illumination/exposure disturbance

Apply representative lighting and auto-exposure changes without introducing a localized object event.

**Pass:**

The system does not systematically emit high-confidence localized confirmed novelty.

---

# C10-T10 — Event-coalescing test

Introduce one object and leave it unchanged.

**Pass:**

One visual episode is generated rather than a new confirmed event every processing cycle.

---

# C10-T11 — Static-room soak

Operate Makad for:

\[
\boxed{\geq1\text{ hour}}
\]

in an ordinary unchanged indoor environment with representative idle neck motion enabled.

No deliberate scene changes are introduced.

### V1 confirmed false-event target

\[
\boxed{\leq2\ confirmed\ false\ novelty\ events/hour}
\]

Provisional events may occur more frequently because they have substantially lower behavioural cost.

The important product criterion is that Makad does not repeatedly perform false curiosity/head-attention reactions.

---

# C10-T12 — Human-attention priority

Establish active SPEC-09 human interaction.

Create an incidental confirmed object novelty elsewhere.

**Pass:**

The event reaches arbitration but does not automatically steal physical attention from the active human target.

---

# C10-T13 — Offline deterministic replay

Record a validation sequence containing:

- head motion;
- scene changes;
- look-away/look-back;
- exposure changes.

Replay the same camera/joint data repeatedly.

**Pass:**

The novelty system produces the same event sequence and materially identical timing classification under identical configuration.

---

# C10-T14 — Replay parameter iteration

Modify one novelty threshold/persistence policy and replay the same recording.

**Pass:**

The developer can objectively compare:

- event latency;
- provisional count;
- confirmed count;
- false positives

without physically repeating the scene.

---

# C10-T15 — Show-and-tell target geometry

Present an object centred within the defined presentation zone.

**Pass:**

The default semantic crop contains the intended object with sufficient surrounding margin for useful semantic interpretation.

---

# C10-T16 — Multiple-object ambiguity

Place multiple plausible objects in the inspection crop without one clearly satisfying the presentation convention.

**Pass:**

The system can return:

`ambiguous_target`

instead of confidently inventing target selection.

---

# C10-T17 — 0.4 m focus test

Present representative objects around:

\[
\boxed{0.4\text{ m}}
\]

from the camera.

**Pass:**

Candidate frames satisfy the calibrated sharpness requirement.

---

# C10-T18 — Pixels-on-target test

Measure projected width of representative small objects at the show-and-tell distance.

**Pass:**

\[
\boxed{
N_{object}
\geq
N_{semantic}
}
\]

for the candidate camera/FOV configuration.

Failure blocks final camera selection.

---

# C10-T19 — Backend resolution-degradation test

Using the Makad object set, progressively reduce effective target resolution.

Measure:

- correct answers;
- uncertainty;
- confidently wrong answers.

Determine:

\[
N_{semantic}
\]

at the chosen acceptable quality point.

This test shall occur before final camera lock.

---

# C10-T20 — Frame-quality blur test

Collect deliberately:

- sharp;
- moderately blurred;
- severely motion-blurred

frames.

Compute the configured blur metric.

**Pass:**

The quality gate reliably rejects frames known to be unusable using thresholds calibrated for the chosen camera.

---

# C10-T21 — Exposure-quality test

Provide:

- acceptable exposure;
- severe highlight clipping;
- severe shadow clipping.

**Pass:**

The exposure metric identifies unusable cases sufficiently for semantic capture gating.

---

# C10-T22 — Acquisition timeout

Continuously prevent acquisition of a valid semantic frame.

**Pass:**

Within:

\[
\boxed{\leq750\text{ ms}}
\]

and after no more than:

\[
\boxed{3}
\]

reacquisition attempts, the request terminates with:

`epistemic_outcome = unusable_image`.

---

# C10-T23 — Bearing retention

Present and semantically inspect an object.

After inference completes, inspect the semantic result.

**Pass:**

The result still contains:

- source ROI;
- capture timestamp;
- capture-time physical bearing.

A late behaviour can therefore orient toward the original observation without reconstructing geometry from the current head pose.

---

# C10-T24 — Orthogonal failure taxonomy

Exercise:

1. visually ambiguous object with functioning backend;
2. unknown object;
3. network disconnection;
4. backend timeout.

**Pass:**

Visual uncertainty appears in `epistemic_outcome`.

Infrastructure failure appears in `system_outcome`.

They are not conflated.

---

# C10-T25 — Working-state latency

Issue a semantic request.

Measure request acceptance to `semantic_processing`.

**Pass target:**

\[
\boxed{\leq150\text{ ms}}
\]

so Makad can begin expressive thinking immediately.

---

# C10-T26 — Semantic cancellation/stale result

Begin slow remote inference.

Cancel the interaction before completion.

**Pass:**

The remote operation may physically finish if it cannot be preempted, but the stale response does not trigger an obsolete Makad behaviour.

---

# C10-T27 — Shared-accelerator blocking test

If semantic inference shares an accelerator with SPEC-09:

1. measure the longest non-preemptible semantic occupancy;
2. run SPEC-09 simultaneously.

**Pass:**

\[
T_{nonpreemptible}\leq J_{9,shared}
\]

and SPEC-09 maintains its own timing requirements.

If this cannot be demonstrated, that local semantic scheduling architecture is rejected.

---

# C10-T28 — Shared-memory coexistence stress test

Run maximum representative SPEC-10 semantic load concurrently with SPEC-09.

Measure:

- SPEC-09 p50/p95/p99 latency;
- dropped frames;
- accelerator utilization;
- DRAM bandwidth if observable;
- thermal throttling.

**Pass:**

SPEC-09 remains within its finalized requirements.

---

# C10-T29 — One-hour semantic/thermal coexistence

Run representative repeated semantic use while SPEC-09 remains active.

**Pass:**

No thermal or memory-resource drift eventually causes SPEC-09 degradation.

---

# C10-T30 — 30-object semantic benchmark

Test approximately 30 physical Makad-relevant objects across:

- multiple views;
- normal indoor lighting;
- handheld presentation;
- approximately 0.4 m;
- representative framing.

Record separately:

- correct/useful;
- uncertain/refusal;
- confidently wrong;
- infrastructure failure;
- latency.

---

# C10-T31 — Semantic regression rerun

Change semantic backend/version/configuration.

Rerun the same object suite.

**Pass:**

Results can be compared directly against the previous baseline.

---

# C10-T32 — Local-only privacy test

Set:

`visual_cloud_enabled = false`

Attempt every available semantic behaviour.

Monitor network traffic.

**Pass:**

No camera-derived visual payload leaves Makad.

---

# C10-T33 — Novelty privacy test

Leave cloud vision enabled but generate only novelty events without semantic requests.

**Pass:**

No image upload occurs.

---

# C10-T34 — Uplink-indicator coupling

Trigger remote visual inference.

Monitor:

- network transfer timing;
- uplink eye-state timing.

**Pass:**

The uplink visual state activates **before** outbound camera-derived payload begins and remains associated with the remote visual operation.

---

# C10-T35 — Transfer-path bypass test

Inspect/code-test all visual remote-backend integrations.

**Pass:**

Camera-derived network transfer cannot occur outside the Visual Uplink Gate.

---

# C10-T36 — Minimum-payload test

Perform ordinary show-and-tell.

Inspect the transmitted image.

**Pass:**

The default centre semantic crop is transmitted rather than the whole room frame unless full-scene context was explicitly required.

---

# C10-T37 — No-image-log test

Perform multiple semantic requests under normal runtime logging.

**Pass:**

Logs contain operational metadata but not raw frames.

---

# C10-T38 — Process/backend failure isolation

Force:

- SPEC-10 crash;
- backend exception;
- network timeout.

**Pass:**

SPEC-08/SPEC-09 and motor-control operation remain functional.

---

# 8. Internal consistency / design review

## 8.1 The largest former hole — novelty latency — is now closed

Novelty no longer has three unrelated tune-later parameters.

The architecture now starts from user-visible reaction:

\[
\boxed{
150\text{ ms provisional}
\rightarrow
400\text{ ms confirmed}
}
\]

and derives processing cadence from it.

That is the correct direction of design.

---

## 8.2 Pose-keyed reference frames are now load-bearing

This is arguably more important than fancy visual saliency.

Without them Makad cannot perform:

> look away → someone changes desk → look back → curiosity.

That behaviour is precisely the sort of thing that makes a small companion robot appear environmentally aware.

---

## 8.3 Kinematic compensation and pose caching complement each other

They solve slightly different problems.

### Kinematic warp

Useful for:

- nearby-in-time frames;
- small pose changes;
- cheap self-motion prediction.

### Pose-keyed cache

Useful for:

- look-away/look-back;
- large temporal gaps;
- returning to previously observed views.

Both use the same physical camera-pose source.

They should not become competing independent geometry systems.

---

## 8.4 Close-range parallax remains the hard novelty case

A single homography cannot perfectly align a 3D scene when the camera translates.

Because Makad's camera moves around a neck pivot rather than its own optical centre:

- close objects;
- large head rotations;
- nearby background layers

remain difficult.

Pose-keyed same-view comparison reduces the problem considerably.

SPEC-10 should not expand into dense depth estimation merely to remove the final residual.

---

## 8.5 Camera tradeoff is now expressed correctly

The previous version only said:

> "camera must focus at 0.4 m."

The actual selection problem is:

\[
\text{human coverage/FOV}
\leftrightarrow
\text{pixels per degree}
\leftrightarrow
\text{small-object semantics}
\]

The new \(N_{semantic}\) gate catches this before component lock.

---

## 8.6 Centre-crop convention deliberately avoids an extra detector

C10-R49 can now be implemented without secretly introducing a class-agnostic object detector.

V1 relies on:

> person presents object centrally.

That is appropriate for Makad's show-and-tell behaviour.

Object proposals/segmentation can be added later only if another behaviour requires them.

---

## 8.7 Accelerator "preemption" has been corrected

The old phrase was physically misleading.

The system can cancel a **request**.

It cannot necessarily interrupt silicon already executing a graph.

The important quantity is now:

\[
T_{nonpreemptible}
\]

rather than thread priority.

If shared hardware cannot satisfy SPEC-09's timing headroom, that architecture loses.

---

## 8.8 Memory bandwidth remains a potential hardware-selection killer

Even if accelerator scheduling looks correct, a large semantic model may still disrupt human tracking through shared memory pressure.

Therefore SPEC-10/SPEC-09 coexistence must be benchmarked on the exact intended hardware before final compute selection.

---

## 8.9 The privacy state is no longer ornamental

The privacy signal is now structurally tied to the uplink path.

That matters far more than whether the indicator is:

- blue;
- blinking;
- an icon;
- or a physical LED.

For Makad specifically, an expressive eye state is more coherent with the established character language and avoids unnecessary enclosure complexity.

---

## 8.10 Local-only mode is architecturally cheap now and expensive later

Adding a single privacy gate now costs little.

Retrofitting it after multiple services begin independently uploading images would be much more difficult.

Therefore local-only belongs in SPEC-10 now.

---

## 8.11 Offline replay is essential for iteration speed

Without replay, tuning novelty means repeatedly:

- position Makad;
- move the neck;
- place/remove objects;
- reproduce lighting;
- record results.

With synchronized frame + joint-state replay, the exact same sequence can be tested hundreds of times.

This is development infrastructure with unusually high leverage and should be implemented early.

---

## 8.12 The one-hour soak matters more than a short accuracy demo

A novelty detector can look excellent in five controlled demonstrations while producing a false event every few minutes during ordinary operation.

That failure makes Makad look:

> distracted, twitchy or paranoid.

The ≤2 confirmed false events/hour V1 requirement gives the system an explicit calmness criterion.

---

## 8.13 Event coalescing must stay out of SPEC-11's job

SPEC-10:

> "this is still the same event."

SPEC-11:

> "yes, but I don't care anymore."

If both systems independently decrease event probability over time, debugging behavioural suppression becomes unnecessarily difficult.

The boundary is now explicit.

---

## 8.14 Build order changes

SPEC-10 cannot be treated as a late software feature.

The correct project sequence is approximately:

```text
candidate camera
      +
basic controlled neck mule
      +
timestamped measured joint pose
             ↓
early moving-camera novelty prototype
             ↓
pose-cache + replay validation
             ↓
camera FOV/focus/pixels-on-target validation
             ↓
compute coexistence benchmark
             ↓
camera + compute lock
```

This should happen before cosmetic final CAD.

Otherwise the project could discover far too late that:

- the chosen FOV starves semantic resolution;
- the camera cannot focus close enough;
- pose compensation is unreliable;
- or the compute platform cannot coexist with SPEC-09.

---

# 9. Final decisions carried forward

## FINAL / MUST

1. SPEC-10 consists of a **lightweight novelty path** and a **slow semantic path**.

2. Core design rule remains:

> **Notice, then optionally name.**

3. Novelty uses two confidence/timing tiers.

4. Provisional novelty shall exist within:

\[
\boxed{\leq150\text{ ms}}
\]

of first usable evidence.

5. Confirmed novelty shall exist within:

\[
\boxed{\leq400\text{ ms}}
\]

for qualifying persistent change.

6. Novelty shall be evaluated at an equivalent maximum interval of approximately:

\[
\boxed{100\text{ ms / 10 Hz minimum}}
\]

while active.

7. Provisional novelty can support eyes-first attention.

8. Confirmed novelty can support later physical head attention.

9. Novelty requires **pose-keyed reference observations**.

10. Look-away/look-back changes are explicitly in scope.

11. SPEC-10 inherits SPEC-09's **kinematic feedforward camera-motion model**.

12. SPEC-10 shall not develop a competing ego-motion coordinate system.

13. Close-range parallax is explicitly recognized as a limitation of pure rotational homography.

14. Novelty events distinguish provisional/confirmed state.

15. Novelty event payload supports:

`appeared | disappeared | changed | moved | unknown_change`.

16. Event coalescing belongs to SPEC-10.

17. Habituation/interest decay belongs to SPEC-11.

18. V1 show-and-tell uses a computable **centre-presentation convention**.

19. Default semantic transmission uses a centre inspection crop.

20. A separate objectness detector is not required for V1.

21. SPEC-08 camera evaluation must include both:

- close focus;
- pixels-on-target.

22. Approximately 0.4 m remains the show-and-tell test distance.

23. The minimum required object pixel width is represented by:

\[
N_{semantic}
\]

and must be experimentally determined before camera lock.

24. Semantic frame quality shall measure blur, exposure and camera-motion state.

25. Semantic frame acquisition is bounded to:

\[
\boxed{3\ attempts,\ \leq750\text{ ms}}
\]

26. Semantic results retain capture-time ROI and target bearing.

27. System failure and visual uncertainty are separate result axes.

28. Local semantic inference is not assumed hardware-preemptible.

29. Shared-accelerator semantic occupancy shall obey SPEC-09-derived:

\[
T_{nonpreemptible}\leq J_{9,shared}
\]

30. Memory-bandwidth/thermal contention must also be measured.

31. If shared local inference cannot protect SPEC-09, semantic work must move to another scheduling/device/backend architecture.

32. Deterministic novelty offline replay is mandatory.

33. Replay data includes synchronized camera frames **and joint state**.

34. Semantic backend/version information is logged.

35. The 30-object benchmark is rerunnable after backend changes.

36. Static-room soak testing is mandatory.

37. V1 confirmed false-novelty target:

\[
\boxed{\leq2/hour}
\]

during a one-hour unchanged-room soak with representative idle motion.

38. All camera-derived remote visual traffic passes through one **Visual Uplink Gate**.

39. Makad has a global **local-only visual mode**.

40. Novelty alone cannot authorize cloud upload.

41. Remote visual analysis has a distinct Makad eye-display state.

42. That display state is driven by the same mechanism authorizing/performing the network transfer.

43. Raw semantic images are not stored/logged by default.

44. SPEC-10 requires controlled moving-neck hardware for full validation.

45. Moving-camera novelty prototyping must occur **before final camera and compute lock**.

---

## TARGET

1. local closed-set recognition;
2. local/remote semantic routing;
3. burst-based best-frame selection;
4. tracked-human novelty suppression;
5. class-agnostic object/ROI proposal if a later behaviour actually needs it;
6. multi-view semantic consistency.

---

## EXPLICITLY DEFERRED

- face recognition;
- persistent object identity;
- remembered object locations;
- semantic maps;
- SLAM;
- OCR;
- arbitrary pointing/reference resolution;
- grasp/manipulation perception;
- safety-grade depth;
- continuous VLM vision;
- surveillance/history recording.

---

# SPEC-10 FINAL DESIGN PRINCIPLE

> **Notice, then optionally name.**

Makad's first perceptual responsibility is to realise quickly:

> **"Something happened over there."**

Its eyes can acknowledge that almost immediately.

Its head can follow once the event becomes credible.

Only after a behaviour genuinely needs semantic information should Makad spend the compute, latency and possible privacy cost required to ask:

> **"What is it?"**
