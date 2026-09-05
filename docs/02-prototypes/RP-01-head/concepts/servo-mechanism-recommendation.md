# RP-01 servo mechanism recommendation

Research date: 2026-09-05. Status: **recommended architecture for the next blockout and prototype; not a selected mechanism, registered gate, packaging proof, or actuator selection.**

Revision 0.2, 2026-09-05: resolves bearing-cover ownership, makes per-axis mass membership explicit, and specifies the remaining interface, harness and dynamic-analysis work. All load calculations here remain illustrative; no calculated or measured per-axis assembly load has been established.

Build a **bearing-supported serial yaw → pitch → roll gimbal**, with elevated pitch pivots near the head's centre of mass, a rear-supported roll spindle, and each actuator housing attached to the frame immediately upstream of its joint. This develops Concept A into a more specific build proposal. The proposed blockout uses short direct 1:1 drives on all three axes and non-rolling ear covers attached to the yaw yoke. Offset transmissions remain conditional comparison options, not automatic packaging fixes.

The decision optimizes for Makad's small reversible expressions, fast pitch/yaw strokes, quiet holds, three powered axes, serviceable printed construction and current packaging. It is an engineering recommendation from the available evidence, not proof of a global optimum. A parallel pitch/roll alternative is specified below so the recommendation can be challenged fairly.

