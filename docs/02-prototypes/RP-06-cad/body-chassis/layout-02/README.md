# RP-06 integrated body/chassis Layout 02

This is the active whole-body CAD path. It retains Layout 01's source-linked RP-01 Layout 03 head, compact two-wheel chassis, connected rear skid, fixed ball-transfer nose, internal packaging and purposeful review layers, while closing the first-pass integration questions:

- four M4 through-bolts and two locating pins now define the body-frame-to-chassis interface;
- enlarged front and rear shell openings are the octagonal service-panel outlines offset inward by a constant 2 mm land; each panel's straight side edges are parallel to the corresponding shell edges (measured from the solids, not the constants); a separate internal frame behind each shell end wall carries four fused M3 bosses, with M3 × 8 screws seated on the panel face;
- the front panel starts at Z = 58 mm, above the chassis deck, so it lifts off forward over the front crossmember; the chassis rails pass the lower front band through open-bottom shell notches, and the deck now stops inside the shell's front wall. The rear panel keeps its Z = 42 mm lower edge;
- the front slat motif is now a functional open speaker grille over a provisional 50 mm basket/44 mm cone, amplifier envelope and acoustic cavity;
- four body-mounted PDM microphone boards, acoustic ports and shell penetrations are allocated; exact audio SKUs remain an RP-05/RP-06 selection gate;
- the front range sensor sits beside the battery at Y = +38 mm, Z = 68 mm, below the speaker grille, and looks through its own window in the front panel; and
- a stationary neck cowl plus head-yaw-moving lower yoke shrouds visually shorten the U-shaped yoke while preserving the existing yaw and pitch axes.

Per CAD-context decision [`RP03-CAD-01`](../../decisions.md#rp03-cad-01--rear-only-ground-reflectance-channel), the layout now uses one guarded rear TCRT5000 channel. Its optical patch is 27 mm behind the skid contact, its optical face is modeled 10 mm above ground, and its protective rails begin at 7 mm. The connected skid pad begins at 3.5 mm, so it contacts first. The front and lateral TCRT packages, mounts and cable reserves are removed.

Per CAD-context decision [`RP03-CAD-02`](../../decisions.md#rp03-cad-02--lean-fixed-ball-nose-with-concealed-contact), the non-functional stance-wide bumper and outboard switches are removed. The frozen ball datum is retained in a narrower load-bearing collar, paired flange keepers and compact shroud, with a 42 mm concealed-contact fascia and 3 mm travel reserve. These are CAD-first choices pending permanent propagation, not project-wide safety approval.

Per CAD-context decision [`RP03-CAD-03`](../../decisions.md#rp03-cad-03--faceted-rear-tail-and-sensor-cartridge), the rear skid and TCRT packaging are consolidated into one eleven-station faceted arc. Its straight ruled links descend from the rear crossmember, form the skid belly, then rise more tightly toward a compact upturned point—there is no smooth spline. The module is a separate selectable top-level group with a genuinely hollow, 34%-opaque ivory shell, visible blue load spine, visible TCRT cartridge/cable path, replaceable 3.5 mm-clearance wear shoe, replaceable 7 mm-clearance protective lips and a translucent flush sensor cap. Layout 01.5 moves the sensor forward from X = −110 to −97 mm, raises its optical face from 8 to 10 mm, and shortens the root-to-tip projection from 84 to 66 mm.

## Files

- `body-chassis.step.py` — buildable STEP entry.
- `body_chassis_model.py` — parametric assembly source and mass/frame data.
- `body-chassis.params.js` — viewer controls for shell, head yaw, electronics, harness, and physics.
- `write_outputs.py` — generated dimensions, frames, and mass/CoM reports.
- `check_layout.py` — deterministic parameter/interface checks.
- `../layout-01/references/purchased/` — shared vendor STEP, kept local (not in Git). Hashes in the Layout 01 README.
- `generated/` — machine-readable and Markdown outputs.
- `snapshots/` — required visual-review packet.

The RP-01 head is a live source dependency. Changes in Layout 03 flow into this assembly on regeneration.

The neutral dimensional stack is 304 mm: 140 mm body/yaw datum + 60 mm neck allocation + 104 mm Layout 03 crown-inclusive head. The 300 mm system figure is therefore a rounded target, not a passed height envelope. The visible body is 110 mm tall with 30 mm ground clearance, matching the system baseline. The RP-01 yaw yoke remains live Layout 03 trial geometry; Layout 02's added shrouds are cosmetic/packaging parts, not evidence that the yoke is load-rated or fabrication-final.

## Generation

Run from the repository root using the CAD environment carried by [`base/pass-01/`](../../base/pass-01/):

```text
docs/02-prototypes/RP-06-cad/base/pass-01/.venv/bin/python \
  <text-to-cad>/skills/cad/scripts/gen \
  docs/02-prototypes/RP-06-cad/body-chassis/layout-02/body-chassis.step.py \
  --write
```

Then run `write_outputs.py`, `check_layout.py`, CAD inspection, validation, and the snapshot job.

The selected TCRT5000 breakout/comparator PCB and connector are still unresolved. The yellow body inside the translucent rear module therefore remains a package envelope and its cyan connector/strain-relief solids are reserved volumes. Layout 02 makes no dedicated forward or lateral cliff-protection claim; its provisional level-floor operating restrictions are recorded in the CAD decision register.

## Validation note

All Layout 02-authored mounts, fascia, panels, panel hardware, audio packaging,
neck treatment, body, chassis, fixed ball-transfer, faceted rear tail and rear
sensor geometry validates as closed, positive-volume BREP. Full-assembly
validation still reports five
inherited self-intersecting occurrences inside the frozen Raspberry Pi 5 vendor
STEP. None is part of this Layout 02 revision; the exact SKU is retained
rather than replaced with a cosmetic placeholder.
