"""Install released KiCad rev-A STEP inputs in the final robot only.

Millimetres. Static transforms are those proved by check_pcbNN_fit.py; no
subsystem source or KiCad layout is changed. PCB-09 remains provisional.
"""
from functools import lru_cache
from pathlib import Path
import re
from build123d import Compound, Solid, Location, Plane, Color
from OCP.TopAbs import TopAbs_COMPOUND, TopAbs_SOLID
from OCP.TopoDS import TopoDS
from cadgen.step_scene import import_step
from OCP.gp import gp_Trsf

ROOT = Path(__file__).resolve().parents[3]
BOARDS = {5:"pcb-05-audio-front-end", 6:"pcb-06-pdm-mic", 10:"pcb-10-c3-carrier",
          11:"pcb-11-status-led", 13:"pcb-13-charge-inlet", 15:"pcb-15-nose-hall"}
GROUPS = {5:"PCB-05 audio front end", 6:"PCB-06 PDM microphone boards x4",
          10:"PCB-10 C3 controller carrier", 11:"PCB-11 status LED carrier",
          13:"PCB-13 charge inlet", 15:"PCB-15 nose Hall carrier"}


def source_path(number):
    name = BOARDS[number]
    return ROOT / "04-pcbs" / name / "cad" / (name + "-revA.step")


@lru_cache(None)
def raw_parts(number):
    shape = import_step(str(source_path(number)))
    # The XCAF importer preserves KiCad reference instances (R3, J1...) and
    # represents the board core as the sole direct, non-assembly solid.
    parts = [(BOARDS[number]+"_PCB" if not c.children else c.label, c)
             for c in shape.children if c.solids()]
    assert sum(label.endswith("_PCB") for label, _ in parts) == 1, number
    return parts


def core_bounds(number):
    return next(s for label, s in raw_parts(number) if label.endswith("_PCB")).bounding_box()


def placements(number, body, head_origin):
    """(instance, STEP-to-world Location), shared with integration verification."""
    bb = core_bounds(number)
    core = bb.max.Z - bb.min.Z
    if number == 5:
        return [("MAIN", Location((-55,119,115.6-1.6+(1.6-core)/2-bb.min.Z)))]
    if number == 6:
        out=[]
        inner = body.MIC_BOARD_OUTER_Y - body.MIC_BOARD_SIZE[1]
        for x,y,z,pos in body.MICROPHONE_PORTS:
            sign = 1 if y > 0 else -1
            centre = -1 if x > body.BODY_AXIS_X else 1
            frame=Location(Plane(origin=(x,sign*inner,z),x_dir=(centre,0,0),z_dir=(0,-sign,0)))
            out.append((pos,frame*Location((-106,107,-0.955))))
        return out
    if number == 10:
        t=gp_Trsf()
        t.SetValues(-1,0,0,156, 0,0,1,-58.4+(1.6-core)/2-bb.min.Z, 0,1,0,225.5)
        return [("MAIN",Location(t))]
    if number == 11:
        loc=Location(Plane(origin=(-7.2-0.035-core,-87.3,194.3),x_dir=(0,1,0),z_dir=(1,0,0)))
        return [("CROWN",Location(head_origin)*loc)]
    if number == 13:
        t=gp_Trsf()
        t.SetValues(0,0,1,body.CHARGE_INLET_BOARD_SEAT_X+(body.PCB_THICKNESS-core)/2-bb.min.Z,
                    1,0,0,-114, 0,1,0,171.5)
        return [("MAIN",Location(t))]
    if number == 15:
        return [("NOSE",Location(Plane(origin=(126.6-core/2-bb.min.Z,-93,135),x_dir=(0,1,0),z_dir=(1,0,0))))]
    raise KeyError(number)


def dnp_refs(number):
    """Read assembly DNP flags from the matching layout, not a second BOM list."""
    name=BOARDS[number]
    text=(ROOT/"04-pcbs"/name/"design"/(name+".kicad_pcb")).read_text()
    out=set()
    for match in re.finditer(r'\(footprint ',text):
        depth=0;quoted=False;escaped=False
        for end in range(match.start(),len(text)):
            char=text[end]
            if char=='"' and not escaped:quoted=not quoted
            if not quoted:depth+=(char=='(')-(char==')')
            escaped=(char=='\\' and not escaped)
            if depth==0:break
        block=text[match.start():end+1]
        if re.search(r'\(attr[^)]*\bdnp\b',block):
            out.add(re.search(r'\(property "Reference" "([^"]+)"',block).group(1))
    return out


def placed_copy(shape,delta=Location()):
    """Copy this branch's wrappers and share OCC geometry; never copy parents.

    Shape.moved() deepcopies the whole assembly through the parent link in
    this build123d version (see makad-v1._shifted). Preserve child placements
    and colours explicitly without carrying that parent into a new board.
    """
    if shape.children:
        out=Compound(label=shape.label,children=[placed_copy(c) for c in shape.children])
        out.location=delta*shape.location
    else:
        raw=shape.wrapped.Moved(delta.wrapped)
        if raw.ShapeType()==TopAbs_SOLID:out=Solid(TopoDS.Solid_s(raw))
        elif raw.ShapeType()==TopAbs_COMPOUND:out=Compound(TopoDS.Compound_s(raw))
        else:raise TypeError((shape.label,raw.ShapeType()))
        out.label=shape.label
    if shape.color is not None:out.color=shape.color
    return out


def installed_board(number, instance, loc):
    parts=[]
    omitted=dnp_refs(number)
    for i,(label,shape) in enumerate(raw_parts(number)):
        if label in omitted:continue
        # Keep the imported model's subparts and colours. Top-level names are
        # unique even when several placements use the same library model.
        part=placed_copy(shape,loc)
        part.label=f"PCB{number:02d}_{instance}_{i:02d}__{label}"
        if label.endswith("_PCB"):
            part.color=Color(0.08,0.36,0.16)
        parts.append(part)
    return Compound(label=f"PCB{number:02d}_KICAD_REVA_{instance}",children=parts)


def leaves(node, parent=Location()):
    here=parent*node.location
    if node.children:
        for child in node.children:
            yield from leaves(child,here)
    else:
        yield node,parent


def retain(number,label):
    """Explicit hardware/plug whitelist; the KiCad input owns mounted parts."""
    if number == 5:
        return "MATED_PLUG" in label
    if number == 6:
        return any(s in label for s in ("GASKET","M2_SCREW","PIGTAIL_RESERVE"))
    if number == 10:
        return "MATED_PLUG" in label or label.startswith("C3_CARRIER_M25_SCREW_")
    if number == 13:
        return label.startswith("PCB13_M2X5_THREAD_FORMING_SCREW_")
    return False


def replace_completed_boards(robot,body,head_origin):
    custom=next(c for c in robot.children if c.label=="Custom PCBs")
    replacements={}
    for number,name in GROUPS.items():
        old=next(c for c in custom.children if c.label==name)
        hardware=[placed_copy(node,parent) for node,parent in leaves(old) if retain(number,node.label or "")]
        expected={5:7,6:24,10:14,11:0,13:2,15:0}[number]
        assert len(hardware)==expected,(number,"retained hardware count",len(hardware),[s.label for s in hardware])
        boards=[installed_board(number,instance,loc) for instance,loc in placements(number,body,head_origin)]
        replacements[name]=Compound(label=name,children=[*boards,*hardware])
    newcustom=Compound(label="Custom PCBs",children=[replacements.get(c.label,c) for c in custom.children])
    return Compound(label=robot.label,children=[newcustom if c is custom else c for c in robot.children])
