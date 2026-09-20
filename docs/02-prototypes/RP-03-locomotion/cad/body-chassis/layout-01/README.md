# RP-03 integrated body/chassis Layout 01

This is the active whole-body CAD path. It replaces the purple head lump and base-only presentation in `base/pass-01` with a source-linked RP-01 Layout 03 head, a 110 mm-tall structural body, translucent shell, internal packaging, a fixed engineered ball-transfer nose, a connected rear skid, tyre-clearance wheel wells, connected 608-bearing carriers, upper wheel arches, and purposeful review layers.

Per CAD-context decision [`RP03-CAD-01`](../../decisions.md#rp03-cad-01--rear-only-ground-reflectance-channel), the layout now uses one guarded rear TCRT5000 channel. Its optical patch is 27 mm behind the skid contact, its optical face is modeled 10 mm above ground, and its protective rails begin at 7 mm. The connected skid pad begins at 3.5 mm, so it contacts first. The front and lateral TCRT packages, mounts and cable reserves are removed.

Per CAD-context decision [`RP03-CAD-02`](../../decisions.md#rp03-cad-02--lean-fixed-ball-nose-with-concealed-contact), the non-functional stance-wide bumper and outboard switches are removed. The frozen ball datum is retained in a narrower load-bearing collar, paired flange keepers and compact shroud, with a 42 mm concealed-contact fascia and 3 mm travel reserve. These are CAD-first choices pending permanent propagation, not project-wide safety approval.

Per CAD-context decision [`RP03-CAD-03`](../../decisions.md#rp03-cad-03--faceted-rear-tail-and-sensor-cartridge), the rear skid and TCRT packaging are consolidated into one eleven-station faceted arc. Its straight ruled links descend from the rear crossmember, form the skid belly, then rise more tightly toward a compact upturned point—there is no smooth spline. The module is a separate selectable top-level group with a genuinely hollow, 34%-opaque ivory shell, visible blue load spine, visible TCRT cartridge/cable path, replaceable 3.5 mm-clearance wear shoe, replaceable 7 mm-clearance protective lips and a translucent flush sensor cap. Layout 01.5 moves the sensor forward from X = −110 to −97 mm, raises its optical face from 8 to 10 mm, and shortens the root-to-tip projection from 84 to 66 mm.

## Files

- `body-chassis.step.py` — buildable STEP entry.
- `body_chassis_model.py` — parametric assembly source and mass/frame data.
- `body-chassis.params.js` — viewer controls for shell, head yaw, electronics, harness, and physics.
- `write_outputs.py` — generated dimensions, frames, and mass/CoM reports.
- `check_layout.py` — deterministic parameter/interface checks.
- `references/purchased/` — checksum-verified purchased STEP dependencies.
- `generated/` — machine-readable and Markdown outputs.
- `snapshots/` — required visual-review packet.

The RP-01 head is a live source dependency. Changes in Layout 03 flow into this assembly on regeneration.

The neutral dimensional stack is 304 mm: 140 mm body/yaw datum + 60 mm neck allocation + 104 mm Layout 03 crown-inclusive head. The 300 mm system figure is therefore a rounded target, not a passed height envelope. The visible body is now 110 mm tall with 30 mm ground clearance, matching the system baseline. The RP-01 yaw yoke remains live Layout 03 trial geometry and is not represented as load-rated or fabrication-final.

## Generation

Run from the repository root using the CAD environment already carried by RP-03 pass 1:

```text
docs/02-prototypes/RP-03-locomotion/cad/base/pass-01/.venv/bin/python \
  <text-to-cad>/skills/cad/scripts/gen \
  docs/02-prototypes/RP-03-locomotion/cad/body-chassis/layout-01/body-chassis.step.py \
  --write
```

Then run `write_outputs.py`, `check_layout.py`, CAD inspection, validation, and the snapshot job.

The selected TCRT5000 breakout/comparator PCB and connector are still unresolved. The yellow body inside the translucent rear module therefore remains a package envelope and its cyan connector/strain-relief solids are reserved volumes. Layout 01 makes no dedicated forward or lateral cliff-protection claim; its provisional level-floor operating restrictions are recorded in the CAD decision register.

## Validation note

The authored body, chassis, fixed ball-transfer, faceted rear tail, rear sensor,
shell, panel and mobility-belt geometry remains closed, positive-volume BREP.
Focused validation of the revised tail and cartridge reports zero invalid or
self-intersecting occurrences. Full-assembly validation still reports five
inherited self-intersecting occurrences inside the frozen Raspberry Pi 5 vendor
STEP. None is part of this RP-03 rear-tail revision; the exact SKU is retained
rather than replaced with a cosmetic placeholder.
