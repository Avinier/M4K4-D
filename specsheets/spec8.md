# MAKAD — SPEC-08 v1.1

## Camera & Visual Sensing Foundation

**Status:** Revised working engineering specification  
**Supersedes:** SPEC-08 v1.0  
**Primary functionality:** Makad will see its surroundings through a camera and use that visual information as part of its behaviour. At minimum it must understand whether a person is present and roughly where relevant things are in its field of view.

---

# 1. Scope of this specification

SPEC-08 defines the **physical camera, image-acquisition pipeline, optical geometry, timebase, calibration, moving-camera compensation, basic person-presence perception, social-gaze target representation, visual uncertainty, camera health, and visual interfaces required by later Makad perception behaviours**.

The intended chain is:

\[
\boxed{
\text{physical scene}
\rightarrow
\text{camera}
\rightarrow
\text{time-corrected calibrated observation}
\rightarrow
\text{typed visual hypotheses}
\rightarrow
\text{direction + uncertainty}
}
\]

This specification covers:

- one primary head-mounted colour camera,
- camera mechanical mounting,
- camera mass/COM/inertia implications,
- field of view,
- image resolution and frame rate,
- focus and indoor-light requirements,
- camera intrinsics,
- distortion calibration,
- camera-to-head extrinsics,
- camera-to-display geometry,
- camera pose while neck axes move,
- rolling-shutter timing,
- camera/neck clock synchronization,
- exposure and gain control,
- head-roll compensation for perception,
- motion blur,
- image-content health,
- basic person presence,
- distinction between face/head/body detections,
- multiple simultaneous observations,
- definition of the point Makad is visually attending to,
- coarse range priors needed for parallax correction,
- visual-bearing uncertainty,
- calibration persistence/lifecycle,
- privacy and frame-retention policy,
- compute/bandwidth implications,
- camera cable routing,
- failure/degraded modes,
- outputs required by SPEC-09, SPEC-10, SPEC-11, SPEC-19 and the behaviour system.

This specification **does not yet define**:

- persistent temporal person tracking,
- re-identification,
- long-term identity,
- final face-tracking control policy,
- object/scene class taxonomy,
- a VLM,
- entry/exit event logic,
- locomotion control,
- obstacle avoidance,
- SLAM,
- mapping,
- mandatory stereo vision,
- mandatory RGB-D,
- safety-grade metric depth estimation.

The project deliberately treats functionality #8–11 and #19 as a shared perception stack while still specifying their responsibilities separately.

---

# 2. Existing Makad decisions that constrain this spec

## 2.1 The camera is physically part of the moving head

SPEC-02's intended kinematic structure is:

\[
\boxed{
Body
\rightarrow
Yaw
\rightarrow
Pitch
\rightarrow
Roll
\rightarrow
Head/Camera
}
\]

Powered roll, pitch and yaw are all mandatory for V1. A 2-DOF yaw/pitch head is not a V1-complete fallback; perception and calibration must therefore support the selected three-axis mechanism across its validated envelope.

Therefore the camera is not fixed to Makad's body frame.

Every neck movement changes camera pose.

---

## 2.2 Physical joint state is authoritative

SPEC-02 already requires perception to use actual physical neck orientation rather than blindly using commanded actuator positions.

If a joint encoder or transmission state becomes untrustworthy, perception must stop claiming that its camera transform is trustworthy.

SPEC-08 therefore inherits:

\[
\boxed{
q_{measured}
\neq
q_{commanded}
\text{ unless demonstrated otherwise}
}
\]

for geometric perception.

---

## 2.3 Camera motion must not look like world motion

SPEC-02 explicitly requires moving-camera-aware perception and includes a stationary-target test while the neck moves.

SPEC-08 must provide all timing, calibration and coordinate information necessary for this to work.

---

## 2.4 Neck precision creates a camera precision requirement

Current SPEC-02 design targets include approximately:

- smallest deliberate physical neck motion:

\[
4^\circ
\]

- maximum reversal backlash:

\[
1^\circ
\]

- TARGET backlash:

\[
0.5^\circ
\]

- TARGET repeatability:

\[
\pm0.5^\circ
\]

- validation logging:

\[
\ge100\,Hz
\]

A camera coordinate system that is wrong by several degrees would make those mechanical targets irrelevant.

---

## 2.5 Head roll is an expressive feature

Head roll is intended to create visible inquisitive/character tilts.

The perception subsystem therefore cannot simply assume:

\[
roll=0
\]

for every frame.

---

## 2.6 Camera and display are spatially separated

The camera is intended to sit above/around the display rather than coinciding with the animated eyes.

Therefore:

\[
T^{head}_{camera}
\neq
T^{head}_{display}
\]

This matters because:

> centring someone's face in the camera does not automatically make Makad's rendered eyes appear to look at that person's eyes.

SPEC-08 must carry both geometries.

---

## 2.7 The visual output is used by later physical behaviours

Makad will eventually use perception to:

- track people,
- orient its head,
- animate its screen eyes,
- turn its mobile base,
- approach/follow where appropriate.

The visual representation therefore must be geometric enough for future behaviour, not merely:

```text
person_detected = true
```

---

# 3. Engineering reasoning / architecture

# 3.1 Primary sensing architecture

Makad V1 shall use **one primary forward-looking colour camera rigidly mounted to the moving head**.

Stereo or RGB-D shall not be made mandatory without a later demonstrated requirement.

The camera is intended to answer:

1. Is a person visually present?
2. Which visual hypotheses are present?
3. Which hypothesis contains a face/head suitable for social gaze?
4. Where is that target relative to the camera?
5. Approximately where is that target relative to Makad's head/body?
6. How uncertain is that answer?

---

# 3.2 There are three different geometric quantities

These must not be conflated.

### A. Camera ray

From an image coordinate:

\[
(u,v)
\]

and calibrated intrinsics:

\[
K
\]

we obtain a ray:

\[
\mathbf r_c
=
K^{-1}
\begin{bmatrix}
u\\v\\1
\end{bmatrix}
\]

This requires **no depth**.

---

### B. Camera-relative angular bearing

The direction of that ray can be represented as camera-relative yaw/pitch.

This also requires **no depth**.

---

### C. Bearing from another displaced reference point

If we want the direction from:

- the neck rotation centre,
- head centre,
- animated-eye plane,
- body frame,

and the camera is translationally displaced from that reference point, we need some information about where along the camera ray the target lies.

This is the parallax problem.

---

# 3.3 Parallax requires coarse range — but not safety-grade depth

Let the camera optical centre be displaced from the desired reference point by perpendicular baseline:

\[
b_\perp
\]

and the target distance be:

\[
d
\]

Approximate parallax magnitude is:

\[
\theta_p
\approx
\frac{b_\perp}{d}
\]

for small angles.

For:

\[
b_\perp=0.05m
\]

and:

\[
d=0.5m
\]

\[
\theta_p
\approx0.1rad
\approx5.7^\circ
\]

Therefore ignoring camera translation is unacceptable at close desk-companion distances.

But we do **not** need precise metric depth.

If the true target distance is \(d\) and we instead use coarse estimate \(\hat d\), the approximate residual parallax error is:

\[
\Delta\theta_p
\approx
b_\perp
\left|
\frac{1}{d}
-
\frac{1}{\hat d}
\right|
\]

For:

\[
b_\perp=0.05m,
\quad
d=0.5m,
\quad
\hat d=0.65m
\]

\[
\Delta\theta_p
\approx
0.023rad
\approx1.3^\circ
\]

So a rough anthropometric/object-size prior can be good enough for **social gaze correction** while remaining completely unsuitable for collision safety.

That distinction is now explicit:

\[
\boxed{
\text{coarse gaze-range prior}
\neq
\text{safety-grade depth sensing}
}
\]

---

# 3.4 Visual target semantics must be defined

A generic person bounding-box centre is **not** Makad's social gaze target.

For a standing human:

```text
person bounding-box centre
≈ torso

social gaze target
≈ face / eye region
```

Those may differ by tens of degrees at close distance.

SPEC-08 therefore introduces a typed observation hierarchy.

### FACE_GAZE

Best social-attention target.

Preferred reference point:

- eye-region midpoint if landmarks are available,
- otherwise calibrated face-centre estimate.

### HEAD

Head/face region available but not enough information for a precise eye reference.

### UPPER_BODY

Upper body visible.

May support approximate head-location inference with greater uncertainty.

### PERSON_BODY

Whole/partial person detected with no reliable head target.

Useful for:

- presence,
- coarse orientation,
- reacquisition.

Not suitable for claiming 3° social-gaze accuracy.

---

# 3.5 Face and person detection are complementary

A person/body detector helps when someone is:

- side-on,
- back turned,
- partially occluded,
- too far for reliable face detection.

A face/head detector helps determine where Makad should actually appear to look.

The architecture therefore needs evidence for both **human presence** and **social gaze location**.

This may be implemented using:

- one multi-output model,
- two models,
- face landmarks,
- body keypoints,
- another validated architecture.

