# Frozen comparison adapters

Status: **experimental / frozen 2026-09-21** after `RP04-P5-REG-01`.

`CS-TIME` and `CS-PROG` are not the live composer. They remain in [`p01_harness.py`](p01_harness.py) (`Adapter` `"TIME"` / `"PROG"`) and [`test_p01_spikes.py`](test_p01_spikes.py) as the evidence that `CS-HYBRID` was selected. Do not delete the adapters, tests, or this note to tidy the tree.

Live maintenance: `HYBRID` only, plus shared `Sim` invariants.
