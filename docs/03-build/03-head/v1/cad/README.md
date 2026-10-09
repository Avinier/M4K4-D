# Head v1 CAD

Head v1 starts from the latest RP-06 head, Layout 04, and is now the live source
used by body v1. The source and purchased reference STEPs are local to this
folder. `head-v1.step.py` produces a parts-only head assembly;
`head-v1-integrated.step.py` places it on the latest body v1 and chassis v1.
The latter imports `build_body_assembly()` from body v1, so the chassis is the
actual chassis v1 reference already used by the body, with no second set of
manually positioned solids.

## Source and outputs

| Path | Role |
|---|---|
| `layout_model.py`, `details.py`, `inspection_scene.py`, `harness.py`, `optics.py` | Editable head geometry, mechanism, and inspection groups. |
| `layout_axes.py`, `motion_envelope.py`, `mass_layout.py` | A0 datums, pose limits, and estimated mass. |
| `purchased/` | The 1:1 display, camera and C2 source STEPs copied from RP-06 Layout 01, the drawing-based STS3045M reference and the official goBILDA 4001-0025-0006 coupler STEP (D-049). `xc330.stp` is kept for history; nothing installs it. |
| `feetech.py` | D-049 STS3045M installation: servo poses, roll coupler and pitch horn stack, mount and collar parameters; the D-050 yoke leg outline, plinth and gusset. |
| `head-v1.step.py` | Standalone head CAD export. |
| `head-v1-integrated.step.py` | Parts-only head plus latest body and chassis assembly. |
| `head-v1-presentation.step.py` | The same robot as built: every part opaque, reservations and overlays left out (D-050). Use it to judge appearance; the inspection models draw the skin and shell at alpha 0.28. |
| `yaw-yoke.step.py` | Compact review of the turntable, legs, accent inlays, and pitch trunnions. |
| `ears-v1.step.py` | Focused two-ear assembly with caps, colour inlays, cradle and service hardware. |
| `check_ears.py`, `generated/ear-service.json` | Nominal cap and inner-mount removal paths, fastener count, and solid/finish checks. |
| `check_integration.py` | Checks the shared yaw datum, disc height, three hub screws, and head sweep floor. |
| `generated/`, `snapshots/` | Derived fit data and review images. |
| `purchased/sts3045m_reference.step.py`, `.step` | Drawing-based Feetech STS3045M packaging reference, checked against the drawing in D-049 step 0. See its [brief](purchased/sts3045m_reference-brief.md). |
| `check_feetech_mounts.py`, `generated/feetech-mounts.json` | D-049 audit: spline and thread engagements, ear joints, insert walls, driver paths and posed minimum clearance of every D-049 part. |
| `check_leg_clearance.py`, `generated/leg-clearance-d049.json` | Both yoke legs against every moving part (56 poses); compare with `generated/feetech-mounts-baseline.json` from the committed head. |
| `check_leg_clearance_d050.py`, `generated/leg-clearance-d050.json` | The same sweep on the D-050 matched legs. |
| `fea/` | Head v1 stiffness FEA (pitch frame, roll mount, +Y yoke leg), adapted from RP-06 Layout 04. See its [README](fea/README.md). |
| `busy_minute.py`, `generated/busy-minute-d049.json` | RP-01 §11.3 busy minute re-run on the D-049 mass tree with the D-046 pitch cap, and STS3045M moving-curve margins. |
| `check_feetech_head_envelopes.py`, `check_feetech_head_fit.py`, `feetech_mass_whatif.py` | **Superseded** pre-installation trials against the XC330 head; see [feetech-head-fit.md](feetech-head-fit.md). |

The [Feetech head fit report](feetech-head-fit.md) records the current
neutral-pose clashes and preferred trial clockings. It is a redesign input,
not a release of the replacement mounts.

Run from this directory with Python 3.13 and `cadgen==0.4.28`; the existing
project runtime is `/Users/avinier/.codex/runtimes/text-to-cad/0.4.28/venv/bin/python`.
The matching legacy model entry point is
`/Users/avinier/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen`.
Use `rtk proxy` before shell commands as required by the repository instructions.

```sh
CAD_PY=/Users/avinier/.codex/runtimes/text-to-cad/0.4.28/venv/bin/python
CAD_GEN=/Users/avinier/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/gen
rtk proxy "$CAD_PY" check_integration.py
rtk proxy "$CAD_PY" "$CAD_GEN" head-v1.step.py --write
rtk proxy "$CAD_PY" "$CAD_GEN" head-v1-integrated.step.py --write
```

The source includes the body's three R22 M3 hub insert locations (210°, 270°,
330°). Head v1 cuts Ø3.4 disc clearances and Ø6 × 1.8 counterbores, with
nominal flush M3 × 6 fasteners. The modeled 3.8 mm engagement into each
body-side M3 × 4 insert leaves the head-to-disc motion clearance unchanged.
The disc still has the central cable bore and top groove. The body yaw
cartridge, bearing, driven gear, scissor pinion, and FFC cassette stay owned by
body v1.

## Yaw yoke

