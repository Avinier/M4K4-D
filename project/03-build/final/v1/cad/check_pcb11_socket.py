"""D-065: measure the PCB-11 LED socket that DROID_ADDS fuses into the bezel's crown.

Run from this folder with the legacy runtime and the PYTHONPATH in ../README.md.
Builds only the head parts (about 1 min), not the whole droid. Head frame R at the
neutral pose; reliefs off (they only cut the skin, ears and cradle, so clearances to
those are conservative).
"""

import importlib.util
from pathlib import Path

from build123d import Compound, Location, Vector

spec = importlib.util.spec_from_file_location("makad_v1_entry", Path(__file__).resolve().with_name("makad-v1.step.py"))
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)
m = entry.layout_model

S = entry.PCB11_SOCKET
BEZEL = "front_bezel_integral_camera_crown"
OWN = ("status_LED_PCB08_carrier_5x5", "status_LED_WS2812B_2020", "crown_status_light_diffuser", BEZEL)
LATER = ("removable_camera_edge_bracket_trial", "camera_module_3_wide_1to1")  # fitted after the board
MIN_GAP = 0.3       # socket to any other part
LED_MAX = 0.99      # WS2812B-2020-V6 height 0.84 + 0.15 tolerance
PASSIVE_MAX = 0.55  # 0402 C or R, maximum height
WIRE_ZONE = (-34.0, -8.0, 15.0, 17.7, 89.3, 94.3)  # back right half of the board, out to the skin


def _vol(shape):
    return shape.volume if shape else 0.0


def _leaves(node, loc=Location()):
    here = loc * node.location
    kids = list(node.children) if getattr(node, "children", None) else []
    if not kids:
        yield node, loc
    for kid in kids:
        yield from _leaves(kid, here)


def _bezel_after(old):
    """Run the real DROID_ADDS pass on the bezel placed as in the droid; return it in head frame R."""
    head = Compound(label="Head v1", children=[Compound(label="Shell and covers", children=[old.moved(Location())])])
    tree = entry._apply_droid_cuts(Compound(children=[head.moved(Location(entry.HEAD_ORIGIN_IN_CHASSIS))]), strict=False)
    found = [(n, l) for n, l in _leaves(tree) if n.label == BEZEL]
    assert len(found) == 1, len(found)
    node, loc = found[0]
    return node.moved(loc).moved(Location(tuple(-v for v in entry.HEAD_ORIGIN_IN_CHASSIS)))


