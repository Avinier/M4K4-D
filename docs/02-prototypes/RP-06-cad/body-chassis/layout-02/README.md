# RP-06 integrated body/chassis Layout 02

This is the active whole-body CAD path. It retains Layout 01's source-linked RP-01 head (now Layout 04), compact two-wheel chassis, connected rear skid, fixed ball-transfer nose, internal packaging and purposeful review layers, while closing the first-pass integration questions:

- four M4 through-bolts and two locating pins now define the body-frame-to-chassis interface;
- the drivetrain physically fits (CAD-context decision [`RP03-CAD-05`](../../decisions.md#rp03-cad-05--axle-stack-that-lets-the-wheels-turn)). Each coaxial gearmotor bolts its output face to a chassis flange whose R15 boss carries the 608 pair and reaches into a pocket in a dished wheel. An 8 mm stub shaft runs in the bearings, takes the motor's D-shaft and drives the wheel web. The axle crossmember, square carriers and gussets are gone: they sat inside the motors and 11 mm into each wheel. Cheek plates carry the rails round the gearboxes, the deck has a relief over the motor cans, and the shell floor is slotted across the axle because the motors hang below it;
- the body sits 16 mm forward on the chassis ([`RP03-CAD-06`](../../decisions.md#rp03-cad-06--body-forward-on-the-chassis-and-a-low-battery-tub)). Shell, panels, body frame, electronics, audio, harness, yaw stage and head all move; the wheels, ball, chassis and keel do not. The battery drops into a chassis tub under the deck, flush with the deck top, with a bottom hatch. The register CoM moves from x +9.4 / h 106.7 to **x +20.2 / h 103.7 mm** (a_tip 0.86 → 1.91 m/s², ball share 0.09 → 0.18). The +25 / 124 baseline target is still missed;
- enlarged front and rear shell openings are the octagonal service-panel outlines offset inward by a constant 2 mm land; each panel's straight side edges are parallel to the corresponding shell edges (measured from the solids, not the constants); a separate internal frame behind each shell end wall carries four fused M3 bosses, with M3 × 8 screws seated on the panel face;
- the front panel starts at Z = 58 mm, above the chassis deck, so it lifts off forward over the ball pod. The deck, rails and front crossmember now stop inside the shell's front wall; only the pod's tongue passes the lower front band, through one open-bottom centre notch. The rear panel keeps its Z = 42 mm lower edge;
- the front slat motif is now a functional open speaker grille over a provisional 50 mm basket/44 mm cone, amplifier envelope and acoustic cavity;
- four body-mounted PDM microphone boards, acoustic ports and shell penetrations are allocated; exact audio SKUs remain an RP-05/RP-06 selection gate;
- the front range sensor sits on the centreline in the ball pod, its face at X = 128 mm (18 mm ahead of the ball contact) and Z = 41 mm, and looks through a window in the touch cap; the front panel no longer carries a sensor window; and
- the head now uses RP-01 Layout 04 at a 49.5 mm neck (was 60), with the spindle replaced by a turntable. Its yaw disc stands 15 mm proud of the body top with a 1 mm running gap. Full roll/pitch motion is kept out to hard stops 3° beyond usable travel, and the stops alone keep the head at least 4.2 mm off the disc. A Ø67 adapter plate spans the lowered upper-frame cross-members (the head load posts are removed) and carries a thin-section bearing and a clock-spring cable reserve. An off-axis XC330-M181 yaw servo on +Y drives the disc through a 1:1 spur pair (pitch Ø37) via a coupling shaft. Everything starts 10.5 mm above the Pi 5 cooler. A Ø90 shell opening passes the stack. The earlier cowl and yaw-moving shrouds are removed.

Per CAD-context decision [`RP03-CAD-01`](../../decisions.md#rp03-cad-01--rear-only-ground-reflectance-channel), the layout now uses one guarded rear TCRT5000 channel. Its optical patch is 27 mm behind the skid contact, its optical face is modeled 10 mm above ground, and its protective rails begin at 7 mm. The connected skid pad begins at 3.5 mm, so it contacts first. The front and lateral TCRT packages, mounts and cable reserves are removed.

Per CAD-context decision [`RP03-CAD-02`](../../decisions.md#rp03-cad-02--lean-fixed-ball-nose-with-concealed-contact), the non-functional stance-wide bumper and outboard switches are removed. [`RP03-CAD-04`](../../decisions.md#rp03-cad-04--lean-ball-pod-with-centred-range-sensor) then replaced that nose's rails, collar, keepers, shroud and fascia with one printed pod: the vendor flange seats on it at Z = 29 mm, three M3 screws clamp the flange from inside its pocket, and two M3 screws tie it to heat-set inserts in the front crossmember. The pod carries the centred GP2Y under a lid. Pod, lid and cap share an eight-sided section that echoes the body's end profile, and the pod (X 92–128.5, 36.5 mm long, exactly the flange footprint plus the sensor) bolts to a crossmember directly behind the flange at X 80–92, inside the shell, so no full-width bar shows ahead of the body. The battery tub has its own 1.5 mm front wall. A 40 mm octagonal touch hood (translucent, alpha 0.45) on compliant arms covers the pod front from the pod seat (Z 29) up, and travels 3 mm onto a lid-mounted tact switch. The nose is 40 mm wide (was 52 mm) and its spin radius grows from 128 to 134.8 mm. These are CAD-first choices pending permanent propagation, not project-wide safety approval.

Per CAD-context decision [`RP03-CAD-03`](../../decisions.md#rp03-cad-03--faceted-rear-tail-and-sensor-cartridge), the rear skid and TCRT sit in one separately selectable rear module, now split by function. A compact faceted keel bolts under the rear crossmember with four M3 screws and carries the replaceable 3.5 mm-clearance 12 × 10 mm wear shoe at X = −27 mm, the replaceable 7 mm-clearance guard lips and the TCRT cartridge at X = −54 mm (both 16 mm forward of their Layout 02.0 positions, with the body's rear wall, under `RP03-CAD-06`). The keel is translucent ivory (alpha 0.34) so the cartridge, cable riser and screws inside stay visible. The cosmetic tail is currently **parked**: `REAR_TAIL_ENABLED = False` keeps its geometry defined and checked but excludes it from the assembly, mass register and rear-panel bores. When enabled it is a short hard-surface stinger with a slate root hub, three telescoping eight-sided ivory segments that repeat the body end profile and sweep progressively upward (23° → 37° → 52°), and a blunt amber chisel tip. Four M3 screws are driven from inside the rear service panel into heat-set inserts in the hub, so no fasteners show. The tail stays inside the spin-in-place circle already set by the ball nose (105.9 vs 134.8 mm planar radius) and below the body top.

## Files

- `body-chassis.step.py` — buildable STEP entry.
- `body_chassis_model.py` — parametric assembly source and mass/frame data.
- `body-chassis.params.js` — viewer controls for shell, head yaw, electronics, harness, and physics.
- `write_outputs.py` — generated dimensions, frames, and mass/CoM reports.
- `check_layout.py` — deterministic parameter/interface checks.
- `../layout-01/references/purchased/` — shared vendor STEP, kept local (not in Git). Hashes in the Layout 01 README.
- `generated/` — machine-readable and Markdown outputs.
- `snapshots/` — required visual-review packet.

The RP-01 head is a live source dependency. Changes in head Layout 04 flow into this assembly on regeneration; its yaw datum, A0, yaw-carried mass/CoM and turntable size are read from that layout's `axes.json`, `mass-placement.json` and `motion-envelope.json`.

The neutral dimensional stack is 293.5 mm: 140 mm body/yaw datum + 49.5 mm neck + 104 mm crown-inclusive head. The yaw stage parts are packaging envelopes, not selected or load-rated parts. The body's vertical head-harness volume still passes through the compute-tray and Pi-cooler envelopes; its route is unresolved. The battery no longer sits in that path since it moved to the chassis tub.

## Generation

The model uses the cadgen 0.4 `gen_step()` contract. The venv cadgen 0.5.1 cannot build it; use the text-to-cad 0.4.28 runtime. Run from the repository root:

```text
PY=~/.codex/runtimes/text-to-cad/0.4.28/venv/bin/python
S=~/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts
$PY $S/gen docs/02-prototypes/RP-06-cad/body-chassis/layout-02/body-chassis.step.py --write
$PY $S/snapshot --job docs/02-prototypes/RP-06-cad/body-chassis/layout-02/snapshots/snapshot-job.json
```

Then run `write_outputs.py` and `check_layout.py` from inside this folder with the same `$PY`. The snapshot job writes timestamped files only; copy the newest set over the un-suffixed PNGs, or reviews show the previous model.

The selected TCRT5000 breakout/comparator PCB and connector are still unresolved. The yellow body inside the translucent rear module therefore remains a package envelope and its cyan connector/strain-relief solids are reserved volumes. Layout 02 makes no dedicated forward or lateral cliff-protection claim; its provisional level-floor operating restrictions are recorded in the CAD decision register.

## Validation note

All Layout 02-authored mounts, fascia, panels, panel hardware, audio packaging,
yaw stage, body, chassis, fixed ball-transfer, rear stinger tail, skid keel and rear
sensor geometry validates as closed, positive-volume BREP. Full-assembly
validation still reports five
inherited self-intersecting occurrences inside the frozen Raspberry Pi 5 vendor
STEP. None is part of this Layout 02 revision; the exact SKU is retained
rather than replaced with a cosmetic placeholder.

`check_layout.py` also measures the service panels from the built solids: the
2 mm land, side-edge parallelism, fastener inset, single-solid frames, the
front panel's forward lift-off path, and zero interference
between panel-area parts and the shell, chassis, body frame, electronics,
audio and sensors. That sweep does not cover the composed head: the RP-01
head's `physical_*` layers currently overlap the body shell and rear panel,
which is a head-composition issue outside the panel work.

The ball nose is measured the same way: the flange seats on the pod with zero
gap and zero overlap, the vendor stack is connected, each ball screw has 3 mm
of thread in the flange, no nose solid interferes with another, the cap's 3 mm
travel volume is empty except for the switch plunger, the cap stops at the pod
seat, a 20 mm floor-level cube (RP-03 `C12`) swept straight in is recorded as
meeting the ball's retaining lip first (not claimed for contact), the GP2Y beam is
clear, and its required look-ahead fits the 300 mm rated range at every
`physics.md` §6/§10 case, including when charged to the nose front.

The drivetrain is measured the same way (`RP03-CAD-05`). Each wheel is
axisymmetric, so its solids are its swept volume, and every stationary solid
(chassis, shell, panels, body frame, electronics, motor) keeps at least 1.5 mm
to them. The tightest gaps are the stub shaft to the gearbox face (1.5 mm), the
boss end to the pocket floor and the tyre to the arch trim (2 mm each), and
the boss to the pocket wall (3 mm). The motor envelopes do not interfere with the
chassis, shell, body frame, electronics or harness volumes. Each gearbox face seats on its
flange with zero gap. The 608 pairs lie inside the bosses, and the battery envelope
clears everything around the tub. Three CoM checks read the hand-kept mass register, not the geometry:
x ≥ +20 mm (the `physics.md` §2.5 margin line; currently +20.21, so borderline), ball share ≥ 0.09, and skid
contact before the CoM crosses the axle.

An all-group clash sweep on 2026-09-24 left these older body-side
overlaps, which no check covers yet: harness volumes against the
Pi cooler, compute tray, IMU and lower front cross; the rear lower cross and
rear dog-legs against the power and safety envelopes; the compute tray against
the speaker magnet; the yaw adapter plate and upper rails against the shell;
the PDM port boots against the shell; and the wheel-arch pods fused into the
shell. They are listed in [`openitems.md`](../../../openitems.md).
