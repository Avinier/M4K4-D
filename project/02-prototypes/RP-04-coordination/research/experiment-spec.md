# RP-04 remaining research — experiment spec

| Field | Value |
|---|---|
| Status | **Paper pass 2026-09-21.** Virtual HYBRID wait language and P-02 cue list closed 2026-09-21. Trial matrix remains a **draft preregistration**. Not G01/G03. Not ADR-05 |
| Owner | Project builder |
| Closed already | [`trigger-comparison.md`](trigger-comparison.md) — family = `CS-HYBRID` (virtual); [`literature.md`](literature.md) grounds it |
| Does not contain | A second architecture survey; ROS; graph-as-trigger; UART/COBS reopen |

## Compact statement

> Test whether a bounded HYBRID cue list—using scheduled time only for authored perceptual lead and measured source/progress events for causal phase advancement—can execute P-01 and P-02 on physical controllers with bounded interruption, honest degradation, reproducible settling, and better observer-rated unity than independent dispatch. Reopen score representation only if P-02’s discrete hand-off cannot be expressed without ad hoc runtime logic; treat continuous counter-yaw as an executor/control-contract question, not evidence for a graph by itself.

No more architecture-family or middleware research. Remaining work is physical measurement, G03 on real clips, and Phase C P-02 execution after the RP-03 base model. The discrete P-02 list is written and validated; representation stays closed.

---

## 1. Boundary

| In scope | Out of scope |
|---|---|
| HYBRID **tuning**: which source event, quorum, and deadline advance each beat | New scheduler families |
| Cue-list **sufficiency** for P-02 discrete orchestration | Treating counter-yaw as a graph argument |
| Preregistered physical trial matrix and G03 endpoints | Tuning the composer against the observer draft |
| Ablation if G03 is ambiguous | UART, COBS, artwork, speaker quality, wake-word, follow |

Wake advances by **authored phase gates**, not one universal trigger.

---

## 2. Q1 — What should fire the next wake cue?

### 2.1 Working hypothesis (this pass)

| Transition | Recommended trigger |
|---|---|
| Accept → first sign of life | Validated scheduled time for face / light / audio |
| First sign → head rise | First confirmed eligible **visible** onset: face **or** light, with `T-DEAD` |
| Rise → acquire/search | A **named** `HM-03` progress threshold plus a fresh target / no-target decision |
| Acquire/search → settle | Named head hold/search completion, audio silent, and no outstanding cues |
| Any phase → cancellation | Immediate asynchronous epoch flush; never wait for normal progress |

That remains HYBRID tuning. **Adopted and implemented in the virtual composer:** `wait_on = any(face:source_onset, light:source_onset)` plus `deadline_us = T-DEAD` (300 ms from that wait’s intended start). Face-only wait is rejected.

### 2.2 Harness as of 2026-09-21 (software close)

`prototype/p01_harness.py` live path is **HYBRID** only. TIME/PROG adapters remain as frozen evidence.

- C02 face, light, audio: `time` at `FACE_LEAD_US` — matches row 1.
- C03 head rise waits `any(face:source_onset, light:source_onset)` with `deadline_us = T-DEAD` and `on_deadline = degrade`.
- C04 search/acquire waits named `HM-03.rise_commit` **and** a target/no-target decision. Search is the default; `inject=target` takes `HM-05`. Unqualified `progress` is rejected by the validator.
- C05 waits `head:P01-C04:complete` with a deadline.
- Cancel/preempt/restart flush the epoch — matches row 5.
- A missing optional visible channel cannot hang the head: face-denied uses light; light-denied uses face; both-denied degrades at `T-DEAD` / immediately when both alternatives are impossible.

Virtual `TR-P01-DEN-F` / `DEN-L` / both-visible / deadline / cancel-during-wait / stale-after-flush are unit tests in `test_p01_spikes.py`. Physical cells in §5 remain open.

### 2.3 Wait language to test next (still HYBRID)

Not a new adapter. Extend `wait_on` so a progress-tagged cue may name:

