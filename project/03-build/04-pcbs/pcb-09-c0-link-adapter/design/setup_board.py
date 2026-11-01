"""Set PCB-09 outline/origins through KiPy in the open Nightly editor.

World -> KiCad: x = world X + 104.7; y = 139 - world Y.
The approved core is 1.6 mm; placement is a review, not a fabrication release.
"""
from kipy import KiCad
from kipy.board_types import BoardSegment, BoardText
from kipy.geometry import Vector2
from kipy.proto.board.board_types_pb2 import BoardLayer as BL
from kipy.proto.board.board_commands_pb2 import BoardOriginType

k = KiCad()
b = k.get_board()
assert b.name == "pcb-09-c0-link-adapter.kicad_pcb", b.name
existing = [s for s in b.get_shapes() if s.layer == BL.BL_Edge_Cuts]
assert len(existing) in (0, 8), "Unexpected outline: inspect before editing"
points = [(100,122.7),(151.8,122.7),(151.8,116.5),(170.7,116.5),
          (170.7,100),(140.7,100),(140.7,116.6),(100,116.6)]
items = []
vec = lambda x, y: Vector2.from_xy(round(x*1e6), round(y*1e6))
for start, end in zip(points, points[1:]+points[:1]):
    s = BoardSegment()
    s.start, s.end = vec(*start), vec(*end)
    s.layer = BL.BL_Edge_Cuts
    s.attributes.stroke.width = 50000
    items.append(s)
if not existing:
    b.create_items(items)
for value in BoardOriginType.values():
    if value:
        b.set_origin(value, vec(100,100))
t = BoardText()
t.value = "PCB-09 / D-073 D-074 / REVIEW - UNROUTED"
t.position, t.layer = vec(136,94), BL.BL_Cmts_User
t.attributes.size = vec(1.2,1.2)
t.attributes.stroke_width = 180000
if not any(x.value == t.value for x in b.get_text()):
    b.create_items([t])
b.save()
print(k.get_version(), b.name, "8 outline edges and origins saved")
