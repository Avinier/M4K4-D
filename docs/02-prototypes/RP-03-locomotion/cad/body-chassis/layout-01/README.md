# RP-03 integrated body/chassis Layout 01

This is the active whole-body CAD path. It replaces the purple head lump and base-only presentation in `base/pass-01` with a source-linked RP-01 Layout 03 head, a 110 mm-tall structural body, translucent shell, internal packaging, a fixed engineered ball-transfer nose, a connected rear skid, tyre-clearance wheel wells, connected 608-bearing carriers, upper wheel arches, and purposeful review layers.

Per CAD-context decision [`RP03-CAD-01`](../../decisions.md#rp03-cad-01--rear-only-ground-reflectance-channel), the layout now uses one guarded rear TCRT5000 channel. Its optical patch is 40 mm behind the skid contact, its optical face is modeled 5 mm above ground, and its sacrificial guard rails begin at 2.5 mm. The front and lateral TCRT packages, mounts and cable reserves are removed. This is a CAD-first choice pending permanent propagation, not a project-wide safety approval.

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

The selected TCRT5000 breakout/comparator PCB and connector are still unresolved. The yellow rear body therefore remains a package envelope and its cyan connector/strain-relief solids are reserved volumes. Layout 01 makes no dedicated forward or lateral cliff-protection claim; its provisional level-floor operating restrictions are recorded in the CAD decision register.

## Validation note

The authored body, chassis, fixed ball-transfer, skid, rear-sensor, shell, panel,
and mobility-belt groups pass deep solid validation (95 scoped occurrences:
closed, positive volume, no reported self-intersections). Full-assembly validation additionally
reports five self-intersecting occurrences under
`C0_RASPBERRY_PI5_EXACT_STEP`. Those occurrences come from the frozen vendor
Pi 5 STEP dependency, not the RP-03-authored geometry; the exact SKU model is
retained rather than substituted with a cosmetically clean placeholder.
