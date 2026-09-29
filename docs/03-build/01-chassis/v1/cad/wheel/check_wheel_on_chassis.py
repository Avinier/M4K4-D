"""Wheel-on-chassis checks: the D-008/D-009 wheel against every static chassis/body part.

A targeted subset of ../check_layout.py for wheel changes, which re-checks the
whole robot and takes far longer. It uses the same static set (chassis frame
without the ball pod, body shell/panels/frame/hardware, electronics, motors
without the output shaft; the bearings bridge static and rotating by design).

Unlike check_layout.py, it does not assume the wheel is axisymmetric: ring
corners, the hub-cap hex, spokes, lugs and screw heads sweep beyond their
resting shape. Every rotating leaf except the rim and the (axisymmetric) stub is replaced by its revolved
envelope (inner radius measured as the distance to the axle line, outer radius
the largest bounding radius over 5-degree rotations). The rim cannot be
enveloped that way, because the bearing housing sits inside its pocket, so it is
rotated through its 60-degree symmetry period in 5-degree steps instead.

Writes generated/on-chassis-checks.json and .md. Run from this folder with the
text-to-cad runtime (PYTHONPATH as in README.md).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from build123d import Axis, Compound, Edge

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import body_chassis_model as M  # noqa: E402

OUT = HERE / "generated"
STEP_DEG = 5.0
RIM_PERIOD_DEG = 60.0


def leaves(shape):
    kids = getattr(shape, "children", None)
    return [leaf for kid in kids for leaf in leaves(kid)] if kids else [shape]


def near(a, b, margin):
    ba, bb = a.bounding_box(), b.bounding_box()
    return all(
        getattr(ba.min, k) - margin <= getattr(bb.max, k) and getattr(bb.min, k) - margin <= getattr(ba.max, k)
        for k in ("X", "Y", "Z")
    )


def main():
    axle = Axis((0.0, 0.0, M.AXLE_Z), (0.0, 1.0, 0.0))
    axle_line = Edge.make_line((0.0, -400.0, M.AXLE_Z), (0.0, 400.0, M.AXLE_Z))

    def r_max(shape):
        best = 0.0
        for i in range(int(RIM_PERIOD_DEG / STEP_DEG)):
            bb = shape.rotate(axle, i * STEP_DEG).bounding_box()
            best = max(best, abs(bb.min.X), abs(bb.max.X), abs(bb.min.Z - M.AXLE_Z), abs(bb.max.Z - M.AXLE_Z))
        return best

    def envelope(shape):
        bb = shape.bounding_box()
        outer = M._axial_bore_y(r_max(shape), bb.min.Y, bb.max.Y, 0.0, M.AXLE_Z)
        inner = shape.distance_to(axle_line)
        if inner > 1e-3:
            outer = outer - M._axial_bore_y(inner, bb.min.Y - 1.0, bb.max.Y + 1.0, 0.0, M.AXLE_Z)
        return outer, round(inner, 3)

    chassis_frame = M.chassis_frame()
    chassis_static = leaves(Compound(children=[c for c in chassis_frame.children if c.label != "BALL_POD"]))
    body_static = [
        M.body_shell(), *leaves(M.body_panels()), *leaves(M.panel_mount_hardware()),
        *leaves(M.body_primary_frame()), *M.electronics().children,
    ]

    rows = []
    min_gap = M.WHEEL_RUNNING_CLEARANCE_MIN
    for side in ("L", "R"):
        motor = [c for c in M.motor_envelope(side).children if "OUTPUT_SHAFT" not in c.label]
        static = [*chassis_static, *body_static, *motor]
        wheel = M.wheel_assembly(side)
        parts = {c.label: c for c in wheel.children}

        swept = {}
        for label, part in parts.items():
            if label.endswith("_RIM_PETG"):
                continue
            if label.endswith("_STUB_SHAFT_8MM"):
                # D-007's turned stub is stepped and axisymmetric: test it as built,
                # as check_layout.py does; its set screw is swept on its own.
                env, inner = part, None
            else:
                env, inner = envelope(part)
            candidates = [t for t in static if near(env, t, 25.0)]
            gap = min(((round(env.distance_to(t), 3), t.label) for t in candidates), default=(None, None))
            swept[label] = {"min_gap_mm": gap[0], "to": gap[1], "inner_r_mm": inner}
        worst = min((v["min_gap_mm"], k) for k, v in swept.items() if v["min_gap_mm"] is not None)
        rows.append({
            "check": f"swept_wheel_parts_clear_{side}",
            "pass": worst[0] >= min_gap - 1e-6,
            "value": {"minimum_mm": min_gap, "worst": {"part": worst[1], **swept[worst[1]]}, "parts_swept": len(swept)},
            "detail": swept,
        })

        rim = parts[f"WHEEL_{side}_RIM_PETG"]
        candidates = [t for t in static if near(rim, t, 10.0)]
        samples = []
        for i in range(int(RIM_PERIOD_DEG / STEP_DEG)):
            turned = rim.rotate(axle, i * STEP_DEG)
            samples.append(min((round(turned.distance_to(t), 3), t.label, i * STEP_DEG) for t in candidates))
        low = min(samples)
        rows.append({
            "check": f"rim_clear_through_60deg_{side}",
            "pass": low[0] >= min_gap - 1e-6,
            "value": {"minimum_mm": min_gap, "min_gap_mm": low[0], "to": low[1], "at_deg": low[2], "static_parts_checked": len(candidates)},
        })

        stub = parts[f"WHEEL_{side}_STUB_SHAFT_8MM"]
        screws = [p for label, p in parts.items() if "_SCREW_M3X6_" in label]
        thread = []
        for sc in screws:
            bb = sc.bounding_box()
            lo, hi = sorted((abs(bb.min.Y), abs(bb.max.Y)))
            thread.append(round(max(0.0, min(hi, M.STUB_FLANGE[2]) - max(lo, M.STUB_FLANGE[1])), 3))
        clash = sum(
            ((a & b).volume if (a & b) is not None else 0.0)
            for i, a in enumerate(parts.values()) for b in list(parts.values())[i + 1:]
        )
        rows.append({
            "check": f"wheel_on_stub_{side}",
            "pass": len(screws) == 3 and all(abs(t - 2.0) < 1e-6 for t in thread) and clash < 1e-3
            and all(sc.distance_to(stub) < 1e-6 for sc in screws),
            "value": {"wheel_screws": len(screws), "thread_in_flange_mm": thread, "internal_overlap_mm3": round(clash, 4)},
        })

    OUT.mkdir(exist_ok=True)
    (OUT / "on-chassis-checks.json").write_text(json.dumps(rows, indent=2) + "\n")
    lines = [
        "# Wheel-on-chassis checks", "",
        "Generated by `check_wheel_on_chassis.py`: the wheel's swept volume against every static chassis/body part.", "",
        "| Check | Result | Value |", "|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['check']} | {'PASS' if r['pass'] else 'FAIL'} | `{json.dumps(r['value'])}` |")
    (OUT / "on-chassis-checks.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    failed = [r for r in rows if not r["pass"]]
    print(f"\n{len(rows) - len(failed)}/{len(rows)} pass")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
