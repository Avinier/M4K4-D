"""D-068 integration fix: JP1 pin relief, static and 2 mm install slide.

Targeted upright geometry only; checks the old interference as a planted case,
remaining side/back material, the screw-hole margin and the actual updated cut.
"""
import importlib.util,json,hashlib
from pathlib import Path
from build123d import Location
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import pcb_integration as P

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('makad_jp1_relief',HERE/'makad-v1.step.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def find(tree,label,parent=Location()):
    here=parent*tree.location
    if tree.label==label:return P.placed_copy(tree,parent)
    for child in tree.children:
        result=find(child,label,here)
        if result is not None:return result
    return None


def volume(a,b):
    operation=BRepAlgoAPI_Common(a.wrapped,b.wrapped)
    assert operation.IsDone()
    props=GProp_GProps()
    BRepGProp.VolumeProperties_s(operation.Shape(),props)
    return props.Mass()


def main():
    original=list(m.DROID_CUTS)
    m.DROID_CUTS=[entry for entry in original if entry!=(r"BODY_FRAME_C3_CARRIER_UPRIGHT_1",m.PCB10_JP1_RELIEF)]
    before=find(m._apply_droid_cuts(m._body.c3_carrier(),strict=False),'BODY_FRAME_C3_CARRIER_UPRIGHT_1')
    m.DROID_CUTS=original
    after=find(m._apply_droid_cuts(m._body.c3_carrier(),strict=False),'BODY_FRAME_C3_CARRIER_UPRIGHT_1')
    instance,loc=P.placements(10,m._body,m.HEAD_ORIGIN_IN_CHASSIS)[0]
    board=P.installed_board(10,instance,loc)
    jp1=next(p for p in board.children if p.label.endswith('__JP1'))
    planted=volume(jp1,before)
    assert planted>0.5,planted
    assert volume(jp1,after)<1e-6
    samples=[]
    for dz in [i/10 for i in range(-20,1)]:
        moving=P.placed_copy(jp1,Location((0,0,dz)))
        samples.append(dict(dz_mm=dz,clearance_mm=moving.distance(after),clash_mm3=volume(moving,after)))
    for dy in (0,0.5,1,2,4,8):
        moving=P.placed_copy(jp1,Location((0,dy,-2)))
        samples.append(dict(dy_mm=dy,dz_mm=-2,clearance_mm=moving.distance(after),clash_mm3=volume(moving,after)))
    assert all(r['clash_mm3']<1e-6 and r['clearance_mm']>=0.3-1e-6 for r in samples),samples
    x0,x1,y0,y1,z0,z1=m.PCB10_JP1_RELIEF
    walls=dict(left_mm=x0-(-12),right_mm=-4-x1,back_mm=y0-(-66),to_lower_screw_bore_mm=z0-(86+1.25))
    assert min(walls.values())>=1.0,walls
    assert after.is_valid and len(after.solids())==1
    extra=BRepAlgoAPI_Cut(after.wrapped,before.wrapped)
    assert extra.IsDone()
    properties=GProp_GProps();BRepGProp.VolumeProperties_s(extra.Shape(),properties)
    added=properties.Mass()
    assert added<1e-6,added
    report=dict(result='PASS',source_main_sha256=hashlib.sha256((HERE/'makad-v1.step.py').read_bytes()).hexdigest(),material_note='Side widths describe the new pocket below its junction with the pre-existing full-width header-row groove.',added_material_mm3=added,removed_material_mm3=before.volume-after.volume,old_clash_mm3=planted,new_clash_mm3=volume(jp1,after),relief_box=m.PCB10_JP1_RELIEF,remaining_material=walls,min_sampled_clearance_mm=min(r['clearance_mm'] for r in samples),samples=samples,scope='JP1 against upright 1; static plus sampled 2 mm vertical slide and front approach; structural strength and other installation paths not asserted')
    (HERE/'pcb10-jp1-relief-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
