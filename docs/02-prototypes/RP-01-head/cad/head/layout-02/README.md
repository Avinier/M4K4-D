# Head Layout 02 — slimmer octagonal head

2026-09-08. Implements the builder-approved [exterior brief](../layout-02-brief.md). This is a **1:1 parametric layout and assembly fit study**, not a fabrication release or servo selection. Layout 01 is preserved unchanged by this revision.

## Review the CAD

- [Interactive complete head](http://127.0.0.1:3245/Users/avinier/robotics/makad/docs/02-prototypes/RP-01-head/cad?file=head%2Flayout-02%2Fhead-layout.step.py): roll, pitch and yaw controls, plus **Show shell and ear caps**. The complete front, side, rear and ear enclosure parts are rendered translucent in the viewer so the internal arrangement can be inspected through the whole head while the enclosure remains visible. Viewer controls change the displayed pose only; exported STEP is neutral. Pitch follows the storyboard convention: positive is chin down, negative is chin up.
- [Internal arrangement](http://127.0.0.1:3245/Users/avinier/robotics/makad/docs/02-prototypes/RP-01-head/cad?file=head%2Flayout-02%2Fhead-internals.step.py): same source geometry with skins/visible screws removed and translucent component/service reserves shown.
- [Primary STEP](head-layout.step), [entry source](head-layout.step.py), [parametric model](layout_model.py), [construction brief](brief.md).

## What changed

| Feature | Layout 01 | Layout 02 |
|---|---:|---:|
| Main shell H × W × D | 95 × 130 × 115 mm | **86 × 130 × 115 mm** |
| Head height including crown | 109 mm | **102 mm** |
| Width including ears | 150 mm | **150 mm** |
| Ear diameter | 45 mm | **60 mm** |
| Camera crown base / top width | 58 / 38 mm | **46 / 34 mm** |
| Flat upper bezel above opening | 23 mm | **15 mm**, to the Z84 front-face edge |
| Visible opening | 99 × 58 mm rectangle | **99 × 58 mm, four 3 mm clips** |
| Active pixels | 95.04 × 53.86 mm | **Unchanged and fully exposed** |

The main shell, rear cover and face have clipped outer corners. A **flat sloping band** joins the face to the sidewall, leaving the two distinct crisp edges requested in the reference. The shell has 0.4 mm recessed side lands and 0.7 × 0.5 mm shallow front panel lines. Front/rear and ear-cap service seams are real; the visual panel lines are integral.

The **front bezel and camera crown are one solid part**. A separate camera edge bracket sits behind it. The addressable-light package reserve is entirely within the crown: its lower edge is Z89.3, **3.3 mm above the main roof**. The full LED assembly still needs its actual on-hand PCB/optic dimensions; the CAD reserve is 5 × 5 × 3 mm plus a small diffuser, not a newly selected LED SKU.

The ears have dark ridged mounting rings, hollow tapered removable caps, reinforced receiving posts, four recessed visible M2 screws per cap and two hidden mounting screws per ear. A thin amber ring and dark centre represent surface treatments. Their cosmetic walls remain thin; the local bosses and internal web provide the mounting material. The current lower/inboard ear/skin openings are **temporary layout-clearance reliefs**, not an approved exposed-mechanism exterior. The finished head needs a moving or overlapping shroud/side panel that hides the yoke in normal views while retaining combined-motion clearance. The circular outer ear faces remain intact; validate the eventual shroud on a physical mock-up from low angles.

Visible hardware totals **18 M2 screws**: six front, four rear, eight ear-cap screws. Four additional hidden ear-mount screws are included in the existing hidden-hardware allowance. Front screws are nominal M2×10; rear/cap/ear-mount screws M2×6. Heads, hex sockets, 4.2 mm wells, clearance holes and receiving pilots are modeled. Threads are simplified major-diameter cylinders. **Receiving pilots are not approved repeat-use PLA threads**: select inserts/captive nuts and finalize screw engagement before printing functional parts.

## What “1:1” means here

No imported component is scaled: catalog STEP solids are rigidly rotated/translated with scale 1, and the authored display/C2/LED reserves use the stated millimetre dimensions. The shell fits around the hardware; the perspective illustration supplies appearance, not dimensional evidence.

| Component | Evidence used | What remains estimated |
|---|---|---|
| Waveshare ESP32-S3-LCD-4.3, no-touch SKU 30493 | Published drawing; conservative union 106.1 W × 68 H × 10.6 D mm; active area 95.04 × 53.86 | Exact connectors, sample tolerances and retention details |
| Camera Module 3 Wide | Existing manufacturer STEP, rigidly rotated/translated; 25 × 24 × 12.4 published envelope used for fit | CSI bend, entrance pupil, optical cone and final bracket hardware |
| Two XC330 references | Existing manufacturer STEP, including horn protrusions, rigid transforms only | Final servo SKU, mount-hole adapters, coupler and thermal/trajectory acceptance |
| ESP32-S3-Zero headerless | **23.5 × 18 mm footprint** and upper-edge USB orientation from [Waveshare drawing](https://docs.waveshare.com/assets/images/Esp32-S3-Zero-Size-b56afa84e292cd9d532df8b52376fcb2.webp) | Board thickness, component-height union, removable mount and cable/plug dimensions |
| M2 button heads | 3.5 mm head diameter, 1.3 mm head height and 1.3 mm hex from [supplier size table](https://monsterbolts.com/pages/m2-bolt-size) | Exact purchased lengths/kit, thread details and measured mass |

The text-to-cad `step-parts` search found **no ESP32-S3-Zero model and no exact M2 button-head model**. Its M2 low-head socket-cap results were not silently substituted for button heads. Existing camera/servo source files remain in [Layout 01 catalog parts](../layout-01/parts/README.md); this revision reuses them. Imported non-solid annotation/open-surface geometry is omitted from the displayed solid assembly; [assembly-checks.json](assembly-checks.json) records retained solid counts and bounds.

Display/camera packaging now has a **1 mm vertical PCB gap**; rear connector and CSI reserves are separate from the hardware. The camera opening is a trial optical clearance and has **not passed a field-of-view/vignetting test**.

## Mechanism and service map

| CAD part | Purpose and moving frame |
|---|---|
| Connected rolling cradle, central flange and ear stalks | Carries the face/display and cosmetic ears; rolls, pitches and yaws. The former floating ribs now connect to a central flange and forward ear mounts. |
| 6 mm rolling spindle | Metal load path through the roll-bearing pair; rotates with the face. Diameter/retention remain trial choices. |
| Two 16 × 6 bearing reserves | Support the spindle independently of the servo output bearing, **22 mm centre-to-centre**. Exact bearings/fits/preload remain open. |
| Bearing cartridge | Holds the bearing pair on the tilting frame. Its 16.6 mm bore is a layout clearance, not a finished bearing fit. |
| Coaxial coupling | Connects the roll output to the independently supported spindle; shown with a shaft bore. Hub fastening and torque transmission remain open. |
| Roll XC330 reference | Housing tilts with pitch and yaws; its output drives roll. It is supported by the modeled saddle. |
| Connected pitch frame and roll-servo saddle | Supports the cartridge and roll actuator, then tilts about the side trunnions. Relieved crossbars clear the fixed pitch actuator. |
| Pitch trunnions | Side pivot shafts defining the pitch axis; separate from the cosmetic ears. |
| Pitch XC330 reference and over-top adapter | Fixed to the yaw-carried assembly; drives the tilting frame. Adapter outline/load path is reserved; manufacturer mounting-hole pattern and fasteners are not detailed. |
| Two outer yoke legs and bridge | Carry the pitch pivots, moving with yaw only. Their swept entry creates the hidden ear/skin openings. |
| Yaw spindle/interface | Marks the body interface and 60 mm neck allocation. Body-fixed yaw actuator and body shell are outside this model. |
| C2 footprint, component reserve and upper USB service reserve | Separate motion controller near the rolling axis. USB exits toward +Z. The service corridor is empty space for a stationary plug/withdrawal operation, not another component. |
| Camera CSI exit reserve | Space for the camera ribbon and its first bend behind the camera board. It does not certify a bend radius or moving-cable lifetime. |
| Display rear connector/flashing reserve | Space behind the complete display stack, distinct from glass, PCB and active pixels. Final connector orientation and flashing breakout remain open. |

Service intent: remove the rear cover with the head powered off and supported; access C2 USB/BOOT/RESET from the rear, or remove its eventual carrier. Front-carrier removal exposes display/window/camera retention. Ear caps reveal the hidden ear-mount screws. A complete sealed flashing breakout, yaw demating connector and guided moving wire loops are still required by CAD-04/CAD-04a/CAD-05; their presence is **not claimed** by a translucent reserve.

## Balance and validation

[mass-placement.json](mass-placement.json) replaces the old shell/crown/frame allocations **within this study**, using authored PLA volumes at 1.24 g/cm³ plus explicit finish, module and hardware allowances. With the 20 g C2 scenario, the carried masses are approximately **371 g roll, 443 g pitch and 515 g yaw/complete moving head**. These are D/E estimates, not accepted W readings. The 10–35 g C2 sensitivity gives approximately 505–530 g complete mass.

A0 is iterated from that ledger: pitch approximately **X−39.40, Z45.32 mm**; roll axis **Y−1.06, Z46.67 mm**. These are layout datums, not measured achieved balance. Estimated neutral inertias are approximately **0.000703 kg·m² roll, 0.000786 pitch, 0.001155 yaw**, using CAD intrinsic properties/explicit box approximations and parallel-axis terms. Actual component distribution, wiring forces and dynamic demand must replace these approximations before servo selection.

Verification artifacts:

- [Combined-motion checks](fit-checks.json): independent 7×8 grid across roll ±18° and pitch −22…+40°, including the changed shell/ears/cradle and both actuator envelopes.
- [Neutral assembly checks](assembly-checks.json): same-frame non-fastener intersections, full-size package fit, active-pixel exposure, LED placement, service corridor and imported solids.
- [Final verification and snapshots](review/verification.md): 54 authored occurrences passed full solid checks; all 715 occurrences passed topology checks. The 8,904 sampled motion-pair checks had no overlaps.

These checks do not establish continuous clearance, manufacturing tolerance, complete cable routing, body/yaw clearance, fatigue, printed stiffness/creep, optics or print readiness. The neutral 102 mm crown-inclusive head also means **302 mm** for the original 140+60 mm body/neck stack; [baseline v1.9](../../../../../01-system/dimensional-baseline.md) records that explicitly for RP-06 integration.

## Reproduce

Use the **text-to-cad 0.4.28** interpreter and matching plugin CLI; the newer global cadgen workflow uses a different entry contract. Run from the repository root. `mass_layout.py --solve` refreshes A0, `write_viewer_params.py` refreshes the self-contained pose sidecar, and the matching plugin `scripts/gen` writes each `.step.py` target with `--write`. Then run `check_layout.py`, `check_assembly.py`, plugin `inspect refs/validate/measure`, and plugin `snapshot --job …/review/snapshot-job.json`. Never edit STEP or generated topology to fix geometry.
