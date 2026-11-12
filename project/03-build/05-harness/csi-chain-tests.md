# CSI chain: bench tests before ordering (D-105)

D-105 runs the camera ribbon outside the head. The CAD check (`final/v1/cad/check_d105_csi_loop.py`) proves the geometry, but four questions can only be answered on the bench. Run them in this order: the stream test decides whether the chain survives at all, and the other three refine it.

The chain under test, Pi end to camera end:

| Segment | Part | Length | Joints |
|---|---|---|---|
| W37, through the yaw cassette | generic 22-way 0.5 mm FFC (BO-050) | ~200 mm | Pi 5 CAM socket; PCB-14 board 1 lower ZIF |
| PCB-14 board 1 | joiner, straight-through (D-101) | 17 mm | two FH34SRJ |
| W45, static on the yaw disc and bracket | generic 22-way FFC (BO-050) | ~355 mm `E` | PCB-14 board 1 upper ZIF; bracket joiner J2 |
| Bracket joiner (fourth PCB-14) | same board | 17 mm | two FH34SRJ |
| W46, the loop | Raspberry Pi standard-mini 300 mm, **shielded** (HD-017) | 300 mm | bracket joiner J1; Camera Module 3 |

That is about 890 mm with four FH34SRJ transitions. Raspberry Pi's engineers do not recommend camera cables over 500 mm: the D-PHY lanes run at up to 500 MHz with a 200 mV swing, and a link that fails shows **magenta bands** where a line was dropped ([forum](https://forums.raspberrypi.com/viewtopic.php?t=369349)). Users run 1–2 m FFCs successfully, but without guarantee; Arducam sees occasional corruption beyond 1 m ([Arducam](https://blog.arducam.com/top-accessories-camera-module-3/)). So the stream test is the gate for the whole of D-105.

## 1. Full-chain stream test (gate)

**Set-up.** Lay the real chain flat on the bench at the real lengths, with both joiners. Cut W45 from the BO-050 stock to the length measured in the fold mock-up (test 3). Before power, meter conductor 1 at the Pi socket to the camera's pin 1 and the camera's 3.3 V conductor end to end. FH34SRJ accepts either face, so a flipped cable puts 3.3 V on a ground.