| Form | Example | Why |
|---|---|---|
| Single event | `head:P01-C03:complete` | Current harness |
| Alternative | `any(face:source_onset, light:source_onset)` | Head rise if face is denied |
| Conjunction | `all(base:accept, base:eligible)` | P-02 body release |
| Named threshold | `head:P01-C03:progress>=HM-03.rise_commit` | Not unqualified `progress` |
| Deadline | `deadline_us` then `OX-DELAY` / degrade / proceed as registered | Must not hang forever |

Unqualified `progress` is not an admissible physical wait.

Literature ([`literature.md`](literature.md) §4): `any` for optional visible onset; `all` only for required conjunctions; a BT Succeeder (report success from a missing channel) is the named anti-pattern. QLab disarmed cues still elapse waits but do not fire. This is still HYBRID tuning, not a new adapter. `deadline_us` is `T-DEAD` from the wait’s intended start, not `T-BEAT` and not `T-BEAT + 300 ms`.

**Falsify this wake trigger** if an allowed single-channel denial stalls a channel the degraded score still requires. Virtual `test_deny_face_still_rises_on_light` / `test_deny_light_still_rises_on_face` do not currently falsify it. Physical `TR-P01-DEN-F` / `DEN-L` remain required.

---

## 3. Q2 — Cue-list sufficiency for P-02

## 3. Q2 — Cue-list sufficiency for P-02

P-02 discrete list is written in `situations.md` §12 and `prototype/score.py`. **Graph not opened.** Physical P-02 and the `counter_yaw` implementation still wait on Phase C and `BD-08`.

| # | Criterion | Paper verdict this pass | Graph? |
|---|---|---|---|
| 1 | Conditional target-sector branching (in-sector vs behind-body) | Two named score variants in `situations.md` §12 | No |
| 2 | Acceptance gates (“C3 accepted and remains eligible”) | `all(base:accept, base:eligible)` on `counter_yaw`; `all(base:eligible, core:target_decision)` before `BM-05` | No |
| 3 | Named progress thresholds | `HM-10.curious_hold`; validator rejects unqualified `progress` | No |
| 4 | Conjunctions or alternatives between events | Same wait language as §2.3 | No |
| 5 | Deadlines and fallback/degrade branches | Every external wait has `T-DEAD` and a named overlay/panel fallback | No |
| 6 | Cancellation from measured intermediate state | Score fallbacks `HM-18` / `BM-12`; epoch flush | No |
| 7 | Parameterized counter-yaw | Named primitive `counter_yaw(base_yaw)` on the behind-body list. **`BD-08` still open** before implementation | **No** |

**Reopen representation** only if P-02’s *discrete* hand-off requires runtime score mutation, polling loops, or special-case code outside the score. A graph will not itself solve counter-yaw.

Physical P-02 waits on Phase C (RP-03 G01/G02/G06). Paper sufficiency is closed: the list plus one named primitive did not require ad hoc runtime logic. No virtual executable P-02 spike until the RP-03 base model exists.

---

## 4. Q3 — Falsification

| Conclusion | Killed by |
|---|---|
| Current wake trigger (face-only wait) | **Virtual closed.** Physical: allowed single-channel denial stalls a channel the degraded score still requires |
| Time-tagged cues | Clock uncertainty or late execution exceeds the **frozen** phase window; or scheduled work runs when the time model is invalid |
| `CS-HYBRID` as composer | Cancellation / preempt leaves any stale visible or acoustic beat (old epoch cue onsets after flush) |
| Cue-list representation | P-02 discrete hand-off needs runtime score mutation, polling, or special-case code outside the score |
| ADR-05 close | Composed is mechanically valid (G01/G02/G04/G05) but does not outperform the independent baseline on the **primary** G03 endpoint |

Failed, aborted, and degraded runs stay in the record.

---

## 5. Q4 — Physical trial matrix (draft preregistration, not run)

Not frozen. Freeze **N**, numeric thresholds, injection magnitudes, and clip/run selection rules in `gates.md` before scored data. Until then this table is a draft cell list.

