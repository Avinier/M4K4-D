# Makad V1 Control-Topology Option Study

| Field | Value |
|---|---|
| Status | **Provisional option study — not a selection.** |
| Version | 0.2 |
| Owner | Project builder |
| Created | 2026-08-17 |
| Last reviewed | 2026-08-27 |
| Governed by | `risk-prototype-plan.md` — permitted provisional option study (decision-closeout: "the architecture phase may begin with provisional option studies while prototypes run") |
| Feeds | RP-02 (electrical/control backbone) → **ADR-06 (power)**, **ADR-12 (control topology)**; the monotonic-timebase deliverable (plan §104) |
| Consumes | `system-design-brief.md` responsibility set + AD-01/AD-06/AD-08; `mass-envelope-ledger.md` head section |

This document surveys **how to split Makad's computation and control across hardware**, grounded in how comparable robots are actually built. It selects nothing. A binding choice is made only when RP-02 closes with measured evidence and the relevant ADRs cite it. The purpose now is to (a) fix the vocabulary, (b) record prior art so we don't re-derive it, and (c) name the specific forks RP-01/RP-02 must resolve.

Nothing here overrides the foundation's deferral of processor, controller, battery, and framework selection.

## 1. The industry pattern: hierarchical, heterogeneous control

Every multi-actuator robot above toy complexity uses the same shape — a small number of processors, each matched to a timing tier, not one processor doing everything. The rule, stated bluntly in the humanoid-timing literature: *no single processor type can satisfy all timing requirements.*

| Layer | Typical host | Rate | Makad jobs |
|---|---|---|---|
| High-level | Linux SBC / GPU | 10–60 Hz | vision/perception, NLU + cloud adapters, behaviour authority, **face rendering**, audio |
| Mid-level | SBC or RTOS | 100 Hz–1 kHz | trajectory shaping, subsystem coordination |
| Real-time | dedicated MCU + RTOS | 200 Hz–low kHz | servo/motor loops, encoder/IMU capture, limits, watchdog, command-expiry, E-stop |

A companion **separation principle** falls straight out of physics and applies directly to Makad: *proprioceptive* sensors (IMU, joint feedback, encoders) feed the fast inner loops **on the MCU**; *exteroceptive* sensors (the camera) feed slower planning **on the SBC** — because you cannot close a low-latency control loop off a high-latency camera stream. For Makad that means: **head-pose IMU + servo feedback → MCU; camera → SBC.**

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
| **A. Vector-style (compute in head)** | SBC + camera + display + IMU in the head; dumb motor MCU in body | shortest camera/display buses; proven by Vector | heaviest 3-axis moving mass; power + data down to body; head-CAD must package an SBC | Viable but taxes the 3-axis mechanism |
| **B. Body-heavy (compute in body)** | SBC in body; head carries only camera + display + light | lightest head, easiest gimbal | **camera bus (MIPI/USB) must flex across 3 joints** — the fragility risk; display bus too | Cable-survival risk is the whole RP-01 concern |
| **C. Hybrid (recommended to study first)** | SBC in **body**; a **head-aggregation MCU** in the head owns head IMU + LED + servo signals; thin serial/bus down; camera routed as its own managed cable; the four-mic array remains body-mounted | light-ish head; local head-pose IMU feedback (Vector-like); collapses many head wires into a thin link; motor limits/watchdog local | camera still crosses the joints; two firmware targets | **Best first candidate**; matches the separation principle (§1) |

Option C is where the **Arduino Nano 33 BLE Sense** fits — see §6. RP-01 (cable behaviour across the workspace) and RP-02 (electrical backbone) exist precisely to decide between A/B/C with measured evidence.

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

## 6. Candidate: Arduino Nano 33 BLE Sense (on hand)

On-hand part; a strong candidate for the **head-aggregation MCU** in Option C. Not selected.

| Feature | Value to Makad |
|---|---|
| nRF52840 (Cortex-M4F) | Ample for a real-time servo/joint loop with limits, watchdog, command-expiry |
| **Onboard IMU** | Free **head-output feedback** for settling, compliance/cable deflection, camera stabilization and RP-01 modal work; not a substitute for body heading |
| **Onboard PDM mic** (Sense variant) | Present but not part of the approved four-microphone body-array architecture; ignore or use only as a diagnostic channel |
| APDS9960 (proximity/gesture/ambient-light) | Free extras: dim the face in a dark room, proximity as a wake cue (non-Core, nice-to-have) |
| I²C / SPI / PWM | Drives LED driver, small display peripherals, generates servo signals — all **local to the head board** (correct use of I²C per §3) |
| BLE | Not needed for internal comms (wired is more reliable); ignore or keep as debug fallback |
| 18 × 45 mm, 3.3 V | Fits the head envelope; 3.3 V logic is fine for servo PWM/I²C/SPI — servo *power* stays on a separate 5–6 V rail |

