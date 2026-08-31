# RP-01 Head Material, Finish and Mass Model — Decision Record

| Field | Value |
|---|---|
| Status | **RP-01 build decisions locked; provisional mass model requires a system-baseline revision** |
| Date | 2026-08-31 |
| Scope | Head shell material, finish system, display-envelope fit and revised mass model |
| Supersedes for RP-01 | `../../01-system/dimensional-baseline.md` head mass target of approximately 250 g and any RP-01 load/actuator conclusion derived from it |
| RP-01 effect | The system-level `~250 g` head target is obsolete for RP-01 sizing; the earlier `~490 g` build-up is now a **pre-M008 lower bound** until the required C2 motion module is selected and weighed |
| Feeds | `payload-mass-capture.md`, CAD blockout, `physics.md`, `rig.md`, `gates.md`, actuator selection |

## 1. Locked RP-01 decisions

| ID | Decision | Rationale / boundary |
|---|---|---|
| D-01 | **Print all RP-01 structure and skin parts in PLA.** | Best sanding/filler behaviour, low iteration cost, high dimensional accuracy and no enclosure requirement. |
| D-02 | PLA is an **RP-01 build decision, not the final Makad material decision**. | Creep and thermal risk remain open. |
| D-03 | Mark structural mass rows M010–M012 as **provisional PLA** pending RP-01 thermal and creep evidence. | A later PETG/ASA structural reprint is then a recorded material change, not an unexplained mass discrepancy. |
| D-04 | Use **real M2 button-head screws** for visible industrial-design fasteners. | Metal should read as metal; planning mass is approximately 0.35 g each until the actual kit is weighed. |
| D-05 | Apply the complete nine-step finish system in §5. | The chipped-over-dark-substrate finish is central to the chosen visual read. |
| D-06 | Fake seams except where assembly/service access requires a real split. | A heavily split shell adds about 28 g of flanges, screws and inserts and weakens the monocoque load path. |
| D-07 | Model panel height offsets of **0.3–0.5 mm** in CAD. | This depth cue cannot be added honestly by paint alone. |
| D-08 | Treat the **250 g complete-head target as infeasible** for this RP-01 build. | The pre-M008 provisional row build-up is approximately 490 g at 1.2 mm PLA walls; required C2 motion hardware adds further mass. |

These eight decisions are change-controlled RP-01 inputs. A later material, finish, seam, fastener, panel-offset or sizing change must name the affected decision ID, state the evidence that displaced it and propagate the resulting mass/CAD changes; it must not silently edit the planning model.

## 2. Selected-display geometry and fit

The selected display is the no-touch **Waveshare ESP32-S3-LCD-4.3, SKU 30493**. The confirmed board outline is **106.1 × 67.8 mm**; the panel is 800 × 480 with approximately **95.0 × 53.9 mm** active area. The published `118 g` remains `D`/listing evidence and is not an accepted mass measurement.

| Dimension | Current RP-01 value |
|---|---:|
| Nominal complete head | 95 H × 150 W × 115 D mm |
| Validation range | 90–100 H × 145–155 W × 110–120 D mm |
| Core excluding side pods | 95 H × 125–130 W × 110–115 D mm |
| Optical aperture | 94–95 W × 53–54 H mm |
| Visible bezel/window | 110–115 W × 60–65 H mm |
| Side pods | 40–50 mm diameter; +8–12 mm per side |

| Axis | Board / stack | Core | Result |
|---|---:|---:|---|
| Width | 106.1 mm board; approximately 114.5 mm with 1.2 mm walls and 3 mm clearance per side | 125–130 mm | Fits, but only approximately 5–8 mm per side remains; do not place heavy ribs or side hardware casually. |
| Height | 67.8 mm board; approximately 76 mm minimum stack | 95 mm | Fits with approximately 19 mm for camera/top structure. |
| Depth | Approximately 12–18 mm display stack | 110–115 mm | Fits with large unused depth; challenge whether 110–115 mm is truly required. |

The 110–115 mm window is wider than the 106.1 mm board. Its rear surface therefore needs an opaque mask across the **full window width** so the head interior cannot be seen beside the panel. The window is shorter than the board, so the board's top and bottom edges correctly disappear behind the opaque shell.

The sealed-head assembly must also provide either external access to the display's USB-C/BOOT/RESET functions or a defined wire-flashing method before CAD freeze.

## 3. Material model and risk

