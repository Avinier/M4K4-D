# RP-06 TODO

| Field | Value |
|---|---|
| Status | **Open.** Working CAD is Layout 03 + body/chassis Layout 02. Physical validation 0% |
| Home | [`README.md`](README.md) |
| Detail | [`checklist.md`](checklist.md) |

Checking a box here does not freeze a SKU, promote `E` to `W`, or register a gate.

- [ ] Decide whether to accept the 304 mm neutral stack or recover 4 mm to meet the rounded 300 mm target.

- [ ] Close the CoM gap: Layout 02 is at x +20.2 / h 103.7 mm (a_tip 1.91 m/s²) after the 16 mm body shift; the target is +25 / 124. Recover it or revise the baseline.

- [ ] Close the new axle stack (`RP03-CAD-05`) on real parts: gearmotor face-screw pattern and shaft length, stub-to-web fixing and axial retention, bearing preload, deck/cheek stiffness.

- [ ] Resolve the older body-side clashes the 2026-09-24 sweep found (harness volumes against electronics, rear frame against power/safety envelopes, yaw plate and upper rails against the shell); see `openitems.md`.

- [ ] Resolve inherited RP-01 blockers:
  - [ ] two screw collisions
  - [ ] pitch-frame stiffness
  - [ ] roll-saddle stiffness
  - [ ] hard-stop margin
  - [ ] bearing SKU
  - [ ] balance trim
  - [ ] CAD/firmware sign mapping
  - [ ] actuator family
  - [ ] production camera interconnect

- [ ] Replace remaining CAD envelopes with exact vendor or measured geometry:
  - [ ] motors and gearboxes
  - [ ] wheels and hubs
  - [ ] ball-transfer article
  - [ ] battery
  - [ ] power modules
  - [ ] motor drivers
  - [ ] sensors
  - [ ] audio hardware
  - [ ] connectors and cable exits

- [ ] Bring boxed body-chassis Layout 02 parts in as real STEP (audit 2026-09-24; only the Pi 5 and 608ZZ are real imports today):
  - [ ] Swap in the downloaded STEPs in `layout-01/references/purchased/` (not yet wired into `body_chassis_model.py`):
    - [ ] `pololu_drv8874_carrier.step` (Pololu 4035; bare board 15.2 x 17.8 x 2.8 mm, no headers) replaces the 20 x 20 x 12 DRV8874 boxes
    - [ ] `vishay_tcrt5000.step` (10.2 x 7.1 x 10.5 mm incl. leads) replaces the 10.2 x 5.8 x 7.0 package box
    - [ ] `sharp_gp2y0a41sk0f.step` is 44.5 x 18.9 x 13.5 mm; the model's `FRONT_RANGE_SENSOR_SIZE` 13.5 x 29.5 x 13 is only the body without ears, so re-check the ball-pod window and touch-cap fit
    - [ ] `robotis_xc330_dummy_assy.step` (20 x 34 x 29 mm, 15 solids) replaces the yaw servo box; it is a third-party mirror (xiaoyatec.com) of ROBOTIS's XL/XC-330 file, so verify against the official ROBOTIS download once signed in
  - [ ] STEP found but login-gated (fetch via a signed-in browser):
    - [ ] Raspberry Pi 5 active cooler: GrabCAD `raspberry-pi-5-active-cooler-1` / `raspberry-pi-5-stock-active-cooler-1`; official mechanical drawing PDF on Olimex RPi5-ACOOL resources
    - [ ] ESP32-S3-DevKitC-1-N8: Digi-Key model page 15295894 (the listing is N8R8; the model uses N8, confirm the board outline matches)
  - [ ] CAD not found, use a vendor drawing or measure:
    - [ ] Pololu ball caster 1" with plastic rollers (item 2691): no STEP, dimension PDF only; use it to settle the "12.2 mm read as a radius" hole pattern in `brief.md`
    - [ ] JGA25-370 gearmotor with encoder: only a community STEP on Printables (`ga25-370-gear-motor-w-encoder`, model 1350984); verify the variant, or select a Pololu 25D motor, which has an official STEP
  - [ ] SKU not chosen, so nothing to download yet:
    - [ ] ICM-42688-P IMU breakout
    - [ ] yaw thin-section bearing (50 g placeholder in `MASS_ROWS`)
    - [ ] speaker, amplifier and four PDM microphones (already listed under audio selection below)
    - [ ] battery, power-distribution and safety/watchdog boards (RP-02)
    - [ ] harness: modeled as volumes, not parts; needs a route

- [ ] Resolve the RP-03 CAD-versus-safety issue:
  - the controller/safety design expects multiple direct stop-path sensors
  - current Layout 02 only packages one guarded rear TCRT channel and explicitly makes no full forward/lateral cliff-protection claim
  - since the touch-cap skirt cut (`RP03-CAD-04`, 2026-09-24), floor objects below the GP2Y beam (Z 41), including `C12`, meet the ball's retaining lip with no contact signal; forward edges and low obstacles now rely on the camera, which is not a low-level stop channel
  - this must be reconciled before physical layout closure

