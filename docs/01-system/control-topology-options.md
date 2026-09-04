# Makad V1 Control-Topology Option Study

| Field | Value |
|---|---|
| Status | **RP-01 C2 selected: separate ESP32-S3 motion controller; C1 rejected on selected carrier; exact C2 module remains open.** |
| Version | 0.8 |
| Owner | Project builder |
| Created | 2026-08-17 |
| Last reviewed | 2026-09-02 |
| Governed by | `risk-prototype-plan.md` — permitted provisional option study (decision-closeout: "the architecture phase may begin with provisional option studies while prototypes run") |
| Feeds | RP-02 (electrical/control backbone) → **ADR-06 (power)**, **ADR-12 (control topology)**; the monotonic-timebase deliverable (plan §104) |
| Consumes | `system-design-brief.md` responsibility set + AD-01/AD-06/AD-08; `mass-envelope-ledger.md` head section |

This document surveys **how to split Makad's computation and control across hardware**, grounded in how comparable robots are actually built. It selects nothing. A binding choice is made only when RP-02 closes with measured evidence and the relevant ADRs cite it. The purpose now is to (a) fix the vocabulary, (b) record prior art so we don't re-derive it, and (c) name the specific forks RP-01/RP-02 must resolve.

Nothing here overrides the foundation's deferral of processor, controller, battery, and framework selection.

## 1. The industry pattern: hierarchical, heterogeneous control

Every multi-actuator robot above toy complexity uses the same shape — a small number of processors, each matched to a timing tier, not one processor doing everything. The rule, stated bluntly in the humanoid-timing literature: *no single processor type can satisfy all timing requirements.*

| Layer | Typical host | Rate | Makad jobs |
|---|---|---|---|
| High-level | Linux SBC / GPU | 10–60 Hz | vision/perception, NLU + cloud adapters, behaviour authority, **semantic face state/assets**, audio; the selected head display performs final rasterization locally |
| Mid-level | SBC or RTOS | 100 Hz–1 kHz | trajectory shaping, subsystem coordination |
| Real-time | dedicated MCU + RTOS | 200 Hz–low kHz | servo/motor loops, encoder/IMU capture, limits, watchdog, command-expiry, E-stop |

A companion **separation principle** falls straight out of physics and applies directly to Makad: *proprioceptive* feedback feeds the fast inner loop **on the MCU**; *exteroceptive* sensing (the camera) feeds slower planning **on the SBC**. RP-01 is a stationary head with servo encoders providing joint angle, so it needs no runtime head IMU. Use an IMU only as a bench instrument for resonance/backlash work. When locomotion arrives, the runtime IMU belongs rigidly on the base: head placement would require subtracting neck motion from commanded angles and recreate the SPEC-09 timing-skew problem.

**Sources:** SiTime, *The Importance of Precision Timing in Humanoids*; RoboCup/UTRA *Global Systems Description* (Jetson TX2 for vision/AI + STM32 for real-time actuator control, linked by pub/sub over USB — "disentangles control from AI, reducing computational bottlenecks and improving reliability").

## 2. The direct precedent: Anki Vector / Cozmo

Vector is the closest shipped analog to Makad — WALL·E-inspired desktop droid with an **animated LCD face, camera, tiltable head, differential-drive base, IMU, mic array, speaker, status LEDs, and cloud NLU**. Its split is worth copying deliberately.

**Two boards:**

| Board | Contents | Role |
|---|---|---|
| **Headboard** ("the brains") | main SoC, RAM/storage, **camera, screen, Wi-Fi/BLE, IMU**, PMIC | perception, AI/SLAM, personality, **face rendering** |
| **Bodyboard** | *tiny* STM32F030 (8 KB RAM, 64 KB ROM), motor drivers, sensors, LEDs | sensors → frames up; frames → motors/LEDs down |

