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
        real=[c for c in group.children if c.label.startswith(f"PCB{n:02d}_KICAD_REVA_")]
        expected=P.placements(n,body,head_origin)
        assert len(real)==len(expected),(n,len(real))
        assert not any(any(t in '/'.join(path) for t in ('C3_DEVKITC_V11_','PCB05_AUDIO_FRONT_END_PCB','status_LED_PCB08','PCB13_CHARGE_INLET_PCB','BALL_NOSE_HALL_CARRIER_PCB')) for path,s in walk(group) if not any('_KICAD_REVA_' in label for label in path))
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
            if n==5:
                assert max(abs(a-b) for a,b in zip((bb[0],bb[1],bb[3],bb[4]),(45,-19,75,19)))<0.01
                assert abs(centre[2]-114.8)<0.01
            elif n==6:
                x,y,z,_=next(row for row in body.MICROPHONE_PORTS if row[3]==instance)
                assert abs(centre[0]-x)<0.01 and abs(centre[2]-z)<0.01
                assert abs(abs(centre[1])-(body.MIC_BOARD_OUTER_Y-body.MIC_BOARD_SIZE[1]/2))<0.01
            elif n==9:
                # D-092 outline: strip X -11 (tab), bay to X 66, Y 16.3..39; core centred in the 1.6 mm board on the standoffs
                assert max(abs(a-b) for a,b in zip((bb[0],bb[1],bb[3],bb[4]),(-11,16.3,66,39)))<0.01
                assert abs(centre[2]-107.25)<0.01
            elif n==10:
                assert max(abs(a-b) for a,b in zip((bb[0],bb[3],bb[2],bb[5]),(-14,56,76,125.5)))<0.01
                assert abs(centre[1]+57.6)<0.01
            elif n==11:
                assert abs(centre[1]-15.2)<0.01 and abs(centre[2]-(91.8+head_origin[2]))<0.01
                assert abs(bb[3]+0.035-(-7.2+head_origin[0]))<0.01
            elif n==13:
                assert abs(centre[0]-(body.CHARGE_INLET_BOARD_SEAT_X+0.8))<0.01
                assert max(abs(a-b) for a,b in zip((bb[1],bb[4],bb[2],bb[5]),(-14,14,56.5,71.5)))<0.01
            elif n==15:
                assert abs(centre[0]-126.6)<0.01 and abs(centre[1]-10)<0.01 and abs(centre[2]-32.7)<0.01
            boards.append((n,instance,board))
            records.append(dict(board=n,instance=instance,components=len(board.children)-1,dnp_omitted=sorted(P.dnp_refs(n)),core_bbox=bbox(cores[0]),transform_bbox_error_mm=err))
    assert len(boards)==10
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
        if any('_KICAD_REVA_' in label for label in path):continue
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
                # D-067: the KiCad spacers sit 0.04 mm proud of copper;
                # their intended contact with the printed bosses is measured
                # independently in check_pcb05_mount/fit, not a duplicate part.
                if n==5 and any(part.label.endswith('__H'+str(k)) for k in (1,2,3)) and path[-1]=='BODY_FRAME_MAIN_PRINT':continue
                # D-092: PCB-09's socket mates the Pi header by design; check_pcb09_fit.py measures the stack.
                if n==9 and part.label.endswith('__J1') and 'C0_RASPBERRY_PI5_EXACT_STEP' in path:continue
                d=part.distance(o)
                if d<0.3:contacts.append(dict(part=part.label,obstacle='/'.join(path),gap_mm=d))
                if d<1e-6:
                    v=intersection_volume(part,o)
                    if v>1e-5:static.append(dict(part=part.label,obstacle='/'.join(path),volume_mm3=v))
    return dict(installed_boards=records,board_count=len(boards),cross_board_neighbours=pairs,cross_board_collisions=collisions,static_interferences=static,static_near_contacts=contacts,
                sources={str(n):dict(path=str(P.source_path(n)),sha256=hashlib.sha256(P.source_path(n).read_bytes()).hexdigest()) for n in P.BOARDS},
                scope="replacement count, core transforms, duplicate placeholder removal and static cross-board and robot interference; intentional own fixing/plug contacts, PCB05 spacer/boss contacts and the PCB09 socket on the Pi header excluded; per-board installation sweeps are separate")


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
    print('Checking ten installed boards...',flush=True)
    result=check(robot,m._body,m.HEAD_ORIGIN_IN_CHASSIS)
    if args.from_step:result['checked_step']=dict(path=str(args.from_step),sha256=hashlib.sha256(args.from_step.read_bytes()).hexdigest())
    result['result']='PASS' if not result['cross_board_collisions'] and not result['static_interferences'] else 'FAIL'
    (HERE/'pcb-integration-report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    return 0 if result['result']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
