# Chassis prints

The printed parts of [chassis v1](../../03-build/01-chassis/v1/BOM.md): the
frame, the axle stack, the wheels, the nose and the rear keel. Most are PETG.
The tyres are TPU and the nose touch cap is ASA. The steps and the status
values are in the [workflow](../workflow.md). The wheels have their own page,
[wheels/](wheels/README.md): parts, printing, how each joint holds, assembly,
service and the 2026-10-29 gap review (D-070). So does the axle stack,
[axle/](axle/README.md), including the motor-alignment step and the 2026-10-30
gap review (D-071). The frame review has started on [frame/](frame/README.md):
the parts and joints are laid out; printing, assembly and the gap table follow.

## Parts

Materials and colours are from the [print guide](../../03-build/final/v1/printguide.md#4-colour-scheme).
Orientation, critical dimensions and settings are filled in when each part is exported.

| ID | Label in the CAD | Qty | Material, colour | Printer | Orientation | Critical | Settings | Status |
|---|---|---|---|---|---|---|---|---|
| CH-001 | `CHASSIS_FRAME_FRONT_MODULE` (deck, battery tub, front rails, crossmember, fuse bracket) | 1 | PETG, deep slate | A1 or Guider II | | J04 rail ends and inserts; tub; J13 holes | | TODO |
| CH-001 | `CHASSIS_FRAME_REAR_MODULE` (deck, rear rails, skid crossmember) | 1 | PETG, deep slate | A1 or Guider II | | J04 rail ends; keel insert bores | | TODO |
| CH-001 | `AXLE_MOTOR_CARRIER_L`, `_R` (plate and cheeks, keyed; mirror images) | 2 | PETG, deep slate | A1 | Outboard plate face down; supports only under the square plate's corners (2.5 mm up) | Plate face flat (the housing seats on it); Ø7.6 pilot; 4 insert holes Ø4.0; face-screw counterbores; J04 keys and cheek faces; set-screw notch (D-071) | | TODO |
| CH-011 | `BATTERY_TUB_BOTTOM_HATCH` | 1 | PETG, deep slate | A1 | | Strap slots; four screw holes | | TODO |
| CH-051 | `AXLE_BEARING_HOUSING_L`, `_R` (mirror images) | 2 | PETG, deep slate | A1 | Inboard face down, no supports (D-071) | Ø16 seat, tried with the real bearings; shoulder; 4 × Ø3.2 holes (close fit, D-071); key slots | | TODO |
| CH-089 | `AXLE_ALIGNMENT_PLUG` (a tool, `PRINT_TOOLS`; not in the robot) | 1 | PETG, any colour | A1 | Outboard end down, no supports | Ø4.05 bore slides on the motor shaft; Ø15.8 body slides into the housing seat | | TODO |
| CH-004 | `WHEEL_L_RIM_PETG` (one STL serves both sides) | 2 | PETG, slate blue | A1 | Lip side down; tree supports inside the dish under the spoke backs and hub web, PLA interface on the web | Ø10 bore; web underside flat (seats on the stub flange); Ø74 seat and 12 ribs; 6 insert holes (1.0 mm wall to the seat); two hub pegs | | TODO |
| CH-004 | `WHEEL_L_CLAMP_RING_PETG` (both sides) | 2 | PETG, slate blue | A1 | Flat inboard face down, no supports | Clamp face flat; Ø63.4 bore on the rim spigot; screw holes | | TODO |
| CH-058 | `WHEEL_L_HUB_CAP_PETG` (both sides) | 2 | PETG, gunmetal | A1 | Underside down, no supports (D-070) | Drops onto the hub pegs without play; centre counterbore | | TODO |
| CH-005 | `WHEEL_L_TYRE_TPU95A_L` in its print state, `PRINT_STATES` (both sides, D-070) | 2 | TPU 95A, black | A1 (direct drive) | On a side face, axis vertical, no supports | Bore Ø73.6 and 12 slots; width 19.3; fit with the V at the top forward | | TODO |
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
| P02 | Motor carriers, bearing housings, alignment plug, hatch, pod seat, lid, wear shoe, shims | PETG deep slate | The plug can be any PETG colour |
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
| M3 × 4 heat-set | Rims (CH-049, 6 per rim), motor plates (CH-054) | 20 |
| M3 × 6 heat-set | J04 rail ends (CH-061), hatch bosses (CH-077) | 12 |
| CNC Kitchen M3 × 5.7 | Pod seat (CH-063), keel crossmember (CH-067) | 7 |
| M2.5 × 4 heat-set, OD 3.9 (CH-080, not bought) | Driver posts on the deck, Ø3.5 pilots (D-073) | 4 |

## Before the first export

- An export script, kept in `final/v1/cad` with the other droid scripts, that
  builds the chassis tree, applies the droid edits with
  `_apply_droid_cuts(tree, strict=False)` from `makad-v1.step.py`, picks each
  leaf above by label, swaps in the print state for labels in `PRINT_STATES`
  (the tyre, D-070), adds the tools in `PRINT_TOOLS` (the axle alignment
  plug, D-071), and writes its STL in print orientation to
  `04-print/01-chassis/stl/`. One STL per wheel part serves both sides; the
  carriers and housings need one each for left and right. It needs the legacy CAD runtime (cadgen 0.4.28); see the
  [final v1 README](../../03-build/final/v1/README.md).
- **Frame insert pilots: fixed ([D-073](../../03-build/decisions.md#d-073)).**
  The J04 rail-end and hatch-boss pilots are Ø4.0 (were Ø4.3) for the OD 4.4
  M3 × 6, the J04 ones 7 mm deep; the driver posts Ø3.5 (were Ø3.9) for the
  M2.5 × 4; the IMU gets Ø1.6 pilots. Droid edits, checked by
  `final/v1/cad/check_frame_print.py`. The pod seat tries the M3 × 6 in Ø4.0
  first, before the modules ([frame page](frame/README.md)).
- **CNC Kitchen M3 × 5.7 positions** (pod seat CH-033/CH-063, keel crossmember
  CH-067; 9 in all) are not ordered. The ordered M3 × 6 (OD 4.4) fits their
  Ø4.0 holes. Check that each bore takes 6 mm instead of 5.7, or order the
  CNC Kitchen part.
- The shims: ask the lab about 1.0 mm walls, or make them 1.2 mm with a
  decision entry and a `final/v1` edit (two shims would then set Z 9.6, not
  Z 10).
