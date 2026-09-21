# RP-04 Observer Protocol

| Field | Value |
|---|---|
| Status | **DRAFT — not frozen.** G03 only. Real Phase B/C clips. No household or mock-video panel |
| Owner | Project builder |
| Created | 2026-09-21 |
| Revised | 2026-09-21 |
| `BD-05` | **SUPERSEDED.** Household instrument-debug panel rejected |

G03 is a scored gate on **measured** composed vs independent-baseline video. It is not a Phase A activity. Acted storyboard, friends-and-family, and virtual playback are not G03 and are not a substitute freeze. `BD-05` (no household/mock panel) is a builder decision, not a literature finding.

Sequence:

```text
engineering tuning on non-scored runs
  → freeze questions, N, pass rule, and clip-selection rule in gates.md
  → capture scored runs
  → select clips by the frozen rule
  → observer scoring
```

Do not tune the composer against the frozen sheet or against scored clips. Non-scored engineering runs may change the composer **before** freeze.

## 1. Purpose

Compare **composed** P-01 (and later P-02/P-03) video against the **honest independent-channel baseline** of the same intent. Questions measure readability of attention and unity of intent, not compliments.

## 2. Stimulus

- Real robot, real channels eligible for that phase. Video only. Builder absent during rating.
- Fixed camera, registered start pose, run ID announced or shown **off the character frame** or cropped in the rated export.
- Eyes in frame. Face channel present (placeholder `E-*` art is allowed).
- If a bench LED or status-light edge is an **engineering timing cue**, it must be **cropped** or placed outside the rated frame. The expressive light that is part of the character may remain visible; it is not the observer’s clock.
- Pair: composed vs independent, labels hidden, order randomized per observer.

## 3. Questions

For each pair, after both clips:

1. In clip A / clip B, which way is the robot attending? (open; coder maps to intended / opposite / unclear)
2. Did that clip read as one reaction or as separate devices? (one / separate / unsure)
3. Did the timing feel deliberate or late/scattered? (deliberate / late / unsure)
4. Forced preference: which clip better matches “wakes and looks for a person as one character”? (A / B / no difference)

No leading “wasn’t that cute” items. Do not mention “composed” or “baseline” in the sheet.

## 4. Scored G03

Part 6 / `gates.md` registers N, pass rule, clip-selection rule, and which performances are in the scored set, **after** non-scored engineering runs and **before** scored capture. P-01, P-02, and P-03 pass separately.

## 5. Literature notes (do not freeze from this)

Detail: [`research/literature.md`](research/literature.md) §5. Q2 is a **custom** construct (entitativity / fluency adjacent), not a Godspeed subscale. Keep Q2 as primary; GQS/RoSAS secondary if used at all (likeability ceiling). 2AFC (Q4) is the form that actually discriminated composed vs naive dispatch in HRI video work. Hide engineering LEDs; builder absent; counterbalance pair order. Video is valid for composition timing; it under-reads social presence. Literature does **not** decide `BD-05`.

## 6. Freeze log

| Version | Date | Event |
|---|---|---|
| 0.1 draft | 2026-09-21 | Questions drafted |
| 0.2 | 2026-09-21 | Household / mock-video panel deleted. G03 waits on real clips |
| 0.3 | 2026-09-21 | Literature notes. Questions unchanged. Still not frozen |
| 0.4 | 2026-09-21 | G03 sequence: tune on non-scored runs, freeze, then scored capture. `BD-05` is a builder decision |
