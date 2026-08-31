# RP-01 Physics — Torque, Inertia, Resonance

| Field | Value |
|---|---|
| Status | Kinematic inputs and preliminary head-load baseline authored; final torque/inertia work remains blocked on CAD mass properties and candidate axis placements |
| Inputs | `storyboard.md` ranges and kinematic sizing cases; `../../01-system/dimensional-baseline.md`; `material-finish-mass-decision.md`; `payload-mass-capture.md`; CAD m, CoM and inertia tensor; candidate axis placements |
| Method | `docs/intuition.md` §5.1 step 3; worked analogue: the Adam head paper |

## Authored kinematic inputs

`storyboard.md` §4 is authoritative for the profile equations, coefficients and per-motion assignment. Each segment is computed from its authored profile; `k=Cₐ` is no longer treated as a free or global value.

### Current authored cases

| Axis | Requirement | Controlling segment/profile | Current authored value |
|---|---|---|---:|
| Pitch | Peak speed | Yes, 26°/0.220 s, `MJ5` | 222°/s |
| Pitch | Peak acceleration | Laugh, 7°/0.100 s, `MJ5` | 4,041°/s² = 70.5 rad/s² |
| Yaw | Peak speed | No, 44°/0.233 s, `MJ5` | 354°/s |
| Yaw | Peak acceleration | No, 14°/0.131 s `MJ5` settle; all segments within 1% | 4,710°/s² = 82.2 rad/s² |
| Roll | Peak speed | Wobble, 24°/0.267 s, `MJ5` | 169°/s |
| Roll | Peak acceleration | Wobble, 22°/0.255 s, `MJ5`; all segments within 1% | 1,953°/s² = 34.1 rad/s² |

The simultaneous startle values remain pitch 46.7, yaw 24.9 and roll 18.7 rad/s². Startle is a combined-load case, not an individual-axis peak.

### Rapid-expression profile-freedom envelope

RP-01 provisionally permits later rapid-profile changes up to `Cᵥ=2.0`, `Cₐ=2π=6.2832`. This is an explicit engineering envelope, not the claimed coefficient of every smooth profile.

| Axis | Envelope driver | Speed envelope | Acceleration envelope |
|---|---|---:|---:|
| Pitch | Yes 26°/0.220 s; Laugh 7°/0.100 s | 236°/s | 4,398°/s² = 76.8 rad/s² |
| Yaw | Speed 44°/0.233 s; acceleration 14°/0.131 s | 378°/s | 5,126°/s² = 89.5 rad/s² |
| Roll | Speed 24°/0.267 s; acceleration 22°/0.255 s | 180°/s | 2,126°/s² = 37.1 rad/s² |

A future rapid trajectory exceeding either coefficient or shortening an authored segment invalidates actuator sizing. Slow `MS7` motions are evaluated directly despite their higher coefficients because their durations are much longer. Final selection still uses the exported firmware trajectory plus torque, RMS/thermal, gravity and margin calculations.

Current proposed best-case usable travel is pitch `-22°…+40°`, yaw `±55°`, roll `±18°`. Minimum-viable proposed usable travel is pitch `-15°…+32°`, yaw `±40°`, roll `±12°`. These include clearance beyond the authored poses but do not yet include final mechanical hard-stop, cable or forbidden-region margin.

## Preliminary physical load baseline

| Input | Current value | How RP-01 uses it |
|---|---:|---|
| Complete moving-head envelope | **~95 H × 150 W × 115 D mm nominal**, including integrated side pods/pivots; validate within **90–100 H × 145–155 W × 110–120 D mm** | Clearance, fixture, cable, and candidate-axis packaging boundary rebuilt from selected component geometry |
| Neck allocation | **60 mm vertical** | Packaging boundary for yaw + pitch + roll; actuators may intrude into body/head |
| Moving-head mass | **~490 g provisional at 1.2 mm PLA; ~472 g at 1.0 mm walls** | `E` planning build-up from `material-finish-mass-decision.md`; replace row-by-row with `W` evidence |
| Historical system target | **~250 g — obsolete for RP-01 sizing** | Retained only to expose the required system-baseline revision; do not use as representative ballast |
| Preliminary head inertia | **~0.001 kg·m² — invalidated as a sizing input** | Recompute from revised per-axis geometry; mass alone is insufficient |
| Preliminary neck peak torque | **~0.2 N·m — invalidated as a sizing input** | Historical sanity check only, not a per-axis threshold |

The moving load includes the selected no-touch Waveshare ESP32-S3-LCD-4.3 SKU 30493 and selected visible-light Raspberry Pi Camera Module 3 Wide SC0874 at their measured module/installed masses, the finished PLA shell, moving structure, required brackets, interfaces, bearings, actuators/outputs, visible and structural fasteners, and local wiring. It excludes the four body-mounted microphones, body-mounted speaker, battery and primary body electronics. The display's integrated ESP32-S3 is already part of M001/M002; M008 is only a possible second controller.

