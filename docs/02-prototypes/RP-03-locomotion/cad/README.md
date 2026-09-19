# RP-03 base CAD

Planning home for the RP-03 base CAD. No geometry here yet.

## Current state

| Item | State |
|---|---|
| Locomotion architecture | Concept A: two powered encoder wheels, passive front support, **mandatory** rear anti-tip skid |
| Front support | Type selected: Ø1″ ball transfer (`D21`, BD-08). **SKU open.** `D20` swivel caster is the **required** comparison swap on the same mount |
| SKU set | **Not frozen.** `D02` / `D21` / `DRV-B` / `S01`/`S04`/`S06`/`S07` are leads; substitutes stay live |
| Gates | None passed. ADR-04 not closed. No purchase authorized |
| CAD in this directory | Not started. This is planning only |
| Requirements and todo | [`body-chassis-plan.md`](body-chassis-plan.md) |
| Part identities and envelopes | [`../research.md`](../research.md) |

## Folder rule

`plan.md` §10 stands: **RP-03 does not produce final chassis CAD.** `base/` is a blockout for the selected concept only, and root `cad/` stays reserved for integrated CAD. Integrated whole-body packaging is RP-06's.

`research.md` §1.4 bounds what a blockout may contain. CAD pass 1 may consume bounding boxes, mount holes, shafts, cable exits, 360° keep-outs, and mass/`(x,h)` lumps. It may **not** consume a SKU as frozen geometry, and it may not produce a pretty shell.

Selection of the ball-transfer *type* (BD-08) is not a gate freeze, not a purchase, and not ADR-04 closure. It does not authorize a styled chassis.

## What the blockout is, when it opens

An **ugly, adjustable envelope model** on the axle datum — origin at the floor on the drive-axle contact line, `+x` toward the front support, `+h` up. Not a mini-droid.

It must keep adjustable everything research proved must stay adjustable:

- Ø80–85 mm wheels at 170 mm track, axle at 42 mm;
- front support at 105–115 mm contact with a **0–15 mm height shim**;
- ball and caster interchangeable **via two adapters on one mount**, at the same contact `x`;
- rear skid adjustable across 60–80 mm reach and 8–16 mm height, not a frozen 14/70 solid;
- ballast that sets mass and both CoM coordinates independently;
- battery volume entirely forward of the axle, with an aft fit geometrically impossible.

The datum list is [`../research.md`](../research.md) §5, adopted verbatim as the parameter set. Three CAD-critical mismatches drive the shim stack: axle 42 mm versus 1″ ball ~29 mm versus 30 mm caster ~38 mm; Ø84 × 21 is not a stock article; the `D02` encoder suffix is not listed in India.

Print hubs, shims, carriers, and the two front-support adapters. Buy the tread, the POM ball, and the import encoder motor. Filled envelopes may feed the ugly model. They do not authorize a SKU freeze, an FDM tyre freeze, or a pretty shell.

## Planned tree

Target structure, not files to create before modelling begins. The workflow mirrors [`RP-01-head/cad/head/layout-03`](../../RP-01-head/cad/head/layout-03/): one active folder, centralized parameters, generated dimensions and mass outputs, deterministic checks, saved review views.

```text
cad/
├── README.md
├── body-chassis-plan.md
└── base/
    └── pass-01/
        ├── brief.md
        ├── source/                  # parametric source and centralized parameters
        ├── references/              # vendor drawings/models and measured envelopes, with capture class
        ├── generated/               # dimensions, mass register, CoM/tip outputs, interface tables
        ├── checks/                  # geometry, clearance, stability, provenance checks
        ├── exports/                 # STEP/STL only when explicitly generated
        └── snapshots/               # review views
```

Accepted values propagate to the Markdown specifications only after checks pass. `decision.md` receives nothing until a freeze.
