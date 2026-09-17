# RP-02 Part 3 — Compute and Control Architecture

| Field | Value |
|---|---|
| Status | **v1.3 design baseline; `RP02-P3-REG-01` registered the Part-3 architecture, `RP02-P3-REG-02` corrected C3, the 2026-09-16 cost review revised only the differential-transceiver implementation lead, and 2026-09-17 noted the RP-03 pin map v0.1 / `CA-14` draft fill.** Hardware purchase remains separately authorized; G04/G05 and physical qualification remain open |
| Owner | Project builder |
| Created | 2026-09-16 |
| Consumes | `RP02-P1-REG-01`; `RP02-P2-REG-01…03`; selected Raspberry Pi 5 2 GB, Waveshare ESP32-S3-Zero C2 and display SKU 30493; `link-contract.md`; `../../01-system/timebase.md` |
| Closes at design level | Compute/control ownership, base-controller class, runtime-process boundaries, physical links, watchdog chain, boot/arm/recovery and update/logging rules |
| Does not close | ADR-03/ADR-12, exact base motor driver/sensors (RP-03 leads only), servo transceiver, numeric watchdog/timeout registration, measured timing/thermal/resource margin, purchase |

Part 3 does not ask how many processors fit. It asks **which processor is allowed to decide what, what survives when another processor fails, and what evidence proves that boundary under concurrent operation**. This document is the single ownership map. `link-contract.md` remains the byte/message ICD; the power documents remain the rail authority.

## 1. Decision in one view

```text
network / control app / cloud
              |
              v
  C0 Raspberry Pi 5 2 GB, body, Linux
  perception · audio · behaviour · expression timeline · logging · UI
              |
              +==== full-duplex differential UART ==== C2 head safety MCU
              |                                        trajectories · limits
              |                                        expiry · servo bus
              |                                              |
              |                                      local RS-485 relay
              |                                              |
              |                                      display ESP32-S3
              |                                      semantic face renderer
              |
              +==== full-duplex differential UART ==== C3 base safety MCU
                                                       wheel control · odometry
                                                       cliff/bump/IMU reflexes

E-stop + ENERGY_OK + C2_READY + C3_READY + SYSTEM_ARM -> hardware motor gate
                 ^                         ^
          external window watchdogs, independent of Linux
```

The architecture has one application computer and three bounded embedded roles:

| Node | Selected hardware | Authority | Explicitly forbidden |
|---|---|---|---|
| `C0` application compute | **Raspberry Pi 5, 2 GB**, body-mounted | Perception, person continuity, invocation/NLU, behaviour and action lifecycle, expression composition, audio, control-app API, run logging, master monotonic time | Raw PWM, motor commutation, unbounded motion streaming, hardware motor permission, treating cloud/network health as safety truth |
| `C2` head control | **Waveshare ESP32-S3-Zero**, head-mounted | `MJ5/MS7/TRACK/BRAKE`, cross-axis setpoints, hard/soft limits, command expiry, head fault response, servo-bus ownership, C2 readiness | Behaviour selection, camera inference, face rasterization, automatic re-arm after reset/link/E-stop recovery |
| `C3` base control | **Espressif ESP32-S3-DevKitC-1-N8** for RP-03/RP-02 rigs; a WROOM-1-N8 carrier may replace it only through controlled equivalence | Wheel velocity loops, encoder capture, base IMU, cliff/bump/proximity inputs, local stop/reflexes, acceleration/velocity envelope, odometry capture, base command expiry, C3 readiness | Following/person choice, high-level path intent, relying on Linux scheduling for the stop path |
| `D1` face renderer | Selected Waveshare ESP32-S3-LCD-4.3 no-touch SKU 30493 | Local assets, eye/utility animation, brightness, frame flip and expiry-to-idle | Motion, motor permission, behavioural authority, raster traffic from C0 |
| Smart actuators / motor drivers | Family-specific, still open where noted | Local current/position/velocity actuation and hardware fault telemetry | Gesture timing, person-facing behaviour, permission to ignore C2/C3 inhibit |

