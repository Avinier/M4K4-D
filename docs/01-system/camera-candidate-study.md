# Makad V1 Head-Camera Candidate Study

| Field | Value |
|---|---|
| Status | **SELECTED AND LOCKED — Raspberry Pi Camera Module 3 Wide, visible-light/IR-cut, order code SC0874** |
| Version | 0.2 |
| Owner | Project builder |
| Created | 2026-08-29 |
| Last reviewed | 2026-08-29 |
| Feeds | RP-01 moving-harness work, RP-06 layout, RP-07 person tracking, ADR-01/ADR-08/ADR-09/ADR-12 |
| Selected upstream component | Waveshare ESP32-S3-LCD-4.3 no-touch, SKU 30493 |

## Selection and decision boundary

Makad V1 uses **one central colour camera in the moving head**. The selected module is the **Raspberry Pi Camera Module 3 Wide, visible-light version with integrated IR-cut filter, commonly listed as order code SC0874**. This explicitly excludes Camera Module 3 Standard, Camera Module 3 NoIR and Camera Module 3 NoIR Wide.

This is a component lock, not a claim that the integrated camera subsystem has already passed. It must still support nearby face/person acquisition, head-directed attention, reacquisition, a same-room come/follow route of up to approximately 3 m, and bounded obstacle evidence. Its complete connector, moving link and mount must remain usable through the three-axis head workspace.

The display choice already fixes head-local face rendering. Camera frames still go to the body-mounted Linux perception computer, so the camera interface crosses the moving head unless a later architecture revision relocates compute.

## Selected module and contingency references

Stock and price below are web-listing snapshots from **2026-08-29** and must be reconfirmed before payment.

