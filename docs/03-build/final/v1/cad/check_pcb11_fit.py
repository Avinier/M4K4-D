"""PCB-11 stage-1 fit: place the KiCad board STEP in the D-065 crown socket and measure it.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds the head parts only (about 1.5 min). Head frame R at the neutral pose.

KiCad's STEP has the board core at Z 0..0.71 (copper not modelled), Y flipped, and the
outline at KiCad x 100..105, y 100..105 (04-pcbs/pcb-11-status-led/README.md). Board-local
u = x - 100 = world Y - 12.7 and v = 105 - y = world Z - 89.3, so STEP X -> Y - 87.3,
STEP Y -> Z + 194.3 and STEP Z -> X, with the front copper (core top + 0.035) on the
socket shoulder at X -7.2.
"""

import importlib.util
from pathlib import Path

from build123d import Compound, Location, Plane, import_step

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("check_pcb11_socket", HERE / "check_pcb11_socket.py")
sock = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sock)
m, S = sock.m, sock.S

BOARD_STEP = HERE.parents[2] / "04-pcbs/pcb-11-status-led/cad/pcb-11-status-led-revA.step"
CORE, COPPER, SOLDER = 0.71, 0.035, 0.05
SHOULDER_X = S["board"][1]                   # -7.2: the pocket's front face
X0 = SHOULDER_X - COPPER - CORE              # core bottom in head frame R
PLACE = Location(Plane(origin=(X0, -87.3, 194.3), x_dir=(0, 1, 0), z_dir=(1, 0, 0)))
LIP_X = S["lip"][1]                          # -5.4: back face of the pipe stop
LED_MAX, PASSIVE_MAX = 0.99, 0.55            # V6 0.84 + 0.15; 0402 C/R maximum height
MIN_GAP = 0.3


def _vol(shape):
    return shape.volume if shape else 0.0


def main():
    parts = m.build_parts(catalog=True, reliefs=False)
    shapes = {n: d["shape"] for n, d in parts.items() if d["kind"] == "physical"}
    bezel = sock._bezel_after(shapes[sock.BEZEL])
    pipe = shapes["crown_status_light_diffuser"]
    others = {n: s for n, s in shapes.items() if n not in sock.OWN}

    board = {}
    for child in import_step(str(BOARD_STEP)).children:
        name = "PCB" if child.label.endswith("_PCB") else child.label
        board.setdefault(name, []).append(Compound(child.solids()).moved(PLACE))

    out = []
    pcb = board["PCB"][0]
    bb = pcb.bounding_box()
    centred = abs((bb.min.Y + bb.max.Y) / 2 - m.LED_Y) < 1e-3 and abs((bb.min.Z + bb.max.Z) / 2 - m.LED_Z) < 1e-3
    walls = bezel & m.block(bb.min.X, bb.max.X - 0.05, bb.min.Y - 1, bb.max.Y + 1, bb.min.Z - 1, bb.max.Z + 1)
    out.append(("board in pocket", centred and _vol(pcb & bezel) < 1e-6 and abs(pcb.distance(walls) - 0.1) < 0.005,
                f"core X {bb.min.X:.3f}..{bb.max.X:.3f}, Y {bb.min.Y:.2f}..{bb.max.Y:.2f}, Z {bb.min.Z:.2f}..{bb.max.Z:.2f}; "
                f"clash {_vol(pcb & bezel):.4f} mm3; edge to wall {pcb.distance(walls):.3f}; core to shoulder {SHOULDER_X - bb.max.X:.3f} (copper and mask)"))

    led = Compound([s for s in board["LED_WS2812B-2020-V6"]])
    lb = led.bounding_box()
    led_centre = ((lb.min.Y + lb.max.Y) / 2 - m.LED_Y, (lb.min.Z + lb.max.Z) / 2 - m.LED_Z)
    real_top = SHOULDER_X + SOLDER + LED_MAX
    out.append(("LED on the pipe axis, clear of the lip", _vol(led & bezel) < 1e-6 and max(map(abs, led_centre)) < 0.01
                and LIP_X - real_top > 0.3,
                f"LED centre off axis by ({led_centre[0]:+.3f}, {led_centre[1]:+.3f}); model top X {lb.max.X:.3f}, "
                f"{LIP_X - lb.max.X:.2f} to the lip; real maximum {real_top:.2f}, {LIP_X - real_top:.2f} to the lip; "
                f"{pipe.bounding_box().min.X - lb.max.X:.2f} to the pipe"))

    back = []
    for name in ("C_0402_1005Metric", "R_0402_1005Metric"):
        for s in board[name]:
            b = s.bounding_box()
            near = min((s.distance(o), n) for n, o in others.items())
            back.append((name[0], b.min.X, b.min.Y, near))
    real_back = SHOULDER_X - COPPER - CORE - COPPER - SOLDER - PASSIVE_MAX
    worst = min(b[3][0] for b in back)
    out.append(("back parts clear", worst >= MIN_GAP and all(b[2] >= 15.0 for b in back),
                "; ".join(f"{n}: X {x:.2f}, Y from {y:.2f} (bracket lip ends at Y 15.0), nearest {d[1]} {d[0]:.2f}"
                          for n, x, y, d in back) + f"; real 0402 back face X {real_back:.2f}"))

    allb = Compound([s for v in board.values() for s in v])
    near = sorted((allb.distance(o), n) for n, o in others.items())[:3]
    out.append(("board clear of every other head part", near[0][0] >= MIN_GAP,
                "; ".join(f"{n} {d:.2f}" for d, n in near)))

    ok = True
    for name, passed, detail in out:
        ok &= bool(passed)
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
