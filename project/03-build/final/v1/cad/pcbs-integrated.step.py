"""Released KiCad boards at the same world positions as the final robot.

Focused geometry/visual review; ten installed boards (PCB-09 added by D-092).
The full-robot integration report checks their surroundings separately.
"""
from build123d import Compound
import body_v1_model as body
from pcb_integration import BOARDS,installed_board,placements


def gen_step():
    return {"shape":Compound(label="Completed KiCad boards - installed positions",children=[
        installed_board(n,instance,loc) for n in BOARDS
        for instance,loc in placements(n,body,body.HEAD_ORIGIN_IN_CHASSIS)])}
