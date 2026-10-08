# Feetech migration execution status (2026-10-07)

This tracks the user's 0–3 checklist against evidence in `03-build`. The
selected servos are **candidates**, not released production actuators. The
existing head and body CAD still install XC330 geometry, so derived axes,
mass, FEA, electrical hardware and whole-robot stability outputs remain the
XC330 baseline until the mechanical and bench gates below close.

| Checklist | Result | Evidence / remaining gate |
|---|---|---|
| 0.1 / 0.3 source data | Partial | STS3045M drawing-based [reference STEP](03-head/v1/cad/purchased/sts3045m_reference.step) and [official ST3215-HS STEP](02-body/v1/cad/purchased/waveshare_feetech_st3215_hs_servo.step); Feetech protocol and memory table recorded in [screen](03-head/v1/feetech-actuator-screen.md). The HS official STEP has one invalid-topology main-case solid, so it is packaging evidence only. The STS3045M horn, tooth geometry and tolerance data are missing. |
| 0.2 physical inputs | Blocked by unavailable hardware | No STS3045M, HS, USB adapter or 12 V bench supply available; [B1–B6 protocol](03-head/v1/feetech-bench-protocol.md) is ready but cannot be run. |
| 1.1–1.4 actuator math and storyboard | Provisional screen and mass sensitivity complete | [Screen](03-head/v1/feetech-actuator-screen.md) records terminal-voltage torque proxy, reflected head motor inertia, P01–P09, and thermal gate. [Storyboard](03-head/v1/feetech-motion-storyboard.md) revises the fast pitch segments. The [unchanged-structure mass what-if](03-head/v1/cad/generated/feetech-mass-whatif.json) quantifies the two 34.8 g cases. Re-running §11.3 from a redesigned mass tree and P07 FEA requires refitted CAD; these are not numerically closed. |
| 1.5–1.9 power | Architecture calculations complete, schematic open | [Power delta](04-pcbs/power-boards.md#4a-feetech-actuator-rail-delta-d-046d-047-2026-10-07) covers 5.5 V divider, 5.23 V terminal minimum, 5.9 V clamp target, 12 V converter loading/heat, braking, overload/current monitor and duty-dependent runtime. Converter schematic, thermal PCB layout, clamp and measured duty are open. |
| 1.10–1.13 harness/bus | Preliminary specification | [Harness](05-harness/README.md) and [bus contract](04-pcbs/feetech-link-contract.md) record 5264-3P, pinout, supply separation and W42 budget. PCB-12 transceiver VIH/VIL, contention and mixed-rail behavior remain bench B5 and schematic gates. |
| 1.14–1.15 firmware/interface | Build contract authored | [Bus contract](04-pcbs/feetech-link-contract.md) gives packet, IDs, 1 Mbps, homing, ±58° yaw counts, dead zone and fault state. This repo contains no C2 firmware implementation to update. |
| 1.16–1.18 ledger/BOM | Updated | `BOM.csv`, head/body BOMs and `decisions.md` carry candidate hardware, tools, horn/screw procurement holds, BO-056/061 holds and D-044 index repair. |
| 2.1–2.7 / 2.9 head CAD | Reference and exact neutral-pose screen ready; refit open | The reference STEP is validated. [Head fit report](03-head/v1/cad/feetech-head-fit.md) checks four clockings against the 100-entry live head source. Lateral roll ears and rearward pitch ears are preferred trials, but the rear cover/trim/strap and pitch trunnion/cradle/adapter intersect. Live `layout_model.py`, `details.py`, `mass_layout.py`, `axes.json` and derived outputs remain the XC330 build. No production mount or new A0 solution may be inferred from photo-estimated details. |
| 2.8 / 2.10 head FEA / print edge | Open | Redesign the pitch frame and roll saddle first, then run the RP-06 FEA method and watertight mesh check. |
| 3.1 yaw bay | **Integrated in the live body model (D-048); physical fit under review** | HS on the true horn axis (the trial screens were 25.5 mm off), horn up, case −X, 7.6 mm lower; Pi/cooler/tray/PCB-09 shifted +10 X / −6 Y. The original yaw checker hid a 0.8 mm mount-hole axis error. The CAD axes and checker are corrected, and the current `check_yaw_stage.py` run passes with four zero axis offsets. Received-part dimensions still need checking. |
| 3.2–3.9 / 3.11 body CAD/electrical layout/stability | CAD integration under review (D-048) | Clamp-ring mount, BO-056 hub and BO-061 screws modelled. The corrected yaw-stage, current frame-fit and cooling checks pass. The compute checker passes again after the Pi USB-C plug was specified as a down-exit right-angle plug with a body ≤ 13 mm (HN-010; reserve 1.74 mm from the C3 DevKitC). The 0.30 N·m yaw limit is an unimplemented/uncalibrated assumption, and the PETG tooth estimate at that limit exceeds its screen flag. Neutral a_tip is 1.667 (current head tree) / 1.621 with the STS3045M mass-only what-if. Open: shell fit, buying a plug that meets the HN-010 envelope, gear/protection proof, PCB-03 converter, exports and head re-balance. |
| 3.10 mic noise | Bench gate open | Add the closer/faster yaw servo to the AR-61 mic noise test before PCB-06 release. |

Release order: verify the provisional yaw packaging against received hardware;
complete the cradle, BO-056 hub, compute tray and PCB-09 source integration;
redesign the head mounts/horns; solve the head mass/axes and verify all
mechanical clearances; regenerate body/chassis stability and §11.3/P07; then
run B1–B6 and freeze the electrical/firmware thresholds from those results.