No fifth “power MCU” is added in V1. Loaded-source truth and rail-present signals are hardware-observed and delivered to both safety controllers under `BR-01`; adding a single supervisory MCU would create a new common point of failure without yet owning a necessary control loop.

## 2. Registered architecture rules (`CA-*`)

### `CA-01` — Linux expresses intent; embedded controllers enforce physics

C0 emits semantic, expiring goals. C2/C3 independently clamp them to compiled limits, reject stale or incompatible intent, and execute bounded trajectories. A Linux thread, ROS node, network process or cloud response is never part of a motor-current or hazard-stop loop.

This carries the recurring pattern from Vector (Linux brain + small body MCU), TurtleBot 4/Create 3 (Pi application layer + base controller with local hazards and stale-command stop), Stretch (host software above firmware safety modes), and Reachy (SDK/ROS/HAL layered above hardware control) without importing their full middleware stacks.

### `CA-02` — One controller owns each actuator bus

- C2 is the only master of the head servo bus.
- C3 is the only owner of base PWM/direction or base smart-motor bus.
- D1 alone owns the panel and LVGL render loop.
- C0 never opens those device buses directly.

One process and one MCU task own each physical transport. Other software uses typed messages. This prevents two writers, partial transactions and “helpful” debug tools from moving hardware behind the safety owner.

### `CA-03` — Base safety is a separate MCU and uses the same family as C2

C3 is mandatory before powered locomotion. On-SBC wheel control is rejected by AD-04 and the ≤50 ms detection-to-deceleration constraint. ESP32-S3 is selected for C3 to keep one ESP-IDF toolchain, one HAL shape, one watchdog strategy and reusable framing/time-sync code.

The RP-03 prototype uses the official ESP32-S3-DevKitC-1-N8 because body volume is not constrained, C3 needs no PSRAM, and the N8 module preserves GPIO35–37. The initially considered N8R8 uses octal PSRAM and consumes those three pins internally; it is not a silent substitute. A later custom WROOM-1-N8 carrier is a packaging/cost change, not an architecture change, provided it preserves firmware, pins by logical role, external watchdog, debug access and all qualification results.

### `CA-04` — The head has one body ingress

The previously open relay alternative is adopted. C0 talks only to C2 across the moving boundary. C2 forwards `FACE_STATE` and `LIGHT_STATE` to D1 through a bounded, lower-priority queue; D1 status returns through the same relay.

Consequences:

1. there is one session/clock model for the whole head;
2. D1 failure cannot block C2 motion tasks;
3. C2 restart makes the face decay to idle but cannot leave motion authorized;
4. display traffic is dropped before head-control traffic under congestion;
5. asset transfer is allowed only while head motion is inhibited and uses a separate maintenance mode.

### `CA-05` — Differential UART is the production physical layer

The `link-contract.md` COBS, CRC, sequence, expiry and time messages stay unchanged. The production electrical layer becomes **full-duplex RS-422/RS-485 signalling** over two twisted pairs plus the registered common reference:

| Link | Electrical layer | Candidate rate | Reason |
|---|---|---:|---|
| C0 ↔ C2 | Two full-duplex differential pairs; THVD1451-class 3.3 V transceiver at each end | 921,600 baud | Motor-adjacent moving harness; no turnaround/collision state; keeps the proven UART software model |
| C0 ↔ C3 | Same differential physical layer | 921,600 baud | Same carrier and diagnostics; base motor noise must not be allowed to falsify commands |
| C2 ↔ D1 | Head-local half-duplex RS-485 using D1's existing RS-485 path and one C2 transceiver | 115,200 baud initially | Semantic face traffic is small; short local run; no second yaw-boundary link |
| C2 ↔ head servos | Family-specific half-duplex TTL or RS-485 | Family-defined | Remains bus-neutral until RP-01 freezes the actuator family |

Bare 3.3 V TTL remains a bench-loopback mode only. USB-CDC remains a recovery/diagnostic option, not the operating link: it complicates branch independence and consumes C2's native-USB service path.

