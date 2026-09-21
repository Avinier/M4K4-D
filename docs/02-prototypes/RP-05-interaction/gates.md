# RP-05 gates (candidates) — audio share

| Field | Value |
|---|---|
| Status | **Candidates only.** No numeric freeze. No scored run. This file lists *metrics* the audio path will eventually have to support, not pass/fail numbers |
| Owner | Project builder |
| Slice | `RP05-A` does not register gates. Audio candidate metrics map to G01 / G03 / G04 / G05; G02 is a later corpus/NLU slice |

The governing plan already named `RP05-G01…G05`. This paper does not invent a sixth gate and does not fill trial counts, rates, or millisecond ceilings. Those freeze **before** scored data, in a later slice.

## Candidate metrics this slice makes obligatory

| Gate | Audio-relevant metric (not yet threshold) | Inherited obligation |
|---|---|---|
| RP05-G01 Invocation | False reject / false wake / wake latency across speakers, distance, household noise, mechanism noise, **and M4 playback**; rejected invocation leaves sleep unchanged | `AR-15`, `AR-21`, `AR-53` |
| RP05-G02 Core semantics | Out of this slice (corpus/NLU) | — |
| RP05-G03 Lifecycle | Stop/cancel of pending or active playback; no stale-epoch replay; underrun ≠ success | `AR-40`…`AR-45` |
| RP05-G04 Failure | Audio device loss (`F-21`) and service-loss cases produce bounded in-character feedback (`A-fail` or silence) and never bypass local motion safety | `AR-13`, `AR-43`, `AR-44` |
| RP05-G05 Composition | Audible onset vs face/light/head; IR-06 `source_onset` joinable with RP-04 cues | `AR-41`, `AR-74`; RP-04 IR-06 |

Contamination (`AR-60`…`AR-63`) is a measurement the G01 acoustic matrix must include. It is not a separate gate ID.

## Registered section

**Empty.**

Do not put an SPL, a false-wake per hour, a 95th-percentile wake latency, or a duplex isolation dB in this file until the later freeze.
