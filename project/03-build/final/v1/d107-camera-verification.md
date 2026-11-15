# D-107 camera harness verification — 2026-11-14

**Result: FAIL / HOLD.** The signal-chain concept is supported by the B0091 documentation, but the current CAD does not verify a buildable camera harness. Do not use the earlier 72/72 clearance count as camera-chain qualification. No hardware was ordered, printed or bench-tested in this review.

## Manufacturer facts

- [Arducam B0091 product page](https://www.arducam.com/arducam-csi-hdmi-cable-extension-module-15pin-60mm-fpc-cable-raspberry-pi-camera-specific-pack-2-1-set.html): one current kit contains two CSI/HDMI adapter boards, two 60 mm 15-pin FPCs, two 73 mm 22-pin FPCs and M2 screw sets. HDMI cable is a separate item. It explicitly lists Camera Module 3/IMX708 and Pi 5 support and calls for a high-quality HDMI 2.1 cable. The board footprint is 27.63 × 25.00 mm. This is a passive CSI extension over HDMI conductors, not a monitor HDMI signal.
- [Arducam HDMI extension instructions](https://docs.arducam.com/Camera-Extension-Solution/HDMI-Extension-Kit/) show a camera-to-adapter ribbon, an adapter-to-Pi ribbon and an HDMI cable between the two boards. They do not document removing 120 mm of the HDMI cable's jacket/shielding for a moving neck.
- [Raspberry Pi Camera Module 3 specification](https://www.raspberrypi.com/products/camera-module-3/?variant=camera-module-3-wide) lists a supplied **200 mm 15 × 1 mm** ribbon. The current CAD assumes a separately selected 150 mm head ribbon. The supplied 200 mm cable could reach the 111.198 mm nominal head path, but its extra slack/contact orientation have not been dressed in CAD or checked with received parts.
- [Arducam B0210](https://www.arducam.com/arducam-for-raspberry-pi-zero-camera-cable-set-1-5-2-87-5-9-ribbon-flex-extension-cables-for-pi-zerow-pack-of-3.html) is a concrete 15-to-22-pin set with 38, 73 and 150 mm cables. A 150 mm member is the candidate for the Pi end; the B0091 kit's 73 mm Pi cable fails the present 84.965 mm route plus insertion/service budget. Verify its contact faces on the actual B0091 and Pi 5 connectors.
- The [older Arducam mechanical drawing](https://www.uctronics.com/download/Amazon/B0091_CSI_to_HDMI.pdf) confirms a 25 × 27.63 mm board outline but is from 2017 and lists an older 80 mm ribbon package. Its hole pattern and current connector heights/position should not be treated as a current board qualification. The CAD board envelope is 25.2 × 27.83 mm, an extra 0.1 mm on each side; connector and plug envelopes remain estimates.

## Independent CAD audit

Reproduce with `check_d107_camera_chain.py` using the legacy runtime specified in [final/v1 README](README.md). The report is [2/5 PASS](cad/check_d107_camera_chain-report.json); the three failures are:

1. **Head HDMI approach is wrong.** The modeled head plug extends to Y=+15.915 mm and Z=72…79 mm. The last two lead points are (−67,14.5,71) and (−67,15.5,75). The lead comes from **below the plug** and points toward +Y. A real cable must approach the plug's rear from beyond Y=+15.915 and point toward −Y into it, with room for its boot and a bend. The old 24.835 mm³ overlap test proves only that the solids intersect; it misses this reversed approach.
2. **Head ribbon is five independent slabs.** Its 111.198 mm centerline reaches under the chosen 150 mm stock budget (13.802 mm nominal reserve after 25 mm insertion/service), but the CAD does not model a continuous ribbon with contact direction or fold/strain relief at its sockets.
3. **Body ribbon lacks 65.035 mm of stock dress.** Its modeled centerline is 59.965 mm. The selected 150 mm cable has 65.035 mm left after the same 25 mm allowance, yet the loft draws no such excess. In the Viewer it rises into wide vertical sheets and a crossed fold. One valid solid and zero CAD interference do not make that a believable FPC installation.

The body HDMI cable starts at the modeled plug's rear face and leaves toward +Y. The head 150 mm ribbon passes the arithmetic reach check. The previous neck/body checks remain clearance screens, not a strength, retention, electrical or cable-life certificate.

The focused [head camera audit STEP](cad/d107-head-camera-audit.step) was opened in CAD Viewer. Its front view confirms the lead rising through the bottom of the plug/board envelope and shows the separate head ribbon slabs. This is review geometry exported from the current source, not a redesigned harness.

## Physical acceptance still required

Select and receive a high-quality HDMI cable; measure its complete head plug/boot against the finished Ø18 liner; test the **actual cable construction** through the neck and at every pitch/roll/yaw pose. Arducam's stated B0091 compatibility is for an HDMI cable, not for the custom jacket-stripped moving section in D-107. Maintain pair shielding/geometry and prove camera streaming through C0–C4 under movement before approving the alteration. Measure the received adapter connectors/contact faces and retainers; fit/dress both real ribbons without tension or sharp folds. Until these checks and the CAD failures above are resolved, the camera harness is **not sorted**.
