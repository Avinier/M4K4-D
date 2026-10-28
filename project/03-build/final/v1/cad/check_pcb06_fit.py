"""PCB-06 stage-1 fit: place the KiCad board STEP on all four shell bosses and measure it.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the body parts only and sweeps (about 8 min, mostly distance queries) the shell's lowering path; the
final/v1 droid edits (DROID_CUTS/ADDS/MOVES) do not touch the body near the mics.

KiCad's STEP has (X, Y) = (KiCad x, -y), the board core at Z 0..0.91 (copper not
modelled; 35 um copper and 10 um mask each side make it 1.0 mm), and parts 0.04 mm above
the front mask. Board-local u = x - 106 runs toward the body centre (the lead side),
v = 107 - y, and n = Z - 0.955 runs inboard from the front (inner) face, so the outer
face lands on the boss seat at |Y| 71.3 (04-pcbs/pcb-06-pdm-mic/README.md). One plane per
position puts u toward the centre and n inboard; v then points down on FRONT_L and
REAR_R, which mount turned over (D-066 Inputs, "one design, four positions").
"""

import sys
from pathlib import Path

from build123d import Box, Compound, Location, Plane, Vector, import_step

import body_v1_model as M

HERE = Path(__file__).resolve().parent
BOARD_STEP = HERE.parents[2] / "04-pcbs/pcb-06-pdm-mic/cad/pcb-06-pdm-mic-revA.step"
PORT_KICAD = (106.0, 107.0)
INNER_FACE_Z = 0.955          # core 0.91 + copper 0.035 + mask 0.01
PART_OFFSET = 0.04            # STEP parts start 0.04 above the front mask
REAL_HEIGHT = {"IM73D122V01_PG-LLGA-5-3": 1.30,  # datasheet 1.2 +- 0.1
               "C_0402_1005Metric": 0.55, "R_0402_1005Metric": 0.55}
JOINT_HEIGHT = 1.0            # AWG28 lead and solder fillet on P1-P4 (the CAD lead reserve)
PADS = (3.6, 5.6, -3.75, 3.75)  # P1-P4 zone, board-local u, v
MIN_GAP = 0.3
SWEEP = 125.0


def leaves(shape):
    kids = getattr(shape, "children", None)
    return [leaf for kid in kids for leaf in leaves(kid)] if kids else [shape]


def vol(shape):
    return shape.volume if shape is not None and shape.solids() else 0.0


def bbox_hit(a, b, pad=0.0):
    """Box test with a margin. Never skips containment (BoundBox.overlaps() does)."""
    p, q = a.bounding_box(), b.bounding_box()
    return not (p.max.X + pad <= q.min.X or q.max.X + pad <= p.min.X or p.max.Y + pad <= q.min.Y or
                q.max.Y + pad <= p.min.Y or p.max.Z + pad <= q.min.Z or q.max.Z + pad <= p.min.Z)


class Frame:
    def __init__(self, x, y, z):
        self.x, self.z = x, z
        self.s = 1.0 if y > 0 else -1.0
        self.c = -1.0 if x > M.BODY_AXIS_X else 1.0
        self.inner = M.MIC_BOARD_OUTER_Y - M.MIC_BOARD_SIZE[1]
        plane = Plane(origin=(x, self.s * self.inner, z), x_dir=(self.c, 0, 0), z_dir=(0, -self.s, 0))
        self.vz = plane.y_dir.Z     # +1 upright, -1 turned over
        self.loc = Location(plane) * Location((-PORT_KICAD[0], PORT_KICAD[1], -INNER_FACE_Z))

    def n(self, world_y):
        return self.inner - self.s * world_y

    def box(self, u0, u1, v0, v1, n0, n1, dz=0.0):
        xs = sorted((self.x + self.c * u0, self.x + self.c * u1))
        zs = sorted((self.z + self.vz * v0, self.z + self.vz * v1))
        ys = sorted((self.s * (self.inner - n0), self.s * (self.inner - n1)))
        return Box(xs[1] - xs[0], ys[1] - ys[0], zs[1] - zs[0] + dz).moved(
            Location(((xs[0] + xs[1]) / 2, (ys[0] + ys[1]) / 2, (zs[0] + zs[1] + dz) / 2)))


def obstacle_n(F, column, fixed):
    """Smallest inboard depth n of any fixed part inside a world column, or None."""
    best = None
    for p in fixed:
        if not bbox_hit(p, column):
            continue
        c = p & column
        if vol(c) > 1e-6:
            bb = c.bounding_box()
            n = min(F.n(bb.min.Y), F.n(bb.max.Y))
            best = n if best is None else min(best, n)
    return best


