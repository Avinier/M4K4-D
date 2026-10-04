# Purchased references used by body v1

`body_v1_model.py` currently reads vendor STEP files from `02-prototypes/RP-06-cad/body-chassis/layout-01/references/purchased/`. Body parts include the Raspberry Pi 5 and active cooler, ESP32-S3 DevKitC, Robotis XC330 yaw servo, and JST GH headers. The body CAD shares the Adafruit DRV8833 source with chassis v1 only because its current `electronics()` builder creates the whole electronics group before the body view filters out chassis-owned parts.

This directory reserves the same source-reference location used by chassis v1. Do not copy vendor files here without updating their provenance and the import paths in `body_v1_model.py`. The photo-derived SparkFun button below is imported by `power_button_mushroom()` in the body v1 assembly.

## Files in this folder

| File | Part | Source | SHA-256 |
|---|---|---|---|
| `infineon_pg_llga_5_4.stp` | Infineon IM73D122V01 MEMS microphone package (PG-LLGA-5-4), 4 × 3 × 1.30 mm body (1.31 with logo faces); pads on Z 0, lid +Z, sound port ring at local (+0.68, 0) | Infineon package page, [`Infineon-PG-LLGA-5-4_3D_STP-Package-v03_00-EN.stp`](https://www.infineon.com/assets/row/public/packages/73/3d_model/infineon-pg-llga-5-4-3d-stp-package-en.stp), downloaded 2026-10-03; internal name `PG-LLGA-5-3_Z8B00214464_V09_3D.stp` | `1ebf2602a7ce46fc213b2a6e84040cbe7ff26c0ca31dbd28c2581ae6d1f873f9` |
| `sparkfun_com_31041_mushroom_red.step` | SparkFun COM-31041 / Tanotis 7447052877909, 16 mm red momentary mushroom pushbutton | Parametric `sparkfun_com_31041_mushroom_red.step.py`, reconstructed from six product photographs supplied by the builder and the [SparkFun product listing](https://www.sparkfun.com/16mm-metal-push-button-switch-mushroom-head-red.html). No manufacturer mechanical drawing was available. | Locally generated; see source |

`body_v1_model.py` imports it with `BODY_V1_PURCHASED / MIC_PACKAGE_STEP`. It drops the zero-volume logo faces and fuses the embedded pads into the substrate, so each mic is one solid with the vendor outline. The datasheet (Fig. 12, 13) confirms the 0.68 mm port offset; the datasheet height is 1.2 ± 0.1 mm against the STEP body's 1.30 mm.

### SparkFun button model limits

SparkFun confirms a nominal 16 mm threaded mount, a normally open momentary contact, two screw terminals, and the supplied nut and gasket. The photo model estimates the Ø25.2 mm mushroom, 20 mm nut across flats, 9.0 mm projection above the mounting face, and 23.8 mm depth including screw heads. It uses the gasket's panel-contact face as Z=0, with the button toward +Z. Thread crests are visual approximations and do not define a real thread form. Verify the head diameter, rear depth, nut size, and panel fit against a physical sample before release.