def main():
    parts = m.build_parts(catalog=True, reliefs=False)
    shapes = {n: d["shape"] for n, d in parts.items() if d["kind"] == "physical"}
    old = shapes[BEZEL]
    bezel = _bezel_after(old)
    socket = entry.pcb11_socket_local()
    out = []

    # 1. Fused: the bezel gains exactly the socket less what it already had, as one solid.
    gained = bezel.volume - old.volume
    expected = socket.volume - _vol(socket & old)
    solids = len(bezel.solids())
    out.append(("fused", abs(gained - expected) < 0.01 and solids == len(old.solids()),
                f"bezel +{gained:.2f} mm3 (socket {socket.volume:.2f}, new {expected:.2f}); solids {len(old.solids())} -> {solids}"))
    crown = entry.extrude(entry.Plane.YZ * entry.Polygon(*m.CROWN_OUTER, align=None), amount=24).moved(Location((-24, 0, 0)))
    out.append(("inside crown skin", _vol(socket - crown) < 1e-6, f"socket outside the crown's outer surface {_vol(socket - crown):.4f} mm3"))

    # 2. Board in the pocket: 0.1 mm side gaps, front face on the shoulder all round.
    board = m.block(*S["board"])
    x0, x1, y0, y1, z0, z1 = S["board"]
    ring = [(y, z) for y in (y0 + 0.25, (y0 + y1) / 2, y1 - 0.25) for z in (z0 + 0.25, z1 - 0.25)]
    ring += [(y0 + 0.25, (z0 + z1) / 2), (y1 - 0.25, (z0 + z1) / 2)]
    shoulder = [bezel.is_inside(Vector(x1 + 0.05, y, z)) for y, z in ring]
    walls = bezel & m.block(x0, x1 - 0.05, y0 - 1, y1 + 1, z0 - 1, z1 + 1)
    side_gap = board.distance(walls)
    sides = [bezel.is_inside(Vector(x0 + 0.4, y, z)) for y, z in ((y0 - 0.4, m.LED_Z), (y1 + 0.4, m.LED_Z), (m.LED_Y, z0 - 0.4), (m.LED_Y, z1 + 0.4))]
    out.append(("board seated", _vol(board & bezel) < 1e-6 and all(shoulder) and all(sides) and abs(side_gap - 0.1) < 0.005,
                f"overlap {_vol(board & bezel):.4f} mm3; shoulder {sum(shoulder)}/{len(shoulder)} points; "
                f"walls on 4 sides {sum(sides)}/4; edge to wall {side_gap:.3f} mm"))

    # 3. Front-part space: nothing of the bezel within the cavity, and room for the parts.
    cx0, cx1, cy0, cy1, cz0, cz1 = S["cavity"]
    led_top = x1 + LED_MAX
    lip_back = S["lip"][1]
    led = m.block(x1, led_top, 14.2, 16.2, 90.8, 92.8)
    passives = m.block(x1, x1 + PASSIVE_MAX, cy0 + 0.05, cy1 - 0.05, cz0 + 0.05, cz1 - 0.05)
    out.append(("front parts room", _vol(led & bezel) < 1e-6 and _vol(passives & bezel) < 1e-6,
                f"LED top (max) X {led_top:.2f}, {lip_back - led_top:.2f} mm to the lip; parts area u,v 0.5-4.5 free"))

    # 4. Light pipe: in the bore over its whole length, resting on the lip.
    pipe = shapes["crown_status_light_diffuser"]
    pb = pipe.bounding_box()
    seat = abs(pb.min.X - S["lip"][2]) < 1e-6 and _vol(pipe & bezel) < 1e-6
    radial = min(pipe.distance(bezel - m.block(pb.min.X - 1, pb.min.X + 0.01, 0, 40, 70, 110)), 9)
    bore_wall = [bezel.is_inside(Vector(x, m.LED_Y + S["bore"][0] + 0.2, m.LED_Z)) for x in (-4.9, -3.5, -2.2)]
    window = not bezel.is_inside(Vector(-5.2, m.LED_Y + 1.0, m.LED_Z))
    out.append(("light pipe held", seat and all(bore_wall) and window and 0.09 < radial < 0.11,
                f"pipe X {pb.min.X:.2f}..{pb.max.X:.2f} on lip at {S['lip'][2]}; radial gap {radial:.3f}; bore wall {sum(bore_wall)}/3; window open {window}"))

    # 5. Clearance to every other physical part.
    near = []
    for n, s in shapes.items():
        if n in OWN:
            continue
        bb = s.bounding_box()
        if bb.max.X < -12 or bb.min.X > 0 or bb.max.Y < 8 or bb.min.Y > 23 or bb.max.Z < 84 or bb.min.Z > 100:
            continue
        near.append((socket.distance(s), n))
    near.sort()
    worst = near[0] if near else (99, "-")
    out.append(("socket clear of other parts", worst[0] >= MIN_GAP,
                "; ".join(f"{n} {d:.2f}" for d, n in near[:4])))

    # 6. Wire exit behind the back's right half, and the board's way in from behind.
    zone = m.block(*WIRE_ZONE)
    hits = [(n, round(_vol(zone & s), 3)) for n, s in shapes.items() if n not in OWN and _vol(zone & s) > 1e-4]
    out.append(("wire zone open", not hits, f"X {WIRE_ZONE[0]}..{WIRE_ZONE[1]}, Y {WIRE_ZONE[2]}-{WIRE_ZONE[3]}: {hits or 'clear'}"))
    path = m.block(-30.0, S["pocket"][0], *S["pocket"][2:])
    blockers = [(n, round(_vol(path & s), 2)) for n, s in shapes.items() if n not in OWN and _vol(path & s) > 1e-4]
    early = [b for b in blockers if b[0] not in LATER]
    out.append(("board goes in from behind", not early,
                f"blocked only by parts fitted after it: {[b[0] for b in blockers] or 'none'}"))

    ok = True
    for name, passed, detail in out:
        ok &= bool(passed)
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