SPEC-08 freezes the required information, not the ML model.

---

# 3.6 Multiple observations are normal

The output of basic perception shall be:

\[
\boxed{
VisualObservation[]
}
\]

not one global target.

Temporal identity continuity belongs to SPEC-09.

SPEC-08 only needs to produce multiple simultaneous hypotheses from the current frame.

---

# 3.7 Full moving-camera transform

Conceptually:

\[
T^{body}_{camera}(t)
=
T^{body}_{neck}
(q(t))
T^{neck}_{head}
(q(t))
T^{head}_{camera}
\]

If another future body joint changes camera pose, that transform must be inserted into the chain.

The camera-to-head transform contains:

\[
R
\]

and:

\[
t
\]

not merely an angular offset.

---

# 3.8 Display geometry is a separate transform

The animated-eye/display plane shall have its own calibrated/CAD transform:

\[
\boxed{
T^{head}_{display}
}
\]

A target point:

\[
P_{target}
\]

can therefore produce different directions for:

### Physical head orientation

\[
g_{head}
\]

### Rendered eye direction

\[
g_{eyes}
\]

because the virtual eyes and camera do not share an origin.

This avoids the robot equivalent of the videoconference gaze-offset problem.

---

# 3.9 Error budget

The old specification independently gave both geometric calibration and complete bearing a 3° target.

That is invalid because end-to-end bearing contains the geometric errors plus target localisation and parallax.

A provisional **design allocation** is therefore introduced.

These numbers are not claims of perfectly independent Gaussian noise; RSS is being used as an engineering budgeting tool.

| Contribution | Provisional allocation |
|---|---:|
| Intrinsic/distortion direction error | 0.4° |
| Camera→head extrinsic error | 0.7° |
| Physical joint-state error | 0.6° |
| Timing/synchronization contribution | 0.5° |
| Residual parallax/range-prior error | 1.0° |
| Face/social-target localisation | 1.5° |

Approximate RSS:

\[
E_{RSS}
=
\sqrt{
0.4^2+
0.7^2+
0.6^2+
0.5^2+
1.0^2+
1.5^2
}
\]

\[
\boxed{
E_{RSS}\approx2.12^\circ
}
\]

This leaves margin below the intended:

\[
\boxed{
3^\circ
}
\]

end-to-end median social-gaze-bearing target.

The allocations are provisional and shall be revised after real measurements.

---

# 3.10 The 3° target applies only to a valid social-gaze observation

If Makad has a reliable face/head target:

\[
\boxed{
E_{bearing,median}
\le3^\circ
}
\]

is the current TARGET.

If only a torso/person-body observation exists, the system shall instead:

- output the coarse direction,
- increase angular uncertainty,
- avoid falsely labelling the estimate as gaze-accurate.

---

# 3.11 Rolling shutter changes timestamp semantics

A rolling-shutter frame is not captured at one instant.

Suppose:

- first row is captured at \(t_0\),
- line time is \(t_l\),
- reference target row is \(y\).

Then the appropriate target timestamp is approximately:

\[
t_{target}
=
t_0
+
y\,t_l
\]

using the appropriate sensor-origin convention.

Exposure midpoint must also be considered.

Therefore SPEC-08 shall define a canonical frame timing model.

Raw camera-driver timestamp semantics may differ between devices, so the software must convert driver timing into Makad's canonical representation.

---

# 3.12 Canonical rolling-shutter time representation

For rolling-shutter operation the preferred canonical quantities are:

\[
t_{row0,mid}
\]

= mid-exposure timestamp of first active image row,

and:

\[
t_{line}
\]

= temporal offset per active row.

Then:

\[
t(y)
=
t_{row0,mid}
+
y\,t_{line}
\]

For a detection whose social reference point is at vertical coordinate \(y_r\):

\[
t_{observation}
=
t(y_r)
\]

and neck state should be interpolated at that time.

Global-shutter cameras reduce to approximately:

\[
t_{line}=0
\]

for this purpose.

---

# 3.13 Clock synchronization is an explicit subsystem requirement

A camera timestamp may originate in the SBC's camera clock domain while neck state may originate in an MCU clock domain.

Those clocks shall not simply be assumed identical.

A mapping such as:

\[
t_{system}
=
a\,t_{MCU}
+
b
\]

shall be maintained where necessary.

Where:

- \(b\) represents offset,
- \(a\) represents relative clock skew.

---

# 3.14 Resynchronization interval must follow measured drift

If relative clock drift is:

\[
\epsilon
\]

and maximum additional drift error allowed between synchronization events is:

\[
\Delta t_{drift,max}
\]

then:

\[
T_{resync}
\le
\frac{
\Delta t_{drift,max}
}{
|\epsilon|
}
\]

For example, a 10 ppm relative drift produces approximately:

\[
36ms/hour
\]

so a 10 ms allowance would be exhausted in roughly:

\[
1000s
\approx16.7min
\]

if no correction occurs.

The system shall therefore determine synchronization interval from **measured clock behaviour**, not an arbitrary hourly resync.

---

# 3.15 Timing should be budgeted as angular error

If head angular speed is:

\[
\omega
\]

and pose timestamp error is:

\[
\Delta t
\]

then:

\[
E_t
\approx
|\omega|\Delta t
\]

At:

\[
60^\circ/s
\]

and:

\[
5ms
\]

\[
E_t
=
0.3^\circ
\]

At:

\[
10ms
\]

\[
E_t
=
0.6^\circ
\]

Therefore time alignment must be considered part of the visual bearing error budget.

---

# 3.16 Head roll should be compensated before face inference

Makad's roll is intentional character motion.

A 20–30° tilted image can unnecessarily reduce detector performance.

Because the actual head roll is already measured, the person/face path shall normally use either:

1. an image rectified into approximately head-upright orientation before inference, or
2. a detector empirically demonstrated to retain equivalent performance throughout the entire required roll range.

For V1, **explicit roll normalization is the preferred design**.

---

# 3.17 Resolution must be derived from target pixels, not bearing pixels

Pixel angular resolution is unlikely to dominate bearing accuracy.

But image resolution does determine whether a face is large enough to detect and localize.

Approximate projected face width is:

\[
N_f
\approx
\frac{
f_x W_f
}{
Z
}
\]

where:

- \(W_f\) = physical face width,
- \(Z\) = target distance,
- \(f_x\) = focal length in pixels.

The normal processing mode therefore needs enough pixels on the face at maximum intended social-interaction distance.

Provisional design goal:

\[
\boxed{
\ge60\ pixels
}
\]

across a normally oriented face for **social-gaze localisation** at the maximum intended gaze distance.

Simple person-presence detection may remain usable below this.

The final floor shall be frozen after detector benchmarking rather than treating 60 px as a universal model constant.

---

# 3.18 Exposure is part of the motion-control interface

Approximate angular image smear is:

\[
\beta
\approx
|\omega|t_e
\]

where:

- \(t_e\) = exposure,
- \(\omega\) = relevant camera angular velocity.

The camera pipeline should use measured head velocity to bound exposure during motion.

Preferred exposure constraint:

\[
t_{e,max}
\approx
\frac{
\beta_{max}
}{
|\omega|
}
\]

where lighting permits.

---

# 3.19 50 Hz mains flicker conflicts with the original 0.5° blur target

In a 50 Hz mains environment, many artificial lights produce approximately 100 Hz intensity variation.

A 10 ms exposure is a natural flicker-compatible timescale.

At:

\[
60^\circ/s
\]

and:

\[
10ms
\]

\[
\beta
=
0.6^\circ
\]

Therefore the old:

\[
\beta\le0.5^\circ
\]

normal-motion target is unnecessarily incompatible with flicker-friendly exposure behaviour.

SPEC-08 v1.1 changes the policy to:

### Preferred when illumination permits

\[
\beta\le0.5^\circ
\]

### Normal-motion TARGET

\[
\boxed{
\beta\le0.7^\circ
}
\]

If maintaining that target requires an exposure shorter than the lighting's flicker-friendly value, detection reliability takes priority over cosmetically perfect banding.

---

# 3.20 Auto-exposure needs explicit behavioural states

The image pipeline should distinguish at least:

### STATIC / LOW-MOTION

Normal AE/AWB operation.

### ACTIVE TRACKING

Exposure bounded by measured head velocity.

### FAST EXPRESSIVE GESTURE

Prefer:

- temporarily holding exposure/gain/AWB where useful,
- preventing AE hunting caused only by the gesture,
- rejecting/de-weighting unusable frames,
- immediate reacquisition when the gesture settles.

This avoids the failure mode:

```text
head turns toward bright window
→ AE hunts
→ detection disappears
→ gaze controller searches
→ exposure changes again
→ unstable loop
```

---

# 3.21 Image-content health is distinct from camera transport health

A camera can successfully deliver 30 fps while showing:

- a hand covering the lens,
- a fogged window,
- severe blur,
- complete overexposure,
- complete underexposure,
- a wall at centimetres distance.

