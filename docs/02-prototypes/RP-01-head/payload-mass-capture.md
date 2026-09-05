# RP-01 Installed Payload Mass Capture

| Field | Value |
|---|---|
| Status | **Open — no accepted mass total until physical readings are entered** |
| Owner | Project builder |
| Created | 2026-08-30 |
| Revised | 2026-09-05 |
| Governing RP-01 model | `material-finish-mass-decision.md`: approximately 490 g **pre-M008 lower bound** at 1.2 mm PLA; the C2 architecture is selected and its exact ESP32-S3 module remains to be chosen/weighed; the system baseline now carries the same lower bound |
| Feeds | Per-axis mass tree, CoM/inertia model, actuator sizing, representative RP-01 ballast |

## Purpose and boundary

This record establishes the **physical installed mass** of the complete Makad head. It rejects seller shipping weights, catalogue weights that may include packaging, and zero placeholders for undecided parts.

The accepted complete-head value is:

`m_head,installed = every part downstream of the yaw axis in the selected mechanism`

It includes the selected display and camera plus their actual mounts, window, shell, moving joint structure, moving actuator parts, bearings or bearing parts that move with the head, fasteners, adhesives, head-local control/sensing hardware, connectors, strain relief and the moving portions of the harness. A body-fixed actuator housing or body-fixed cable segment is excluded, but its moving horn, coupler, shaft or rotor-side output hardware is included when it crosses the boundary.

This is a **build-time inventory**, geometry and whole-assembly mass record, not a post-assembly audit. Parts that become bonded, coated or hidden must be weighed and located immediately before the irreversible step. The next step assigns every row to yaw, pitch and roll according to the selected physical mounting arrangement; do not infer that membership here.

Every physical part receives exactly one `Boundary owner ID` before weighing. A note such as “exclude if another row counts it” is insufficient: either that other row owns the part or this row does. Conditional rows resolved to quantity zero require a decision reference so zero cannot be confused with omission.

**Inventory ownership is distinct from per-axis moving membership.** M013/M014/M015 are actuator inventory owners at the complete-head yaw boundary, not instructions to count only parts rotating about the actuator's own axis. For a yaw→pitch→roll serial arrangement, the roll servo housing is carried by yaw and pitch, the pitch servo housing by yaw, and a body-fixed yaw housing belongs to none of the head's downstream sets. Include every housing downstream of yaw once in M900; partition its contribution to the per-axis tree separately. Split mixed-frame kits such as yokes, bearing rings, shell/ear covers and harness branches into named subitems while preserving their parent totals. This clarification selects no mechanism and changes no provisional mass allowance.

## Accepted evidence rule

Only `W` evidence contributes to the final real-mass total:

- `W`: physically weighed in the exact recorded state.
- `D`: manufacturer datasheet value; useful only for planning before the sample exists.
- `E`: estimate from geometry, slicer or analogy; useful only for an explicit provisional range.
- `U`: unknown or not selected. It remains an open non-zero item and is never entered as `0 g`.

The currently published `118 g` display value is therefore not an accepted measurement. It remains a planning upper-bound/listing value until the exact received module is weighed without packaging.

## Scale and measurement method

Use a digital scale with **0.1 g resolution or better**. Its capacity, including the tray/fixture, must be at least **2× the largest expected reading**. With the current approximately 490 g model, use at least a 1 kg scale. A 1 g kitchen scale may screen the assembled head but is not adequate for the camera, cable, fastener or adhesive rows.

Before a measurement session:

1. Put the scale on a rigid, level surface away from fan airflow and cable contact.
2. Record scale make/model, resolution, stated accuracy and maximum capacity below.
3. Verify zero, then check with traceable/known masses near **10 g, 100 g and 200 g**. Each indication must be within `±max(0.2 g, the scale's stated accuracy)` of the known value. On failure, reject the session's `W` evidence until the scale is recalibrated, repaired or replaced; never silently correct readings.
4. Use a tared ESD-safe tray for camera and bare electronics. Nothing may touch the bench or pull on the item while reading.
5. Take three independent readings, removing and replacing the item between readings. Accept the median. If the range exceeds `max(0.2 g, 0.2% of the reading)`, investigate and repeat.
6. Photograph the item state and scale display for each accepted row. The evidence reference may be a local photo path or run-record ID.