- **Internal link:** plain **RS-232 (CMOS-level serial) + USB.** No fieldbus, no micro-ROS.
- **Software:** three processes over Unix sockets — `vic-engine` (vision/SLAM/personality), `vic-anim` (face rendering, TTS, wake-word), `vic-robot` (talks to the body MCU).
- **Cozmo** (one size down): head PCB = NXP Kinetis M4 + camera + display; body = a Nordic BLE chip doing PWM + quadrature-encoder motor control.

**Three lessons Makad should carry forward:**

1. **Vector put the brain in the head, not the body** — because the camera, display, and IMU (the highest-bandwidth items) all live in the head, so the SoC went there to keep those buses short and send only motor/sensor traffic down a thin serial link.
2. **The body MCU is intentionally dumb and tiny** — a relay with local motor control, not a second brain.
3. **The internal link is boring serial** — two boards in one enclosure, short run → UART/USB is correct.

**The Makad difference that breaks the copy:** Vector's head tilts on **one** axis. Makad's head moves on **three** (roll/pitch/yaw — AD-02). An SoC + camera + display + IMU riding a 3-axis gimbal is far more moving mass and cable flex than Vector ever handled. So Vector answers "how to split," but not "where the compute sits" — that is §4.

**Sources:** os-vector.github.io hardware + software architecture pages; Vector TRM (Randall Maas); Fictiv and MicrocontrollerTips teardowns; anki vector-python-sdk `external_interface.proto` (semantic command surface: `SetHeadAngle`, `DriveWheels`, `DisplayFaceImageRGB`, `StopAllMotors`, event stream — a clean example of behaviour-level intents over a link, not raw PWM).

## 3. Communication bus — what to use and when

Field consensus, converging across the Thelliez robotics-bus breakdown, the CopperHill I²C-vs-CAN analysis, and the Vector teardown:

> **SPI for speed · I²C for local housekeeping · UART for simple point-to-point · CAN for robot wiring.**

