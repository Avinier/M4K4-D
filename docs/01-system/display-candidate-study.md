# Makad V1 4.3-inch IPS Face-Display Candidate Study

| Field | Value |
|---|---|
| Status | **SELECTED AND LOCKED — Waveshare ESP32-S3-LCD-4.3, no touch, SKU 30493** |
| Version | 0.6 |
| Owner | Project builder |
| Created / last reviewed | 2026-08-29 / 2026-08-30 |
| Governs | `candidate-sourcing-matrix.md` face-display row |
| Feeds | RP-01 moving-head mass/roll-support blockout, RP-02 control topology, RP-06 optical/layout mock-up |

## Decision summary

The AMOLED requirement was explicitly dropped on 2026-08-29 because it imposed disproportionate cost, sourcing and controller risk. The project builder then selected and locked the **Waveshare ESP32-S3-LCD-4.3, no-touch, SKU 30493** as Makad V1's face-display module.

The selected module combines the correctly sized 800×480 IPS panel with a local ESP32-S3 renderer, 16 MB flash and 8 MB PSRAM. The body SBC can therefore send semantic face state over the eventual internal link while the head renders animations locally in LVGL. This avoids a continuous HDMI/DSI video cable across the three moving head axes.

- India listing checked 2026-08-29: **₹3,065 including GST, two units shown in stock**.
- Display: 4.3-inch IPS, 800×480, no touch, 65K colour.
- Board: ESP32-S3 dual-core up to 240 MHz, 16 MB flash, 8 MB PSRAM.
- Module outline: approximately **106.1 W × 67.8 H mm** in installed landscape orientation.
- Published product weight: **0.118 kg**. Treat this as an upper-bound/listing value until the received assembly is weighed without packaging.
- Software path: ESP-IDF/Arduino plus LVGL; official examples and documentation exist.

This is now a component selection, not a continuing display competition. Its 67.8 mm hidden body sits behind an approximately 53–54 mm-high optical aperture; the surrounding visible bezel/window treatment may be 60–65 mm high. The head CAD must provide the full hidden clearance and non-contact mounting. Its installed mass is material within the approximately 250 g complete moving-head target and must be measured immediately.

The acceptance tests below validate integration and establish measured design inputs. They do **not** reopen the selection merely because another screen is cheaper, brighter or lighter. Reopening requires a recorded hard failure: the exact module cannot be procured, cannot fit the approved envelope, forces the head beyond an accepted mass/dynamics limit, cannot meet the registered optical/animation gate, or creates an unresolved safety/reliability fault.

## Locked selection and integration gates

| Requirement | Gate |
|---|---|
| Active image | Approximately 95 W × 54 H mm in landscape; 800×480 is the preferred native resolution |
| Optical aperture / visible treatment | Approximately 94–95 W × 53–54 H mm optical aperture within a 110–115 W × 60–65 H mm bezel/window treatment; the head core separately clears the hidden 106.1 × 67.8 mm module body |
| Exact module | **Waveshare ESP32-S3-LCD-4.3, no touch, SKU 30493; substitutions require explicit change control** |
| Technology | Full-colour IPS; no touch |
| Brightness | 300 nit is acceptable only after RP-06 passes through the actual smoked window; prefer ≥400 nit when mass and controller cost are comparable |
| Refresh | Demonstrate fluid eye motion at 50–60 fps or show that the selected animation style remains convincing at the achieved rate |
| Architecture | Head-local ESP32-S3/LVGL rasterization is fixed by the selected module; the body-to-head transport remains an RP-02/ADR-12 decision |
| Installed mass | Weigh display, controller, connectors, mount, window and harness; do not use shipping weight in the mass ledger |
| Supply | Live India stock or written delivery quote; exact SKU and touch/no-touch variant verified before payment |
| Documentation | Mechanical drawing, power input, pinout, source/examples and replacement path available |

## Selected module and contingency references

