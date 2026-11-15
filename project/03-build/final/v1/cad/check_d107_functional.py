"""D107 support/retention/reach screens omitted by the original clearance checks.

Hand beam/section calculations with explicit E material credit, not FEA or
qualification. The first actual print must pass the stated proof loads.
"""
import math
import numpy as np
from build123d import Location
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import module_checks as C
import d107_umbilical as U
import head_harness as H
import pcb_integration as P

MATERIAL_CREDIT_MPA=20.  # E, must be demonstrated by the selected PETG/process
DESIGN_FACTOR=2.
ALLOWABLE_MPA=MATERIAL_CREDIT_MPA/DESIGN_FACTOR


def section(shape):
    """Unit-height extrusion -> measured planar area and section moduli."""
    p=GProp_GProps();BRepGProp.VolumeProperties_s(shape.wrapped,p)
    a=p.Mass();c=p.CentreOfMass();b=C._box(shape);I=p.MatrixOfInertia()
    ix=I.Value(1,1)-a/12;iy=I.Value(2,2)-a/12
    return a,ix/max(c.Y()-b[1],b[4]-c.Y()),iy/max(c.X()-b[0],b[3]-c.X()),(c.X(),c.Y(),c.Z())


def main():
    e=C.load_entry();r=C.Report('check_d107_functional')
    pc=U.pcb08_cradle();bc=U.body_clamp()
    raw=e._body.body_primary_frame()
    base=next(C.place(sh,l) for p,sh,l in C._leaves(raw) if p[-1]=='BODY_FRAME_MAIN_PRINT')
    joint=pc & base & U.block(28.8,38.4,-47,-29,134,135)
    area,zx,zy,centroid=section(joint)
    rear_root=C.common(pc & U.block(-36,-28,-33,-30,126,134),base)
    r.check('broad_hanger_and_two_real_frame_roots',area>=100 and C.common(pc,base)>200 and rear_root>50,
            plate_attachment_area_mm2=area,section_moduli_X_Y_mm3=[zx,zy],attachment_volume_mm3=C.common(pc,base),
            rear_crossrail_tie_volume_mm3=rear_root,
            hanger_nominal_section_mm=[9.6,18.],note='actual overlap with UNEDITED frame; extra upper tie is not credited in the stress screen')
    connector=50.*24./zy
    cable=40./area+40.*abs(centroid[1]+16.)/zx
    r.check('hanger_connector_and_cable_load_screen',max(connector,cable)<=ALLOWABLE_MPA and 2*connector<=MATERIAL_CREDIT_MPA,
            connector_force_N=50.,cable_pull_N=40.,proof_connector_force_N=100.,
            connector_bending_MPa=connector,cable_axial_plus_bending_MPa=cable,
            assumed_material_credit_MPa=MATERIAL_CREDIT_MPA,nominal_factor=DESIGN_FACTOR,
            note='separate load cases; connector service with harness released. PETG solid modifier at beams/web/roots; verify100N first-print proof without permanent set/cracking')
    # Guaranteed rectangular material below the conservative rotating envelope.
    throat=bc & U.block(32,38.4,-23.1,-22.9,111.5,120.9)
    throat_area=C.volume(throat)/.2
    modulus=6.4*9.4**2/6
    sigma=40*13/modulus
    r.check('body_saddle_gusset_pull_screen',throat_area>=6.4*9.4-.01 and sigma<=ALLOWABLE_MPA,
            guaranteed_section_mm=[6.4,9.4],measured_section_mm2=throat_area,
            pull_N=40.,lever_mm=13.,bending_MPa=sigma,proof100N_MPa=100*13/modulus)
    # Input connector force enters the rear edge stop at the board midplane.
    rear=pc & U.block(-15,-14,-48.5,-46.15,102,112)
    expected=2.35*10
    stress=50/expected+50*(112.8-107)/(2.35*10**2/6)
    r.check('rear_beam_connector_force_screen',C.volume(rear)>=expected-.01 and stress<=ALLOWABLE_MPA,
            measured_section_mm2=C.volume(rear),force_N=50.,axial_plus_bending_MPa=stress,
            factor_to_assumed_material=MATERIAL_CREDIT_MPA/stress,proof100N_MPa=2*stress)
    bearing=50/(4.2*1.53);stop_bend=50*1.6/(4.2*3.85**2/6)
    r.check('board_edge_stop_bearing_screen',max(bearing,stop_bend)<=ALLOWABLE_MPA,
            stop_thickness_mm=3.85,engaged_length_mm=4.2,bearing_MPa=bearing,bending_MPa=stop_bend,
            note='does not qualify connector solder joints or FR4; support the housing during first mating and proof the complete cradle')
    loc=P.placements(8,e._body,e.HEAD_ORIGIN_IN_CHASSIS)[0][1]
    core=next(s for s in P.installed_board(8,'MAIN',loc).children if s.label.endswith('_PCB'))
    retainer=pc+U.pcb08_keeper();travel={}
    for name,v in [('X+', (1,0,0)),('X-',(-1,0,0)),('Y+',(0,1,0)),('Y-',(0,-1,0)),('Z+',(0,0,1)),('Z-',(0,0,-1))]:
        travel[name]=C.common(core.moved(Location(v)),retainer)
    r.check('pcb08_rigid_capture_in_six_directions',C.common(core,retainer)<1e-4 and all(v>.1 for v in travel.values()),
            translated_1mm_obstruction_mm3=travel,note='keeper fitted; service path deliberately releases the keeper first; not a pull-out strength test')
    for name,points,stock in [('HEAD_15WAY',H.HEAD_FFC_POINTS,H.HEAD_FFC_LENGTH),('PI_22_TO_15',H.BODY_FFC_POINTS,H.BODY_FFC_LENGTH)]:
        points=np.asarray(points);route=float(np.linalg.norm(np.diff(points,axis=0),axis=1).sum());straight=float(np.linalg.norm(points[-1]-points[0]))
        need=route+H.FFC_INSERTION_ALLOWANCE+H.FFC_SERVICE_ALLOWANCE
        r.check(name+'_purchased_length_reaches',stock>=need,stock_mm=stock,routed_mm=route,straight_mm=straight,
                insertion_allowance_mm=H.FFC_INSERTION_ALLOWANCE,service_allowance_mm=H.FFC_SERVICE_ALLOWANCE,reserve_mm=stock-need,
                kit60mm_reaches=60>=need,note='separate BOM ribbon; verify contact face/pin mapping and dress unused length at receipt, never tension the socket')
    r.check('head_clamp_taped_size_specified',True,hard_bore_mm=7.2,pads_each_mm=.25,uncompressed_soft_bore_mm=6.7,
            taped_target_mm=6.8,tolerance_mm=.05,nominal_pad_compression_percent=20.,
            note='repack first, tape to measured size. If bare bundle exceeds6.85mm do not crush it; revise clamp/pads for the received bundle')
    r.finish()


if __name__=='__main__':main()
