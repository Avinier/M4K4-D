# RP-03 CAD pass 1

Ugly, adjustable envelope model of Concept A. **Not a SKU freeze, purchase, pretty shell, G01–G06 claim, or ADR-04 closure.**

[Ball assembly](http://127.0.0.1:3246/?file=STEP/assembly.step) · [Caster swap](http://127.0.0.1:3246/?file=STEP/assembly_caster.step) · [brief](brief.md) · [dimensions](generated/dimensions.md) · [checks](generated/checks.md)

## What this is

An axle-origin blockout so every scored geometric question can be measured and every adjustable dimension can actually be adjusted. Displayed pose:

| Datum | Displayed | Band (still adjustable) |
|---|---|---|
| Track / axle | 170 / 42 mm | fixed by baseline |
| Wheel family | **C** Ø84 × 24 mm + 608 | A and B tabulated, not composed |
| Front contact `x` | 110 mm | 105–115 |
| V1 support | ball class envelope, shim 13 mm | caster swap shim 4 mm, same `x` |
| Skid | 72 × 12 mm | 60–80 reach, 8–16 height |
| Battery CoM | x=+65, z=25 | must stay x>0 |
| Head | Layout 03 lump 509 g | identity rotation, origin (37.965, 0, 200) |

## Tree

```
pass-01/
  brief.md
  src/                 # parametric models (plan: source/)
  STEP/                # generated (plan: exports/)
  generated/           # dimensions, mass, physics, U register
  checks/              # write_outputs.py, check_layout.py
  references/evidence.md
  snapshots/           # review views
```

Python: `.venv` with cadgen 0.5.1. From this folder:

```bash
PYTHONPATH=src .venv/bin/python src/assembly.py
PYTHONPATH=src .venv/bin/python src/assembly_caster.py
PYTHONPATH=src .venv/bin/python checks/write_outputs.py
PYTHONPATH=src .venv/bin/python checks/check_layout.py
.venv/bin/cadgen step snapshot --job snapshots/snapshot-job.json
```

## Checks that ran

- Layout script: all listed rows OK. Drive mass 573 g (band 200–600). `a_tip` +3.15 m/s² at scored CoM (paper, not a gate). Skid inequality holds at displayed 12/72. Battery xmin = +31 mm. Contact `x` identical ball/caster.
- `cadgen step inspect validate` on `STEP/assembly.step`: ok, 154 occurrences, 0 failures.
- `refs --facts`: bbox 246 × 205 × 307 mm, centre (39, 0, 150.5). Width matches the 205 mm bumper span. Height is the 304 mm stack plus triad/pad. Depth **exceeds CON-14 180 D** (cliff 40 mm ahead of contact + skid reach) — reported HOLD, not silently shrunk.
- Snapshots: iso, iso-opposite, side, front, top, underside, plus caster iso.

## Do not read as

A freeze of `D02` / `D21` / `DRV-B` / `S01`/`S04`/`S06`/`S07`. A 14/70 skid. A 21 mm tyre. Averaged stall current. A pretty chassis. Integrated CAD (RP-06).
