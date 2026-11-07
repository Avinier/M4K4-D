# Chassis prints

> **D-095 front module regenerated (2026-11-07, [D-099](../../03-build/decisions.md#d-099)).** `CH-001_CHASSIS_FRAME_FRONT_MODULE.stl` and its manifest row are re-exported from `final/v1/cad/makad-v1.step.py` by `final/v1/cad/export_chassis_front_stl.py`, with the D-095 balance-lead Ø5 deck hole and the tub-bay plate's insert pilots (two M3 × 4 through the deck strip at X 21, two M3 × 6 in the front crossmember at X 83). The script checks both the B-rep and the mesh (13/13): hole open, pilots open with walls over the insert depth, mesh closed, volume within 0.0001 % of the B-rep. Orientation and supports are unchanged; the new holes are vertical. No other existing chassis print changed in D-095. The two new chassis-side prints, the tub-bay plate (CH-106) and the IMU adapter (CH-107), are exported by `final/v1/cad/export_d095_prints_stl.py` (rows below); the body-side rear-bay plate (CH-108) is in [02-body](../02-body/README.md).

The printed parts of [chassis v1](../../03-build/01-chassis/v1/BOM.md): the
frame, the axle stack, the wheels, the nose and the rear keel. Most are PETG.
The tyres are TPU and the nose touch cap is ASA. The steps and the status
values are in the [workflow](../workflow.md). The wheels have their own page,
[wheels/](wheels/README.md): parts, printing, how each joint holds, assembly,
service and the 2026-10-29 gap review (D-070). So does the axle stack,
[axle/](axle/README.md), including the motor-alignment step and the 2026-10-30
gap review (D-071). The frame has its own page, [frame/](frame/README.md): parts, joints, printing,
assembly, service and the 2026-10-30/31 gap review (D-075 to D-078). The combined
[nose](nose/README.md) and [keel](keel/README.md) review covers J07–J10 (D-079 to D-081).

## Parts

Materials and colours are from the [print guide](../../03-build/final/v1/printguide.md#4-colour-scheme).
Orientation, critical dimensions and settings are filled in when each part is exported.

| ID | Label in the CAD | Qty | Material, colour | Printer | Orientation | Critical | Settings | Status |
|---|---|---|---|---|---|---|---|---|
| CH-001 | `CHASSIS_FRAME_FRONT_MODULE` (deck, battery tub, front rails, crossmember, fuse bracket) | 1 | PETG, deep slate | A1 or Guider II | Tub bottom down, as it sits (D-076); tree supports under the deck's X 17–24 ledge, the corner pockets and the fuse shelf (1131 mm², after D-077) | J04 rail ends and inserts; tub; J13 holes; D-095 balance hole Ø5 at (52, 47.4) and four tub-plate insert pilots | | EXPORTED (re-exported 2026-11-07, D-099) |
| CH-001 | `CHASSIS_FRAME_REAR_MODULE` (deck, rear rails, skid crossmember) | 1 | PETG, deep slate | A1 or Guider II | Deck top down (D-076); supports only under the four crossmember ends (194 mm²); drill the rear pin hole Ø4.1 | J04 rail ends; keel insert bores | | EXPORTED |
| CH-001 | `AXLE_MOTOR_CARRIER_L`, `_R` (plate and cheeks, keyed; mirror images) | 2 | PETG, deep slate | A1 | Outboard plate face down; supports only under the square plate's corners (2.5 mm up) | Plate face flat (the housing seats on it); Ø7.6 pilot; 4 insert holes Ø4.0; face-screw counterbores; J04 keys and cheek faces; set-screw notch (D-071) | | EXPORTED |
| CH-011 | `BATTERY_TUB_BOTTOM_HATCH` | 1 | PETG, deep slate | A1 | Outer face down, no supports (D-076) | Strap slots; four screw holes | | EXPORTED |
| CH-051 | `AXLE_BEARING_HOUSING_L`, `_R` (mirror images) | 2 | PETG, deep slate | A1 | Inboard face down, no supports (D-071) | Ø16 seat, tried with the real bearings; shoulder; 4 × Ø3.2 holes (close fit, D-071); key slots | | EXPORTED |
| CH-089 | `AXLE_ALIGNMENT_PLUG` (a tool, `PRINT_TOOLS`; not in the robot) | 1 | PETG, any colour | A1 | Outboard end down, no supports | Ø4.05 bore slides on the motor shaft; Ø15.96 body slides into the tuned housing seat (D-072) | | EXPORTED |
| CH-004 | `WHEEL_L_RIM_PETG` (one STL serves both sides) | 2 | PETG, slate blue | A1 | Lip side down; tree supports inside the dish under the spoke backs and hub web, PLA interface on the web | Ø10 bore; web underside flat (seats on the stub flange); Ø74 seat and 12 ribs; 6 insert holes (1.0 mm wall to the seat); two hub pegs | | EXPORTED |
| CH-004 | `WHEEL_L_CLAMP_RING_PETG` (both sides) | 2 | PETG, slate blue | A1 | Flat inboard face down, no supports | Clamp face flat; Ø63.4 bore on the rim spigot; screw holes | | EXPORTED |
| CH-058 | `WHEEL_L_HUB_CAP_PETG` (both sides) | 2 | PETG, gunmetal | A1 | Underside down, no supports (D-070) | Drops onto the hub pegs without play; centre counterbore | | EXPORTED |
| CH-005 | `WHEEL_L_TYRE_TPU95A_L` in its print state, `PRINT_STATES` (both sides, D-070) | 2 | TPU 95A, black | A1 (direct drive) | On a side face, axis vertical, no supports | Bore Ø73.6 and 12 slots; width 19.3; fit with the V at the top forward | | EXPORTED |
| CH-002 | `BALL_POD_PRINTED_SEAT` | 1 | PETG, deep slate | A1 | Caster seat down (−Z), no supports (D-080) | Caster seat; Ø4 insert bores; sensor floor; Hall slot; crossmember face | | EXPORTED |
| CH-003 | `BALL_POD_SENSOR_LID` | 1 | PETG, deep slate | A1 | Front end down (+X); brim; 89 mm² support inside the hump (D-080) | Tongue; hump interior; countersink | | EXPORTED |
| CH-007 | `BALL_NOSE_TOUCH_CAP` | 1 | ASA, ivory | X1E | Top down (+Z); 33 mm² support at the visor underside; keep finger slits free (D-080); ASA assumed allowed by builder for planning | Snap fingers/slits; slide; magnet pocket; visor | | EXPORTED |
| CH-008 | `REAR_KEEL_FACETED_BODY` | 1 | PETG, taupe | A1 | Crossmember seat down (+Z); 312 mm² supports in upper cavity/end recesses (D-080) | Mounting face; insert/screw paths; sensor pocket and shoe groove | | EXPORTED |
| CH-009 | `REAR_KEEL_REPLACEABLE_WEAR_SHOE` | 1 | PETG, deep slate | A1 | Sole down (−Z), no supports (D-080) | Sliding tongue; Ø1.6 pilot; sole | | EXPORTED |
| CH-010 | `REAR_TCRT_BEZEL_WITH_GUARDS` | 1 | PETG, taupe | A1 | Guard lips down (−Z); 26 mm² support under bezel plate (D-080) | Contoured sensor cradles; optical window; screw/pin fits | | EXPORTED |
| CH-068 | `REAR_TCRT_HEIGHT_SHIM_*` | 2 (print 4) | PETG, deep slate | A1 | Flat (±Z), no supports (D-080) | 1.2 ±0.05 mm thickness; two fitted preserve face Z 10 (D-079); three/four need requalification | | EXPORTED |
| CH-106 | `TUB_BAY_MODULE_PLATE` (D-095: carries both S18V20ALV over the tub) | 1 | PETG, deep slate | A1 | Bottom down, as it sits; no supports. The Ø6.8 × 0.6 ballast-head reliefs on the underside bridge | Four Ø3.4 fixing holes; eight Ø1.6 M2 pilots in the 2.5 mm bosses | | EXPORTED (2026-11-07, D-099) |
| CH-107 | `IMU_ADAPTER_LSM6DSOX` (D-095: LSM6DSOX on the J15A pilots) | 1 | PETG, deep slate | A1 | Bottom down, as it sits; no supports | Two Ø2.2 J15A holes; two Ø1.6 M2 pilots in the bosses | | EXPORTED (2026-11-07, D-099) |

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
| P06 | Both tyres | TPU 95A black | Batch together per builder sequencing below; fit and grip checked during assembly |
| P07 | Touch cap | ASA ivory | Prints with the first body-skin plate on the X1E |

## Order

**Builder revision, 2026-11-01: minimise lab visits.** Prepare the full chassis
STL package and request the complete quantities, including both tyres. Use the
reviewed CAD nominal interfaces; unrecorded motor, bearing and insert
measurements do not hold up export or the batch request. This does not record
physical fit acceptance. The builder prioritises fewer visits and accepts the
possibility of corrective reprints.

1. Export and validate all reviewed parts, recording any unresolved geometry
   separately. The battery restraint route remains unresolved if adapting the
   proposed 20 × 2 mm strap; no wider-slot redesign is implemented or implied.
2. Submit all released parts together with quantities, materials, orientations,
   supports and critical surfaces. Use the recorded lab machines; the lab applies
   its actual machine/filament profiles. OrcaSlicer is installed on the builder's Mac.
3. Run PETG groups on available A1/Guider II machines, TPU on a separate A1,
   and the ASA touch cap on the X1E, subject to lab allocation and supervised
   starts. Assume ASA is allowed for planning, per builder instruction; this is
   not a recorded lab approval. Do not reserve a separate visit for a first tyre
   or first housing, or gate the other parts on those checks.
4. Inspect fits while removing supports and assembling at home or during the
   scheduled visit. Obtain missing screws/inserts and fabricate the metal axle
   parts in parallel. Correct a demonstrated mismatch if one occurs; physical
   acceptance is still required before operating the assembled chassis.

## Hardware order and inserts

The [2026-11-01 order reconciliation](hardware-order.md) records the builder's actual list, shared pools and remaining items. It includes 25 bearings (four installed), 35 M3 × 4 inserts (20 installed), 15 selected slant-knurled M3 × 6 inserts plus 10 other M3 × 6 inserts (21 positions total). Both M3 × 6 listings give OD 4.4, but the other article needs qualification before sharing the reviewed positions. The builder reports motors, bearings and 1.5 mm EVA foam received on 2026-11-01; measurements remain open. The hatch straps are purchased hook-and-loop material threaded through the print, not printed themselves.

Inserts needed for one chassis:

| Article | Used in | Qty |
|---|---|---|
| M3 × 4 heat-set | Rims (CH-049, 6 per rim), motor plates (CH-054) | 20 |
| M3 × 6 heat-set, OD 4.4 (selected slant-knurled article; see order reconciliation) | J04 rail ends (CH-061), hatch bosses (CH-077), pod seat (CH-063), front pod pilots (CH-033), keel pilots (CH-067); Ø4.0 throughout | 21 |
| M2.5 × 4 heat-set, OD 3.9 (CH-080, not bought) | Driver posts on the deck, Ø3.5 pilots (D-075) | 4 |
| M4 × 8 heat-set, OD 5.9 (CH-095, not bought) | J13 body bolts in the deck, Ø5.5 pilots (D-077) | 3 |

## Before the first export

**Current sequencing:** the batch plan above supersedes the earlier staged
first-part/second-visit proposal and the earlier deferral of export planning.
ASA is assumed allowed for planning. Use the existing lab record and nominal
CAD specifications; do not add a separate measurement or proof visit before
preparing the lab package. Exact lab profiles are not stored in this repository.

- An export script, kept in `final/v1/cad` with the other droid scripts, that
  builds the chassis tree, applies the droid edits with
  `_apply_droid_cuts(tree, strict=False)` from `makad-v1.step.py`, picks each
  leaf above by label, swaps in the print state for labels in `PRINT_STATES`
  (the tyre, D-070), adds the tools in `PRINT_TOOLS` (the axle alignment
  plug, D-071), and writes its STL in print orientation to
  `04-print/01-chassis/stl/`. One STL per wheel part serves both sides; the
  carriers and housings need one each for left and right. It needs the legacy CAD runtime (cadgen 0.4.28); see the
  [final v1 README](../../03-build/final/v1/README.md).
- **Frame insert pilots: fixed ([D-075](../../03-build/decisions.md#d-075)).**
  The J04 rail-end and hatch-boss pilots are Ø4.0 (were Ø4.3) for the OD 4.4
  M3 × 6, the J04 ones 7 mm deep; the driver posts Ø3.5 (were Ø3.9) for the
  M2.5 × 4; the IMU gets Ø1.6 pilots. Droid edits, checked by
  `final/v1/cad/check_frame_print.py`. Check the M3 × 6 installation during assembly
  ([frame page](frame/README.md)); it does not gate the module batch.
- **Nose/keel insert positions resolved (D-079).** The in-hand M3 × 6 replaces all nine
  CNC Kitchen positions (CH-033/063/067). Seat bores are through 6 mm; crossmember pilots
  7 mm. Check the pod seat insert fit during assembly; no coupons or separate visit.
- **Shims resolved (D-079).** 1.2 mm shims, sensor flat recessed 0.4 mm: two retain optical
  face Z 10. Print four, fit two; three/four lose shoe-first contact on tip-back and need
  requalification before running.
- **Nose/keel assembly acceptance:** obtain the specified M2 thread-formers; check
  fit, cable slack, sensing and floor contact during assembly. ASA is assumed
  allowed for planning. These checks do not impose a separate first-part visit;
  see the two review pages §8 for the acceptance details.
