# RP-01 Gate Registrations

| Field | Value |
|---|---|
| Status | Not started (thresholds come from `intent.md` + `storyboard.md` + `physics.md`; freeze before first scored run) |
| Authority | Gate definitions and registration-record fields: `risk-prototype-plan.md` §RP-01. This file holds the registered numeric versions. |
| Physical baseline | `material-finish-mass-decision.md`; current RP-01 planning load ~490 g at 1.2 mm PLA pending measured per-axis tree and system-baseline revision |

Gates to register (from the plan):

- **RP01-G01 Safety** — bounded state for every injected stop/timeout/feedback-loss/restart case
- **RP01-G02 Three-axis Core** — roll, pitch, yaw each execute registered authored-motion cases under representative load
- **RP01-G03 Motion quality** — range, tracking, repeatability, reversal, overshoot, settling, noise, vibration, cross-axis
- **RP01-G04 Integration** — camera calibratable/usable, wiring survives endurance, safe unpowered state
- **RP01-G05 Buildability** — credible fabrication/assembly/calibration/service/sourcing path with complete cost range
- **RP01-G06 Evidence** — commands, state, current/voltage, faults, video correlatable per run

Each registration uses the plan's required fields: Gate ID, Metric, Threshold, Rationale, Conditions, Repetitions, Instrument, Freeze record (date + builder approval **before** scored data is inspected). Threshold changes after results create a new gate version with a documented reason and fresh test set — never an edit.

## Candidate motion-case matrix — not registered

This matrix prepares coverage from `storyboard.md`; it does **not** freeze a threshold. “Minimum viable” and “best case” remain authored design envelopes until the builder approves a versioned gate registration.