`THVD1451D` in 8-SOIC is the prototype implementation lead, not a purchased suffix. It is a 3–5.5 V, full-duplex 50 Mbps part with ±15 V common-mode range, open/short/idle fail-safe behavior and ±18 kV IEC-contact ESD protection, comfortably above the chosen baud. The VSON suffix is a later assembly-cost option only when placement/inspection/rework capability makes it cheaper in the complete carrier. Termination, common reference, protection network, power-off loading and exact suffix close on the carrier schematic and harness measurement.

### `CA-06` — Pi GPIO allocation reserves independent transports

The Pi 5 RP1 exposes five PL011 UARTs. The initial, conflict-aware allocation is:

| Function | Pi 5 peripheral / pins | Rule |
|---|---|---|
| Head link | UART0, GPIO14 TX / GPIO15 RX | Linux console disabled on this UART; routed through the head differential transceiver |
| Base link | UART2, GPIO4 TX / GPIO5 RX | `uart2-pi5` overlay; routed through the base differential transceiver |
| Power/housekeeping | I²C1, GPIO2/3 | Local body PCB only; never crosses a joint |
| Audio TDM/I²S reservation | GPIO18–21 | Preserved for RP-05 microphone/playback decisions |
| SPI/service reservation | GPIO8–11 or later conflict-free set | Must be audited against any final HAT/carrier before PCB freeze |

The exact device names are discovered by stable udev aliases, never hard-coded `/dev/ttyAMA*` enumeration. A boot self-test records the active pin mux and refuses arm if the expected links are absent or mapped differently.

### `CA-07` — No ROS 2 or micro-ROS in the V1 safety path

ROS 2 may be introduced later for simulation, visualization or a capability that materially earns it. V1 does not use DDS between C0 and the MCUs, and the MCUs do not run micro-ROS. The topology is fixed, the traffic is small, and the existing ICD requires stricter expiry/session behavior than a generic pub/sub graph gives by default.

On C0, use a small typed local IPC surface over Unix-domain sockets. Protobuf is permitted for C0-only IPC and control-app APIs; the MCU wire format remains allocation-free packed records generated from one schema. No network listener can publish directly to a motor link.

### `CA-08` — C0 uses bounded process isolation, not a process per feature

| Service | Owns | Failure response |
|---|---|---|
| `makad-core` | Operating vector, person continuity, action lifecycle, behaviour authority, expression schedule, fresh-intent epoch | Loss invalidates the authority lease; `makad-hwd` sends inhibit once, stops refreshing authorization and flushes outbound intent |
| `makad-hwd` | Both serial devices, framing, time sync, MCU sessions, power/health inputs, bounded command queues, immutable event capture | Never invents/continues a behaviour. Link or codec fault isolates that endpoint and reports it to core |
| `makad-perception` | libcamera capture, face/person observations and uncertainty, capture timestamps | Observation becomes stale/unavailable; no direct actuator access |
| `makad-audio` | Capture/playback device, wake front end, astromech playback timing | Audio channel degrades independently; no direct actuator access |
| `makad-edge` | Control app, cloud/NLU/Spotify adapters, authentication and backoff | Network loss is an external-service state, not a reboot or safety event |

`makad-core` and `makad-hwd` are the minimum running pair for normal interaction. Media processes are isolated because camera/audio drivers can block or restart. More process boundaries require evidence that they improve containment enough to justify memory, IPC and diagnostic cost on a 2 GB system.

### `CA-09` — Authority is a renewable lease, not “process exists”

Every motion command carries the C0 boot UUID, a monotonically increasing session epoch, sequence, source timestamp and expiry. `makad-core` renews an authority lease to `makad-hwd` from the same event loop that advances action state. A timer thread that remains alive while the core is wedged cannot renew it.

On lease loss, `makad-hwd`:

1. emits one `HEAD_INHIBIT` and `BASE_INHIBIT` if the links are writable;
2. drops both outbound queues;
3. stops the valid heartbeat/session stream;
4. continues receive-only evidence capture if possible.

C2/C3 then brake on local command/heartbeat expiry even if the inhibit frame was lost.

### `CA-10` — Three watchdog layers, with hardware withdrawal of readiness