Before actuator selection, replace the provisional rows with the registered per-axis mass tree and CAD-derived `J_com`, record each component/assembly CoM, apply the parallel-axis theorem for each candidate axis, and calculate dynamic plus gravity torque at the controlling storyboard cases. Register `m_yaw` as everything downstream of yaw, `m_pitch` as everything downstream of pitch, and `m_roll` as the roll cradle and its payload. Include moving actuators, bearing portions, yokes, fasteners, finish and harness segments according to their physical mounting boundaries.

The authored speeds and accelerations in `storyboard.md` remain motion requirements; they are not reduced merely because the head became heavier. What is invalidated is any actuator/load conclusion based on the old mass and inertia. Dynamic torque does not simply double with mass because the revised shell, display, structure and actuators change both `J_com` and axis offsets. Recompute the actual inertia tensor and torque-speed operating points.

PLA is locked for RP-01 structure and skin but remains provisional beyond the prototype. The physics result must include sustained-load creep and thermal exposure at representative parked pitch/roll poses. If M010–M012 are reprinted in PETG or ASA, revise their mass, CoM, stiffness and modal estimates rather than applying a density-only correction.

## Candidate gimbal-centre geometry

Concept A in `concepts/elevated-ear-pivot-serial-gimbal.md` uses body-fixed yaw, pitch pivots near ear-pod height and head-fixed roll. Pitch and roll intersecting, or nearly intersecting, near the measured 3D head CoM is the gravity target to evaluate, subject to a display-clear roll-support and load-path proof. Raising pitch alone while leaving roll below the CoM preserves an inverted-pendulum roll load, so the design variable is the **pitch–roll gimbal centre plus its feasible support layout**, not pitch-axis height in isolation.

For pitch, define `x` as the CoM's forward offset from the pitch axis and `z` as its upward offset. Use

`τ_g,pitch(θ) = m·g·(x·cos θ + z·sin θ)`.

For roll, use the corresponding lateral and vertical offsets about the head-fixed forward axis. Evaluate at least:

| Geometry point | CoM relative to pitch axis | Intent |
|---|---:|---|
| A0 | `x=0 mm`, `z=0 mm` | Ideal gravity null |
| A1 | `x=+5 mm`, `z=0 mm` | Small same-sign pitch preload |
| A2 | `x=+5 mm`, `z=+10 mm` | Packaging compromise with bounded hold load |

These are sensitivity points, not a frozen mechanism specification. The calculation is iterative because the yoke, bearings, actuators and cable loops change the CoM:

`component blockout → initial CoM → axis candidate → mechanism mass → revised CoM → torque/RMS comparison`.

For the `490 g` provisional complete-head sensitivity case, A1 (`x=+5 mm`, `z=0`) gives approximately `0.0240 N·m` at neutral, `0.0223 N·m` at `-22°`, and `0.0184 N·m` at `+40°`. These values scale only the simple gravity term and must not be reported as actuator torque. Final sizing uses the registered downstream mass and inertia for each axis rather than applying the complete-head mass blindly to pitch or roll.

A small persistent load may keep a gearbox on one tooth flank, but preload is a measured mitigation rather than evidence that backlash is gone. Prefer a small fore–aft pitch offset if it retains one torque sign across the usable range. Keep roll close to balance and evaluate a low-rate torsion/elastic bias only if reversal testing warrants it; avoid an arbitrary lateral mass imbalance.

The pitch actuator moves with yaw. Include `m_actuator·r²` for its lateral offset in `J_yaw`. Compare that penalty with the added mass, compliance and reversal loss of any belt/gear relocation before choosing an offset transmission.

Cable restoring torque is part of `τ_friction/τ_bias`, not zero. Measure it versus joint angle for the complete candidate harness and include its worst same-direction and opposing-direction values in slow-motion, hold and unpowered cases.

## Output precision and structural-dynamics inputs

Candidate output-axis requirements, measured at the head under representative load:

- loaded reversal hysteresis at the complete output—gearbox lash, spline/horn and linkage motion, structural compliance plus control behaviour—`≤0.50°` minimum viable, `≤0.25°` target under the registered quasi-static load cycle;
- no visible or instrumented hold hunting: register external-angle and current peak-to-peak/RMS limits and dwell duration before scored testing;
- first loaded yaw/roll structural mode `f₁ ≥25 Hz` as a screening target and `≥30 Hz` as the best-case target;
- first loaded pitch structural mode `f₁ ≥30 Hz` for minimum viable and `≥40 Hz` for the unshaped best-case laugh.