The current [decision register](../decision.md#candidate-register) still marks the mechanism open, requires a comparison concept and leaves direct/belt drive unresolved. This recommendation does not claim an existing direct-only lock or select an alternative on the builder's behalf.

## Requirements extracted from the project

Sources: [storyboard](../storyboard.md), [intent](../intent.md), [physics](../physics.md), [dimensional baseline](../../../01-system/dimensional-baseline.md), [mass decision](../material-finish-mass-decision.md), [mass capture](../payload-mass-capture.md) and [harness study](../../../01-system/head-harness-routing-study.md). The storyboard's numbers remain provisional authored targets, not accepted bench performance.

### Size and mass

| Input | Current evidence |
|---|---|
| Complete head | Nominal **95 H × 150 W × 115 D mm**; validation band 90–100 H × 145–155 W × 110–120 D mm |
| Head core | 95 H × 125–130 W × 110–115 D mm |
| Neck | **60 mm vertical allocation**, approximately 35–45 mm externally visible; intrusion into head/body permitted |
| Selected display | Module approximately **106.1 × 67.8 mm**; thickness, connectors and service space must be established from the sample |
| Complete moving assembly | Approximately **490 g + M008** at 1.2 mm PLA; M008 is the required separate C2 motion-controller assembly |
| Thinner-shell scenario | Approximately 472 g + M008 at 1.0 mm PLA; not a structural recommendation |
| Accepted measured mass | **Unknown.** M900 and the component measurements are blank |

The 490 g model already includes 133 g installed display, 15 g window/mask, 23 g camera/interconnect/light, 80 g cradle/yoke/yaw interface, 35 g provisional actuator moving hardware, 22 g bearing portions, 148 g finished shell, 15 g harness and 19 g fasteners. Rounded rows total about 490 g. It is not 490 g of bare payload to which the entire mechanism should be added again.

However, **the 35 g actuator allowance is not evidence that the moving pitch and roll servo housings will fit that mass**. In this proposed layout their full housings move downstream of yaw and must be counted. Replace that allowance and every other provisional row with actual boundary-owned masses. The final result can exceed 490 g + M008 substantially. Neither a 550 g nor a 650 g finished head can currently be promised.

The old 250 g target, 0.001 kg·m² inertia proxy and 0.2 N·m neck-torque estimate must not be used for selection. This study does not replace them with another guessed sizing inertia.

### Per-axis mass membership for this proposed construction

**M900 is the complete assembly downstream of yaw. It is not the pitch or roll payload.** Inventory ownership and joint membership are different: one item is weighed once but may contribute to several nested downstream mass sets. The following table describes this recommendation, not a frozen production layout.

| Physical item / inventory owner | Yaw set | Pitch set | Roll set |
|---|:---:|:---:|:---:|
| Display/renderer, window, camera, light: M002/M003/M005/M007 | Yes | Yes | Yes |
| C2 motion controller and its mount: **M008**, proposed on rolling cradle | Yes | Yes | Yes |
| Roll cradle/backplate/ribs: M010; spindle is assigned to M013 below | Yes | Yes | Yes |
| Rolling shell portion of M019c and its attached fasteners | Yes | Yes | Yes |
| Roll output horn/coupling/spindle: assigned M013 subitems | Yes | Yes | Yes |
| Roll servo housing/mount: M013; rear cartridge housing: tilting M011 subitem; non-rolling bearing portions: M016 | Yes | Yes | No |
| Tilting pitch frame: M011 subitem; pitch output trunnions: M014 subitems | Yes | Yes | No |
| Pitch servo housing/mount: M014; yaw U-yoke and pitch-bearing housings: yaw-only M011 subitems | Yes | No | No |
| **Ear covers attached to the yaw yoke**: M019c subitems, separated from rolling shell ownership | Yes | No | No |
| Yaw moving interface, shaft/output hardware: M012/M015 and moving M018 portions | Yes | No | No |
| Body-fixed yaw servo housing and yaw bearing housing | No | No | No |
| Bearing rings, cable segments, guides, connectors and fasteners | Assign each subitem by its attachment and flex boundary; do not apply one membership flag to the entire kit | By subitem | By subitem |

Split M011 into named yaw-yoke and tilting-frame subitems and M019c into rolling-shell and non-rolling-cover subitems when constructing the CAD mass tree. Preserve each parent total; do not add the subitems again. Likewise, M013 owns the roll actuator hardware downstream of yaw even though its housing does not roll. A row named after an actuator axis is not permission to omit its housing from the upstream axes that carry it.

In compact form, `m_pitch = m_roll + pitch-carried non-rolling hardware`, and `m_yaw = m_pitch + yaw-carried non-pitching hardware`, with cable and bearing parts apportioned consistently. All three final values remain **TBD**. Replace the 35 g actuator allowance and the existing structural/bearing allowances with their actual totals; do not add a new 80–120 g mechanism package on top of the unadjusted 490 g ledger. Published or weighed servo mass alone cannot establish the complete installed set.

This table concerns bodies and payload carried by each joint. Motor rotors and internal gears also contribute drive inertia about their driven axes; include those separately when data or identification permits, without counting their physical mass twice in M900.

**C2 and M008 identify the same separate motion-controller assembly.** The display's integrated ESP32-S3 is already included in M002. This proposal has two head boards, not an additional controller beyond M008. Putting M008 on the rolling cradle is the recommendation's explicit placement assumption; moving it to a yaw-only support changes its pitch/roll membership and the harness branch map and must be recorded before calculating loads. It remains in M900 if it stays downstream of yaw.

### Movement and timing

Pitch positive means down; negative means up. All speeds below are **head-output** values.

| Behaviour | Authored motion / timing | Mechanical consequence |
|---|---|---|
| Attentive / powered-off | Deliberate stillness; off-state is passively supported or follows a bounded safe path | Low hunting and low static effort; power-off support cannot rely on a position command |
| Sleep / wake | Down 28–35° over 2.4–3 s; wake within 0.85–1 s | Sustainable down pose and shaped rise |
| Search | Yaw ±35–50° with 200 ms inspections; phrase 2.5–2.7 s | Wide, repeatable yaw and controlled cable travel |
| Acquire / track | Acquisition 300–700 ms; intentional corrections 2–4° over 180–500 ms across the two target tiers | Small reversals must survive gearbox, coupling and frame hysteresis |
| Yes | Two pitch cycles: minimum +14/−6° in 1 s; best first extrema +18/−8°, declining over 0.90 s | Pitch speed and repeated reversals |
| No | Two yaw cycles: minimum ±16° in 1 s; best first extrema ±22°, declining over 0.95 s | Highest output speed and acceleration |
| Laugh | Minimum two groups over 0.80 s; best three unequal forward pulses in 0.68 s plus 0.17 s hold | **7° reversal in 100 ms** controls pitch acceleration and exposes lost motion |
| Indian wobble | Roll ±8° minimum / first extrema ±12° best; declining two-cycle phrase over 1.15 / 1.08 s | Powered roll must reverse smoothly; not merely hold a tilt |
| Curious / affection | Roll roughly 8–12° with small pitch lift; 0.6–2 s holds depending on phrase | Roll balance, quiet holding and off-neutral cable torque |
| Curious yes / no | Hold roll 8–12° while executing pitch/yaw phrases | Combined-pose clearance and cross-axis load/control |
| Happy / anger / sadness / confusion | Asymmetric multi-axis poses; short accents through slow 1.8–2.2 s droops and long holds | Stiffness plus smooth low-speed motion, rather than continuous oscillation |
| Startle | Three-axis outbound stroke in 180–250 ms, then hold and slower recovery | Concurrent load and current case |
| Cancel | Proposed stop/settle within 300–500 ms where physically safe | Stop from current velocity/acceleration; no queued stale gesture |

### Travel and dynamic envelope

| Axis | Minimum usable travel | Best-case usable travel | Current peak speed | Current peak acceleration | Rapid-profile sizing envelope: speed / acceleration |
|---|---:|---:|---:|---:|---:|
| Pitch | −15…+32° | **−22…+40°** | 222°/s | 70.5 rad/s² | **236°/s / 76.8 rad/s²** |
| Yaw | ±40° | **±55°** | 354°/s | 82.2 rad/s² | **378°/s / 89.5 rad/s²** |
| Roll | ±12° | **±18°** | 169°/s | 34.1 rad/s² | **180°/s / 37.1 rad/s²** |

Usable travel includes margin beyond authored poses, but hard stops and cable limits need additional, separately established stopping margin. Separate axis limits do not prove that every corner of their Cartesian product is available.

The current MJ5 peaks were independently recalculated using `ω_peak=1.875·Δθ/T` and `α_peak=5.7735·Δθ/T²`. The wider rapid-profile envelope uses coefficients 2 and 2π. Speed and acceleration maxima need not occur simultaneously; use full trajectories when calculating torque-speed demand.

### How frequent?

There are three different quantities:

1. **Within-gesture cadence:** best Yes averages 2/0.90 ≈ **2.22 cycles/s**; No 2/0.95 ≈ **2.11 cycles/s**; Wobble 2/1.08 ≈ **1.85 cycles/s**. These are averages over declining, nonstationary phrases. Laugh has three pulses in 0.68 s, about **4.4 pulses/s during its active window**; its 100 ms local reversal is not a sustained 10 Hz oscillation.
2. **Which axes dominate:** the storyboard expects pitch and yaw together to account for **80–90% of authored head activity**. This is not an 80–90% motor duty factor. Roll still holds load during compound expressions.
3. **Occurrences per minute / lifetime:** **not specified yet**. The system requires at least 20 minutes of representative mixed-duty battery operation; that does not define gestures per minute or establish thermal equilibrium.

Proposed design-validation schedule, not an approved interaction policy: make a 60 s script with 5 s slots for wake/track, two Yes phrases, two No phrases, two Laugh phrases, search/track, two Wobbles, curious Yes/No, tracking, Yes/No/startle, and sleep; use the final 10 s for an off-neutral static hold. All approach/return blends must fit and be included in the export. Record actual moving time and holds from that export, repeat under the representative load, and separately test sustained holds until the thermal trend is understood. Final endurance cycles must come from expected use and intended life, not an arbitrary universal cycle count.

## Exact actuator placement and structure

```text
BODY / FIXED FRAME
  yaw servo housing — 1:1 drive — independently supported yaw stage
                                   │
                            rising yaw U-yoke
                      [pitch servo housing on yoke]
                                   │
                    left + right pitch trunnion bearings
                                   │
                            tilting pitch frame
                       [roll servo housing on frame]
                                   │
                      rear roll bearing cartridge
                                   │
                         rolling payload cradle
                    display + camera + rolling shell + M008
```

The servos provide torque. The bearing/frame chain supports weight, bending and side loads. Structural supports must remain functional with an actuator removed during an unpowered service operation.

| Servo | Housing attaches to | Output direction at neutral | Placement and drive | Housing moves with |
|---|---|---|---|---|
| Yaw | Body chassis | Vertical | Below the yaw bearing cartridge, recessed into torso; short 1:1 coaxial coupling first | Nothing |
| Pitch | Rotating yaw U-yoke | Left–right | Adjacent to one supported pitch trunnion, housing tucked inward into the side/rear mechanism pocket; short 1:1 coupling | Yaw only |
| Roll | Tilting pitch frame | Front–back | Behind display, near the centreline; coaxial drive into a separate rear-supported spindle first | Yaw and pitch |

**Yaw:** use a compact spaced-bearing spindle or appropriately rated combined-load bearing arrangement. Axial retention/shoulders carry the head's weight; bearing spacing carries overturning moment. A servo horn sitting under the whole head is not this arrangement. First block out a direct coaxial drive with a controlled cable passage beside the shaft or through a hollow spindle. A hollow spindle also needs a cable exit that clears the solid servo output, coupling, bearings and retainers; the bore alone is not a complete route. If neither direct-drive route fits, document that failure before comparing an offset drive. A short 1:1 timing belt would add tension-dependent compliance, pulley interfaces and bearing loads directly to the fast yaw path and must clear the complete-output tests before being adopted.

**Pitch:** raise two pivots toward the *pitch assembly's* measured CoM. One servo drives one side; the other side is a passive bearing. Join the two through a rigid pitch frame. Two servos rigidly fighting over the same shaft add synchronization, heat and backlash issues without creating another useful degree of freedom. The inward servo pocket and complete roll sweep must be shown in section before accepting this placement. If the direct pocket fails, quantify that failure before comparing an offset drive within the yaw frame; do not silently grow the ears.

**Ear-cover choice for this proposal:** attach both cosmetic pods/covers to the **yaw yoke's pitch-bearing housings**. They yaw with the neck, but do not pitch or roll with the face. The trunnions rotate inside the supported pivots while the covers remain centred on their housings. The 8–12 mm side allowance is for these covers and bearing access, not an entire unspecified servo.

A cover attached to the rolling shell at a 75 mm lateral radius would move approximately **23.2 mm vertically and 3.7 mm inward at 18° roll** relative to the non-rolling support. That arrangement cannot be described as a cover remaining centred on the bearing. The selected proposal therefore uses fixed-to-yoke covers rather than shell-mounted covers travelling around slotted trunnion apertures. The rolling shell still needs a proven clearance relief around the stationary support; concealing that relief under a cover is a packaging goal, not an established invisible seam. Check pitch and compound poses as well as roll, and include the covers only in the yaw mass set.

**Roll:** keep its axis near the *rolling payload's* CoM. A rear bearing cartridge carries a short metal spindle connected to a rigid payload backplate/spider, which supports the front display and shell through ribs. The roll servo housing stays on the pitch frame; it does not roll with its own payload. The roll axis is an imaginary line through the head; **no physical shaft needs to pass through the display**.

Start the rear-cartridge blockout with two radially supporting bearings separated by **20–25 mm**, plus explicit axial location. This is a geometry trial, not a selected bearing specification. A common accurately aligned cartridge avoids relying on two independently aligned printed housings; its bearing seats still require fit verification. Place a removable roll drive coupling behind it. If the coaxial servo makes the assembly too deep, record the failed section and compare support/drive alternatives before adopting an offset drive. Keep the drive, bearings, shaft and payload backplate distinct in the drawing.

Two rear bearings **do not remove the overhung load**. For illustration only, a 0.40 kg rolling assembly with its CoM 35 mm ahead of the support reference produces about `0.40·9.81·0.035 = 0.137 N·m` of static bending moment. A 20–25 mm bearing separation resolves that into a moment-couple contribution of about 6.9–5.5 N, in addition to direct weight reactions. Acceleration, belt forces, retention and frame deflection must also be calculated. This example is not a final load rating or the actual rolling mass.

Use genuine metal servo horns/clamping hubs and supported metal shafts. Keep removal and calibration access outside cosmetic shell dependencies. Prototype PLA remains the project's material assumption; actuator heat, insert retention and sustained-load creep still need evidence.

### Drive interfaces and output error budget

The proposed roll torque path is **servo spline → matched metal horn/hub → removable coupling → supported spindle → piloted/clamped payload flange → rigid cradle**. The load path returns from the cradle through the spindle bearings and cartridge into the pitch frame. The spline retaining screw must not substitute for a fitted torque interface, and a loose shaft in a printed hole is not an acceptable spindle-to-cradle connection.

| Interface | Blockout/construction requirement | Evidence still required |
|---|---|---|
| Servo spline to horn/hub | Genuine matching spline; specified retention and accessible fastening | Reversal play and retained clamp/fastener state |
| Horn/hub to supported shaft | Short coupling with defined alignment accommodation and a positive or clamped torque interface; shaft bearings carry structural loads | Torsional stiffness, lost motion and absence of binding through travel |
| Roll spindle to payload cradle | Piloted flange or split-clamp hub rigidly fastened to a load-spreading backplate; explicitly draw spindle/flange retention | Relative angular movement under reversing torque; creep/slip after dwell |
| Pitch trunnions and yaw output flange | Defined shaft/hub fits, axial retention and bearing-seat alignment | Clearance, support deflection and repeatable reassembly |
| Frame joints and bearing cartridges | Load carried through fitted structural interfaces and retained fasteners rather than cosmetic covers | Loaded hysteresis, reversible deflection, modal response and thermal/creep behaviour |

| Test axis | Complete path covered by its head-output test | Minimum / best-case loaded hysteresis |
|---|---|---|
| Yaw | Yaw actuator, drive/output interfaces, supports and downstream frame response with pitch/roll held | ≤0.50° / ≤0.25° |
| Pitch | Pitch actuator, trunnion/frame interfaces and downstream roll support/cradle response with yaw/roll held | ≤0.50° / ≤0.25° |
| Roll | Roll actuator, coupling, spindle, flange/cradle and support response with yaw/pitch held | ≤0.50° / ≤0.25° |

These are the existing per-axis complete-output targets, not three additive shares of a 0.25° total and not passed tests. The interface allocation remains **open** until component response is known: assign bounded actuator, coupling, fit/fastener and structural hysteresis contributions within each axis's target, with an explicit integration reserve. Do not invent equal interface allowances or subtract elastic endpoint deflection as though it were measured hysteresis. Independently instrument accessible interfaces to diagnose contributions, then accept/reject at the head output using the [draft measurement method](../storyboard.md#25-candidate-loaded-hysteresis-and-hold-hunting-test).

For compound orientation, map small joint errors through the actual angular Jacobian, `δφ ≈ Jω(q)·δq`, and include structural rotations at their own locations. The separate per-axis tests do not prove a 0.25° bound on the norm of combined face-orientation error. Register that combined-case criterion separately. Dynamic reversal delay, settling and hold hunting also remain separate from the quasi-static hysteresis result.

### Harness branches and conduit section

| Branch | Proposed moving path | What crosses a joint? |
|---|---|---|
| LCD panel to its integrated display renderer | Both mounted on the rolling payload | The internal display FPC stays local; it does **not** need to traverse roll/pitch/yaw |
| Camera CSI to body Linux SBC | Rolling camera → controlled roll loop → pitch-frame anchor → pitch loop → yaw-yoke anchor → yaw loop → body | Camera-compatible interconnect across all three joints |
| Display and M008 power/semantic communications | Body → yaw → pitch → roll → rolling boards | Power and low-bandwidth links, not the display's raw panel FPC |
| M008 servo bus/power distribution | Rolling M008 → roll-frame servo branch; continue across pitch to yaw-carried pitch servo, then across yaw to body-fixed yaw servo as required by the actual distribution | Document branch terminations and conductors once; do not assume every servo lead traverses every joint |
| Status LED/local wiring | Retained on rolling payload | Local unless the chosen electrical connection requires otherwise |

The conduit-section drawing must freeze **M008's mounting frame**, exact conductor/connector envelopes, service-loop lengths, installed bend radii, clamp locations and roll-cartridge/yaw-coupling exits together. With M008 on the cradle, its outgoing servo branch crosses roll even though the roll servo housing does not. Moving M008 upstream changes that branch geometry and mass membership. M008 placement does not remove the camera's three-axis route while camera and SBC remain on opposite sides of those joints.

Give each joint a mechanically controlled flex zone and strain-relieved endpoints; use a continuous camera interconnect unless an added connection is justified by signal evidence. A separable yaw-plane service boundary must also satisfy the mass-capture convention. The finished conduit and live-camera flex performance remain unproved; a schematic wire drawn through an axis is not clearance or endurance evidence.

## Why this layout is the best first build

**Balance before reduction.** Gremsy's balancing procedure treats fore–aft and vertical tilt balance separately, then roll and pan balance. That supports a genuinely three-dimensional CoM adjustment rather than simply lifting a neck pivot. For Makad, adjust the rolling payload first, then balance the complete pitch output, then position that assembly over yaw. ([Gremsy balancing guide](https://docs.gremsy.com/gimbals/pixy-lr-sp/getting-started/gimbal-balance))

An illustrative 0.60 kg assembly with its CoM 50 mm directly above pitch adds **0.169 N·m gravity torque at 35°** and **0.0015 kg·m²** from the offset alone. At 76.8 rad/s² that offset contributes another **0.115 N·m inertial torque**. These are separate terms, not a claim that their maxima coincide. A 5 mm forward offset with zero vertical offset gives only **0.029 N·m at neutral**. This is why moving the pivot toward CoM is more valuable than beginning with a large reduction under the head. Real values require each downstream mass set.

Balancing removes the relevant gravity lever arm and reduces the parallel-axis term `m·d²`; **intrinsic `I_cm` remains**. Yaw is a leading candidate for the binding torque-speed requirement because it carries the largest set and has the highest speed/acceleration envelope. Pitch remains the critical small-reversal/modal case. Neither statement selects a servo or proves feasibility: calculate `τ_i(t)` and `ω_i(t)` together from the actual per-axis mass properties, gravity, cable/friction and coupling terms. Do not pair independent peak acceleration and peak velocity as though they occur at the same instant.

**Preserve the fast pitch path.** Pitch is responsible for small laugh reversals and vigorous nods. A short direct coupling removes the additional joints and elastic spans that a remote linkage would introduce. This reduces sources of error; it does not certify the servo's gearbox. The current output hysteresis goals remain ≤0.50° minimum and ≤0.25° best case, measured at the head.

**Keep heavy housings upstream.** Yaw carries both moving servo housings, pitch carries the roll housing, and roll carries neither housing. Do not place all three housings on the head. Also avoid unnecessary lateral offset: moving an illustrative 60 g pitch servo from 70 mm to 25 mm yaw radius reduces the point-mass inertia term by 0.0002565 kg·m², worth about 0.023 N·m at the yaw acceleration envelope. A belt may or may not be worth that saving after its own mass, tension and compliance are included.

**Retain speed.** At a 2:1 reduction the drive must turn approximately 756°/s for the 378°/s yaw output envelope, before load-related speed loss. Begin with 1:1 architecture and sufficient motor-side travel; earn any reduction through the complete torque-speed calculation. This is not a servo selection.

**Treat belts as engineered transmissions.** Gates explicitly makes installation tension, shaft load and pulley/belt geometry part of drive design. A short belt can relocate a housing and open a cable passage, but “timing belt” does not mean zero compliance or automatic precision. Do not transfer industrial belt dimensions or tension numbers directly to this small mechanism. ([Gates drive design tools](https://www.gates.com/DesignPower.html), [Gates design manual](https://www.gates.com/content/dam/documents-library/catalogs/poly-chain-gt-carbon-drive-design-manual-en.pdf))

**Keep backlash mitigation honest.** Begin near balance, with adjustable small offsets. Add light preload only if output tests show a benefit. It will not eliminate dynamic flank changes if inertial/cable torque reverses the total load. Do not introduce a large constant spring load merely to hide unloaded buzz.

## Credible alternatives and why they are not first choice

| Architecture | Concrete arrangement | Benefit | Cost for Makad | Recommendation |
|---|---|---|---|---|
| Proposed serial yaw → pitch → roll | Body yaw; supported ear-height pitch; rear roll cartridge | Simple independent axes, short fast-pitch path, straightforward service and calibration | Moving pitch/roll housings; tight side pocket and rear roll support | **First blockout and RP-01 build** |
| Yaw + parallel pitch/roll | Body-fixed yaw rotates a platform carrying two tilt servos, a central mast and a near-CoM universal joint; two short rigid pushrods attach fore/aft-offset and left/right-offset on the output | Both tilt housings remain upstream of both tilt axes; compact external neck; load sharing | Two rod paths and joints, nonlinear leverage, shared actuator limits, extra calibration and potential reversal error | **Strongest comparison concept** if serial packaging fails |
| Yaw → roll → pitch | Rear roll support rotates a U-yoke with inner double-supported pitch and pitch servo | Familiar gimbal topology; pitch occurs in the rolled local frame | Roll must accelerate the pitch yoke and servo; different gravity/clearance map | Compare if it resolves a real assembly conflict |
| Three-actuator spherical parallel neck | Three coupled drives orient one output about a common centre | Compact rotational centre and upstream motors possible | Precision transmission, nonlinear kinematics/workspace and fabrication burden | Useful reference, not the first custom build |
| Low three-servo stack / flexible tendon neck | Pitch/roll axes below the head or compliant neck spine | Easy initial assembly or deliberate compliance | Gravity/inertia penalty, moving stacks or elastic modes oppose fast clean reversals | Poor match to current small-expression requirements |

The parallel comparison is a real three-DOF concept: use a **two-DOF universal joint**, rather than a free ball joint leaving uncontrolled relative yaw, atop the yaw-carried mast. Tilt rods have articulating ends and output anchors with both fore–aft and lateral separation, so their vertical-force components can generate pitch and roll moments. Equal rod movements predominantly pitch; opposite movements predominantly roll near neutral. With rotary servos, exact crank/rod geometry determines the mapping. Do not apply a linear sum/difference law throughout −22…+40° pitch or declare the full combined workspace clear without checking transmission angles, rod interference and joint articulation. It is also not “all motors body-fixed”: both tilt housings still yaw in this version.

Engineered Arts documents a central intersecting-axis neck with two parallel linear actuators for pitch/roll and a separate rotary yaw actuator. Its series elasticity, encoders and nested force/position control are important differences; copying the layout alone does not copy its performance. ([Engineered Arts](https://wiki.engineeredarts.co.uk/Compliant_neck))

The Twente neck research explicitly uses a differential lower pair to reduce moving mass, minimize backlash and add gravity compensation. It establishes the value of that tradeoff, not that a custom differential beats a short serial transmission in Makad's envelope. ([Brouwer et al., ICRA 2009](https://doi.org/10.1109/ROBOT.2009.5152585))

The documented **Reachy 2023** Orbita has a 70 mm diameter, 170 mm height and 850 g mass and uses machined aluminium, SLS parts, custom steel gears, bearings and shafts. These are generation-specific figures: that implementation is not a drop-in fit for Makad's 60 mm neck allocation, although the spherical topology remains legitimate. ([Pollen Robotics specifications](https://pollen-robotics.github.io/reachy-2023-docs/advanced/specifications/orbita-specs/))

Adam is a useful caution when counting motors: it uses three neck servos but only **two neck DOFs**, with two synchronized pitch linkage drives and one yaw drive. Its 1.05 kg head, 70 mm CoM offset and 1 Hz simulated nod are unlike Makad's current load and fast small gestures. Its torque results cannot be adopted here, and its architecture would still need powered roll. ([Said et al., 2024](https://doi.org/10.3390/asi7030042))

## Packaging and motion checks that can change the recommendation

1. **Prove the rear roll section.** Place actual display thickness/connectors, camera, front carrier, rolling backplate, spindle, bearings, coupling and servo envelope inside the head depth. Record the CoM-to-bearing overhang and structural deflection at the display. If rear support fails, compare perimeter support or the parallel concept; do not silently lower roll far below CoM.
2. **Prove the pitch pocket and rolling-shell sweep.** A 130 × 95 mm rectangular cross-section rolls to roughly **153 mm projected width at 18°**, even before stationary supports. This is a conservative rectangular silhouette calculation, not a demonstrated collision of the final shaped head. Side pods/pivots cannot simply be added outside it. The neutral head dimension and its moving swept volume must be distinguished. Check yoke arms, shell cutaways, ear covers, connectors and fasteners through compound poses, not just individual sweeps.
3. **Balance the correct downstream sets.** Pitch and roll do not have exactly the same CoM because the pitch output includes the roll housing and support. Aim for nearby axis intersections while balancing each assembly; add adjustable mounts or exchangeable spacers before final hole positions. Recalculate the whole-robot CoM after the heavier head is known.
4. **Preserve the intended coordinate semantics.** In a yaw → pitch → roll chain, holding the roll joint while moving pitch is not automatically a nod about the already-rolled head's local left–right axis. Use rotation matrices/quaternions and the actual forward/inverse kinematics to implement the storyboard's chosen robot-relative or head-local meaning. Recheck actuator peaks if that remapping introduces coupled joint movement.
5. **Design the harness with the mechanism.** Use the branch and conduit-section requirements above, with M008's mounting frame explicit. One mechanically controlled flex zone per axis; yaw near-axis loop, pitch loop near a pivot, controlled roll loop at the rear. Keep camera CSI separate from power/bus strain relief; avoid unnecessary CSI connectors. Bounded ±55° yaw does not require a slip ring. Apply the current mass baseline to all moving harness hardware.
6. **Validate output quality under the actual load.** Registered external-output hysteresis/hold tests; representative cable-torque measurements; pitch modal screening ≥30 Hz minimum / ≥40 Hz for unshaped best-case laugh and yaw/roll ≥25/30 Hz; real gesture settling and combined-pose checks. Modal targets are project hypotheses, not guaranteed settling bandwidth. Follow with busy-minute current/temperature, sustained holds, and unpowered support/stop checks. No powered tests were performed for this recommendation.

The actionable next artifact is a **sectioned mass-and-envelope blockout of this serial layout and the parallel comparison**, using actual component envelopes while keeping actuator choices open. If both fit, the serial architecture is preferred for its short pitch drive and simpler reversal behaviour. If the serial design needs a large roll ring, enlarged ear pods or excessive rear depth, re-evaluate the parallel layout from the same mass, stiffness, cable and gesture criteria before selecting hardware.

## Research method and limits

Exa searches were run through agent-reach/mcporter for robot-head gimbals, balancing, spherical/differential mechanisms, Adam, and timing-belt engineering. Only original papers and manufacturer/project documentation support the engineering conclusions above. Exa supplied indexed primary-source excerpts; direct web opens additionally verified the Gremsy balance and Reachy 2023 specification pages. Some direct publisher/wiki opens were unavailable, so those entries rely on the primary-source excerpts rather than claimed full-text inspection. Source designs demonstrate mechanisms and design practices, not Makad-specific performance. All new numerical examples are explicitly illustrative and independently calculated; no FEA, CAD interference proof, servo testing or procurement was performed.

**Calculation status:** the 0.40 kg rear-support example and 0.60 kg pivot-offset example use stated hypothetical loads. They neither apply 490 g to every joint nor constitute final calculations for the actual downstream sets. `m_roll`, `m_pitch`, `m_yaw`, their CoMs/inertia tensors, bearing reactions and trajectory-dependent torque-speed demands must all be produced from the component table before any load capability is claimed. The authored kinematic peaks and illustrative geometry/load arithmetic have been checked; assembly-level dynamics remain open.
