# Makad v1 — photorealistic image-agent prompt

Attach `references/01-front.png` and `references/02-rear.png`, then paste the master prompt below. Generate the baseline first. Use one follow-up at a time, carrying forward the same reference images and accepted baseline. The text is self-contained for agents without repository access.

## Master prompt — faithful baseline

Create a hyperrealistic photograph of **Makad (M4K4-D)**, the small personal droid shown in the two attached CAD reference images, as if its physical parts have been fabricated, finished and assembled. This is an appearance study of this specific build. Preserve its geometry, proportions, assembly, and component placement. Translate the flat CAD appearance into convincing real materials, optical surfaces, lighting and grounded photography.

The first attachment is the current front three-quarter view; the second is the rear three-quarter view of the same robot. Use both to understand the object, but produce **one front three-quarter photograph**, matching the first reference's viewing side and neutral head pose. Show the entire robot, including wheel and caster contact, with breathing room around it. Deliver a single high-resolution image, ideally 2400 × 1600 or higher, with no labels, border, watermark or collage.

### Geometry and scale — preserve these

Makad is approximately **293.5 mm tall in its neutral pose**: a roughly 29 cm floor droid. It has a squat, broad, faceted body and a separately supported, expressive screen head. Its presence is mechanical, approachable and visibly assembled. Let the actual design create its character.

- Two driven side wheels, **84 mm diameter × 24 mm wide**, with **170 mm centre-to-centre track**. This gives approximately 194 mm across the nominal tyre outer faces; that is a wheel scale reference, not a guaranteed maximum envelope of every trim and screw. Preserve the reference's intricate radial wheel geometry, dished faces, clamp rings, dark central hub caps, fasteners and directional tread. Do not substitute generic solid toy wheels or tank tracks.
- A small forward **ball caster**, beneath the protruding nose sensor/touch assembly, provides the third rolling support. Preserve its real ball-in-housing geometry. The dark horizontal slot in the ivory nose cap contains the range-sensor optics. The low rear keel is a separate part, not another wheel.
- Body shell approximately **162.2 mm front-to-back**, maximum belly width **182.2 mm**, and **110 mm shell height**, occupying approximately 30–140 mm above the floor. Preserve the stepped, chamfered shoulders, sloping sides, broad lower belly, panel borders, wheel arches and open wheel clearance.
- A central circular neck turntable approximately **125 mm diameter**, whose top is approximately **155 mm above the floor**, stands 15 mm above the body roof. Keep its tapered rim and real holes. Two separated, faceted charcoal yoke legs rise from this disc to support the head. Preserve their plinths, narrow waists, upper arms, amber spine inlays and the open space between them. Do not replace them with a single cylindrical neck or enclose the gap.
- The head is an angular, chamfered/octagonal housing, **130 mm across the main face and approximately 150 mm across its ear assemblies**. Keep its substantial front-to-back depth, taper toward the smaller rear cover, and planar facets. Preserve the two-part skin seam at ear height and the removable screwed rear cover. Do not turn it into a sphere, soft capsule, or thin tablet.
- The face has one landscape display behind a dark window. The outer mask is approximately **106 × 64 mm**, the clear optical area **99 × 58 mm**, and the active display **95.04 × 53.86 mm**. Preserve the bezel width, clipped corners and screw positions. For this baseline, show an **unlit near-black display behind optical glass**, with a subtle believable reflection. The flat blue-grey CAD fill is a viewport representation, not the intended screen colour.
- Above the display, retain the current **slim camera fin with a trapezoidal front**, one camera lens and a tiny adjacent status-light diffuser. The fin is approximately **44 mm wide near its base**, narrowing to a **34 mm flat top**; its top rises about **18 mm above the main head roof**. The front crown is about **24 mm deep**, and the rear hood slopes down at about **35.5°**. Follow the reference silhouette precisely. This is a small integrated fin, not a tall antenna or a second face.
- Preserve the large side ear assemblies, their ivory outer caps, fine amber inlays, dark inset centres and two visible retaining screws per cap. The caps' actual flattened/cut-away outlines matter; do not replace them with perfect headphone discs or animal ears.
- Preserve the **single exposed round speaker** in the taupe front service panel, including its recessed cup, dark cone and surround. Do not add a grille or the obsolete decorative badge above it. Preserve the four front panel screws.
- At the rear, preserve the taupe service panel, four fasteners, central **red power button with a signal-amber bezel**, flanking vent slots and lower USB-C opening. The side fan grille belongs on the side shown in the rear reference, with a small clear gap above the wheel arch; do not mirror it onto every side. Keep the small microphone apertures at their actual positions.