| Session field | Entry |
|---|---|
| Date/time | `TBD` |
| Scale make/model | `TBD` |
| Resolution / stated accuracy / capacity | `TBD` |
| 10 g check: known / indicated / error | `TBD` |
| 100 g check: known / indicated / error | `TBD` |
| 200 g check: known / indicated / error | `TBD` |
| Calibration acceptance | `TBD — PASS/FAIL` |
| Operator | `TBD` |

## Weigh-in sequence

Weigh parts in both useful states where practical:

1. **Bare received component:** exact part with seller packaging, shipping films and loose accessories removed.
2. **Installed subassembly:** component plus only the mount, pads, connector retention and local cable that remain in the head.
3. **Irreversible intermediate:** weigh immediately before and after coating/bonding/hidden assembly where the process destroys the earlier state.
4. **Complete moving head:** final downstream assembly weighed independently as a cross-check against the row sum.

Do not add a bare component row and its installed-subassembly row together. The `Count in roll-up?` column identifies the mutually exclusive installed rows that form the total.

## Measurement register

`State / exact boundary` must be detailed enough to reproduce the reading. Examples: cable length present, protective film removed or retained, screws/inserts included, adhesive cured, and whether a servo horn or output coupler is attached.

Use the head Cartesian frame already adopted by RP-01: origin and final datum remain tied to the selected CAD blockout; `+X` forward, `+Y` robot-left and `+Z` up. Record each row's approximate component CoM coordinates and coarse `X × Y × Z` bounding box while it is still accessible. Replace bench estimates with CAD-derived properties later, retaining the original capture as evidence.

