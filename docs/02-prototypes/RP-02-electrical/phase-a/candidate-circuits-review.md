# RP-02 Phase A candidate circuits and paper review — 2026-09-17

**Status:** paper configurations, not schematics for build or selections. Candidate IDs and their sourced limits are in `../power-component-candidate-screen.md` and `../compute-control-component-screen.md`. No values here are measured, no protection rating is frozen, and G01/G06 remain unscored.

## Candidate circuit boundaries

| Circuit | Paper signal/energy path | Candidate parts | Required pre-schematic calculation or check |
|---|---|---|---|
| Compute | `PB-MAIN` → branch protection → dedicated 5.1 V converter → output measurement/hold-up → Pi 5 power entry; return paired to star | `PCD-PRO-01` + `PCD-CVT-01`, with `PCD-CVT-02` rework comparison | Minimum-source/5 A transient regulation, 100 mV steady drop allocation, inrush versus branch trip, Pi power-entry policy, converter heat and off-state back-power |
| C2 safety | `PB-SAFE-C2` independent input protection → its own 5 V converter → local hold-up/PG → Zero; C2 READY hardware-qualified | `PCD-PRO-02` + `PCD-CVT-06`; `PCD-CVT-07` bench substitute | Startup at installed load/capacitance, UVLO/PG sequence, brownout stop reserve, reverse current and safe boot GPIO levels |
| Display | `PB-DISPLAY` independent protection → separate 5 V converter → D1; enable restricted in charge mode | `PCD-PRO-02` + second `PCD-CVT-06`; `PCD-CVT-08` bench substitute | 0.70 A planning peak, inrush, charge-mode source selection and no C2/display back-feed |
| Motor E-stop | Source-adjacent main fuse → hardware motor-arm switch → `PB-MOTOR`; NC mushroom loop and separate fresh `SYSTEM_ARM` permission both required; diagnostics remain on safety rail | `PCD-PRO-03` family, `PCD-EST-01`, `PCD-EST-02` external-FET approach | Fault-current range, FET/shunt SOA, regeneration path, interruption/discharge, fault-loop wetting and fuse coordination. No switch or fuse value selected |
| C0↔C2 | Pi UART0 → body full-duplex transceiver → two twisted pairs/common reference across yaw → head transceiver → C2 UART; protect each connector boundary, terminate each receive pair at the physical end | `CCD-LNK-05` THVD1451D lead and `CCD-HDL-01/02` carriers | Termination/bias values, TVS capacitance and common-mode, power-off loading, cable flex/length and G05 CRC/noise window. Do not assume a pin-compatible alternative |

The C2 carrier reserves the UART transceiver, watchdog feed and hardware-qualified READY, safe-pull E-stop/motor-present/energy inputs, servo bus transceiver footprint left open for RP-01 family, and test points for each rail and link pair. External window-watchdog **family** is fixed by Part 3, but suffix/window/latch circuit follows measured boot and loop timing. C3 carrier reserves only link, E-stop, energy, READY and watchdog functions; RP-03 owns motor driver, sensors and their pin map.

## G01 paper walk

| Check | Review finding | What prevents closure |
|---|---|---|
| Source isolation and bounded paths | `PA-*`/`PB-*` tree has a retained pack disconnect, main protection, branch protection and independent safety branches in the intended path | Pack assembly and exact installed protection/connector/wire ratings absent |
| Motor-arm and E-stop precedence | Hardwired NC loop is separate from `SYSTEM_ARM`; release cannot authorize motion by the Part-2/4 contracts | Switch/FET/shunt schematic and F-12/F-13 injection absent |
| Returns and back-power | Paired return/star intent and partial-power injection are named | Carrier nets, shield termination and off-state measurements absent |
| Selectivity and thermal | Calculation ledger gives method; candidate screen rejects clear mismatches | Actual path impedance, thermal curves and fault-current envelope absent |

**Paper result:** architecture is reviewable with explicit protection boundaries. No G01 pass or rating claim.

## G06 paper walk

| Check | Review finding | What prevents closure |
|---|---|---|
| Main isolation | Keyed, retained disconnect is in the architecture | Body placement/reach and selected connector absent |
| Charge inlet | Low-voltage keyed charge path and charge-mode display are defined | Chemistry, inlet/charger settings and body placement absent |
| Battery removal | Service separation is required | RP-06 enclosure route and timed procedure absent |
| Measurement points | Main and branch source/load-end points are named in rig/branch contracts | Carrier/body placement and probe-access demonstration absent |
| C2 service | Native USB and yaw demate are reserved | Installed head service access and timed replacement absent |

**Paper result:** no obvious missing service category in the current architecture. G06 remains open until the selected hardware is physically demonstrated twice and timed.
