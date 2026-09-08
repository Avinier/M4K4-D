# Layout 02 — exterior revision brief

Status: **builder approved implementation; generated as [Layout 02](layout-02/README.md)**. The construction brief, STEP, parameter source, mass tree and bounded checks live together there. Fabrication interfaces remain open.

This brief captures the review of [Layout 01](layout-01/README.md). Preserve the chosen yaw → pitch → roll arrangement, A0 balance target, rolling cosmetic ears, separate C2 and removable service assemblies. Layout 01 dimensions and its sampled clearance results do not validate the revised shape.

## Physical dimensions and coordinated height reduction

Use purchased components at **1:1 physical scale**, from the exact model/drawing where available. Distinguish active display area, glass/PCB boundaries, installed connectors, mounting hardware and service space. Scale the reference's visual proportions around those real dimensions; do not resize a camera, display, servo or board to make the shell fit. The perspective reference is an appearance guide, not a dimensioned drawing.

Reduce the excessive top screen bezel **and lower the crown's highest point as part of the same proportion revision**. The builder does not want only the lateral roof lowered while leaving Layout 01's crown at 109 mm. Find the achievable reduction by revising display/camera placement, mounting margins and any useful depth staggering; preserve the selected visible crown. Do not promise an exact new overall height before checking the complete real component stack. The existing 68 mm display-board height and 24 mm camera-board height already consume about 92 mm if stacked without vertical overlap, before gaps, walls and mounts.

## Octagonal silhouette and faceted perimeter

Follow [the full appearance reference](../../../../../visuals/mvp-after-head-servo-archv2.png) and [the builder's close-up](../../../../../visuals/head/front-shell-facets-reference.png).

- Clip all four outer front corners to establish the characteristic octagonal silhouette. Carry this profile coherently through the shell and rear cover.
- Retain **crisp planar facets**. The earlier suggestion of aesthetically softened/rounded shell edges is superseded.
- Between the front face and side shell, provide a **flat sloping perimeter band**, creating two distinct edges: front face → angled band → sidewall. This is a deliberate ridge/bevel treatment in depth, in addition to the four corner cuts visible from the front.
- Clip the four **inner screen-opening corners** only slightly, maximizing exposed screen area. Set the diagonal edges against the actual active-image rectangle and registration tolerances. Keep cuts outside active pixels where the available masked margin permits; do not copy the illustration's larger aperture cuts blindly.
- Continue the stepped inner display surround shown in the reference where it fits, without consuming unnecessary active image area.

## Crown, camera and LED

Narrow the trapezoid base from the generous Layout 01 trial around the actual camera board, removable bracket, optical opening and connector access. The builder accepted a **single front bezel incorporating the crown**, with a separately removable camera bracket behind it. Separate overlapping CAD bodies in Layout 01 do not define a manufactured joint.

Put the LED opening and its complete installed package **within the crown**, rather than straddling the main bezel/crown boundary. Retain it only if it fits the compact crown without undermining service access; the builder authorizes omission if necessary. An LED omission must propagate to its mass/BOM and status-indication records.

## Visible screw construction

Implement the existing [CAD requirements](requirements.md) and [D-04/D-06/D-07 material decisions](../../material-finish-mass-decision.md): real visible M2 button-head screws, correctly sized recessed wells and bosses, and 0.3–0.5 mm panel offsets. Place prominent screw points on the broad perimeter/corner lands as suggested by the reference; determine exact positions from the display keepout, retained material, tool access and attachment loads.

Do not replace metal fasteners with painted dots or turn every visual panel line into a separate service joint. The existing front carrier, rear cover and removable ears supply useful real assembly boundaries. Decorative seams remain integral where no service split is justified. Count visible hardware in its existing mass ownership rather than adding it twice.

## Larger cosmetic ears

Increase the ears' visual presence, using the reference's layered/ridged rim and larger round face rather than Layout 01's plain cylinders. Hollow construction and thinner cosmetic walls are explicitly acceptable. The suggested 55 and 60 mm diameters remain comparison candidates, **not selected final dimensions**; wall thickness also remains to be established.

Retain robust local mounting bosses and the selected rolling attachment. Recompute each carried assembly's mass distribution, inertia and required clearances after the shape revision. Keep the visible outer face intact; review inner reliefs from oblique views as well as neutral front/side views. Prefer light geometry and internal component placement before considering ballast.

## Review output

Show the revised front silhouette, side/depth facets, compact crown with LED disposition, screen exposure, larger ears and visible screw positions. Report revised main-head and crown-inclusive dimensions separately, with remaining fit assumptions. Recheck the changed geometry and supports through combined motion before carrying forward any clearance claim from Layout 01.