The perception stack therefore needs an image usability state independent of:

> camera connected/disconnected.

---

# 3.22 Confidence is not uncertainty

A detector confidence score such as:

\[
0.87
\]

does not mean:

\[
\pm1.2^\circ
\]

The gaze system instead needs a directional uncertainty estimate.

Each geometrically usable observation shall therefore carry at least approximate uncertainty such as:

\[
\sigma_{yaw},
\quad
\sigma_{pitch}
\]

or an equivalent covariance representation.

For V1 this may initially be an empirically calibrated heuristic.

---

# 3.23 Calibration is persistent configuration

Calibration is not something run once in a notebook and forgotten.

Makad must know whether it is:

- calibrated,
- uncalibrated,
- calibration-invalid,
- camera-failed.

Those are separate runtime states.

---

# 3.24 Privacy architecture must exist before long-duration camera testing

The camera is intended to operate continuously.

Therefore SPEC-08 establishes:

\[
\boxed{
\text{processing by default}
\neq
\text{recording by default}
}
\]

Normal operation shall not require persistent raw-frame recording.

---

# 4. Formal requirements

## Camera hardware and mechanics

### C8-R01 — Primary visual sensor — MUST-HAVE

Makad shall contain at least one forward-facing colour-capable camera available to the onboard perception system.

---

### C8-R02 — Head-mounted architecture — MUST-HAVE

The primary camera shall be rigidly mounted downstream of all neck axes affecting head orientation.

---

### C8-R03 — Camera mass properties — MUST-HAVE

The neck mass model shall include:

- camera module,
- sensor PCB,
- lens,
- camera bracket,
- optical window,
- moving connector,
- moving cable section.

Their effects on:

\[
m,\ COM,\ I_{yaw},\ I_{pitch},\ I_{roll}
\]

shall be included before actuator freeze.

---

### C8-R04 — Mechanical transform stability — MUST-HAVE

Normal handling and required neck acceleration shall not allow the camera-to-head transform to shift enough to invalidate calibrated visual-bearing performance.

---

### C8-R05 — Full camera extrinsics — MUST-HAVE

Makad shall maintain:

\[
T^{head}_{camera}
\]

including both:

- rotation,
- translation.

---

### C8-R06 — Display transform — MUST-HAVE

Makad shall maintain:

\[
T^{head}_{display}
\]

or an equivalent calibrated representation of the animated-eye/display plane relative to the head.

---

### C8-R07 — Camera/display physical geometry recorded — MUST-HAVE

CAD/final assembly documentation shall record:

- camera optical-centre location,
- display plane location,
- approximate animated-eye reference points,
- relevant neck rotation centres.

---

### C8-R08 — Boresight alignment — TARGET

Camera optical axis should remain approximately aligned with Makad's apparent face-forward direction.

Provisional target:

\[
\le2^\circ
\]

yaw/pitch boresight offset where mechanically practical.

Residual misalignment shall be represented in calibration.

---

### C8-R09 — No required-FOV self-occlusion — MUST-HAVE

Normal required visual field shall not be substantially blocked by:

- shell,
- brow,
- screen bezel,
- ears,
- cable,
- neck covers.

---

## Optical performance

### C8-R10 — FOV derived from interaction geometry — MUST-HAVE PROCESS

Final HFOV/VFOV shall be selected from measured interaction geometry rather than arbitrary camera specifications.

Provisional HFOV design region:

\[
\boxed{
70^\circ-90^\circ
}
\]

remains TARGET.

---

### C8-R11 — Vertical interaction coverage — MUST-HAVE

The normal camera mode shall permit observation of nearby seated/standing users across intended interaction geometry without requiring constant neck-pitch saturation.

---

### C8-R12 — Capture resolution — MUST-HAVE

The camera shall support at least a **720p-class** mode at useful perception frame rate.

4K is not required.

---

### C8-R13 — Minimum target-pixel criterion — MUST-HAVE

Processing resolution shall not be selected by compute convenience alone.

For the selected social-gaze detector, maximum intended face-gaze distance shall provide enough face pixels for validated localisation performance.

Provisional TARGET:

\[
\boxed{
N_{face}\ge60px
}
\]

across normal face width.

---

### C8-R14 — Frame-rate capability — MUST-HAVE

Normal visual acquisition shall support:

\[
\boxed{
\ge30FPS
}
\]

at the selected perception mode.

---

### C8-R15 — Focus performance — MUST-HAVE

The optical system shall remain acceptably focused over the intended person-interaction distance range.

Autofocus is not mandatory.

---

### C8-R16 — Autofocus stability — TARGET

If autofocus is used, focus hunting shall not routinely interrupt person/face perception during normal head movement.

---

### C8-R17 — Indoor lighting — MUST-HAVE

Basic person-presence perception shall function under ordinary indoor lighting.

Provisional validation floor:

\[
\boxed{
100lux
}
\]

at the interaction region.

Lower-light operation remains TARGET.

---

### C8-R18 — Optical-window quality — MUST-HAVE

Any protective cover shall not create unacceptable:

- blur,
- glare,
- reflection,
- distortion,
- vignetting.

Final calibration shall include the intended optical window.

---

## Calibration

### C8-R19 — Intrinsic calibration — MUST-HAVE

For every geometric perception mode, Makad shall maintain appropriate:

\[
f_x,\ f_y,\ c_x,\ c_y
\]

and the required lens-distortion model.

---

### C8-R20 — Distortion-model selection — MUST-HAVE

The calibration model shall be chosen based on held-out calibration performance.

A standard low-order distortion model shall not be retained merely because it is the default if wide-angle peripheral residuals remain excessive.

---

### C8-R21 — Spatial calibration validation — MUST-HAVE

Calibration quality shall be evaluated by image radius/region rather than global mean error alone.

At minimum results shall separately report:

- central region,
- middle region,
- outer usable region.

---

### C8-R22 — Central calibration target — TARGET

Central/middle held-out reprojection error should target approximately:

\[
\le0.5px
\]

for the normal operating mode.

---

### C8-R23 — Peripheral calibration target — TARGET

Within the declared usable peripheral FOV, held-out error should target:

\[
\le1.0px
\]

for most calibration observations.

If this cannot be achieved, the usable FOV or distortion model shall be revised.

---

### C8-R24 — Calibration mode binding — MUST-HAVE

Calibration shall be associated with every setting that materially changes intrinsics, including as applicable:

- resolution,
- crop,
- binning,
- digital scaling,
- lens/focus state.

---

### C8-R25 — Persistent calibration storage — MUST-HAVE

Calibration shall be persistently stored with:

- calibration version,
- camera identifier where available,
- image mode,
- timestamp/date,
- calibration parameters,
- validation result.

---

### C8-R26 — Calibration boot validation — MUST-HAVE

At startup Makad shall detect whether the active camera/mode has a compatible valid calibration.

---

### C8-R27 — Explicit uncalibrated state — MUST-HAVE

If calibration is missing/incompatible:

- image-space detection may continue,
- calibrated body/head bearing shall be invalid,
- precise gaze control shall not silently proceed.

---

### C8-R28 — Service recalibration — MUST-HAVE

Camera removal or any mechanical operation capable of altering:

\[
T^{head}_{camera}
\]

shall trigger calibration verification before precise gaze is considered valid.

---

## Timing and moving-camera compensation

### C8-R29 — Declared system timebase — MUST-HAVE

The vision/neck architecture shall define one logical system time domain used for geometric perception.

---

### C8-R30 — Clock-domain mapping — MUST-HAVE

If camera and neck measurements originate from separate clocks, their mapping shall estimate at least:

- offset,
- relative skew/drift where material.

---

### C8-R31 — Synchronization uncertainty — MUST-HAVE

During normal visual tracking, effective camera-to-joint-state temporal alignment shall be sufficient that timing contributes no more than approximately:

\[
\boxed{
0.5^\circ
}
\]

to the provisional bearing-error allocation.

For representative:

\[
60^\circ/s
\]

head motion, this corresponds to approximately:

\[
8.3ms
\]

maximum effective timing error.

Preferred TARGET:

\[
\le5ms
\]

---

### C8-R32 — Resynchronization policy — MUST-HAVE

Clock resynchronization interval shall be calculated from measured drift and required timing budget.

It shall not be assumed that boot-time synchronization remains valid indefinitely.

---

### C8-R33 — Sync diagnostics — MUST-HAVE

Logging shall expose at least:

- estimated clock offset,
- estimated skew where used,
- most recent synchronization time,
- current synchronization uncertainty.

---

### C8-R34 — Frame sequence and stale-frame detection — MUST-HAVE

The acquisition layer shall distinguish:

- genuinely new frame,
- repeated/stale frame,
- dropped frame,
- stalled stream,
- camera failure.

---

### C8-R35 — Canonical capture timestamp — MUST-HAVE

Each frame shall be mapped into a canonical acquisition-time representation rather than using arbitrary software-receipt time.

---

