# Chassis prints

The printed parts of [chassis v1](../../03-build/01-chassis/v1/BOM.md): the
frame, the axle stack, the wheels, the nose and the rear keel. Most are PETG.
The tyres are TPU and the nose touch cap is ASA. The steps and the status
values are in the [workflow](../workflow.md).

## Parts

Materials and colours are from the [print guide](../../03-build/final/v1/printguide.md#4-colour-scheme).
Orientation, critical dimensions and settings are filled in when each part is exported.

| ID | Label in the CAD | Qty | Material, colour | Printer | Orientation | Critical | Settings | Status |
|---|---|---|---|---|---|---|---|---|
| CH-001 | `CHASSIS_FRAME_FRONT_MODULE` (deck, battery tub, front rails, crossmember, fuse bracket) | 1 | PETG, deep slate | A1 or Guider II | | J04 rail ends and inserts; tub; J13 holes | | TODO |
| CH-001 | `CHASSIS_FRAME_REAR_MODULE` (deck, rear rails, skid crossmember) | 1 | PETG, deep slate | A1 or Guider II | | J04 rail ends; keel insert bores | | TODO |
| CH-001 | `AXLE_MOTOR_CARRIER_L`, `_R` (plate and cheeks, keyed) | 2 | PETG, deep slate | A1 | | Motor face pattern and pilot; J04 key | | TODO |
| CH-011 | `BATTERY_TUB_BOTTOM_HATCH` | 1 | PETG, deep slate | A1 | | Strap slots; four screw holes | | TODO |
| CH-051 | `AXLE_BEARING_HOUSING_L`, `_R` | 2 | PETG, deep slate | A1 | | 688 ZZ bores, tried with the real bearings | | TODO |
| CH-004 | `WHEEL_L_RIM_PETG`, `WHEEL_R_RIM_PETG` | 2 | PETG, slate blue | A1 | | Hub bore on the stub flange; tyre seat; 12 insert bosses | | TODO |
| CH-004 | `WHEEL_L_CLAMP_RING_PETG`, `WHEEL_R_CLAMP_RING_PETG` | 2 | PETG, slate blue | A1 | | Clamp face; screw holes | | TODO |
| CH-058 | `WHEEL_L_HUB_CAP_PETG`, `WHEEL_R_HUB_CAP_PETG` | 2 | PETG, gunmetal | A1 | | Centre screw seat | | TODO |
| CH-005 | `WHEEL_L_TYRE_TPU95A_L`, `WHEEL_R_TYRE_TPU95A_R` (handed) | 2 | TPU 95A, black | A1 (direct drive) | | Seat bore; keyway; chevron direction per side | | TODO |
| CH-002 | `BALL_POD_PRINTED_SEAT` | 1 | PETG, deep slate | A1 | | Caster flange seat; three insert bosses; sensor pocket | | TODO |
| CH-003 | `BALL_POD_SENSOR_LID` | 1 | PETG, deep slate | A1 | | Rear tongue; lead hump | | TODO |
| CH-007 | `BALL_NOSE_TOUCH_CAP` | 1 | ASA, ivory | X1E | | 3 mm slide; snap fingers; magnet pocket | | TODO |
| CH-008 | `REAR_KEEL_FACETED_BODY` | 1 | PETG, taupe | A1 | | Four M3 × 30 bores; dovetail | | TODO |
| CH-009 | `REAR_KEEL_REPLACEABLE_WEAR_SHOE` | 1 | PETG, deep slate | A1 | | Dovetail slide | | TODO |
| CH-010 | `REAR_TCRT_BEZEL_WITH_GUARDS` | 1 | PETG, taupe | A1 | | Sensor seat; guard lips | | TODO |
| CH-068 | `REAR_TCRT_HEIGHT_SHIM_*` | 2 (print 4) | PETG, deep slate | A1 | | 1.0 mm thickness: below the lab's 1.2 mm preferred minimum | | TODO |

The body's wheel-arch pods and trims are in the chassis CAD file but belong to
the body BOM, so they print with the body skins.

## Plates (proposed)

Grouped by filament, because each plate is one spool unless it uses the AMS.
The lab lays the STLs out on the plate; this list is what to ask for together.

| Plate | Parts | Filament | Notes |
|---|---|---|---|
| P01 | Front and rear frame modules | PETG deep slate | One or two plates, decided at export by their footprint |
| P02 | Motor carriers, bearing housings, hatch, pod seat, lid, wear shoe, shims | PETG deep slate | |
| P03 | Rims and clamp rings | PETG slate blue | |
| P04 | Hub caps | PETG gunmetal | Small; can share an AMS plate with P03 |
| P05 | Keel body and TCRT bezel | PETG taupe | |
| P06 | Tyres | TPU 95A black | One tyre first; the second once it grips and clamps |
| P07 | Touch cap | ASA ivory | Prints with the first body-skin plate on the X1E |

## Order

No separate test prints: the small parts go first and are the test.

1. **First visit: P02 and one tyre.** The bearing housings, motor carriers,
   hatch and pod seat are small and carry the fits that matter: the 688 ZZ
   bores, the motor face pattern and the insert bosses. Try them with the real
   bearings, motor and inserts. One tyre settles the TPU question (D-005): if
   it grips and clamps, the printed tyre goes ahead; if not, the O-ring
   fallback. The carriers and housings wait until a motor and the bearings are
   in hand.
2. **Fix and re-export** anything that did not fit (slicer offset or a
   `final/v1` edit), before the big parts.
3. **Second visit: P01, P03, P04 and the second tyre.** The frame modules
   (several hours each) and the wheels. Then the first tests in the
   [chassis test system](../../03-build/01-chassis/v1/testsystem.md):
   receiving inspection, the axle rig, the J04 joint, rolling.
4. **Then P05 and P07:** the nose and keel, for the sensor tests.

## Inserts to have on hand

| Article | Used in | Qty |
|---|---|---|
| M3 × 4 heat-set | Rims (CH-049), motor plates (CH-054) | 20 |
| M3 × 6 heat-set | J04 rail ends (CH-061), hatch bosses (CH-077) | 12 |
| CNC Kitchen M3 × 5.7 | Pod seat (CH-063), keel crossmember (CH-067) | 7 |
| M2.5 heat-set | Driver posts on the deck | 4 |

## Before the first export

- An export script, kept in `final/v1/cad` with the other droid scripts, that
  builds the chassis tree, applies the droid edits with
  `_apply_droid_cuts(tree, strict=False)` from `makad-v1.step.py`, picks each
  leaf above by label, and writes its STL in print orientation to
  `04-print/01-chassis/stl/`. It needs the legacy CAD runtime (cadgen 0.4.28); see the
  [final v1 README](../../03-build/final/v1/README.md).
- The shims: ask the lab about 1.0 mm walls, or make them 1.2 mm with a
  decision entry and a `final/v1` edit (two shims would then set Z 9.6, not
  Z 10).