### Finish specification — apply by part

Treat these hex values as clean base colours under neutral illumination. Keep the differences visible without exaggerating their saturation. Lighting may change highlights and shadows, but it must not recolour the product.

| Parts | Base colour | Real-world appearance |
|---|---|---|
| Body shell, wheel-arch pods, head bezel and camera fin, upper and lower head skins, rear head cover, outer ear caps, nose touch cap | **Ivory #DDD4BA** | Warm, slightly muted ivory; matte ASA housing or matte-painted ASA, fine tactile grain like a good power-tool housing |
| Front and rear body service panels, rear keel and rear sensor bezel | **Taupe #A9A28E** | Warm khaki-grey, clearly darker than ivory; same fine matte housing grain. The keel is finished PETG |
| Wheel-arch upper trim, ear inlays, narrow yoke spine inlays | **Amber #B88636** | Restrained ochre/mustard painted or printed trim; matte, solid colour, non-emissive |
| Rear power-button bezel only | **Signal amber #D39F36** | Slightly brighter safety amber; retain the red purchased button inside it |
| Visible neck turntable and ear dark centres | **Deep slate #4F575B** | Very dark, subtly blue-grey; fine matte metallic casing finish, achievable with paint over printed parts |
| Wheel rims/spokes and clamp rings | **Slate blue #6F8189** | Lighter desaturated blue-grey in the same family; matte metallic finish over PETG, broad restrained highlights |
| Wheel hub caps | **Gunmetal #3A464D** | Dark matte metallic coating over PETG |
| Yoke legs and pivot retainer | **Carbon #2A2C2E** | Raw chopped-carbon-fibre-filled printed polymer, dry fine texture; no woven carbon-fibre checkerboard pattern |
| Tyres | **Tyre black #2B3034** | Black TPU 95A with a rubber-like semi-matte surface and the reference tread |
| Visible screws, nuts and shafts | **Steel #B7BFC0** | Real stainless steel, small crisp highlights; preserve the individual hardware types and locations |

Hidden chassis/body structure is deep-slate PETG; head structural frames are deep-slate PLA; do not change structural materials simply to match the cosmetic skins. These parts should appear only where actually exposed. Genuine aluminium bearing caps are #9DA3A6 and heat-set inserts are brass #C38A47, but do not expose hidden hardware for decoration.

The skin finish is a **fine, even matte grain** informed by textured build plates and restrained fuzzy-skin printing. At normal viewing distance it should read as a carefully finished physical housing. Up close, allow faint manufacturing evidence and tiny layer traces, especially on unfinished composite supports. Avoid coarse sandpaper, oversized extrusion ridges, pitting, and fabric-like texture. Keep mating edges, small ports and screw seats precise and clean.

The slate parts have a bead-blasted/anodised-metal *appearance*, while remaining painted printed parts where specified. Do not make the entire robot metallic. Optical glass, the camera lens, stainless hardware and the speaker surround have their own appropriate reflections; matte housings must not become shiny automotive paint. Use tiny natural edge highlights without rounding away the CAD facets.

### Physical realism and photography

Photograph a freshly completed engineering prototype on a neutral, lightly textured warm-grey floor against a quiet seamless background. Use a large soft daylight-balanced key light and gentle fill, approximately 50–70 mm full-frame-equivalent perspective, with enough depth of field to inspect the whole robot. The front three-quarter view should reveal the face, speaker, nose, one wheel face, opposite wheel where physically visible, ear and neck structure. Keep colour grading neutral and shadows open enough to compare the finishes.

The two tyres and front caster must meet the same floor plane. Use tight contact shadows and believable soft cast shadows. A roughly 2.65 kg assembled engineering estimate informs a small solid object resting under gravity, not a floating toy; do not visibly squash the tyres or bend the supports. Preserve real air gaps and mechanical clearances. Opaque shell panels hide the electronics; remove viewport edge outlines and all CAD overlays without removing physical seams or holes. The open neck space remains open, but do not invent hanging wires to fill it.

