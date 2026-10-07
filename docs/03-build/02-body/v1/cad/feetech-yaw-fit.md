# ST3215-HS yaw-bay fit screen

> **Superseded by [D-048](../../../decisions.md#d-048) (2026-10-07).** The screens below put the STEP
> origin on the pinion; the horn axis is 25.5 mm from it (Waveshare 2D drawing: 10.11 mm from the
> case end), and the "case screw" holes are the horn's. The live model now installs the servo on the
> true axis, horn up, case −X, 7.6 mm lower, with the compute stack shifted +10 X / −6 Y;
> `check_yaw_stage.py` and `check_compute_mount.py` pass on it. Keep this page as history only.

The [checker](check_feetech_yaw_fit.py) places the official ST3215-HS STEP at
the existing pinion centre (X 16, Y 37 mm), purchased-STEP top Z 130 mm. The
actual horn mating plane still needs measurement. The checker tests
the **entire authored PCB-09 envelope** (GPIO socket, strip, bridge, main box,
top and side plugs), the live primary frame, Pi STEP, placed Active Cooler,
fan and C3 carrier. Results are in
[`feetech-yaw-fit.json`](generated/feetech-yaw-fit.json). The official STEP has
one invalid-topology main-case solid, so these numbers are packaging evidence,
not manufacturing clearance approval.

| Clocking at current pinion | Confirmed solid intersections, mm³ |
|---:|---|
| 0° | PCB-09 strip **156.892**, GPIO socket 342.194, Pi STEP 310.502; frame 0 |
| 90° | PCB-09 strip 184.541, socket 338.642, bridge 25.529, main box 302.696, side plug 12.443; frame 0 |
| 180° | Frame 144.695; PCB-09 strip 75.385, socket 249.418, bridge 75.675, main box 3763.723, top plugs 940.964, side plug 232.917 |
| 270° | Frame 1121.685; PCB-09 socket 42.981, bridge 2.866, main box 302.154, side plug 93.687; fan web 2453.129 and fan box 7660.851 |

The Pi and cooler were exact-screened at 0°; the other three clockings already
failed the PCB/frame gate, so their Pi/cooler overlaps are unmeasured. **No
clocking fits at the current pinion centre with the original compute layout.** The earlier 0.388 mm X gap was
only to PCB-09's *main box* and concealed the real strip, socket and Pi
collisions. The case bottom is Z 92.2 mm.

The pinion may move around the R37 pitch-centre circle without changing the
1:1 gear ratio. The checker samples every 30° with four case clockings using
conservative neighbour boxes; none is AABB-clear, mainly because the Pi and
cooler boxes cover broad regions. The follow-up [exact relocation checker](check_feetech_yaw_relocation.py)
tests two 0° case-clock candidates:

| Pinion angle from +X | Centre XY, mm | Frame | PCB-09 complete | Pi STEP | Active Cooler |
|---:|---:|---:|---:|---:|---:|
| 210° | (−16.043, −18.5) | 162.714 | **0** | 282.080 | 671.303 |
| 0° | (53, 0) | 278.570 | **0** | 4432.234 | 2132.678 |

Volumes are mm³. These two positions clear PCB-09 but still hit the Pi/cooler
and current frame. They do not establish that *every* position on the circle
fails: intermediate angles, case clocking, axial height and a redesigned
bracket need a proper search. In particular, moving the pinion changes the
D-044 pad and shaft location and requires new checks for the hard-stop bumps,
three hub bosses, cassette exit at 300°, mesh phase, insertion path, shell,
cable, tool access and physical Pi/cooler clearance. D-047's XC330 fallback is
reserved for a demonstrated failure to fit a Feetech case, not the failed
original compute layout.

## Original-centre packaging route (provisional)

A second exact-solid trial keeps the pinion at **(16, 37) mm** on the R37
circle, at the original gear height and 0° case clocking. It removes the XC330
pad, moves the Pi 5 and Active Cooler **6 mm toward −Y**, and moves PCB-09 with
the Pi. PCB-09's wide outer board and its mounted connectors additionally move
**6 mm toward +X**; its over-header socket/strip and connecting bridge remain
registered to the Pi. This is a board-shape revision, not a loose translation
of a finished PCB. The [compute-shift checker](check_feetech_yaw_compute_shift.py)
records exact intersection volumes and minimum shape distances in
[`feetech-yaw-compute-shift.json`](generated/feetech-yaw-compute-shift.json).

The purchased HS STEP has **zero solid intersection** with the modified frame,
compute tray (with shifted Pi bosses), Pi, cooler, complete trial PCB-09,
current cartridge housing, cassette, fan web, C3 carrier and shell. The shifted
Pi/tray face has a 0.005 mm STEP placement overlap (0.327 mm³), which needs
datum clean-up before fabrication. The servo's minimum measured separations include 2.18 mm
to the Pi, 2.42 mm to PCB-09, 8.91 mm to the cooler, and 4.00 mm to the frame.
The Pi board now has about 1.17 mm to the tray's inner −Y rim in the simple
envelope; that also needs a tolerance and assembly check.
This avoids relocating D-044's pinion and leaves its gear ratio, stop and
cassette clocking at their current nominal positions. It does not certify the
gear drive or the full yaw sweep.

A [frame-integral U-cradle trial](feetech_yaw_cradle.py) replaces the old pad.
The cradle fuses into the current fan web. A separate steel strip marks the
intended front retainer location; it has **no fasteners yet** and cannot be
treated as a working clamp. The [cradle checker](check_feetech_yaw_cradle.py) finds one
valid connected solid after joining cradle and frame, and zero case/Pi/PCB-09
intersections. The **95.04 mm³** cradle/frame overlap is the intended joint,
not a component clash. Review the separate
[candidate frame STEP](feetech-yaw-frame-candidate.step),
[cradle STEP](feetech-yaw-cradle.step) and
[package STEP](feetech-yaw-package.step); these are trial sources, not the live
body assembly. The official servo's invalid-topology solid causes the package
STEP validator to fail; the locally generated cradle and candidate frame
validate independently.

Before changing the live assembly or ordering parts, the trial needs a real
retainer screw/insert pattern and load path, printed-frame stress and access
checks, a measured servo shaft datum and new BO-056 HS-compatible drive/hub, plus the
modified Pi tray bosses, PCB-09 layout and fan connector/W41 route. Re-run the
compute-tray, cooling, yaw-stage, shell and mass/stability checks on that
integrated source, including servo insertion and tool access. Finally verify
the physical HS dimensions and bench B1/B4 lash/current. The present geometry
answers the **case packaging** question; it does not release a structural mount
or complete the Feetech migration.