### C8-R36 — Rolling-shutter timing model — MUST-HAVE WHEN APPLICABLE

For rolling-shutter operation the camera shall have known/characterised:

- timestamp semantics,
- active-frame readout direction,
- line time or equivalent row timing,
- exposure timing.

---

### C8-R37 — Row-aware observation time — MUST-HAVE WHEN APPLICABLE

The effective timestamp used for a detection shall account for the row containing its visual reference point.

Conceptually:

\[
t_{obs}
=
t_{row0,mid}
+
y_r t_{line}
\]

or equivalent.

---

### C8-R38 — Rolling-shutter confidence degradation — MUST-HAVE

If target extent/head motion makes a single reference-row correction insufficient because geometric skew becomes excessive, the observation shall be:

- corrected more completely,
- assigned increased uncertainty,
- or rejected.

---

### C8-R39 — Moving-camera transform — MUST-HAVE

For every geometrically valid observation the system shall be capable of obtaining camera pose from the measured mechanism state corresponding to observation time.

---

### C8-R40 — Physical pose failure behaviour — MUST-HAVE

If neck physical pose cannot be trusted:

- camera/image observations may continue,
- calibrated head/body/world-relative target direction shall become invalid,
- precise visual tracking shall be inhibited.

This is consistent with SPEC-02's existing failure architecture.

---

## Roll handling

### C8-R41 — Roll-normalized person/face perception — MUST-HAVE

During normal perception, head roll shall be compensated before the social-person/face inference path, unless the selected detector is explicitly validated to provide equivalent performance over the required roll envelope.

Preferred V1 solution:

\[
\boxed{
\text{measured roll}
\rightarrow
\text{image orientation normalization}
}
\]

---

### C8-R42 — Roll transform remains physically preserved — MUST-HAVE

Image de-rotation for inference shall not erase the actual physical roll state from the geometric coordinate model.

The detector may see an upright image while Makad still knows:

\[
roll_{physical}\neq0
\]

---

## Exposure, flicker and motion

### C8-R43 — Exposure-control access — MUST-HAVE

The selected camera/driver shall provide sufficient control over exposure/gain behaviour to implement a motion-aware visual pipeline.

Passive metadata-only access is insufficient.

---

### C8-R44 — Motion-aware exposure ceiling — MUST-HAVE CAPABILITY

The perception system shall be able to bound exposure using measured camera/head angular velocity.

Conceptually:

\[
t_{e,max}
=
\frac{
\beta_{target}
}{
|\omega|
}
\]

where practicable.

---

### C8-R45 — Normal motion blur — TARGET

During ordinary tracking motion the preferred smear target remains:

\[
\beta\le0.5^\circ
\]

where illumination permits.

The normal V1 TARGET is relaxed to:

\[
\boxed{
\beta\le0.7^\circ
}
\]

to remain compatible with practical 50 Hz lighting behaviour.

---

### C8-R46 — Flicker-aware exposure — MUST-HAVE

Under 50 Hz mains lighting, exposure control shall avoid unnecessarily severe flicker/banding while maintaining perception performance.

If required motion exposure is shorter than a flicker-friendly duration:

\[
\boxed{
\text{perception reliability takes priority over cosmetic banding}
}
\]

---

### C8-R47 — AE convergence — TARGET

After a representative sudden scene-brightness change, exposure should return to a detection-usable state within approximately:

\[
\boxed{
500ms
}
\]

without causing prolonged visual-target loss.

This is provisional and shall be validated against the selected camera.

---

### C8-R48 — Fast-gesture AE/AWB policy — MUST-HAVE

During known rapid expressive head gestures the imaging system shall support an intentional policy such as:

- freeze AE/AWB temporarily,
- constrain exposure/gain changes,
- lower observation confidence,
- suppress gaze correction,
- immediately reacquire after settling.

The final strategy is implementation-dependent.

---

### C8-R49 — Fast-motion degraded perception — MUST-HAVE

Makad is not required to maintain perfect perception during every extreme expressive recoil/gesture.

It is required to prevent corrupted measurements from destabilizing gaze behaviour.

---

### C8-R50 — Shutter architecture — TARGET

Rolling shutter is acceptable for V1 if tests pass.

Global shutter remains a contingency/TARGET rather than a mandatory component requirement.

---

## Visual observation model

### C8-R51 — Observation list — MUST-HAVE

The perception layer shall output zero or more simultaneous observations:

\[
\boxed{
VisualObservation[]
}
\]

rather than only one global target.

---

### C8-R52 — Observation type — MUST-HAVE

Each human-related observation shall identify its available target semantics, for example:

- `FACE_GAZE`,
- `HEAD`,
- `UPPER_BODY`,
- `PERSON_BODY`.

Equivalent naming is acceptable.

---

### C8-R53 — Human-presence evidence — MUST-HAVE

The visual system shall provide evidence sufficient to determine whether a person is visually present even when a reliable face is not available.

---

### C8-R54 — Social-gaze target — MUST-HAVE

When a usable face/head is available, Makad shall produce a visual reference point corresponding to the person's face/head rather than defaulting to full-body bounding-box centre.

---

### C8-R55 — Preferred face reference point — TARGET

Where suitable landmarks are available, the preferred social-gaze reference shall approximate the person's eye-region/central-face direction.

If only a face box is available, a calibrated face reference point may be used with greater uncertainty.

---

### C8-R56 — Body-only fallback semantics — MUST-HAVE

If no reliable face/head target exists but a person is visible:

- `PERSON_BODY`/`UPPER_BODY` presence may remain valid,
- coarse body direction may remain valid,
- social-gaze accuracy shall not be claimed.

---

### C8-R57 — Single-frame fusion — MUST-HAVE

When compatible face/head and person-body evidence overlap in one frame, they shall be associated into one human observation where practical.

This does **not** require temporal identity tracking.

---

### C8-R58 — Ambiguous hypotheses — MUST-HAVE

If evidence cannot be safely associated, hypotheses shall remain separate rather than inventing an identity association.

---

### C8-R59 — Image coordinates — MUST-HAVE

Every observation shall include:

- bounding region or equivalent,
- defined visual reference point,
- normalized image coordinate or equivalent.

---

### C8-R60 — Camera ray — MUST-HAVE

For calibrated image modes, the defined reference point shall be convertible to a ray in the camera optical frame.

---

### C8-R61 — Detector confidence — MUST-HAVE

Each observation shall expose detector/classification confidence or equivalent evidence quality.

---

### C8-R62 — Angular uncertainty — MUST-HAVE

Geometrically usable observations shall also expose estimated directional uncertainty separate from detector confidence.

At minimum:

\[
\sigma_{yaw},\sigma_{pitch}
\]

or equivalent.

---

### C8-R63 — Observation timestamp — MUST-HAVE

Each observation shall contain the effective acquisition timestamp corresponding to its reference point, including rolling-shutter correction where required.

---

### C8-R64 — Observation staleness — MUST-HAVE

Consumers shall be able to determine:

- observation age,
- stale state,
- lost state.

Stale observations shall not remain indefinitely active.

---

## Coarse range and parallax

### C8-R65 — Coarse range prior — MUST-HAVE WHEN PARALLAX CORRECTION IS USED

When converting a camera ray into a direction referenced to a significantly displaced head/neck/display origin, the system shall use:

- a coarse range estimate,
- or explicitly retain the ray as camera-origin-relative.

It shall not silently pretend camera translation is zero.

---

### C8-R66 — Range-prior sources — TARGET

Coarse range may come from validated cues such as:

- face width,
- head width,
- upper-body/person geometry,
- later ToF data,
- another validated estimator.

Exact implementation is deferred.

---

### C8-R67 — Range uncertainty — MUST-HAVE

Where coarse range is used, its uncertainty shall contribute to the observation's angular uncertainty.

---

### C8-R68 — Parallax residual allocation — TARGET

For valid social-gaze observations within the normal interaction range, residual parallax contribution should target approximately:

\[
\boxed{
\le1^\circ
}
\]

within the provisional error budget.

---

### C8-R69 — No safety-depth claim — MUST-HAVE

A coarse gaze-range prior shall not be interpreted as certified obstacle range.

Safety/collision behaviour shall use its own validated sensing architecture.

---

## Bearing accuracy and jitter

### C8-R70 — Geometric calibration contribution — TARGET

Camera intrinsics + extrinsics + measured joint transform, excluding detector target-localisation and range-prior errors, should target substantially better than the final 3° bearing requirement.

Provisional geometric target:

\[
\boxed{
\le1.2^\circ
}
\]

median in validation.

---

### C8-R71 — Social-gaze bearing accuracy — TARGET

When a valid `FACE_GAZE`/equivalent observation exists under calibrated normal conditions:

\[
\boxed{
median\ error\le3^\circ
}
\]

Target:

\[
\boxed{
90\%\ of\ observations\le5^\circ
}
\]

The exact percentile may be revised after prototype statistics.

---

### C8-R72 — Body-only accuracy classification — MUST-HAVE