| Layer | Mechanism | Required outcome |
|---|---|---|
| MCU internal | ESP-IDF interrupt watchdog + task watchdog configured to panic/reset; subscribed safety/control tasks | Detect blocked ISR/task scheduling; reset into inhibited boot |
| MCU external | TPS3436-Q1-class **window watchdog** per C2/C3 carrier; feed edge generated only after one complete healthy safety-loop cycle | Too-early, too-late or absent feed deasserts the controller's hardware-qualified READY path and resets/latches per final suffix/circuit |
| SBC service | systemd `Type=notify`, `WatchdogSec`, bounded restart policy; notification gated by real loop progress | Restart only the failed service; never substitute for MCU expiry |
| SBC host | Pi hardware watchdog through systemd only after bench validation | Recover a wedged host; C2/C3 have already inhibited motion long before reboot |

`C2_READY` and `C3_READY` are not raw GPIO-high claims. Each is ANDed with its external watchdog-good output and pulled inactive when the MCU is unpowered, resetting or disconnected. Debuggers disabling ESP watchdogs do not disable the external device. The exact watchdog window is registered from measured worst-case loop time, not chosen from a round number.

### `CA-11` — Local reflexes outrank remote intent

C3 applies this priority, highest first:

1. hardware E-stop / motor-gate loss;
2. energy or controller-readiness loss;
3. cliff, pickup/tip, encoder implausibility, driver fault and registered obstacle envelope;
4. command expiry / C0 session loss;
5. explicit base inhibit/cancel;
6. valid authored/follow command;
7. procedural micro-motion.

A higher-priority condition can clamp, brake or reject a lower one. Clearing a condition reports availability but does not replay or resume old intent. Create 3's local hazard/reflex and stale-velocity behavior is the direct precedent; Makad retains its stricter fresh-arm rule.

### `CA-12` — Loop and publication rates are contracts with measured margin

| Node/function | Design rate | Deadline rule |
|---|---:|---|
| C2 trajectory task | 200 Hz minimum | p99 jitter ≤10% of 5 ms period; already a G05 candidate |
| C2 servo transaction | 100 Hz minimum for 3 axes | Must complete with telemetry before the next scheduled transaction; exact bus budget waits on family |
| C3 wheel control | 500 Hz target | Motor-driver and encoder evidence may revise upward/downward; ≤50 ms detection-to-deceleration remains invariant |
| C3 hazard scan/fusion | 200 Hz target | No single sensor age may silently exceed its registered bound |
| C2/C3 telemetry | 100 Hz state, 20 Hz heartbeat | Event faults transmit immediately and remain latched in heartbeat |
| D1 render | 30–40 fps acceptance direction | Face expiry and idle continue locally if C0/C2 disappear |
| C0 behaviour schedule | 50–100 Hz | Not safety-critical; missed deadline stops lease renewal rather than producing a late burst |

All tasks use fixed-capacity queues. Control/state replaces older values (“latest wins”); faults are latched; configuration and arm messages require ACK. There is no unbounded FIFO anywhere in the motion path.

### `CA-13` — Boot and arm is a two-phase commit

1. Power rails become valid; external motor gate stays open.
2. C2/C3 boot inhibited, initialize outputs safe, validate compiled configuration and start watchdogs.
3. C0 boots; systemd starts `makad-hwd`, then media, then `makad-core`.
4. Each MCU completes `HELLO`, contract/firmware compatibility and time-sync bootstrap.
5. C0 sends limits/configuration; MCU clamps and echoes the effective set.
6. Floor/Table mode is freshly selected where required; E-stop, energy and all installed-controller readiness are checked.
7. C0 issues a new arm nonce and epoch. Hardware `SYSTEM_ARM` may then be latched.
8. Only fresh post-arm goals are executable.

Reset or reconnect returns to step 2 or 3. Releasing E-stop, restoring a rail, restoring network or receiving a delayed ACK never jumps to step 7.

### `CA-14` — Configuration has one generated source and two limit layers

A versioned machine-readable configuration source generates:

- C0 schema/types and human-readable manifest;
- C2/C3 compiled **hard maxima** and board-role pin maps;
- runtime soft limits sent in `LIMITS_SET` / base equivalent;
- run-record configuration hash.

