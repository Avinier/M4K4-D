# Purchased-part references

Retrieved for Layout 01 on 2026-09-07. Models are reference geometry, not a servo purchase selection. Preserve upstream geometry; do not resize to force a fit.

| File | Provenance | Observed bounds and use |
|---|---|---|
| `camera-module-3-wide.step` | [STEP-parts exact Camera Module 3 Wide record](https://www.step.parts/parts/raspberry_pi_camera_module_3_wide), sourced there from Raspberry Pi design files | Raw CAD spans 23.862 × 25 × 11.4 mm; retain the published 25 × 24 × 12.4 mm conservative installed-module reservation. The CAD does not establish the optical entrance pupil. |
| `xc330.stp` | [ROBOTIS XC330 eManual](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/), official STEP download no. 1987, resolving to the manufacturer's linked Dropbox `XL,XC-330.stp` | Raw bounds X −10…10, Y −24.5…9.5, Z −22.5…6.5 mm. Total 20 × 34 × 29 mm including supplied protrusions, larger than nominal 26 mm package depth. Output cylinders are coaxial with local Z at X=Y=0. |
| `robotis_xl_xc330_drawing.pdf` | ROBOTIS e-manual "Drawings" download no. 1986, resolving to the manufacturer's Dropbox `XL,XC-330.pdf` (retrieved 2026-09-25), "for reference only", dated 28 May 2020 | Case 20 × 34 × 23 mm; Ø16 × 3 mm horn on the output and on the idler side (29 mm overall); output axis 9.5 mm from the top edge. Horn: 4 × Ø1.6 holes, 3.0 mm deep max, on PCD Ø12, for M2 tapping screws. Case: M2 tapping-screw holes at the four corners of each 20 × 34 face, 16 mm × 30 mm apart, Ø1.6 × 3.5 mm (front) and × 4.5 mm (rear) |
| `robotis_xl_xc330_moment_of_inertia.pdf` | ROBOTIS e-manual "Moment of Inertia" download no. 2136, Dropbox `XL330,XC330 Moment of Inertia.pdf`, released Feb 2023 | Whole-servo rigid-body mass properties, "reference only": XC330-M181 23.0 g, CoG (−0.24, −7.57, −11.18) mm, principal diagonal 3530 / 1797 / 2979 g·mm²; XC330-M288 23.0 g, CoG (−0.23, −7.55, −11.17) mm, diagonal 3529 / 1802 / 2977 g·mm². Housing values, **not** rotor or gear-train inertia. The CoG matches the STEP frame (it lies inside the case, below the output axis); the axes are assumed to be the STEP's |
| `waveshare_esp32_s3_touch_lcd_4_3.stp` | Waveshare "3D Drawing" zip, `files.waveshare.com/wiki/ESP32-S3-Touch-LCD-4.3/ESP32-S3-Touch-LCD-4in3_3D_Drawing.zip` (retrieved 2026-09-24) | Touch variant of the SKU 30493 family: 106.1 x 68.3 x 16.9 mm, 693 solids. Used as the conservative outline for the non-touch SKU 30493. Front glass at STEP Z +4.8; only a 5 mm connector strip on one short edge reaches the full 16.9 mm depth. |
| `waveshare_esp32_s3_zero_v2.step` | `files.waveshare.com/wiki/ESP32-S3-Zero/manual/ESP32-S3-Zero%20V2.step` (retrieved 2026-09-24) | Bare PCB 18.0 x 23.5 mm, 0.8 mm thick, components to +1.14 mm; no USB-C shell or headers in the file. |

**Not stored in Git.** Generated `head-layout.step` and purchased solids (`camera-module-3-wide.step`, `xc330.stp`) stay local. Re-download the purchased files from the provenance links above and verify the checksums below before use. Regenerate the assembly with `python3 head-layout.step.py`.

Camera SHA256: `3c73aaa3091e78f92b0d5d9fa84d6be2389f843a15106f5251a770759ef651df` (catalog checksum verified).

Servo SHA256: `e2f7b060801a1d6a21f23bca2554f29a402f7d73b8498cb201c9e6adf3139eb6`. **Re-verified 2026-09-25:** a fresh download from ROBOTIS download no. 1987 is byte-identical to this file and to `body-chassis/layout-01/references/purchased/robotis_xc330_dummy_assy.step`, the body copy earlier flagged as a third-party mirror. Both repo copies are the official ROBOTIS model (Creo `DC15_A01_DUMMY_ASSY_IDLE_ASM`, 2020-07-27). One model serves the M181 and the M288: they share the case, horns and 23 g mass.

Drawing SHA256: `948b707cb26a64501c03fc45b1a9557b69a554dd5d6934f02e8e6f86cf2b46c2`. Mass-property sheet SHA256: `dacd173dfde3de78effa6ccb94baeea98edf378d63424aa3b26af81adc0c3df2`. Both PDFs are small and are kept in Git.

Catalog searches for `XC330`, `XC330-M288`, `ROBOTIS 330`, `ESP32-S3-LCD-4.3` and `Waveshare 4.3` returned zero results. `Camera Module 3` returned standard, wide and an unrelated camera; the **wide** model was downloaded. `SC0874` returned zero. The official servo model was found after the catalog miss.

Display geometry uses the [Waveshare non-touch drawing](https://docs.waveshare.com/assets/images/ESP32-S3-LCD-4.3-details-size-368725c4e453fa389f729e2b8708ccad.webp) linked by its [product documentation](https://docs.waveshare.com/ESP32-S3-Touch-LCD-4.3). The no-touch glass is about 105.42 × 67.07 mm and its PCB about 106 × 68 mm. The study reserves their conservative union, 106.1 × 68 mm. The documented 6.6 mm face-to-PCB dimension plus rear projections is represented by a 10.6 mm hardware envelope; plugged cables are separate reservations. The earlier baseline's 106.1 × 67.8 mm must not be interpreted as the complete PCB/plug outline.

Camera transformation: local X → head +Z, local Y → head +Y, local Z → head −X; translation (−10.805, −12.5, 81). The inspected lens cylinder axis is at local (14.4, 12.5), giving head optical-axis height Z=95.4. Frontmost CAD surface is X=−2, rear X=−13.4; reserve an additional 1 mm behind it against the published depth. Board connector is on the back; its exit corridor is reserved below/behind the board.

Roll-servo transformation: local X → head +Y, local Y → head +Z, local Z → head +X; local output-axis origin translated to (−84, roll-Y, roll-Z). The supplied frontmost hardware reaches X=−77.5 and rear hardware X=−106.5. Pitch-servo local output axis points +Y, with origin (pitch-X, 47, pitch-Z).

The source imports both models through the CAD cache. The small component-envelope variant in the fit checker intentionally uses conservative boxes rather than the hundreds of camera PCB detail solids. Neither model includes our harness, mounts, finish or manufacturing tolerances.
