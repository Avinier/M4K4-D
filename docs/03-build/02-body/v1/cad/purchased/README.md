# Purchased references used by body v1

`body_v1_model.py` currently reads vendor STEP files from `02-prototypes/RP-06-cad/body-chassis/layout-01/references/purchased/`. Body parts include the Raspberry Pi 5 and active cooler, ESP32-S3 DevKitC, Robotis XC330 yaw servo, and JST GH headers. The body CAD shares the Adafruit DRV8833 source with chassis v1 only because its current `electronics()` builder creates the whole electronics group before the body view filters out chassis-owned parts.

This directory reserves the same source-reference location used by chassis v1. Do not copy vendor files here without updating their provenance and the import paths in `body_v1_model.py`.
