"""D-107 rev B PCB, plugs, camera receiver, clamps and bore passage.

Actual edited body/chassis solids; vendor Pi is surveyed face by face rather
than replaced by a single obstructing bounding envelope.
"""
from pathlib import Path
from build123d import Axis, Compound, Location, Wire
import module_checks as C
import d107_umbilical as U
import pcb_integration as P
from module_checks import face_boxes


def main():
    entry,tree,leaves=C.droid_tree(revb_pcb08=False)   # this check installs rev B itself
    report=C.Report('check_d107_body')
    loc=P.placements(8,entry._body,entry.HEAD_ORIGIN_IN_CHASSIS)[0][1]
    board=P.installed_board(8,'MAIN',loc)
    plugs=P.pcb08_mated_plugs(board,entry._body)
    import head_harness as H
    moving=entry._apply_droid_cuts(Compound(children=entry._body.yaw_drive_moving_parts()),strict=False)
    moving_leaves=[C.Leaf(p,C.place(n,l),False) for p,n,l in C._leaves(moving)]
    leaves+=moving_leaves
    pi=C.find(leaves,'C0_RASPBERRY_PI5_EXACT_STEP')
    faces=face_boxes(pi.shape)
    skip=('YAW_JUNCTION','C0_RASPBERRY_PI5_EXACT_STEP')
    for item in [*board.children,*plugs]:
        bb=C._box(item)
        collisions=C.clashes(item,leaves,skip=skip)
        face_hits=[b for b in faces if C._hit(bb,b)]
        report.check(item.label+'_clear',not collisions and not face_hits,
                     clashes=collisions,pi_face_bbox_hits=len(face_hits),bounds=bb)
    # Body and receiver mounts must join the existing single frame.
    frame=C.find(leaves,'BODY_FRAME_MAIN_PRINT').shape
    report.check('frame_with_mounts_is_one_valid_solid',frame.is_valid and len(frame.solids())==1,
                 solids=len(frame.solids()),valid=bool(frame.is_valid),pieces=[(C.volume(s),C._box(s)) for s in frame.solids()])
    for label,shape in [('BODY_CAMERA_MOUNT',U.body_camera_mount()),('BODY_CLAMP',U.body_clamp()),('PCB08_CRADLE',U.pcb08_cradle())]:
        collisions=C.clashes(shape,leaves,skip=('BODY_FRAME_MAIN_PRINT','D107_PCB08_KEEPER_M2X4','C0_RASPBERRY_PI5_EXACT_STEP'))
        pi_hits=[i for i,b in enumerate(faces) if C._hit(C._box(shape),b) and C.common(shape,C.bbox_shape(b))>1e-4]
        report.check(label+'_external_clearance',not collisions and not pi_hits,clashes=collisions,pi_face_hits=pi_hits)
    for label,shape in {**U.camera_parts(U.BODY_BOARD),'RETAINING_TIE':U.camera_tie(U.BODY_BOARD)}.items():
        collisions=C.clashes(shape,leaves,skip=('D107_B0091_BODY_','C0_RASPBERRY_PI5_EXACT_STEP'))
        ph=[b for b in faces if C._hit(C._box(shape),b)]
        report.check('B0091_BODY_'+label+'_clear',not collisions and not ph,clashes=collisions,pi_face_hits=len(ph))
    # The main axial passage remains clear after removing the stator. The
    # bushing and liner are intentional passage walls, not obstacles.
    bore=U.zc(9.,120.,156.,16.)
    collisions=C.clashes(bore,leaves,skip=('D107_ROTOR_SMOOTH_LINER','D107_DISC_BORE_BUSHING'))
    report.check('diameter18_axial_passage',not collisions,clashes=collisions)
    centre=Wire.make_polygon(U.body_path(),close=False)
    tube=U.tube(U.body_path(),U.RADIUS)
    collisions=C.clashes(tube,leaves,skip=('D107_ROTOR_SMOOTH_LINER','D107_DISC_BORE_BUSHING','D107_B0091_BODY_',
                                         'BODY_FRAME_MAIN_PRINT','C0_RASPBERRY_PI5_EXACT_STEP','YAW_JUNCTION'))
    # Face boxes are conservative local Pi bounds, including pins and ports.
    pi_hits=[b for b in faces if C._hit(C._box(tube),b) and C.common(tube,C.bbox_shape(b))>1e-4]
    report.check('body_run_clear',not collisions and not pi_hits,clashes=collisions,pi_face_hits=len(pi_hits))
    gap=C.distance(centre,frame)-U.RADIUS
    report.check('body_bundle_clear_of_own_mounts',gap>=.2,minimum_mm=gap)
    # Use centreline distance, not an overlapping Compound cable Boolean.
    # The latter can omit parts of a nested or self-overlapping cable shell.
    real=[C.Leaf((x.label,),x,False) for x in [*board.children,*plugs]]
    wire_min=[]
    for name,pts,radius,colour in H.body_wire_paths():
        path=Wire.make_polygon(pts,close=False);near=(999.,None)
        own='J8_9_MATED' if 'AWG22' in name or any(t in name for t in ('+5V_','GND_C2','GND_DISPLAY')) else 'J8_10_MATED'
        for lf in [*leaves,*real]:
            if not C.is_part(lf.path) or lf.vendor or 'YAW_JUNCTION' in '/'.join(lf.path):continue
            if own in lf.label or ('STRIPPED_HDMI' in name and 'D107_B0091_BODY_HDMI' in lf.label):continue
            if not C._hit(C._box(path),lf.box,radius+2):continue
            d=C.distance(path,lf.solid)-radius
            if d<near[0]:near=(d,lf.label)
        wire_min.append((name,near))
    report.check('individual_body_wires_clear',all(v[0]>=.1 for n,v in wire_min),minima=wire_min)
    ribbons=H.body_ffc()
    report.check('body_camera_ribbon_continuous_valid',len(ribbons)==1 and ribbons[0].is_valid and len(ribbons[0].solids())==1,
                 pieces=len(ribbons),solids=len(ribbons[0].solids()),valid=bool(ribbons[0].is_valid),
                 note='mitered thin envelope and tapered15-to22 end; received fold and contact orientation remain U')
    ribbon_hits=[]
    for i,sh in enumerate(ribbons):
        hit=C.clashes(sh,leaves,skip=('C0_RASPBERRY_PI5_EXACT_STEP','PI5_ACTIVE_COOLER_STEP','D107_B0091_BODY_CSI15_SOCKET_E'))
        # Pi surfaces lie below the ribbon including its actual CSI mouth;
        # the cooler's bounding box crosses the CSI corridor, so test real BREP.
        # One continuous ribbon spans the receiver and Pi, so its overall
        # bounding box contains unrelated Pi faces. Test the actual Pi BRep.
        pf=[b for b in faces if C._hit(C._box(sh),b)]
        pi_overlap=C.common(sh,pi.shape) if pf else 0.
        cooler=C.find(leaves,'PI5_ACTIVE_COOLER_STEP')
        cv=C.common(sh,cooler.shape) if C._hit(C._box(sh),cooler.box) else 0
        if hit or pi_overlap>1e-4 or cv>1e-4:ribbon_hits.append((i,hit,len(pf),cv,pi_overlap))
    report.check('body_static_camera_ribbon_clear',not ribbon_hits,clashes=ribbon_hits,
                 pi_csi_mouth_mm=[37.4,-24.72,99.55],note='mouth from imported Pi STEP; received FFC latch/contact dress remains U')
    pull=[]
    for sign,i in ((1,0),(-1,1)):
        for d in range(0,7):
            hit=C.clashes(plugs[i].moved(Location((sign*d,0,0))),leaves,
                          skip=('YAW_JUNCTION','C0_RASPBERRY_PI5_EXACT_STEP'))
            if hit:pull.append((plugs[i].label,d,hit))
    report.check('microfit_straight_pull_6mm',not pull,clashes=pull,note='shell removed and neck harness slack released')
    removal=[];axis=Axis((0,-46,112.8),(1,0,0))
    poses=[(a,0,0) for a in range(0,16,1)]+[(15,d,0) for d in range(1,7)]+[(15,6,dx) for dx in range(-2,-61,-2)]
    for a,dy,dx in poses:
        for sh in board.children:
            subject=sh.rotate(axis,a).moved(Location((dx,dy,0)))
            hit=C.clashes(subject,leaves,skip=('YAW_JUNCTION','D107_PCB08','C0_RASPBERRY_PI5_EXACT_STEP',
                                            'BODY_SHELL','REAR_SERVICE_PANEL','REAR_PANEL_BUTTON'))
            ph=[b for b in faces if C._hit(C._box(subject),b)]
            if hit or ph:removal.append((sh.label,a,dy,dx,hit,len(ph)))
    report.check('pcb08_service_removal',not removal,clashes=removal[:20],
                 sequence='shell and rear panel off; unplug all five; remove M2×4 and keeper; tilt front15°; slide +Y6mm; withdraw -X60mm')
    report.check('assumed_plug_sections_only',max((13.2**2+7**2)**.5,(16**2+7**2)**.5)<18,
                 microfit_diagonal_mm=(13.2**2+7**2)**.5,hdmi_diagonal_mm=(16**2+7**2)**.5,
                 clear_bore_mm=18,physical_passage_qualified=False,
                 note='ENVELOPE ARITHMETIC ONLY. Buy HDMI cable first; measure full housing/boot. If it fails18mm, do not print/order closed inserts; use head-end unplugging or redesign split inserts for the bare21mm bore.')
    labels=[lf.label for lf in leaves]
    old=[n for n in labels if n.startswith(('YAW_FFC_CASSETTE_STATOR','PCB14_JOINER_','YAW_CASSETTE_M2X6_POST_SCREW_'))]
    report.check('cassette_and_joiners_absent',not old,obsolete=old)
    report.finish()


if __name__=='__main__':main()
