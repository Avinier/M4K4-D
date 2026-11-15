"""Visible, nominal chassis leads for the D-106 harness corridors.

World coordinates, millimetres.  These are insulated wire/cable envelopes, not
cut-length or bend-radius proofs.  D106_ROUTES and BALANCE in the final assembly
remain the routing authority; their translucent boxes are inspection reserves.
"""

from build123d import Compound, Cylinder, Location, Plane, Solid, Sphere, Vector


def _tube(points, radius):
    """Connected cable envelope with rounded sample joints."""
    pieces = []
    for a, b in zip(points, points[1:]):
        a, b = Vector(*a), Vector(*b)
        delta = b - a
        if delta.length > 1e-7:
            pieces.append(Solid.make_cylinder(
                radius, delta.length, Plane(origin=a, z_dir=delta)))
    pieces.extend(Sphere(radius).moved(Location(tuple(p))) for p in points[1:-1])
    return Compound(children=pieces)

# HN-006: two supported, insulated multiwire splice envelopes. The bodies lie
# along Y over the CH-106 rear arms, one each side of the IMU. Dimensions are E
# until the selected rated splice and sleeve are measured.
TUB_SPLICES = {"POS": (19.0, 14.0, 69.0), "NEG": (27.0, 14.0, 69.0)}
TUB_SPLICE_RADIUS = 3.25
TUB_SPLICE_LENGTH = 24.0

# Initial continuous signal-cable dress to the fitted PCB-10 GH plugs. These
# paths are CAD-cleared at neutral; cable clips, actual connector exits and
# lift slack remain E until the populated first build.
SIGNAL_CABLES = (
    ("W29_IMU_TO_J10_7_GH8_CABLE", 1.4, "#65a7b5",
     [(25,-13,64),(30,-18,67),(25,-25,69),(10,-35,72),(10,-44,78),(13,-49,93)]),
    ("W30_ENCODER_L_TO_J10_3_GH4_CABLE", 1.1, "#9bba71",
     [(-13,11,42),(-22,18,52),(-22,35,57),(-10,35,63),(0,35,66),
      (10,35,70),(10,0,72),(15,-25,72),(25,-44,78),(25,-49,93)]),
    ("W31_ENCODER_R_TO_J10_4_GH4_CABLE", 1.1, "#709f6d",
     [(-13,-11,42),(-22,-18,52),(-22,-36,57),(-10,-36,73),
      (0,-36,74),(20,-45,74),(35,-49,93)]),
    ("W32_DRIVER_L_TO_J10_5_GH6_CABLE", 1.3, "#71a4ca",
     [(40,45,70),(35,35,73),(25,30,74),(15,0,75),(13,-44,78),(13,-49,86)]),
    ("W33_DRIVER_R_TO_J10_6_GH6_CABLE", 1.3, "#6b86b9",
     [(40,-34,71),(32,-34,73),(25,-35,73),(33,-49,86)]),
)


def _mid(box):
    return tuple((box[2 * i] + box[2 * i + 1]) / 2 for i in range(3))


def _through_boxes(boxes):
    """Join consecutive convex route boxes through their shared region."""
    if len(boxes) == 1:
        x0, x1, y0, y1, z0, z1 = boxes[0]
        return [(x0 + 2, (y0 + y1) / 2, (z0 + z1) / 2),
                (x1 - 2, (y0 + y1) / 2, (z0 + z1) / 2)]
    points = [_mid(boxes[0])]
    for a, b in zip(boxes, boxes[1:]):
        overlap = tuple(v for i in range(3) for v in
                        (max(a[2 * i], b[2 * i]), min(a[2 * i + 1], b[2 * i + 1])))
        if any(overlap[2 * i] > overlap[2 * i + 1] + 0.01 for i in range(3)):
            raise ValueError(f"disconnected chassis route boxes: {a} -> {b}")
        points.append(_mid(overlap))
    points.append(_mid(boxes[-1]))
    return points


def _path(entry, chain):
    return _through_boxes([entry.D106_ROUTES[name] for name in chain])


def _offset(points, dz):
    return [(x, y, z + dz) for x, y, z in points]


def _shift(points, dx=0., dy=0., dz=0.):
    return [(x + dx, y + dy, z + dz) for x, y, z in points]


