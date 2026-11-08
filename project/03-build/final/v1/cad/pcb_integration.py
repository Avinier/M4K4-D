"""Install KiCad STEP inputs in the final robot.

Millimetres. Static transforms are those proved by check_pcbNN_fit.py; no
subsystem source or KiCad layout is changed.
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
# D-093/D-095: PCB-05 and PCB-06 became bought modules and PCB-13 was deleted.
BOARDS = {9:"pcb-09-c0-link-adapter", 10:"pcb-10-c3-carrier", 11:"pcb-11-status-led", 15:"pcb-15-nose-hall"}
GROUPS = {9:"PCB-09 C0 link adapter", 10:"PCB-10 C3 controller carrier", 11:"PCB-11 status LED carrier",
          15:"PCB-15 nose Hall carrier"}


def source_path(number):
    name = BOARDS[number]
    revision = "revB" if number == 9 else "revA"
    return ROOT / "04-pcbs" / name / "cad" / (name + f"-{revision}.step")


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
    if number == 9:
        # D-092: STEP exported with --user-origin 0x0mm, (Xs, Ys) = (KiCad x, -y); KiCad x = X + 104.7,
        # y = 139 - Y. The board's underside is on the standoffs at Pi top + 11.0 = Z 106.45.
        return [("MAIN",Location((-104.7,139.0,106.45+(1.6-core)/2-bb.min.Z)))]
    if number == 10:
        t=gp_Trsf()
        t.SetValues(-1,0,0,156, 0,0,1,-58.4+(1.6-core)/2-bb.min.Z, 0,1,0,225.5)
        return [("MAIN",Location(t))]
    if number == 11:
        loc=Location(Plane(origin=(-7.2-0.035-core,-87.3,194.3),x_dir=(0,1,0),z_dir=(1,0,0)))
        return [("CROWN",Location(head_origin)*loc)]
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
    revision = "REVB" if number == 9 else "REVA"
    return Compound(label=f"PCB{number:02d}_KICAD_{revision}_{instance}",children=parts)


def leaves(node, parent=Location()):
    here=parent*node.location
    if node.children:
        for child in node.children:
            yield from leaves(child,here)
    else:
        yield node,parent


def retain(number,label):
    """Explicit hardware/plug whitelist; the KiCad input owns mounted parts."""
    if number == 9:
        return label.startswith(("PCB09_M25X11_ROUND_STANDOFF_","PCB09_M25X5_SOCKET_SCREW_"))
    if number == 10:
        return "MATED_PLUG" in label or label.startswith("C3_CARRIER_M25_SCREW_")
    return False


# PCB-09's placeholder plugs stood on the review-placement headers; the KiCad headers moved
# (D-092), so the mated GHR plugs are rebuilt on the installed headers, as the body model
# draws them: top-entry plugs above BM headers, J9-1's side-entry plug beyond the +Y edge.
PCB09_PLUGS = {"J5":("J9_4",2,"top"), "J3":("J9_2",6,"top"), "J4":("J9_3",10,"top"),
               "J2":("J9_1",6,"side"), "J6":("J6",6,"top")}  # KiCad refs


def pcb09_mated_plugs(board,body):
    from build123d import Box
    out=[]
    for part in board.children:
        key=part.label.split("__")[-1]
        if key not in PCB09_PLUGS:
            continue
        cid,n,entry=PCB09_PLUGS[key]
        b=part.bounding_box()
        cx=(b.min.X+b.max.X)/2
        if entry=="side":                         # side entry, mating +Y over the board's +Y edge (Y 39)
            size=(body.gh_plug_width(n),body.GH_PLUG_PROUD,body.GH_PLUG_THICKNESS)
            centre=(cx,39.0+body.GH_PLUG_PROUD/2,b.min.Z+body.GH_PLUG_THICKNESS/2)
        else:
            size=(body.gh_plug_width(n),body.GH_PLUG_THICKNESS,body.GH_PLUG_PROUD)
            centre=(cx,(b.min.Y+b.max.Y)/2,b.max.Z+body.GH_PLUG_PROUD/2)
        plug=Box(*size).moved(Location(centre))
        plug.label=f"C0_{cid}_GHR{n:02d}_MATED_PLUG"
        plug.color=Color(0.957,0.945,0.902)
        out.append(plug)
    assert len(out)==5,[p.label for p in out]
    return out


def replace_completed_boards(robot,body,head_origin):
    custom=next(c for c in robot.children if c.label=="Custom PCBs")
    replacements={}
    for number,name in GROUPS.items():
        old=next(c for c in custom.children if c.label==name)
        hardware=[placed_copy(node,parent) for node,parent in leaves(old) if retain(number,node.label or "")]
        expected={9:4,10:14,11:0,15:0}[number]
        assert len(hardware)==expected,(number,"retained hardware count",len(hardware),[s.label for s in hardware])
        boards=[installed_board(number,instance,loc) for instance,loc in placements(number,body,head_origin)]
        if number == 9:
            hardware+=pcb09_mated_plugs(boards[0],body)
        replacements[name]=Compound(label=name,children=[*boards,*hardware])
    newcustom=Compound(label="Custom PCBs",children=[replacements.get(c.label,c) for c in custom.children])
    return Compound(label=robot.label,children=[newcustom if c is custom else c for c in robot.children])
