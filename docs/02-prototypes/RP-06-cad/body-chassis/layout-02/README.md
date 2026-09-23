# RP-06 integrated body/chassis Layout 02

This is the active whole-body CAD path. It retains Layout 01's source-linked RP-01 head (now Layout 04), compact two-wheel chassis, connected rear skid, fixed ball-transfer nose, internal packaging and purposeful review layers, while closing the first-pass integration questions:

- four M4 through-bolts and two locating pins now define the body-frame-to-chassis interface;
- enlarged front and rear shell openings are the octagonal service-panel outlines offset inward by a constant 2 mm land; each panel's straight side edges are parallel to the corresponding shell edges (measured from the solids, not the constants); a separate internal frame behind each shell end wall carries four fused M3 bosses, with M3 × 8 screws seated on the panel face;
- the front panel starts at Z = 58 mm, above the chassis deck, so it lifts off forward over the front crossmember; the chassis rails pass the lower front band through open-bottom shell notches, and the deck now stops inside the shell's front wall. The rear panel keeps its Z = 42 mm lower edge;
- the front slat motif is now a functional open speaker grille over a provisional 50 mm basket/44 mm cone, amplifier envelope and acoustic cavity;
- four body-mounted PDM microphone boards, acoustic ports and shell penetrations are allocated; exact audio SKUs remain an RP-05/RP-06 selection gate;
- the front range sensor sits beside the battery at Y = +38 mm, Z = 68 mm, below the speaker grille, and looks through its own window in the front panel; and
- the head now uses RP-01 Layout 04 at a 40 mm neck (was 60), with the spindle replaced by a turntable. Its yaw turntable disc stands 9.5 mm proud of the body top with a 1 mm running gap. Full roll/pitch motion is kept, and the hard stops alone keep the head at least 4 mm off the disc. The body carries a thin-section bearing and a clock-spring cable reserve above a Ø69 adapter plate, a ring gear with a skirt up to the disc, an off-axis pinion and an XC330-size yaw servo on +Y. Everything starts 10.5 mm above the Pi 5 cooler. A Ø90 shell opening passes the gear skirt. The earlier cowl and yaw-moving shrouds are removed.

Per CAD-context decision [`RP03-CAD-01`](../../decisions.md#rp03-cad-01--rear-only-ground-reflectance-channel), the layout now uses one guarded rear TCRT5000 channel. Its optical patch is 27 mm behind the skid contact, its optical face is modeled 10 mm above ground, and its protective rails begin at 7 mm. The connected skid pad begins at 3.5 mm, so it contacts first. The front and lateral TCRT packages, mounts and cable reserves are removed.

Per CAD-context decision [`RP03-CAD-02`](../../decisions.md#rp03-cad-02--lean-fixed-ball-nose-with-concealed-contact), the non-functional stance-wide bumper and outboard switches are removed. The frozen ball datum is retained in a narrower load-bearing collar, paired flange keepers and compact shroud, with a 42 mm concealed-contact fascia and 3 mm travel reserve. These are CAD-first choices pending permanent propagation, not project-wide safety approval.

Per CAD-context decision [`RP03-CAD-03`](../../decisions.md#rp03-cad-03--faceted-rear-tail-and-sensor-cartridge), the rear skid and TCRT sit in one separately selectable rear module, now split by function. A compact faceted keel bolts under the rear crossmember with four M3 screws and carries the replaceable 3.5 mm-clearance 12 × 10 mm wear shoe at X = −43 mm, the replaceable 7 mm-clearance guard lips and the TCRT cartridge at X = −70 mm. The keel is translucent ivory (alpha 0.34) so the cartridge, cable riser and screws inside stay visible. The cosmetic tail is currently **parked**: `REAR_TAIL_ENABLED = False` keeps its geometry defined and checked but excludes it from the assembly, mass register and rear-panel bores. When enabled it is a short hard-surface stinger with a slate root hub, three telescoping eight-sided ivory segments that repeat the body end profile and sweep progressively upward (23° → 37° → 52°), and a blunt amber chisel tip. Four M3 screws are driven from inside the rear service panel into heat-set inserts in the hub, so no fasteners show. The tail stays inside the spin-in-place circle already set by the ball nose (121.9 vs 128 mm planar radius) and below the body top.

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

The neutral dimensional stack is 284 mm: 140 mm body/yaw datum + 40 mm neck + 104 mm crown-inclusive head. The yaw stage parts are packaging envelopes, not selected or load-rated parts. The body's vertical head-harness volume still passes through the battery, compute-tray and Pi-cooler envelopes, as it did before this change; its route is unresolved.

## Generation

Run from the repository root using the CAD environment carried by [`base/pass-01/`](../../base/pass-01/):

```text
docs/02-prototypes/RP-06-cad/base/pass-01/.venv/bin/python \
  <text-to-cad>/skills/cad/scripts/gen \
  docs/02-prototypes/RP-06-cad/body-chassis/layout-02/body-chassis.step.py \
  --write
```

Then run `write_outputs.py`, `check_layout.py`, CAD inspection, validation, and the snapshot job.

The selected TCRT5000 breakout/comparator PCB and connector are still unresolved. The yellow body inside the translucent rear module therefore remains a package envelope and its cyan connector/strain-relief solids are reserved volumes. Layout 02 makes no dedicated forward or lateral cliff-protection claim; its provisional level-floor operating restrictions are recorded in the CAD decision register.

## Validation note

All Layout 02-authored mounts, fascia, panels, panel hardware, audio packaging,
yaw stage, body, chassis, fixed ball-transfer, rear stinger tail, skid keel and rear
sensor geometry validates as closed, positive-volume BREP. Full-assembly
validation still reports five
inherited self-intersecting occurrences inside the frozen Raspberry Pi 5 vendor
STEP. None is part of this Layout 02 revision; the exact SKU is retained
rather than replaced with a cosmetic placeholder.
