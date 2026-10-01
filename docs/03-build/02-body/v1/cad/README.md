# Body v1 CAD

This directory follows the chassis v1 CAD layout: an editable model and STEP entry point at the root, `generated/` for derived reports, `snapshots/` for review images, and `purchased/` for vendor-reference provenance. Subsystem folders are added when a body component has its own model. The current body is one scoped assembly, so its source remains in the root.

| Path | Purpose |
|---|---|
| `body_v1_model.py` | Geometry, dimensions, labels, and the body/chassis scope boundary. |
| `body-v1.step.py` | CADgen build entry point for `body-v1.step`. |
| `body-v1.step` | Derived body assembly; ignored by Git and regenerated from source. |
| `write_outputs.py` | Writes body dimensions, frames, and a partial body mass-register report to `generated/`. |
| `purchased/` | Provenance and current import locations for vendor STEP sources. |
| `snapshots/` | Dated images from STEP review. |

Build with the project's CAD Python environment from this directory:

```bash
python body-v1.step.py
python write_outputs.py
```

The view includes the body frame, shell, service panels and their internal frames, panel hardware, speaker, microphones, compute tray, Raspberry Pi 5 and cooler, C3 carrier/DevKitC, power-distribution boards, yaw stage, internal wiring, and body connector/plug reserves. It uses the body/chassis boundary from chassis v1: the battery pack, the ATOF main-fuse holder envelope (CH-028), Adafruit drive boards, deck IMU, GP2Y front range sensor, concealed nose contact assembly, motor wiring, rear TCRT wiring, and chassis connector reserves stay with chassis v1 and are filtered out here.

The separate head assembly is not part of the body enclosure. Its body-side yaw drive and body-side head wiring are included. This is a subsystem review model, not a fabrication release. The model still depends on purchased STEP files in the prototype and chassis directories; see `purchased/README.md`.