| ID | Item / exact selected state | Qty | Boundary owner ID | Evidence | R1 (g) | R2 (g) | R3 (g) | Accepted (g) | CoM x/y/z (mm) | Box X×Y×Z (mm) | Roll-up? | Evidence / decision reference |
|---|---|---:|---|:---:|---:|---:|---:|---:|---|---|:---:|---|
| M001 | Face display, bare Waveshare ESP32-S3-LCD-4.3 no-touch SKU 30493; no packaging or loose accessories | 1 | M001 | `U` |  |  |  |  |  | 106.1×67.8×TBD | No | Sample reading required; 118 g remains listing evidence only |
| M002 | Installed display: M001 + carrier/pads/retention and hardware explicitly assigned here | 1 | M002 | `U` |  |  |  |  |  |  | Yes | Mount open |
| M003 | Final smoked window + full-width opaque rear mask + retained adhesive/pads | 1 | M003 | `U` |  |  |  |  |  |  | Yes | Material open |
| M004 | Bare Raspberry Pi Camera Module 3 Wide visible/IR-cut SC0874 | 1 | M004 | `U` |  |  |  |  |  | 25×24×12.4 | No | Sample reading required |
| M005 | Installed camera: M004 + final retainer/mount and connector-retention parts owned here | 1 | M005 | `U` |  |  |  |  |  |  | Yes | Mount open; cable parts must be assigned to M005 or M006 before weighing |
| M006 | Final camera moving interconnect: assigned cable/adapters/stiffeners/connectors/strain relief downstream of yaw | 1 set | M006 | `U` |  |  |  |  |  |  | Yes | Production interconnect open |
| M007 | Status LED/PCB + optic/diffuser + mount + wiring assigned here | 1 | M007 | `U` |  |  |  |  |  |  | Yes | Implementation open |
| M008 | **Dedicated C2 motion controller, ESP32-S3 module class**, plus its mount/connectors | 1 | M008 | `U` |  |  |  |  |  |  | Yes | C1 is rejected on the selected carrier's GPIO budget. Select and weigh the exact C2 module, mount, connectors and local harness before any complete-head mass claim |
| M009 | Runtime head IMU | 0 | M009 | `E` |  |  |  | 0 |  |  | No | RP-01 architecture decision: not installed; bench IMU is excluded from this ledger. Any future installed sensor requires a superseding decision/new row. |
| M010 | Roll cradle/payload frame, final cleaned **provisional PLA** part with retained inserts assigned here | 1 set | M010 | `U` |  |  |  |  |  |  | Yes | Thermal/creep flag remains open |
| M011 | Pitch yoke/moving support, final cleaned **provisional PLA** part with retained inserts assigned here | 1 set | M011 | `U` |  |  |  |  |  |  | Yes | Thermal/creep flag remains open |
| M012 | Yaw moving interface, final cleaned **provisional PLA** plate/flange/coupler structure downstream of yaw | 1 set | M012 | `U` |  |  |  |  |  |  | Yes | Thermal/creep flag remains open |
| M013 | Roll actuator hardware downstream of yaw: include the whole actuator when its housing is downstream of yaw, even if the housing does not roll; otherwise assigned moving output hardware only | 1 | M013 | `U` |  |  |  |  |  |  | Yes | Record housing/output subitems and their yaw/pitch/roll membership separately; name the owner of mount/spindle hardware |
| M014 | Pitch actuator hardware downstream of yaw: include its housing when mounted on the yaw yoke even though that housing does not pitch; record horn/mount ownership explicitly | 1 | M014 | `U` |  |  |  |  |  |  | Yes | Record housing/output subitems and their yaw/pitch/roll membership separately |
| M015 | Yaw moving horn/coupler/output hardware when housing is body-fixed; whole actuator only if actually downstream | 1 | M015 | `U` |  |  |  |  |  |  | Yes | Boundary depends on mechanism |
| M016 | Moving portion of roll bearings/pivots; record ring allocation or conservative whole-bearing ownership | 1 set | M016 | `U` |  |  |  |  |  |  | Yes | Support open |
| M017 | Moving portion of pitch bearings/pivots downstream of yaw; record allocation method | 1 set | M017 | `U` |  |  |  |  |  |  | Yes | Support open |
| M018 | Moving portion of yaw bearing/shaft/retainer; body-fixed race/housing excluded by explicit ownership | 1 set | M018 | `U` |  |  |  |  |  |  | Yes | Support open |
| M019a | Bare shell/face frame/pod covers, final printed and cleaned, supports removed and sanded; **before primer**, inserts/magnets absent | 1 set | M019a | `U` |  |  |  |  |  |  | No | Strict first state; weigh before coating |
| M019b | M019a + complete nine-step finish, cured ≥24 h; insert bores empty and paint-free | 1 set | M019b | `U` |  |  |  |  |  |  | No | Coating mass = M019b − M019a; record masking/drilling method |
| M019c | M019b + heat-set inserts, magnets and retained adhesive assigned here | 1 set | M019c | `U` |  |  |  |  |  |  | Yes | Replaces retired M019 |
| M020 | Non-camera power/data/servo moving harness downstream of yaw, terminating at CAD-05 separable boundary | 1 set | M020 | `U` |  |  |  |  |  |  | Yes | Final routing/gauge open; continuous non-separable conductors block M900 closure |
| M021 | Structural/hidden screws, washers, nuts, clips, adhesive, tape and strain relief not owned elsewhere | 1 kit | M021 | `U` |  |  |  |  |  |  | Yes | Weigh complete kit; before/after differencing is flagged fallback only |
| M021a | Visible real M2 button-head industrial-design fasteners, as-installed count | 1 kit | M021a | `U` |  |  |  |  |  |  | Yes | Planning only: approximately 0.35 g each |
| M022 | Other installed moving item, named explicitly |  | M022 | `U` |  |  |  |  |  |  | Conditional | Add rows as required; qty 0 requires decision reference |
| M900 | **Complete moving head cross-check**, independently weighed downstream of yaw and ready to operate | 1 | M900 | `U` |  |  |  |  |  |  | Cross-check | Include harness in defined neutral service-loop state; requires CAD-05 boundary |

## Parallel provisional model

This `D`/`E` model supports pre-purchase physics and actuator screening. It remains permanently separate from the accepted `W` total.