Body-only observations are exempt from C8-R71.

Their lower precision shall be expressed through larger angular uncertainty.

---

### C8-R73 — Stationary observation jitter — TARGET

For a stationary clear face target with the head stationary, raw or minimally processed visual bearing should target approximately:

\[
\boxed{
RMS\ jitter\le1^\circ
}
\]

over a representative short interval.

This is a perception-measurement target; final motion smoothing belongs partly to SPEC-09/gaze control.

---

### C8-R74 — Uncertainty calibration — TARGET

Across held-out validation data, reported angular uncertainty should correlate with actual bearing error.

A first V1 target is that approximately 90% of tested ground-truth bearings fall within the system's declared ~2σ-like uncertainty envelope.

This is a calibration-quality target rather than a strict probabilistic guarantee.

---

## Image-content health

### C8-R75 — Image usability monitoring — MUST-HAVE

The perception pipeline shall monitor image-content quality sufficient to distinguish at least:

- usable,
- degraded,
- unusable.

---

### C8-R76 — Health cues — TARGET

The image-health system should consider inexpensive cues such as:

- sharpness,
- extreme darkness,
- extreme saturation,
- low variance,
- excessive blur,
- prolonged exposure saturation.

Exact algorithm is deferred.

---

### C8-R77 — Unusable-image behaviour — MUST-HAVE

If frames continue arriving but image content is unusable:

- precise targeting shall be invalidated,
- visual confidence shall fall,
- the system shall distinguish this from transport failure.

---

## Camera/display social-gaze mapping

### C8-R78 — Separate eye-direction solution — MUST-HAVE

The visual target used to command physical head orientation shall not automatically be used unchanged for rendered screen-eye direction.

---

### C8-R79 — Display-origin compensation — MUST-HAVE

When sufficient range/geometry is available, rendered-eye direction shall account for:

\[
T^{head}_{display}
\]

so the eyes appear to look toward the same external target as the physical head.

---

### C8-R80 — Empirical social-gaze correction — TARGET

A small empirically calibrated eye-direction correction may be layered on the geometric display transform if naive-observer tests show systematic apparent-gaze bias.

---

## Latency

### C8-R81 — Person-presence latency — MUST-HAVE

For basic person presence in normal operating conditions:

\[
\boxed{
\le250ms
}
\]

from acquisition to usable observation shall be the initial maximum.

---

### C8-R82 — Gaze-path latency — TARGET

Architecture shall target approximately:

\[
\boxed{
\le100ms
}
\]

from image acquisition to updated target-bearing estimate for the later tracking loop.

---

### C8-R83 — Latency telemetry — MUST-HAVE

Perception diagnostics shall distinguish at least:

- capture time,
- preprocessing,
- inference,
- geometry/fusion,
- output publication.

This allows latency to be decomposed instead of reporting one unexplained number.

---

## Compute, transport, power and thermal

### C8-R84 — Camera bandwidth calculation — MUST-HAVE BEFORE COMPONENT FREEZE

Actual required camera-link/memory bandwidth shall be calculated for selected modes.

For raw frames:

\[
Bandwidth
=
W
\times
H
\times
bytes/pixel
\times
FPS
\]

with compression/copies/decode treated appropriately.

---

### C8-R85 — Compute profiling — MUST-HAVE BEFORE COMPUTE FREEZE

Representative vision workloads shall be profiled for:

- CPU,
- GPU/NPU,
- RAM,
- memory bandwidth,
- preprocessing,
- inference,
- latency.

---

### C8-R86 — Camera power budget — MUST-HAVE

Camera average/peak consumption shall be included in Makad's final power budget.

---

### C8-R87 — Thermal integration — MUST-HAVE

Continuous visual operation shall not produce unacceptable heating of:

- camera,
- display,
- microphone area,
- printed head,
- nearby compute electronics.

---

## Cabling and serviceability

### C8-R88 — Neck cable routing — MUST-HAVE

Camera wiring through the moving neck shall comply with SPEC-02 requirements for:

- bend radius,
- strain relief,
- mechanical stops,
- edge protection,
- cable torque.

---

### C8-R89 — Harness endurance inheritance — MUST-HAVE

Camera wiring shall participate in the existing minimum neck-harness test of:

\[
\boxed{
50,000cycles
}
\]

with:

\[
100,000cycles
\]

as TARGET.

---

### C8-R90 — Camera serviceability — MUST-HAVE

The camera shall be replaceable without destructive head disassembly.

Repeatable locating features should be used where practical.

---

## Privacy

### C8-R91 — Visible camera-active indication — MUST-HAVE

Makad shall provide a user-visible indication whenever its camera is actively capturing visual data.

Implementation may be hardware- or system-driven provided failure behaviour is understood.

---

### C8-R92 — No persistent recording by default — MUST-HAVE

Normal perception shall not require continuous raw-frame storage.

---

### C8-R93 — Diagnostic recording opt-in — MUST-HAVE

Any recording used for debugging/validation shall be deliberately enabled rather than occurring silently in normal operation.

---

### C8-R94 — Diagnostic retention policy — MUST-HAVE

Recorded debug video/images shall have a defined storage location and deletion/retention policy.

They shall not accumulate indefinitely without operator awareness.

---

### C8-R95 — Frame logging separation — MUST-HAVE

Normal R48-style numeric/metadata diagnostics shall be capable of operating without storing the corresponding raw frames.

---

### C8-R96 — Visual data transmission — MUST-HAVE ARCHITECTURAL RULE

Raw camera frames shall not be transmitted off-device by default.

Any future feature requiring external/cloud visual processing must explicitly declare that dependency and privacy behaviour.

---

## Faults

### C8-R97 — Camera transport failure — MUST-HAVE

Camera loss/stall shall:

1. invalidate visual target state,
2. inhibit visual closed-loop tracking,
3. prevent stale target commands,
4. report the fault,
5. permit safe bounded non-visual behaviour.

---

### C8-R98 — Perception-process failure — MUST-HAVE

Failure of visual inference while the camera remains operational shall be distinguishable from camera hardware failure.

---

### C8-R99 — Calibration-invalid failure — MUST-HAVE

Invalid calibration shall be distinguishable from:

- no person visible,
- detector failure,
- camera failure.

---

### C8-R100 — Image-health failure — MUST-HAVE

Lens obstruction/extreme unusable image shall be distinguishable from camera transport failure.

---

## Diagnostics

### C8-R101 — Visual diagnostics — MUST-HAVE

Validation logging shall expose at least:

- frame index,
- raw/canonical timestamp,
- rolling-shutter reference-row timestamp if used,
- exposure,
- gain where available,
- active image mode,
- image-health state,
- detections,
- observation types,
- reference points,
- detector confidence,
- coarse range and uncertainty where available,
- camera ray,
- angular uncertainty,
- measured neck state used,
- clock offset/skew estimate,
- camera-pose validity,
- calibration version,
- processing latency,
- dropped-frame count.

Raw frames are **not** implied by this requirement.

---

# 5. Interfaces and dependencies

## SPEC-01 — Animated face

SPEC-08 now imposes a real geometry requirement on the display subsystem.

It requires:

\[
T^{head}_{display}
\]

or equivalent physical geometry.

SPEC-01/gaze animation will eventually receive a target direction specifically transformed for the display-eye origin.

Therefore:

```text
camera aim
≠
head aim
≠
screen-eye aim
```

although all three refer to the same external target.

---

## SPEC-02 — Neck/head movement

SPEC-02 provides:

- physical yaw/pitch/roll,
- state timestamps,
- mechanism validity,
- physical velocity.

SPEC-08 uses these for:

- camera pose,
- rolling-shutter pose lookup,
- motion-aware exposure,
- roll normalization.

SPEC-08 provides:

- target bearing,
- uncertainty,
- validity.

It does not directly command actuators.

---

## SPEC-03 — Upper-body motion

Any later body joint that changes camera/display pose must enter the transform tree with measured physical state.

SPEC-08 does not force a powered torso joint to exist.

---

## SPEC-09 — Person/face tracking

SPEC-09 inherits:

- multiple visual observations,
- face/head/body semantics,
- social reference point,
- coarse range,
- angular uncertainty,
- timestamp,
- pose validity.

SPEC-09 adds:

- temporal continuity,
- target selection,
- identity persistence over short intervals,
- reacquisition,
- tracking control.

---

## SPEC-10 — Broader visual understanding

Objects/scenes can reuse:

- camera calibration,
- timebase,
- coordinate-frame system,
- image-health system.

Not every object needs the human social-gaze hierarchy.

---

## SPEC-11 — Presence events

SPEC-11 converts observation history into:

- appeared,
- approached,
- left,
- remained.

SPEC-08 only provides current evidence.

---

## SPEC-18 — Collision sensing

Coarse visual range shall not replace dedicated collision/proximity validation.

---

## SPEC-19 — Perception-controlled locomotion

SPEC-19 may consume:

- body-relative target bearing,
- coarse range where useful,
- uncertainty.