| Material | Density (g/cm³) | E (GPa) | Approx. E/ρ | Thermal note | RP-01 role |
|---|---:|---:|---:|---|---|
| **PLA** | 1.24 | 3.0–3.5 | 2.6 | Softens around 60 °C; sustained-load creep risk | Locked structure and skin for RP-01 |
| PETG | 1.27 | 1.7–2.1 | 1.5 | Better heat resistance; poor sanding | Open-frame structural fallback |
| ASA | 1.07 | ~2.0 | 1.9 | Around 100 °C class; enclosure required | Enclosed-printer structural fallback |
| PA12 MJF | 1.01 | ~1.75 | 1.7 | High HDT; outsourced | Reference only |

PLA has the best specific stiffness and finish behaviour for RP-01, but the head is a sealed volume containing servos and a display driver and may remain parked under a static pitch moment. RP-01 must therefore measure structural creep and operating temperature before PLA is promoted beyond the prototype.

For the approximately 730 cm² shell area in §6:

| Wall | PLA | PETG | ASA | PA12 |
|---|---:|---:|---:|---:|
| 1.0 mm | 91 g | 93 g | 78 g | 74 g |
| 1.2 mm | 109 g | 112 g | 94 g | 89 g |
| 1.5 mm | 136 g | 140 g | 118 g | 111 g |
| 2.0 mm | 182 g | 186 g | 157 g | 148 g |

If PLA fails structural creep/thermal evidence, reprint M010–M012 in PETG or ASA according to printer capability. The skin remains PLA unless its own evidence rejects it.

## 4. CAD requirements

| ID | Requirement |
|---|---|
| CAD-01 | Model adjacent panels at 0.3–0.5 mm relative height offsets. |
| CAD-02 | Provide correctly sized wells and bosses for each real visible M2 fastener. |
| CAD-03 | Make the rear-surface window mask opaque across the full 110–115 mm width. |
| CAD-04 | Provide display flashing access or a defined wire-flashing path in the sealed head. |
| CAD-05 | Provide a demateable connector or a defined separable cut plane at the yaw boundary so M020 and M900 can be weighed without cutting conductors. |
| CAD-06 | Use panel lines at least 0.6–0.8 mm wide × 0.5 mm deep, raised rivets at least 2 mm diameter × 0.5 mm proud, recessed fastener wells at least 3 mm diameter and real panel gaps at least 0.8 mm. |

Only rear/bottom access and pod-cap seams should be real unless another split is justified by assembly or service. Cosmetic panel lines and rivets should remain integral features.

## 5. Finish system

Order is part of the process definition:

1. Filler-prime and sand until objectionable layer stepping is gone.
2. Apply a dark grey-brown near-black base coat.
3. Apply two light, deliberately uneven passes of fine texture coat; validate grain on scrap first.
4. Apply two light coats of chipping medium and let them become tacky-dry.
5. Apply several thin white top coats.
6. Activate the chipping medium with water and lift white paint at edges/corners using a stiff brush.
7. Apply a dark enamel/oil panel-line wash and clean the flats.
8. Add an uneven brown-grey grime filter, then restrained steel/aluminium drybrushing on only the sharpest edges.
9. Apply one light matte sealer coat after the weathering is complete.

The expected coating build-up on 730 cm² is planning-only:

| Layer | Estimated mass |
|---|---:|
| Filler primer, two coats | 5 g |
| Dark base | 3 g |
| Texture coat | 12 g |
| White top coat | 4 g |
| Washes and drybrush | 2 g |
| Matte sealer | 3 g |
| **Total** | **~29 g** |

Validate this with a **60 × 60 mm finish coupon** containing representative panel lines and three fastener wells. Weigh it bare and after the complete cured finish to obtain a real coating mass per unit area and judge whether the texture grain is appropriate at head scale.

Install heat-set inserts **after the coated-shell M019b reading**. Keep insert bores empty and paint-free for that reading by masking or drilling them clean, and record the method.

## 6. Provisional mass model

The shell-area estimate uses a 127.5 W × 112.5 D × 95 H mm core box, subtracts the window opening and adds two side pods:

| Contribution | Area |
|---|---:|
| Front + back | 242.3 cm² |
| Top + bottom | 286.9 cm² |
| Left + right | 213.8 cm² |
| Less window opening | −70.3 cm² |
| Two pods | +60 cm² |
| **Approximate shell area** | **~730 cm²** |

All values below are `E` evidence. They are a planning model only and never merge with the accepted `W` roll-up.

