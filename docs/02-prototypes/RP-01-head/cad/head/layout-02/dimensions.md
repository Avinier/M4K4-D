# Layout 02 dimensions

Generated from [`write_dimensions.py`](write_dimensions.py) against the current parametric model. **Layout 02 logging only** — not a fabrication drawing, not a freeze, and not Layout 03 geometry.

| Field | Value |
|---|---|
| Pose | Neutral |
| Units | mm |
| Frame | +X forward (face), +Y robot-left, +Z up; origin front/bottom centre |
| Assembly box | 115 × 150 × 162 (X -115.0…0.0, Y -75.0…75.0, Z -60.0…102.0) |
| Machine-readable | [dimensions.json](dimensions.json) |

Mass and CoM stay in [mass-placement.json](mass-placement.json). Refresh both after geometry changes.

## Datums

| Datum | Point (X, Y, Z) | Direction |
|---|---|---|
| Roll axis | 0, -1.06, 46.67 | +X |
| Pitch axis | -39.4, 0, 45.32 | +Y |
| Yaw axis | -39.4, 0, -60 | +Z |

## Envelope constants

| Item | Value |
|---|---|
| Main shell H × W × D | 86 × 130 × 115 |
| Crown-inclusive height | 102 |
| Skin thickness | 1.2 |
| Ear diameter / centre | Ø60 at X -43, Z 42, Y ±66.5 |
| Display board Z | 6…74 |
| Camera board Z | 75…99 |
| Camera–display vertical gap | 1.0 |
| Roll bearing centres X | −43 and −65 (22 spacing) |

## Yoke length (Layout 02 as modelled)

| Segment | mm | Role |
|---|---:|---|
| Pitch axis above head bottom | 45.321 | A0 / elevated ear-pivot; do not shorten by dropping the axis |
| Visible yoke below head bottom | 32 | Knee at Z −32; visible neck / look-up clearance |
| Pitch axis to knee | 77.321 | Structural leg length in this model |
| Yaw interface Z | -60 | 60 mm neck allocation |

Yoke-leg length changes belong to [Layout 03](../layout-03-brief.md), not this file.

## Purchased / 1:1 envelopes

| Part | Frame | Owner | Size (ΔX × ΔY × ΔZ) | Box min | Box max |
|---|:---:|:---:|---|---|---|
| `active_display_95_04x53_86` | R | M002 | 0.2 × 95.04 × 53.86 | -3.75, -47.52, 13.07 | -3.55, 47.52, 66.93 |
| `display_module_1to1_envelope` | R | M002 | 10.6 × 106.1 × 68 | -14.4, -53.05, 6 | -3.8, 53.05, 74 |
| `camera_module_3_wide_1to1` | R | M005 | 12.4 × 25 × 24 | -14.4, -12.5, 75 | -2, 12.5, 99 |
| `C2_ESP32_S3_Zero_23_5x18_footprint` | R | M008 | 1.6 × 18 × 23.5 | -26.6, -38, 28 | -25, -20, 51.5 |
| `roll_XC330_1to1_reference` | P | M013-15-roll | 29 × 20 × 34 | -106.5, -11.06, 22.17 | -77.5, 8.94, 56.17 |
| `pitch_XC330_1to1_reference` | Y | M013-15-pitch | 34 × 29 × 20 | -63.9, 17.5, 35.32 | -29.9, 46.5, 55.32 |

## Skin, window, ears

| Part | Frame | Owner | Size (ΔX × ΔY × ΔZ) | Box min | Box max |
|---|:---:|:---:|---|---|---|
| `front_bezel_integral_camera_crown` | R | M019a | 24 × 130 × 102 | -24, -65, -0 | 0, 65, 102 |
| `main_octagonal_skin` | R | M019a | 103.8 × 130 × 86 | -112.6, -65, -0 | -8.8, 65, 86 |
| `removable_octagonal_rear_cover` | R | M019a | 2.7 × 130 × 86 | -115, -65, -0 | -112.3, 65, 86 |
| `window_opaque_mask_110mm` | R | M003 | 1.5 × 110 × 64 | -2.65, -55, 8 | -1.15, 55, 72 |
| `window_clear_optical_area` | R | M003 | 1.5 × 99 × 58 | -2.65, -49.5, 11 | -1.15, 49.5, 69 |
| `crown_status_light_diffuser` | R | M007 | 2.9 × 3.4 × 3.4 | -5, 13.5, 90.1 | -2.1, 16.9, 93.5 |
| `ear_-1_ridged_inner_mount` | R | M019a | 60 × 7.1 × 45.41 | -73, -72.1, 26.59 | -13, -65, 72 |
| `ear_-1_hollow_removable_cap` | R | M019a | 60 × 6.2 × 57.61 | -73, -75, 14.39 | -13, -68.8, 72 |
| `ear_-1_amber_inlay` | R | M019a | 43.6 × 0.18 × 43.6 | -64.8, -74.78, 20.2 | -21.2, -74.6, 63.8 |
| `ear_-1_dark_centre` | R | M019a | 42 × 0.15 × 42 | -64, -74.75, 21 | -22, -74.6, 63 |
| `ear_1_ridged_inner_mount` | R | M019a | 60 × 7.1 × 45.16 | -73, 65, 26.84 | -13, 72.1, 72 |
| `ear_1_hollow_removable_cap` | R | M019a | 60 × 6.2 × 57.57 | -73, 68.8, 14.43 | -13, 75, 72 |
| `ear_1_amber_inlay` | R | M019a | 43.6 × 0.18 × 43.6 | -64.8, 74.6, 20.2 | -21.2, 74.78, 63.8 |
| `ear_1_dark_centre` | R | M019a | 42 × 0.15 × 42 | -64, 74.6, 21 | -22, 74.75, 63 |