Every scored cell records: start pose, power/battery class, software/firmware/score/architecture versions, timebase validity, overlay IDs, cold vs warm, `run_id`. Report **every run** plus median and range. Add a percentile (p95 / p99) only when the frozen `n` supports it. Do not promise p99 from this draft. Virtual onsets are not G01 `W`.

`n` and consecutive-run count wait `BD-06` / Part 6. Do not fill them after seeing data.

### 5.1 P-01 (Phase B — first physical object)

| ID | Condition | Inject | What it answers |
|---|---|---|---|
| `TR-P01-NOM` | Composed HYBRID, all five channels | none | Nominal G01 |
| `TR-P01-IND` | Independent immediate dispatch, same panels/pose | none | G03 pair / ablation A |
| `TR-P01-DLY` | Late head onset past phase window | `OX-DELAY` | Wait vs desync |
| `TR-P01-CLK` | Invalid or late time model | `OX-TIME` | Time-tag NACK; progress continues |
| `TR-P01-STK` | Head progress stuck | stuck `HM-03` | Search must not fire on the clock |
| `TR-P01-CAN-PRE` | Cancel before head onset | `OX-CANCEL` | No rise, no search |
| `TR-P01-CAN-MID` | Cancel during rise | `OX-CANCEL` | `HM-18`; no `HM-04/05` |
| `TR-P01-CAN-SET` | Cancel during settle/search | `OX-CANCEL` | No leftover beat |
| `TR-P01-PRE` | P-02 intent during search | `OX-PREEMPT` | New epoch; gaze lead; no search-success log |
| `TR-P01-DEN-F` | Face denied | `OX-DENY(face)` | Light/head/audio continue; no claimed face onset |
| `TR-P01-DEN-L` | Light denied | `OX-DENY(light)` | Face quorum still advances head |
| `TR-P01-DEN-A` | Audio denied | `OX-DENY(audio)` | Visual/head wake; silence |
| `TR-P01-INH` | Base inhibited | `OX-INHIBIT-BASE` | HOLD; P-01 still valid |
| `TR-P01-STL` | Stale epoch cue after flush | `OX-STALE` | Reject; no local start |
| `TR-P01-RST` | C2 or C0 restart mid-rise | `OX-RESTART` | No epoch-1 resume |
| `TR-P01-COLD` | Documented cold start | none | G05 input |
| `TR-P01-WARM` | Immediate repeat from same config | none | G05 input |

`TR-P01-DEN-F` is closed as a **virtual** unit; it remains a physical G04 cell.

### 5.2 P-02 / P-03 (Phase C — same shape, not runnable now)

Same nominal / independent / delay / stall / cancel-pre / cancel-mid / cancel-set / deny-base / inhibit / restart / cold / warm cells. P-02 adds:

| ID | Extra cell | Why |
|---|---|---|
| `TR-P02-SEC` | In-sector target, base HOLD | Head-only path |
| `TR-P02-BHD` | Behind-body, C3 accepts | Hand-off + counter-yaw primitive |
| `TR-P02-BHD-NACK` | Behind-body, C3 denies | Full P-02 denied; not a fake orientation |
| `TR-P02-ABL` | HYBRID timing, counter-yaw/hand-off **off** | Ablation B |

P-03: inhibit-base and deny-base **deny the spin**; a head-only flourish is not P-03 success.

---

## 6. Q5 — G03 endpoints

G03 uses **real** Phase B/C clips against the independent baseline. Virtual playback, acted mocks, and household dry-runs are not G03. `BD-05` (no household/mock panel) is a **builder** decision, not a literature finding.

**Primary endpoint (freeze in `gates.md` with N, pass, and clip-selection, after non-scored engineering runs, before scored capture):** “Did that clip read as one reaction or as separate devices?”

This wording is a **custom** construct, not a Godspeed/RoSAS subscale. Adjacent literature that actually discriminated composed vs naive dispatch: 2AFC / forced preference; fluency/cohesion; attention-direction. Godspeed likeability/intelligence ceilings after a friendly demo — keep GQS **secondary**. Detail: [`literature.md`](literature.md) §5.

