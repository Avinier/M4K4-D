# Head packaging estimates

Recorded: **2026-09-07**, from the fitting discussion and its component-dimension research. Status: **layout inputs and estimates; no CAD fit proof**. Use [decisions.md](decisions.md) for choices and [requirements.md](requirements.md) for inherited CAD requirements.

## System envelope

The [dimensional baseline](../../../../01-system/dimensional-baseline.md) remains the authority. Values below are a working extract; revise this extract if that source changes.

**Camera-crown update, 2026-09-07:** [HEAD-CAD-06](decisions.md#head-cad-06--camera-crown-and-continuous-bezel) selects an upward trapezoidal protrusion at the camera, integrated into the head shell and continuous bezel. The figures below predate its dimensioned layout. Include the crown in total head height and swept clearance, then revise shell/finish, camera-mount mass and per-axis properties. Its dimensions and any resulting revision to the earlier head-height band are not yet established.

| Item | Current input |
|---|---|
| Complete head, including side pods | Nominal **95 H × 150 W × 115 D mm**; validation band 90–100 H × 145–155 W × 110–120 D mm |
| Head core | Approximately 95 H × 125–130 W × 110–115 D mm |
| Neck | 60 mm vertical allocation; approximately 35–45 mm visible, with head/body intrusion allowed |
| Selected display | Waveshare ESP32-S3-LCD-4.3, no-touch SKU 30493; baseline 106.1 × 67.8 mm module, 95.04 × 53.86 mm active image |
| Selected camera | Raspberry Pi Camera Module 3 Wide, visible-light/IR-cut SC0874; 25 × 24 × 12.4 mm |
| Head mass | Approximately 490 g **pre-M008 planning lower bound** at 1.2 mm PLA; required C2 assembly additional, actual complete and per-axis masses unknown |

The display's current [manufacturer drawing](https://docs.waveshare.com/assets/images/ESP32-S3-LCD-4.3-details-size-368725c4e453fa389f729e2b8708ccad.webp) shows an approximately 106 × 68 mm board and a 6.6 mm front-to-PCB stack with additional rear projections. Those rounded drawing values do not silently replace the repository baseline, and **6.6 mm is not the installed depth with connectors and access**. Confirm the received no-touch revision. Camera dimensions are published on the [Raspberry Pi product page](https://www.raspberrypi.com/products/camera-module-3/?variant=camera-module-3-wide).

## Candidate servo envelopes

These are sourced package references, not chosen actuators. Manufacturer axis labels describe the servo body; orient each drawing by its output shaft before placing it in head coordinates. Mounts, horns, couplers, plugs and cable exits require additional space.

| Reference | Published nominal package | Published mass | Layout use |
|---|---|---|---|
| [ROBOTIS XL330-M288](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/) | 20 × 34 × 26 mm | 18 g | Small X330 comparison envelope |
| [ROBOTIS XC330-M288](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/) | 20 × 34 × 26 mm | 23 g | Initial coaxial roll reference; 26 mm along the output-axis depth |
| [ROBOTIS XC430-W240](https://emanual.robotis.com/docs/en/dxl/x/xc430-w240/) | 28.5 × 46.5 × 34 mm | 65 g | Larger roll-package sensitivity case |
| [Feetech STS3215 family](https://www.feetechrc.com/products.html?keyword=STS3215) | Approximately 45.2 × 24.7 × 35 mm nominal | Approximately 55 ± 1 g, variant dependent | Exact sourced SKU/drawing must be matched before use |

The inspected [Feetech ST3215-C046 manufacturer datasheet](https://files.seeedstudio.com/products/Feetech/101090142_Feetech_ST-3215-C046_Datasheet.pdf), dated 2025-04-15, shows a 45.23 × 24.73 mm outline and **36.5 mm full axial outline** on page 6. The C046 trial below uses 36.5 mm, rather than treating the 35 mm family body dimension as the complete axial envelope. Do not transfer C046 dimensions or performance to another STS/ST3215 variant without checking its drawing.

Published masses are not installed measurements. The current mass model already has a 35 g provisional allowance for moving actuator hardware; **replace** that allowance with the actual owned masses. Include the complete pitch and roll servo housings in the upstream joints that carry them.

## Initial coaxial roll depth stack

This is a one-dimensional planning sum, not a collision check. The front-to-back allowances are provisional except for the referenced servo package; camera placement, pitch hardware, connectors and service space can change the result.

| Region | Initial allowance | Trial range | Basis |
|---|---:|---:|---|
| Window/display/front mounting | 18 mm | 12–18 mm | Estimated installed front assembly |
| Bay behind front assembly | 15 mm | 15–25 mm | Estimated space for routing and local components |
| Roll flange and bearing cartridge | 30 mm | 30–36 mm | Trial support package; bearing centres approximately 20–25 mm apart |
| Short coupling | 10 mm | 8–12 mm | Estimated; no coupling selected |
| X330 servo along output axis | 26 mm | 26 mm | Referenced servo envelope |
| Rear shell and clearance | 6 mm | 4–6 mm | Estimated |
| **Total** | **105 mm** | **95–123 mm** | Sum of the assumptions above |

The point estimate leaves an arithmetic **10 mm** against the nominal 115 mm head depth. That is not demonstrated usable clearance: the trial range extends beyond the 120 mm validation band, and this sum does not place every component.

Holding the other allowances fixed gives **113 mm** with the XC430's 34 mm axis-depth package or **115.5 mm** with the C046 drawing's 36.5 mm outline. These are sensitivity comparisons, not claims that either complete servo installation fits. No bearing diameter, support stiffness, coupling fit or pitch-servo pocket has been established.

## Layout evidence still needed

1. Place exact component envelopes, output-axis locations, mounting holes, connector exits and the C2 board.
2. Lay out the load-bearing roll cartridge, pitch pivots/yoke and body-fixed yaw support with assembly/tool access.
3. Implement the builder-selected face-attached rolling ears and check combined-motion clearance for the head, ears, yoke, body and cable guides.
4. Assign each physical part once in the mass ledger and to each joint that carries it; calculate per-axis mass, 3D centre of mass and inertia.
5. Feed those results into the existing actuator and prototype evidence process before selecting hardware or freezing geometry.

These are next-layout checks, not completed work. The exact fasteners, printed fits, bearings, controller and cable geometry remain open.

The [pre-layout brief](pre-layout-brief.md) connects these envelopes to RP-01's existing mass estimates, pivot candidates and internal arrangement proposal.
