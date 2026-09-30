"""Service-access sweeps for the ball-transfer nose (J07/J08, D-011), body installed.

Moves each serviceable part along its removal path in 1 mm steps through the whole
assembly and records the first solid it would hit. Also checks the tool paths and the
J10-8 cable route reserves. Writes generated/nose-service.json and .md. The full run
takes about an hour; pass a comma-separated list of sweep names to run only those.
Run with the text-to-cad 0.4.28 runtime from this folder:

    python check_nose_service.py [sensor_up,lid_forward,...]

The RP-01 head is replaced by far-away stubs: every swept tool stays below Z 130,
under the yaw stage, so the head cannot be hit.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from build123d import Align, Box, Compound, Cylinder, Location

import body_chassis_model as M

HERE = Path(__file__).resolve().parent
REGION = (30.0, 175.0, -75.0, 75.0, -80.0, 130.0)
IGNORE = ("PHYSICS_OVERLAYS", "AXES_", "OPTICAL_AXIS", "TRAVEL_RESERVE", "RETURN_SPRING")  # springs compress


def _stub_head():
    def stub(name):
        return Compound(label=name, children=[Box(1, 1, 1).moved(Location((0, 0, 1000)))])
    return stub("RP01_HEAD_LAYOUT03"), stub("RP01_HEAD_HARNESS"), stub("RP01_HEAD_PHYSICS")


def _leaves(node, path=()):
    kids = list(getattr(node, "children", []) or [])
    here = (*path, node.label or "")
    if kids:
        return [leaf for kid in kids for leaf in _leaves(kid, here)]
    return [("/".join(p for p in here if p), solid) for solid in node.solids()]


def _meets(a, b):
    A, B = a.bounding_box(), b.bounding_box()
    return A.min.X < B.max.X and A.max.X > B.min.X and A.min.Y < B.max.Y and A.max.Y > B.min.Y and A.min.Z < B.max.Z and A.max.Z > B.min.Z


def _vol(shape):
    return 0.0 if shape is None else shape.volume


def main():
    M.rp01_head_groups = _stub_head
    assembly = M.build_assembly()
    near = []
    for label, solid in _leaves(assembly):
        b = solid.bounding_box()
        if any(k in label for k in IGNORE):
            continue
        if b.max.X > REGION[0] and b.min.X < REGION[1] and b.max.Y > REGION[2] and b.min.Y < REGION[3] and b.max.Z > REGION[4] and b.min.Z < REGION[5]:
            near.append((label, solid))

    def clashes(tool, exclude=()):
        out = {}
        for label, solid in near:
            if any(e in label for e in exclude) or not _meets(tool, solid):
                continue
            v = _vol(tool & solid)
            if v > 1e-3:
                out[label.split("/")[-1]] = round(v, 2)
        return out

    def sweep(pick, vector, distance, removed=(), shape_fn=None):
        moving = [s for label, s in near if pick(label)]
        names = sorted({label.split("/")[-1] for label, _ in near if pick(label)})
        if shape_fn:
            moving = [shape_fn(s) for s in moving]
        first = {}
        for step in range(1, int(distance) + 1):
            for s in moving:
                mv = s.moved(Location(tuple(v * step for v in vector)))
                for label, v in clashes(mv, exclude=tuple(removed) + tuple(names)).items():
                    first.setdefault(label, {"at_mm": step, "mm3": v})
        return {"moving": names, "removed_first": list(removed), "vector": vector, "distance_mm": distance, "first_hits": first}

    def zcyl(r, z0, z1, x, y):
        return Cylinder(r, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, z0)))

    caster_moving = ("BALL_TRANSFER_POM_BALL", "BALL_TRANSFER_PURCHASED_HOUSING", "BALL_TRANSFER_ROLLER")
    hook_zone = M._block(M.TACTILE_SNAP_HOOK_X[0] - 0.01, M.TACTILE_SNAP_HOOK_X[2] + 0.01, -30.0, 30.0, *M.TACTILE_SNAP_HOOK_Z)
    only = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else None
    paths = {
        # Caster swap from below, nothing else removed: unsnap housing, ball and rollers; unscrew; drop the base.
        "caster_housing_ball_down": lambda: sweep(lambda l: any(k in l for k in caster_moving), (0.0, 0.0, -1.0), 40),
        "caster_screws_down": lambda: sweep(lambda l: "BALL_M3_" in l, (0.0, 0.0, -1.0), 40, removed=(*caster_moving, "BALL_SEAT_HEATSET_INSERT")),  # leaving their own threads
        "caster_base_down": lambda: sweep(lambda l: "BALL_TRANSFER_PURCHASED_3HOLE_FLANGE" in l, (0.0, 0.0, -1.0), 40, removed=(*caster_moving, "BALL_M3_")),
        # Cap: fingers spread (hooks out of their slots), slide forward.
        "cap_forward_fingers_spread": lambda: sweep(lambda l: l.endswith("BALL_NOSE_TOUCH_CAP"), (1.0, 0.0, 0.0), 20, shape_fn=lambda s: s - hook_zone),
        # Lid: cap off, front screw out; slide forward from under the shell band, then lift.
        "lid_forward": lambda: sweep(lambda l: l.endswith("BALL_POD_SENSOR_LID"), (1.0, 0.0, 0.0), 12, removed=("BALL_NOSE_TOUCH_CAP", "BALL_POD_LID_M2X8")),
        "lid_up_after_11mm_forward": lambda: sweep(lambda l: l.endswith("BALL_POD_SENSOR_LID"), (0.0, 0.0, 1.0), 40, removed=("BALL_NOSE_TOUCH_CAP", "BALL_POD_LID_M2X8"),
                                           shape_fn=lambda s: s.moved(Location((11.0, 0.0, 0.0)))),
        "lid_up_in_place": lambda: sweep(lambda l: l.endswith("BALL_POD_SENSOR_LID"), (0.0, 0.0, 1.0), 4, removed=("BALL_NOSE_TOUCH_CAP", "BALL_POD_LID_M2X8")),
        # Sensor and switch: lid and cap off, lift out.
        "sensor_up": lambda: sweep(lambda l: "GP2Y0A21YK0F_STEP" in l or "GP2Y_J10_8_SOLDERED_LEAD_RESERVE" in l, (0.0, 0.0, 1.0), 40,
                           removed=("BALL_NOSE_TOUCH_CAP", "BALL_POD_SENSOR_LID", "BALL_POD_LID_M2X8")),
        # D-027: the real GP2Y body stands over the Hall slot, so the sensor comes out first.
        "hall_board_up": lambda: sweep(lambda l: any(k in l for k in ("HALL_CARRIER_PCB", "HALL_DRV5055")), (0.0, 0.0, 1.0), 40,
                               removed=("BALL_NOSE_TOUCH_CAP", "BALL_POD_SENSOR_LID", "BALL_POD_LID_M2X8", "GP2Y0A21YK0F_STEP", "GP2Y_J10_8_SOLDERED_LEAD_RESERVE")),
    }
    results = {k: run() for k, run in paths.items() if not only or k in only}
    # Tool paths. 2 mm hex key (O2.3 over corners) up into each caster screw from below with the
    # housing and ball out; T6/PH0 bit (O3) down onto the lid screw with the cap off.
    tools = {}
    for i, (x, y) in enumerate(M.ball_screw_points(), start=1):
        head_bottom = M.BALL_POD_Z0 - M.BALL_FLANGE_WEB - M.AXLE_BUTTON_HEAD[1]
        tools[f"caster_screw_{i}_hex_key_from_below"] = clashes(zcyl(1.15, -60.0, head_bottom - 0.05, x, y), exclude=(*caster_moving, "BALL_M3_"))
    lx, ly = M.LID_SCREW_XY
    tools["lid_screw_driver_from_above"] = clashes(zcyl(1.5, M.BALL_POD_STATIONS[-1][2] + 0.05, 128.0, lx, ly), exclude=("BALL_NOSE_TOUCH_CAP",))
    # J10-8 route reserves against every real solid (reserves and keep-outs are skipped).
    route = [(l, s) for l, s in near if "HARNESS_NOSE_J10_8" in l]
    route_hits = {}
    for label, s in route:
        hits = {k: v for k, v in clashes(s, exclude=("HARNESS_NOSE_J10_8",)).items() if not any(t in k for t in ("RESERVE", "KEEP_OUT", "CORRIDOR", "SLIDE_PATH"))}
        route_hits[label.split("/")[-1]] = hits

    report = {"sweeps": results, "tools": tools, "j10_8_route_hits": route_hits, "region": REGION}
    out = HERE / "generated" / "nose-service.json"
    out.write_text(json.dumps(report, indent=1) + "\n")
    lines = ["# Nose service-access sweeps (D-011)", "", "Generated by `check_nose_service.py`, body installed. A path is clear when it has no first hit.", ""]
    for name, r in results.items():
        hits = ", ".join(f"`{k}` at {v['at_mm']} mm" for k, v in r["first_hits"].items()) or "clear"
        lines.append(f"- **{name}** ({r['distance_mm']} mm, removed first: {', '.join(r['removed_first']) or 'nothing'}): {hits}")
    for name, hits in tools.items():
        lines.append(f"- **{name}**: {', '.join(hits) or 'clear'}")
    for name, hits in route_hits.items():
        lines.append(f"- **{name}**: {', '.join(f'{k} {v} mm3' for k, v in hits.items()) or 'clear'}")
    (HERE / "generated" / "nose-service.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