| Role | Candidate | Evidence | Strength | Main risk / verdict |
|---:|---|---|---|---|
| **Selected** | **Waveshare ESP32-S3-LCD-4.3, no touch, SKU 30493** | Hubtronics India: ₹3,065 incl. GST, two shown in stock. Official specification: 800×480 IPS, ESP32-S3, 16 MB flash, 8 MB PSRAM, LVGL support, 106.1×67.8 mm, listed 0.118 kg. | Complete local-renderer architecture at nearly the cost of a bare display; thin semantic body-to-head link; open C/C++ firmware. | **Locked for V1.** Measure actual mass, 50–60 fps eye animation, concurrent communications, power and smoked-window visibility. Do not give this board motor-safety ownership until jitter/fault tests pass. |
| Contingency only | **Waveshare 43H-800480-IPS, no touch, SKU 24159** | Official: 800×480 IPS, 60 Hz, 300 nit, 1200:1, 95.04×53.86 mm active area, 105.42×67.07×2.90 mm body, 15-pin two-lane DSI, about 1.2 W. | Thin, exact active-area fit and mature Raspberry Pi DSI path. | Not an active candidate. May be reconsidered only through the hard-failure change-control rule above. |
| Contingency only | **DWIN DMG80480T043_09WN, no touch** | 800×480 IPS, 900 nit, 262K colour, T5L0 controller, UART, 8 MB flash; 93.60×56.16 mm active area. | Strong brightness and low-bandwidth UART. | Not an active candidate. May be reconsidered only through the hard-failure change-control rule above. |
| 4 | Waveshare 4.3-inch 24-bit RGB capacitive-touch module | ElectronicsComp showed about ₹2,689 before GST, four available; 800×480 IPS, 95.04×53.86 mm active area, 106×68 mm, listed 90 g. | Locally orderable and exact image geometry. | Touch is wasted and it still needs a framebuffer/controller. Its system cost and complexity are worse than rank 1. |
| 5 | Generic no-touch 4.3-inch raw RGB panel | RoboticsDNA showed ₹2,186 incl. GST and one left; 330 nit, 45-pin RGB, approximately 105.75×62.36×2.10 mm rotated landscape. | Lowest panel price and thin body. | Sparse documentation, custom controller/PCB burden and no turnkey renderer. **Do not choose on panel price alone.** |
| Bench only | Waveshare 4.3-inch HDMI LCD (B) | India listings exist around ₹5k; 800×480 IPS and roughly 110 g. | Fastest direct Linux video bring-up. | Touch, mass and a high-bandwidth HDMI cable across the gimbal make it unsuitable for the final head. |

## Why the ESP32-S3 module is selected

The panel alone is not the subsystem. Makad needs a panel, framebuffer, renderer, power path, connector, mounting and a reliable moving cable. A ₹2.2k raw RGB panel is only about ₹900 cheaper than the complete no-touch ESP32-S3 module and immediately creates a controller-board and PCB/integration project.

The local-renderer module also changes the moving harness from continuous video to small messages such as:

```text
FACE_STATE happy
GAZE x=-0.35 y=0.10
BLINK duration_ms=120
BRIGHTNESS 180
```

Assets and firmware can be updated while stationary; real-time expression commands are tiny. This is better aligned with a three-axis head than HDMI or DSI from the body.

The ESP32-S3 display board should initially own only display rasterization and face communications. A dedicated controller remains responsible for motor limits, watchdog, command expiry and head sensing until RP-02 proves that consolidating those responsibilities is safe under worst-case rendering load.

## Mechanical fit

- The 800×480 active image is approximately **95.04 × 53.86 mm**, essentially the current 95 × 54 mm target.
- A 106.1 × 67.8 mm module sits behind an approximately 94–95 × 53–54 mm optical aperture. The surrounding bezel/window treatment may occupy about 110–115 × 60–65 mm visually, but it is not the clear aperture. The hidden cavity still requires at least about 68 mm vertical module clearance.
- Do not clamp the LCD glass or PCB. Use a perimeter carrier with compliant pads, connector access and strain relief.
- Reserve space for the USB/power connector and any low-bandwidth harness before freezing the roll-support geometry.
- Verify the module's centre of mass relative to the roll and pitch axes, not merely its ability to fit inside the shell.

