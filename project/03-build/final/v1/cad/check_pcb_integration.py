"""Verify the final assembly's KiCad replacements and cross-board collisions.

Run in the legacy environment from final/v1/README.md. Writes JSON evidence;
static interferences are errors, small positive clearances are reported. Existing
per-board checks own datasheet heights and assembly sweeps; no new sweep pass is
claimed by this checker.
"""
import importlib.util
import json
import hashlib
import argparse
from pathlib import Path
from build123d import Location, Compound
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import pcb_integration as P

HERE=Path(__file__).resolve().parent


def bbox(s):
    b=s.bounding_box()
    return (*tuple(b.min),*tuple(b.max))


def gap(a,b):
    return max(b[0]-a[3],a[0]-b[3],b[1]-a[4],a[1]-b[4],b[2]-a[5],a[2]-b[5],0)


def intersection_volume(a,b):
    # Work on the physical world-frame OCC shapes; nested Compound's Python
    # boolean operator can discard a parent transform (JP1 planted case).
    common=BRepAlgoAPI_Common(a.wrapped,b.wrapped)
    assert common.IsDone()
    props=GProp_GProps();BRepGProp.VolumeProperties_s(common.Shape(),props)
    return props.Mass()


def walk(node,parent=Location(),path=()):
    path=(*path,node.label or "?")
    here=parent*node.location
    if node.children:
        for c in node.children:yield from walk(c,here,path)
    else:yield path,P.placed_copy(node,parent)


