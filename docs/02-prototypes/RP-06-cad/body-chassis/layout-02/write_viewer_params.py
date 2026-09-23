"""Write body-chassis.params.js: viewer pose controls for Layout 02.

Presentation only; the STEP stays at the neutral pose. Every pivot is
recomputed here in chassis coordinates from the model's constants and the
head Layout 04 axes, and every part is bucketed into a motion frame from the
built assembly tree, so a rebuild or a head change regenerates them.

Frames, innermost first (each transform is applied in the world frame, so
the order is roll -> pitch -> yaw -> drive):
  R  roll-carried head parts        P  pitch-carried head parts
  Y  yaw-carried (yoke legs, turntable spur, clamp ring, yaw branch)
  wheel L / R spin about their own axle, then the whole robot drives.

Looping animations (the viewer's Animation panel) drive the same sliders.

Run from this folder after `gen`, with the legacy runtime's Python.
"""

from __future__ import annotations

import json
from pathlib import Path

import body_chassis_model as M

HERE = Path(__file__).resolve().parent
ASSEMBLY = HERE / "__cadgen__/models/body-chassis.step.py/assembly.json"
OUT = HERE / "body-chassis.params.js"

# Head physics markers that ride a frame (the rest stay neutral), as in
# head/layout-04/write_viewer_params.py.
HEAD_PHYSICS_FRAMES = {
    "R": ["estimated_CoM_R", "roll_A0_residual", "camera_102deg_FOV_corner_envelope"],
    "P": ["roll_axis_through_A0", "estimated_CoM_RP", "pitch_A0_residual"],
    "Y": ["pitch_axis_through_A0", "estimated_CoM_RPY", "yaw_axis"],
}
HEAD_PHYSICAL_FRAMES = {"R": "rolling", "P": "pitch_carried", "Y": "yaw_carried"}
HEAD_TRAVEL = {
    "roll": M.HEAD_ENVELOPE["usable_travel"]["roll_deg"],
    "pitch": M.HEAD_ENVELOPE["usable_travel"]["pitch_deg"],
    "yaw": [-55.0, 55.0],  # clock-spring reserve rating, RP-06 yaw stage
}
WHEEL_TURNS = 3  # slider range, each way; a spin turn on the spot needs ~2.02


def _index(root):
    by_path, by_name = {}, {}

    def walk(node, path):
        path = path + (node["name"],)
        by_path[path] = node["id"]
        by_name.setdefault(node["name"], []).append(node["id"])
        for child in node.get("children", []):
            walk(child, path)

    walk(root, ())
    return by_path, by_name


def _one(by_name, name):
    ids = by_name.get(name, [])
    if len(ids) != 1:
        raise SystemExit(f"expected one node named {name!r}, found {ids}")
    return ids[0]


def _ref(ids):
    return {"ref": "#" + ",".join(ids)}