## Optical gate

The selected module is a 300-nit-class IPS path. First-order light through a neutral-smoke window is:

| Window transmission | Approximate output from 300 nit |
|---:|---:|
| 40% | 120 nit |
| 50% | 150 nit |
| 60% | 180 nit |
| 70% | 210 nit |

Start RP-06 with **60–70% visible-transmission neutral smoke**, a black internal mask and the smallest practical air gap. IPS black is not self-emissive black, so the mask/window stack must hide the panel rectangle when the face is dark. If that cannot be achieved without an unacceptably bright window, test the 900-nit DWIN candidate before reopening AMOLED.

## First-sample acceptance test

1. Photograph the exact SKU, invoice, board revision and packaging labels.
2. Weigh the bare received module, then the installed module with mount, connectors and harness.
3. Measure idle, typical animated-face and worst-case full-white power at the intended brightness.
4. Render the representative eye animation for 30 minutes; record achieved frame rate, frame-time spikes and board temperature.
5. Repeat while receiving semantic commands and running the intended communications stack.
6. View dark, neutral and bright faces through 60%, 70% and clear window samples under dim-room and daylight-room conditions.
7. Install the mass dummy/module in the RP-01 head blockout and measure actuator current, settling and cable restoring torque.
8. Record whether a second identical unit remains orderable and identify the DSI or DWIN fallback before committing CAD.

## Sources checked 2026-08-29

- [Waveshare ESP32-S3-LCD-4.3 official product page](https://www.waveshare.com/product/esp32-s3-touch-lcd-4.3.htm)
- [Waveshare ESP32-S3-LCD-4.3 documentation](https://docs.waveshare.com/ESP32-S3-Touch-LCD-4.3)
- [Hubtronics India — Waveshare ESP32-S3-LCD-4.3 no-touch](https://hubtronics.in/development-boards/microcontroller-development-boards/esp32-s3-lcd-4.3)
- [Waveshare 43H-800480-IPS official product page](https://www.waveshare.com/product/displays/lcd-oled/43h-800480-ips.htm)
- [Waveshare 43H-800480-IPS technical wiki](https://www.waveshare.com/wiki/43H-800480-IPS)
- [Zbotic — Waveshare 4.3-inch DSI display](https://zbotic.in/product/waveshare-4-3inch-dsi-display/)
- [RoboticsDNA — DWIN DMG80480T043_09WN](https://roboticsdna.in/product/4-3inch-800x480-ips-industrial-hmi-uart-lcd-display-without-touch-2/)
- [TME — DWIN DMG80480T043_09WN mechanical listing](https://www.tme.eu/en/details/dmg80480t043-09wn/intelligent-displays-modules/dwin-technology/dmg80480t043-09wn/)
- [ElectronicsComp — Waveshare 4.3-inch RGB touch module](https://www.electronicscomp.com/waveshare-4.3-inch-capacitive-touch-lcd-display)
- [RoboticsDNA — generic 4.3-inch no-touch RGB panel](https://roboticsdna.in/product/tft-lcd-4-3inch-480x800-2/)

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-08-29 | 0.3 | Recorded the earlier AMOLED sourcing study and controller blockers. |
| 2026-08-29 | 0.4 | Dropped the AMOLED requirement by project decision; ranked India-available IPS paths and recommended the no-touch Waveshare ESP32-S3-LCD-4.3 as the first prototype purchase. |
| 2026-08-29 | 0.5 | Project builder locked the no-touch Waveshare ESP32-S3-LCD-4.3, SKU 30493, as the V1 display; converted alternatives to change-controlled contingencies and retained integration tests as validation gates. |
| 2026-08-30 | 0.6 | Rebuilt the head-facing geometry around the selected module: separated the 94–95 × 53–54 mm optical aperture from the larger bezel/window treatment and propagated the smaller head-envelope direction without reopening display selection. |