The first value preserves at least 75% of a 2° correction before residual tracking error. Gear material, bus protocol and servo-reported position do not prove it. Use the complete-output, dial-indicator procedure in `storyboard.md` §2.5: at a fixed command, sweep quasi-static output load through `+0.50·τ_peak,op → -0.50·τ_peak,op → +0.50·τ_peak,op`, at a 50 mm measurement radius, with 10 conditioning reversals and 5 measured cycles. Record the independent external angle against matched applied-torque points on both sweep directions; report the maximum branch separation, reversal delay and settled command error. Then dwell at representative holds and log external angle plus current for hunting. This intentionally retains horn/spline fit, joints, printed-part deflection and closed-loop behaviour in the result.

The [XL330 public specification](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/) establishes a 12-bit single-turn absolute position sensor and closed-loop position control, but does not explicitly document the sensor's physical placement. Treat output-side sensing as an inference unless teardown/CAD evidence closes it. In either case the external instrument is necessary: `0.25°` is only about 2.8 counts at the published `0.088°/count` resolution, and servo readback cannot independently validate complete-head motion.

Do **not** divide the `≤0.25°` complete-output target equally among yaw, pitch and roll. A reversal directly traverses the tested axis's transmission; other joint errors and compliance map into face orientation through the mechanism Jacobian and current pose. Test each axis independently while the other two are energized at representative poses, then run an additional combined-motion orientation-error case.

The pitch-specific modal target recognizes the 100 ms laugh reversal's characteristic content around 10 Hz and its meaningful higher-frequency content. A 30–40 Hz pitch result requires validated input shaping or a slower laugh; it is not an unqualified best-case pass. Modal frequency alone does not guarantee 300 ms settling—damping, trajectory spectrum and closed-loop bandwidth also determine ring-down. Estimate in CAD, screen with an impact/tap test under representative mass and confirm during commanded motion.

## Explicit combined-load cases

Use the actual candidate mechanism's axis order and mass properties; do not treat these as separable single-axis tests:

1. **Curious yes, best case:** hold roll at `R+12°` while pitch executes `P-4° → P+12° → P-7° → P+8° → P-4°` over 0.90 s. Evaluate roll static gravity torque at every pitch extremum plus dynamic cross-axis reactions.
2. **Curious no, best case:** hold `R+12° P-4°` while yaw executes `Y0° → YL18° → YR18° → YL12° → Y0°` over 0.95 s. Evaluate roll holding torque, yaw acceleration and bearing/linkage load together.
3. Compare both with the neutral-axis cases to decide whether roll-axis balancing or gravity compensation is required. The worst case depends on gimbal order and axis-to-CoM geometry, so it cannot be declared from Euler angles alone.

## Load-dependent analysis to complete

Per axis, per candidate axis placement, compute:

1. **Load quantities:** m, d (axis→CoM perpendicular distance), J_axis = J_com + m·d², estimated K (structure + horn + spline)
2. **Time-varying torque:** `τ(t) = J_axis·α(t) + τ_gravity(θ,t) + τ_friction + τ_cable + τ_coupling`; preserve sign rather than adding every magnitude blindly
3. **Transient screen:** compare worst-case `τ(t)` at the simultaneous required speed with the actuator's measured torque-speed/current envelope at the intended voltage and temperature. Do not multiply a peak transient by a generic selection factor and compare it with a continuous/rated point; do not treat stall torque at zero speed as the available trajectory torque.
4. **Busy-minute RMS/current screen:** `τ_RMS = sqrt((1/T)·∫τ(t)²dt)` over a preregistered realistic busy minute, with measured `I_RMS`, voltage sag and temperature preferred for acceptance. This precedes actuator freeze and remains separate from the transient screen.
5. **Reflected inertia** J/N² vs. rotor inertia, target <~10× — only where the actuator publishes rotor inertia; otherwise mark UNCOMPUTABLE → moves to the rig, not assumed passed
6. **Resonance estimate** f_n ≈ (1/2π)·√(K/J_eff) — flag anything the storyboard excites near it
7. **Balance/preload option:** compare A0/A1/A2 plus any torsion/counterbalance candidate; an ordinary torsion spring must remain pre-wound with its free angle outside usable travel if same-sign preload is required. Record torque versus angle, added mass, inertia, asymmetric load, unpowered path, hold current and thermal consequence
8. **Combined tilted cases:** evaluate the explicit curious-yes and curious-no trajectories above, including roll holding torque while the other axis accelerates

Cross-axis handling: evaluate each axis at the worst-case configuration of the other two (no full Newton–Euler at this stage).

Every number carries its assumption. A cell without a source is a guess wearing a number's clothes.

## Results

Physical installed-mass evidence is captured in `payload-mass-capture.md`. The per-axis mass tree and CAD-derived CoM/inertia results remain open until that register and the selected mechanism architecture provide the required membership and geometry.
