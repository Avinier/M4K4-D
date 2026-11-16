"""D-109 Level 2: placement envelopes for body-harness parts that had no CAD.

World mm. All are `E` allowances for unbought or unselected parts; labels carry
ENVELOPE. They are placement proofs, not part selections. Checked by
check_d109_placements.py.
"""

from build123d import Box, Cylinder, Location

# B-07: the unswitched negative charge splice, beside the existing + splice
# (axis -45.6, -34), forward of the rear plate and above the cross rail.
NEG_CHARGE_SPLICE = dict(axis=(-37.5, -34.0), r=3.25, z=(70.0, 84.0))   # under the compute tray (Z 84.5)

# B-02: shared-5 V +/- splices (one AWG18 feed in, three outputs: W11, W12, W14)
# under the compute tray, -Y of M5, axis along X; SS34 potted joint on W11.
SHARED_5V = {"POS": (-12.0, -38.2, 77.6), "NEG": (-12.0, -43.4, 77.6)}   # Z 75.1-80.1: above the J-S18 body-lead reserve (Z 75)   # NEG stays Y > -46: C3 plug layer
SHARED_5V_R, SHARED_5V_LEN = 2.5, 16.0   # X -20..-4: W10 drops through the tray at X -3..3
SS34_POTTED = dict(centre=(12.0, -38.5, 75.5), r=3.0, length=18.0)

# B-04: Micro-Fit 3.0 1x6 inline pair, mated (E 21 x 7.3 x 10), on the rear plate's
# +Y half above M6, between the J6 lead from PCB-09 and the W40/W44 tails.
REAR_BREAK = (-45.5, -35.5, 14.0, 35.0, 94.0, 101.5)

# B-01: audio hub v2 replaces the M13 perfboard. Below it the fuse-holder envelope
# tops out at Z 99; beyond Y 58.5 is the frame's front +Y post. So the board grows
# only down to Z 99.5 (18.5 x 23). Parts side (-X): four 2.54 mm 2x3 latching
# headers (Molex C-Grid III class, U) in a 2x2 grid, mated plugs toward -X, plugged
# through the front aperture in the D-037 order. Resistors are 0805 SMD on the
# bracket side in the 1.5 mm boss gap. The two M2 screws are dropped (they sit in
# the header area); the board is held in a printed cradle on the bracket bosses
# with VHB, like the bought-module cradles. W26 lands on solder pads on the top edge.
# A mic-end break was screened on 2026-11-16 and rejected: anything riding with the
# shell inboard of |Y| 70.3 hits the frame's upper side rail as the shell lowers.
# B-08: W28 2-way inline break.
HUB_V2_BOARD = (63.2, 64.8, 40.0, 58.5, 99.5, 122.5)
MIC_HEADERS_MATED = (49.0, 63.2, 40.5, 58.0, 100.0, 122.0)
SPEAKER_BREAK = (74.0, 82.0, 30.0, 36.0, 100.0, 105.0)


def _box(b):
    x0, x1, y0, y1, z0, z1 = b
    return Box(x1 - x0, y1 - y0, z1 - z0).moved(Location(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)))


def parts(tag):
    """[(label, shape)] tagged with the entry's _tag(shape, label, colour)."""
    out = []
    a, r, (z0, z1) = NEG_CHARGE_SPLICE["axis"], NEG_CHARGE_SPLICE["r"], NEG_CHARGE_SPLICE["z"]
    out.append(tag(Cylinder(r, z1 - z0).moved(Location((a[0], a[1], (z0 + z1) / 2))),
                   "D109_CHARGE_SPLICE_NEG_AWG16_ENVELOPE", "#202020"))
    for pol, xyz in SHARED_5V.items():
        out.append(tag(Cylinder(SHARED_5V_R, SHARED_5V_LEN, rotation=(0, 90, 0)).moved(Location(xyz)),
                       f"D109_SHARED_5V_{pol}_SPLICE_ENVELOPE", "#8B1E1E" if pol == "POS" else "#202020"))
    s = SS34_POTTED
    out.append(tag(Cylinder(s["r"], s["length"], rotation=(0, 90, 0)).moved(Location(s["centre"])),
                   "D109_W11_SS34_POTTED_JOINT_ENVELOPE", "#555555"))
    out.append(tag(_box(REAR_BREAK), "D109_J6_REAR_BREAK_MICROFIT3_1X6_MATED_ENVELOPE", "#3A4044"))
    out.append(tag(_box(HUB_V2_BOARD), "D109_AUDIO_HUB_V2_PERFBOARD", "#C8A060"))
    out.append(tag(_box(MIC_HEADERS_MATED), "D109_W27_FOUR_2X3_MIC_HEADERS_MATED_ENVELOPE", "#F4F1E6"))
    out.append(tag(_box(SPEAKER_BREAK), "D109_W28_SPEAKER_INLINE_BREAK_ENVELOPE", "#F4F1E6"))
    return out
