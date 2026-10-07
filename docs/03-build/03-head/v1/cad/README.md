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
mount ring has a 2 mm radial wall and an internal web; four M2 cap receivers
tie into that ring. Two exposed M2 × 6 screws on the upper arc hold each cap;
the lower quadrant is kept clear of the pitch yoke's stop sweep. Behind it,
two recessed M2 × 4 screws hold the inner mount to the cradle stalks. A
central M2 × 6 retainer holds the removable Ø12 × 2.5 mm tungsten trim slug;
the cap must come off to reach it.
This gives 5.46 g maximum trim per ear at the estimated tungsten density;
the working mass model uses half that capacity. Final A0 balance must be
measured on the assembled head.

The intended service order is to remove the two exposed screws, withdraw
the cap and bonded colour inserts outboard, remove the two hidden mount
screws, and withdraw the inner ring. `check_ears.py` tests that nominal
straight path on both sides at neutral and checks one valid solid per main
print part. The check does not prove driver room, wire slack, insert pull-out,
or repeated removal. Print dimensions and orientation still need a slicer
and fit coupon; see `../fabrication-audit.md`.

## Verification

- `generated/integration-fit.json`: head/body yaw datums and disc seating
  coincide, all three screw axes meet the hub inserts, nominal screw engagement
  is 3.8 mm, and the bolt shafts keep at least 10.47 mm from the stationary
  pinion's modeled outer radius over ±62° yaw.
- `revision-checks.json`: the 56 sampled roll/pitch poses pass with no
  mechanism or harness intersections; neutral service extraction and hard-stop
  checks pass.
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
pitch-servo adapter detail, loaded stiffness, cable flex, and measured A0
trim remain build gates; the CAD geometry alone does not close them.