**Secondary (report, do not let them rescue a primary fail):** attention-direction correctness; deliberate vs late/scattered timing; forced preference vs independent.

Sequence (do not invert):

```text
engineering tuning on non-scored runs
  → freeze questions, N, pass rule, and clip-selection rule
  → capture scored runs
  → select clips by the frozen rule
  → observer scoring
```

Part 6 / `gates.md` must register, **before** scored capture:

| Item | Rule |
|---|---|
| N and pass | Register with the gate. Not a friends-and-family majority |
| Minimum meaningful improvement | Composed beats independent on the **primary** endpoint by a stated margin or test; “no difference” is not a pass |
| Clip/run sampling | Frozen rule: which physical `TR-*` runs become clips; one clip per condition version |
| Counterbalancing | Pair order randomized per observer; labels hidden |
| Exclusion | Incomplete sheets; builder present; engineering LED visible in rated frame; eyes not in frame |
| Pooling | **P-01, P-02, and P-03 pass separately.** Do not pool to hide a fail |

Do not tune the composer against the frozen sheet or against scored clips. Non-scored engineering runs may change the composer **before** freeze.

---

## 7. Q6 — What “better” attributes to

Keep the all-channels-immediately baseline (`BD-02`). If G03 (or G01 vs baseline timing) is ambiguous, run the diagnostic ablation:

| Arm | What it is | Answers |
|---|---|---|
| A | Same panels, independent immediate dispatch | Is the composed system better at all? |
| B | HYBRID timing; counter-yaw / body hand-off **disabled** | Did the gain come from timing alone? |
| C | Full HYBRID composition | Timing + hand-off / counter-motion |

P-01 has no counter-yaw: A vs C is enough. P-02 needs A/B/C. Do not treat a prettier choreography that uses different panels as a win.

---

## 8. This pass (2026-09-21 software close)

| Finding | Class | Follows |
|---|---|---|
| Architecture family is closed: virtual `CS-HYBRID` | Decided | `trigger-comparison.md`; literature **supports the taxonomy**; exact-one-trigger is Makad’s |
| Wake uses `any(face, light)` + `T-DEAD` | **Implemented** in the HYBRID harness | `p01_harness.py`; TIME/PROG retained |
| Face-deny / light-deny no longer stall head rise | Virtual closed | `test_deny_face_still_rises_on_light`; `test_deny_light_still_rises_on_face`. Physical `TR-P01-DEN-F` / `DEN-L` remain |
| Cue list is sufficient for P-02 discrete orchestration | Paper closed | `situations.md` §12; `score.py` validator. No graph. No executable P-02 spike |
| Counter-yaw is an executor primitive, not a representation argument | Paper + literature | §3 #7; **`BD-08` before implementation** |
| Split `T-LEAD` / `T-BEAT` / `T-DEAD` | Literature `E`; harness uses `T-DEAD` | `T-DEAD` = 300 ms from the wait’s intended start |
| Exploratory packed codec layout revision 2 | Host reference | RP-02 `phase-a/`; `BASE_STATE` 62 bytes with safety fields. Not G04/G05. Lateness window numeric still open |
| Trial matrix | Draft preregistration | Freeze N, thresholds, injections, selection before data |
| `start_at_us` semantics accepted (`RP02-P4-REG-03`) | Inherited | Physical TIME tags still need G05 |
| No physical `W`; G03 not run | Open | §§5–6 |

Next executable research steps, in order:

1. Physical `TR-P01-*` when the head, D1, timebase, and audio stand-in exist. Engineering tune on non-scored runs; freeze G03 N/pass/clip-selection; then capture scored clips.
2. Close `BD-08` before implementing counter-yaw. Executable P-02 after the RP-03 base model.
3. P-02/P-03 and ablation B when the base is eligible.

RP-04 remains **blocked on Phase B/C evidence**. This file does not close ADR-05.

---

## 9. Non-goals

No second family comparison. No ROS. No UART/COBS ownership move. No G03 from this paper pass. No ADR-05 from this file.
