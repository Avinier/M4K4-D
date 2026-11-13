"""Nominal, visible head cable solids in the head-local neutral pose.

The source harness schedule and D-104/D-105 routes define these paths.  These
are cable bodies for visual assembly review, separate from the larger HARNESS_*
clearance volumes.  Connector dress and the exact wire split still need a
physical fit on the assembled head.
"""

from build123d import Box, Compound, Location, Plane, Solid, Sphere, Vector


def _wire(points, radius):
    """A round insulated conductor with connected, rounded bends."""
    pieces = []
    for a, b in zip(points, points[1:]):
        start, end = Vector(*a), Vector(*b)
        delta = end - start
        pieces.append(Solid.make_cylinder(radius, delta.length,
                                          Plane(origin=start, z_dir=delta)))
    pieces += [Sphere(radius).moved(Location(p)) for p in points[1:-1]]
    return Compound(children=pieces)


def _ribbon_segment(a, b, width_axis, width, thickness=0.3):
    """A flat FFC segment; the width direction is explicit at every fold."""
    start, end = Vector(*a), Vector(*b)
    along = (end - start).normalized()
    across = Vector(*width_axis).normalized()
    normal = along.cross(across).normalized()
    mid = (start + end) * 0.5
    return Box((end - start).length, width, thickness).moved(
        Plane(origin=mid, x_dir=along, z_dir=normal).location)


def _ribbon(points, width_axis, width):
    return Compound(children=[_ribbon_segment(a, b, width_axis, width)
                              for a, b in zip(points, points[1:])])


def build_head_harness(entry):
    """One switchable Harness / Head wires group, in the head-local frame."""
    paint = entry._tag
    px, pz = entry.layout_model.PITCH_X, entry.layout_model.PITCH_Z

    # D-104: two insulated AWG24 power conductors and eleven AWG30 signal
    # conductors.  Two rows fill the documented 6.0 x 2.2 mm bundle envelope.
    # Each core is shown through the disc run, left leg, tube and its branch.
    core_specs = [
        ("+6V3_HEAD_PR", 0.7, "#c93a35"),
        ("GND_HEAD", 0.7, "#272b31"),
        *[(f"SIGNAL_{i:02d}", 0.4, "#e2b34f" if i % 2 else "#6a8eb4")
          for i in range(1, 12)],
    ]
    columns = (-2.45, -1.65, -0.85, -0.05, 0.75, 1.55, 2.35)
    wire_children = []
    for i, (name, radius, color) in enumerate(core_specs):
        col = columns[i // 2]
        row = -0.55 if i % 2 == 0 else 0.55
        # Centreline follows the D-104 reserved disc crossing, channel and
        # 8 mm tube bore.  The bend inside the leg is a neutral-pose sketch.
        common = [
            (-22.9 + col, 42.0, -33.4 + row),
            (-22.9 + col, -43.4, -33.4 + row),
            (-59.9 + col, -43.4, -33.4 + row),
            (-59.9 + col, -46.0, -26.0 + row),
            (-59.9 + col, -54.3, -26.0 + row),
            (-59.9 + col, -54.3, pz - 30.0 + row),
            (px + col, -54.3, pz + row),
            (px + col, -42.6, pz + row),
            (px + col, -40.0, pz + row),
        ]
        # The schedule gives the bundle count but does not allocate every
        # signal to a branch.  A four-way servo / nine-way PCB-12 split is
        # shown as the current packaging assumption.
        key = "HARNESS_D104_SERVO_BRANCH" if i < 4 else "HARNESS_D104_PCB12_BRANCH_PITCH"
        branch_points = list(entry.D104_BRANCHES[key][2])[1:]
        if i >= 4:
            branch_points += list(entry.D104_BRANCHES["HARNESS_D104_PCB12_BRANCH_ROLL"][2])[1:]
        path = common + [(x + col * 0.45, y, z + row * 0.45) for x, y, z in branch_points]
        wire_children.append(paint(_wire(path, radius), f"{name}_INSULATED_WIRE", color))
    wires = Compound(label="13 conductors through left trunnion (nominal split)",
                     children=wire_children)

    # Rotor-to-head FFCs, 22 contacts, 11.5 mm wide and 0.3 mm thick.  The
    # first upper ZIF feeds W45; the remaining two feed the head electronics.
    rotor_ffcs = []
    for label, y0, z in (("W45_CSI_TO_DISC", -4.5, -34.6),
                         ("W42_HEAD_POWER", 0.0, -34.2),
                         ("W43_HEAD_SIGNAL", 4.5, -33.8)):
        path = [(px, y0, -36.1), (px, y0, z), (px, 14.0, z)]
        rotor_ffcs.append(paint(_ribbon(path, (1, 0, 0), 11.5),
                                label, "#d9aa63"))
    rotor = Compound(label="Three rotor-to-head FFCs", children=rotor_ffcs)

    # W45 follows the D-105 yaw-carried static route up the bracket.  Folds
    # between runs are represented as short flat segments at the neutral pose.
    w45_runs = [
        _ribbon_segment((px, 19.0, -34.3), (-91.5, 22.6, -34.3), (0, 1, 0), 12.0),
        _ribbon_segment((-91.5, 22.6, -34.3), (-105.5, 22.6, -31.8), (0, 1, 0), 12.0),
        _ribbon_segment((-105.5, 22.6, -31.8), (-150.0, 22.6, -31.8), (0, 1, 0), 12.0),
        _ribbon_segment((-150.0, 22.6, -31.8), (-150.0, 22.6, 108.0), (0, 1, 0), 12.0),
    ]
    # The top FFC lies along the mast's 15 degree bracket-top frame.
    top_origin, direction, normal = entry._d105_frame()
    top_a = tuple(top_origin[k] + 2.0 * normal[k] for k in range(3))
    top_b = tuple(top_origin[k] + 29.0 * direction[k] + 2.0 * normal[k] for k in range(3))
    top_side = (top_a[0], 22.6, top_a[2])
    w45_runs.append(_ribbon_segment((-150.0, 22.6, 108.0), top_side,
                                    (0, 1, 0), 12.0))
    w45_runs.append(_ribbon_segment(top_side, top_a, (1, 0, 0), 12.0))
    w45_runs.append(_ribbon_segment(top_a, top_b, (0, 1, 0), 12.0))
    w45 = paint(Compound(children=w45_runs), "W45_STATIC_CSI_FFC_TO_TOP_JOINER", "#d9aa63")

    # W46 is the 16 mm standard-mini wear cable.  Reuse the neutral-pose
    # elastica ribbon already solved by D-105; continue it through the cover
    # slot and roof guide as thin cable rather than the large reserve blocks.
    loop = entry.d105_local("loop_reserves")[0][1]
    w46_loop = paint(loop, "W46_CSI_FREE_C_LOOP_NEUTRAL_POSE", "#e0c9a5")
    w46_inside = paint(Compound(children=[
        _ribbon_segment((-116.0, -1.0, 48.16), (-115.4, -1.0, 80.0), (0, 1, 0), 16.0),
        _ribbon_segment((-115.4, -1.0, 80.0), (-24.0, -1.0, 80.0), (0, 1, 0), 16.0),
    ]), "W46_CSI_THROUGH_COVER_AND_ROOF", "#e0c9a5")
    csi = Compound(label="CSI ribbons W45 and W46", children=[w45, w46_loop, w46_inside])

    return Compound(label="Harness", children=[
        Compound(label="Head wires", children=[wires, rotor, csi]),
    ])