| Row | Provisional mass (g) | Evidence / basis |
|---|---:|---|
| M002 | 133 | `D/E`: 118 g display listing + approximately 15 g carrier |
| M003 | 15 | `E`: 1.5 mm PMMA window + mask/adhesive |
| M005 | 10 | `E`: camera + retainer |
| M006 | 8 | `E`: FPC/stiffeners/strain relief |
| M007 | 5 | `E` |
| M008 | `U` | Required C2 motion-controller module after C1 carrier-GPIO failure; no defensible mass until the exact module/mount/harness is selected |
| M009 | 0 | No runtime RP-01 head IMU; bench IMU excluded |
| M010 | 25 | `E`: provisional PLA roll cradle |
| M011 | 35 | `E`: provisional PLA pitch yoke |
| M012 | 20 | `E`: provisional PLA yaw moving interface |
| M013–M015 | 35 | `E`: boundary-dependent moving actuator hardware |
| M016–M018 | 22 | `E`: moving bearing portions |
| M019c | 148 | `E`: 109 g 1.2 mm PLA shell + 29 g coating + 10 g inserts/magnets/retained adhesive; visible M2 set excluded |
| M020 | 15 | `E`: moving harness |
| M021 | 8 | `E`: structural/hidden fasteners |
| M021a | 11 | `E`: visible M2 button-head set at approximately 0.35 g each; separately owned and tradeable |
| **Provisional complete head including unknown M008** | **~490 + M008** | Planning-only lower bound; see `material-finish-mass-decision.md` |

The corresponding 1.0 mm PLA-wall case is approximately **472 g + M008**. Neither number is accepted `W` evidence.

## Roll-up and closure checks

Do not publish a single real payload mass until all rows marked `Yes` have `W` evidence or have been explicitly removed because the final architecture does not contain them.

| Check | Result |
|---|---:|
| Sum of accepted `W` installed rows marked `Yes` | `TBD g` |
| Complete moving-head cross-check M900 | `TBD g` |
| Difference: M900 minus row sum | `TBD g` |
| Difference as percentage of M900 | `TBD %` |
| Difference from provisional pre-M008 lower bound: `M900 - 490 g` | `TBD g` |
| Historical system-target overrun: `M900 - 250 g` | `TBD g` |

Closure requires:

- absolute row-sum difference no greater than **2.0 g or 0.5% of M900, whichever is larger**;
- no unresolved `U` row that exists in the final assembly;
- no double counting between bare components and installed subassemblies;
- every part has one and only one boundary-owner row;
- all conditional qty 0 rows cite the decision that removed them;
- every excluded actuator, bearing part or harness segment identified as physically upstream/body-fixed rather than silently omitted;
- the complete head weighed in a defined, reproducible cable/service-loop state at a separable yaw-plane boundary.

Retain M900 regardless of its relationship to either planning value. A mismatch is a design/model finding or a controlled baseline revision; it is never corrected by deleting real mass from the record.

## Finish-coupon capture

Before coating M019a, print a 60 × 60 mm PLA coupon with representative 0.6–0.8 mm panel lines and three 3 mm fastener wells. Run the exact nine-step process in `material-finish-mass-decision.md`.

| Coupon field | Entry |
|---|---|
| Printed/cleaned area and thickness | `TBD` |
| Bare readings / accepted mass | `TBD` |
| Finished readings / accepted mass after ≥24 h cure | `TBD` |
| Coating mass difference | `TBD g` |
| Coating areal mass | `TBD g/cm²` |
| Texture product / batch / passes | `TBD` |
| Visual verdict at head scale | `TBD — PASS/ITERATE` |

## Immediate first batch

The first useful bench work does not wait for a complete head:

1. Verify the scale at 10, 100 and 200 g.
2. Print, weigh and finish the 60 × 60 mm coupon; derive coating areal mass.
3. M001: weigh bare Waveshare SKU 30493 when received.
4. M004: weigh bare Raspberry Pi Camera Module 3 Wide SC0874 when received.
5. Weigh supplied display leads/accessories as separate temporary rows, without assuming they will be installed.
6. Weigh the supplied 200 mm camera FPC separately; it is bench hardware, not yet the production moving interconnect.

These readings establish the unavoidable core mass but **not** the installed payload or complete moving-head mass. The latter remains open until the actual mounts, window, structure, bearings, actuators, controller choice and moving harness exist.
