# Chassis v1 CAD starting point

See the [chassis v1 BOM](../BOM.md) for the modeled quantities, shared test dependencies, and release holds.

This folder contains a copy of the latest working [Layout 02 whole-robot CAD](../../../../02-prototypes/RP-06-cad/body-chassis/layout-02/) as the starting point for chassis v1. `body-chassis.step` is the local, full-assembly STEP snapshot; `body-chassis.step.py` and `body_chassis_model.py` are the editable source. The check scripts, parameter sidecar, and saved reports came with that snapshot. The large STEP is ignored by Git and can be regenerated from the source.

Copied from the Layout 02 working tree on 2026-09-27. STEP SHA-256: `73c63c29f7f4d8733b28b023c546889812590d7d05636319c4c75f0d10a0b339`. The saved check reports were copied, not rerun for v1.

**Changed after the copy:** the drive gearmotors are now the ThinkRobotics MOT3001-6V230RPM (a generic JGA25-370 with encoder). No vendor STEP exists, so they are modelled parametrically from the seller's drawing. The face screw pattern, tapped depth and gearbox length are assumptions until a unit is measured. See [decision D-003](../../../decisions.md#d-003) in the build ledger, which records every CAD change made in `03-build/`.

The axle stack was rebuilt per [D-007](../../../decisions.md#d-007) and the bearing selection superseded by [D-012](../../../decisions.md#d-012) ([axle-stack.md](../research/axle-stack.md)): 5 mm motor plate, bolt-on printed housing for two 688 ZZ (8 × 16 × 5) bearings per side, aluminium cap, and turned stub with a set screw, flange and spigot. D-010 integrates the plate and front/rear cheeks into one keyed carrier per side, bolted to the split rails. The wheel bolts to the stub flange. The 608 pair, 2 mm diaphragm and countersunk face screws are gone. The supplier listing was sold out at D-012; the project [BOM](../../../BOM.csv) records the 2026-09-30 in-stock observation for BB688ZZ. Maker, rating data, received fits, stiffness, print tolerances and the physical axle rig remain open.

The copied model still reads purchased STEP references and the Layout 04 head from `02-prototypes/RP-06-cad`. Those external paths are explicit in `body_chassis_model.py`. This is **not** a chassis-only model or a print release yet. Separate the chassis parts, resolve their joints and print settings, and rerun the checks before releasing v1.

The scoped export is built by **chassis-v1.step.py** as **chassis-v1.step**. In Solid display, the frame and both wheels use 30% opacity; the other leaf parts use 60%. Open the [generated CAD scene](http://127.0.0.1:3245/Users/avinier/robotics/makad/docs/03-build/01-chassis/v1/cad?file=chassis-v1.step.py) to review that appearance. Reimporting the `.step` in this viewer currently loses most STEP transparency styles, so its separate `.step` entry appears opaque. The assembly contains 145 occurrences, including 120 leaf occurrences, and passed CAD solid validation with zero failures before this appearance change.

The [frame print-split study](frame-split/README.md) remains a separate review view. Its split deck, rail, crossmember and battery hatch interfaces are incorporated into the main `chassis-v1.step.py` model. The main CAD shows the two deck prints, four rail segments, front crossmember, rear skid crossmember and removable four-screw battery hatch as distinct geometry. The split joints and insert bores remain provisional until printer/process selection and coupons; J04 architecture is defined in the main model, with fit and structural proof still open.

**Drive wheels ([D-008](../../../decisions.md#d-008), [D-009](../../../decisions.md#d-009)):** the wheel is modelled once, in [`wheel/`](wheel/README.md). `wheel_assembly()` imports it, mounts a left and a right wheel with handed tyres on the D-007 stubs, and fails if the hub interface drifts. After a wheel change:

- rebuild `chassis-v1.step`;
- run `wheel/check_wheel.py` for the wheel alone;
- run `wheel/check_wheel_on_chassis.py`, which sweeps the non-axisymmetric wheel against the chassis in about 9 min;
- rerun the full `check_layout.py` with the next release.

**Ball-transfer nose ([D-011](../../../decisions.md#d-011)):** covers joints J07 and J08.

- **Caster:** the three caster screws are ISO 7380 M3 × 8, driven from below into CNC Kitchen M3 × 5.7 inserts in a 6 mm pod seat. Unsnap the housing and ball first to reach them.
- **Touch cap:** it slides 3 mm on a constant-section nose, is held by two snap fingers, and is returned by two springs. Contact is sensed contactlessly by a DRV5055 Hall sensor reading a magnet in the cap ([D-013](../../../decisions.md#d-013), [board spec](../research/nose-hall-board.md)).
- **Lid:** a rear tongue sits under the shell band, and one M2 × 8 countersunk screw goes in behind the sensor at X 111.8. A hump covers the sensor's header and soldered lead, and the cap's top notch clears it ([D-027](../../../decisions.md#d-027)).
- **Front sensor:** the GP2Y0A21YK0F is the vendor STEP with its ears trimmed, lenses forward and connector up. Take it out before the Hall board.
- **J10-8 cable:** it leaves through a round-cornered slot in the pod's back wall and rises through a Ø5 bore in the crossmember and deck at (86, −31).

**Rear TCRT keel ([D-014](../../../decisions.md#d-014)):** covers joints J09 and J10.

- **Keel:** four ISO 4762 M3 × 30 screws, driven from below into CNC Kitchen M3 × 5.7 inserts in the rear crossmember.
- **Sensor:** the TCRT sits on a screwed bezel that also carries the guard lips. It swaps from below with the keel on.
- **Height:** 1 mm shims set the optical height: two give Z 10, zero to four give 12 to 8.
- **Wear shoe:** it slides in on a dovetail and is held by one M2 screw.
- **J10-10 cable:** it rises out of the keel top behind the crossmember with a 30 mm slack loop and a zip-tie lug, and runs to the C3 carrier.
- **Lead:** there is no board in the keel. The TCRT is soldered to a 4-wire GH lead that plugs into C3 J10-10 ([spec](../research/rear-tcrt-lead.md), [D-016](../../../decisions.md#d-016)); the keel only comes off after the sensor is pulled out below.

After a keel change, run `check_rear_keel.py` (about 2 min). It writes `generated/rear-keel-checks.json`.

**Battery and ballast ([D-026](../../../decisions.md#d-026)):** the two 25R cells sit at a 19.5 mm pitch (1.1 mm gap), and the tub grows 0.9 mm rearward to match. The CH-038 ballast screws are modeled as ISO 7046-1 countersunk heads in 90° deck seats, into 9 mm tapped holes. After a battery, tub or ballast change, run `check_battery_ballast.py` (about 10 min). It sweeps the pack, hatch, front deck and ballast against the whole model, checks the head seat, engagement and tip clearance and the register CoM, and writes `generated/battery-ballast-checks.json`. It reports the hatch/shell overlap and three other pre-existing overlaps as OPEN.

After a nose change, run `check_nose_joints.py` (about 30 s, the J07/J08 rows of `check_layout.py`), then `check_nose_service.py` (about an hour; pass sweep names to run a subset). It sweeps the caster, cap, lid, sensor and switch removal paths and the tool paths with the body installed, and writes `generated/nose-service.md`. The full `check_layout.py` carries the J07/J08 geometry checks.

## Chassis boundary for v1

| Scope | Included parts or interface | Current CAD location |
|---|---|---|
| Structure and rolling gear | Deck, rails, crossmembers, axle flanges/cheeks, both Ø84 wheels and tyres, stub shafts, two 688 ZZ bearing pairs, two gearmotors and face screws, purchased Pololu #2691 ball caster plus its custom printed caster/sensor mount pod, rear skid/keel and wear pieces | `CHASSIS_PRIMARY_FRAME`, `WHEEL_L/R`, `BEARING_PAIR_L/R`, `MOTOR_L/R`, `BALL_TRANSFER`, `REAR_SKID_TCRT_MODULE` |
| Drive and base sensing | Two Adafruit #3297 DRV8833 motor driver boards (one per motor; bridges paired within each board), motor leads, deck IMU, rear TCRT, GP2Y0A21YK0F front range sensor, and Hall nose contact/cap. Include minimum wiring and a controller for rolling-chassis tests. | Driver boards and IMU are inside `BODY_ELECTRONICS`; rear TCRT is inside the keel; front sensor envelope and Hall touch cap are inside `BODY_SENSORS` |
| Mass and mounting | Battery tub/hatch and retention, ballast, body mounting holes, four M4 fasteners and two locating pins. Use a representative battery and body/head mass/CoM for load tests. | Tub and ballast are inside `CHASSIS_PRIMARY_FRAME`; battery pack is inside `BODY_ELECTRONICS`; fasteners/pins are `BODY_CHASSIS_MOUNT_HARDWARE` |
| Shared interface, not a chassis-only release | Battery/BMS, power distribution, E-stop, controller, harness routing, and body-side mounts must be specified enough to run and load the base. Their final electrical and body packaging belongs to the linked subsystem releases. | Split across `BODY_ELECTRONICS`, `HARNESS_ROUTES`, `BODY_PRIMARY_FRAME`, and connector groups |

The body shell/frame beyond its mounting interface, Pi 5 and audio, yaw stage, head, and parked cosmetic tail are outside the chassis v1 fabrication scope. Keep their envelopes or mass stand-ins where they affect fit, load, or stability.

The scoped export includes the first three rows: 2 gearmotors, 2 Adafruit DRV8833 boards, 2 wheels, 2 bearing pairs, the frame and body mount hardware, ball transfer/pod, rear skid/TCRT keel, battery pack, deck IMU, GP2Y0A21YK0F, and Hall nose assembly. The A21 and Adafruit #3297 are vendor or vendor-derived STEPs in [`purchased/`](purchased/README.md) (D-027); check both against received units. It leaves out the C3 controller, power-distribution boards, E-stop, Pi, shell, body frame, audio, yaw stage, head, and cosmetic tail.

**Open boundary decisions:** proof of the D-007/D-010 axle carrier (fits, insert retention, deflection, outward bearing retention and alignment); motor driver hardware; battery and harness mounting; rear-only cliff sensing and low-object contact coverage. The J04 geometry and test limits are recorded in [axle-stack §9](../research/axle-stack.md#9-j04-carrier-and-test-plan). Use the [RP-06 open items](../../../../02-prototypes/RP-06-cad/TODO.md) and [RP-03 gates](../../../../02-prototypes/RP-03-locomotion/gates.md) before setting the v1 release.
