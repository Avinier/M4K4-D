# Layout 03 verification — 2026-09-09

**Geometry, sampled motion, modeled jackets, optics, hard stops and the revised service paths passed the checks below.** Layout 02 was not modified by this implementation. Layout 03 retains unresolved purchased fits and cable-flex transitions; it is not a fabrication release.

## Envelope and taper decision

Physical bounds: X -115.0…0.0, Y -75.0…75.0, Z -60.0…104.0 mm. Inspection overlays do not define product bounds.

Helmet refinement: upper shoulder chamfers deepen from 14 to 24 mm between X−26 and X−60. The 130 mm ear mounting belt continues through X−78, then narrows to 104 mm at X−115. The rear lower edge rises to Z10 and its upper edge is Z84 (74 mm rear height). Rear M2 lands and matching receivers move to Y±44 at Z26/65. The pitch-servo adapter’s unused rear/outboard top corner is clipped along a diagonal from (pitch X−26, Y41) to (pitch X−5, Y55), clearing the deeper shoulder at combined roll/look-up. Its servo seat, back wall and yoke attachment remain. Integral recesses follow the new flanks. Front/ear fit and service splits remain. Nominal wall setting is 1.2 mm; no FEA or printed stiffness claim. The initial conservative 122 × 82 mm stern and its evidence are archived in [pre-helmet source archive](pre-helmet-source-and-evidence.zip).

Camera/display board gap **3 mm**. Crown **104 mm**, +2 mm against Layout 02. The provisional body+neck+head sum is **304 mm**, not 302. Visible yoke **32 mm** retained for the rearward knee, look-up clearance and external loop. Yaw interface Z−60; pitch axis derives from balance and was not lowered for styling.

## Mass and A0

D/E estimates: authored PLA at 1.24 g/cm³ and the existing explicit installed-module, hardware, finish and cable allowances. No duplicate mass from physics/harness/annotation solids.

| Carried set | Layout 02 mass (g) | Layout 03 mass (g) | Layout 02 inertia (kg m²) | Layout 03 inertia (kg m²) |
|---|---:|---:|---:|---:|
| roll | 371.330 | 361.962 | 0.000702609 | 0.000656427 |
| pitch | 443.364 | 436.355 | 0.000785705 | 0.000728097 |
| yaw | 515.339 | 509.361 | 0.001154970 | 0.001080605 |

A0: roll Y=-1.10534, Z=46.91913; pitch X=-37.96453, Z=45.55341 mm. Targeted neutral axis-to-CoM residuals are below 0.002 mm in this estimated mass model. Complete CoM: (-39.564, 0.781, 40.308) mm. These are not achieved measured balance or servo-selection evidence.

The complete estimated mass is 5.98 g lower than Layout 02, while the estimated principal demand inertias also decrease. Together with the checked clearances and extraction paths, this supports the feasibility decision; it does not certify shell stiffness.

## Checks actually run

| Check | Result |
|---|---|
| Physical cross-frame motion | 56 poses × 490 pairs = 27,440; zero detected overlaps |
| Modeled jacket vs mechanism | 56 poses × 210 pairs = 11,760; zero detected pinches |
| Neutral same-frame non-fastener intersections | Zero |
| Original full-size display/package checks | Zero package overlap; zero active-display volume excluded |
| Optical envelope | Nine neutral/extreme combined poses × five obstructions; zero revised intersections |
| Roll hard stops | Contact at −18/+18°; positive interference at −19/+19° |
| Pitch hard stops | Contact at −22/+40°; positive interference at −23/+41° |
| C2 USB installed plug / withdrawal / rear-tool reserves | Clear with rear cover removed |
| C2 removal | Three lift samples to +Z27, then five rearward samples to −X100; tray and board clear other retained physical components |
| Camera removal | Four rearward samples on detached front carrier; camera and bracket clear crown opening |
| Bearing centres | Exported selector measurement: 22.000 mm |
| Authored solid checks | 358 occurrences, zero failures, including self-intersection |
| Entire assembly topology | 1,019 solid occurrences, zero failures; whole-assembly self-intersection skipped for catalog detail |
| Viewer controls | Actual installed resolver tested: 16 master combinations, three pose settings, no missing/double frame assignments; sidecar A0 matches axes.json |