Locomotion shall not assume the SPEC-08 range prior is a collision-safe distance measurement.

---

## SPEC-20 — Behaviour arbitration

SPEC-20 consumes semantic visual observations/events.

It should not be reasoning directly from raw frames.

---

# 6. Quantities still requiring CAD/prototype/component validation

## Physical geometry

- exact camera optical-centre location,
- camera↔neck baseline,
- camera↔display baseline,
- display-eye locations,
- head frame definition,
- camera boresight,
- shell occlusion.

---

## Interaction geometry

- Makad camera height,
- desk height,
- normal seated user distance,
- normal standing user distance,
- closest expected social interaction distance,
- maximum distance at which face gaze is expected.

---

## Optics

- exact HFOV,
- exact VFOV,
- lens distortion class,
- fixed-focus versus autofocus,
- useful depth of field,
- low-light behaviour.

---

## Detector geometry

- minimum person pixels,
- minimum face pixels,
- minimum reliable landmark pixels,
- face-reference-point error,
- body-only directional uncertainty.

---

## Range prior

- estimator type,
- usable distance interval,
- percent/range error,
- parallax residual versus distance,
- fallback behaviour if no range estimate is available.

---

## Timing

- camera-driver timestamp meaning,
- frame readout direction,
- line time,
- MCU/SBC clock drift,
- synchronization uncertainty,
- appropriate resync cadence.

---

## Exposure

- available manual controls,
- AE/AWB lock behaviour,
- flicker suppression,
- blur/detection trade-off,
- brightness-step convergence.

---

## Compute

- processing resolution,
- detector architecture,
- roll-rectification cost,
- inference device,
- memory bandwidth,
- concurrent audio/display/control load.

---

## Privacy implementation

- hardware vs software camera indicator,
- debug recording UI,
- retention duration,
- storage location.

---

# 7. Acceptance tests

## C8-T01 — Camera streaming

Run the intended normal camera mode continuously.

Measure:

- actual FPS,
- dropped frames,
- stalls,
- timestamps.

### Pass

Normal stream operates at required frame rate without persistent unexplained interruption.

---

## C8-T02 — FOV and self-occlusion

Measure actual HFOV/VFOV using a known angular target.

Repeat at representative:

- yaw,
- pitch,
- roll.

### Pass

Required interaction field remains usable without unacceptable self-occlusion.

---

## C8-T03 — Face-pixel-distance test

Place representative faces/face targets at increasing distance.

Record face width in pixels.

### Pass

At maximum intended social-gaze distance, selected processing mode satisfies the final detector-derived minimum.

Provisional target:

\[
\ge60px
\]

---

## C8-T04 — Intrinsic calibration spatial test

Collect calibration data covering:

- centre,
- middle,
- outer usable FOV,
- several orientations,
- several distances.

Use held-out images for validation.

### Record separately

- centre residual,
- middle residual,
- outer residual.

### TARGET

Central/middle:

\[
\le0.5px
\]

Most outer usable observations:

\[
\le1.0px
\]

If not, change distortion model/FOV.

---

## C8-T05 — Camera-to-head extrinsic test

Lock the neck at accurately measured orientations.

Observe known targets.

Isolate error caused by camera-to-head extrinsics as far as practical.

### TARGET

Extrinsic contribution consistent with approximately:

\[
\le0.7^\circ
\]

design allocation.

---

## C8-T06 — Geometric-stack test

Using a known stationary target, test:

- intrinsics,
- extrinsics,
- measured neck state,

while excluding detector target-centre ambiguity where possible by using a fiducial/known point.

### TARGET

Median transformed bearing error:

\[
\boxed{
\le1.2^\circ
}
\]

This replaces the old 3° geometric test.

---

## C8-T07 — Parallax/range-prior test

Place a target at multiple known distances and lateral/vertical bearings.

Compare:

1. camera-origin ray only,
2. falsely assuming camera translation is zero,
3. coarse-range parallax compensation.

### TARGET

Within normal interaction geometry, coarse-range correction keeps residual parallax contribution approximately:

\[
\le1^\circ
\]

where a valid range prior is declared.

---

## C8-T08 — Range-prior degradation test

Deliberately bias the range estimate.

Measure resulting angular error.

### Pass

Reported uncertainty increases appropriately and the system does not silently claim high-precision social gaze from a badly uncertain range estimate.

---

## C8-T09 — Person/face semantic test

Prepare scenes containing:

- front-facing person,
- profile person,
- back-turned person,
- seated person,
- partially occluded person.

### Pass

The system distinguishes when it has:

- body presence only,
- head evidence,
- usable social-gaze face target.

A torso centre shall not be silently labelled as a face-gaze target.

---

## C8-T10 — Multi-person test

Use scenes with at least:

- zero people,
- one person,
- two people,
- three people.

### Pass

The system outputs a list of simultaneous hypotheses rather than collapsing the scene into one unspecified person.

No temporal identity requirement is imposed here.

---

## C8-T11 — Social target-point validation

For front-facing people, compare the reported social-gaze target with a manually/fiducially defined eye/face reference point.

### TARGET

Target-localisation contribution should be compatible with approximately:

\[
1.5^\circ
\]

design allocation under normal conditions.

---

## C8-T12 — End-to-end face-bearing test

Place a face/face target at measured bearings across normal FOV and distance.

Use the full normal pipeline.

### TARGET

Median:

\[
\boxed{
\le3^\circ
}
\]

and approximately 90%:

\[
\boxed{
\le5^\circ
}
\]

when a valid `FACE_GAZE` observation exists.

Body-only observations are evaluated separately.

---

## C8-T13 — Body-only uncertainty test

Repeat with the face hidden but body visible.

### Pass

- person presence remains possible where appropriate,
- observation type changes,
- uncertainty increases,
- the system does not claim the C8-T12 social-gaze accuracy.

---

## C8-T14 — Clock drift test

Run camera + neck timing for at least:

\[
4hours
\]

without reboot.

Record:

- camera timestamps,
- MCU timestamps,
- estimated offset,
- estimated skew,
- resync events.

### Pass

Effective timing uncertainty remains within the allocated angular timing budget throughout the test.

A slowly increasing bearing error is a synchronization failure even if every individual sensor appears healthy.

---

## C8-T15 — Rolling-shutter line-time test

For the selected rolling-shutter mode, characterise:

- readout direction,
- total active readout time,
- line time,
- raw timestamp semantics.

Use controlled LED/strobe or another practical timing fixture if needed.

### Pass

The software can convert raw timestamps into its declared canonical row-time representation.

---

## C8-T16 — Row-timestamp moving-head test

Place stationary visual targets near:

- top of image,
- centre,
- bottom.

Move the head at representative angular velocity.

Compare bearing error:

1. without row correction,
2. with row correction.

### Pass

Row correction measurably removes systematic top-vs-bottom timing bias where rolling shutter makes it relevant.

---

## C8-T17 — Moving-camera stationary-target test

Keep target stationary.

Move Makad through:

- yaw,
- pitch,
- roll,
- combined motion.

### Pass

The target remains approximately stationary in reconstructed head/body-relative direction and does not create a self-excited gaze oscillation.

---

## C8-T18 — Moving-target + moving-camera test

Move a human/target laterally while Makad simultaneously performs tracking-like head motion.

This is the actual operating case.

### Measure

- end-to-end latency,
- bearing error,
- dropped observations,
- timestamp alignment,
- reacquisition.

### TARGET

Performance remains stable enough for SPEC-09 to consume without systematic runaway lag.

This test intentionally does not yet define SPEC-09's final tracking success criteria.

---

## C8-T19 — Roll-normalization test

Use a person/face target with head roll at approximately:

\[
0^\circ,\ \pm10^\circ,\ \pm20^\circ
\]

and the final required roll envelope.

Compare face-target reliability with/without normalization.

### Pass

Normal perception path maintains acceptable recall/localisation throughout the required expressive roll range.

---

## C8-T20 — Motion-blur/exposure test

Move the head at several known angular velocities.

Record:

- exposure,
- gain,
- calculated smear,
- detector performance.

Check:

\[
\beta
\approx
\omega t_e
\]

### TARGET

Ordinary tracking motion:

\[
\beta\le0.7^\circ
\]

where practical.

Preferred:

\[
\le0.5^\circ
\]

when lighting permits.

---

## C8-T21 — 50 Hz lighting test

Test under representative Indian indoor mains-powered lighting.

Compare:

- flicker/banding,
- exposure,
- blur,
- detection reliability.

### Pass

Exposure policy chooses a usable trade-off.

Detector reliability shall not be sacrificed solely to make the image cosmetically band-free.

---

## C8-T22 — AE transition test

Create a repeatable luminance transition such as:

- normal room → bright window,
- bright area → darker wall.

Move the head through the transition.

### TARGET

Perception returns to a usable exposure state in approximately:

\[
\le500ms
\]

without prolonged unstable gaze correction.

---

## C8-T23 — Fast-gesture exposure test

