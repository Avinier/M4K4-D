"""Deterministic source-level checks for RP-03 integrated Layout 02."""

from __future__ import annotations

import json
import math
from pathlib import Path

from build123d import Axis, Compound, GeomType, Location, Vertex

import body_chassis_model as M

# physics.md 2.5: the +20 mm margin line is a_tip = g*20/124 at the 124 mm baseline CoM height.
PHYSICS_MARGIN_A_TIP_MIN = 9.81 * 20.0 / 124.0

def _vol(shape):
    """Volume of a boolean result; an empty intersection is None, meaning zero."""
    return 0.0 if shape is None else shape.volume


HERE = Path(__file__).resolve().parent


def main():
    transformed_yaw = tuple(
        M.HEAD_ORIGIN_IN_CHASSIS[index] + M.HEAD_LOCAL_YAW[index]
        for index in range(3)
    )
    wheel_l_y = tuple(M.wheel_assembly("L").children[0].bounding_box().center())[1]
    wheel_r_y = tuple(M.wheel_assembly("R").children[0].bounding_box().center())[1]
    rear_module = M.rear_skid_tcrt_module()
    rear_keel = rear_module.children[-1]
    # The tail is a parked accessory: check its geometry standalone so it stays
    # valid for re-enabling, and check that it is really out of the assembly.
    rear_tail = M.rear_tail()
    module_labels = [child.label for child in rear_module.children]
    tail_segments, tail_root = rear_tail.children
    keel_body, keel_floor, keel_cartridge, keel_cable, keel_hardware = rear_keel.children
    keel_shoe, keel_guard_l, keel_guard_r = keel_floor.children
    keel_sensor_package = keel_cartridge.children[0]
    body_frame = M.body_primary_frame()
    chassis_frame = M.chassis_frame()
    frame_chassis_overlap = _vol(body_frame & chassis_frame)
    audio_sensor_overlap = _vol(M.body_audio() & M.sensors())
    # Stationary yaw stage against everything it could hit inside the body.
    yaw_stage = M.body_yaw_stage()
    # Air above the Pi cooler: no yaw-stage part, stationary or moving, and no
    # clock-spring reserve inside the headroom prism over the cooler footprint.
    headroom = M._block(-26.0 + M.BODY_SHIFT_X, 38.0 + M.BODY_SHIFT_X, -22.0, 22.0, M.PI_COOLER_TOP_Z, M.PI_COOLER_TOP_Z + M.PI_COOLER_HEADROOM)
    moving_parts = M.yaw_drive_moving_parts()
    clockspring = [c for c in M.harness_routes().children if c.label == "HARNESS_HEAD_YAW_CLOCKSPRING_RESERVE"]
    plate = [c for c in body_frame.children if c.label == "HEAD_YAW_ADAPTER_PLATE"]
    cooler_headroom_clash = sum(_vol(headroom & part) for part in [*yaw_stage.children, *moving_parts, *clockspring, *plate])
    yaw_clash = sum(
        _vol(part & other)
        for part in [*yaw_stage.children, *moving_parts]
        for other in [*body_frame.children, *M.electronics().children, M.body_shell(), *M.sensors().children, *M.body_audio().children]
    )
    rear_crossmember = next(child for child in chassis_frame.children if child.label == "REAR_SKID_CROSSMEMBER")
    body_shell = M.body_shell()
    body_panels = M.body_panels()

    # Service panels, measured from the built solids rather than the
    # constants that generated them.
    panel_by_face = {
        "FRONT": next(c for c in body_panels.children if c.label == "FRONT_SERVICE_PANEL_FUNCTIONAL_GRILLE"),
        "REAR": next(c for c in body_panels.children if c.label == "REAR_SERVICE_PANEL_OCTAGONAL"),
    }
    panel_hardware = M.panel_mount_hardware()
    frame_by_face = {face: next(c for c in panel_hardware.children if c.label == f"{face}_PANEL_INTERNAL_FRAME_WITH_BOSSES") for face in panel_by_face}
    outer_face_x = {"FRONT": M.BODY_X_FRONT + M.SHELL_THICKNESS, "REAR": M.BODY_X_REAR - M.SHELL_THICKNESS}
    shell_face_x = {"FRONT": M.BODY_X_FRONT, "REAR": M.BODY_X_REAR}

    def side_edge_slope(shape, x):
        """|dy/dz| of the outermost straight, non-chamfer, +Y side edge in the plane X = x."""
        best = None
        for edge in shape.edges():
            if edge.geom_type != GeomType.LINE:
                continue
            a, b = edge.start_point(), edge.end_point()
            if abs(a.X - x) > 1e-6 or abs(b.X - x) > 1e-6 or min(a.Y, b.Y) <= 0.0:
                continue
            dy, dz = abs(b.Y - a.Y), abs(b.Z - a.Z)
            if dy < 1e-6 or dz < 1e-6 or dy / dz > 0.5:
                continue
            if best is None or max(a.Y, b.Y) > best[0]:
                best = (max(a.Y, b.Y), dy / dz)
        return best[1]

    panel_edge_angle_deg = {
        face: {
            "panel": round(math.degrees(math.atan(side_edge_slope(panel_by_face[face], outer_face_x[face]))), 4),
            "shell": round(math.degrees(math.atan(side_edge_slope(body_shell, shell_face_x[face]))), 4),
        }
        for face in panel_by_face
    }
    # Land width = shell area under the panel outline / mean outline perimeter.
    panel_land_mm = {}
    for face, x in shell_face_x.items():
        inward = -1.0 if face == "FRONT" else 1.0
        slab = M._service_panel_outline(face, min(x, x + inward), max(x, x + inward))
        land_area = _vol(slab & body_shell)
        outline = M._service_panel_outline(face, x, x + 1.0).faces().filter_by(Axis.X)[0]
        opening = M._service_panel_outline(face, x, x + 1.0, -M.PANEL_OVERLAP).faces().filter_by(Axis.X)[0]
        mean_perimeter = (sum(e.length for e in outline.outer_wire().edges()) + sum(e.length for e in opening.outer_wire().edges())) / 2.0
        panel_land_mm[face] = round(land_area / mean_perimeter, 4)

    def fastener_inset(face, y, z):
        outline = M._service_panel_outline(face, 0.0, 1.0).faces().filter_by(Axis.X)[0]
        return min(Vertex(0.0, y, z).distance_to(edge) for edge in outline.outer_wire().edges())

    fastener_insets = {
        face: [round(fastener_inset(face, y, z), 3) for y, z in points]
        for face, points in (("FRONT", M.FRONT_PANEL_FASTENERS), ("REAR", M.REAR_PANEL_FASTENERS))
    }

    def probe_hits(shape, x0, x1, y, z):
        return _vol(shape & M._block(x0, x1, y - 0.5, y + 0.5, z - 0.25, z + 0.25)) > 1e-6

    # Probe the frame plate on the centreline just inside its top and bottom edges.
    frame_plate_x = {"FRONT": (M.BODY_X_FRONT - 4.0, M.BODY_X_FRONT - 3.0), "REAR": (M.BODY_X_REAR + 3.0, M.BODY_X_REAR + 4.0)}
    panel_z0 = {"FRONT": M.FRONT_PANEL_Z0, "REAR": M.REAR_PANEL_Z0}
    frame_rings = {
        face: {
            "solids": len(frame.solids()),
            "bottom_bar": probe_hits(frame, *frame_plate_x[face], 0.0, panel_z0[face] + 3.0),
            "top_bar": probe_hits(frame, *frame_plate_x[face], 0.0, M.PANEL_Z1 - 3.0),
        }
        for face, frame in frame_by_face.items()
    }
    # Every panel-area part against the body, chassis and interior groups.
    sensor_parts = [c for c in M.sensors().children if c.label != "GP2Y_OPTICAL_AXIS"]
    optical_axis = next(c for c in M.sensors().children if c.label == "GP2Y_OPTICAL_AXIS")
    panel_parts = [*(c for c in body_panels.children if not c.label.startswith("WHEEL_ARCH")), *panel_hardware.children]
    others = [body_shell, *chassis_frame.children, *body_frame.children, *M.electronics().children, *M.body_audio().children, *sensor_parts]
    panel_clashes = {}
    for part in panel_parts + [c for c in sensor_parts if c.label == "GP2Y0A41SK0F_STEP"]:
        for other in others + panel_parts:
            if other is part or "KEEP_OUT" in other.label:
                continue
            if not part.bounding_box().overlaps(other.bounding_box()):
                continue
            volume = _vol(part & other)
            if volume > 1e-3:
                key = " x ".join(sorted((part.label, other.label)))
                panel_clashes[key] = round(volume, 3)
    range_window_blockage = sum(
        _vol(optical_axis & shape)
        for shape in [
            body_shell,
            *panel_parts,
            *chassis_frame.children,
            *[c for c in sensor_parts if c.label == "BALL_NOSE_CONCEALED_CONTACT_MODULE"][0].children,
        ]
        if "TRAVEL_RESERVE" not in shape.label
    )
    removal_path = M._service_panel_outline("FRONT", M.BODY_X_FRONT + M.SHELL_THICKNESS, M.BODY_X_FRONT + 48.0)
    front_removal_blockers = {
        shape.label: round(_vol(removal_path & shape), 3)
        for shape in [*chassis_frame.children, M.ball_transfer(), *sensor_parts]
        if _vol(removal_path & shape) > 1e-3
    }

    def keel_underside_z(x, y):
        probe = M._block(x - 0.2, x + 0.2, y - 0.2, y + 0.2, 0.0, 40.0)
        hit = keel_body & probe
        return round(hit.bounding_box().min.Z, 4) if _vol(hit) > 1e-9 else None

    shoe_top_z = M.SKID_SHOE_BOTTOM_Z + M.SKID_SHOE_SIZE[2]
    shoe_x0 = M.SKID_PAD_CENTER[0] - M.SKID_SHOE_SIZE[0] / 2.0 + 1.0
    shoe_x1 = M.SKID_PAD_CENTER[0] + M.SKID_SHOE_SIZE[0] / 2.0 - 1.0
    shoe_backing = {
        f"{x:.1f},{y:.1f}": keel_underside_z(x, y)
        for x in (shoe_x0, M.SKID_PAD_CENTER[0], shoe_x1)
        for y in (-M.SKID_SHOE_SIZE[1] / 2.0 + 1.0, 0.0, M.SKID_SHOE_SIZE[1] / 2.0 - 1.0)
        if not any(abs(x - sx) < 3.0 and abs(y - sy) < 3.0 for sx in M.REAR_KEEL_SCREWS_X for sy in (-5.5, 5.5))
    }
    guard_top_z = M.TCRT_GUARD_BOTTOM_Z + M.REAR_KEEL_GUARD_HEIGHT
    guard_backing = {
        f"{x:.1f}": keel_underside_z(x, 5.6)
        for x in (M.REAR_KEEL_GUARD_X[0] + 0.5, sum(M.REAR_KEEL_GUARD_X) / 2.0, M.REAR_KEEL_GUARD_X[1] - 0.5)
    }

    def first_contact_pitch_deg(shape):
        angles = [math.degrees(math.atan2(v.Z, -v.X)) for v in shape.vertices() if v.X < 0.0]
        return round(min(angles), 3)

    pitch = {
        "shoe": first_contact_pitch_deg(keel_shoe),
        "guards": first_contact_pitch_deg(keel_guard_l),
        "keel_body": first_contact_pitch_deg(keel_body),
        "tcrt": first_contact_pitch_deg(keel_sensor_package),
    }
    tail_points = [joint[:2] for joint in M.REAR_TAIL_JOINTS] + [M.REAR_TAIL_TIP]
    tail_rise_deg = [
        round(math.degrees(math.atan2(b[1] - a[1], a[0] - b[0])), 2)
        for a, b in zip(tail_points, tail_points[1:])
    ]
    tail_sizes = M.rear_tail_segment_sizes()

    def spin_radius(shape):
        return max(math.hypot(v.X, v.Y) for v in shape.vertices())

    # Ball nose (RP03-CAD-04), measured from the built solids.
    def leaves(shape):
        kids = getattr(shape, "children", None)
        return [leaf for kid in kids for leaf in leaves(kid)] if kids else [shape]

    def by_label(shapes, label):
        return next(s for s in shapes if s.label == label)

    ball_parts = leaves(M.ball_transfer())
    pod_group = next(c for c in chassis_frame.children if c.label == "BALL_POD")
    pod_parts = leaves(pod_group)
    front_crossmember = next(c for c in chassis_frame.children if c.label == "FRONT_CROSSMEMBER")
    nose_module = next(c for c in M.sensors().children if c.label == "BALL_NOSE_CONCEALED_CONTACT_MODULE")
    nose_parts = leaves(nose_module)
    gp2y_parts = [c for c in M.sensors().children if c.label.startswith("GP2Y") and c.label != "GP2Y_OPTICAL_AXIS"]
    flange = by_label(ball_parts, "BALL_TRANSFER_PURCHASED_3HOLE_FLANGE")
    housing = by_label(ball_parts, "BALL_TRANSFER_PURCHASED_HOUSING")
    pod_seat = by_label(pod_parts, "BALL_POD_PRINTED_SEAT")
    touch_cap = by_label(nose_parts, "BALL_NOSE_TOUCH_CAP")
    travel_reserve = by_label(nose_parts, "BALL_NOSE_3MM_TRAVEL_RESERVE")
    plunger = by_label(nose_parts, "BALL_NOSE_SWITCH_PLUNGER")
    ball_seat = {
        "flange_top_z_mm": round(flange.bounding_box().max.Z, 4),
        "pod_seat_z_mm": round(pod_seat.bounding_box().min.Z, 4),
        "gap_mm": round(flange.distance_to(pod_seat), 4),
        "overlap_mm3": round(_vol(flange & pod_seat), 4),
    }
    ball_stack_gaps = {
        "housing_to_flange_mm": round(housing.distance_to(flange), 4),
    }
    ball_screw_engagement = {
        part.label: round(min(part.bounding_box().max.Z, flange.bounding_box().max.Z) - max(part.bounding_box().min.Z, flange.bounding_box().min.Z), 3)
        for part in pod_parts
        if part.label.startswith("BALL_M3_SHANK")
    }

    # Every nose solid against every other, except a screw inside its own insert.
    nose_solids = [*ball_parts, *pod_parts, front_crossmember, *gp2y_parts, *[p for p in nose_parts if p is not travel_reserve]]
    nose_clashes = {}
    for i, a in enumerate(nose_solids):
        for b in nose_solids[i + 1:]:
            pair = {a.label.rsplit("_", 1)[0], b.label.rsplit("_", 1)[0]}
            if pair == {"BALL_POD_M3_SHANK", "BALL_POD_HEATSET_INSERT"}:
                continue
            if not a.bounding_box().overlaps(b.bounding_box()):
                continue
            volume = _vol(a & b)
            if volume > 1e-3:
                nose_clashes[" x ".join(sorted((a.label, b.label)))] = round(volume, 3)
    travel_blockers = {
        s.label: round(_vol(travel_reserve & s), 3)
        for s in [*ball_parts, *pod_parts, *gp2y_parts, *[p for p in nose_parts if p not in (travel_reserve, plunger)]]
        if _vol(travel_reserve & s) > 1e-3
    }
    rigid_nose = [*ball_parts, *pod_parts, *gp2y_parts]
    rigid_front_x = max(s.bounding_box().max.X for s in rigid_nose)
    # RP-03 C12: a 20 mm floor-level cube straight ahead. Since the skirt cut
    # (RP03-CAD-04, 2026-09-24) it is not claimed for the cap; record what it meets.
    # Sweep the cube's path rearward; the part whose hit face is furthest forward meets it first.
    c12_path = M._block(0.0, 170.0, -10.0, 10.0, 0.0, 20.0)
    c12_first = {}
    for s in [*rigid_nose, touch_cap]:
        hit = c12_path & s
        if _vol(hit) > 1e-3:
            c12_first[s.label] = round(hit.bounding_box().max.X, 3)
    c12_first_label = max(c12_first, key=c12_first.get)
    nose_front_x = touch_cap.bounding_box().max.X
    face_ahead = M.FRONT_RANGE_SENSOR_FACE_X - M.BALL_CONTACT[0]
    lookahead = {
        case: {
            "from_ball_contact_mm": required,
            "needed_from_face_mm": round(required - face_ahead, 2),
            "needed_from_face_if_charged_to_nose_front_mm": round(required + (nose_front_x - M.FRONT_RANGE_SENSOR_FACE_X), 2),
        }
        for case, required in M.FRONT_RANGE_REQUIRED_MM.items()
    }
    lookahead_ok = all(
        row["needed_from_face_if_charged_to_nose_front_mm"] <= M.FRONT_RANGE_MAX_MM for row in lookahead.values()
    )
    nose_width = touch_cap.bounding_box().size.Y
    # The pod's tongue passes the shell's front notch; the crossmember and rails stay inside.
    pod_shell_overlap = {s.label: round(_vol(s & body_shell), 3) for s in pod_parts if _vol(s & body_shell) > 1e-3}
    chassis_front_x = max(
        c.bounding_box().max.X for c in chassis_frame.children if c.label != "BALL_POD"
    )

    tail_spin_radius = spin_radius(rear_tail)
    nose_spin_radius = spin_radius(Compound(children=[M.ball_transfer(), pod_group, nose_module]))
    tail_head_parts = [
        child for child in tail_root.children if child.label.startswith("REAR_TAIL_ROOT_M3_HEAD")
    ]
    tail_shell_overlap = _vol(rear_tail & body_shell)
    # Parked, the rear panel carries no tail bores, so leave the M3 shanks out.
    tail_body_parts = [tail_segments] + [
        child for child in tail_root.children if M.REAR_TAIL_ENABLED or "_M3_" not in child.label
    ]
    tail_panel_overlap = _vol(Compound(children=tail_body_parts) & body_panels)
    keel_shell_overlap = _vol(rear_keel & body_shell)
    keel_crossmember_overlap = _vol(keel_body & rear_crossmember)
    keel_crossmember_gap = keel_body.distance_to(rear_crossmember)
    _hit = keel_sensor_package & keel_body
    tcrt_keel_collision = _hit.volume if _hit is not None else 0.0
    tail_bbox = rear_tail.bounding_box()

    # Drivetrain fit (RP03-CAD-05), measured from the built solids. The wheel
    # is axisymmetric about the axle, so its solids are its swept volume; every
    # stationary solid must keep a running gap to them. Bearings bridge the
    # stationary boss and the rotating stub by design, and the motor's output
    # shaft turns with the stub, so both are left out of the static set.
    chassis_static = leaves(Compound(children=[c for c in chassis_frame.children if c.label != "BALL_POD"]))
    # Electronics stay at group level: the Pi 5 vendor STEP's sub-shapes lose
    # their parent placement when walked as leaves.
    body_static = [body_shell, *leaves(body_panels), *leaves(panel_hardware), *leaves(body_frame), *M.electronics().children]
    def near(a, b, margin):
        ba, bb = a.bounding_box(), b.bounding_box()
        return all(
            getattr(ba.min, k) - margin <= getattr(bb.max, k) and getattr(bb.min, k) - margin <= getattr(ba.max, k)
            for k in ("X", "Y", "Z")
        )

    wheel_clearance = {}
    drivetrain_clashes = {}
    flange_seat = {}
    for side in ("L", "R"):
        rotating = M.wheel_assembly(side).children
        motor = [c for c in M.motor_envelope(side).children if "OUTPUT_SHAFT" not in c.label]
        static = [*chassis_static, *body_static, *motor]
        nearest = min(
            (round(r.distance_to(t), 3), r.label, t.label)
            for r in rotating
            for t in static
            if near(r, t, 5.0)
        )
        wheel_clearance[side] = {"min_gap_mm": nearest[0], "between": nearest[1:]}
        motor_solids = [c for c in motor if "PIGTAIL" not in c.label]
        for part in motor:
            for other in [*chassis_static, *body_static, *leaves(M.harness_routes())]:
                if not part.bounding_box().overlaps(other.bounding_box()):
                    continue
                if other.label.startswith(f"AXLE_MOTOR_SCREW_M3X8_{side}_"):
                    continue  # threads in the tapped faceplate; measured in motor_joint below
                volume = _vol(part & other)
                if volume > 1e-3:
                    drivetrain_clashes[f"{part.label} x {other.label}"] = round(volume, 3)
        gearbox = next(c for c in motor_solids if c.label.endswith("GEARBOX"))
        flange = by_label(chassis_static, f"AXLE_MOTOR_FLANGE_BEARING_BOSS_{side}")
        flange_seat[side] = {"gap_mm": round(gearbox.distance_to(flange), 4), "overlap_mm3": round(_vol(gearbox & flange), 4)}
    # Motor face joint (Pololu #4804): M3 x 8 countersunk screws through the
    # flange plate and diaphragm into the 6 mm blind face holes; the O4 shaft
    # engages the stub bore; the flush heads stay clear of the inner bearing.
    motor_joint = {}
    for side in ("L", "R"):
        screws = [c for c in chassis_static if c.label.startswith(f"AXLE_MOTOR_SCREW_M3X8_{side}_")]
        insertion = [round(M.MOTOR_FACE_Y - min(abs(sc.bounding_box().min.Y), abs(sc.bounding_box().max.Y)), 3) for sc in screws]
        # The vendor STEP taps only the faceplate (O2.5 minor diameter), with a
        # clearance cavity behind; the screw's overlap with it is the thread.
        gearbox = next(c for c in M.motor_envelope(side).children if c.label.endswith("GEARBOX"))
        engage = []
        for sc in screws:
            thread = sc & gearbox
            engage.append(0.0 if thread is None or thread.volume < 1e-3 else round(thread.bounding_box().size.Y, 3))
        shaft = next(c for c in M.motor_envelope(side).children if "OUTPUT_SHAFT" in c.label)
        stub = next(c for c in M.wheel_assembly(side).children if "STUB_SHAFT" in c.label)
        shaft_in_stub = round(abs(shaft.bounding_box().max.Y if side == "L" else shaft.bounding_box().min.Y) - M.STUB_SHAFT_Y[0], 3)
        inner_bearing = M.bearing_pair(side).children[0]
        motor_joint[side] = {
            "screw_count": len(screws),
            "screw_insertion_mm": insertion,
            "thread_engaged_in_faceplate_mm": engage,
            "hole_depth_mm": M.MOTOR_SCREW_HOLE_DEPTH,
            "shaft_engaged_in_stub_mm": shaft_in_stub,
            "shaft_stub_overlap_mm3": round(_vol(shaft & stub), 4),
            "screw_head_to_inner_bearing_mm": round(min(sc.distance_to(inner_bearing) for sc in screws), 3),
        }
    bearings_in_boss = {}
    for side in ("L", "R"):
        boss = by_label(chassis_static, f"AXLE_MOTOR_FLANGE_BEARING_BOSS_{side}").bounding_box()
        for bearing in M.bearing_pair(side).children:
            bb = bearing.bounding_box()
            bearings_in_boss[bearing.label] = boss.min.Y - 1e-6 <= bb.min.Y and bb.max.Y <= boss.max.Y + 1e-6
    battery = by_label(M.electronics().children, "BATTERY_2S1P_18650_PACK")
    battery_parts = leaves(battery)
    battery_clashes = {}
    for other in [*chassis_static, *body_static, *leaves(M.harness_routes()), *leaves(M.body_audio()), *leaves(M.motor_envelope("L")), *leaves(M.motor_envelope("R"))]:
        if other.label == battery.label:
            continue
        volume = sum(_vol(part & other) for part in battery_parts if part.bounding_box().overlaps(other.bounding_box()))
        if volume > 1e-3:
            battery_clashes[other.label] = round(volume, 3)
    # The pack must sit inside the tub interior with retention clearance and
    # stay below the deck top; the tub's hatch is its floor.
    pack_bb = battery.bounding_box()
    tub_inner = {
        "x": (M.BATTERY_TUB_X[0] + M.BATTERY_TUB_WALL, M.BATTERY_TUB_X[1]),
        "y": (-(M.BATTERY_TUB_HALF_Y - M.BATTERY_TUB_WALL), M.BATTERY_TUB_HALF_Y - M.BATTERY_TUB_WALL),
    }
    battery_tub_margin = {
        "rear_x_mm": round(pack_bb.min.X - tub_inner["x"][0], 3),
        "front_x_mm": round(tub_inner["x"][1] - pack_bb.max.X, 3),
        "side_y_mm": round(min(pack_bb.min.Y - tub_inner["y"][0], tub_inner["y"][1] - pack_bb.max.Y), 3),
        "floor_z_mm": round(pack_bb.min.Z - M.BATTERY_TUB_FLOOR_Z[1], 3),
        "below_deck_top_z_mm": round((M.DECK_Z + 2.0) - pack_bb.max.Z, 3),
    }
    ballast_parts = [c for c in chassis_static if c.label.startswith("BALLAST_")]
    ballast_clashes = {}
    for other in [*(c for c in chassis_static if not c.label.startswith("BALLAST_")), *body_static, *leaves(M.harness_routes()), *leaves(M.body_audio()), *battery_parts, *leaves(M.motor_envelope("L")), *leaves(M.motor_envelope("R"))]:
        volume = sum(_vol(part & other) for part in ballast_parts if part.bounding_box().overlaps(other.bounding_box()))
        if volume > 1e-3:
            ballast_clashes[other.label] = round(volume, 3)
    ballast_gaps = {
        "tub_front_wall_mm": round(M.BALLAST_X[0] - (M.BATTERY_TUB_X[1] + M.BATTERY_TUB_WALL), 3),
        "front_crossmember_mm": round(M.FRONT_CROSSMEMBER_X[0] - M.BALLAST_X[1], 3),
        "deck_underside_mm": round(M.DECK_Z - 2.0 - M.BALLAST_Z[1], 3),
    }
    # The tub's walls and hatch pass through the shell floor opening.
    tub_shell_overlap = {
        part.label: round(_vol(part & body_shell), 3)
        for part in M.battery_tub().children
        if _vol(part & body_shell) > 1e-3
    }
    # RP-02 power-distribution boards (proposal 2026-09-25), measured from the built
    # solids. Everything real is checked for zero interference; the keep-outs are
    # reserved volumes and are checked the same way. The harness volumes are
    # unresolved route placeholders, so their overlaps with the boards are recorded
    # as OPEN and guarded against change rather than counted as a pass.
    power_group = by_label(M.electronics().children, "POWER_DISTRIBUTION_BOARDS")
    power_parts = leaves(power_group)
    electronics_others = [c for c in M.electronics().children if c.label != "POWER_DISTRIBUTION_BOARDS"]
    power_hardware = [
        *chassis_static,
        body_shell,
        *leaves(body_panels),
        *leaves(panel_hardware),
        *leaves(body_frame),
        *leaves(M.body_audio()),
        *leaves(M.body_yaw_stage()),
        *M.yaw_drive_moving_parts(),
        *sensor_parts,
        *electronics_others,
        *leaves(M.motor_envelope("L")),
        *leaves(M.motor_envelope("R")),
        *leaves(M.wheel_assembly("L")),
        *leaves(M.wheel_assembly("R")),
        *leaves(M.battery_tub()),
    ]
    power_clashes = {}
    power_gaps = {}
    for part in power_parts:
        best = None
        for other in power_hardware:
            if other.label == part.label:
                continue
            if part.bounding_box().overlaps(other.bounding_box()):
                volume = _vol(part & other)
                if volume > 1e-3:
                    power_clashes[f"{part.label} x {other.label}"] = round(volume, 3)
                    continue
            # The E-stop clamps on its well floor, so it touches the well by design.
            mounted = part.label.startswith("ESTOP_XA1E") and other.label == "REAR_PANEL_ESTOP_WELL"
            if "KEEP_OUT" not in part.label and not mounted and near(part, other, 5.0):
                distance = part.distance_to(other)
                if best is None or distance < best[0]:
                    best = (round(distance, 3), other.label)
        if best is not None:
            power_gaps[part.label] = {"nearest_mm": best[0], "to": best[1]}
    power_self_clashes = {}
    for i, a in enumerate(power_parts):
        for b in power_parts[i + 1:]:
            if a.label.split("_PCB")[0].split("_PARTS")[0] == b.label.split("_PCB")[0].split("_PARTS")[0]:
                continue  # a board's own plate and parts envelope touch by design
            if a.label.startswith("ESTOP_XA1E") and b.label.startswith("ESTOP_XA1E"):
                continue  # the switch body sits inside its own behind-panel keep-out
            if a.bounding_box().overlaps(b.bounding_box()) and _vol(a & b) > 1e-3:
                power_self_clashes[f"{a.label} x {b.label}"] = round(_vol(a & b), 3)
    power_harness_overlaps = {}
    harness_volumes = leaves(M.harness_routes())
    for part in power_parts:
        if "KEEP_OUT" in part.label:
            continue
        for volume_shape in harness_volumes:
            if part.bounding_box().overlaps(volume_shape.bounding_box()) and _vol(part & volume_shape) > 1e-3:
                power_harness_overlaps[f"{part.label} x {volume_shape.label}"] = round(_vol(part & volume_shape), 1)
    board_box = {c.label: c.bounding_box() for c in power_group.children}
    bay_gaps = {
        "pcb04_to_lower_cross_rear_mm": round(board_box["PCB04_BRANCH_CONVERTERS"].min.X - by_label(leaves(body_frame), "BODY_LOWER_CROSS_REAR").bounding_box().max.X, 3),
        "pcb03_to_lower_cross_front_mm": round(by_label(leaves(body_frame), "BODY_LOWER_CROSS_FRONT").bounding_box().min.X - board_box["PCB03_MOTOR_GATE_AND_HEAD_RAIL"].max.X, 3),
        "pcb04_to_pcb03_mm": round(board_box["PCB03_MOTOR_GATE_AND_HEAD_RAIL"].min.X - board_box["PCB04_BRANCH_CONVERTERS"].max.X, 3),
        "pcb03_to_drv8874_y_mm": round(min(by_label(electronics_others, "DRV8874_LEFT_INSTALLED").bounding_box().min.Y, -by_label(electronics_others, "DRV8874_RIGHT_INSTALLED").bounding_box().max.Y) - board_box["PCB03_MOTOR_GATE_AND_HEAD_RAIL"].max.Y, 3),
        "pcb04_top_to_head_harness_vertical_z_mm": round(by_label(harness_volumes, "HARNESS_HEAD_VERTICAL").bounding_box().min.Z - board_box["PCB04_BRANCH_CONVERTERS"].max.Z, 3),
        "pcb04_top_to_compute_tray_z_mm": round(by_label(electronics_others, "COMPUTE_TRAY").bounding_box().min.Z - board_box["PCB04_BRANCH_CONVERTERS"].max.Z, 3),
        "pcb02_to_rear_panel_frame_x_mm": round(board_box["PCB02_CHARGE_AND_SYSTEM_POWER"].min.X - by_label(leaves(panel_hardware), "REAR_PANEL_INTERNAL_FRAME_WITH_BOSSES").bounding_box().max.X, 3),
    }
    footprints = {
        "PCB03_mm2": round((board_box["PCB03_MOTOR_GATE_AND_HEAD_RAIL"].size.X * board_box["PCB03_MOTOR_GATE_AND_HEAD_RAIL"].size.Y), 1),
        "PCB04_mm2": round((board_box["PCB04_BRANCH_CONVERTERS"].size.X * board_box["PCB04_BRANCH_CONVERTERS"].size.Y), 1),
        "PCB02_board_mm2 (vertical)": round((board_box["PCB02_CHARGE_AND_SYSTEM_POWER"].size.Y * board_box["PCB02_CHARGE_AND_SYSTEM_POWER"].size.Z), 1),
        "PCB01_mm2 (on the pack)": round(M.BATTERY_BMS_SIZE[0] * M.BATTERY_BMS_SIZE[1], 1),
        "removed_placeholder_envelopes_mm2": round(48.0 * 36.0 + 42.0 * 28.0, 1),
    }
    estop_head = by_label(power_parts, "ESTOP_XA1E_MUSHROOM_D29")
    estop_keep_out = by_label(power_parts, "ESTOP_XA1E_BEHIND_PANEL_KEEP_OUT")
    estop_well = next(c for c in body_panels.children if c.label == "REAR_PANEL_ESTOP_WELL")
    rear_frame = next(c for c in panel_hardware.children if c.label == "REAR_PANEL_INTERNAL_FRAME_WITH_BOSSES")
    pcb02_parts = [by_label(power_parts, n) for n in ("PCB02_CHARGE_AND_SYSTEM_POWER_PCB", "PCB02_CHARGE_AND_SYSTEM_POWER_PARTS_ENVELOPE")]
    rear_panel_solid = panel_by_face["REAR"]
    estop_geometry = {
        "head_min_x_mm": round(estop_head.bounding_box().min.X, 3),
        "head_max_x_mm": round(estop_head.bounding_box().max.X, 3),
        "panel_outer_face_x_mm": M.ESTOP_REAR_OUTER_X,
        "keep_out_x_mm": [round(estop_keep_out.bounding_box().min.X, 3), round(estop_keep_out.bounding_box().max.X, 3)],
        "keep_out_z_mm": [round(estop_keep_out.bounding_box().min.Z, 3), round(estop_keep_out.bounding_box().max.Z, 3)],
        "head_z_mm": [round(estop_head.bounding_box().min.Z, 3), round(estop_head.bounding_box().max.Z, 3)],
        "rear_panel_top_z_mm": round(rear_panel_solid.bounding_box().max.Z, 3),
        "head_vs_panel_mm3": round(_vol(estop_head & rear_panel_solid), 3),
        "head_proud_of_panel_mm": round(M.ESTOP_REAR_OUTER_X - estop_head.bounding_box().min.X, 3),
        "well_vs_frame_mm3": round(_vol(estop_well & rear_frame), 3),
        "well_gap_to_frame_mm": round(estop_well.distance_to(rear_frame), 3),
        "keep_out_vs_pcb02_mm3": round(sum(_vol(estop_keep_out & p) for p in pcb02_parts), 3),
        "rear_panel_cut_out": "octagonal well with a Ø16.2 floor cut-out (IDEC XA)",
    }
    # RP03-CAD-11 selected peripherals (../../peripheral-selection.md), measured from the
    # built solids: speaker, PCB-05, four PCB-06 mic boards and the PCB-07 IMU board must
    # clear every real part; the ports and boots pass the shell bores by design.
    audio_group = M.body_audio()
    imu_group = M.imu_board()
    audio_leaves = leaves(audio_group)
    imu_leaves = leaves(imu_group)
    selected_parts = [p for p in audio_leaves + imu_leaves if not any(k in p.label for k in ("ACOUSTIC_PORT", "PORT_BOOT"))]
    deck = by_label(chassis_static, "CHASSIS_DECK_WITH_BODY_INTERFACE")
    imu_shanks = [p for p in imu_leaves if p.label.startswith("IMU_M2_SCREW_SHANK")]
    selected_others = [
        *chassis_static, body_shell, *leaves(body_panels), *leaves(panel_hardware), *leaves(body_frame),
        *power_parts, *[c for c in M.electronics().children if c.label not in ("POWER_DISTRIBUTION_BOARDS", "IMU_PCB07")],
        *sensor_parts, *leaves(M.body_yaw_stage()), *M.yaw_drive_moving_parts(),
        *leaves(M.motor_envelope("L")), *leaves(M.motor_envelope("R")), *leaves(M.battery_tub()),
    ]
    selected_clashes = {}
    for part in selected_parts:
        for other in selected_others:
            if part in imu_shanks and other.label == deck.label:
                continue  # the M2 shank thread-forms into the deck by design
            if part.bounding_box().overlaps(other.bounding_box()):
                volume = _vol(part & other)
                if volume > 1e-3:
                    selected_clashes[f"{part.label} x {other.label}"] = round(volume, 3)
    # Within the group only the speaker in its own cavity, and screws through their board, touch by design.
    selected_self_clashes = {}
    for i, a in enumerate(selected_parts):
        for b in selected_parts[i + 1:]:
            if "CAVITY_KEEP_OUT" in a.label + b.label and "SPEAKER_K50WP" in a.label + b.label:
                continue
            if "IMU_M2_SCREW" in a.label + b.label and "IMU_PCB07_BOARD" in a.label + b.label:
                continue
            if a.bounding_box().overlaps(b.bounding_box()) and _vol(a & b) > 1e-3:
                selected_self_clashes[f"{a.label} x {b.label}"] = round(_vol(a & b), 3)
    selected_harness_overlaps = {}
    for part in selected_parts:
        for volume_shape in harness_volumes:
            if part.bounding_box().overlaps(volume_shape.bounding_box()) and _vol(part & volume_shape) > 1e-3:
                selected_harness_overlaps[f"{part.label} x {volume_shape.label}"] = round(_vol(part & volume_shape), 1)
    speaker_box = by_label(audio_group.children, "SPEAKER_VISATON_K50WP_8OHM").bounding_box()
    speaker_outline = {
        "depth_mm": round(speaker_box.max.X - speaker_box.min.X, 3),
        "diameter_mm": round(speaker_box.max.Y - speaker_box.min.Y, 3),
        "frame_face_x_mm": round(speaker_box.max.X, 3),
        "front_panel_inner_face_x_mm": M.BODY_X_FRONT,
        "vendor": "Visaton K 50 WP 8 ohm: Ø50 x 18 mm, Ø46 cutout, 48 g",
    }
    mic_axis = {}
    for x, y, z, name in M.MICROPHONE_PORTS:
        package = by_label(audio_leaves, f"PDM_MIC_{name}_IM73D122").bounding_box()
        board = by_label(audio_leaves, f"PDM_MIC_{name}_PCB06").bounding_box()
        mic_axis[name] = {
            "package_off_axis_mm": round(math.hypot(package.center().X - x, package.center().Z - z), 3),
            "board_outer_abs_y_mm": round(max(abs(board.min.Y), abs(board.max.Y)), 3),
        }
    imu_board_box = by_label(imu_leaves, "IMU_PCB07_BOARD").bounding_box()
    imu_seat = {
        "board_bottom_z_mm": round(imu_board_box.min.Z, 3),
        "deck_top_z_mm": round(deck.bounding_box().max.Z, 3),
        "shank_in_deck_mm3": {s.label: round(_vol(s & deck), 3) for s in imu_shanks},
        "board_vs_deck_mm3": round(_vol(by_label(imu_leaves, "IMU_PCB07_BOARD") & deck), 3),
        "board_x_mm": [round(imu_board_box.min.X, 3), round(imu_board_box.max.X, 3)],
    }
    pcb01 = by_label(battery_parts, "BATTERY_BMS_PCB01_PACK_PROTECTION")
    power_mass_ids = [
        "PCB02_CHARGE_AND_SYSTEM_POWER", "PACK_INTERFACE_SBS_MINI_AND_FUSE", "PCB03_MOTOR_GATE_AND_HEAD_RAIL",
        "PCB04_BRANCH_CONVERTERS", "C3_DEVKITC_N8", "DRV8874_CARRIERS_X2", "IMU_PCB07", "TCRT5000_BREAKOUT_AND_CABLE",
    ]
    mass_by_id = {row[0]: row[1] for row in M.MASS_ROWS}
    replaced_row_g = round(sum(mass_by_id[i] for i in power_mass_ids), 1)
    com = M.mass_properties()["com_mm"]
    com_ratio = com[0] / com[2]
    a_tip = 9.81 * com_ratio
    ball_share = com[0] / M.BALL_CONTACT[0]
    com_cross_pitch_deg = math.degrees(math.atan2(com[0], com[2]))
    top_level_labels = [child.label for child in M.build_assembly().children]
    checks = [
        ("concept_a_track", M.TRACK == 170.0, {"actual_mm": M.TRACK}),
        ("wheel_geometry_mirrors_about_centerline", abs(wheel_l_y + wheel_r_y) < 1e-9, {"left_center_y_mm": wheel_l_y, "right_center_y_mm": wheel_r_y}),
        ("wheel_geometry_track_is_170", abs((wheel_l_y - wheel_r_y) - M.TRACK) < 1e-9, {"measured_track_mm": wheel_l_y - wheel_r_y}),
        ("loaded_radius_matches_axle_height", M.WHEEL_OD / 2.0 == M.AXLE_Z, {"radius_mm": M.WHEEL_OD / 2.0, "axle_z_mm": M.AXLE_Z}),
        ("wheel_well_has_radial_clearance", M.WHEEL_WELL_RADIAL_CLEARANCE >= 3.0, {"radial_clearance_mm": M.WHEEL_WELL_RADIAL_CLEARANCE}),
        ("wheel_running_clearance_to_static_parts", all(v["min_gap_mm"] >= M.WHEEL_RUNNING_CLEARANCE_MIN - 1e-6 for v in wheel_clearance.values()), {"minimum_mm": M.WHEEL_RUNNING_CLEARANCE_MIN, "sides": wheel_clearance}),
        ("drivetrain_static_parts_do_not_interfere", not drivetrain_clashes, {"clashes_mm3": drivetrain_clashes}),
        ("motor_face_seats_on_axle_flange", all(v["gap_mm"] < 1e-6 and v["overlap_mm3"] < 1e-3 for v in flange_seat.values()), flange_seat),
        ("motor_face_joint_is_engaged", all(v["screw_count"] == 2 and all(e >= 2.5 for e in v["thread_engaged_in_faceplate_mm"]) and all(i <= v["hole_depth_mm"] - 0.5 for i in v["screw_insertion_mm"]) and v["shaft_engaged_in_stub_mm"] >= 8.0 and v["shaft_stub_overlap_mm3"] < 1e-3 and v["screw_head_to_inner_bearing_mm"] >= 0.4 for v in motor_joint.values()), {"sides": motor_joint, "rule": "M3 thread in the tapped faceplate >= 2.5 mm, insertion <= hole depth - 0.5; shaft >= 8 mm in the stub; heads >= 0.4 mm off the bearing"}),
        ("bearings_sit_inside_flange_boss", all(bearings_in_boss.values()), {"bearings": bearings_in_boss, "boss_end_y_mm": M.AXLE_BOSS_END_Y}),
        ("battery_pack_fits_tub_with_retention_gap", all(v >= 0.4 for k, v in battery_tub_margin.items() if k != "floor_z_mm") and -1e-6 <= battery_tub_margin["floor_z_mm"] <= M.BATTERY_WRAP_T + 1e-6, battery_tub_margin),
        ("ballast_bar_is_clear_and_seated", not ballast_clashes and ballast_gaps["tub_front_wall_mm"] >= 0.5 and ballast_gaps["front_crossmember_mm"] >= 0.5 and abs(ballast_gaps["deck_underside_mm"]) < 1e-6, {"clashes_mm3": ballast_clashes, "gaps": ballast_gaps, "mass_g": round(M.BALLAST_BAR_G + M.BALLAST_SCREWS_G, 1)}),
        ("battery_pack_is_2s1p_18650", sum("BATTERY_CELL_" in p.label for p in battery_parts) == 2 and any("BMS" in p.label for p in battery_parts), {"parts": [p.label for p in battery_parts]}),
        ("battery_tub_is_clear", not battery_clashes and not tub_shell_overlap, {"battery_center_mm": M.BATTERY_CENTER, "battery_size_mm": M.BATTERY_SIZE, "clashes_mm3": battery_clashes, "tub_vs_shell_mm3": tub_shell_overlap}),
        ("ball_transfer_is_frozen_default", M.BALL_CONTACT == (110.0, 0.0, 0.0), {"contact_mm": M.BALL_CONTACT}),
        ("ball_mount_is_fixed_not_interchangeable", M.BALL_MOUNT_MODE == "FIXED_3HOLE_NON_INTERCHANGEABLE", {"mount_mode": M.BALL_MOUNT_MODE}),
        ("ball_flange_seats_on_pod", ball_seat["gap_mm"] < 1e-6 and ball_seat["overlap_mm3"] < 1e-3 and abs(ball_seat["flange_top_z_mm"] - M.BALL_NATIVE_HEIGHT) < 1e-6, ball_seat),
        ("ball_article_stack_is_connected", all(gap < 1e-6 for gap in ball_stack_gaps.values()), ball_stack_gaps),
        ("ball_screws_engage_flange", len(ball_screw_engagement) == 3 and all(depth >= 2.5 for depth in ball_screw_engagement.values()), {"thread_engagement_mm": ball_screw_engagement}),
        ("ball_nose_parts_do_not_interfere", not nose_clashes, {"clashes_mm3": nose_clashes}),
        ("touch_cap_travel_reserve_is_clear", not travel_blockers, {"blockers_mm3": travel_blockers, "travel_mm": M.TACTILE_NOSE_TRAVEL}),
        ("rigid_nose_stays_behind_cap_travel", rigid_front_x <= M.TACTILE_CAP_INNER_X - M.TACTILE_NOSE_TRAVEL + 1e-6, {"rigid_front_x_mm": round(rigid_front_x, 3), "cap_inner_x_mm": M.TACTILE_CAP_INNER_X}),
        ("touch_cap_stops_at_pod_seat", abs(touch_cap.bounding_box().min.Z - M.BALL_POD_Z0) < 1e-3, {"cap_bottom_z_mm": round(touch_cap.bounding_box().min.Z, 3), "pod_seat_z_mm": M.BALL_POD_Z0, "housing_bottom_z_mm": round(housing.bounding_box().min.Z, 3)}),
        ("c12_low_object_contact_not_claimed", c12_first_label != "BALL_NOSE_TOUCH_CAP", {"first_contact": c12_first_label, "hit_face_x_mm": c12_first}),
        ("front_range_sensor_on_centreline", abs(M.FRONT_RANGE_SENSOR_Y) < 1e-9, {"sensor_y_mm": M.FRONT_RANGE_SENSOR_Y}),
        ("front_range_face_ahead_of_ball_contact", face_ahead > 0.0, {"face_x_mm": M.FRONT_RANGE_SENSOR_FACE_X, "ball_contact_x_mm": M.BALL_CONTACT[0], "credited_mm": face_ahead}),
        ("front_range_lookahead_within_rated_range", lookahead_ok, {"rated_max_mm": M.FRONT_RANGE_MAX_MM, "cases": lookahead}),
        ("ball_pod_passes_shell_notch", not pod_shell_overlap, {"overlap_mm3": pod_shell_overlap}),
        ("front_chassis_stays_inside_shell", chassis_front_x <= M.BODY_X_FRONT - M.SHELL_THICKNESS, {"chassis_front_x_mm": round(chassis_front_x, 3), "shell_inner_front_x_mm": M.BODY_X_FRONT - M.SHELL_THICKNESS}),
        ("ball_nose_is_lean", nose_width <= 42.0, {"nose_width_mm": round(nose_width, 2), "previous_shroud_width_mm": 52.0, "nose_front_x_mm": round(nose_front_x, 2), "spin_radius_mm": round(nose_spin_radius, 2)}),
        ("rp01_yaw_transform_closes", all(abs(transformed_yaw[i] - M.HEAD_YAW_DATUM[i]) < 1e-9 for i in range(3)), {"transformed_mm": transformed_yaw, "datum_mm": M.HEAD_YAW_DATUM}),
        ("body_frame_has_four_m4_mounts", len(M.BODY_MOUNT_POINTS) == 4, {"mount_points_mm": M.BODY_MOUNT_POINTS}),
        ("body_frame_has_two_locating_pins", len(M.BODY_LOCATING_POINTS) == 2, {"locating_points_mm": M.BODY_LOCATING_POINTS}),
        ("body_frame_no_longer_interpenetrates_chassis", frame_chassis_overlap < 1e-3, {"overlap_volume_mm3": frame_chassis_overlap}),
        ("body_mount_hardware_is_separate_top_level_group", "BODY_CHASSIS_MOUNT_HARDWARE" in top_level_labels, {"top_level_labels": top_level_labels}),
        ("panel_openings_have_continuous_overlap", all(abs(width - M.PANEL_OVERLAP) < 0.02 for width in panel_land_mm.values()), {"measured_land_mm": panel_land_mm, "target_mm": M.PANEL_OVERLAP}),
        ("front_panel_edges_parallel_front_shell_edges", abs(panel_edge_angle_deg["FRONT"]["panel"] - panel_edge_angle_deg["FRONT"]["shell"]) < 0.01, {"measured_edge_angle_deg": panel_edge_angle_deg["FRONT"], "panel_widths_mm": [M.FRONT_PANEL_BOTTOM_WIDTH, round(M.FRONT_PANEL_TOP_WIDTH, 3)]}),
        ("rear_panel_edges_parallel_rear_shell_edges", abs(panel_edge_angle_deg["REAR"]["panel"] - panel_edge_angle_deg["REAR"]["shell"]) < 0.01, {"measured_edge_angle_deg": panel_edge_angle_deg["REAR"], "panel_widths_mm": [M.REAR_PANEL_BOTTOM_WIDTH, round(M.REAR_PANEL_TOP_WIDTH, 3)]}),
        ("panel_fasteners_sit_inside_boss_inset", all(inset >= M.PANEL_FASTENER_MIN_INSET - 1e-6 for insets in fastener_insets.values() for inset in insets), {"inset_to_panel_edge_mm": fastener_insets, "minimum_mm": M.PANEL_FASTENER_MIN_INSET}),
        ("panel_frames_are_closed_rings_with_fused_bosses", all(r["solids"] == 1 and r["bottom_bar"] and r["top_bar"] for r in frame_rings.values()), {"frames": frame_rings}),
        ("panel_area_parts_do_not_interfere", not panel_clashes, {"clashes_mm3": panel_clashes}),
        ("front_range_sensor_has_clear_window", range_window_blockage < 1e-3, {"blocked_volume_mm3": round(range_window_blockage, 3), "sensor_face_mm": [M.FRONT_RANGE_SENSOR_FACE_X, M.FRONT_RANGE_SENSOR_Y, M.FRONT_RANGE_SENSOR_Z]}),
        ("front_panel_lifts_off_forward", not front_removal_blockers, {"blockers_mm3": front_removal_blockers, "panel_bottom_z_mm": M.FRONT_PANEL_Z0}),
        ("service_panels_repeat_eight_sided_shell_profile", M.PANEL_LOWER_CORNER > 0.0 and M.PANEL_UPPER_CORNER > 0.0, {"panel_vertex_count": 8, "lower_corner_mm": M.PANEL_LOWER_CORNER, "upper_corner_mm": M.PANEL_UPPER_CORNER}),
        ("front_and_rear_panels_have_four_fasteners_each", len(M.FRONT_PANEL_FASTENERS) == 4 and len(M.REAR_PANEL_FASTENERS) == 4, {"front_count": len(M.FRONT_PANEL_FASTENERS), "rear_count": len(M.REAR_PANEL_FASTENERS)}),
        ("panel_hardware_is_separate_top_level_group", "PANEL_MOUNT_HARDWARE" in top_level_labels, {"top_level_labels": top_level_labels}),
        ("body_audio_is_separate_top_level_group", "BODY_AUDIO" in top_level_labels, {"top_level_labels": top_level_labels}),
        ("four_body_microphones_are_allocated", len(M.MICROPHONE_PORTS) == 4, {"microphone_ports": M.MICROPHONE_PORTS}),
        ("speaker_and_front_range_sensor_do_not_overlap", audio_sensor_overlap < 1e-3, {"overlap_volume_mm3": audio_sensor_overlap}),
        ("selected_audio_and_imu_parts_are_clear", not selected_clashes and not selected_self_clashes, {"clashes_mm3": selected_clashes, "self_clashes_mm3": selected_self_clashes, "harness_volume_overlaps_OPEN_mm3": selected_harness_overlaps, "parts": len(selected_parts)}),
        ("speaker_is_k50wp_outline_behind_front_panel", abs(speaker_outline["depth_mm"] - 18.0) < 0.01 and abs(speaker_outline["diameter_mm"] - 50.0) < 0.01 and M.BODY_X_FRONT - speaker_box.max.X >= 0.4, speaker_outline),
        ("mic_packages_on_port_axes_against_boots", all(v["package_off_axis_mm"] < 0.01 and abs(v["board_outer_abs_y_mm"] - M.MIC_BOARD_OUTER_Y) < 0.01 for v in mic_axis.values()), mic_axis),
        ("imu_board_seated_on_deck_with_both_screws_in_material", abs(imu_seat["board_bottom_z_mm"] - imu_seat["deck_top_z_mm"]) < 0.01 and imu_seat["board_vs_deck_mm3"] < 1e-3 and all(v >= 0.95 * math.pi * 1.0 ** 2 * 4.0 for v in imu_seat["shank_in_deck_mm3"].values()), imu_seat),
        ("head_sweep_floor_clears_disc_top", M.HEAD_SWEEP_FLOOR_Z - M.YAW_DISC_TOP_Z >= 4.0 - 1e-9, {"sweep_floor_z_mm": M.HEAD_SWEEP_FLOOR_Z, "disc_top_z_mm": M.YAW_DISC_TOP_Z}),
        ("hard_stops_alone_keep_head_off_disc", M.HEAD_ENVELOPE["hard_stops_alone_keep_4mm"] and M.HEAD_ENVELOPE["overtravel_1deg_case"]["clearance_to_disc_top_mm"] >= 2.0, {"hard_stop_corner": M.HEAD_ENVELOPE["hard_stop_fault_case"], "overtravel_1deg": M.HEAD_ENVELOPE["overtravel_1deg_case"]}),
        ("head_motion_is_full_range_to_hard_stops", all(r["roll_min_deg"] == M.HEAD_ENVELOPE["hard_stops"]["roll_deg"][0] and r["roll_max_deg"] == M.HEAD_ENVELOPE["hard_stops"]["roll_deg"][1] for r in M.HEAD_ENVELOPE["rows"]), {"rows": len(M.HEAD_ENVELOPE["rows"]), "hard_stops": M.HEAD_ENVELOPE["hard_stops"], "usable_travel": M.HEAD_ENVELOPE["usable_travel"]}),
        ("pi_cooler_headroom_kept", cooler_headroom_clash < 1e-3, {"headroom_mm": M.PI_COOLER_HEADROOM, "yaw_parts_in_headroom_mm3": cooler_headroom_clash}),
        ("yaw_disc_fits_flat_body_top", M.YAW_DISC_RADIUS <= M.BODY_WIDTH_UPPER / 2.0 - 10.0, {"disc_radius_mm": M.YAW_DISC_RADIUS, "flat_top_half_width_mm": M.BODY_WIDTH_UPPER / 2.0 - 10.0}),
        ("yaw_stage_clears_frame_electronics_shell", yaw_clash < 1e-3, {"overlap_volume_mm3": yaw_clash}),
        ("yaw_disc_rim_has_running_gap", M.YAW_DISC_TOP_Z - M.YAW_DISC_THICKNESS - M.BODY_Z_TOP >= 1.0 - 1e-9, {"disc_rim_bottom_z_mm": M.YAW_DISC_TOP_Z - M.YAW_DISC_THICKNESS, "body_top_z_mm": M.BODY_Z_TOP}),
        ("yaw_spur_pair_meshes_1to1", abs(math.hypot(*M.YAW_PINION_CENTER) - 2.0 * M.YAW_GEAR_PITCH_RADIUS) < 1e-9 and M.YAW_GEAR_RATIO == 1.0, {"centre_distance_mm": math.hypot(*M.YAW_PINION_CENTER), "ratio": M.YAW_GEAR_RATIO}),
        ("yaw_pinion_is_lash_free_scissor_gear", (
            abs(M.YAW_GEAR_MODULE * M.YAW_GEAR_TEETH - 2.0 * M.YAW_GEAR_PITCH_RADIUS) < 1e-9
            and abs(2.0 * M.YAW_SCISSOR_HALF_FACE + M.YAW_SCISSOR_GAP - (M.YAW_DISC_PLATE_BOTTOM_Z - M.YAW_BEARING_Z[1] - 1.0)) < 1e-9
            and M.YAW_SCISSOR_PRELOAD_NM >= 1.5 * M.YAW_PEAK_EXTERNAL_TORQUE_NM
            and {"YAW_DRIVE_SCISSOR_PINION_FIXED_HALF", "YAW_DRIVE_SCISSOR_PINION_SPRUNG_HALF"} <= {c.label for c in M.body_yaw_stage().children}
        ), {"module": M.YAW_GEAR_MODULE, "teeth": M.YAW_GEAR_TEETH, "half_face_mm": M.YAW_SCISSOR_HALF_FACE, "gap_mm": M.YAW_SCISSOR_GAP,
            "preload_nm": M.YAW_SCISSOR_PRELOAD_NM, "peak_external_nm": round(M.YAW_PEAK_EXTERNAL_TORQUE_NM, 4),
            "servo_current_limit_torque_nm": round(M.YAW_SERVO_CURRENT_LIMIT_TORQUE_NM, 3)}),
        ("yaw_servo_speed_covers_peak_yaw_at_3v7", M.YAW_SERVO_NO_LOAD_RPM["3.7V"] / M.YAW_GEAR_RATIO >= 1.3 * M.YAW_PEAK_OUTPUT_RPM, {"output_no_load_rpm": {k: v / M.YAW_GEAR_RATIO for k, v in M.YAW_SERVO_NO_LOAD_RPM.items()}, "peak_output_rpm": M.YAW_PEAK_OUTPUT_RPM, "required_margin": 1.3}),
        ("body_fits_track_width", M.BODY_WIDTH_LOWER < M.TRACK + M.WHEEL_WIDTH, {"body_width_mm": M.BODY_WIDTH_LOWER, "wheel_stance_mm": M.TRACK + M.WHEEL_WIDTH}),
        ("body_ground_clearance_in_baseline_band", 25.0 <= M.BODY_Z_BOTTOM <= 35.0, {"body_bottom_mm": M.BODY_Z_BOTTOM, "target_mm": [25.0, 35.0]}),
        ("visible_body_height_in_baseline_band", 105.0 <= M.BODY_Z_TOP - M.BODY_Z_BOTTOM <= 115.0, {"body_height_mm": M.BODY_Z_TOP - M.BODY_Z_BOTTOM, "target_mm": [105.0, 115.0]}),
        ("neutral_stack_is_documented_293p5_mm", abs(M.OVERALL_PHYSICAL_HEIGHT - 293.5) < 1e-9, {"overall_height_mm": M.OVERALL_PHYSICAL_HEIGHT, "rounded_target_mm": 300.0}),
        ("neck_allocation_is_49p5_mm", abs(M.NECK_ALLOCATION - 49.5) < 1e-9, {"neck_allocation_mm": M.NECK_ALLOCATION}),
        ("rear_tcrt_is_only_cliff_channel", M.TCRT_CHANNELS == ("REAR",), {"channels": M.TCRT_CHANNELS}),
        ("rear_tcrt_has_contact_lookahead", M.SKID_PAD_CENTER[0] - M.TCRT_REAR_CENTER[0] >= M.TCRT_REAR_LOOKAHEAD, {"sensor_x_mm": M.TCRT_REAR_CENTER[0], "skid_contact_x_mm": M.SKID_PAD_CENTER[0], "lookahead_mm": M.SKID_PAD_CENTER[0] - M.TCRT_REAR_CENTER[0]}),
        ("rear_tcrt_optical_face_matches_raised_datum", abs(M.TCRT_REAR_CENTER[2] - M.TCRT_PACKAGE_SIZE[2] / 2.0 - M.TCRT_OPTICAL_FACE_Z) < 1e-9 and M.TCRT_OPTICAL_FACE_Z == 10.0, {"optical_face_z_mm": M.TCRT_OPTICAL_FACE_Z}),
        ("rear_tcrt_lookahead_remains_bounded", 25.0 <= M.TCRT_REAR_LOOKAHEAD <= 30.0, {"lookahead_mm": M.TCRT_REAR_LOOKAHEAD}),
        ("tcrt_guard_is_lower_than_optical_face", 0.0 < M.TCRT_GUARD_BOTTOM_Z < M.TCRT_OPTICAL_FACE_Z, {"guard_bottom_z_mm": M.TCRT_GUARD_BOTTOM_Z, "optical_face_z_mm": M.TCRT_OPTICAL_FACE_Z}),
        ("rear_pitch_contact_order_is_shoe_guard_keel_sensor", pitch["shoe"] < pitch["guards"] < min(pitch["keel_body"], pitch["tcrt"]), {"first_contact_pitch_deg": pitch}),
        ("rear_keel_seats_on_crossmember_without_interference", keel_crossmember_overlap < 1e-6 and keel_crossmember_gap < 1e-6, {"overlap_volume_mm3": keel_crossmember_overlap, "gap_mm": keel_crossmember_gap}),
        ("rear_keel_bolted_with_four_m3", len(keel_hardware.children) == 8, {"hardware_solids": len(keel_hardware.children)}),
        ("rear_keel_shoe_fully_backed", all(z is not None and abs(z - shoe_top_z) < 1e-3 for z in shoe_backing.values()), {"shoe_top_z_mm": shoe_top_z, "keel_underside_z_mm": shoe_backing}),
        ("rear_keel_guards_seated_full_length", all(z is not None and z < guard_top_z for z in guard_backing.values()), {"guard_top_z_mm": guard_top_z, "keel_underside_z_mm": guard_backing}),
        ("rear_tcrt_package_clears_keel", tcrt_keel_collision < 1e-6, {"collision_volume_mm3": tcrt_keel_collision}),
        ("rear_keel_passes_shell_floor_slot", keel_shell_overlap < 1e-6, {"overlap_volume_mm3": keel_shell_overlap}),
        ("rear_tail_parked_out_of_assembly", M.REAR_TAIL_ENABLED or ("REAR_TAIL_STINGER" not in module_labels and all(row[0] != "REAR_TAIL_STINGER" for row in M.MASS_ROWS)), {"enabled": M.REAR_TAIL_ENABLED, "module_children": module_labels}),
        ("rear_keel_is_translucent_ivory", M.REAR_KEEL_COLOR == M.IVORY and M.REAR_KEEL_ALPHA < 0.5, {"color": M.REAR_KEEL_COLOR, "alpha": M.REAR_KEEL_ALPHA}),
        ("rear_tail_is_faceted_telescoping_stinger", M.REAR_TAIL_STYLE == "FACETED_TELESCOPING_STINGER" and len(tail_segments.children) == len(M.REAR_TAIL_JOINTS), {"style": M.REAR_TAIL_STYLE, "segment_labels": [child.label for child in tail_segments.children]}),
        ("rear_tail_sweeps_progressively_upward", all(0.0 < a < b < 90.0 for a, b in zip(tail_rise_deg, tail_rise_deg[1:])), {"segment_rise_deg": tail_rise_deg}),
        ("rear_tail_segments_telescope", all(end > nxt[0] for (_start, end), nxt in zip(tail_sizes, tail_sizes[1:])), {"segment_start_end_widths_mm": [[round(a, 2), round(b, 2)] for a, b in tail_sizes]}),
        ("rear_tail_tip_is_blunt_chisel", min(M.REAR_TAIL_TIP_SECTION) >= 2.0, {"tip_section_w_h_mm": M.REAR_TAIL_TIP_SECTION}),
        ("rear_tail_inside_nose_spin_circle", tail_spin_radius <= nose_spin_radius, {"tail_planar_radius_mm": round(tail_spin_radius, 2), "nose_planar_radius_mm": round(nose_spin_radius, 2)}),
        ("rear_tail_below_body_top", tail_bbox.max.Z <= M.BODY_Z_TOP - 10.0, {"tail_max_z_mm": round(tail_bbox.max.Z, 2), "limit_z_mm": M.BODY_Z_TOP - 10.0}),
        ("rear_tail_clears_shell_and_panels", tail_shell_overlap < 1e-6 and tail_panel_overlap < 1e-6, {"shell_overlap_mm3": tail_shell_overlap, "panel_overlap_mm3": tail_panel_overlap}),
        ("rear_tail_stays_above_body_ground_clearance", tail_bbox.min.Z > M.BODY_Z_BOTTOM, {"tail_min_z_mm": tail_bbox.min.Z, "body_bottom_z_mm": M.BODY_Z_BOTTOM}),
        ("rear_tail_root_has_four_hidden_m3", len(M.rear_tail_root_screw_points()) == 4 and all(head.bounding_box().min.X > M.BODY_X_REAR for head in tail_head_parts), {"screw_points_y_z_mm": M.rear_tail_root_screw_points(), "head_min_x_mm": [round(head.bounding_box().min.X, 2) for head in tail_head_parts]}),
        ("rear_tail_uses_head_ivory", M.REAR_TAIL_VISIBLE_COLOR == M.IVORY, {"tail_color": M.REAR_TAIL_VISIBLE_COLOR, "head_palette_ivory": M.IVORY}),
        ("rear_skid_tcrt_is_separate_top_level_group", "REAR_SKID_TCRT_MODULE" in top_level_labels, {"top_level_labels": top_level_labels}),
        ("tactile_nose_precedes_ball_surface", M.TACTILE_NOSE_FACE_X > M.BALL_CONTACT[0] + M.BALL_DIAMETER / 2.0, {"tactile_face_x_mm": M.TACTILE_NOSE_FACE_X, "ball_front_x_mm": M.BALL_CONTACT[0] + M.BALL_DIAMETER / 2.0}),
        ("tactile_nose_has_bounded_travel", 2.0 <= M.TACTILE_NOSE_TRAVEL <= 4.0, {"travel_mm": M.TACTILE_NOSE_TRAVEL}),
        ("battery_forward_of_axle", M.BATTERY_CENTER[0] > 0.0, {"battery_x_mm": M.BATTERY_CENTER[0]}),
        ("power_boards_are_in_the_electronics_group", {c.label for c in power_group.children} >= {"PCB02_CHARGE_AND_SYSTEM_POWER", "PCB03_MOTOR_GATE_AND_HEAD_RAIL", "PCB04_BRANCH_CONVERTERS", "PACK_ATOF_FUSE_HOLDER_ENVELOPE", "ESTOP_XA1E_BV3U02KT_R"} and not any(c.label in ("POWER_DISTRIBUTION_RP02_ENVELOPE", "SAFETY_AND_WATCHDOG_ENVELOPE") for c in M.electronics().children), {"children": [c.label for c in power_group.children], "proposal": "RP-02 board-specs.md sec 2, 2026-09-25"}),
        ("power_boards_clear_of_all_real_hardware", not power_clashes, {"clashes_mm3": power_clashes, "checked_against": len(power_hardware), "keep_outs_included": True}),
        ("power_boards_do_not_interfere_with_each_other", not power_self_clashes, {"clashes_mm3": power_self_clashes}),
        ("power_boards_keep_running_gaps", all(v["nearest_mm"] >= 0.4 for v in power_gaps.values()), {"minimum_mm": 0.4, "nearest": power_gaps}),
        ("power_bay_gaps_are_about_1mm_and_have_no_slack", all(v >= 0.89 for v in bay_gaps.values()) and abs(bay_gaps["pcb04_to_pcb03_mm"] - 1.0) < 1e-6, {"gaps": bay_gaps, "note": "PCB-03 and PCB-04 use the whole free band under the tray: 44 + 1 + 41 mm between the lower cross-members; a larger board or the 3.3 mF hold-up footprint needs a different bay"}),
        ("power_boards_clear_of_harness_power_routes", not power_harness_overlaps, {"overlaps_mm3": power_harness_overlaps, "note": "HARNESS_BATTERY_TRUNK (Y +18, Z 57.5-62.5) and HARNESS_MOTOR_BRANCH (X 30-42, Z 56.5-62.5) run in the 7 mm slot under PCB-03/04 (Z 56-63) and clear the IMU; still route-volume placeholders, not a wire-by-wire harness"}),
        ("power_board_footprints_recorded", footprints["PCB03_mm2"] >= 2460.0 - 1.0 and footprints["PCB04_mm2"] >= 3080.0 - 1.0, {"footprints": footprints, "source": "WS-H estimates from the part inventory; nothing is laid out"}),
        ("estop_operator_is_outside_the_rear_panel_and_keep_out_clears_the_pi", estop_geometry["head_max_x_mm"] <= M.ESTOP_REAR_OUTER_X + 1e-6 and estop_geometry["head_z_mm"][1] <= estop_geometry["rear_panel_top_z_mm"] and estop_geometry["head_vs_panel_mm3"] < 1e-3 and estop_geometry["well_vs_frame_mm3"] < 1e-3 and estop_geometry["keep_out_vs_pcb02_mm3"] < 1e-3, estop_geometry),
        ("pcb01_replaces_generic_bms_at_2p9mm", abs(pcb01.bounding_box().size.Z - 2.9) < 1e-6 and abs(pcb01.bounding_box().size.X - 20.0) < 1e-6 and abs(pcb01.bounding_box().size.Y - 48.0) < 1e-6, {"pcb01_size_mm": [round(pcb01.bounding_box().size.X, 3), round(pcb01.bounding_box().size.Y, 3), round(pcb01.bounding_box().size.Z, 3)], "previous_bms_mm": [20.0, 48.0, 4.5]}),
        ("control_power_sensors_row_replaced_by_board_rows", "CONTROL_POWER_SENSORS" not in mass_by_id and all(i in mass_by_id for i in power_mass_ids) and "ESTOP_XA1E_BV3U02KT_R" in mass_by_id, {"replaced_rows_g": replaced_row_g, "removed_row_g": 121.5, "estop_g": mass_by_id["ESTOP_XA1E_BV3U02KT_R"], "battery_g": mass_by_id["BATTERY"], "total_mass_g": round(M.mass_properties()["mass_g"], 1), "note": "hand-kept register: masses are RP-02 estimates, not derived from the solids"}),
        ("head_source_exists", (M.HEAD_DIR / "layout_model.py").exists(), {"path": str(M.HEAD_DIR / "layout_model.py")}),
        ("pi_step_exists", (M.PURCHASED / "raspberry_pi_5.step").exists(), {"path": str(M.PURCHASED / "raspberry_pi_5.step")}),
        ("bearing_step_exists", (M.PURCHASED / "bearing_608zz.step").exists(), {"path": str(M.PURCHASED / "bearing_608zz.step")}),
        ("com_inside_support_x", 0.0 < M.mass_properties()["com_mm"][0] < M.BALL_CONTACT[0], {"com_x_mm": M.mass_properties()["com_mm"][0]}),
        ("com_forward_of_physics_margin_line", a_tip >= PHYSICS_MARGIN_A_TIP_MIN, {"com_x_mm": round(com[0], 2), "com_h_mm": round(com[2], 2), "x_over_h": round(com_ratio, 4), "a_tip_m_s2": round(a_tip, 3), "a_tip_min_m_s2": round(PHYSICS_MARGIN_A_TIP_MIN, 3), "equivalent_min_x_mm_at_this_h": round(PHYSICS_MARGIN_A_TIP_MIN * com[2] / 9.81, 2), "margin_over_a_peak_1p00": round(a_tip / 1.00, 3), "baseline_target": {"x_mm": 25.0, "h_mm": 124.0, "x_over_h": 0.202}, "body_shift_x_mm": M.BODY_SHIFT_X, "rule": "RP-03 physics.md 2.5 margin is a_tip = g*x/h against a_peak 0.80-1.00 m/s2. The +20 mm line is that margin evaluated at h = 124 mm (a_tip 1.582); it is re-based 2026-09-25 (builder acceptance BA-06, decision RP03-CAD-09) to the same a_tip because the register CoM height is now about 105 mm. Neutral head only; head-pose corners are in RP03-CAD-09"}),
        ("ball_share_above_spin_walk_flag", ball_share >= 0.09, {"ball_share": round(ball_share, 4), "flag_below": 0.09}),
        ("rear_skid_catches_before_com_crosses_axle", pitch["shoe"] < com_cross_pitch_deg, {"shoe_first_contact_pitch_deg": pitch["shoe"], "com_over_axle_pitch_deg": round(com_cross_pitch_deg, 3)}),
        ("com_below_head_yaw", M.mass_properties()["com_mm"][2] < M.HEAD_YAW_DATUM[2], {"com_z_mm": M.mass_properties()["com_mm"][2]}),
    ]
    payload = {
        "layout_id": M.LAYOUT_ID,
        "ok": all(row[1] for row in checks),
        "checks": [{"name": name, "ok": ok, "evidence": evidence} for name, ok, evidence in checks],
    }
    out = HERE / "generated"
    out.mkdir(parents=True, exist_ok=True)
    (out / "checks.json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = ["# RP-03 Layout 02 deterministic checks", ""]
    lines.extend(f"- [{'x' if ok else ' '}] `{name}` — {evidence}" for name, ok, evidence in checks)
    (out / "checks.md").write_text("\n".join(lines) + "\n")
    if not payload["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