def check(robot,body,head_origin):
    groups=next(c for c in robot.children if c.label=="Custom PCBs")
    boards=[];records=[]
    for n,name in P.GROUPS.items():
        print(f'Checking PCB-{n:02d} replacement and datums...',flush=True)
        group=next(c for c in groups.children if c.label==name)
        revision="REVB" if n==9 else "REVA"
        real=[c for c in group.children if c.label.startswith(f"PCB{n:02d}_KICAD_{revision}_")]
        expected=P.placements(n,body,head_origin)
        assert len(real)==len(expected),(n,len(real))
        assert not any(any(t in '/'.join(path) for t in ('C3_DEVKITC_V11_','status_LED_PCB08','BALL_NOSE_HALL_CARRIER_PCB',
                                                         'YAW_JUNCTION_PCB08_BOARD','YAW_JUNCTION_J8_6_J8_7','PCB14_JOINER_',
                                                         'C2_ESP32_S3_Zero'))
                       for path,s in walk(group) if not any('_KICAD_REV' in label for label in path))
        for board,(instance,loc) in zip(real,expected):
            assert len(board.children)==len(P.raw_parts(n))-len(P.dnp_refs(n))
            cores=[s for s in board.children if s.label.endswith('_PCB')]
            assert len(cores)==1
            source_core=P.placed_copy(next(s for l,s in P.raw_parts(n) if l.endswith('_PCB')),loc)
            err=max(abs(a-b) for a,b in zip(bbox(source_core),bbox(cores[0])))
            assert err<1e-6,(n,instance,err)
            # Independent installed datum checks against the frozen envelopes,
            # rather than checking only that the placement helper agrees with itself.
            bb=bbox(cores[0]);centre=tuple((bb[k]+bb[k+3])/2 for k in range(3))
            if n==9:
                # D-092 mount with the rev B service extension to X 78.
                assert max(abs(a-b) for a,b in zip((bb[0],bb[1],bb[3],bb[4]),(-11,16.3,78,39)))<0.01
                assert abs(centre[2]-107.25)<0.01
            elif n==10:
                assert max(abs(a-b) for a,b in zip((bb[0],bb[3],bb[2],bb[5]),(-14,56,76,125.5)))<0.01
                assert abs(centre[1]+57.6)<0.01
            elif n==11:
                assert abs(centre[1]-15.2)<0.01 and abs(centre[2]-(91.8+head_origin[2]))<0.01
                assert abs(bb[3]+0.035-(-7.2+head_origin[0]))<0.01
            elif n==15:
                assert abs(centre[0]-126.6)<0.01 and abs(centre[1]-10)<0.01 and abs(centre[2]-32.7)<0.01
            elif n==8:      # main plate X -22..10 and the +X extension to 20, Y -44..-23
                assert max(abs(a-b) for a,b in zip((bb[0],bb[1],bb[3],bb[4]),(-22,-44,20,-23)))<0.01
            elif n==12:     # head-local X -25.0 component face, Y -44..-14, Z 8..51.5
                assert abs(bb[0]-(-25.0+head_origin[0]))<0.01 and abs(bb[1]-(-44+head_origin[1]))<0.01
                assert abs(bb[2]-(8+head_origin[2]))<0.01 and abs(bb[5]-(51.5+head_origin[2]))<0.01
            elif n==14 and instance=="JOINER_4_CSI_LOOP":   # D-105 bracket top: 27.2 across Y about the ribbon centre Y -1
                assert abs(bb[4]-bb[1]-27.2)<0.01 and abs((bb[1]+bb[4])/2-(-1.0+head_origin[1]))<0.01 and bb[0]<-125+head_origin[0]
            elif n==14:     # 27.2 mm across the tabs about the yaw axis X 16, Z 133.9..150.7, D-101 plane
                y0=P.PCB14_BOARD_Y0[int(instance[-1])-1]
                assert max(abs(a-b) for a,b in zip((bb[0],bb[3],bb[2],bb[5],bb[1]),(2.4,29.6,133.9,150.7,y0)))<0.01
            elif n==16:     # head-local X -62.4..-26, Y 35.5..54 on the disc top Z -34.5
                assert max(abs(a-b) for a,b in zip((bb[0],bb[1],bb[2],bb[3],bb[4]),
                           (-62.4+head_origin[0],35.5+head_origin[1],-34.5+head_origin[2],-26+head_origin[0],54+head_origin[1])))<0.01
            boards.append((n,instance,board))
            records.append(dict(board=n,instance=instance,components=len(board.children)-1,dnp_omitted=sorted(P.dnp_refs(n)),core_bbox=bbox(cores[0]),transform_bbox_error_mm=err))
    assert len(boards)==11  # PCB-08, 09, 10, 11, 12, 14 x4 (D-105 adds the camera-loop joiner), 15, 16 (D-093/D-095 removed PCB-05, 06, 13)
    # All completed boards against each other, not against their old envelopes.
    pairs=[];collisions=[]
    for i,(n,inst,a) in enumerate(boards):
        for m,jst,b in boards[i+1:]:
            if gap(bbox(a),bbox(b))>3:continue
            best=(float('inf'),None,None)
            for ca in a.children:
                for cb in b.children:
                    if gap(bbox(ca),bbox(cb))>min(best[0],3):continue
                    d=ca.distance(cb)
                    if d<best[0]:best=(d,ca.label,cb.label)
                    if d<1e-6:
                        v=intersection_volume(ca,cb)
                        if v>1e-5:collisions.append(dict(a=ca.label,b=cb.label,volume_mm3=v))
            if best[0]<3:pairs.append(dict(a=f"PCB{n:02d}/{inst}",b=f"PCB{m:02d}/{jst}",gap_mm=best[0],parts=best[1:]))
    # Compare the installed component geometry with the surrounding robot.
    # Own retained fixing/plug hardware is checked by the existing per-board
    # fit scripts; reservations are envelopes, not physical interference.
    obstacles=[]
    for path,shape in walk(robot):
        if any('_KICAD_REV' in label for label in path):continue
        if any(token in '/'.join(path).upper() for token in ('RESERVE','KEEP_OUT','KEEPOUT','OVERLAY','PHYSICS','HARNESS','ENVELOPE')):continue
        obstacles.append((path,shape,bbox(shape)))
    static=[];contacts=[]
    for n,inst,board in boards:
        print(f'Checking PCB-{n:02d}/{inst} static interferences...',flush=True)
        board_box=bbox(board)
        nearby=[(path,o,bb) for path,o,bb in obstacles if P.GROUPS[n] not in path and gap(board_box,bb)<0.3]
        for part in board.children:
            pb=bbox(part)
            for path,o,ob in nearby:
                if gap(pb,ob)>=0.3:continue
                # D-092: PCB-09's socket mates the Pi header by design; check_pcb09_fit.py measures the stack.
                if n==9 and part.label.endswith('__J1') and 'C0_RASPBERRY_PI5_EXACT_STEP' in path:continue
                d=part.distance(o)
                if d<0.3:contacts.append(dict(part=part.label,obstacle='/'.join(path),gap_mm=d))
                if d<1e-6:
                    v=intersection_volume(part,o)
                    if v>1e-5:static.append(dict(part=part.label,obstacle='/'.join(path),volume_mm3=v))
    return dict(installed_boards=records,board_count=len(boards),cross_board_neighbours=pairs,cross_board_collisions=collisions,static_interferences=static,static_near_contacts=contacts,
                sources={str(n):dict(path=str(P.source_path(n)),sha256=hashlib.sha256(P.source_path(n).read_bytes()).hexdigest()) for n in P.BOARDS},
                scope="replacement count, core transforms, duplicate placeholder removal and static cross-board and robot interference; intentional own fixing/plug contacts and the PCB09 socket on the Pi header excluded; the D-095 bought modules are obstacles; per-board installation sweeps are separate")


def main():
    spec=importlib.util.spec_from_file_location('makad_pcb_integration',HERE/'makad-v1.step.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from-step',type=Path,help='Check the actual rebuilt inspection STEP')
    args=parser.parse_args()
    if args.from_step:
        print('Reading rebuilt final STEP...',flush=True)
        robot=P.import_step(str(args.from_step.resolve()))
    else:
        print('Building current final assembly...',flush=True)
        robot=m.build_robot()
    print('Checking the eleven installed boards...',flush=True)
    result=check(robot,m._body,m.HEAD_ORIGIN_IN_CHASSIS)
    if args.from_step:result['checked_step']=dict(path=str(args.from_step),sha256=hashlib.sha256(args.from_step.read_bytes()).hexdigest())
    result['result']='PASS' if not result['cross_board_collisions'] and not result['static_interferences'] else 'FAIL'
    (HERE/'pcb-integration-report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    return 0 if result['result']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