**Caveats to confirm in RP-01/RP-02:**
- Variant matters: plain *Nano 33 BLE* has the IMU but **no mic**; the **Sense** adds the mic + APDS9960. (Ours is the Sense.)
- Register the exact board revision and IMU. Configure a higher-rate sensor path for RP-01 modal work; a 104 Hz convenience configuration is too sparse for reliable identification around the 40 Hz pitch target.
- A separate **body-frame IMU** belongs with the base/drive controller for chassis heading, caster/traction disturbance and tip/pickup detection. Joint encoders plus body attitude provide a kinematic head-pose estimate; the head IMU observes downstream compliance that estimate cannot see.
- One MCU driving 3 coordinated axes **plus** LED/mic — verify the timing budget holds when everything runs at once (AD-08 concurrent-load risk).
- Whether it is head-local (Option C) or the system settles on Option A/B is the RP-01/RP-02 decision.

**Heterogeneity caution:** using *different* MCU families for head and base multiplies toolchains and debug surfaces for a solo builder. Vector's head-SoC vs body-STM32 split was heterogeneous **by necessity** (one must run Linux, one is a tiny motor relay) — not by preference. If a base MCU is added, prefer the **same family** as the head unless a role genuinely forces otherwise.

## 7. Provisional recommendation (to be confirmed by RP-02)

1. **Two controllers, heterogeneous by role, not by variety:** a **Linux SBC** (vision, NLU, behaviour, face rendering) + **≥1 real-time MCU**. The **Nano 33 BLE Sense** is a strong head-aggregation candidate; a **base/drive MCU with body-frame IMU input** is the likely second node — same family if possible.
2. **Internal link: UART/USB serial**, Vector-style. Not CAN, not micro-ROS, not I²C across joints — those are documented "grow-into-it" options.
3. **Compute placement (Option A/B/C) is the open fork** — study Option C first; let RP-01 (cable behaviour) and RP-02 (backbone) decide with evidence.
4. **Timebase: one master + timestamp-at-source + serial offset reconciliation.** Not PTP.
5. **Motor limits, watchdog, and E-stop live on the MCU, never on the SBC** — every source insists safety-critical loops must survive the Linux side being busy or rebooting (reinforces the `workbench.md` scored-test gate).
6. **Command surface across the link should be semantic** (`set head angle`, `drive wheels`, `display face`), not raw PWM — per the system-design-brief's "behaviour expresses intent, controllers enforce physics," and mirrored by Vector's SDK proto.

## 8. Open items → RP-02 / ADR-12 / ADR-06

- [ ] Decide compute placement (Option A / B / C) from RP-01 cable-behaviour + RP-02 backbone evidence.
- [ ] Confirm head-aggregation MCU candidate (Nano 33 BLE Sense) against the RP-01 3-axis timing budget.
- [ ] Register the on-hand Nano revision/IMU and prove the head-sensor sampling/timestamp path used for RP-01 modal and settling measurements.
- [ ] Select or identify the body-frame IMU path independently of the head IMU; feed it into RP-03 locomotion/heading evidence.
- [ ] Choose and prototype the internal link (UART/USB first); register the message set + expiry/health semantics.
- [ ] Decide the base/drive MCU and whether it shares the head's family.
- [ ] Implement the provisional timebase (master + timestamp-at-source + offset reconciliation) before first scored RP-01 run.
- [ ] Feed the resulting topology into `system-architecture.md` when ADR-12/ADR-06 close.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-08-17 | 0.1 | First provisional study created from prior-art research (Vector/Cozmo, humanoid/AV/cobot literature); Nano 33 BLE Sense added as head-aggregation candidate. No selections made. |
| 2026-08-27 | 0.2 | Separated head-output and body-heading IMU responsibilities; aligned Option C with the body-mounted microphone array and added exact-revision/high-rate head-IMU checks. |