Execute representative rapid expressive gestures.

### Pass

The system either:

- retains usable perception,
- or intentionally lowers confidence/rejects affected frames,

then reacquires after settling.

No corrupted observation should create a large false gaze correction.

---

## C8-T24 — Stationary-face jitter test

Keep both Makad and a clear face target stationary.

Record at least:

\[
30s
\]

of observations.

### TARGET

Bearing jitter:

\[
\boxed{
RMS\le1^\circ
}
\]

for a valid face-gaze observation under normal lighting.

---

## C8-T25 — Uncertainty calibration test

Use a ground-truth bearing set including:

- centre/periphery,
- near/far,
- bright/dim,
- frontal/profile.

Compare actual error against reported uncertainty.

### TARGET

Approximately 90% of test observations lie inside the declared ~2σ-like uncertainty envelope.

If not, uncertainty calibration must be revised.

---

## C8-T26 — Image-health obstruction test

Test:

- clear lens,
- hand over lens,
- heavily blurred cover,
- extreme overexposure,
- extreme darkness,
- blank/near-uniform wall.

### Pass

Image-health status changes appropriately and precise gaze becomes invalid when image content is not trustworthy.

---

## C8-T27 — Stale-frame test

Freeze/repeat camera buffers while keeping the process alive.

### Pass

The pipeline identifies stale data and does not continue presenting old detections as current.

---

## C8-T28 — Camera-failure test

Disable camera transport.

### Pass

Visual tracking invalidates and Makad enters defined degraded behaviour.

---

## C8-T29 — Neck-pose-failure test

Keep camera working while invalidating one required physical neck orientation.

### Pass

Image detections continue where possible.

Body/head-referenced geometric gaze becomes invalid.

---

## C8-T30 — Calibration-state test

Run Makad with:

1. correct calibration,
2. missing calibration,
3. calibration for wrong mode,
4. invalidated camera remount.

### Pass

The runtime explicitly distinguishes these states and does not silently perform calibrated gaze with incompatible parameters.

---

## C8-T31 — Camera remount repeatability

Calibrate camera, remove it, reinstall it using intended service procedure, and remeasure extrinsics.

### Result

This determines whether service removal can preserve calibration or must always invalidate it.

No assumption is made in advance.

---

## C8-T32 — Camera/display gaze-offset test

Place target at known distance and direction.

Calculate:

- camera aim,
- head aim,
- display-eye aim.

### Pass

The display-eye solver applies the display offset rather than reusing camera-centred direction unchanged.

---

## C8-T33 — Naive-observer social-gaze test

Recruit at least:

\[
5
\]

people who did not tune the system.

Test at approximately three representative interaction distances.

For each presentation ask only:

> Where does Makad appear to be looking?

Forced-choice answers:

- at you,
- above you,
- below you,
- left of you,
- right of you.

### MUST-HAVE provisional criterion

“At you”:

\[
\boxed{
\ge70\%
}
\]

of judgements.

### TARGET

\[
\boxed{
\ge85\%
}
\]

with no strong systematic directional bias.

If there is consistent above/below/left/right bias, tune the empirical display-eye calibration rather than altering camera calibration to compensate.

---

## C8-T34 — Person-presence validation

Use a representative dataset/test sequence containing:

- empty scenes,
- people entering,
- seated people,
- standing people,
- partial people,
- profile/back views.

### TARGET

Approximately:

\[
90\%
\]

correct clear-scene presence decisions across the agreed Makad validation set.

This is a project acceptance metric, not a general CV benchmark.

---

## C8-T35 — Empty-room false-presence test

Operate for at least:

\[
30min
\]

in a representative empty room containing:

- screens,
- posters,
- furniture,
- normal visual clutter.

### Pass

No persistent phantom-person state.

Short detector spikes may occur but must not create sustained presence without supporting evidence.

---

## C8-T36 — Privacy default-state test

Operate Makad normally.

Inspect storage and network behaviour.

### Pass

- visual processing runs,
- camera-active indication is visible,
- no persistent raw-frame archive is created by default,
- raw camera stream is not silently sent off-device.

---

## C8-T37 — Diagnostic-recording test

Enable debug recording intentionally.

### Pass

The system clearly distinguishes this mode from normal operation and stores recordings only in the documented location.

---

## C8-T38 — Cable endurance

Include the production-intent camera harness in SPEC-02's neck-cycle fixture.

Minimum:

\[
50,000cycles
\]

TARGET:

\[
100,000cycles
\]

Afterward verify:

- continuity,
- enumeration,
- image integrity,
- full frame rate,
- absence of intermittent dropouts.

---

## C8-T39 — Four-hour visual endurance

Operate camera/perception for at least:

\[
4hours
\]

with:

- idle head motion,
- people appearing/disappearing,
- roll,
- tracking-like movements,
- occasional fast gestures.

Log:

- temperature,
- FPS,
- frame loss,
- sync offset,
- sync drift,
- latency,
- calibration state,
- image health,
- perception faults.

### Pass

No progressive degradation breaks normal visual operation.

---

## C8-T40 — Compute and bandwidth integration

Run camera perception simultaneously with representative:

- display animation,
- audio,
- actuator telemetry,
- behaviour software.

Measure:

- CPU/GPU/NPU,
- RAM,
- memory bandwidth,
- image pipeline latency,
- dropped frames.

### Pass

The eventual system compute budget has sufficient measured margin rather than relying on isolated detector benchmarks.

---

# 8. Internal consistency / design review

## 8.1 The original parallax contradiction is now resolved

SPEC-08 no longer says both:

> translation matters

and

> depth is completely unavailable.

Instead:

\[
\boxed{
\text{camera ray}
+
\text{coarse range prior}
\rightarrow
\text{parallax-corrected social bearing}
}
\]

where needed.

But:

\[
\boxed{
\text{coarse gaze range}
\not\Rightarrow
\text{safe navigation depth}
}
\]

---

## 8.2 Full 6-DOF extrinsics remain justified

The alternative would be deliberately discarding known physical camera translation.

That would be particularly damaging at the short distances where companion-robot gaze quality matters most.

---

## 8.3 A body detector alone cannot satisfy the social-gaze requirement

The spec no longer pretends:

```text
person bbox centre
=
where Makad should look
```

The observation type determines what accuracy claims are allowed.

---

## 8.4 Face-only perception would also be wrong

Face detection can fail on:

- profile,
- back-of-head,
- partial occlusion,
- longer distances.

Therefore human-presence evidence and social-gaze evidence remain distinct.

---

## 8.5 The end-to-end 3° requirement now has a budget

The current budget is:

\[
2.12^\circ
\]

RSS-like design allocation.

This is not yet a measured system result.

If prototype contributors exceed their allocation, we will know **which contributor consumed the margin** rather than discovering only that T12 fails.

---

## 8.6 Detector localisation is currently the largest error allocation

At:

\[
1.5^\circ
\]

it consumes more budget than calibration, timing or individual joint error.

That is appropriate.

Once a camera has reasonable resolution, ML target definition is likely to dominate social-gaze direction more than pixel quantisation.

---

## 8.7 Time synchronization is now an architecture item, not a software afterthought

The system must solve:

\[
camera\ time
\leftrightarrow
joint\ time
\]

continuously enough that clock drift does not slowly corrupt gaze over a long run.

This will influence:

- MCU protocol,
- actuator bus,
- SBC architecture,
- validation software.

---

## 8.8 Rolling shutter is now treated primarily as spatiotemporal geometry

The spec no longer models it only as a visually bent-image problem.

A target at the bottom of the image can genuinely correspond to a different physical head angle than a target near the top.

The row-time model captures this.

Residual geometric distortion during rapid motion remains a separate issue.

---

## 8.9 Global shutter remains unnecessary until evidence says otherwise

Row-aware timing, exposure control and frame rejection may be enough.

If T15/T16/T18/T20 fail systematically, global shutter becomes justified by measured failure rather than theoretical anxiety.

---

## 8.10 50 Hz flicker and blur are no longer contradictory requirements

The spec now explicitly permits the normal motion smear target to reach about:

\[
0.7^\circ
\]

and prioritizes detector reliability if an exposure shorter than the flicker-friendly interval is required.

---

## 8.11 AE may be a bigger practical problem than nominal sensor sensitivity

A sensor that handles static low light well but takes half a second to recover after every head turn toward a window could still make Makad feel blind.

Component evaluation therefore must include exposure dynamics.

---

## 8.12 Resolution now has two separate roles

### Bearing quantisation

Usually easy.

### Minimum target size

Potentially limiting.

Therefore processing downsampling must be justified against:

\[
N_{face}
\]

rather than simply:

> “640×480 is enough because each pixel is only 0.1°.”

---

## 8.13 Calibration is now judged where Makad actually finds new people

A new person often first appears near the image periphery.

A global reprojection average dominated by central checkerboard points is therefore insufficient.

---

## 8.14 Confidence no longer masquerades as geometric quality

Detector confidence and bearing uncertainty are two different outputs.

