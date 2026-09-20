# RP-03 pass-01 models

Ugly envelope blockout. Leads are not freezes. No purchase, no ADR-04, no pretty shell.

| Script | Artifact | Description |
|---|---|---|
| assembly.py | STEP/assembly.step | Root, **ball** installed (V1 displayed) |
| assembly_caster.py | STEP/assembly_caster.step | Same mount, **caster** swap |
| axle_frame.py | STEP/axle_frame.step | Open axle frame + aft bulkhead |
| motor.py | STEP/motor.step | Ø28×90 class keep-out |
| wheel.py | STEP/wheel.step | Family C Ø84×24 |
| hub_carrier.py | STEP/hub_carrier.step | Printed 608 carrier |
| motor_clamp.py | STEP/motor_clamp.step | Axle-centred clamp |
| front_mount.py | STEP/front_mount.step | Shared mount + mm scale |
| adapter_ball.py | STEP/adapter_ball.step | Pololu 3-hole adapter |
| adapter_caster.py | STEP/adapter_caster.step | 33×38 caster adapter |
| ball_transfer.py | STEP/ball_transfer.step | D21 class envelope |
| swivel_caster.py | STEP/swivel_caster.step | D20 class envelope, trail U |
| skid_carrier.py | STEP/skid_carrier.step | Adjustable anti-tip catch |
| ballast_bay.py | STEP/ballast_bay.step | Forward-only bay |
| head_lump.py | STEP/head_lump.step | Layout 03 mass/interface lump |

Build from `pass-01/`:

```bash
PYTHONPATH=src .venv/bin/python src/assembly.py
PYTHONPATH=src .venv/bin/python src/assembly_caster.py
PYTHONPATH=src .venv/bin/python checks/write_outputs.py
PYTHONPATH=src .venv/bin/python checks/check_layout.py
```

Wheel families A and B are tabulated in `generated/`, not composed into the default assembly.
