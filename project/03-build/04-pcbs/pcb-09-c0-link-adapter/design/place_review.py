"""PCB-09 review placement via the open Nightly editor, using kp helpers.

After API flips, use Nightly Tools > Update Footprints from Library with Match
pad positions enabled; preserve fabrication attributes and text placement. This
clears the flip-related library mismatch warnings; read back the pads afterwards.

No routing. Connector positions are candidates until populated CAD fit proves
them. The numbered socket grid is checked after the actual bottom-side flip.
"""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]/"tools"))
import kp

assert kp.b.name == "pcb-09-c0-link-adapter.kicad_pcb"
kp.b.clear_selection()
placements = {
    "J1": (101.77,120.93831,270,True),
    "J2": (146.5,103.6,180,False), "J3": (161.5,112.2,0,False),
    "J4": (161.5,105,0,False), "J5": (146.5,111.6,0,False),
    "U1": (145.5,106,0,True), "U2": (161,108,0,True),
    "C1": (150.8,106,0,True), "C2": (166.5,108,0,True),
    "R1": (146,109.7,0,True), "R2": (161,112,0,True),
    "R3": (142.1,111,90,True), "R4": (166.5,111,90,True),
    "Q1": (151.5,108.7,0,True), "R5": (154.5,110.5,0,True),
    "R6": (155.1,108,0,True), "D1": (155,113.4,0,True),
    "C3": (165.5,114.2,0,True), "C4": (169,110,90,True),
    "TP1": (105.58,119.66831,0,False), "TP2": (108.12,119.66831,0,False),
    "TP3": (110.66,119.66831,0,False), "TP4": (168.3,113.6,0,True),
    "TP5": (128.44,119.66831,0,False), "TP6": (133.52,119.66831,0,False),
}
readback = {}
for ref, position in placements.items():
    readback[ref] = kp.place(ref, *position)
    print(ref, json.dumps(readback[ref]), flush=True)
for n in range(1, 41):
    _, x, y = readback["J1"][str(n)]
    expected = (101.77+((n-1)//2)*2.54, 120.93831-((n-1)%2)*2.54)
    assert abs(x-expected[0]) < 0.0002 and abs(y-expected[1]) < 0.0002, (n,x,y,expected)
kp.exclude_from_pos(*[f"TP{n}" for n in range(1,7)])
kp.refs_to_fab()
kp.save()
(HERE/"placement-readback.json").write_text(json.dumps(readback,indent=2)+"\n")
print("PASS: actual 40-pad underside socket grid and review placement saved")