**Run** on a Pi 5 with the robot's camera mode:
1. `rpicam-hello --list-cameras`: the IMX708 is detected.
2. `rpicam-vid -t 1800000 --mode <robot mode> -o /dev/null --framerate <robot rate>` for 30 minutes while logging `dmesg -w`.
3. Repeat with both head servos and the drive motors running under load, and with the chain laid along a motor lead (the robot's real EMI).
4. Repeat with the loop cable flexing by hand through its full pitch travel.

**Pass:**
- no magenta or green bands in a saved clip (spot-check 5 minutes at full resolution);
- no `rp1-cfe` / CSI errors or frame-start timeouts in `dmesg`;
- frame count within 0.1 % of the expected count.

**If it fails**, try in order and re-test:
1. **Drop the bracket joiner** (two transitions fewer): one custom 22-to-15 FFC from PCB-14 board 1 to the camera, about 650 mm.
2. **Shorten W45.** The disc run and climb are geometry, but folds can be tightened by up to about 20 mm.
3. **Replace W45 with an Arducam CSI-to-HDMI pair** on the disc and the bracket. The HDMI cable's shielded 100 Ω pairs carry D-PHY better than an unshielded FFC; Pi 5 users report 1 m working and 5 m failing ([Arducam forum](https://forum.arducam.com/t/csi-to-hdmi-with-b0399-64mp-cam-rasp-pi-5/7312)).
4. **A serialiser extension kit** (FPD-Link class). This means a head redesign.

## 2. Loop flex-cycle test

**Why.** The official cable is a laminate with a shield, which is stiffer and has thinner outer layers than the plain FFC the design radius assumed (R 15.4 mm, 1.0 % strain at 0.3 mm). Field reports run both ways:
- One pan-tilt user saw a standard cable "break up and fall apart" after a few dozen flexes, almost certainly at a tight radius.
- Others report a year or more of daily pan-tilt use, and 800 h on a 3D-printer gantry ([forum 1](https://forums.raspberrypi.com/viewtopic.php?t=297215), [forum 2](https://klipper.discourse.group/t/i-need-help-setting-up-my-webcam/9180)).

Datasheets for polyester FFC give these lives:

| Source | Cycles | Bend radius | Notes |
|---|---|---|---|
| Axon, standard 0.5 mm pitch | 100k–500k | R 10 mm | |
| Axon, 50 µm flexible | 2.5M | R 10 mm | |
| Flex Connection, 0.5 mm pitch | > 3M | R 15 mm | |
| GCT | 100k | R 10 mm | |
| Molex standard jumper | 6,000 | — | test conditions not given |
| Molex extra-flexible 0.12 mm | 900,000 | — | test conditions not given |

Construction matters more than anything else ([Axon](https://www.axon-cable.com/publications/Axojump-flat-flexible-cables_cg.pdf), [Flex Connection](https://flexconnection.global/products/0-50mm-pitch-flexible-flat-cable/), [Molex](https://www.content.molex.com/dxdam/2d/2d73ee52-1c37-44c5-8b5e-787e4af51b13/987650-6631.pdf)).

**Measure first.** Measure the received cable's thickness at the loop section with a micrometer. If it is over 0.3 mm, rerun `check_d105_csi_loop.py` with `D105["ribbon"]["t"]` set to the value; the strain scales with it.

**Jig.** Print the bracket top and a dummy head arm that swings the head clamp through the real arc: pitch −25° to +43° about a pivot 73 mm away, and at least ±21° of twist at the head clamp. Use the real clamps.
- Cycle at 0.5 Hz while streaming as in test 1, logging errors.
- Target **50,000 cycles** with no stream errors and no visible cracking. For scale, 10 nods a minute for 8 hours a day is about 4,800 a day.

**If it fails early:**
1. Retest with an unshielded Arducam 22-to-15 cable of the same length; check the stream again.
2. Then a **polyimide flex cable** in the same outline: rolled-annealed copper, single layer, ground-signal-ground pairs. It drops into the bracket joiner, and the loop geometry is unchanged.

## 3. W45 fold mock-up

The static FFC's folds are reserve boxes in the CAD (`HARNESS_D105_CSI_*`). Fold a length of the real BO-050 FFC through a printed bracket and a printed disc segment, or a 1:1 paper print of the head-local plan:

1. **Out of the channel.** At the CSI exit (head-local Y ~22–29.8) the CSI is the top FFC of the stack. Lift it out of the channel and make one **45° crease** so it runs −X, flat on the disc at Y 16.6–28.6. It must stay below Y 29.8: PCB-16's rise reserves start there.
2. **Disc and tray.** Lay it flat to the rim (X −91.5), up 2.5 mm onto the bracket tray past the rim, and along the tray to X −150.
3. **Climb.** Make a 90° bend up (no crease) beside the +Y carbon tube, in the tube's plane (X −150, Y 16.6–28.6), clipped to the tube every ~30 mm, up to Z ~118.
4. **Top.** Make a 90° bend forward over the joiner (no crease), then a **pair of 45° creases** to shift it 17.6 mm toward −Y onto the ribbon centre (Y −1). Run past J2's mouth (u ≈ 22.3) and make a 180° turn down (R ≥ 2 mm) back into J2.

**Pass:**
- the cable seats fully in both ZIFs;
- conductor 1 is on the same side at both ends;
- no crease falls within 5 mm of a ZIF mouth;
- the folded stack stays inside the reserves;
- the measured length is ≤ 360 mm.

Record the length for the stream test.

## 4. Head clamp bond pull test

The clamp base (HD-020) is bonded to the 1.6 mm rear cover. The cover cannot take inserts, and the roll servo's sweep leaves no room for bosses behind it.

**Loads.** In service the loop pulls on the clamp with well under 1 N (EI/R² ≈ 100/15² N). A snag (a hand or a cable caught in the loop) is the design case.

**Coupon.** Print a cover-material coupon and a clamp base. Bond with 3M VHB (4910 or 5952 class) after an IPA wipe and adhesion promoter on the print; cure 24 h. Pull normal to the cover with a luggage scale.
- **Pass:** ≥ 20 N without peel.
- Then pull 10 N in shear along the loop direction for 10 s, ten times.

**If it fails,** add two M2 through-bolts with thin nuts inside the cover beside the strip. Re-check their clearance to the roll servo's sweep first: the outside run is 2.6 mm from it at roll 21°, pitch 43°.