This first image is **clean and unweathered** so we can judge colour and texture. A few almost imperceptible handling marks are acceptable. No rust, dirt wash, paint chips or battle damage yet. No extra markings, logos or fictional controls. No dramatic neon rim lighting, orange/teal grading, bloom, lens flares, motion blur or shallow focus that hides the geometry.

The result should be convincing as a photograph of this exact, carefully assembled droid. Geometry fidelity takes precedence over cinematic styling. Check the attachment silhouettes, wheel size, head width, neck gap, trapezoidal camera fin, panels, trim placement and hardware before delivering.

## Follow-up 1 — rear verification

Using the same materials, neutral pose, scale, floor and lighting as the accepted baseline, create one rear three-quarter photograph matching attachment 2. Preserve the screwed ivory rear head cover, open charcoal yoke, taupe rear panel, red button and signal-amber bezel, vent slots, USB-C opening, side fan grille and low taupe rear keel. Make the wheel and caster contacts consistent with the front view. Keep the camera fin facing forward; do not put a lens on its rear. Change only the viewpoint.

## Follow-up 2 — close-up finish inspection

Create a macro photograph of the junction between one ivory wheel arch, its amber upper trim, the slate-blue wheel face, gunmetal hub cap, steel screws and black tyre. Retain the exact reference geometry. Show restrained housing grain, printed-composite/painted-polymer realism, crisp service boundaries and believable rubber-like TPU tread. Use neutral light and enough depth of field to compare finishes. No dirt or added damage.

## Follow-up 3 — gently used droid

Start with the accepted baseline and keep camera, geometry, palette and lighting identical. Add only subtle use: a restrained dark-grey wash in selected seams and screw recesses, tiny handling scuffs, slight amber trim wear, and a trace of floor dust on the tread. Painted polymer chips reveal compatible primer or polymer, not imaginary solid metal. Any silver edge dry-brushing must read as a sparing decorative finish. Keep the display, camera, microphone holes and grille openings clean. Preserve the underlying colours. It is a cared-for working companion, not abandoned machinery.

## Follow-up 4 — controlled colour comparison

Use the clean baseline as the image-edit source. Make three separate images at exactly the same camera, pose, crop, exposure and material texture. Change only the listed finish colours, preserving every colour-to-part boundary. These are aesthetic proposals, not approved build changes. Keep the carbon supports, black tyres, steel hardware, dark optical window, red button and signal-amber safety bezel identical in all versions.

1. **A — print-guide baseline:** all colours unchanged.
2. **B — lighter warm housing:** change ivory skins only to #E7DFC9; retain taupe #A9A28E and every other baseline colour. This tests whether the body should feel brighter while preserving panel contrast.
3. **C — quieter accent:** retain the baseline ivory/taupe/slate colours; change decorative amber only to #A7793A, a more muted bronze-ochre. Keep the rear signal-amber bezel #D39F36 unchanged.

Return separate files named A, B and C if supported; do not put captions onto the robot. Compare identical images side by side outside the generation step. Do not combine a new palette with new weathering or a new environment.

## Follow-up 5 — personality and real-life scale

After the finish has been selected, photograph the same 29 cm droid on a real indoor floor near a chair leg or low workbench for scale. Use soft window light and restrained background detail. Keep the full droid clearly visible and the chosen finish unchanged. Retain the neutral mechanical pose. Activate just two simple, restrained warm-ivory eye shapes within the existing black display, with no mouth or extra hardware; this expression is a temporary visual proposal, not a specified UI. Keep emission low enough to preserve the screen reflections and avoid lighting the entire bezel. The camera lens remains a real separate lens above the screen.

## Correction prompt if the image agent redesigns it

Compare your output with both CAD attachments. Restore the exact head/body proportions, ear outlines, two faceted yoke supports and open gap, raised circular turntable, trapezoidal camera fin, wheel geometry and tread, speaker, front caster/nose, service panels and screw locations. Restore the specified part-by-part palette. Remove invented grilles, arms, antennas, badges, cables, lights and extra wheels. Preserve only the photographic lighting and realistic material rendering from the previous output. Produce one corrected image with the same framing.
