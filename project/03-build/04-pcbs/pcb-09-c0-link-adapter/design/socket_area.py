"""Add the socket-only underside rule area through KiPy (no copper pour)."""
from kipy import KiCad
from kipy.board_types import Zone
from kipy.geometry import PolyLine, PolyLineNode, PolygonWithHoles, Vector2
from kipy.proto.board.board_types_pb2 import BoardLayer as BL, ZoneType

b = KiCad().get_board()
assert b.name == "pcb-09-c0-link-adapter.kicad_pcb"
name = "SOCKET_ONLY_B"
if not any(z.name == name for z in b.get_zones()):
    line = PolyLine()
    for x, y in [(100,116.55),(151.8,116.55),(151.8,122.7),(100,122.7)]:
        line.append(PolyLineNode.from_point(Vector2.from_xy_mm(x,y)))
    line.closed = True
    outline = PolygonWithHoles()
    outline.outline = line
    zone = Zone()
    zone.type = ZoneType.ZT_RULE_AREA
    zone.name, zone.layers, zone.outline = name, [BL.BL_B_Cu], outline
    # A custom disallow rule applies only to B-side footprints other than J1.
    # Copper/vias remain routable; J1's plated lands are intentionally here.
    b.create_items([zone])
b.save()
print("Saved SOCKET_ONLY_B: custom rule reserves the underside for J1")