This will matter later when SPEC-09 decides whether to:

- move immediately,
- filter,
- wait,
- reacquire.

---

## 8.15 Visual jitter can directly become servo jitter

If the camera target randomly jumps:

\[
\pm1.5^\circ
\]

at 30 Hz and the gaze controller obeys it, Makad's precision mechanics will faithfully reproduce bad perception.

Therefore observation jitter needs its own test before blaming neck mechanics.

---

## 8.16 Camera-health monitoring prevents misleading failures

A covered lens is not:

> “there are no people.”

It is:

> “visual observation is unavailable.”

That distinction matters for autonomous behaviour.

---

## 8.17 Calibration state must survive reboot and maintenance

A vision demo that only works after manually running a calibration notebook is not an integrated robot subsystem.

---

## 8.18 Continuous camera use requires explicit privacy behaviour

The intended Makad is continuously perceptive.

That makes raw recording a qualitatively different choice from live processing.

Default non-retention is therefore part of the architecture now rather than an afterthought before demonstration day.

---

## 8.19 Display gaze is now correctly separated from camera gaze

The robot can physically centre a human in its camera while its rendered eyes still appear to look below them because the screen eyes sit lower.

SPEC-08 now gives this problem an explicit transform and an empirical test.

---

## 8.20 The naive-observer test is intentionally not replaced by geometry

Perfect geometric projection does not guarantee that stylised animated eyes are perceived correctly.

Makad's actual success criterion is:

> does a person feel that the droid is looking at them?

That is a perceptual requirement.

---

# 9. Final decisions carried forward

## DECIDED

1. Makad V1 uses one primary head-mounted forward-looking colour camera.

2. Camera geometry uses a full 6-DOF extrinsic transform including translation.

3. Physical measured neck orientation is required for calibrated gaze.

4. Camera pose shall correspond to the actual time the relevant image content was captured.

5. Rolling-shutter operation requires known timestamp semantics and row timing.

6. Camera and neck clocks shall share a declared logical timebase with offset/drift correction where necessary.

7. Clock synchronization shall be maintained over long runtimes rather than performed only at boot.

8. Head roll shall be compensated in the face/person perception path, unless an alternative detector is explicitly validated across the full roll range.

9. Camera intrinsics/distortion shall be calibrated and evaluated spatially across the image, including the periphery.

10. Calibration shall be persistent, versioned and mode-specific.

11. `UNCALIBRATED`, `CAMERA_FAILED`, `PERCEPTION_FAILED`, and `IMAGE_UNUSABLE` are distinct states.

12. The normal capture architecture remains approximately 720p/30-class or better.

13. Processing resolution shall additionally satisfy a detector-derived minimum target-pixel requirement.

14. Approximately 60 px face width at maximum intended social-gaze range is the current provisional TARGET.

15. Person presence and social-gaze target are separate concepts.

16. Visual output shall be a list of simultaneous observations.

17. Observations shall distinguish at least face/head/upper-body/person-body quality levels.

18. A full-body bbox centroid is not accepted as a generic social-gaze reference point.

19. Face/eye-region reference is preferred when available.

20. Body-only observations remain valid for presence/coarse orientation but do not inherit the 3° social-gaze target.

21. Detector confidence and angular uncertainty are separate quantities.

22. Visual observations shall expose directional uncertainty.

23. Coarse range estimation is permitted and required where necessary for parallax correction.

24. Coarse range used for gaze shall not be treated as collision-safe metric depth.

25. Residual parallax contribution targets approximately ≤1°.

26. The provisional bearing-error design budget is approximately 2.12° RSS-like combined contribution, leaving margin below the 3° target.

27. End-to-end valid social-gaze bearing targets ≤3° median and approximately ≤5° for 90% of normal validation observations.

28. The isolated geometric stack targets substantially better performance, approximately ≤1.2° median.

29. Normal stationary face-bearing jitter targets ≤1° RMS.

30. Camera exposure shall be controllable, not merely observable.

31. Exposure shall be capable of responding to measured head velocity.

32. Preferred motion smear remains ≤0.5° where lighting permits.

33. Normal practical motion-smear TARGET is relaxed to ≤0.7°.

34. 50 Hz flicker and motion-blur requirements shall be explicitly traded rather than treated as simultaneously absolute.

35. Detection reliability takes priority over cosmetically perfect flicker suppression.

36. AE/AWB behaviour during fast gestures shall be intentional.

37. Image-content health monitoring is mandatory.

38. Rolling shutter remains acceptable if validation passes.

39. Global shutter remains non-mandatory.

40. Autofocus remains non-mandatory.

41. Stereo/RGB-D remains non-mandatory.

42. Camera and display require separate head-frame transforms.

43. Rendered-eye gaze shall be solved separately from physical head/camera gaze.

44. Naive-observer gaze testing becomes part of camera/display integration acceptance.

45. Normal visual processing shall not imply persistent raw-video recording.

46. Camera-active state shall have a visible user-facing indication.

47. Raw frame recording shall be opt-in for debugging.

48. Raw camera frames shall not leave the robot by default.

49. Moving target + moving camera is now a required integration test.

50. Camera cable remains part of SPEC-02's ≥50k neck-cycle validation.

---

## PROVISIONAL / REQUIRES VALIDATION

- exact camera model,
- exact lens,
- exact HFOV/VFOV,
- final interaction distance envelope,
- final face-pixel threshold,
- final detector architecture,
- face landmarks versus face-box reference,
- range-prior algorithm,
- range-prior accuracy,
- final parallax allocation,
- rolling-shutter readout time,
- camera timestamp semantics,
- clock synchronization protocol,
- AE convergence target,
- final image-health algorithm,
- final uncertainty calibration,
- final privacy indicator implementation,
- final naive-observer pass percentage if mockup data suggests adjustment.

---

## EXPLICITLY DEFERRED TO SPEC-09

- persistent person identity across frames,
- target selection between multiple people,
- temporal tracking,
- target-loss hysteresis,
- reacquisition policy,
- face/person tracking controller,
- eye/head/base tracking arbitration.

---

## EXPLICITLY DEFERRED TO SPEC-10

- object-recognition taxonomy,
- scene semantics,
- useful non-human visual understanding,
- optional VLM functionality.

---

## EXPLICITLY DEFERRED TO SPEC-11

- appeared/left/approached events,
- presence timing/hysteresis,
- interaction-space event logic.

---

## EXPLICITLY DEFERRED TO SPEC-18

- obstacle/proximity sensing,
- validated collision range,
- safety-distance sensing.

---

## EXPLICITLY DEFERRED TO SPEC-19

- visual person following,
- target following distance,
- base orientation policy,
- approach/retreat behaviour.

---

# Final SPEC-08 v1.1 architecture

```text
                           PHYSICAL SCENE
                                  │
                                  ↓
                              CAMERA
                                  │
                  raw frame + sensor timing
                                  │
                 ┌────────────────┴───────────────┐
                 │                                │
                 ↓                                ↓
         IMAGE ACQUISITION                 IMAGE HEALTH
                 │
       exposure / gain / AE
                 │
        rolling-shutter model
                 │
                 ↓
        CANONICAL FRAME TIME
                 │
                 │
      clock offset/skew correction
                 │
                 ↓
       JOINT STATE @ ROW/TARGET TIME
                 │
                 │
       measured yaw/pitch/roll
                 │
                 ├───────────────┐
                 │               │
                 ↓               ↓
        ROLL NORMALIZATION   CAMERA POSE
                 │               │
                 ↓               │
        PERSON/FACE INFERENCE    │
                 │               │
      ┌──────────┼──────────┐    │
      ↓          ↓          ↓    │
    FACE       HEAD       PERSON │
      │          │          │    │
      └──────────┼──────────┘    │
                 ↓               │
         TYPED OBSERVATIONS      │
                 │               │
        defined reference point  │
                 │               │
                 ↓               │
            CAMERA RAY           │
                 │               │
       coarse range + uncertainty
                 │               │
                 └───────┬───────┘
                         ↓
               PARALLAX-CORRECTED
                 TARGET GEOMETRY
                         │
                 angular uncertainty
                         │
          ┌──────────────┴───────────────┐
          ↓                              ↓
   HEAD/BODY TARGET              DISPLAY-EYE TARGET
          │                              │
      SPEC-09                        SPEC-01
   tracking/gaze                  rendered eye aim
          │
          ↓
   SPEC-02 / SPEC-19
   head + later base
```

The central result carried forward is now:

\[
\boxed{
\text{Visual target}
+
\text{target semantics}
+
\text{intrinsics}
+
\text{range prior where needed}
+
\text{camera/display geometry}
+
\text{actual mechanism state at the correct capture time}
+
\text{uncertainty}
=
\text{usable Makad gaze perception}
}
\]

not merely:

\[
\text{person bbox}
\rightarrow
\text{servo angle}
\]

That distinction is what makes SPEC-08 a real foundation for Makad's later person tracking rather than just a camera demo.