D-050 makes the two legs one matched design (`feetech.py`, `layout_model.py`).
Each is a 6 mm web with a faceted outline: a plinth flaring onto the disc, a
waist at disc+23, and an arm rising into the head to the Ø22.4 pad. An inboard
gusset fans out under the head. The outline is the D-049 free corridor eroded
0.5 mm and simplified at 0.45 mm, so every facet lies inside the measured free
space, unioned with the pre-D-049 leg, which the shell reliefs are cut around.
That replaces D-049's +Y leg, which followed the corridor in 1 mm stair steps,
had a ledge out to dx +10 at disc+15 and a 24.5 × 15 mm box foot. The +Y leg
adds the horn pocket and screws, the −Y leg the trunnion bore and pitch-stop
sector. The skin, ear and cradle reliefs are still cut by the pre-D-049 leg
(`relief_tool`), so no head shell volume changes.

The outside faces keep the 0.75 mm raised rear rail, the 1.15 mm recessed
spine panel and its copper inlay (0.05 mm adhesive bed, 0.15 mm proud), now
ending at disc+30.5 so the waist keeps a ≥ 1.2 mm lip in front of the pocket.
Both legs carry the ear trim-stack band and the 0.5 mm skin step. Both are
printed in CF-filled filament (D-049).

The turntable disc's rim tapers from R62.5 under the plate to R58.5 at its
foot, with a 0.6 mm top chamfer, so its lower edge sits inside the body roof
(it overhung the roof's rear edge by 2.4 mm). The rim keeps 2.0 mm from the
body's yaw pinion.

## Ears

Each ear is a layered enclosure, now detailed as separately printable inner
mount, hollow cap, 1.2 mm amber ring, and 1.2 mm dark centre. The centre
recess leaves a 1.7 mm cap backing and a 0.1 mm adhesive bed. The inner
mount ring has a 2 mm radial wall and an internal web; two stepped M2 cap
receivers on the upper arc tie into that ring, each with an M2 heat-set
insert. Two exposed M2 × 6 screws hold each cap; the lower quadrant is kept
clear of the pitch yoke's stop sweep. Behind it, two recessed M2 × 4 screws
hold the inner mount to inserts in the cradle stalk pads; their heads seat on
a 1.2 mm floor. A central M2 × 5 retainer holds the removable Ø12 × 2.5 mm
trim stack (tungsten slugs plus spacer discs, always built to 2.5 mm so the
screw cannot bottom); the cap must come off to reach it.
This gives 5.46 g maximum trim per ear at the estimated tungsten density;
the working mass model uses half that capacity. Final A0 balance must be
measured on the assembled head.

The intended service order is to remove the two exposed screws, withdraw
the cap and bonded colour inserts outboard, remove the two hidden mount
screws, and withdraw the inner ring. `check_ears.py` tests that nominal
straight path on both sides at neutral and checks one valid solid per main
print part. The check does not prove driver room, wire slack, insert pull-out,
or repeated removal. Print dimensions and orientation still need a slicer
and fit coupon; see [`../research/fabrication-audit.md`](../research/fabrication-audit.md).

## Fabrication details (2026-10-07)

Changes from the [fabrication audit](../research/fabrication-audit.md):

- **Walls.** The skin inset is 1.3 mm (`SKIN`), which keeps the tapered rear
  facets at ≥ 1.2 mm along their normals; the recessed stern lands have a
  0.5 mm inner doubler. The front bezel's band and crown walls are 1.3 mm
  along their own normals (`bezel_band_inner`, `crown_inner`). The window lip
  is 1.3 mm: the glass sits 0.35 mm further back and is now **106 mm** wide
  (was 110), still 3.5 mm per side under the lip beyond the 99 mm aperture.
  The front chamfer is 9.5 mm (was 10) so the band's lower corner keeps its
  wall at the display board corner. The crown's rear CSI opening follows the
  crown cavity instead of notching the sloped sides.
- **Pitch stop pin.** The lug leaves a 2 mm ligament round the Ø2 pin; the
  pitch frame now exports as a watertight mesh.
- **Inserts.** Every printed M2 receiver takes one article: M2 × 3 brass,
  OD 3.6, in a Ø3.2 pilot at least 3.5 mm deep (CNC Kitchen / Purecrea
  class; the OnlyScrews M2 × 3 is OD 3.9 and does not suit this pilot).
  Screw tips that pass an insert run into Ø2.2 reliefs, not plastic. The
  six front receivers now run forward to X −5, so each bezel pad clamps on
  its receiver; the front screws are M2 × 8. The side screws moved to
  |Y| 56.4. The ear cap receivers carry inserts (the old pockets at
  45/135/225/315° had no screws and are gone).
- **Hardware added.** Four ISO 4762 M2 × 25 screws fix the bearing
  cartridge to the pitch-frame slab (2 mm side-open spot faces, slab widened
  to ±13 at each pair; D-049 moved the rear pair to X −57.5). The
  roll-bearing retainers are 1.2 mm plates held by M2 × 4 screws on the lower
  diagonals at R10.5: at R9 on ±Y their insert pockets broke 0.15 mm into
  the bearing seats.
- **Pitch and roll servos.** Superseded by D-049; see *STS3045M
  installation* below.
- **Small parts.** Camera receivers at Y ±16 with R2.8 bosses; the bracket's
  lips, cap and boss are ≥ 1.25 mm. C2 tray jaws are 1.25 mm.

`check_fasteners.py` writes `generated/fastener-stack.json`: for every
modeled M2 screw it samples what the shank passes through (clearance,
insert pocket, plastic, tapped metal or air) and fails on plastic, short
engagement or a pocket shallower than the insert.

## STS3045M installation (D-049)

`feetech.py` holds every D-049 dimension; `layout_model.py` and `details.py`
build from it. Summary (full record: [D-049](../../../decisions.md#d-049)):

- **Roll:** servo on a 5 mm ear plate behind the torsion box, spline on the
  roll axis, long side down, 1.0 mm in front of the rear cover. goBILDA
  4001-0025-0006 coupler clamps the Ø6 spindle (X −74.6…−40). Rear bearing at
  X −60.6 (spacing 17.6). Ear screws drive from behind with the cover off.
- **Pitch:** servo on the pitch frame (collar, web to the torsion box, floor
  to the keel), spline on the pitch axis, long side at 244°. Its 25T horn sits
  in a 0.6 mm pocket on the +Y yoke leg and is screwed to it from outside, so
  the case turns round a fixed output. No +Y trunnion pin or adapter.
- **Ears:** ISO 7380 M2 × 6 on ISO 7089 M2.5 washers into M2 × 3 inserts.
- **Yoke legs:** the +Y leg is widened within the swept-volume corridor, with
  a foot, an inboard rib and a Ø22.4 horn pad. Both legs have an outer-face
  relief band along the ear trim stacks' path and shorter styling rails.
  Shell reliefs still use the pre-D-049 legs. Print both legs in CF-filled
  filament (E ≥ 4.5 GPa).
- **Rear trim:** two Ø14 brass stacks at the roll axis ±30 mm in Y, 22 mm up.

`check_feetech_mounts.py` audits the interfaces and posed clearance;
`fea/` holds the stiffness FEA; `busy_minute.py` re-runs the §11.3 busy minute.

## Verification

`cad_cache.py` stores source-keyed BinTools BReps under ignored `.cache/`;
`mass_layout.py --solve` bypasses it while changing A0 axes. Cold relief
sampling uses spawned workers and can be forced serial with
`MAKAD_RELIEF_SERIAL=1` when inspecting a build. To compare full
check outputs with the checked in references, run
`python tools/compare_golden.py`. The active goldens come from committed
D-049. `run_checks.py` runs mass, envelope, head
checks and body hand-off in dependency order, with input hashes for incremental
reruns. `--fast` uses separate revision, layout, mount and fastener outputs;
the full 7 × 8 grid remains the sign-off run. The mount script writes
`generated/feetech-mounts-fast.json` for this mode. See
`tools/profiling.md` for measured
timings and remaining targets.

- `generated/integration-fit.json`: head/body yaw datums and disc seating
  coincide, all three screw axes meet the hub inserts, nominal screw engagement
  is 3.8 mm, and the bolt shafts keep at least 10.47 mm from the stationary
  pinion's modeled outer radius over ±62° yaw.
- `revision-checks.json` (D-049): the 56 sampled roll/pitch poses pass with no
  mechanism or harness intersections (3,208 pairs per pose); neutral service
  extraction, retention and hard-stop checks pass.
- `generated/fastener-stack.json` (D-049): all 40 modeled M2 screws pass,
  including the eight servo ear screws; insert joints have 2.6–3.0 mm of
  shank in the insert.
- `fea/results.json`: pitch frame 112.5 N·m/rad, +Y leg 49.9, roll mount
  455.9 at E 3.5 GPa; pitch chain 31.6 Hz in PLA, 34.3 Hz with CF legs.
- `generated/busy-minute-d049.json`: §11.3 rebuilt and validated against the
  RP-01 workbook; STS3045M worst moving-curve ratios pitch 1.71×, roll 3.04×.
- Body v1's `generated/yaw-stage.json`: the yaw stage, drive sweep, gear mesh,
  assembly lowering paths, and modeled disc/hub contact pass. Its gear and
  bearing estimates remain estimates.
- `dimensions.md` and `mass-placement.json`: source-derived dimensions and
  estimated mass. The 293.5 mm whole-robot crown height uses the shared body
  yaw datum.
- `snapshots/`: the integrated isometric snapshot reviewed after export.

Head v1 retains the RP-06 Layout 04 head mechanism and 1:1 module envelopes:
removable front carrier and rear cover, camera bracket, C2 tray, ears,
bearing cartridge, and servo mounts. The main CAD views group parts by shell,
ears, display, camera, controller, roll, pitch, yaw, and fasteners. Inspection
overlays remain in the source and checks but are omitted from these exports.
The harness branches are trial routes and the mass tree is estimated. Purchased bearing/insert fit coupons,
the received STS3045M, horn and coupler fits (D-049), loaded stiffness, cable
flex, and measured A0 trim remain build gates; the CAD geometry alone does not
close them.