## Mechanism and supports

| Part | Frame | Owner | Size (ΔX × ΔY × ΔZ) | Box min | Box max |
|---|:---:|:---:|---|---|---|
| `connected_rolling_cradle_flange_ear_stalks` | R | M010 | 25 × 141 × 73.5 | -40, -70.5, 2.5 | -15, 70.5, 76 |
| `rolling_spindle_6mm` | R | M016-18-R | 32 × 6 × 6 | -72, -4.06, 43.67 | -40, 1.94, 49.67 |
| `bearing_cartridge_trial` | P | M010-P | 30 × 24 × 24 | -69, -13.06, 34.67 | -39, 10.94, 58.67 |
| `coaxial_coupling_trial` | R | M013-15-R | 8.5 × 12 × 12 | -77.5, -7.06, 40.67 | -69, 4.94, 52.67 |
| `pitch_trunnion_-49` | P | M016-18-P | 8 × 9 × 8 | -43.4, -53.5, 41.32 | -35.4, -44.5, 49.32 |
| `pitch_trunnion_49` | P | M016-18-P | 8 × 9 × 8 | -43.4, 44.5, 41.32 | -35.4, 53.5, 49.32 |
| `connected_pitch_frame_roll_servo_saddle` | P | M011-P | 74.6 × 102 × 32.15 | -108, -51, 19.17 | -33.4, 51, 51.32 |
| `yaw_yoke_leg_-55` | Y | M011-Y | 38.6 × 6 × 83.32 | -74, -58, -32 | -35.4, -52, 51.32 |
| `yaw_yoke_leg_55` | Y | M011-Y | 38.6 × 6 × 83.32 | -74, 52, -32 | -35.4, 58, 51.32 |
| `yaw_yoke_spindle_bridge` | Y | M012 | 38.6 × 116 × 4 | -74, -58, -36 | -35.4, 58, -32 |
| `pitch_servo_to_yoke_adapter_trial` | Y | M011-Y | 30 × 41 × 24 | -65.4, 17, 34.32 | -35.4, 58, 58.32 |

## Other authored solids

| Part | Frame | Owner | Size (ΔX × ΔY × ΔZ) | Box min | Box max |
|---|:---:|:---:|---|---|---|
| `removable_camera_edge_bracket_trial` | R | M005 | 2.2 × 30 × 26 | -17, -15, 74 | -14.8, 15, 100 |

## Reserves and keep-outs

| Part | Frame | Owner | Size (ΔX × ΔY × ΔZ) | Box min | Box max |
|---|:---:|:---:|---|---|---|
| `display_connector_and_flashing_access_reserve` | R | — | 3.6 × 106.1 × 68 | -18, -53.05, 6 | -14.4, 53.05, 74 |
| `camera_CSI_exit_and_bend_reserve` | R | — | 9.5 × 22 × 12 | -24, -11, 73 | -14.5, 11, 85 |
| `addressable_status_LED_package_reserve` | R | M007 | 3 × 5 × 5 | -8, 12.7, 89.3 | -5, 17.7, 94.3 |
| `C2_installed_components_reserve` | R | — | 7.4 × 18 × 23.5 | -34, -38, 28 | -26.6, -20, 51.5 |
| `C2_USB_C_withdrawal_BOOT_RESET_service_reserve` | R | — | 9 × 12 × 30 | -33, -35, 51.5 | -24, -23, 81.5 |
| `roll_bearing_1_16x6_reserve` | P | M016-18-P | 6 × 16 × 16 | -46, -9.06, 38.67 | -40, 6.94, 54.67 |
| `roll_bearing_2_16x6_reserve` | P | M016-18-P | 6 × 16 × 16 | -68, -9.06, 38.67 | -62, 6.94, 54.67 |
| `yaw_spindle_interface_reserve` | Y | M016-18-Y | 8 × 8 × 24 | -43.4, -4, -60 | -35.4, 4, -36 |

## Fasteners (modelled geometry)

