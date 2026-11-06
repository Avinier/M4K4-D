# PCB-09 — C0 link adapter

Pi-header board: 2 × RS-422 (THVD1451), audio pass-through and the enclosure-fan switch `J9-4`. **Rev A designed** ([D-092](../../decisions.md#d-092)): 77 × 22.7 × 1.6 mm, four layers, on the Pi header through a Samtec SSW-120-01-T-D socket and two M2.5 × 11 mm standoffs.

| | |
|---|---|
| Register | [04-pcbs board register](../README.md#board-register) |
| Project BOM | CH-084 in [BOM.csv](../../BOM.csv) |
| Location | Body, on the Pi header |
| Specification | [audiosystem.md §4](../../02-body/v1/research/audiosystem.md#4-audio-functions-on-the-shared-boards)<br>[D-042](../../decisions.md#d-042), [D-073](../../decisions.md#d-073), [D-074](../../decisions.md#d-074), [D-092](../../decisions.md#d-092) |
| CAD placeholder | `_c0_link_adapter()` in [`body_v1_model.py`](../../02-body/v1/cad/body_v1_model.py) |
| CAD labels | `C0_LINK_ADAPTER_PCB09` |
| Final CAD | `Custom PCBs › PCB-09 C0 link adapter` in [makad-v1.step.py](../../final/v1/cad/makad-v1.step.py): the rev-A KiCad STEP, standoffs, screws and mated plugs ([pcb_integration.py](../../final/v1/cad/pcb_integration.py)) |

## Stages

See [workflow.md](../workflow.md) for what each stage involves and when it is done.

| Stage | Status | Revision / evidence | Date |
|---|---|---|---|
| 1. Design | **Done, rev A** ([D-092](../../decisions.md#d-092)) | [design/](design/), [fab/revA](fab/revA/README.md), [cad/](cad/); ERC 0/0; DRC 0 violations, 0 unconnected, 0 parity; `check_pcb09_mount.py` 7/7, `check_pcb09_fit.py` 5/5 | 2026-11-06 |
| 2. Procure | Waits for the design batch ([D-064](../../decisions.md#d-064)) | — | — |
| 3. Integrate | **CAD replacement complete**; physical acceptance open | [pcb_integration.py](../../final/v1/cad/pcb_integration.py), `check_pcb_integration.py` | 2026-11-06 |

## Inputs

Header audit started 2026-10-31. The electrical interface below is the **builder-agreed allocation baseline v0.2** ([D-073](../../decisions.md#d-073)); CR-02 and boot-safe audit closure remain open. The D-074 strip outline and all 40 socket pad positions have since been checked, and a review schematic and placement exist below. Socket selection, installed height, retention and populated fit were the remaining lesson-1 gaps; they are closed in the [input freeze](#input-freeze--2026-11-06-d-092) (D-092).

**Set by PCB-05.** `J9-3` (audio, `W26` to PCB-05 `J5-1`) carries signals only: GPIO18 BCLK, GPIO19 LRCLK, GPIO20 SDI0, GPIO22 SDI1, GPIO21 SDO0, GPIO23 `AMP_SD`, the Pi's 3V3, two GND and one spare, and **no 5 V** ([D-067](../../decisions.md#d-067), PCB-05 2026-10-27; `CA-06` CR-01 accepted there). Pin order, set by the PCB-05 schematic (2026-10-27): **1 3V3, 2 LRCLK, 3 GND, 4 BCLK, 5 GND, 6 SDO0, 7 SDI1, 8 SDI0, 9 AMP_SD, 10 spare (5V_SENSE)** (reordered 2026-10-27 at PCB-05 routing, D-067); W26 is wired 1:1. Route the spare pin to a test pad: PCB-05 carries an unfitted 5V-present divider on it, which a later `CA-06` change could bring to a Pi GPIO.

**Set by other boards.** `J9-2` (base link, `W25` to PCB-10 `J10-2`) was set by [PCB-10](../pcb-10-c3-carrier/README.md#connectors-and-who-owns-each-pin-order) on 2026-10-27 and reordered at its layout on 2026-10-28 (the order its THVD1451's pins come in, so the pairs run straight). The pairs are named by direction so `W25` is wired 1:1: 1 GND, 2 `C0TX+` and 3 `C0TX−` (this board's driver `Y`/`Z`), 4 `C3TX−` and 5 `C3TX+` (this board's receiver `B`/`A`, with its 120 Ω termination), 6 spare. The `J9-1` head link may follow the same rule; that is this board's choice.

### Pi 5 header audit — 2026-10-31

**Lesson.** A GPIO has three separate properties: where it is on the connector, which peripheral it can carry, and what voltage it presents before software takes control. A correct UART pin can still send a break at boot; a correct fan pin can still turn the switch partly on if its bias is wrong. Covering all 40 contacts also makes PCB-09 responsible for access to reserved buses. Mechanical contact with a socket does not imply an electrical trace on the adapter.

**Result:** BCM-to-header mappings and proposed peripheral functions pass the paper check; the active owners do not overlap. **The complete boot-safe interface is not yet passed or frozen. CR-02 remains OPEN:** GPIO24 is the builder-selected, conflict-free fan pin; accepting the entire change still requires the outstanding evidence below. CR-01 remains accepted under D-067; this audit adds software implementation conditions rather than reopening that allocation. The builder accepted HA-02…04's recommended dispositions on 2026-10-31 (D-073), explicitly retaining CR-02 as open.

#### Evidence and authority

Read on 2026-10-31. RP-02 is read-only; build changes belong here and in [decisions.md](../../decisions.md); the selected dispositions are recorded as D-073. Source-code URLs use Raspberry Pi's `rpi-6.12.y` branch as an inspected reference, **not** evidence of the kernel installed on C0.

| Ref | Source | What was checked |
|---|---|---|
| H | Raspberry Pi [40-pin header documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio) and its [pin diagram](https://raw.githubusercontent.com/raspberrypi/documentation/master/documentation/asciidoc/computers/raspberry-pi/images/GPIO-Pinout-Diagram-2.png) | All 40 physical positions, supply contacts, GPIO0/1 reservation; 3.3 V GPIO, no 5 V tolerance. The shared diagram's older peripheral labels are not the Pi 5 mux authority |
| R | [RP1 peripherals datasheet](https://datasheets.raspberrypi.com/rp1/rp1-peripherals.pdf), §3.1 Table 4, GPIO CTRL and PADS Table 21 | UART/I²S mux, NULL reset function, output disabled and input buffer disabled at reset |
| P | Raspberry Pi engineer clarification, [Pi5 GPIO Reset Defaults](https://forums.raspberrypi.com/viewtopic.php?t=366826), 2024-03-04…06 | GPIO0–8 pull up; GPIO9–27 pull down. Table 21 only says “varies”; this clarification supplies the per-pin bias and corrects the initial “inputs” description |
| T | TI [THVD1451, SLLSEY3E](https://www.ti.com/lit/ds/symlink/thvd1451.pdf), §§7.3, 7.5, 7.7, 9.1 | 3.0–5.5 V operation, logic thresholds, receiver swing, 3 mA maximum no-load current; always-enabled driver and receiver |
| U | Official [uart0-pi5](https://raw.githubusercontent.com/raspberrypi/linux/rpi-6.12.y/arch/arm/boot/dts/overlays/uart0-pi5-overlay.dts), [uart2-pi5](https://raw.githubusercontent.com/raspberrypi/linux/rpi-6.12.y/arch/arm/boot/dts/overlays/uart2-pi5-overlay.dts), [rp1.dtsi](https://raw.githubusercontent.com/raspberrypi/linux/rpi-6.12.y/arch/arm64/boot/dts/broadcom/rp1.dtsi) and [overlay reference](https://raw.githubusercontent.com/raspberrypi/linux/rpi-6.12.y/arch/arm/boot/dts/overlays/README) | UART pin groups and optional flow-control claims; default I²S group stops at GPIO21 |
| F | Official [gpio-fan overlay](https://raw.githubusercontent.com/raspberrypi/linux/rpi-6.12.y/arch/arm/boot/dts/overlays/gpio-fan-overlay.dts) and [driver](https://raw.githubusercontent.com/raspberrypi/linux/rpi-6.12.y/drivers/hwmon/gpio-fan.c) | One active-high control pin; temperature and hysteresis parameters; probe preserves the observed GPIO level, shutdown drives off |
| B | Official [UART configuration](https://www.raspberrypi.com/documentation/computers/configuration.html#configuring-uarts) and [BOOT_UART](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#BOOT_UART) | Pi 5 debug UART is normally UART10 on the separate debug connector; configuration can change the primary UART, so silence on GPIO14 must be checked on the installed image |
| C | RP-02 [CA-06](../../../02-prototypes/RP-02-electrical/compute-control-architecture.md#ca-06--pi-gpio-allocation-reserves-independent-transports), [D-042](../../decisions.md#d-042), [D-043](../../decisions.md#d-043), [D-067](../../decisions.md#d-067), PCB-05/PCB-10 READMEs linked above | Existing allocations, fan circuit, selected 3010 fan, connector contracts and audio power ownership |

#### 40-row header interface (allocation baseline v0.2)

Directions are relative to the Pi. `N↑`/`N↓` mean **NULL function, output disabled, input buffer disabled**, with the indicated weak pull at RP1 reset (R/P); they do not promise an unchanged state throughout firmware, Linux or a warm reboot. Voltages are nominal signal/rail domains, not absolute maximum ratings. `NC` means a socket contact with **no trace, via, test pad or other load on PCB-09**, apart from its own land. Reserved contacts remain reserved even when NC. Supply rows are shared rail contacts, not competing GPIO owners.

| Physical pin | BCM GPIO | PCB-09 net / disposition | Owner / authority | Direction | RP1 reset / external bias | Voltage |
|---|---|---|---|---|---|---|
| 1 | — | +3V3_PI | Pi supply → PCB-09 + PCB-05 | Power in | Rail sequencing | 3.3 V |
| 2 | — | +5V_PI → fan only | D-042 / D-043 | Power in | May remain powered at halt | 5 V |
| 3 | 2 | I2C1_SDA → labelled SDA service pad | CA-06 / D-073 housekeeping | Bidirectional | N↑; Pi has fixed pull-up | 3.3 V |
| 4 | — | +5V_PI, same rail as pin 2 | D-042 / D-043 | Power in | May remain powered at halt | 5 V |
| 5 | 3 | I2C1_SCL → labelled SCL service pad | CA-06 / D-073 housekeeping | Bidirectional | N↑; Pi has fixed pull-up | 3.3 V |
| 6 | — | GND | Common return | Return | GND | 0 V |
| 7 | 4 | BASE_TX → base THVD1451 D | CA-06 UART2 | Out | N↑; 4.7 kΩ to 3V3 (D-073) | 3.3 V |
| 8 | 14 | HEAD_TX → head THVD1451 D | CA-06 UART0 | Out | N↓; 4.7 kΩ to 3V3 (D-073) | 3.3 V |
| 9 | — | GND | Common return | Return | GND | 0 V |
| 10 | 15 | HEAD_RX ← head THVD1451 R | CA-06 UART0 | In | N↓; R drives after VCC valid | 3.3 V |
| 11 | 17 | NC; UART0 RTS prohibited | PCB-09 unused | — | N↓ | 3.3 V |
| 12 | 18 | BCLK → J9-3.4 | CA-06 / D-067 I²S0 | Out | N↓ | 3.3 V |
| 13 | 27 | NC | PCB-09 unused | — | N↓ | 3.3 V |
| 14 | — | GND | Common return | Return | GND | 0 V |
| 15 | 22 | SDI1 ← J9-3.7 | CR-01 / D-067 I²S0 | In | N↓; converter powered by Pi | 3.3 V |
| 16 | 23 | AMP_SD → J9-3.9 | CR-01 / D-067 GPIO | Out | N↓; PCB-05 SD_MODE pulls low | 3.3 V |
| 17 | — | +3V3_PI, same rail as pin 1 | Pi supply → PCB-09 + PCB-05 | Power in | Rail sequencing | 3.3 V |
| 18 | 24 | FAN_EN → 100 Ω → MOSFET gate | D-042 / D-073; CR-02 open | Out | N↓; 100 kΩ gate–source | 3.3 V |
| 19 | 10 | NC; SPI0 MOSI reserved | CA-06 SPI/service | — | N↓ | 3.3 V |
| 20 | — | GND | Common return | Return | GND | 0 V |
| 21 | 9 | NC; SPI0 MISO reserved | CA-06 SPI/service | — | N↓ | 3.3 V |
| 22 | 25 | NC | PCB-09 unused | — | N↓ | 3.3 V |
| 23 | 11 | NC; SPI0 SCLK reserved | CA-06 SPI/service | — | N↓ | 3.3 V |
| 24 | 8 | NC; SPI0 CE0 reserved | CA-06 SPI/service | — | N↑ | 3.3 V |
| 25 | — | GND | Common return | Return | GND | 0 V |
| 26 | 7 | NC; SPI0 CE1 / UART2 RTS alternatives | PCB-09 unused | — | N↑ | 3.3 V |
| 27 | 0 | NC; ID_SD only | Pi HAT-ID reservation | — | N↑ | 3.3 V |
| 28 | 1 | NC; ID_SC only | Pi HAT-ID reservation | — | N↑ | 3.3 V |
| 29 | 5 | BASE_RX ← base THVD1451 R | CA-06 UART2 | In | N↑; R drives after VCC valid | 3.3 V |
| 30 | — | GND | Common return | Return | GND | 0 V |
| 31 | 6 | NC; UART2 CTS prohibited | PCB-09 unused | — | N↑ | 3.3 V |
| 32 | 12 | NC; PWM-capable spare | PCB-09 unused | — | N↓ | 3.3 V |
| 33 | 13 | NC; PWM-capable spare | PCB-09 unused | — | N↓ | 3.3 V |
| 34 | — | GND | Common return | Return | GND | 0 V |
| 35 | 19 | LRCLK → J9-3.2 | CA-06 / D-067 I²S0 | Out | N↓ | 3.3 V |
| 36 | 16 | NC; UART0 CTS prohibited | PCB-09 unused | — | N↓ | 3.3 V |
| 37 | 26 | NC | PCB-09 unused | — | N↓ | 3.3 V |
| 38 | 20 | SDI0 ← J9-3.8 | CA-06 / D-067 I²S0 | In | N↓; converter powered by Pi | 3.3 V |
| 39 | — | GND | Common return | Return | GND | 0 V |
| 40 | 21 | SDO0 → J9-3.6 | CA-06 / D-067 I²S0 | Out | N↓ | 3.3 V |

**Count:** 11 functional GPIO (including FAN_EN with CR-02 open), 2 reserved I²C1 GPIO exposed on service pads, 15 other GPIO contacts, 4 supply contacts and 8 grounds = 40. GPIO0/1 have no adapter EEPROM or test points. Both contacts of each supply rail join that rail; all eight grounds join the common plane. J9-3.1 gets +3V3_PI; J9-3.3/.5 get GND. J9-3.10 goes **only to an isolated 5V_SENSE test pad**, never to a Pi GPIO or either supply. Its name does not make it a 5 V power connection. PCB-05's divider remains DNP; fitting it and connecting a GPIO needs CR-03.

#### Function selection and software ownership

Table 4 (R) confirms UART0 on GPIO14/15 at **a4**, UART2 on GPIO4/5 at **a2**, and I²S0 BCLK/WS/SDI0/SDO0/SDI1 on GPIO18/19/20/21/22 at **a2**. GPIO23 and GPIO24 use plain GPIO outputs (RIO path), never I²S. GPIO23's a2 is SDO1; GPIO24's a2 is SDI2, so enabling additional audio lanes indiscriminately would collide with both control signals.

| Consumer | Allowed GPIO claim | Condition / finding |
|---|---|---|
| `uart0-pi5` | 14, 15 | Use the Pi 5 overlay explicitly. No `ctsrts` or `rs485`: those also claim 16/17. Full-duplex THVD1451 needs no RTS control |
| `uart2-pi5` | 4, 5 | No `ctsrts` or `rs485`: those also claim 6/7 |
| Audio sound-card overlay | 18, 19, 20, 21, 22 only | **Not yet supplied or compiled.** The inspected `rp1_i2s0_18_21` group omits SDI1. Define/select a five-pin I²S0 group; keep GPIO23/24 out of it. Bind one shared clock interface with four capture channels on two stereo lanes and two-channel playback; enabling `i2s` alone is not a sound-card implementation |
| Amp control | 23 only | Start low; assert only after valid playback clocks/data; lower before stopping clocks and at orderly shutdown. One software owner; do not combine a permanent GPIO hog with a driver that also requests it |
| `gpio-fan` | 24 only | Proposed `dtoverlay=gpio-fan,gpiopin=24,temp=60000,hyst=5000`: 60 °C on / 55 °C off. Explicit pin required: the default is GPIO12. Temperatures remain bench starting points |
| I²C1 | 2, 3 reserved; SDA/SCL/GND service pads (D-073) | No additional pull-ups, attached consumer or bus cable. Keep the controller disabled until a consumer is deliberately configured |
| SPI0 | None | Reservation preserved; no adapter traces or access. SPI0's usual second CS is GPIO7, outside CA-06's 8–11 shorthand; leave SPI disabled unless deliberately configured |

**Console check is a release condition.** Pi 5 normally sends debug output through UART10, not GPIO14/15 (B); that is not proof that every EEPROM/image configuration is silent. Require EEPROM `BOOT_UART=0`, disable firmware debug output (`uart_2ndstage`), remove any kernel `console=`/`earlycon` targeting either link (including aliases), and disable serial getty/debug applications on both resolved ports. Preserve CA-06's stable udev names and boot mux self-test. Capture the installed EEPROM settings, `config.txt`, `cmdline.txt`, resolved aliases and enabled services; scope HEAD_TX through cold boot, warm reboot and shutdown. `enable_uart=1` alone is not the pin-ownership proof.

#### Boot/reset findings and selected circuit remedies

1. **FAN_EN: correct default, incorrect “beats any pull-up” premise.** GPIO24 is reset NULL/pulled down, so its internal pull and D-042's 100 kΩ gate-to-source resistor agree. Retain the 100 Ω series resistor, gate pull-down at the MOSFET, common source ground, flyback Schottky (cathode to FAN+, anode to FAN−), and local 10 µF + high-frequency bypass. A 100 kΩ pull-down does not dominate a tens-of-kΩ pull-up: even an illustrative 50 kΩ pull-up gives about 2.2 V at the gate. Thus no overlay/firmware may enable a pull-up or other function on GPIO24. With only 100 kΩ present, require the selected MOSFET's worst-case gate leakage plus board leakage to keep VGS below its off limit. Confirm gate voltage and fan inactivity on real cold boot/reset; an output driven high by a hung kernel is not corrected by a pull-down. This is a reset-off switch, not an independent thermal failsafe.
2. **UART TX: head reset is a break, not an unspecified floating signal.** GPIO14 defaults pulled down; THVD1451 forwards D continuously. GPIO4 defaults pulled up and is nominally idle-high. Add **4.7 kΩ from each D/TX to the same Pi 3V3 rail** (D-073): both links then have a deliberate idle-high bias before the UART owns them. TI specifies up to 6.2 µA D input leakage; include it and the opposing RP1 pull in the high-level calculation, against TI's 2.0 V VIH. A 100 kΩ pull-up is unsuitable against the head pin's pull-down. As a cross-check only, the [CM5 RP1 GPIO table](https://pip-assets.raspberrypi.com/categories/944-raspberry-pi-compute-module-5/documents/RP-008180-DS-7-cm5-datasheet.pdf?disposition=inline) gives a 35 kΩ minimum pull-down: 3.0 V × 35/(35+4.747) − 6.2 µA × (35 kΩ ∥ 4.747 kΩ) ≈ **2.62 V** with a +1% pull-up. This is a same-controller comparison, not a Pi 5 board-specific guaranteed limit; confirm the Pi 5 bound or measure with margin before sign-off. Low-state pull-up load at 3.3 V is about 0.70 mA. Pull-ups cannot suppress actively transmitted boot text or guarantee clean signalling while VCC ramps. C2/C3 must reject framing errors, breaks, stale sessions and invalid commands before arming; verify recovery after these events.
3. **AMP_SD: reset bias agrees with off.** GPIO23's pull-down reinforces PCB-05's external 100 kΩ and MAX98357A's internal pull-down, through the existing 2.2 kΩ series resistor (D-067). No I²S group may take GPIO23. That remote pull-down defines off if W26 is unplugged. PCB-05 owns the unpowered-amp SD_MODE injection mitigation; its accepted 2.2 kΩ circuit remains the contract. A warm reboot need not instantly restore RP1 reset defaults: test amp mute ordering rather than assuming it.
4. **Audio inputs and outputs.** SDI0/SDI1 come from converters supplied from the Pi's own 3V3, with a passive filtered mic rail; no independent 5 V receiver drives a Pi input. BCLK/LRCLK/SDO0 are outputs, normally held low by reset bias while the amp is off. Retain PCB-05's clock damping and verify clock edges and rail sequencing with the real W26. Shared supply origin does not by itself prove transient sequencing during a fast shutdown; scope the filtered rail and SDI lines at bring-up.

#### Voltage and rail budget

Both THVD1451 VCC pins and TX pull-ups must use **+3V3_PI, never +5V_PI**. TI's receiver high is referenced to VCC; with VCC = 3.3 V its specified VOH ≥ VCC − 0.4 V at −8 mA is compatible with 3.3 V Pi logic. A 5 V supply would expose RX to a 5 V-class output. Put 100 nF at each VCC/GND pair. Each local receiver A/B pair gets 120 Ω; no extra termination across this board's Y/Z driver pair (the far receiver terminates it). TI's open/short/idle receiver fail-safe does not fix a low or noisy driver D input. Keep the transceiver selection open until its footprint and alternatives are reviewed; a substitute needs its own bias/power check.

| Header rail | Incremental loads | Paper allowance / remaining evidence |
|---|---|---|
| 3V3 | Two THVD1451, both continuously driving remote 120 Ω loads | No-load maximum **2 × 3 = 6 mA**. Termination current is additional: a deliberately conservative 3.3 V/120 Ω ceiling per driver gives **55 mA** total load current; about **61 mA** including quiescent, before dynamic/cable-capacitance current |
| 3V3 | PCB-05 via J9-3.1 | **15 mA design allowance**, from its README; includes converters and four mics. Do not count it again as a 5 V load on PCB-09 |
| 3V3 | TX pull-ups, AMP_SD and switching activity | Up to about **1.4 mA** if both TX held low, plus amp-control bias and dynamic current; use **80 mA provisional normal-operation allocation** for the complete sub-branch, then measure at link/audio load. This is not a short-circuit or inrush rating |
| 5V | D-043's purchased 3010 fan via J9-4.1, local capacitor charging | Running, startup and locked-rotor currents **unknown**. No defensible numerical total or rail-margin pass yet; measure the actual fan, not the superseded 4010 listing |

3V3 fault demand is separate: TI lists driver short-circuit current magnitude up to 250 mA per device; two shorted outputs could dominate the 80 mA normal allowance. Check supply droop/current limiting and fault behaviour before release. The Pi header rails are supply outputs here; there is no external rail tied in through W25/W26/W41. Size the 5 V path, ground return, MOSFET at its **2.5/3.3 V gate drive**, diode, connector and protection from measured fan startup/stall and capacitor inrush. `VGS(th)` is not an on-resistance specification. The full Pi + USB + Active Cooler + adapter budget remains under the compute branch; available fan margin cannot be inferred from a “5 A supply” label alone. Keep fan current loops away from mic/audio returns.

#### Findings and dispositions (D-073)

| ID | Finding | Proposed disposition / closure |
|---|---|---|
| HA-01 | All assigned BCM/physical mappings and mux functions pass; no active pin collision | Allocation baseline v0.2 agreed by the builder under D-073, including HA-02…04 below. Boot-safe audit closure remains open; physical socket mirroring is the next step |
| HA-02 | CA-06's reserved I²C1 is inaccessible under the full socket; no v1 consumer/harness is identified in the reviewed build specs | **Selected 2026-10-31:** preserve access with labelled SDA/SCL/GND service pads on PCB-09; no additional pull-ups (Pi already has them), bus cable or consumer implied. Pins 3/5 are routed to their respective service pads; the CA-06 reservation remains |
| HA-03 | UART0 reset sends a break; base TX relies on a weak default pull | **Selected 2026-10-31:** fit two 4.7 kΩ TX pull-ups to Pi 3V3. Check Pi-specific worst-case bias and scope startup before release; framing/session checks stay mandatory |
| HA-04 / CR-02 | GPIO24 is suitable and has the correct reset pull. The fan circuit/current and deployed software are not fully verified | **Selected 2026-10-31:** retain GPIO24 and the D-042 100 kΩ pull-down, with the documented mux restriction. CR-02 stays OPEN until boot/overlay and fan-current checks pass; do not claim full audit pass or schematic implementation |
| HA-05 | Stock I²S group does not include GPIO22; a broad lane group could steal GPIO23/24 | Custom audio overlay required; compile/apply to the exact target DTB and inspect merged pinctrl/claims, then prove four-channel capture + playback and independent AMP_SD/FAN_EN |
| HA-06 | Pi 5 normally uses separate debug UART, but the installed image/EEPROM was not inspected | Record console/getty/alias configuration and scope both TX lines through cold boot, reboot and halt; prove no boot text on either link |
| HA-07 | Fan current and complete rail margin not established | Measure D-043 fan run/start/stall, verify switch ratings, inrush, rail droop and thermal/noise conditions. Normal 3V3 estimate is not a measured rail budget |
| HA-08 | J9-3 spare must not silently acquire a GPIO | Isolated test pad only; no GPIO claim without CR-03. J9-2.6 remains spare/NC; J9-1 order still to be chosen with its far-end contract |

**Builder disposition recorded:** “Use all three recommendations” (2026-10-31), [D-073](../../decisions.md#d-073). D-042's CR-02 cross-reference records that it is still open. Historical RP-02 is unchanged. The next design step is the CAD envelope and socket-orientation check; implement the selected service pads and TX bias in the schematic afterwards. Evidence needing the deployed Pi or real fan remains an integration/release gate.

### Mechanical inputs and socket orientation — 2026-10-31

**Lesson.** A connector's plastic body is only part of its footprint. Copper pads need an edge margin, solder tails occupy the other face, and courtyards reserve assembly space around neighbouring parts. A board can clear the robot in CAD while still leaving pads outside its outline. This survey checks those separately.

**CAD brief.** Inspect the current PCB-09 placeholder, its mating Pi header and nearby body/chassis parts in world millimetres (+X forward, +Y robot-left, +Z up). Keep the accepted electrical map and connector pin orders. Measure the board and screen the stock socket/SOIC/GH footprints. The initial survey tested the strip extension without changing geometry; the builder then approved it and it is applied in the final assembly under [D-074](../../decisions.md#d-074). Output: the reusable [input survey](../../final/v1/cad/check_pcb09_inputs.py) and its [measurement report](mechanical-audit.json). The final assembly entry is the geometry authority; subsystem sources stay unchanged.

**Run performed.** Built `chassis_v1_reference()` and `build_body_assembly()`, applied the current droid edits with `strict=False`, and intersected the actual shapes with board/face probes. Read the nightly library's socket, SOIC-8 and GH lands/courtyards. The script checks all 40 numbered pad centres and includes an intentionally wrong row reflection that fails on all 20 even pins. This is a static packaging and land-pattern screen, **not KiCad DRC, an insertion sweep or a final board fit check**. The head assembly was not built.

From the repository root:

```sh
rtk proxy env MAKAD_RELIEF_SERIAL=1 PYTHONPATH=project/03-build/03-head/v1/cad:project/03-build/02-body/v1/cad /Users/avinier/.codex/runtimes/text-to-cad/0.4.28/venv/bin/python project/03-build/final/v1/cad/check_pcb09_inputs.py --output project/03-build/04-pcbs/pcb-09-c0-link-adapter/mechanical-audit.json
```

#### Actual board outline and neighbourhood

The D-074 core is **1.6 mm**, at **Z 106.4…108.0**. It is the union of these three XY rectangles, not a 70.7 × 22.7 mm rectangle. Its volume is **1,299.344 mm³** (area 812.09 mm²), up 97.68 mm³ from the initial survey, and it remains one solid.

| Region | World X | World Y | Size XY |
|---|---|---|---|
| Header strip (D-074) | −4.7…36.0 | 16.3…22.4 | 40.7 × 6.1 |
| Bridge | 36.0…47.1 | 16.3…22.5 | 11.1 × 6.2 |
| Wide connector area | 36.0…66.0 | 22.5…39.0 | 30.0 × 16.5 |

Both the original core and the applied D-074 core have **zero intersecting external solids or reserves** in this static body/chassis check. This does not approve the populated board or its assembly path.

| Face / region probed | Nearest intersecting part or reserve in the probe | Consequence |
|---|---|---|
| Above strip, Z 108.001…128 | Yaw FFC cassette starts at Z 120.0; rolling-loop reserve at 121.35 | 12.0 mm geometric space above the core to the cassette in this column; leave assembly/tolerance margin. Socket solder tails and their copper still restrict placement |
| Below strip, Z 96.4…106.399 | Pi header tips at Z 104.045 | **2.355 mm** from pin tips to adapter underside. This is not a socket body height or a proved engagement length |
| Above wide area | PCB-05 +Y lead reserve starts at Z 115.6 over X 45…66, Y 22.5…28; fan lead at Z 118 over X 36…39, Y 33…39; frame at Z 126 | The lead reserve is only **7.6 mm** above the board face. J9-2's modelled header + plug reaches Z 115.4, leaving 0.2 mm vertically to that reserve. Route the leads deliberately; a body-only clearance is not a harness pass |
| Below wide area, Z 96.4…106.399 | No intersecting external solid/reserve in the 10 mm-deep column | Candidate space for underside circuitry. Initially keep parts within the old reserve's Z ≥ 104 floor (2.4 mm below the board), then check real parts, tails and service access |

These are spatially bounded probe results, not uniform allowable component heights. The Pi and cooler were intersected as geometry rather than treating their complete bounding boxes as solid obstacles. Old comments about 0.1 mm to the former XC330 position and the unshifted strip are not the current envelope authority.

#### Mating grid and socket numbering

The vendor Pi header is centred at approximately **(21.2, 19.331690)**. Its two rows are **Y 18.061690 and 20.601690**, pitch 2.54 mm, with 20 positions from **X −2.93 to 45.33**. Numbering follows the official Pi top-view diagram (H): pin 1 is the inner (−Y) row at the end away from USB/Ethernet (−X).

| Header pin | World XY | Sanity check |
|---|---|---|
| 1 | (−2.93, 18.061690) | 3V3, inner row |
| 2 | (−2.93, 20.601690) | 5 V, outer row |
| 39 | (45.33, 18.061690) | GND, inner row |
| 40 | (45.33, 20.601690) | GPIO21, outer row |

The socket mounts on the **underside** of PCB-09. The stock `PinSocket_2x20_P2.54mm_Vertical` library has pad 1 at (0, 0), pad 2 at (−2.54, 0), and pad 3 at (0, 2.54). For those **unplaced library coordinates**, the intended numbered mating map is:

```text
world X = −2.93 + library y
world Y = 18.061690 − library x
```

This specifies correspondence, not a KiCad rotation command. When the footprint is put on B.Cu, verify the actual placed pad centres against the report's 40-entry map; a bottom-side flip and an extra hand mirror must not both be applied. The script deliberately catches the wrong row reflection. Before power, continuity-check pins 1/2/6 and all assigned signals from the actual mating contacts to their destinations; verify the purchased socket's pin-1 drawing and the printed square-pad mark. No final physical footprint placement has yet been made.

#### Mechanical findings and dispositions

| ID | Evidence / gap | Disposition proposed for the next step |
|---|---|---|
| ME-01 | Stock socket pads are Ø1.7 mm. **Pins 2, 4, …, 32** extended past the original strip edge: outer copper reaches Y 21.451690 against edge 20.9. With the fab-neutral 0.3 mm edge gap, the minimum edge is **Y 21.751690** | **Closed by D-074, 2026-10-31:** builder approved and the final assembly now extends only the strip's +Y edge to 22.4 mm (width 4.6 → 6.1 mm), preserving bridge, wide area and core Z. All 40 stock pad envelopes pass the 0.3 mm screen; the current core has no static clash. The planted original outline still fails on 16 pads |
| ME-02 | Head transceiver is labelled/modelled SOIC-14, but THVD1451D is SOIC-8 (T). At that placeholder's centre (41.325, 19.5), the real SOIC-8 land pattern has **14 definite pad/socket-copper overlaps** at 0°, and 8 at 90° | Do not carry the placeholder placement into the schematic/layout. Recommend packing both transceivers on the underside of the wide area, clear of the socket and fan-header tails. Actual positions, orientations, decouplers and routing need a scratch-board DRC before freeze |
| ME-03 | J9-2 and J9-3 are 6.5 mm apart. Their stock GH courtyards are both 6.6 mm deep: **0.1 mm overlap**, even before adding margin | Separate the rows further within the wide area. Screen J9-1, J9-4 and all mating plugs at the same time; their final coordinates are not frozen |
| ME-04 | The base transceiver's old box occupies the J9-4 fan connector's reserve. There is no real J9-4 header in `_c0_link_adapter()` | Include the actual fan header and tails in the footprint packing. JST's stock B2B-XH-A footprint is **2.50 mm pitch**; the older “XH2.54” wording is not a dimensional drawing. Confirm the purchased fan lead's housing mates before specifying it |
| ME-05 | `C0_GPIO_SOCKET` is just a 2.3 mm-high block at Z 104.1…106.4, described as the portion above the male tips. There is no selected socket MPN, full body/contact geometry or verified mating depth | Select a named 2×20 socket from its drawing; verify engagement, body seating and lead protrusion. Do not interpret 2.355 mm pin-tip clearance as contact engagement. Preserve the current board Z only if that socket really establishes it; any height change requires rechecking the neighbours |
| ME-06 | The wide area has no dedicated PCB-09 mounting holes, clips or support in the model | Design retention/connector reaction support before freeze. The header alone is not yet justified for connector insertion/removal forces; leave room for support while packing footprints |
| ME-07 | Face probes encounter W26/W27-side and W41 reserves. No PCB-09 insertion/removal path, moving-head sweep or populated-board check has run | Keep the existing assembly sequence (compute tray, then PCB-09, then later overhead assemblies) as an input, not a passed test. Check installation, connector access and cable dressing after the real footprint packing |

**Status:** allocation baseline v0.2 remains agreed under D-073; **ME-01 is implemented under D-074**. The mechanical inputs are not fully frozen: Real-footprint placement has since addressed the paper packing conflicts in ME-02…04 provisionally; selected-part confirmation and targeted populated CAD checks remain open for ME-02…07. The focused [review scene](../../final/v1/cad/pcb09-inputs.step.py) exports [pcb09-inputs.step](../../final/v1/cad/pcb09-inputs.step); gold land markers and the orange added-strip highlight are inspection aids, not fabricated copper or a routed board. The whole-robot inspection and presentation STEPs were rebuilt on 2026-11-01 with the completed-board replacements. PCB-09 still uses this provisional placeholder and updated strip; its populated KiCad placement has not passed fit verification.

**D-074 visual and artifact check:** the [rendered top view](../../final/v1/cad/snapshots/pcb09-strip-d074-top.png) was reviewed; all land markers sit inside the outline. CAD inspection reports 43 occurrences, zero geometry validity failures, core face area 812.09 mm² and measured thickness 1.600 mm. The review model intentionally omits unselected components and mounting.

### Input freeze — 2026-11-06 (D-092)

**Lesson.** Freezing the inputs means every fact the layout leans on has a source: the part that sets the height, the fixing that carries the plug forces, the pin orders the cables are wired to. Before this step the board could be routed, but any of those could have moved it.

| Open item | Closed by |
|---|---|
| ME-05 socket MPN and height | **Samtec SSW-120-01-T-D**: 8.51 mm insulator, 3.68–6.35 mm pin insertion; the Pi header gives 6.11 mm. The stack, 2.5 + 8.51 = 11.01 mm, puts the board's underside at Z 106.45 (CAD 106.4 + 0.05 lift). Tin contacts are the builder's choice; a contact check after vibration goes on the bench list |
| ME-06 retention | **Two M2.5 × 11 mm round male-female standoffs at Pi holes 3 and 4**, as on a HAT, replacing the Pi's screws there; M2.5 × 5 DIN 912 screws from the top. Outline tabs reach both holes (X −11…−4.7 and 47.1…53.4). They are round because a hex standoff hits the Active Cooler. The frame is 15.4 mm over hole 4's head, so **PCB-09 is screwed on at the bench, with the Pi on the tray, before the tray goes in** (`check_pcb09_mount.py` sweeps the unit in) |
| ME-02…04 real footprints | Placed and routed with the real land patterns (below); J9-4 became a GH 2-way SMD header and the bay grew 6 mm toward −X (D-092 amended) |
| ME-07 populated fit | `check_pcb09_fit.py` with the KiCad STEP: every part and the rebuilt plugs clear the robot by 0.2 mm, and the parts slide in with the tray. Harness dressing stays open (stage 3) |
| HA-08 / J9-1 order | **1 GND, 2 C0TX+, 3 C0TX−, 4 C2TX−, 5 C2TX+, 6 spare** (the W25 rule); `W24` is 1:1 and the 05-harness row is updated. PCB-08 `J8-4` and PCB-12 follow it |
| Layers | Four (F, In1 GND, In2 3V3 + three audio hops, B): the 6.1 mm strip holds four 0.16 mm tracks per layer and ten nets run its length |

CR-02 (boot/overlay evidence and the measured fan current) and HA-05/06/07 stay open: they need the deployed Pi and the real fan.

## Schematic

The project is [design/pcb-09-c0-link-adapter.kicad_pro](design/pcb-09-c0-link-adapter.kicad_pro), with its [schematic](design/pcb-09-c0-link-adapter.kicad_sch) and [schematic PDF](design/pcb-09-c0-link-adapter-schematic.pdf). It was created in **KiCad Nightly 10.99.0-5923-gde08734017**, and the first circuit transfer used F8 in the GUI (2026-10-31). Stock symbols are embedded, and `fp-lib-table` points to an empty `pcb09.pretty/`: every land pattern is stock. [build_schematic.py](design/build_schematic.py) authored the first draft; the saved schematic is the source.

The circuit is the D-073 allocation, with 25 board parts plus three power flags:
- two THVD1451DR channels on Pi 3V3, each with a 100 nF bypass, a receiver-only 120 Ω termination and a 4.7 kΩ TX pull-up;
- the fixed W26 audio interface;
- GPIO24's 100 Ω / AO3400A / 100 kΩ fan switch, with a 1N5819HW flyback diode and 10 µF + 100 nF bypass;
- six test pads.

Rev A changes:
- J1's value is now the selected **SSW-120-01-T-D**.
- J5 (J9-4) uses `JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical` (D-092 amended).
- The title block reads rev A.

The pin roles are unchanged.

| Ref | Interface |
|---|---|
| J1 | Pi underside 2 × 20 socket, Samtec SSW-120-01-T-D; all 40 pad positions verified after bottom-side placement |
| J2 | J9-1 head RS-422, side entry: 1 GND, 2 C0TX+, 3 C0TX−, 4 C2TX−, 5 C2TX+, 6 spare (D-092, W25 rule) |
| J3 | J9-2 base RS-422, PCB-10 / W25 contract |
| J4 | J9-3 audio, exact PCB-05 / W26 1:1 order |
| J5 | J9-4 fan, GH 2-way top entry: 1 +5V_PI, 2 FAN_SW |
| TP1…TP6 | SDA, SCL, GND, isolated 5V_SENSE, Pi 3V3, Pi 5 V; all left out of the BOM and position files |

**Checks.** Nightly `kicad-cli sch erc --severity-all`: **0 errors, 0 warnings** ([schematic-erc.rpt](design/schematic-erc.rpt)). The exported [netlist](design/pcb-09-c0-link-adapter.net) gives the same pin-to-net map as [netlist-audit.json](design/netlist-audit.json) (111 pins). J5's two pins keep +5V_PI and FAN_SW, and only J5's footprint and J1's value differ.

## Board set-up

**Outline** (eight Edge.Cuts → ten, D-074 + D-092):
- the strip, world X −4.7…36, Y 16.3…22.4;
- the bridge, X 36…47.1, Y 16.3…22.5;
- the bay, **X 30…66**, Y 22.5…39 (the 6 mm −X extension);
- the standoff tabs, X −11…−4.7 (Y 16.3…22.4) and X 47.1…53.4 (Y 17.2…22.5).

It is one 1.6 mm core: 77.0 × 22.7 mm overall and 983.5 mm² of board. KiCad x = world X + 104.7, KiCad y = 139 − world Y. **The aux and grid origins are at the bottom-left corner as seen from the top**, KiCad (93.7, 122.7) = world (−11, 16.3). The Gerbers, drill and position files all use it.

**Stackup**: PCB-10's 1.6 mm four-layer build: F.Cu 35 µm, prepreg 0.2104, In1 (power), core 1.065, In2 (signal), prepreg 0.2104, B.Cu 35 µm.

**Rules** ([design/pcb-09-c0-link-adapter.kicad_dru](design/pcb-09-c0-link-adapter.kicad_dru)):
- the fab-neutral set of D-062, unchanged: 0.16 mm track and gap, 0.67/0.35 mm vias, 0.31 mm from a via to other copper, 0.3 mm to the edge;
- `PCB09 socket-only underside`: J1 is the only part allowed under the strip and the tabs on B;
- `J1 grounds on In1 only`: the socket's eight GND pins join the In1 plane, not the F/B pour slivers between the strip's lanes, which cannot give them two thermal spokes.

**Holes.** H1/H2 are `MountingHole_2.7mm_M2.5` NPTH holes, marked board-only and left out of the BOM and position files, at world (−7.8, 19.33) and (50.2, 19.33). Each has an all-layer rule area of R 2.6 that keeps copper away from the DIN 912 head and the Ø4.5 standoff face.

## Layout

**Lesson: the board as a set of lanes.** The socket's two rows of Ø1.7 mm pads, 2.54 mm apart, leave four narrow channels on every copper layer along the strip:
- **A**, above the outer row (one track up to 0.49 mm);
- **U** and **L**, two 0.16 mm tracks between the rows;
- **W**, below the inner row (one track up to 0.45 mm).

A net launched from an outer pin can only use A or U without crossing another lane, and an inner pin can only use L or W. A lane must also leave the strip in order: A turns up first, then U through a pin-row gap, then L, then W. Ten nets run the strip's length, so the lanes had to be planned before any track was drawn. Most of this lesson was choosing which net goes in which lane, so that each copper layer reaches its connector with no tracks crossing.

**Headless editing (D-092 item 7).** The KiCad Nightly GUI had PCB-02 open in a parallel session, and KiPy talks only to the open board. So [design/layout_pcb09.py](design/layout_pcb09.py) writes the set-up, placement, every track, via and pour into the `.kicad_pcb` through [../tools/kfile.py](../tools/kfile.py), the file-based counterpart of `kp.py`. The Nightly `kicad-cli` then refills the zones and runs DRC with parity. Every coordinate is written by hand in the script, and `kfile.track()` refuses any segment that isn't at 0°, 45° or 90°. **No autorouter was used.** Rerunning the script removes its own items (one UUID namespace) and writes them again; `--export` also writes the outputs.

**Placement** (KiCad x, y; world in brackets):
- Top face:
  - J2 (143.0, 103.6) r180, the side-entry header at the +Y edge;
  - **U1** (143.045, 112.0) r90, the head THVD1451, its 8–5 pins under J2's 5–2 and its 1–4 pins facing the strip;
  - C1 beside U1;
  - J5 (153.7, 104.0) fan;
  - J3 (164.5, 103.3) base;
  - J4 (161.5, 111.3) audio, with its pads facing the audio band;
  - TP3/TP5 in the bay extension, TP6 on the 5V track.
- Bottom face:
  - U2 (164.5, 110.9) r90 under J3, its 5–8 pins one via each from J3's 2–5 pins;
  - R4 and R3 over the U2/J3 and U1/J2 vias;
  - R1 under U1 (HEAD_TX reaches it by a via under U1's body);
  - R2 and C2 beside U2;
  - the fan switch Q1, R5, R6, D1, C3 and C4 under J5.

**Strip lanes:**

| Layer | A | U | L | W | Pad rises |
|---|---|---|---|---|---|
| F | HEAD_RX (pin 10 → U1 pin 2) | HEAD_TX (pin 8 → U1 pin 3) | LRCLK (pin 35, gap 146.22) | SDI1 (pin 15 → past the pins) | SDO0 (pin 40) |
| In1 | 3V3 (pin 1 → U1's via) | — | — | 5V (pins 2/4 → the 5V via) | (GND plane) |
| In2 | BCLK (pin 12 → via at 148.76) | SDI0 (pin 38 → via) | AMP_SD (pin 16 → via) | 3V3 link pins 1–17 | (3V3 bay plane) |
| B | FAN_EN (pin 18 → R5) | — | BASE_TX (pin 7 → U2 pin 3) | BASE_RX (pin 29 → U2 pin 2) | 5V link pins 2–4 |

In the bay:
- The **F audio band** runs under J4's pads: six 0.16 mm tracks at 0.32 mm pitch, LRCLK on top. Each peels up into its pad. Entry order is the J4 order: LRCLK, then BCLK by via, SDO0, SDI1, then SDI0 and AMP_SD by via.
- The **B band** carries BASE_TX over BASE_RX into U2's 1–4 row.
- **5V**: In1 W lane → via → F, round U1's right side, through TP6 to J5.1, with a via to the fan parts on B.
- **3V3**: the In2 plane covers the bay. In the strip, AMP_SD's lane cuts In2 off, so 3V3 also rides In1's A lane to U1's via.
- **GND**: In1 is solid except the two power tracks; F and B are GND pours with stitching vias.

Totals: 142 segments, 27 vias, 4 pours, 3 rule areas.

## Checks and outputs (rev A, 2026-11-06)

| Check | Result |
|---|---|
| Nightly ERC, all severities | **0 errors, 0 warnings** |
| Nightly DRC with schematic parity, all severities, zones refilled | **0 violations, 0 unconnected, 0 parity issues** ([design/layout-drc.json](design/layout-drc.json)) |
| Footprint/model audit | All 21 fitted footprints name a stock 3D model that exists on disk; the six test pads and two holes have none. The STEP's `PRODUCT` list carries every model |
| `check_pcb09_mount.py` (final/v1/cad) | **7/7**: socket stack 106.447 vs standoff top 106.450; standoffs coaxial with the Pi inserts; ≥ 0.5 mm webs round both holes; mount clears its neighbours by 0.2 mm; planted hex standoff and un-raised tab hit the cooler; the bench-assembled unit slides in ([mount-check.json](mount-check.json)) |
| `check_pcb09_fit.py` (final/v1/cad) | **5/5**: the KiCad core is the droid board (offset 0.000, underside Z 106.450, area + holes = 983.5 mm²); the socket model is centred on the Pi header and seated on its plastic (−0.03 mm); every part and the four rebuilt plugs clear the robot by 0.2 mm; the real parts slide in with the tray. Info: the J9-3 plug top is 0.1 mm under PCB-05's +Y edge plug reserve |
| `check_pcb09_inputs.py` | Reruns with the tabs and extension; zero core clashes ([mechanical-audit.json](mechanical-audit.json)) |
| Final integration | PCB-09's KiCad STEP replaces the placeholder in `pcb_integration.py`; `check_pcb_integration.py` result in [final/v1/cad/pcb-integration-report.json](../../final/v1/cad/pcb-integration-report.json) |

Outputs:
- the [board STEP](cad/pcb-09-c0-link-adapter-revA.step), exported with `--user-origin 0x0mm`;
- [fab/revA](fab/revA/README.md): Gerbers, drill, BOM, position and CPL files, the zip and the order parameters.

## Open items

- **Stage 2 (procure):**
  - quote **two-sided assembly** (SMD on both faces) plus J1, one THT part on B;
  - source the SSW-120-01-T-D from element14;
  - order THVD1451DR × 2 from Mouser India (consign them);
  - find the round Ø ≤ 4.5 mm M2.5 × 11 standoffs (BO-065);
  - take the GH headers from the fab's stock;
  - run the DFM check.
- **Bench:**
  - CR-02 / HA-05…07: boot console, overlays, audio overlay and the measured fan run, start and stall current against the AO3400A, 1N5819HW and GH 1 A rating;
  - TX idle level with the 4.7 kΩ pull-ups;
  - socket seating on a real Pi, and a tin-on-gold contact-resistance check after vibration.
- **Stage 3:**
  - harness dressing for W24–W26 and W41 (the J9-3 plug sits under PCB-05's plug reserve);
  - PCB-08 `J8-4` and PCB-12 adopt the J9-1 order;
  - the builder's review of the board in the Nightly GUI.

### Workflow comparison — 2026-11-01 (review stage, before D-092)

Compared with the playbook and PCB-15, PCB-11, PCB-06, PCB-05 and PCB-10. Their lesson counts vary; the playbook's step numbers below are the common sequence.

| Playbook step | PCB-09 evidence / disposition |
|---|---|
| 1. Freeze inputs | **Open.** D-073 allocation and D-074 strip extension are accepted, but socket height, support and populated fit are not frozen. Subsequent work is provisional, not permission to skip this gate |
| 2. Schematic | Real Nightly schematic, stock symbols, labelled nets, PWR_FLAGs, NCs and bare-copper exclusions; ERC 0/0 and exported-netlist check. PDF added to match the other boards |
| 3. Board set-up | Real outline, 1.6 mm two-layer core, local origins, PCB-15 fab-neutral `.kicad_dru`, and a proved socket-only rule area. Project minimums and Default routing presets aligned with PCB-10, below |
| 4. Layout handoff | Native Tools → Update PCB from Schematic (F8), then save, then KiPy on the open board. This handoff occurred in the prior session. The builder's normal lesson checkpoint must be explained before future circuit transfers; KiPy does not replace F8 |
| 4. Placement and routing | Candidate placement read back and DRC checked; **routing not started**. Reapply `exclude_from_pos()` after every F8, then `refs_to_fab()`, `audit()` and save; rerun parity DRC after circuit changes |
| 5. Checks and outputs | Model-path audit and review exports exist. No populated-board STEP fit check, fab package or released revision; these must wait for completed design and the normal final checks |

**Project preset mismatch (corrected).** The fresh `.kicad_pro` had the stock Default via of 0.60/0.30 mm, below the 0.67/0.35 mm custom rule. After saving and closing Nightly, copied only PCB-10's fab-neutral project minimums and Default clearance/track/via settings: clearance/track minimum 0.16 mm, edge 0.30 mm, hole clearance/separation 0.31 mm, via diameter/drill 0.67/0.35 mm, annulus 0.16 mm and silkscreen text 1.0/0.16 mm; normal signal width stays 0.20 mm. No circuit-specific rules or four-layer stackup were copied. [workflow-review.json](design/workflow-review.json) records before/after values. DRC and ERC exclusion lists are empty; ERC severities match PCB-05/10. Native control initially timed out at the 3D Viewer, then recovered; the project was closed before the file edit, as the playbook requires. Reopened PCB-09 in Nightly and read the live Default net class through KiPy: 0.16 mm clearance, 0.20 mm signal width and 0.67/0.35 mm vias. Fresh ERC remains 0/0; placement DRC remains 0 violations, 0 parity issues and 67 unconnected items.

**Resume point.** Finish the input/mechanical gaps and freeze the candidate placement before routing. At the next schematic change, open the saved schematic in Nightly, save it, use F8 in the PCB editor and inspect its change list before applying; preserve existing placements. Reapply bare-copper exclusions, read back changed pads and run parity DRC before continuing with KiPy. This is the same handoff used on the earlier boards, without restarting the existing project.

## Log

- **2026-10-31:** lesson-1 header audit drafted. Checked the official 40-pin diagram, RP1 mux/reset tables and Raspberry Pi reset clarification, TI transceiver ratings, UART/fan overlay sources and existing build contracts. Added 40-row draft map, HA-01…08, normal 3V3 estimate and explicit unresolved 5 V fan budget. CR-01 remains D-067 accepted; CR-02 remains OPEN. Builder dispositions pending; no schematic, CAD change or interface freeze yet.

- **2026-10-31:** builder selected all three recommended dispositions: labelled I²C1 SDA/SCL/GND service pads without added pull-ups; fitted 4.7 kΩ pull-ups on both UART TX lines; GPIO24 with D-042's 100 kΩ gate pull-down. Recorded D-073 and allocation baseline v0.2. CR-02 remains OPEN for boot/overlay and fan-current evidence. No schematic or CAD implementation yet.

- **2026-10-31:** measured mechanical inputs with the current body/chassis and droid edits; added `check_pcb09_inputs.py` and `mechanical-audit.json`. Found 16 socket pads outside the narrow strip, head-IC copper overlaps, GH courtyard overlap and the base-IC/fan-header reserve conflict. Proposed strip edge Y 22.4 and real-footprint repacking; envelope decision, socket MPN/height, retention and assembly proof remain open. No robot geometry changed.

- **2026-10-31:** builder approved the strip extension; implemented D-074 in the final assembly only. Rerun verifies all 40 socket pad envelopes at 0.3 mm edge margin, one core solid, +97.68 mm³ and zero static core clashes. Added a focused review scene. ME-02…07 and CR-02 remain open.

- **2026-10-31, Nightly implementation follow-up:** created the actual project in Nightly, authored the review schematic, transferred it with F8, applied the D-074 outline and real footprints through KiPy, corrected/read back the underside socket orientation, added/proved the socket-only rule, and cleared placement/library warnings with native library refresh. Final ERC 0/0; placement DRC 0 violations and 0 parity issues, 67 unrouted. Package-matched the diode to 1N5819HW/SOD-123. Mechanical freeze and routing remain open.

- **2026-11-01:** compared the project and README with PCB-05/06/10/11/15 and the playbook. Restored the common Schematic / Board set-up / Layout / Checks / Open items structure, corrected the stale lesson-1 status, added a schematic PDF and recorded the exact F8 → save → KiPy handoff. Found and corrected stock project routing presets after saving/closing Nightly; recorded the before/after comparison. Native control recovered after an initial timeout. No circuit, placement or input-freeze approval changed.

- **2026-11-01:** the completed PCB-05/06/10/11/13/15 designs were integrated in the final assembly and both whole-robot exports rebuilt. PCB-09 remains a provisional placeholder with D-074’s strip extension; no populated PCB-09 fit or mechanical input freeze is claimed.

- **2026-11-06:** inputs frozen and the board laid out on a separate branch (`pcb-09-c0-link-adapter`) while PCB-02 used the Nightly GUI (D-092).
  - Builder choices:
    - Samtec SSW-120-01-T-D (tin);
    - HAT-style M2.5 × 11 round standoffs at Pi holes 3/4, with outline tabs and bench assembly;
    - J9-1 on the W25 rule;
    - four layers;
    - headless layout;
    - J9-4 as a GH 2-way SMD header;
    - the bay 6 mm longer toward −X.
  - CAD: `PCB09_MOUNT` in the final assembly, `check_pcb09_mount.py` 7/7, `check_pcb09_inputs.py` updated.
  - Layout: written by hand in `layout_pcb09.py` (new `tools/kfile.py`); ERC 0/0; DRC 0/0/0.
  - Outputs: fab/revA and the board STEP.
  - Fit and integration: `check_pcb09_fit.py` 5/5; KiCad STEP installed in the final assembly with rebuilt plugs.