| Case | Storyboard input | Candidate gate coverage | What must eventually be measured |
|---|---|---|---|
| Representative head load and envelope | Complete head ~95 H × 150 W × 115 D mm nominal, validated within 90–100 H × 145–155 W × 110–120 D mm; current `E` build-up ~490 g at 1.2 mm PLA / ~472 g at 1.0 mm; selected Waveshare no-touch SKU 30493 display and visible-light Camera Module 3 Wide SC0874 | G02–G06 | registered per-axis downstream mass tree, as-built/CAD CoM and inertia, axis offsets, ballast revision, selected-display/camera clearance proxies and complete moving interconnect. The old 250 g, `J≈0.001 kg·m²` and `~0.2 N·m` values are not admissible scored-load inputs. |
| Finish-system mass and scale | 60 × 60 mm representative PLA coupon using the complete nine-step finish process | G05, G06 | bare/finished mass after ≥24 h cure, coating g/cm², exact products/passes and visual `PASS/ITERATE` for texture/chip/detail scale before M019a is coated |
| PLA thermal/creep viability | M010–M012 representative structure under worst credible parked pitch/roll load at measured sealed-head temperature | G01, G03–G06 | preregistered dwell duration, load/moment, maximum in-dwell deflection, residual deformation and inspection method; failure selects the recorded PETG/ASA structural fallback rather than being waived |
| CAD access and mass-boundary closure | Full-width opaque rear window mask; display flashing path; yaw-plane demateable connector/cut plane; minimal real service seams | G04–G06 | optical/interior concealment, flash/service demonstration, M020/M900 weighability without cutting, service access and no unowned/double-counted mass rows |
| Depth challenge | Current 110–115 mm core depth versus approximately 90 mm blockout | G03–G05 | display/camera/roll-support/harness clearance, revised shell area/mass, pitch moment arm, service access and stiffness; choose depth before CAD freeze |
| Gimbal-centre and roll-support sensitivity | Concept A A0/A1/A2 axis-to-CoM points plus rear-cartridge, annular/perimeter and displaced-roll-axis layouts from `physics.md`/concept note | G02–G05 | gravity/hold torque over full travel, busy-minute RMS/current/temperature, unpowered direction, display/camera/yoke/ear clearance, bearing reactions/deflection and revised CoM after mechanism mass is added |
| Slow smooth pitch | `HM-02` sleep, 28–35° over 2–3 s | G02, G03, G04 | low-speed smoothness, hold load/noise, final settle, safe rest |
| Fast sharp pitch | `HM-03` wake and `HM-06` yes; Yes critical speed segment 26°/220 ms `MJ5` | G02, G03 | peak current, tracking, overshoot, repeated reversal, ≤1 s phrase feasibility |
| Wide smooth yaw | `HM-04` search, authored ±35° / ±50° | G02–G04 | usable range, cable clearance, camera coverage, sector settle |
| Fast sharp yaw | `HM-07` no, exactly 2 cycles/1.00 s or 2 cycles/0.95 s; stitched `MJ5` reversals | G02, G03 | launch, every reversal and settle; peak acceleration/current, loaded reversal hysteresis, hunting/ringing and final settle |
| Small correction and loaded hold | `HM-05` tracking, authored 4° / 2–4°, plus fixed-command load sweeps and hold dwells | G03, G04 | smallest repeatable move; external-angle versus applied-torque hysteresis at `±0.50·τ_peak,op`, candidate maximum branch separation ≤0.50° / ≤0.25°; reversal delay, settled error, external-angle/current hunting, chatter and camera disturbance |
| Combined orientation reversal | Coordinated yaw/pitch/roll reversal at representative neutral and tilted poses | G03, G04 | complete face-orientation error; per-axis contributions mapped at the tested pose rather than assuming an equal one-third lash allocation |
| Pitch micro-pulse | `HM-08` laugh, 2 pulses/0.80 s or 3 pulses in 0.68 s active window; `MJ5` pulse train | G03 | 7°/100 ms local reversal, candidate loaded-hysteresis budget, unintended vibration/noise |
| Medium-fast roll | `HM-09` wobble, authored ±8° / ±12°; stitched `MJ5` reversals | G02, G03 | current roll peak speed/acceleration, rounded reversal, cross-axis disturbance and settle |
| Curious yes combined load | `HM-11A`: hold `R+8°/+12°`; pitch uses the explicit storyboard extrema | G02–G04 | roll static gravity/holding torque during dynamic pitch, coupling, clearance and camera usability |
| Curious no combined load | `HM-11B`: hold `R+8°/+12°` and `P-2°/-4°`; yaw to ±13° / ±18° | G02–G04 | roll holding torque during dynamic yaw, coupling, clearance and camera usability |
| Multi-axis recoil | `HM-15` startle; 250/180 ms outbound only | G01–G04 | simultaneous three-axis load, freeze/ringing, separate slower recovery and interruption; not an individual-axis peak |
| Loaded pitch structural dynamics | Best laugh's 7°/100 ms reversal under representative mass | G03, G04 | candidate first loaded pitch mode ≥30 Hz minimum / ≥40 Hz unshaped best case, plus damping and commanded ring-down; otherwise validate shaping/slower motion |
| Loaded yaw/roll structural dynamics | Fast no and wobble under representative mass | G03, G04 | candidate first loaded mode ≥25 Hz / ≥30 Hz plus measured damping and commanded ring-down |
| Harness restoring load and live-signal endurance | Complete H1/H2/H3 candidate head harness through yaw/pitch/roll workspace, with the selected camera streaming and representative concurrent electrical load | G03–G06 | angle-dependent restoring torque, slow-motion distortion, clamp/connector motion, actual installed radii/torsion, strain relief, frame gaps/drops, capture/driver errors, visible corruption, reset/re-enumeration, milestone inspection and unpowered pull. Route must approach each joint near its axis; candidate milestone counts and the exact definition of one cycle must be frozen before scored use. |
| Busy-minute actuator duty | Preregistered realistic busiest one-minute sequence assembled from the storyboard | G02–G06 | transient torque/current at required speed kept separate from RMS/current/thermal acceptance; voltage sag and all actuator temperatures logged before selection |
| Head/body IMU role separation | Head IMU on moving output; body IMU or body-attitude proxy recorded where chassis disturbance is in scope | G03, G04, G06 | head settling/compliance/modal data is not misreported as body heading; joint/body/head timestamps are correlatable |
| Profile-law conformance | Every scored motion segment | G03, G06 | logged/exported trajectory identifies profile code and version; measured `ω/α/jerk` remain within the registered authored case and `Cᵥ≤2.0`, `Cₐ≤2π` rapid-profile envelope |
| Controlled cancel | `HM-18` from every motion class | G01, G03 | command acceptance, deceleration, stale-keyframe rejection, bounded hold |
| Unpowered/fault rest | `HM-00` plus power/controller/feedback fault cases | G01, G04 | measured passive motion/backdrive, supported rest versus bounded forward sleep-like settle, hard-stop/cable behavior and restart policy; gearbox ratio alone is not evidence |

Best-case failure alone cannot fail V1 if the later-approved minimum-viable three-axis case passes and remains perceptually coherent. Conversely, a minimum-viable label here is not permission to declare a pass without preregistered thresholds and scored evidence.

## Registered gates

*(none yet)*