| Candidate | Imaging and envelope | Link | India evidence | Current role |
|---|---|---|---|---|
| **Raspberry Pi Camera Module 3 Wide — SELECTED** | Sony IMX708, colour rolling shutter, 11.9 MP, PDAF autofocus, HDR, 120° diagonal / 102° horizontal / 67° vertical FOV, common modes through 1080p50, **25 × 24 × 12.4 mm** | 2-lane MIPI CSI-2; official product brief specifies a 200 mm, 15-way 1 mm-pitch FPC | [ElectroPi](https://www.electropi.in/raspberry-pi-camera-module-3-wide) listed ₹3,088 and 62 available; [Silverline](https://www.silverlineelectronics.in/products/copy-of-test-1) listed ₹3,210 and in stock | **Locked camera module; supplier and production moving interconnect remain open** |
| Arducam B031202 IMX708 Wide | Same sensor class and nominal 120° diagonal / 102° horizontal FOV; rolling shutter; autofocus; 25 × 24 × 11.5 mm listing; includes 15 cm 22↔22 and 15↔22 FPCs | MIPI CSI-2 | [Fab.to.Lab](https://www.fabtolab.com/arducam-b031202-12mp-imx708-autofocus-wide-angle-camera-module-3-raspberry-pi-hdr-mode-pdaf-supported) listed in stock; landed price needs confirmation | Contingency substitute only; using it requires recorded camera change control |
| Arducam 12 MP UVC camera with 110° horizontal M12 lens | 12 MP colour, manual-focus interchangeable M12 lens, MJPEG/YUY2, advertised 4K30 | USB 2.0 UVC | [Robu](https://robu.in/product/arduam-12mp-usb-camera-module-with-m12-lens/) has a domestic listing; current stock, price, board dimensions, working current and installed mass remain unverified | Moving-link contingency/diagnostic reference only |
| Waveshare OV5693 5 MP USB camera | 5 MP colour, 95° horizontal FOV, autofocus, **18 × 18 × 19.69 mm** listing; 1080p15 listed | USB 2.0 | [Robu listing](https://oldwp.robu.in/product/waveshare-ov5693-5mp-usb-camera-fixed-focus-auto-focusing-m12-camera-module/) | Compact USB contingency; 15 fps and 500 mA listing are disadvantages |
| Arducam OV9281 global-shutter USB board | 1 MP high-frame-rate global shutter | USB UVC | [Robu listing](https://robu.in/product/arducam-120fps-global-shutter-usb-camera-board-1mp-ov9281-uvc-webcam-module-with-low-distortion-m12-lens-without-microphones/) | Motion-blur diagnostic reference only; not a colour-camera substitute |

The official [Camera Module 3 Wide product page](https://www.raspberrypi.com/products/camera-module-3/?variant=camera-module-3-wide) and [product brief](https://pip-assets.raspberrypi.com/categories/786-raspberry-pi-camera-module-3/documents/RP-008151-DS-1-camera-module-3-product-brief.pdf) are the primary specification references. [TME's SC0874 listing](https://www.tme.eu/en/details/sc0874/raspberry-pi-acessories/raspberry-pi/camera-module-3-wide/) provides the commonly used order code. Seller-reported weights conflict and often include packaging, so **no camera mass is accepted until the sample, cable, stiffeners and mount are weighed separately**.

## Standard versus wide lens

The standard Camera Module 3 has greater face pixel density and a brighter nominal lens, but its approximately 66° horizontal FOV gives less room for initial acquisition, head/body movement and obstacle context. Makad has only one camera and must search, track and follow within a room. The selected Wide module's approximately 102° horizontal view prioritizes coverage. RP-07 must still prove adequate target pixels and calibrated distortion across 0.6–3 m.

## The real blocker: moving link

| Path | Advantage | Risk to prove |
|---|---|---|
| CSI over ordinary camera FFC | Lowest camera-board mass, direct RAW path, mature Picamera2/libcamera support | Common FFC is primarily bend-to-install, not a documented continuous-flex harness; three-axis service loops can develop restoring torque, conductor fatigue or ZIF movement |
| USB UVC over fine round cable | Replaceable, mechanically familiar, tolerant of a longer body-to-head run and broad SBC support | Larger/heavier camera electronics, cable mass and stiffness, compression/USB buffering latency, power and connector retention |
| CSI with a purpose-designed moving interconnect or bridge | Retains the preferred sensor while improving service/flex behaviour | Extra boards/connectors/mass/cost; exact dynamic rating and latency must be sourced rather than assumed |

Do not treat a static FFC bend-radius claim as a flex-life rating. The selected harness must record conductor construction, connector retention, bend/twist geometry, service-loop length, installed mass, signal errors and endurance cycles.

## Shopping criteria for other agents

Use this minimum capture schema for every proposed camera:

1. Exact manufacturer part number and lens/FOV suffix; reject listings that mix standard and wide specifications.
2. Colour sensor; shutter type; sensor size and pixel size; RAW/compressed output; real 1080p frame rate; autofocus/fixed/manual focus and useful focus range.
3. Horizontal, vertical and diagonal FOV separately; distortion/calibration data if available.
4. PCB width/height, lens projection, connector orientation, bare module mass, cable mass, mount mass and installed centre-of-mass location.
5. Exact interface, connector pin count/pitch, supplied cable length, permitted host/SBC and Linux driver path.
6. Exposure/HDR and image quality under ordinary household light; rolling-shutter smear during representative head motion.
7. Source timestamps or demonstrable frame-age measurement; buffering and end-to-end capture latency at the intended mode.
8. India stock, GST-inclusive price, dispatch location, return terms and one true substitute.
9. For the complete link: minimum bend radius **and dynamic flex/torsion rating**, connector retention, bend locations, service path, replacement cost and spare availability.
10. Evidence at Makad geometry: face/person detection at 0.6, 0.9, 1, 2 and 3 m; target exit/re-entry; household lighting; head motion; camera-side LED on/off; display animation on/off.

## Acceptance and change control

The module is locked now so procurement, CAD, perception setup and harness testing have an exact target. The following are acceptance tests, not permission to resume an unconstrained camera comparison:

- adequate acquisition/tracking and calibrated FOV over the RP-07 geometry;
- acceptable motion smear, exposure behaviour, frame age and processing load;
- no unacceptable display or status-light optical contamination;
- a complete moving cable that clears roll/pitch/yaw, produces acceptable restoring torque and survives the registered endurance block without frame errors or connector movement;
- measured installed mass/CoM inside the RP-01 envelope;
- confirmed compatibility with the selected body SBC;
- one verified India source and one acceptable substitute, or an explicitly accepted single-source risk.

Reopen the camera-module selection only after a recorded hard failure: procurement unavailability, selected-body-SBC incompatibility that cannot be resolved without disproportionate architecture cost, inadequate RP-07 acquisition/tracking/FOV/exposure evidence, unacceptable rolling-shutter/frame-age behaviour, mass/envelope failure, optical contamination that cannot be packaged out, or failure to produce a viable moving CSI interconnect. A failure of the supplied ordinary FPC alone first triggers moving-link redesign; it does not automatically reject the selected sensor module.

## Selection record

**Selected:** Raspberry Pi Camera Module 3 Wide, visible-light/IR-cut version, order code SC0874. Buy one sample first; a second unit waits for acceptance evidence. The body SBC, supplier and production moving interconnect are not selected by this decision. The supplied 200 mm FPC may be used for static bench/image work but is not accepted as the production three-axis moving harness without endurance evidence.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-08-29 | 0.1 | Added the exact camera and moving-link shortlist, India leads, shopping criteria and seven-part lock gate. |
| 2026-08-29 | 0.2 | Project builder selected and locked Raspberry Pi Camera Module 3 Wide, visible-light/IR-cut, order code SC0874; converted the prior lock gate into acceptance/change-control evidence and left supplier, body SBC and production moving interconnect open. |