Runtime soft limits may only tighten compiled maxima. A hash mismatch blocks arm. Calibration values are separate from limits, CRC-protected, versioned and reported in `HELLO`; an unreadable calibration puts the affected axis/subsystem unavailable.

RP-03 Part 4 (`RP03-P4-REG-01`) supplies the C3 half of this source as a **draft**: pin map v0.1 and `BASE_LIMITS_SET` field list in `../RP-03-locomotion/base-control-architecture.md`. The generated board-role header and compiled hard maxima are still unbuilt. Byte layouts stay open. The pin map is a pre-carrier gate, not a SKU freeze.

### `CA-15` — Updates and service access require physical inactivity

- C2/C3 radios are disabled at build time; there is no MCU Wi-Fi/BLE control or OTA path in V1.
- Firmware update requires the motor domain physically unavailable, a service connection and a release manifest naming compatible protocol/config versions.
- C2 native USB remains accessible through the head service path; C3 keeps both native USB and USB-UART access in the body.
- D1 assets may update while stationary with motion inhibited; D1 firmware uses its own service procedure.
- C0 system updates occur only in maintenance state. A failed update boots or restores a known-good image/card; no autonomous update runs during a scored or normal interaction session.

### `CA-16` — Logs are bounded and diagnostic, not a new load fault

Every event record includes master timestamp, raw local timestamp where applicable, boot UUID, session epoch, source, type, sequence/config/firmware hashes and health. `makad-hwd` writes an append-only binary ring; human logs use rate-limited journald. Scored runs export the immutable ring into the run folder.

Normal operation must cap log space and write rate. “Disk full” is an injected fault: nonessential capture stops, safety/control continues, health becomes degraded, and no reboot loop is allowed. The selected storage path and log policy must pass repeated abrupt-power and endurance tests before ADR-03 closure.

## 3. Base-controller I/O budget

The exact driver and sensors remain RP-03 decisions, but C3 is only credible if it reserves their interfaces now.

| Function | Signals / peripheral budget | Notes |
|---|---:|---|
| Two encoder channels | 4 GPIO with edge capture / PCNT | Quadrature A/B for left/right |
| Two motor commands | 4–6 GPIO / 2 PWM units | PWM + direction, or PH/EN driver-specific mapping |
| Driver faults/current alerts | 2–4 GPIO/ADC | Hardware fault inputs preferred; current telemetry sampled locally |
| Cliff/proximity/bump | 4–8 GPIO/ADC/I²C | Safety scan local to C3; no USB sensor in the stop path |
| Base IMU | 1 SPI + interrupt preferred | Rigidly mounted to base; capture timestamp at interrupt |
| C0 link | UART TX/RX | Behind differential transceiver |
| E-stop / `ENERGY_OK` / motor-present | 3 inputs | Independent signals, safe pulls, avoid strapping pins |
| READY / watchdog feed / debug | 3–5 signals | External window watchdog and qualified READY are carrier functions |

The N8 DevKitC exposes 36 header GPIO before reservations. The gross budget above spans **27–37 signals** before bus sharing and driver-specific simplification. Avoiding strapping GPIO0/3/45/46 for safety-critical outputs and reserving GPIO19/20 for native USB plus GPIO43/44 for USB-UART leaves 28 ordinarily assignable header GPIO (27 if the board RGB LED is retained). Therefore the selection is credible but tight, not “ample”: the RP-03 pin map is a hard pre-carrier gate and must retain at least two unassigned safe GPIO after all direct safety inputs, watchdog and debug reservations. Safety-critical inputs may not be hidden behind a general GPIO expander merely to make the count fit. If the map fails, move to a WROOM-1-N8 carrier with the required direct I/O or change the driver/sensor interface through change control; do not fall back to N8R8.

## 4. Resource and thermal acceptance on C0

The 2 GB selection is not justified by an invented workload estimate. It remains selected and receives these measurable acceptance rules under `CC-PEAK-01` and `ST-01`:

