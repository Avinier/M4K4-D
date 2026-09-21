# RP-04 executable prototype

| Field | Value |
|---|---|
| Status | Part 5 spikes run 2026-09-21. **Selected adapter: `CS-HYBRID` (virtual only).** TIME/PROG retained as frozen evidence. Not G01/G03 |
| Owner | Project builder |
| Tests | `python3 -m unittest test_p01_spikes -v` (9 tests, pass) |

Phase 3 shortlisted TIME / PROG / HYBRID. This folder is one event schema, one virtual C2/C3/D1/audio, three **thin** trigger adapters in [`p01_harness.py`](p01_harness.py).

TIME models `start_at_us` without waiting on RP-02.

## Selection (rule in `research/README.md`)

All three passed shared invariants. Discriminating results:

| Injection | TIME | PROG | HYBRID |
|---|---|---|---|
| Late head | delay logged | delay logged | delay logged |
| Invalid time | all scheduled cues NACK | no time NACK | time-tagged cues NACK |
| Stuck head progress | still dispatches `P01-C04` | no `P01-C04` | no `P01-C04` |
| Restart | no epoch-1 head resume | same | same |

**Select `CS-HYBRID`** for the live virtual composer: P-01 needs an authored face/light lead (time tag) and a head chain (progress tag). At selection time TIME was also penalized by IR-03 still unaccepted; `RP02-P4-REG-03` later accepted `start_at_us`. TIME still wipes the score on `OX-TIME`. PROG cannot express the lead without becoming HYBRID. Demo polish was not used.

## Frozen evidence — do not delete

[`EXPERIMENTAL.md`](EXPERIMENTAL.md). Adapters `TIME` and `PROG` stay in `p01_harness.py` and `test_p01_spikes.py`. They are not the live composer.

## Out of scope

UART, ROS, P-02/P-03 as comparison object, G03 clips from this model.