def main():
    root = json.loads(ASSEMBLY.read_text())["assembly"]["root"]
    by_path, by_name = _index(root)
    top = {name: node_id for path, node_id in by_path.items() if len(path) == 2 for name in [path[1]]}

    M._load_head_model()
    import harness  # head/layout-04, on sys.path after the load above

    routes, _ = harness.routes()
    frames = {"R": [], "P": [], "Y": []}
    for frame, group in HEAD_PHYSICAL_FRAMES.items():
        frames[frame].append(by_path[(root["name"], "RP01_HEAD_LAYOUT03", "physical", group)])
        frames[frame] += [_one(by_name, n) for n in HEAD_PHYSICS_FRAMES[frame]]
    for name, route in routes.items():
        frames[route["frame"]].append(_one(by_name, name))
    # Body-side half of the yaw stage that turns with the head.
    frames["Y"].append(_one(by_name, "BODY_YAW_DRIVE_MOVING"))

    features = {f"frame_{k}": _ref(v) for k, v in frames.items()}
    features["yaw_pinion"] = _ref([_one(by_name, "YAW_DRIVE_SPUR_1TO1")])
    for side in "LR":
        features[f"wheel_{side}"] = _ref([top[f"WHEEL_{side}"], _one(by_name, f"MOTOR_{side}_OUTPUT_SHAFT")])
    groups = {
        "shell": ["BODY_SHELL", "BODY_PANELS", "PANEL_MOUNT_HARDWARE"],
        "head": ["RP01_HEAD_LAYOUT03"],
        "structure": ["CHASSIS_PRIMARY_FRAME", "BODY_PRIMARY_FRAME", "BODY_CHASSIS_MOUNT_HARDWARE", "BODY_YAW_STAGE"],
        "drive": ["WHEEL_L", "WHEEL_R", "MOTOR_L", "MOTOR_R", "BEARING_PAIR_L", "BEARING_PAIR_R", "BALL_TRANSFER"],
        "rear_tail": ["REAR_SKID_TCRT_MODULE"],
        "electronics": ["BODY_ELECTRONICS"],
        "sensors": ["BODY_SENSORS"],
        "audio": ["BODY_AUDIO"],
        "harness": ["HARNESS_ROUTES", "RP01_HEAD_HARNESS"],
        "physics": ["RP01_HEAD_PHYSICS", "PHYSICS_OVERLAYS"],
    }
    for key, names in groups.items():
        features[key] = _ref([top[n] for n in names])
    missing = set(top) - {n for names in groups.values() for n in names}
    if missing:
        raise SystemExit(f"top-level nodes with no visibility group: {sorted(missing)}")

    ox, oy, oz = M.HEAD_ORIGIN_IN_CHASSIS
    a = M.HEAD_AXES
    pivots = {
        "roll": [ox, oy + a["roll_y"], oz + a["roll_z"]],
        "pitch": [ox + a["pitch_x"], oy, oz + a["pitch_z"]],
        "yaw": list(M.HEAD_YAW_DATUM),
        "pinion": [M.BODY_AXIS_X + M.YAW_PINION_CENTER[0], M.YAW_PINION_CENTER[1], 0.0],
        "wheel_L": list(M.WHEEL_CENTER_L),
        "wheel_R": list(M.WHEEL_CENTER_R),
    }
    geometry = {
        "pivots": {k: [round(v, 4) for v in p] for k, p in pivots.items()},
        "wheel_radius": M.WHEEL_OD / 2.0,
        "track": M.TRACK,
        "yaw_ratio": M.YAW_GEAR_RATIO,
        "wheel_limit_deg": 360 * WHEEL_TURNS,
        "travel": HEAD_TRAVEL,
    }

    parameters = {}
    for joint, (lo, hi) in HEAD_TRAVEL.items():
        parameters[f"head_{joint}_deg"] = dict(type="number", label=f"Head {joint}", unit="°", min=lo, max=hi, step=1, default=0)
    span = 360 * WHEEL_TURNS
    for side, label in (("L", "left"), ("R", "right")):
        parameters[f"wheel_{side}_deg"] = dict(
            type="number", label=f"Wheel {label} (+ = forward)", unit="°", min=-span, max=span, step=5, default=0
        )
    parameters["drive_on_floor"] = dict(type="boolean", label="Wheels drive the robot on the floor", default=True)
    for key, label, default in [
        ("shell", "Show translucent shell", True),
        ("head", "Show RP-01 Layout 04 head", True),
        ("structure", "Show body/chassis structure", True),
        ("drive", "Show drivetrain", True),
        ("rear_tail", "Show rear skid/TCRT keel", True),
        ("electronics", "Show electronics", True),
        ("sensors", "Show sensors", True),
        ("audio", "Show speaker and microphones", True),
        ("harness", "Show harness routes", True),
        ("physics", "Show physics overlays", False),
    ]:
        parameters[f"show_{key}"] = dict(type="boolean", label=label, default=default)

    manifest = dict(
        schemaVersion=1,
        step={"path": "body-chassis/layout-02/body-chassis.step"},
        parameters=parameters,
        features=features,
    )
    code = (
        "// Generated by write_viewer_params.py; presentation only, the STEP stays neutral.\n"
        "// Pivots are chassis coordinates (mm): origin on the floor under the axle.\n"
        f"const geo = {json.dumps(geometry)};\n"
        + JS_BODY.replace("__MANIFEST__", json.dumps(manifest, indent=2, ensure_ascii=False))
    )
    OUT.write_text(code)
    print(f"Wrote {OUT.name}: " + ", ".join(f"{k} {len(v['ref'].split(','))}" for k, v in features.items()))


