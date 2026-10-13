# Makad v1 — photorealistic prompt pack

Prepared 2026-10-13 from the current build sources and the 2026-10-12 finish snapshots. This folder contains a prompt and unchanged CAD reference images; **no photorealistic images have been generated yet**.

## Use

1. Upload both images in `references/` to the image creation agent.
2. Paste the **Master prompt** section from [PROMPT.md](PROMPT.md). Start with one clean front view.
3. Check silhouette and part placement before choosing colours. Use the correction prompt if needed.
4. Generate the rear view and material close-up, then try weathering and colour comparisons separately.
5. Save accepted outputs here with descriptive names, for example `baseline-front.png`, `baseline-rear.png`, `finish-closeup.png`, `weathered-front.png`, and `palette-b-front.png`.

Reference images matter: a text-only prompt cannot reliably reproduce this CAD. If an agent accepts actual CAD, the optional geometry input is [the presentation STEP](../../docs/03-build/final/v1/cad/makad-v1-presentation.step), approximately 0.5 GB. Most image agents should receive the PNGs instead. Image generations are aesthetic studies, not dimensionally verified renders.

## Sources and authority

| Source | Used for |
|---|---|
| [Print guide §§2–4](../../docs/03-build/final/v1/printguide.md) | Material assignments, finishes, exact baseline palette, optional weathering |
| [Finish colour rules](../../docs/03-build/final/v1/cad/finish_colours.py) | Current presentation colour-to-part mapping |
| [Final assembly README](../../docs/03-build/final/v1/README.md) | Opaque presentation assembly, excluding inspection overlays |
| [Build decisions](../../docs/03-build/decisions.md) | D-049 composite legs; D-050 faceted supports/disc; D-053 split head skin; D-054/D-056 camera fin; D-055 speaker-panel badge removal and grille clearance |
| [Head dimensions](../../docs/03-build/03-head/v1/cad/dimensions.md) | Face, display, ears, crown and head dimensions |
| [Head motion envelope](../../docs/03-build/03-head/v1/cad/motion-envelope.json) | Body/head datum, raised disc and neutral height calculation |
| [Current body source](../../docs/03-build/02-body/v1/cad/body_v1_model.py) | Wheel scale, body placement, current interfaces |
| [Body dimensions](../../docs/03-build/02-body/v1/cad/generated/dimensions.md) | Shell envelope |
| [Vision](../../docs/00-foundation/vision.md) and [memory](../../MEMORY.md) | Personal droid identity, visibly assembled and repairable character; authority of foundation intent |

The two supplied references are byte-for-byte copies of:

- `docs/03-build/final/v1/cad/snapshots/makad-v1-finish-front_20261012T191514Z.png` → `references/01-front.png`.
- `docs/03-build/final/v1/cad/snapshots/makad-v1-finish-rear_20261012T191531Z.png` → `references/02-rear.png`.

## Interpretation notes

- The print guide remains a **draft**. ASA skins are proposed, CF grade is unresolved, TPU availability requires confirmation, and the lab visit is pending. The prompt visualizes that proposed finish accurately; it does not approve materials or fabricate a release.
- Current head placement: body datum Z140 minus head-local body datum −49.5 gives head origin Z189.5; crown Z104 therefore gives **293.5 mm neutral height**. Disc top: 189.5 − 34.5 = **155 mm**. The word “flush” in a part label must not be interpreted as flush with the body roof. Its actual top is 15 mm proud.
- Some generated chassis reports describe older geometry and inspection colours. The current body envelope, newest decisions and final finish snapshots take precedence. Avoid using the archived concept images already in `visuals/` as geometry references.
- The roughly **2.65 kg** weight is an engineering estimate from the recent decision record, not a measured finished ASA build. The finish guide's mass reconciliation remains unfinished. The prompt uses weight only to cue believable contact and scale.
- Camera and screen glass require realistic optical shading; their CAD viewport fills are not a paint specification. An unlit black display is the neutral baseline. The optional eye graphics are explicitly a proposal.
- The prompt keeps a neutral head pose to make finish comparisons reliable. It does not ask an image agent to reconstruct the compound motion constraints from prose.
- New colour variants B/C, scene lighting and photography choices are proposals authored for this study. They do not alter the build documents or the baseline palette.

## Review before selecting a finish

- Same silhouette and proportions as both CAD views; no changed wheel size, head depth or neck height.
- Two driven wheels and a front ball caster; grounded contacts and unchanged rear keel.
- Actual seams, screw heads, ports, speaker and camera preserved; no invented decorative components.
- Taupe service panels distinct from ivory skins; amber restricted to assigned trim; composite legs charcoal.
- Fine housing grain, matte coated wheel/neck surfaces, raw composite supports, TPU tyres and optical glass remain distinguishable.
- All palette comparisons use the same image conditions. Assess clean colours before adding weathering.
