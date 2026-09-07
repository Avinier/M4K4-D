# Purchased-part references

Retrieved for Layout 01 on 2026-09-07. Models are reference geometry, not a servo purchase selection. Preserve upstream geometry; do not resize to force a fit.

| File | Provenance | Observed bounds and use |
|---|---|---|
| `camera-module-3-wide.step` | [STEP-parts exact Camera Module 3 Wide record](https://www.step.parts/parts/raspberry_pi_camera_module_3_wide), sourced there from Raspberry Pi design files | Raw CAD spans 23.862 × 25 × 11.4 mm; retain the published 25 × 24 × 12.4 mm conservative installed-module reservation. The CAD does not establish the optical entrance pupil. |
| `xc330.stp` | [ROBOTIS XC330 eManual](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/), official STEP download no. 1987, resolving to the manufacturer's linked Dropbox `XL,XC-330.stp` | Raw bounds X −10…10, Y −24.5…9.5, Z −22.5…6.5 mm. Total 20 × 34 × 29 mm including supplied protrusions, larger than nominal 26 mm package depth. Output cylinders are coaxial with local Z at X=Y=0. |

Camera SHA256: `3c73aaa3091e78f92b0d5d9fa84d6be2389f843a15106f5251a770759ef651df` (catalog checksum verified).

Servo SHA256: `e2f7b060801a1d6a21f23bca2554f29a402f7d73b8498cb201c9e6adf3139eb6` (local file hash, not an upstream checksum assertion).

Catalog searches for `XC330`, `XC330-M288`, `ROBOTIS 330`, `ESP32-S3-LCD-4.3` and `Waveshare 4.3` returned zero results. `Camera Module 3` returned standard, wide and an unrelated camera; the **wide** model was downloaded. `SC0874` returned zero. The official servo model was found after the catalog miss.

Display geometry uses the [Waveshare non-touch drawing](https://docs.waveshare.com/assets/images/ESP32-S3-LCD-4.3-details-size-368725c4e453fa389f729e2b8708ccad.webp) linked by its [product documentation](https://docs.waveshare.com/ESP32-S3-Touch-LCD-4.3). The no-touch glass is about 105.42 × 67.07 mm and its PCB about 106 × 68 mm. The study reserves their conservative union, 106.1 × 68 mm. The documented 6.6 mm face-to-PCB dimension plus rear projections is represented by a 10.6 mm hardware envelope; plugged cables are separate reservations. The earlier baseline's 106.1 × 67.8 mm must not be interpreted as the complete PCB/plug outline.

Camera transformation: local X → head +Z, local Y → head +Y, local Z → head −X; translation (−10.805, −12.5, 81). The inspected lens cylinder axis is at local (14.4, 12.5), giving head optical-axis height Z=95.4. Frontmost CAD surface is X=−2, rear X=−13.4; reserve an additional 1 mm behind it against the published depth. Board connector is on the back; its exit corridor is reserved below/behind the board.

Roll-servo transformation: local X → head +Y, local Y → head +Z, local Z → head +X; local output-axis origin translated to (−84, roll-Y, roll-Z). The supplied frontmost hardware reaches X=−77.5 and rear hardware X=−106.5. Pitch-servo local output axis points +Y, with origin (pitch-X, 47, pitch-Z).

The source imports both models through the CAD cache. The small component-envelope variant in the fit checker intentionally uses conservative boxes rather than the hundreds of camera PCB detail solids. Neither model includes our harness, mounts, finish or manufacturing tolerances.