| Row | Item | Provisional mass | Basis |
|---|---|---:|---|
| M002 | Display installed | 133 g | 118 g listing/planning value + approximately 15 g carrier |
| M003 | Window + mask | 15 g | 1.5 mm PMMA at approximately 112.5 × 62.5 mm + mask/adhesive |
| M005 | Camera installed | 10 g | Camera Module 3 planning mass + retainer |
| M006 | Camera moving interconnect | 8 g | FPC + stiffeners + strain relief |
| M007 | Status-light assembly | 5 g | Planning allowance |
| M008 | Dedicated motion controller, ESP32-S3 module class, conditional on C1 outcome | `U` | C1 fails on the selected carrier, making C2 required; exact module/mount/harness mass is not estimated and must be weighed |
| M009 | Runtime head IMU | 0 g | Not installed for stationary RP-01; bench IMU is excluded from the ledger |
| M010 | Roll cradle, provisional PLA | 25 g | Planning allowance |
| M011 | Pitch yoke, provisional PLA | 35 g | Planning allowance |
| M012 | Yaw moving interface, provisional PLA | 20 g | Planning allowance |
| M013–M015 | Actuator moving hardware | 35 g | Boundary-dependent allowance |
| M016–M018 | Moving bearing portions | 22 g | Planning allowance |
| M019c | Installed finished shell, 1.2 mm PLA, excluding visible M2 set | 148 g | 109 g shell + 29 g coating + 10 g inserts/magnets/retained adhesive |
| M020 | Non-camera moving harness | 15 g | Planning allowance |
| M021 | Structural/hidden fasteners | 8 g | Planning allowance |
| M021a | Visible M2 button-head fastener set | 11 g | Approximately 0.35 g each; separately tradeable and weighed as one kit |
| **Total before M008** | | **~490 g** | 1.2 mm PLA build lower bound; excludes required C2 motion hardware |

At 1.0 mm shell walls the corresponding pre-M008 estimate is approximately **472 g**. Add the selected C2 controller, mount, connectors and local harness to either figure before treating it as a representative head load. The finished shell, visible M2 set and bare-display planning value alone total approximately 277 g at 1.2 mm walls, before the window, camera, internal structure, bearings, actuators or harness. This makes the old 250 g target unusable for RP-01 load sizing.

The mass result does not itself alter the authored motion vocabulary. It invalidates actuator/load conclusions calculated from the old mass and preliminary inertia. Recompute the per-axis mass tree, CoM, inertia, transient torque, busy-minute RMS/current/temperature and whole-robot CoM/tip sensitivity before selecting actuators or freezing motion limits.

## 7. Mass-capture amendments

`payload-mass-capture.md` implements these rules:

- M019 is retired in favour of sequential M019a bare, M019b coated and M019c installed/finished states.
- M021a separately owns visible M2 fasteners; M021 retains structural/hidden fasteners and consumables.
- The register is a build-time log: weigh irreversible states immediately before coating, bonding or assembly hides them.
- Every physical item gets exactly one boundary-owner row before weighing.
- Record component CoM coordinates and a coarse bounding box in the head frame at the same time as mass.
- Keep `W` and provisional `D`/`E` totals parallel and visibly separate.
- Resolve conditional qty 0 rows with a decision reference.
- Use kit weighing for small fastener sets; large before/after differencing is a flagged fallback.
- M900 closure requires the yaw-plane harness boundary defined by CAD-05.

## 8. Downstream consequences and blockers

| Item | Consequence |
|---|---|
| Neck physics | Replace 250 g sensitivity sizing with the ~490 g pre-M008 lower bound **plus C2** and then the actual per-axis tree. Dynamic torque must use revised inertia, not a simple mass multiplier. |
| Actuator family | Reopen any XL330-class conclusion; evaluate torque-speed, current, RMS/thermal and feedback quality against the revised load. Heavier moving actuators feed back into the tree. |
| Structural dynamics | Real seams and heavier finish affect stiffness/mass; retain the existing ≥25 Hz yaw/roll and ≥30 Hz pitch screening targets until registered evidence changes them. |
| Whole-robot stability | A heavier head raises whole-robot CoM and reduces acceleration margin; propagate after the system baseline accepts a measured/revised value. |

Open blockers:

1. Decide whether 110–115 mm head-core depth is a real packaging requirement or may shrink toward approximately 90 mm.
2. Record whether the available printer is enclosed; this selects ASA versus PETG if the PLA structure fails.
3. Revise the system-level head-mass baseline after accepting this RP-01 model.
4. Resolve the roll-bearing arrangement versus the display envelope.
5. Implement a yaw-plane connector or separable cut plane.
6. Implement display flashing access.
7. Define and run head thermal/creep evidence.

## 9. Immediate actions

1. Print and run the 60 × 60 mm finish coupon through all nine steps; weigh it bare and finished.
2. Answer the depth and printer-enclosure blockers.
3. Apply the provisional ~490 g pre-M008 lower bound **plus the selected C2 controller** to the per-axis physics model and actuator-family screen.
4. Weigh bare M001 and M004 samples as soon as they are available.
5. Replace every provisional row with `W` evidence during the irreversible build sequence.
