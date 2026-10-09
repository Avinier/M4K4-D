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
| `purchased/` | The four 1:1 display, camera, C2, and XC330 source STEPs copied from RP-06 Layout 01. |
| `head-v1.step.py` | Standalone head CAD export. |
| `head-v1-integrated.step.py` | Parts-only head plus latest body and chassis assembly. |
| `yaw-yoke.step.py` | Compact review of the turntable, legs, accent inlays, and pitch trunnions. |
| `ears-v1.step.py` | Focused two-ear assembly with caps, colour inlays, cradle and service hardware. |
| `check_ears.py`, `generated/ear-service.json` | Nominal cap and inner-mount removal paths, fastener count, and solid/finish checks. |
| `check_integration.py` | Checks the shared yaw datum, disc height, three hub screws, and head sweep floor. |
| `generated/`, `snapshots/` | Derived fit data and review images. |
| `purchased/sts3045m_reference.step.py`, `.step` | Drawing-based Feetech STS3045M packaging reference. See its [brief](purchased/sts3045m_reference-brief.md); horn and mounts still need measured details. |
| `check_feetech_head_envelopes.py`, `check_feetech_head_fit.py`, `feetech_mass_whatif.py` | Candidate placements, source-built collision screen and non-destructive mass sensitivity. These do not change the live XC330 assembly or A0 axes. |

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

The two exposed yoke legs now have a darker, faceted outside face: a 0.75 mm
raised rear load-path rail, a 1.1 mm deep recessed spine panel, and a stepped
inward shoulder. A pair of separately printable copper-coloured spine inlays
sit in the recesses with a 0.05 mm adhesive bed and 0.15 mm proud face; the
pockets can also be painted if the inlays are omitted. The 6 mm structural web
remains at least 4.9 mm thick at the recess; the shoulder step leaves at least
5.5 mm across its narrowest point.
The pitch bearing bores, hard-stop contact, disc feet, and inside clearance
are unchanged. Each leg can still print flat on its plain inside face without
trapped support.

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
  to ±13 at each pair). The roll-servo strap moved to X −94, has 4.7 mm
  posts and two M2 × 25 screws into frame bosses beside the saddle. The
  roll-bearing retainers are 1.2 mm plates held by M2 × 4 screws on the lower
  diagonals at R10.5: at R9 on ±Y their insert pockets broke 0.15 mm into
  the bearing seats.
- **Pitch servo.** The adapter has a 3 mm inboard face plate with four
  M2 × 6 screws into the XC330's tapped face holes (axis −22.5/+7.5 in X,
  ±8 in Z, from the vendor STEP). The fit proxy is now case plus two horns.
  The adapter-to-yoke-leg joint is still unfastened.
- **Small parts.** Camera receivers at Y ±16 with R2.8 bosses; the bracket's
  lips, cap and boss are ≥ 1.25 mm. C2 tray jaws are 1.25 mm.

`check_fasteners.py` writes `generated/fastener-stack.json`: for every
modeled M2 screw it samples what the shank passes through (clearance,
insert pocket, plastic, tapped metal or air) and fails on plastic, short
engagement or a pocket shallower than the insert.

## Verification

`cad_cache.py` stores source-keyed BinTools BReps under ignored `.cache/`;
`mass_layout.py --solve` bypasses it while changing A0 axes. Cold relief
sampling uses spawned workers and can be forced serial with
`MAKAD_RELIEF_SERIAL=1` when inspecting a build. To compare full
check outputs with the checked in references, run
`python tools/compare_golden.py`. The D-048 checkout has no
`generated/feetech-mounts.json`, so use `--allow-missing` only until D-049 is
merged and its golden is reviewed. `run_checks.py` runs mass, envelope, head
checks and body hand-off in dependency order, with input hashes for incremental
reruns. `--fast` uses separate revision, layout, mount and fastener outputs;
the full 7 × 8 grid remains the sign-off run. The D-049 mount script must be
updated to write `generated/feetech-mounts-fast.json` for this mode. See
`tools/profiling.md` for measured
timings and remaining targets.

- `generated/integration-fit.json`: head/body yaw datums and disc seating
  coincide, all three screw axes meet the hub inserts, nominal screw engagement
  is 3.8 mm, and the bolt shafts keep at least 10.47 mm from the stationary
  pinion's modeled outer radius over ±62° yaw.
- `revision-checks.json`: the 56 sampled roll/pitch poses pass with no
  mechanism or harness intersections; neutral service extraction and hard-stop
  checks pass.
- `generated/fastener-stack.json`: all 50 modeled M2 screws pass; insert
  joints have 2.6–3.0 mm of shank in the insert.
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
the pitch adapter-to-yoke joint, loaded stiffness, cable flex, and measured A0
trim remain build gates; the CAD geometry alone does not close them.
