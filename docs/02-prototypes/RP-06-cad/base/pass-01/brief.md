# RP-03 CAD pass 1 — construction brief

Ugly, adjustable envelope model of the Concept A base. Not a freeze, not a purchase, not a pretty shell, not final chassis CAD, not RP-06 integration.

## Authority

| Item | Status in this model |
|---|---|
| Architecture | Concept A: two powered encoder wheels, passive front support, **mandatory** rear anti-tip skid |
| Front support type | Ball transfer V1 (`D21`, BD-08). **SKU open.** |
| Required swap | `D20` Ø25–32 mm swivel caster on the **same mount**, same contact `x` |
| SKU set | **Not frozen.** Leads only: `D02` / `D21` / `DRV-B` / `S01`/`S04`/`S06`/`S07` |
| Gates / ADR-04 | None claimed. No `BD-` row issued |

Consumed revisions: RP-01 Layout 03 (mass + yaw-interface lump only); RP-02 electrical architecture (keep-outs only). Wheel family **C** (Ø84 × 24 mm skate + 608) is the **displayed** envelope; A and B remain as labelled alternate solids, not composed into the default assembly.

## Coordinate system

Axle-origin, millimetres. Do not use the RP-01 head origin.

- origin: floor plane, drive-axle ground-contact line, longitudinal centre
- `+x`: forward, toward the front support
- `+y`: robot left
- `+z` (`+h`): up
- drive axle: `x = 0`, `z = 42`
- track: 170 mm
- loaded tyre radius assumption: **42.0 mm** (equals `h_axle`; squash is `U` and gates the shim)

Positive wheel rotation is the sense that produces **+x** chassis velocity. About a wheel axis parallel to `+y`, that sense is **negative** right-hand rotation (top of the tyre moves toward −x, contact pushes +x).

## RP-01 import

Head-local origin: front/bottom centre, `+X` face, `+Y` left, `+Z` up. Yaw demate at `(pitch_x, 0, −60)` ≈ `(−37.965, 0, −60)`. Axes agree, rotation = identity. Translation of the head origin into the chassis frame: **`(37.965, 0, 200)`**, so `F_NECK` is `(0, 0, 140)`. The head is a **mass/interface lump**, not a re-authoring of Layout 03 STEP.

## Live `U` blockers (do not model around)

India 6 V ~176 RPM encoder SKU; D-shaft vs round on the bought wheel; caster trail millimetres; ball `C_rr` / laminate dent; gearbox radial rating; SPI IMU **module** outline; GP2Y optical-axis number (lens-centre figures adopted, ray is not a single number); loaded-radius squash.

## Outputs

Parametric source in `src/`. STEP in `STEP/` (plan `exports/`). Generated dimensions, mass, frames, and checks in `generated/` and `checks/`. Snapshots in `snapshots/`.

Python: `pass-01/.venv` (cadgen 0.5.1). Build: `PYTHONPATH=src .venv/bin/python src/assembly.py`.
