"""Visible, nominal chassis leads for the D-106 harness corridors.

World coordinates, millimetres.  These are insulated wire/cable envelopes, not
cut-length or bend-radius proofs.  D106_ROUTES and BALANCE in the final assembly
remain the routing authority; their translucent boxes are inspection reserves.
"""

from build123d import Box, Compound, Cylinder, Location, Plane, Solid, Sphere, Vector


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

# HN-006: two WAGO 221-415 five-conductor connectors, each with one AWG16
# input and four AWG18 outputs. Manufacturer dimensions 30 x 18.6 x 8.4 mm;
# fine-stranded 24–12 AWG, 32 A/450 V nominal. The boxes lie above the tub
# modules, under the compute tray, with 2.9 mm separation between polarities.
TUB_SPLICES = {"POS": (35., 65., 1.5, 20.1, 74.5, 82.9),
               "NEG": (35., 65., -20., -1.4, 74.5, 82.9)}
TUB_SPLICE_PORT_X = {"IN": 38., "M2": 44., "M3": 50., "LEFT": 56., "RIGHT": 62.}

# Continuous signal-cable dress to the fitted PCB-10 GH plugs. Rerouted 2026-11-17
# after the D-106..D-109 review (piecewise clash test): W30/W31 rise through the
# motor-bay deck opening (X > -17) beside the encoder cap instead of through the
# solid rear deck; all five cross under W11 (Z 82.2) and over W09 in the X 22-35
# window at Y -38..-46, then rise in the plug layer (Y -44..-48) to their plugs.
# W29 no longer passes through the SS34 joint; W32 leaves the left driver between
# W03a+ and W08. Cable clips, connector exits and lift slack remain E.
SIGNAL_CABLES = (
    ("W29_IMU_TO_J10_7_GH8_CABLE", 1.4, "#65a7b5",
     [(25,-13,64),(26,-20,70),(24.5,-33,73.5),(24.5,-47,73.5),(16,-47,73.5),(16,-47,93),(16,-50,93)]),
    ("W30_ENCODER_L_TO_J10_3_GH4_CABLE", 1.1, "#9bba71",
     [(-13,11,42),(-14.6,11,46),(-14.6,11,59),(-8,11,65),(6,5,67),(6,-8,68.5),(14,-20,71),
      (25.5,-28.5,76),(27,-38,76.5),(27,-47,76.5),(27,-47,93),(26.5,-50,93)]),
    ("W31_ENCODER_R_TO_J10_4_GH4_CABLE", 1.1, "#709f6d",
     [(-13,-11,42),(-14.6,-11,46),(-14.6,-11,59),(-8,-11,65),(9,-13,66),(28,-27,68.5),
      (34,-35,73),(34,-38,75.5),(34,-47,75.5),(34,-47,93),(34,-50,93)]),
    ("W32_DRIVER_L_TO_J10_5_GH6_CABLE", 1.3, "#71a4ca",
     [(39,45.5,69.3),(34,45.5,72.5),(31,43,75.5),(28,34,75.5),(25,30,75),(19,0,75),(19,-28,77),
      (23,-33,78),(23,-43.5,78),(11.5,-43.5,78),(11.5,-43.5,86.5),(11.5,-50,86.5)]),
    ("W33_DRIVER_R_TO_J10_6_GH6_CABLE", 1.3, "#6b86b9",
     [(40,-34,71),(36,-36,78),(30.5,-39,78),(30.5,-47,78),(30.5,-47,86.5),(30.5,-50,86.5)]),
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


LAST_PATHS = {}   # label -> centreline points of the last build (harness_cut_list.py)


def build_chassis_harness(entry):
    groups = {name: [] for name in (
        "Pack and balance", "Fused and switched distribution", "Drive and motor",
        "Head supply from tub", "Chassis control signals", "Chassis sensors")}

    def wire(group, label, points, radius, colour):
        LAST_PATHS[label] = [tuple(map(float, p)) for p in points]
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
    for n, dx, z, colour in (("BMINUS", -1.1, 42.2, "#484d54"),
                           ("BMID", 0., 44.8, "#e6be48"),
                           ("BPLUS", 1.1, 47.4, "#c44942")):
        # D-115: CH-103 card on the BMS. Short stubs from the BMS B-/BM/B+
        # pads (+Y end, U) to the fuses; fused tails leave the card's +Y edge,
        # cross over the pack's +Y end, drop in the strap-to-wall gap and enter
        # the tub window to join the PA lead.
        fx = {"BMINUS": 41.5, "BMID": 44.5, "BPLUS": 47.5}[n]
        cell_stub = [(fx, 22.8, 55.0), (fx, 20.6, 55.1)]
        protected = [(fx, 17.4, 55.1), (fx, 24.0, 55.1), (fx, 24.6, 54.6),
                     (fx, 24.6, 51.3), (44.0 + dx, 30.0, 51.3), (44.0 + dx, 34.05, 51.3),
                     (44.0 + dx, 34.05, z), (44.0 + dx, 36.0, z),
                     *_shift(balance_pack[1:], dx=dx)]
        wire("Pack and balance", f"W02P_BMS_TO_CH103_{n}_AWG24", cell_stub, .52, colour)
        wire("Pack and balance", f"W02P_CH103_TO_PA_{n}_AWG24", protected, .52, colour)
        wire("Pack and balance", f"W02B_PA_TO_XHP3_{n}_AWG24",
             _shift(balance_body, dx=dx), .52, colour)

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
    feeder = feeder[:-2] + [(31., 28., 62.35), (32.2, 25., 61.)]
    for polarity, box in TUB_SPLICES.items():
        x0,x1,y0,y1,z0,z1=box
        block=Box(x1-x0,y1-y0,z1-z0).moved(Location(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)))
        groups["Fused and switched distribution"].append(entry._tag(
            block,f"HN006_TUB_{polarity}_WAGO_221_415_INSULATED",
            "#a22b2b" if polarity=="POS" else "#22282e"))
        colour="#cf413a" if polarity=="POS" else "#30343a"
        mouth=y1 if polarity=="POS" else y0
        outside=26. if polarity=="POS" else -26.
        z=(z0+z1)/2
        port=lambda name:(TUB_SPLICE_PORT_X[name],mouth,z)
        if polarity=="POS":
            source=[*_shift(feeder,dy=-1.,dz=1.1),(32.,26.,70.),(38.,26.,70.),(38.,outside,z),port("IN")]
        else:
            source=[*_shift(feeder,dy=1.,dz=-1.1),(33.,26.,67.),(33.,26.,82.7),(33.,-26.,82.7),(38.,-26.,z),port("IN")]
        wire("Fused and switched distribution",f"W05c_JCHASSIS_TO_TUB_{polarity}_AWG16",source,1.,colour)
        for module,x in (("M2",40.),("M3",64.)):
            if polarity=="POS":
                pts=[port(module),(TUB_SPLICE_PORT_X[module],26.,z),(x,26.,z),(x,26.,70.),(x,23.,64.)]
            else:
                pts=[port(module),(TUB_SPLICE_PORT_X[module],-26.,z),(33.,-26.,z),
                     (33.,-26.,82.7),(33.,26.,82.7),(x,26.,82.7),(x,23.,64.)]
            wire("Fused and switched distribution",f"W05t_TUB_TO_{module}_{polarity}_AWG18",pts,.83,colour)
        for side, key in (("LEFT","W06"),("RIGHT","W07")):
            route=_path(entry,entry.D106_CHAINS[key]);end=route[0]
            if polarity=="POS" and side=="LEFT":
                pts=[port(side),(TUB_SPLICE_PORT_X[side],26.,z),(end[0],26.,70.),end]
            elif polarity=="NEG" and side=="RIGHT":
                pts=[port(side),(TUB_SPLICE_PORT_X[side],-26.,z),(end[0],-26.,70.),end]
            elif polarity=="POS":
                pts=[port(side),(TUB_SPLICE_PORT_X[side],26.,z),(33.5,26.,79.),
                     (33.5,-26.,79.),end]
            else:
                pts=[port(side),(TUB_SPLICE_PORT_X[side],-26.,z),(33.,-26.,82.7),
                     (33.,26.,82.7),end]
            stem="W06_TUB_TO_DRIVER_L" if side=="LEFT" else "W07_TUB_TO_DRIVER_R"
            wire("Drive and motor",f"{stem}_{polarity}_AWG18",[ *pts,*_offset(route[1:],.83 if polarity=="POS" else -.83)],.83,colour)
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
    # 2026-11-17: continued to the C3 J10-8 plug (grid-routed: parts >= 0.4, power >= 0.5, W08/W09 >= 5 mm)
    nose += [(86.2,-30.8,70.2),(67.2,-47.8,73.2),(55.8,-47.8,73.2),(49.2,-47.8,80.6),(38.6,-48.2,80.6),
             (38.2,-48.4,79.8),(38.0,-50.,79.6)]
    wire("Chassis sensors", "W34_NOSE_HALL_TOUCH_TO_J10_8_GH5_CABLE",
         nose, 1.0, "#55a8a9")
    wire("Chassis sensors", "W36_REAR_TCRT_TO_J10_10_GH4_CABLE",
         _path(entry, entry.D106_CHAINS["W36 TCRT"]) + [   # 2026-11-17: on to the C3 J10-10 plug (grid-routed)
             (-51.2,-22.2,60.2),(-48.8,-25.8,58.2),(-25.8,-28.8,59.2),(-17.8,-33.8,64.2),(-8.2,-34.2,69.8),
             (-6.2,-36.3,71.7),(4.2,-44.2,75.2),(22.2,-44.2,75.2),(24.8,-45.2,77.5),(26.2,-44.8,79.2),
             (32.8,-44.2,85.8),(44.2,-46.8,93.2),(44.3,-50.,93.2)], .9, "#6989b6")
    for label, radius, colour, points in SIGNAL_CABLES:
        wire("Chassis control signals", label, points, radius, colour)
    return Compound(label="Chassis wires", children=[
        Compound(label=name, children=parts) for name, parts in groups.items()])