| Bus | Good for | Wrong for | Relevance to Makad |
|---|---|---|---|
| **I²C** | sensors/peripherals **on the same board** (Nano's local IMU/mic/LED driver) | anything across a moving joint near motors — <1 m, ~400 pF limit, noise-sensitive | Fine *inside* the head node; **not** the head↔body link |
| **SPI** | fast local register access (IMU, ADC) | cabled runs across a limb | Local to a board only |
| **UART / USB-serial** | one SBC ↔ one/few MCUs in a shared enclosure; **fastest path to a working prototype** | many distributed noisy nodes | **Makad V1 internal link** |
| **CAN / CAN-FD** | 3+ distributed nodes on a noisy moving chassis; CRC + retransmit + fault confinement; up to 40 m | overkill for two boards in one shell | **Grow-into-it** if a 3rd node (power/base) earns it |

**On micro-ROS** (making each MCU a first-class ROS 2 node): the research points *away* from it for a solo V1. The Newton capstone documented *"Less is More: Why We Abandoned Micro-ROS for UART"* after a QoS/buffering interaction produced erratic motors and cost two weeks. The openvmp "why not micro-ROS" rule is the decision test: **if there is a permanent wired link and worst-case traffic won't saturate it, a dumb serial relay beats running DDS on a constrained MCU.** That is Makad exactly. Micro-ROS earns its place only once you are already on ROS 2, expect growth, and multiple engineers will touch the firmware.

## 4. The open fork: where does the compute sit?

The camera **must** ride in the head (AD-06). The real question is whether the **SBC** rides with it. Three candidates:

| Option | How | Pros | Cons | Verdict |
|---|---|---|---|---|
| **A. Vector-style (compute in head)** | SBC + camera + display + IMU in the head; dumb motor MCU in body | shortest camera/display buses; proven by Vector | heaviest 3-axis moving mass; power + data down to body; head-CAD must package an SBC | **Requires an explicit dimensional-baseline revision** because the current baseline body-mounts primary electronics; retain only as a fallback architecture |
| **B. Body-heavy (compute in body)** | SBC in body; head carries only camera + display + light | lightest head, easiest gimbal | **camera bus (MIPI/USB) must flex across 3 joints** — the fragility risk; display bus too | Cable-survival risk is the whole RP-01 concern |
| **C. Hybrid — SELECTED for RP-01** | SBC in **body**; ESP32-S3 motion firmware owns the head servo bus, limits, watchdog and command expiry; camera remains its own managed cable; the four-mic array remains body-mounted. **Selected C2:** a separate ESP32-S3 module runs motion while the display board renders. **Rejected C1:** motion and rendering share the display board's ESP32-S3. | Single motion-firmware target from the start; thin semantic body-to-head link; no runtime head IMU or Nano moving mass | Camera still crosses the joints; C2 adds a board, mount and harness. C1 lacks the required carrier I/O. | **C2 selected.** C1 is rejected for SKU 30493 and reopens only with changed/materially different hardware. |

The on-hand **Arduino Nano 33 BLE Sense** is a bench instrument, not an Option-C installed-controller candidate; see §6. RP-01 and RP-02 still validate timing, watchdog and electrical backbone, but they do not write the motion firmware twice on two MCU families.

### 4.1 Consequence of the selected 4.3-inch IPS module

The project builder selected and locked the no-touch **Waveshare ESP32-S3-LCD-4.3, SKU 30493**, which includes an ESP32-S3/LVGL renderer. Head-local display rasterization is therefore a fixed property of the display subsystem. RP-01 now also selects the separate C2 ESP32-S3 motion/safety boundary; the exact C2 module, wider compute placement, internal transport implementation and final RP-02/ADR closure remain open.

The selected path and its change-controlled architectural contingency are:

| Path | Body-to-head traffic | What must be installed in the head | Main risk |
|---|---|---|---|
| **D1: body rasterization — contingency only** | Continuous DSI/HDMI-class video across all three joints | Bare IPS panel plus receiver/host/power hardware | High-bandwidth flex life, restoring torque, connector service and SBC/panel compatibility; not active unless display change control is triggered |
| **D2: head rasterization — SELECTED display path** | Semantic face state, gaze/blink parameters, text/data and occasional asset updates over the eventual internal link | Waveshare ESP32-S3-LCD-4.3 no-touch SKU 30493 with local assets/LVGL | Approximately 106×68 mm board and a listed 118 g value must fit the mass/CoM envelope; rendering load and fault behaviour must be measured |

The selected display path is **D2 using Waveshare no-touch SKU 30493**. The body SBC owns behaviour and semantic face state; the head ESP32-S3 owns rasterization, animation playback and panel refresh. The exact wired transport remains open. HDMI does not solve the cable problem: with a body-mounted SBC it simply makes HDMI the moving high-bandwidth link.

The display ESP32-S3 is a **head-local co-processor**, not Makad's main brain: the body SBC still owns perception, behaviour and semantic intent. In C1, that same physical ESP32-S3 may also execute the local motion/safety firmware; this is a board-consolidation decision, not a transfer of system authority. The primary C1 mitigation is ESP-IDF dual-core affinity: keep rendering/communications on Core 0, pin the high-priority motion task to Core 1, and keep the servo ISR path IRAM-safe. ESP-IDF documents [pinned dual-core tasks](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/freertos_idf.html) and [Core-1/IRAM interrupt guidance](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/performance/speed.html). C1 would still need an on-the-same-chip before/after timing comparison with rendering off and on, plus fault containment evidence.

The **C1 electrical-feasibility gate fails on the selected carrier** before any timing test: it does not provide the required clean GPIO budget. C2 uses a separate ESP32-S3 motion-controller module class and is selected for RP-01; it runs the motion firmware from the start. Neither path makes the display board the main Linux/behaviour computer.

D1 and the DWIN module are now change-controlled contingency references, not active parallel candidates. Reconsider either only if SKU 30493 records a hard procurement, envelope, mass/dynamics, optical/animation or safety/reliability failure under the selection rule in `display-candidate-study.md`.

## 5. Time synchronization — the monotonic-timebase deliverable, grounded

The moment there is more than one controller there is more than one clock, and every distributed-robot source treats clock drift as a first-order problem: independent oscillators drift at several ppm, so *"the same instant" means something different to each node* — which shows up as an incoherent, laggy character (violating AD-01, "must feel like one character"). Options, heavy to light:

| Method | Accuracy | Cost | Fit for Makad |
|---|---|---|---|
| **PTP / IEEE-1588** | sub-µs | needs Ethernet + hardware timestamping | **Overkill** — what humanoids/AVs/cobots use |
| **NTP** | ~tens of ms jitter | software only | **Too coarse** for coordinated motion (AV teams abandoned it) |
| **PPS + shared-timer trigger, timestamp-at-source** | µs–ms | one MCU as timing master + serial offset reconciliation | **Right level for Makad** |

**Recommended provisional approach (implementable, no PTP hardware):**
1. Make **one node the time master** — a stable-timer MCU, or the SBC.
2. **Timestamp every scored measurement where it is captured** ("as close to the sensor source as possible" — the recurring Principle 4), not when it arrives at the SBC.
3. **Reconcile the SBC↔MCU offset over the serial link** with a periodic round-trip estimate (the MultiSense "crude NTP over the status channel" trick: halve the round-trip, average the offset).

This is the concrete shape of the plan's **monotonic event-time strategy** (§104) and a hard prerequisite for trustworthy RP-01…RP-07 scored data.

**Sources:** SiTime humanoid timing overview; arXiv *A General and Efficient System for Precise Sensor Synchronization* (Principles 1–4); arXiv *Simultaneous Triggering and Synchronization* (Teensy 4.1 + RTC PPS, MCU as PTP master to a Linux OBC); Carnegie Robotics MultiSense time-sync docs; Mayoral Vilches, *Distributed synchronization of industrial robots through ROS 2*.

## 6. Bench instrument: Arduino Nano 33 BLE Sense (on hand)

The Nano is **not installed hardware**, is excluded from the head mass ledger and does not host RP-01 motion firmware. It belongs with the PSU, soldering station and logic analyzer in `workbench.md`. Its nRF52840 supports **BLE only, not Wi-Fi**.

| Feature | Value to Makad |
|---|---|
| Onboard IMU | Bench-only resonance/backlash measurement when useful; never runtime RP-01 head hardware |
| Onboard PDM mic (Sense variant) | Candidate early DOA bench work toward the 13° target; not the approved body microphone array |
| APDS9960 | Candidate auto-brightness and proximity-startle bench prototype; neither is installed or Core scope |
| BLE | Optional debug path only; internal control remains wired. The nRF52840 has no Wi-Fi. |
| I²C / SPI / GPIO | Convenient on-bench sensor interfaces; not a reason to add the board to the moving head |

Register the exact Nano revision and the bench sensor configuration when it contributes evidence. A base-mounted runtime IMU remains a later locomotion decision; do not buy a SPI IMU or XIAO now.

### 6.1 C1/C2 head-node comparison

| Criterion | C1: one ESP32-S3 on the selected display carrier | C2: separate ESP32-S3 motion-controller module |
|---|---|---|
| Added moving hardware | None beyond M001/M002 display assembly | Added ESP32-S3 module, mount, connectors and local harness; own and weigh it as M008 |
| GPIO feasibility | **Fails on this carrier:** the future-ready screen is ten signals—SPI (4), half-duplex servo bus/direction (3), E-stop, fault and interrupt. Stationary RP-01 removes the IMU/interrupt need but still requires five clean motion/safety signals; this carrier plainly exposes only GPIO6. | Select a module with the full required pin budget before purchase |
| Timing isolation | Proposed mitigation only: rendering/communications on Core 0, motion task on Core 1, ISR in IRAM; must be measured on the same chip with rendering off then on | Physical isolation from display rendering; still prove motion timing and fault handling |
| Safety ownership | Local ESP32-S3 motion task would own limits, watchdog and command expiry | Dedicated ESP32-S3 owns limits, watchdog and command expiry |
| Runtime IMU | None for stationary RP-01 | None for stationary RP-01 |
| Firmware/tooling | Same ESP-IDF motion firmware, shared with display application | Same ESP-IDF motion firmware, deployed to a dedicated module |

The 2026-08-31 [official-schematic](https://files.waveshare.com/wiki/ESP32-S3-Touch-LCD-4.3/ESP32-S3-Touch-LCD-4.3-Sch.pdf) audit resolves C1 on this carrier: GPIO0/1/2/10/14/17/18/21/38–42/45/47/48 plus GPIO3/5/7/46 are LCD RGB/timing; GPIO11–13 are SD, GPIO8/9 are the shared I²C/CH422G path, GPIO15/16 the RS-485 path, GPIO19/20 USB/CAN, and GPIO43/44 USB-UART. GPIO6 is the only plainly exposed sensor GPIO. The CH422G expander cannot stand in for a deterministic servo bus, E-stop/fault or ISR path. Thus C1 fails both the original ten-signal screen and the reduced stationary-RP-01 five-signal screen. C1 may be reopened only if the received board materially differs from the official schematic or a new carrier is selected through change control.

### 6.2 Locked RP-01 runtime ownership

| Layer | Owner | Contract |
|---|---|---|
| Behaviour/perception | Body Linux SBC | Produces gaze/head goals, motion requests and cancellations; it does not stream raw PWM or depend on Linux timing for safety. |
| Face presentation | Selected display carrier's ESP32-S3 | Renders eye expressions, animation and panel refresh from semantic face commands. It does not own the RP-01 servo bus. |
| Head trajectory and safety | **Separate C2 ESP32-S3** | Instantiates and samples the registered `MJ5`/`MS7`/`TRACK`/`BRAKE` laws, synchronizes yaw/pitch/roll setpoints, applies limits, and owns watchdog, E-stop/fault handling and command expiry. |
| Actuator inner loop | Purchased smart servos | Closes the local motor/current/position loop around C2 setpoints and reports available position/current/voltage/temperature/fault telemetry. Servo-local interpolation may be used only as a measured low-level aid; it cannot own Makad gesture timing or cross-axis coordination. |

This boundary is selected for RP-01. Exact message schema, bus protocol, update rate and feedforward fields remain interface decisions, but they must preserve centralized, deterministic trajectory ownership on C2.

**Heterogeneity caution:** using *different* MCU families for head and base multiplies toolchains and debug surfaces for a solo builder. Vector's head-SoC vs body-STM32 split was heterogeneous **by necessity** (one must run Linux, one is a tiny motor relay) — not by preference. If a base MCU is added, prefer the **same family** as the head unless a role genuinely forces otherwise.

## 7. Selected RP-01 boundary and provisional wider-system recommendation

1. **Three roles, two RP-01 head boards:** a body **Linux SBC** for vision/NLU/behaviour, the selected head-local **ESP32-S3 display renderer**, and a separate **ESP32-S3 motion controller** for servo limits/watchdog/command expiry. C1 consolidation onto the display carrier is electrically blocked; C2 is not a second firmware implementation. A base/drive MCU with a base-mounted runtime IMU remains a later locomotion decision.
2. **Internal link: UART/USB serial**, Vector-style. Not CAN, not micro-ROS, not I²C across joints — those are documented "grow-into-it" options.
3. **Option C is the active RP-01 baseline.** RP-01 cable evidence and RP-02 still close the wider body/head transport and final system architecture; they do not reopen C1 on SKU 30493 without change control.
4. **Timebase: one master + timestamp-at-source + serial offset reconciliation.** Not PTP.
5. **Motor limits, watchdog, and E-stop live on the MCU, never on the SBC** — every source insists safety-critical loops must survive the Linux side being busy or rebooting (reinforces the `workbench.md` scored-test gate).
6. **Command surface across the link should be semantic** (`set head angle`, `drive wheels`, `set face state/parameters`), not raw PWM or streamed raster frames — per the system-design-brief's "behaviour expresses intent, controllers enforce physics," and mirrored by Vector's SDK proto.

## 8. Open items → RP-02 / ADR-12 / ADR-06

- [ ] Close the wider body/head compute placement and transport in RP-02/ADR-12 while retaining selected RP-01 Option C/C2 unless change control records contrary evidence.
- [ ] Validate the selected D2 display path with no-touch Waveshare SKU 30493: installed mass/CoM, animation frame time, optical result, power/thermal behaviour, complete moving harness and fault response.
- [ ] Select an ESP32-S3 motion-controller module with the required SPI/servo/E-stop/fault/interrupt pin budget; no purchase is authorized yet.
- [ ] Treat C1 as electrically blocked on SKU 30493's carrier. If later hardware changes reopen it, run the same-chip rendering-off/on timing comparison with Core-0/Core-1/IRAM mitigation before consolidation.
- [ ] Register the on-hand Nano only when its IMU, APDS9960 or PDM mic produces a bench result.
- [ ] Select or identify the base-frame IMU path when locomotion begins; feed it into RP-03 heading evidence.
- [ ] Choose and prototype the internal link (UART/USB first); register the message set + expiry/health semantics.
- [ ] Decide the base/drive MCU and whether it shares the head's family.
- [ ] Implement the provisional timebase (master + timestamp-at-source + offset reconciliation) before first scored RP-01 run.
- [ ] Feed the resulting topology into `system-architecture.md` when ADR-12/ADR-06 close.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-08-17 | 0.1 | First provisional study created from prior-art research (Vector/Cozmo, humanoid/AV/cobot literature); Nano 33 BLE Sense added as head-aggregation candidate. No selections made. |
| 2026-08-27 | 0.2 | Separated head-output and body-heading IMU responsibilities; aligned Option C with the body-mounted microphone array and added exact-revision/high-rate head-IMU checks. |
| 2026-08-28 | 0.3 | Split hybrid head aggregation into C1 Nano and C2 display-MCU + external-IMU candidates; made installed mass, display concurrency and local fault handling the selection evidence. |
| 2026-08-29 | 0.4 | Applied the exact 4.3-inch AMOLED search: marked head-SBC Option A as baseline-revision-only, replaced the blanket Linux-rendering assumption with semantic body ownership, and defined D1 body-raster versus D2 head-raster paths for the raw MIPI panel candidates. |
| 2026-08-29 | 0.5 | Replaced the blocked AMOLED-controller hypothesis with the India-orderable IPS paths; made the ESP32-S3/LVGL head renderer the first D2 prototype while keeping motion safety on a dedicated controller. |
| 2026-08-29 | 0.6 | Propagated the builder's SKU 30493 lock: D2 head-local display rendering is now selected while the internal transport, motion controller and safety boundary remain evidence-gated. |
| 2026-08-31 | 0.7 | Locked ESP32-S3 as the RP-01 motion-firmware class; moved Nano 33 BLE Sense to bench-only equipment; removed the runtime head-IMU path; recorded Core-0/Core-1/IRAM C1 mitigation and the official schematic audit that blocks C1 on the selected carrier, leaving a separate ESP32-S3 C2 module as the active implementation path. |
| 2026-09-02 | 0.8 | Closed the C1/C2 fork in favour of C2, locked display-versus-motion ownership, centralized trajectory execution and safety on the separate ESP32-S3, and retained only the exact module and interface details as open. |