| Part | Frame | Owner | Size (ΔX × ΔY × ΔZ) | Box min | Box max |
|---|:---:|:---:|---|---|---|
| `ear_-1_M2_1` | R | M021a | 3.5 × 7.18 × 3.5 | -27.07, -74.68, 57.93 | -23.57, -67.5, 61.43 |
| `ear_-1_M2_2` | R | M021a | 3.5 × 7.18 × 3.5 | -62.43, -74.68, 57.93 | -58.93, -67.5, 61.43 |
| `ear_-1_M2_3` | R | M021a | 3.5 × 7.18 × 3.5 | -62.43, -74.68, 22.57 | -58.93, -67.5, 26.07 |
| `ear_-1_M2_4` | R | M021a | 3.5 × 7.18 × 3.5 | -27.07, -74.68, 22.57 | -23.57, -67.5, 26.07 |
| `ear_-1_hidden_mount_M2_-4` | R | M021-R | 3.5 × 7.18 × 3.5 | -22.25, -72.78, 36.25 | -18.75, -65.6, 39.75 |
| `ear_-1_hidden_mount_M2_4` | R | M021-R | 3.5 × 7.18 × 3.5 | -22.25, -72.78, 44.25 | -18.75, -65.6, 47.75 |
| `ear_1_M2_1` | R | M021a | 3.5 × 7.18 × 3.5 | -27.07, 67.5, 57.93 | -23.57, 74.68, 61.43 |
| `ear_1_M2_2` | R | M021a | 3.5 × 7.18 × 3.5 | -62.43, 67.5, 57.93 | -58.93, 74.68, 61.43 |
| `ear_1_M2_3` | R | M021a | 3.5 × 7.18 × 3.5 | -62.43, 67.5, 22.57 | -58.93, 74.68, 26.07 |
| `ear_1_M2_4` | R | M021a | 3.5 × 7.18 × 3.5 | -27.07, 67.5, 22.57 | -23.57, 74.68, 26.07 |
| `ear_1_hidden_mount_M2_-4` | R | M021-R | 3.5 × 7.18 × 3.5 | -22.25, 65.6, 36.25 | -18.75, 72.78, 39.75 |
| `ear_1_hidden_mount_M2_4` | R | M021-R | 3.5 × 7.18 × 3.5 | -22.25, 65.6, 44.25 | -18.75, 72.78, 47.75 |
| `front_M2x10_1` | R | M021a | 11.18 × 3.5 × 3.5 | -11.7, -59.15, 14.25 | -0.52, -55.65, 17.75 |
| `front_M2x10_2` | R | M021a | 11.18 × 3.5 × 3.5 | -11.7, 55.65, 14.25 | -0.52, 59.15, 17.75 |
| `front_M2x10_3` | R | M021a | 11.18 × 3.5 × 3.5 | -11.7, -59.15, 62.25 | -0.52, -55.65, 65.75 |
| `front_M2x10_4` | R | M021a | 11.18 × 3.5 × 3.5 | -11.7, 55.65, 62.25 | -0.52, 59.15, 65.75 |
| `front_M2x10_5` | R | M021a | 11.18 × 3.5 × 3.5 | -11.7, -33.75, 76.25 | -0.52, -30.25, 79.75 |
| `front_M2x10_6` | R | M021a | 11.18 × 3.5 × 3.5 | -11.7, 30.25, 76.25 | -0.52, 33.75, 79.75 |
| `rear_M2x6_1` | R | M021a | 7.18 × 3.5 × 3.5 | -114.68, -57.75, 17.25 | -107.5, -54.25, 20.75 |
| `rear_M2x6_2` | R | M021a | 7.18 × 3.5 × 3.5 | -114.68, 54.25, 17.25 | -107.5, 57.75, 20.75 |
| `rear_M2x6_3` | R | M021a | 7.18 × 3.5 × 3.5 | -114.68, -57.75, 65.25 | -107.5, -54.25, 68.75 |
| `rear_M2x6_4` | R | M021a | 7.18 × 3.5 × 3.5 | -114.68, 54.25, 65.25 | -107.5, 57.75, 68.75 |

## Fastener seats

Eighteen visible M2 modelled: six front M2×10 at YZ (-57.4, 16); (57.4, 16); (-57.4, 64); (57.4, 64); (-32, 78); (32, 78). Four rear M2×6 at YZ (-56, 19); (56, 19); (-56, 67); (56, 67). Eight ear-cap M2×6 (four per ear at 45°/135°/225°/315° on a 25 mm radius). Four hidden ear-mount M2×6 (two per ear). Heads 3.5 mm diameter × 1.3 mm; 4.2 mm wells. Pilots are layout geometry, not approved PLA threads.

## Limits

- Size is the axis-aligned bounding box, so rotated/octagonal/hollow parts read larger than a manufacturing stock size.
- Camera and XC330 rows here are the layout envelopes used by the fit checkers. Manufacturer STEP is used in the exported assembly with rigid transforms only.
- Receiving pilots are not approved PLA threads. Spindle, bearings, coupling and yoke section are trial.
- Refresh with: python write_dimensions.py from this directory.