| Quantity | Acceptance direction before registration |
|---|---|
| Memory | No OOM kill; swap activity zero during scored interaction; sustained `MemAvailable` margin recorded, target ≥20% |
| CPU | Per-service utilization and run-queue latency recorded; `makad-core`/`makad-hwd` lease deadlines remain clean during camera + audio + UI + logging |
| Thermal | No thermal throttling in final body airflow at registered ambient; CPU temperature and cooler RPM logged |
| Storage | No I/O stall that violates authority lease; bounded write rate; abrupt-power recovery and filesystem check pass |
| Startup | Cold-boot-to-inhibited-health and cold-boot-to-arm-ready recorded separately; neither permits motion automatically |

The **official Raspberry Pi 5 Active Cooler is selected** for the prototype configuration. Passive-only cooling is rejected for a camera/audio workload until measurements prove equivalent margin. Enclosure ducting and acoustic impact remain physical evidence, not assumptions.

## 5. Qualification additions created by Part 3

These obligations extend, not replace, G04/G05 and the Part-1 fault campaign:

| ID | Injection | Required result |
|---|---|---|
| `F-23` | Freeze `makad-core` while its process remains alive | Authority lease expires; both MCUs brake/inhibit; no queue replay after service restart |
| `F-24` | Freeze `makad-hwd` / stop serial progress | MCU heartbeat expiry contains motion; systemd restarts the service; new sessions remain inhibited |
| `F-25` | Stop C2 external-watchdog feed; separately feed too early | Qualified `C2_READY` withdraws and head motor permission drops; reset reason exposed; fresh arm required |
| `F-26` | Same on C3 during base motion | Qualified `C3_READY` withdraws; base stops within registered bound; no old velocity resumes |
| `F-27` | Flood display relay / hold D1 bus busy | C2 loop and head link retain timing; display traffic drops/degrades; motion stays bounded |
| `F-28` | Corrupt one differential pair / remove termination | CRC/sequence health exposes degradation; registered error threshold inhibits; no valid-looking corrupted command executes |
| `F-29` | Fill C0 log partition or force slow writes | Nonessential logging stops/degrades; authority and MCU links stay within deadlines |
| `F-30` | Reset C0, C2, C3 and D1 one at a time and in plausible brownout order | Each node boots inactive; compatibility/time/limits/arm sequence required from the beginning |

Additional G05 metrics:

- C2 and C3 control-loop p50/p95/p99/max period and jitter under their worst registered local loads;
- end-to-end inhibit latency for process lease, link loss and hardware watchdog paths;
- link CRC/sequence errors per hour on static and flexing/noisy harnesses;
- C0 scheduling/memory/thermal margin during `CC-PEAK-01` and `ST-01`;
- D1 relay flood isolation;
- watchdog window margin and false-trigger count across boot, operation and maintenance.

## 6. Prior-art conclusions actually used