JS_BODY = """const clamp = (value, min, max) => Math.max(min, Math.min(max, Number(value) || 0));
const rot = (axis, origin, angleDeg) => ({ rotate: { axis, origin, angleDeg } });
const RAD = Math.PI / 180;

// Differential drive from the two wheel angles: equal arcs translate, unequal
// arcs turn about the instantaneous centre on the axle line (x = 0).
function drivePose(leftDeg, rightDeg) {
  const sL = leftDeg * RAD * geo.wheel_radius;
  const sR = rightDeg * RAD * geo.wheel_radius;
  const turn = (sR - sL) / geo.track;
  const travel = (sL + sR) / 2;
  if (Math.abs(turn) < 1e-9) return { translate: [travel, 0, 0] };
  return rot([0, 0, 1], [0, travel / turn, 0], turn / RAD);
}

const wave = (progress) => Math.sin(2 * Math.PI * progress);
// Wheel angle for one full heading turn on the spot: each wheel rolls once
// round a circle of radius track / 2, i.e. pi * track of travel.
const SPIN_TURN_DEG = (geo.track / 2 / geo.wheel_radius) * 360;
const animations = {
  wheels_spin: {
    label: "Wheels spin in place",
    duration: 2,
    update({ progress, set }) {
      set("drive_on_floor", false);
      set("wheel_L_deg", 360 * progress);
      set("wheel_R_deg", 360 * progress);
    }
  },
  drive_forward_back: {
    label: "Drive forward and back",
    duration: 5,
    update({ progress, set }) {
      const angle = 540 * wave(progress);
      set("drive_on_floor", true);
      set("wheel_L_deg", angle);
      set("wheel_R_deg", angle);
    }
  },
  spin_turn: {
    // Out and back: a full turn leaves the wheels at ~729 deg, not a whole
    // number of wheel turns, so a one-way loop would jump the wheel index.
    label: "Turn 360° on the spot and back",
    duration: 8,
    update({ progress, set }) {
      const angle = SPIN_TURN_DEG * (1 - Math.cos(2 * Math.PI * progress)) / 2;
      set("drive_on_floor", true);
      set("wheel_L_deg", -angle);
      set("wheel_R_deg", angle);
    }
  },
  head_look_around: {
    label: "Head look around",
    duration: 8,
    update({ progress, set }) {
      const t = geo.travel;
      set("head_yaw_deg", t.yaw[1] * wave(progress));
      set("head_pitch_deg", (t.pitch[1] / 2) * Math.max(0, wave(2 * progress)) + (t.pitch[0] / 2) * Math.max(0, -wave(2 * progress)));
      set("head_roll_deg", (t.roll[1] / 2) * wave(progress + 0.25));
    }
  }
};

export default {
  manifest: { ...__MANIFEST__, animations },
  update({ params, effects }) {
    const t = geo.travel;
    const roll = clamp(params.head_roll_deg, t.roll[0], t.roll[1]);
    const pitch = clamp(params.head_pitch_deg, t.pitch[0], t.pitch[1]);
    const yaw = clamp(params.head_yaw_deg, t.yaw[0], t.yaw[1]);
    const r = rot([1, 0, 0], geo.pivots.roll, roll);
    const p = rot([0, 1, 0], geo.pivots.pitch, pitch);
    const y = rot([0, 0, 1], geo.pivots.yaw, yaw);
    effects.transform("frame_R", { transforms: [r, p, y] });
    effects.transform("frame_P", { transforms: [p, y] });
    effects.transform("frame_Y", y);
    // External 1:1 spur mesh: the servo pinion turns the other way.
    effects.transform("yaw_pinion", rot([0, 0, 1], geo.pivots.pinion, -yaw / geo.yaw_ratio));

    const wl = clamp(params.wheel_L_deg, -geo.wheel_limit_deg, geo.wheel_limit_deg);
    const wr = clamp(params.wheel_R_deg, -geo.wheel_limit_deg, geo.wheel_limit_deg);
    // Positive rotation about +Y carries the tyre top toward +X: forward roll.
    effects.transform("wheel_L", rot([0, 1, 0], geo.pivots.wheel_L, wl));
    effects.transform("wheel_R", rot([0, 1, 0], geo.pivots.wheel_R, wr));
    if (params.drive_on_floor !== false) effects.transform("*", drivePose(wl, wr));

    for (const key of ["shell", "head", "structure", "drive", "rear_tail", "electronics", "sensors", "audio", "harness", "physics"]) {
      effects.visible(key, params[`show_${key}`] !== false);
    }
  }
};
"""


if __name__ == "__main__":
    main()
