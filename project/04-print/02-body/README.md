# Body prints

The printed parts of [body v1](../../03-build/02-body/v1/BOM.md). This page is started early for one part; the body frame, compute tray, yaw stage and skins are added when phase 2 and phase 3 export (see the [print plan](../README.md#plan)).

Materials and colours are from the [print guide](../../03-build/final/v1/printguide.md#4-colour-scheme). STLs are written from the final CAD with every droid edit; each script checks its meshes before writing the manifest.

| ID | Label in the CAD | Qty | Material, colour | Printer | Orientation | Critical | Settings | Status |
|---|---|---|---|---|---|---|---|---|
| CH-108 | `REAR_BAY_MODULE_PLATE` (D-095: carries the power switch and INA226 behind the rear panel) | 1 | PETG, deep slate | A1 | On its back (−X) face: the counterbores open on the bed, the arms and cradles point up; no supports | Two Ø3.4 M3 holes with Ø6.4 counterbores; cradle rims 0.25 mm round the boards (UNMEASURED outlines: re-check on the received switch and INA226 before printing) | | EXPORTED (2026-11-07, [D-099](../../03-build/decisions.md#d-099)) |

`stl/manifest.json` lists each file, its orientation, size and volume. Exported by `final/v1/cad/export_d095_prints_stl.py` (27/27 checks with CH-106 and CH-107).