| Reference | Observed practice | Makad consequence |
|---|---|---|
| [Vector hardware/software architecture](https://os-vector.github.io/vector-docs/5.-Hardware/index.html) and [TRM](https://randym32.github.io/Vector-TRM.pdf) | Linux SoC owns character/perception; small MCU owns body I/O over simple serial; services are separated by role | Keep semantic Linux/MCU split and boring framed serial; do not copy Vector's heavy head placement |
| [TurtleBot 4 overview](https://turtlebot.github.io/turtlebot4-user-manual/software/overview.html) | Pi application computer is distinct from Create 3's base processor | Separate C3 is mandatory |
| [Create 3 movement](https://iroboteducation.github.io/create3_docs/api/moving-the-robot/), [safety](https://iroboteducation.github.io/create3_docs/api/safety/) and [reflexes](https://iroboteducation.github.io/create3_docs/api/reflexes/) | Last velocity expires; hazards and reflexes pre-empt user commands locally | Local expiry/reflex priority on C3; stale motion is never held indefinitely |
| [Stretch safety features](https://docs.hello-robot.com/0.2/stretch-tutorials/stretch_body/tutorial_safe_coding/) and [firmware](https://github.com/hello-robot/stretch_firmware) | Firmware safety mode/runstop plus monitor/sentry above; distributed controller boards are diagnosable | Separate firmware containment and application health; do not confuse warning/reporting with motor inhibit |
| [Reachy software architecture](https://pollen-robotics.github.io/reachy-2023-docs/advanced/software/presentation/) | HAL/control/API layers make ownership explicit | Preserve a hardware daemon boundary without importing ROS 2 for V1 |
| [ESP32-S3 watchdogs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/wdts.html) | Interrupt/task watchdogs cover different scheduling failures; default task-watchdog behavior must be configured for reset | Subscribe real safety tasks and enable panic/reset; add an external window watchdog |
| [ESP32-S3 UART/RS-485 support](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-reference/peripherals/uart.html) | Hardware/driver support exists for RS-485 modes and collision/error reporting | Use differential physical layers while retaining the UART protocol |
| [THVD1451](https://www.ti.com/product/THVD1451) | 3–5.5 V full-duplex differential transceiver with extended common mode, fail-safe behavior, strong IEC ESD protection and ample data-rate headroom | Cost-down production head/base link lead; SOIC for prototype, VSON only with qualified assembly |
| [TPS3436-Q1](https://www.ti.com/lit/ds/symlink/tps3436-q1.pdf) | Window watchdog detects early and late feeds and offers latched-output variants | Hardware-qualify C2/C3 readiness; exact timing/suffix follows measurement |
| [Pi 5 RP1 peripherals](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008370-DS-1-rp1-peripherals.pdf) | Five PL011 UARTs and explicit GPIO alternate functions | Reserve independent head and base UARTs without stealing the audio pins |
| [systemd watchdog API](https://www.freedesktop.org/software/systemd/man/latest/sd_watchdog_enabled.html) | Service watchdog keepalive must arrive within the configured interval | Service recovery is layered above, never substituted for, MCU expiry |
| [Pi 5 Active Cooler](https://www.raspberrypi.com/products/active-cooler/) | Dedicated temperature-controlled cooler for sustained Pi 5 load | Select it and validate inside the body |

## 7. What is fixed and what remains evidence-gated

**Fixed by `RP02-P3-REG-01`:** node roles; separate C3; ESP32-S3 family; one head ingress with C2 display relay; differential production links; no ROS/micro-ROS safety path; C0 service boundaries; authority lease; three watchdog layers; two-phase arm; radio-off MCU policy; official Pi Active Cooler. **Corrected by `RP02-P3-REG-02`:** C3 prototype suffix is DevKitC-1-N8, not N8R8, to preserve GPIO35–37.

**Still open without weakening the architecture:** exact RS-422 transceiver suffix and protection network; external-watchdog suffix/window/latch circuit; **C3 pin map v0.1 exists as an RP-03 design-definition draft** (`RP03-P4-REG-01`) and still awaits carrier/firmware generation; motor driver and base sensors unselected (D02/S01/S04/S06/S07 are leads, not a freeze); servo transceiver; storage SKU; numeric timeouts; final PCB/carrier; all G04/G05 evidence and purchases.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-09-16 | 1.0 | Created and registered the Part-3 ownership, links, runtime, watchdog, boot/recovery and qualification baseline under `RP02-P3-REG-01`; selected the initial prototype C3 board suffix and Pi Active Cooler; no purchase or gate outcome. |
| 2026-09-16 | 1.1 | GPIO audit corrected the C3 prototype from DevKitC-1-N8R8 to DevKitC-1-N8 under `RP02-P3-REG-02`: C3 needs no PSRAM, while N8R8 consumes GPIO35–37. Added explicit reservation/margin rules. All other Part-3 decisions unchanged. |
| 2026-09-16 | 1.2 | Cost-down sourcing review replaced the MAX3490E implementation lead with THVD1451D SOIC while preserving the registered full-duplex differential topology. No architecture rule, purchase, gate or exact schematic suffix was registered. |
| 2026-09-17 | 1.3 | Noted RP-03 pin map v0.1 and `BASE_LIMITS_SET` draft as the C3 fill of `CA-14` / §3. The map retains ≥2 spare safe GPIO. Not `RP02-P3-REG-03`. No purchase, no pin freeze, no G05 evidence. |