def main():
    step = import_step(str(BOARD_STEP))
    parts = [(c.label, Compound(c.solids())) for c in step.children]
    assert sum(1 for l, _ in parts if l.endswith("_PCB")) == 1 and len(parts) == 7, [l for l, _ in parts]

    shell = M.body_shell()
    audio = M.body_audio()
    frame = leaves(M.body_primary_frame())
    chassis = leaves(M.chassis_v1_reference())
    electronics = leaves(M.electronics())
    pcb05 = [l for c in audio.children if c.label == "PCB05_AUDIO_FRONT_END" for l in leaves(c)]
    conns = leaves(M.connectors_and_exits())
    mic_hw = [l for c in audio.children if (c.label or "").startswith("PDM_MIC_") for l in leaves(c)
              if any(k in (l.label or "") for k in ("GASKET", "M2_SCREW"))]
    placeholders = {c.label: {l.label: l for l in leaves(c)} for c in audio.children if (c.label or "").startswith("PDM_MIC_")}
    others = [shell, *frame, *chassis, *electronics, *pcb05, *conns, *mic_hw,
              *leaves(M.sensors()), *leaves(M.harness_routes()), *leaves(M.body_panels()),
              *leaves(M.panel_mount_hardware()), *leaves(M.shell_frame_hardware()),
              *leaves(M.wheel_arch_hardware()), *leaves(M.body_yaw_stage()), *M.yaw_drive_moving_parts()]
    fixed = [*[p for p in chassis if not (p.label or "").startswith("ESTOP_XA1E_")], *frame,
             *[p for p in electronics if not (p.label or "").startswith(("ESTOP_XA1E_", "POWER_BUTTON_", "PCB13_"))],
             *pcb05, *[p for p in conns if (p.label or "").startswith("PCB05_")]]

    ok = True

    def report(name, passed, detail):
        nonlocal ok
        ok &= bool(passed)
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}", flush=True)

    for x, y, z, pos in M.MICROPHONE_PORTS:
        F = Frame(x, y, z)
        placed = [(l, s.moved(F.loc)) for l, s in parts]
        core = next(s for l, s in placed if l.endswith("_PCB"))
        comps = [(l, s) for l, s in placed if not l.endswith("_PCB")]
        ph = placeholders[f"PDM_MIC_{pos}"]
        print(f"--- {pos}: {'upright' if F.vz > 0 else 'turned over'}", flush=True)

        # 1. Same outline and place as the CAD placeholder; holes on the port axis and the pilots.
        cb, pb = core.bounding_box(), ph[f"PDM_MIC_{pos}_PCB06"].bounding_box()
        same = all(abs(a - b) < 0.01 for a, b in ((cb.min.X, pb.min.X), (cb.max.X, pb.max.X), (cb.min.Z, pb.min.Z), (cb.max.Z, pb.max.Z)))
        holes = {k: not core.solids()[0].is_inside(Vector(*p)) for k, p in (
            ("port", (x, F.s * (F.inner + 0.5), z)),
            ("H+5", (x, F.s * (F.inner + 0.5), z + 5.0)), ("H-5", (x, F.s * (F.inner + 0.5), z - 5.0)))}
        report("outline, sound hole and screw holes", same and all(holes.values()),
               f"core X {cb.min.X:.2f}..{cb.max.X:.2f}, Z {cb.min.Z:.2f}..{cb.max.Z:.2f} against the placeholder; holes open {holes}")

        # 2. Mic package where the CAD has it: its centre 0.68 from the port toward the post.
        mic = next(s for l, s in comps if l.startswith("IM73D122"))
        mb, cad = mic.bounding_box(), ph[f"PDM_MIC_{pos}_IM73D122"].bounding_box()
        d = (mb.center() - cad.center())
        report("MK1 on the port", abs(d.X) < 0.01 and abs(d.Z) < 0.01,
               f"package centre vs CAD package: dX {d.X:+.3f}, dZ {d.Z:+.3f}; model top n {F.n(mb.min.Y if F.s > 0 else mb.max.Y):.2f}")

        # 3. Seated: outer face on the boss (copper and mask, 0.045, fill the gap), no clash.
        gap = core.distance(shell)
        report("seated on the boss", vol(core & shell) < 1e-6 and abs(gap - 0.045) < 0.005,
               f"core to boss {gap:.3f} (copper + mask 0.045)")

        # 4. Static clearance of the real board to everything else.
        near = []
        for l, s in [("core", core), *comps]:
            cands = [o for o in others if bbox_hit(s, o, pad=3.0)]
            if cands:
                near.append(min((s.distance(o), l, o.label or "unnamed") for o in cands))
        clash = [(l, o) for d, l, o in near if d < 1e-6 and l != "core"]
        comp_min = min((d for d, l, o in near if l != "core"), default=99.0)
        report("parts clear of every body part", not clash and comp_min >= MIN_GAP,
               "; ".join(f"{l} {d:.2f} to {o}" for d, l, o in sorted(near)[:4]))

        # 5. Lowering path: each part's column, from installed to 125 mm up, against the fixed parts;
        #    clearance measured from the datasheet maximum height, not the KiCad model.
        rows = []
        for l, s in comps:
            b = s.bounding_box()
            us = sorted((F.c * (b.min.X - x), F.c * (b.max.X - x)))
            vs = sorted((F.vz * (b.min.Z - z), F.vz * (b.max.Z - z)))
            n_obst = obstacle_n(F, F.box(us[0], us[1], vs[0], vs[1], 0.0, 6.0, dz=SWEEP), fixed)
            top = PART_OFFSET + REAL_HEIGHT[l]
            rows.append((l, top, n_obst))
        u0, u1, v0, v1 = PADS
        pad_col = F.box(u0, u1, v0, v1, 0.0, 6.0, dz=SWEEP)
        rows.append(("P1-P4 joints", JOINT_HEIGHT, obstacle_n(F, pad_col, fixed)))
        worst = min((n - t, l) for l, t, n in rows if n is not None)
        report("lowering path, real heights", worst[0] >= MIN_GAP,
               "; ".join(f"{l} top {t:.2f} / obstacle {('none' if n is None else f'{n:.2f}')}" for l, t, n in rows)
               + f"; worst {worst[1]} {worst[0]:.2f}")

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