The motion grid is 7 roll values (−18, −15, −6, 0, 6, 15, 18) × 8 pitch values (−22, −15, −5, 0, 10, 20, 30, 40). The sole excluded cross-frame pair is the intentional pitch-servo/output-trunnion interface. Conservative catalog envelopes are used for collision checking; the export retains all 631 camera and 15+15 servo solids at scale 1.

The first extraction route (sideways, then rearward) failed against the pitch frame. It was replaced with the +Z27 lift and rearward path. The helmet refinement reruns the entire 56-pose grid after its mass/A0 update, together with static, optics, hard-stop and service checks. See [source-tagged final checks](../revision-checks.json), [neutral/package report](../assembly-checks.json), [full solid validation](validate-authored.json), [all topology](validate-all-topology.json) and [viewer checks](viewer-checks.json).

## Vignetting report

The old Ø17.2 aperture intersects the conservative corner field envelope by 285.349 mm³ in the modeled front rim. This is a geometric hit, not a predicted percentage of dark pixels. The revised flared opening adds 0.4 mm margin around the field and clears the crown/bezel, display mask/window, main skin and diffuser in all checked poses.

102° horizontal, vertical tangent from 16:9; pupil at X−8 and entrance half-size3mm, front of lens X−2; no entrance-pupil measurement or optical certification.

## Harness limits

The repaired display branch sits farther inward; C2 exits 2 mm higher; the external loop endpoints stop at Z−33. These remove the first-grid jacket pinches. The CSI guide and 30 mm straight sections are modeled, but roll/pitch transitions remain explicitly open. The LED rearward straight reserve does not fit the crown and is a keep-out only. The external R8 yaw loop is illustrative; actual cable radius, pitch-servo exit, guide fasteners, CSI orientation/width, live signal integrity and body-side yaw anchoring are not resolved. CAD-05 is a demating reserve. M006/M020 remain the single cable mass allowances.

## Visual review

The following PNGs render the exported STEP with its explicit pose/visibility sidecar. Front = +X (renderer preset “right”); side = −Y (“front”); rear = −X (“left”). Shell transparency is intentional, inherited from Layout 02 inspection practice.
- [iso](iso_20260909T161154Z.png)
- [front](front_20260909T161154Z.png)
- [side](side_20260909T161154Z.png)
- [rear](rear_20260909T161154Z.png)
- [pitch-up](pitch-up_20260909T161154Z.png)
- [combined](combined_20260909T161154Z.png)
- [physics-fov-on](physics-fov-on_20260909T161154Z.png)
- [physics-fov-off](physics-fov-off_20260909T161154Z.png)
- [harness-on](harness-on_20260909T161154Z.png)
- [harness-off](harness-off_20260909T161154Z.png)
- [C2-rear-access](C2-rear-access_20260909T161517Z.png)
- [C2-isolated-open-rear-XYZ](C2-isolated-open-rear-XYZ_20260909T161656Z.png)

Isolated tray annotation: global neutral centre **(-29.300, -29.000, 40.000) mm**; **ΔX × ΔY × ΔZ = 11.400 × 25.600 × 28.000 mm**. RGB triads and dimension bars are geometry; numeric labels are native occurrence-tree names. The open-rear view avoids hiding the centre triad behind the tray wall.

The initial iso snapshot and first failing reports are retained as diagnostic history only; they are not the final verification images.

## Remaining hardware-specific work

Confirm purchased insert fits and screw lengths, servo mounting pattern/adapters and liner/preload, complete spindle/horn retention, bearing SKU/preload, display retention hardware, guide fastening and cable flex zones. C2 component/USB/BOOT locations and the LED package remain installed reserves awaiting the actual parts. Optical entrance pupil and final window effects require measurement. These limits are explicit in the source/brief and do not constitute a servo freeze, optical certification, continuous-motion certificate, print approval or scored RP gate.

Final STEP SHA-256: `ed17a3c7a9556424f14136d814420add83b65f789783ff6e7d2b310c6bfdd01d`.
