"""Deterministic source-level checks for RP-03 integrated Layout 02."""

from __future__ import annotations

import json
import math
from pathlib import Path

from build123d import Axis, Compound, GeomType, Location, Vertex

import body_chassis_model as M

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
    panel_parts = [*body_panels.children[:3], *panel_hardware.children]
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
                volume = _vol(part & other)
                if volume > 1e-3:
                    drivetrain_clashes[f"{part.label} x {other.label}"] = round(volume, 3)
        gearbox = next(c for c in motor_solids if c.label.endswith("GEARBOX"))
        flange = by_label(chassis_static, f"AXLE_MOTOR_FLANGE_BEARING_BOSS_{side}")
        flange_seat[side] = {"gap_mm": round(gearbox.distance_to(flange), 4), "overlap_mm3": round(_vol(gearbox & flange), 4)}
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
        ("head_sweep_floor_clears_disc_top", M.HEAD_SWEEP_FLOOR_Z - M.YAW_DISC_TOP_Z >= 4.0 - 1e-9, {"sweep_floor_z_mm": M.HEAD_SWEEP_FLOOR_Z, "disc_top_z_mm": M.YAW_DISC_TOP_Z}),
        ("hard_stops_alone_keep_head_off_disc", M.HEAD_ENVELOPE["hard_stops_alone_keep_4mm"] and M.HEAD_ENVELOPE["overtravel_1deg_case"]["clearance_to_disc_top_mm"] >= 2.0, {"hard_stop_corner": M.HEAD_ENVELOPE["hard_stop_fault_case"], "overtravel_1deg": M.HEAD_ENVELOPE["overtravel_1deg_case"]}),
        ("head_motion_is_full_range_to_hard_stops", all(r["roll_min_deg"] == M.HEAD_ENVELOPE["hard_stops"]["roll_deg"][0] and r["roll_max_deg"] == M.HEAD_ENVELOPE["hard_stops"]["roll_deg"][1] for r in M.HEAD_ENVELOPE["rows"]), {"rows": len(M.HEAD_ENVELOPE["rows"]), "hard_stops": M.HEAD_ENVELOPE["hard_stops"], "usable_travel": M.HEAD_ENVELOPE["usable_travel"]}),
        ("pi_cooler_headroom_kept", cooler_headroom_clash < 1e-3, {"headroom_mm": M.PI_COOLER_HEADROOM, "yaw_parts_in_headroom_mm3": cooler_headroom_clash}),
        ("yaw_disc_fits_flat_body_top", M.YAW_DISC_RADIUS <= M.BODY_WIDTH_UPPER / 2.0 - 10.0, {"disc_radius_mm": M.YAW_DISC_RADIUS, "flat_top_half_width_mm": M.BODY_WIDTH_UPPER / 2.0 - 10.0}),
        ("yaw_stage_clears_frame_electronics_shell", yaw_clash < 1e-3, {"overlap_volume_mm3": yaw_clash}),
        ("yaw_disc_rim_has_running_gap", M.YAW_DISC_TOP_Z - M.YAW_DISC_THICKNESS - M.BODY_Z_TOP >= 1.0 - 1e-9, {"disc_rim_bottom_z_mm": M.YAW_DISC_TOP_Z - M.YAW_DISC_THICKNESS, "body_top_z_mm": M.BODY_Z_TOP}),
        ("yaw_spur_pair_meshes_1to1", abs(math.hypot(*M.YAW_PINION_CENTER) - 2.0 * M.YAW_GEAR_PITCH_RADIUS) < 1e-9 and M.YAW_GEAR_RATIO == 1.0, {"centre_distance_mm": math.hypot(*M.YAW_PINION_CENTER), "ratio": M.YAW_GEAR_RATIO}),
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
        ("head_source_exists", (M.HEAD_DIR / "layout_model.py").exists(), {"path": str(M.HEAD_DIR / "layout_model.py")}),
        ("pi_step_exists", (M.PURCHASED / "raspberry_pi_5.step").exists(), {"path": str(M.PURCHASED / "raspberry_pi_5.step")}),
        ("bearing_step_exists", (M.PURCHASED / "bearing_608zz.step").exists(), {"path": str(M.PURCHASED / "bearing_608zz.step")}),
        ("com_inside_support_x", 0.0 < M.mass_properties()["com_mm"][0] < M.BALL_CONTACT[0], {"com_x_mm": M.mass_properties()["com_mm"][0]}),
        ("com_forward_of_physics_margin_line", com[0] >= 20.0, {"com_x_mm": round(com[0], 2), "com_h_mm": round(com[2], 2), "x_over_h": round(com_ratio, 4), "a_tip_m_s2": round(a_tip, 3), "baseline_target": {"x_mm": 25.0, "h_mm": 124.0, "x_over_h": 0.202}, "body_shift_x_mm": M.BODY_SHIFT_X, "rule": "RP-03 physics.md 2.5: a_peak 0.80-1.00 m/s2 has margin only when x_CoM >= +20 mm"}),
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