- [ ] Fix `_vertical_bore` in `body_chassis_model.py`: it builds a Z-centred cylinder, so every bore sits half its length too low (6 uses left). Switch them to `_z_cylinder`, then re-run the checks and review the keel, pads and locators.

- [ ] Close the ball-nose touch cap on real parts: flexure stiffness, tact-switch force and over-travel stop, debounce, and the 3 mm travel.

- [ ] Confirm the GP2Y 0.70 m/s look-ahead on real floors: charged to the nose front it needs 294.5 mm against the 300 mm rating.

- [ ] Propagate `RP03-CAD-01`…`06` to the permanent RP-03 documents as one reviewed change set (sensor count, bump coverage, the fixed ball-only mount versus the required `D20` swap, CoM and motion restrictions).

- [ ] Select the status LED and diffuser/optic.

- [ ] Select microphone front end, microphone boards, speaker, and amplifier.

- [ ] Select battery and enough of the power hardware to verify actual packaging.

- [ ] Obtain or fabricate representative articles and measure:
  - [ ] every relevant mass
  - [ ] complete robot CoM
  - [ ] head installed mass/CoM
  - [ ] service clearances
  - [ ] cable bend and demate volumes
  - [ ] airflow and temperatures

- [ ] Perform the physical display tests:
  - [ ] smoked window
  - [ ] viewing angle
  - [ ] distance
  - [ ] lighting
  - [ ] frame rate and tearing

- [ ] Perform camera tests:
  - [ ] FOV and occlusion
  - [ ] calibration
  - [ ] focus lock
  - [ ] motion smear
  - [ ] LED/display contamination
  - [ ] live CSI endurance

- [ ] Perform audio tests:
  - [ ] speaker level and vibration
  - [ ] microphone contamination
  - [ ] cooler and mechanism noise
  - [ ] playback-while-listening behaviour

- [ ] Demonstrate replacement of a named high-risk module and record time/tools.

- [ ] Verify current suppliers, landed costs, and substitutes.

- [ ] Register and execute RP06-G01…G06.

## CAD gaps and inefficiencies

Running list of ways the current CAD falls short of a production design. Add to it as they turn up.

- [ ] Layout 02 is a packaging and fit-check model, not a production design (noted 2026-09-24). Passing checks means no clashes and the clearances hold, not that the design is complete. Open causes:
  - [ ] Pi 5 and active cooler have no retention: no standoffs, cooler push-pins or fasteners, and the compute tray is a plain 3 mm box. The cooler is only positioned (`PI_COOLER_TOP_Z`), and nothing ties it to the Pi
  - [ ] Check underside clearance for the cooler push-pin tips and the Pi-to-tray standoff gap (currently an assumed ~16 mm)
  - [ ] Check fan intake and airflow: only 10.5 mm of headroom over the cooler under the yaw stage
  - [ ] Yaw-stage parts are packaging envelopes, not selected or load-rated parts
  - [ ] Head-harness route is unresolved (see the Layout 02 README)

- [ ] Wheel arches and trim have no attachment (noted 2026-09-24). `WHEEL_ARCH_POD_L/R` and the amber `WHEEL_ARCH_UPPER_TRIM_L/R` are separate solids under `BODY_PANELS`, not part of `BODY_SHELL`, and nothing fixes them in place: no screws, tabs, bosses or adhesive land, and no snap or bond for the trim on the arch.
  - [ ] Decide the concept: integral flanges in the printed shell, or bolt-on fenders fixed to the chassis cheeks. The shell floor is open across the axle so the body lowers on from above, which rules out a simple bond
  - [ ] The arches are X-centred on the axle (0.0), not on the body, so they don't follow `BODY_SHIFT_X` (16 mm). Confirm that's intended
  - [ ] Measure the arch-to-shell overlap or gap, and whether the arch sits inside or outside the shell wall; it is part of the open panel-versus-shell clash sweep
  - [ ] Add the fixing and its clearances to the checks

- [ ] Fasteners are positions and bores, not engineered joints (noted 2026-09-24). `CON-P01` (`00-foundation/constraints.md`) makes screw-together construction a requirement for serviceability, and `brief.md` leaves "thread engagement, inserts, sealing/gasket detail, tolerances, material/process selection and structural proof" unresolved. The checks cover screw count, edge inset and ball-flange thread engagement (>= 2.5 mm), not load or stiffness. To do:
  - [ ] List every joint (M4 body/chassis through-bolts and locating pins, M3 service panels, ball flange and pod, keel, axle flange, yaw stage, arches) with its screw, insert or nut, clamp stack, and load path
  - [ ] Set thread engagement and boss geometry per joint: heat-set insert depth, boss wall, edge distance, pull-out margin
  - [ ] Add clearance holes, counterbores, captive nuts or inserts, and washers where the joint needs them, so the CAD carries what would be bought and machined
  - [ ] Size for preload, shear and stiffness on the load-bearing joints first: axle flange, body/chassis bolts, yaw plate and bearing
  - [ ] Choose the material and process (printed, machined or moulded), then the tolerances and any gasket or seal
  - [ ] Add per-joint checks: engagement, edge distance, tool access and service removal path
  - [ ] Add a fastener schedule (BOM) to the generated outputs