def build_chassis_harness(entry):
    groups = {name: [] for name in (
        "Pack and balance", "Fused and switched distribution", "Drive and motor",
        "Head supply from tub", "Chassis control signals", "Chassis sensors")}

    def wire(group, label, points, radius, colour):
        groups[group].append(entry._tag(_tube(points, radius), label, colour))

    def pair(group, stem, chain, awg, radius, colours=("#cf413a", "#30343a")):
        points = _path(entry, chain)
        spacing = radius + .10
        for suffix, dz, colour in (("POS", spacing, colours[0]), ("NEG", -spacing, colours[1])):
            wire(group, f"{stem}_{suffix}_AWG{awg}", _offset(points, dz), radius, colour)

    # Pack-side wires end at the J-PK/PA envelope; cell-end terminations and
    # protection have deliberately not been invented in this model.
    pack = [(30., 37., 44.5), (34., 42., 44.5), (38., 43.5, 44.5)]
    for suffix, dz, colour in (("POS", 1.1, "#cf413a"), ("NEG", -1.1, "#30343a")):
        wire("Pack and balance", f"W01_PACK_TO_JPK_{suffix}_AWG16", _offset(pack, dz), 1.0, colour)
    balance_pack = _through_boxes(entry.BALANCE["pack_lead"])
    balance_pack += [_mid(entry.BALANCE["pair"])]
    balance_body = [_mid(entry.BALANCE["pair"])] + _through_boxes(entry.BALANCE["body_lead"])
    for n, dx, colour in (("BMINUS", -1.1, "#484d54"), ("BMID", 0., "#e6be48"),
                          ("BPLUS", 1.1, "#c44942")):
        for stem, points in (("W02P_CELL_TO_PA", balance_pack),
                             ("W02B_PA_TO_XHP3", balance_body)):
            wire("Pack and balance", f"{stem}_{n}_AWG24",
                 _shift(points, dx=dx), .52, colour)

    wire("Fused and switched distribution", "W03a_JPK_TO_FUSE_POS_AWG16",
         _shift(_path(entry, entry.D106_CHAINS["W03a+"]), dy=-1.2, dz=1.0), .85, "#cf413a")
    negative = _path(entry, entry.D106_CHAINS["W03a-"])
    negative = [(x, y + (1.2 if i < 3 else -1.0),
                 z + (0.0 if i < 3 else (0.0 if i == 3 else -.7 if i == 4 else -1.0)))
                for i, (x, y, z) in enumerate(negative)]
    wire("Fused and switched distribution", "W03a_JPK_TO_JBAT_NEG_AWG16",
         negative, .85, "#30343a")
    fused = _path(entry, entry.D106_CHAINS["W03b"])
    fused = [(x, y + (-1.0 if i == 4 else 1.0), z + 1.0)
             for i, (x, y, z) in enumerate(fused)]
    wire("Fused and switched distribution", "W03b_FUSE_TO_JBAT_POS_AWG16",
         fused, .9, "#cf413a")
    feeder = _path(entry, entry.D106_CHAINS["W05c"])
    feeder = feeder[:-1] + [(32.2, 25., 61.)]  # end at the still-unplaced tub distribution
    for suffix, dy, dz, colour in (("POS", -1.0, 1.1, "#cf413a"),
                                   ("NEG", 1.0, -1.1, "#30343a")):
        wire("Fused and switched distribution", f"W05c_JCHASSIS_TO_TUB_{suffix}_AWG16",
             _shift(feeder, dy=dy, dz=dz), 1.0, colour)
    for polarity, xyz in TUB_SPLICES.items():
        splice = Cylinder(TUB_SPLICE_RADIUS, TUB_SPLICE_LENGTH,
                          rotation=(90, 0, 0)).moved(Location(xyz))
        groups["Fused and switched distribution"].append(entry._tag(
            splice, f"HN006_TUB_{polarity}_AWG16_MULTI_WIRE_SPLICE_ENVELOPE",
            "#a22b2b" if polarity == "POS" else "#22282e"))
    # The +Y and -Y plate strips represent the unfrozen tub distribution.
    pair("Fused and switched distribution", "W05t_TUB_TO_M2_M3_INPUT",
         ["PLATE_STRIP_PY"], 18, .83)
    for side, stem in (("L", "W06_TUB_TO_DRIVER_L"), ("R", "W07_TUB_TO_DRIVER_R")):
        pair("Drive and motor", stem, entry.D106_CHAINS["W06" if side == "L" else "W07"], 18, .83)
    for side, stem in (("L", "W08_DRIVER_TO_MOTOR_L"), ("R", "W09_DRIVER_TO_MOTOR_R")):
        points = _path(entry, entry.D106_CHAINS["W08 left" if side == "L" else "W09 right"])
        for suffix, dy, colour in (("POS", .55, "#c46a39"), ("NEG", -.55, "#5d6470")):
            routed = (_shift(points, dy=dy) if side == "L" else
                      [(x, y + (0.55 if suffix == "POS" else -0.55), z + .15)
                       for x, y, z in points])
            wire("Drive and motor", f"{stem}_{suffix}_AWG22", routed, .55, colour)
    points = _path(entry, entry.D106_CHAINS["W13/W17"])
    for stem, dy, colour in (("W13_M2_TO_JS18H_HEAD_6V3", -1.5, "#d8a344"),
                             ("W17_M3_TO_JS18Y_YAW_11V1", 1.5, "#a77ac4")):
        for suffix, offset, c in (("POS", -.75, colour), ("NEG", .75, "#30343a")):
            wire("Head supply from tub", f"{stem}_{suffix}_AWG20",
                 _shift(points, dy=dy + offset), .75, c)
    # Signal cables are shown as outer envelopes: the GH5/GH4 cores remain
    # individually specified by the connector schedule, not falsely spaced in
    # the Ø5 nose bore or the rear keel tunnel.
    nose = _path(entry, entry.D106_CHAINS["W34 nose"])
    nose += [(86., -31., 34.5), (86., -31., 56.5), _mid(entry.D106_ROUTES["NOSE_J10_8_RISER"])]
    wire("Chassis sensors", "W34_NOSE_HALL_TOUCH_TO_J10_8_GH5_CABLE",
         nose, 1.0, "#55a8a9")
    wire("Chassis sensors", "W36_REAR_TCRT_TO_J10_10_GH4_CABLE",
         _path(entry, entry.D106_CHAINS["W36 TCRT"]), .9, "#6989b6")
    for label, radius, colour, points in SIGNAL_CABLES:
        wire("Chassis control signals", label, points, radius, colour)
    return Compound(label="Chassis wires", children=[
        Compound(label=name, children=parts) for name, parts in groups.items()])
