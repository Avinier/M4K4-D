# RP-03 CAD

| Field | Value |
|---|---|
| Status | **Reserved.** No blockout until a concept is frozen |
| Rule | `../plan.md` §10: RP-03 does not produce final chassis CAD. `base/` is a blockout for the *selected* concept only. Root `cad/` stays reserved for integrated CAD |

Concept A chassis and sensing (three look-downs, analog-IR in the stop path) plus **`D21` ball transfer** is the **selected installed path** in `../concepts/README.md` and `../decision.md` BD-08. The caster stays the required swap. That is not a gate freeze. Do not start a pretty chassis from the lead.

Pre-blockout research lives in [`../research.md`](../research.md) §1.5 (print vs buy) and §5 (filled datums, 2026-09-19). Three CAD-critical mismatches: axle 42 mm vs 1″ ball ~29 mm vs 30 mm caster ~38 mm; Ø84×21 not a stock article; D02 encoder 176 RPM suffix not listed in India. **Print hubs, shims, and the two front-support adapters. Buy the tread, the POM ball, and the import encoder motor.** Filled envelopes may feed a later ugly model. They do not authorize a SKU freeze, an FDM tyre freeze, or a pretty shell.

When a freeze exists, this folder holds the ugly-rig blockout: Ø80–85 wheels at 170 mm track, adjustable 105–115 mm front support **with 0–15 mm height shim**, interchangeable ball / caster **via two adapters**, adjustable skid, ballast that sets mass and both CoM coordinates independently. Not a mini-droid.
