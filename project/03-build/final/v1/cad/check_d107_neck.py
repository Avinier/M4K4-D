"""D-107 geometry gates against actual final-owned edits, not study summaries.

Legacy runtime; run from the repository root with MAKAD_RELIEF_SERIAL=1.
This is geometric evidence only. Camera function, conductor fatigue, received
plug dimensions and unmodelled connector dress stay physical release holds.
"""
import json
import math
from pathlib import Path
import numpy as np
from build123d import Location, Wire
import module_checks as C
import d107_umbilical as U
from study_umbilical_span import Head, bend_radius

HERE=Path(__file__).resolve().parent


def line(points):
    return Wire.make_polygon([tuple(p) for p in points],close=False)


def trim_end(points,length):
    p=np.asarray(points,float).tolist()
    while length>0 and len(p)>1:
        a,b=np.asarray(p[-2]),np.asarray(p[-1]);d=np.linalg.norm(b-a)
        if d<=length:p.pop();length-=d
        else:p[-1]=(b-length*(b-a)/d).tolist();length=0
    return p


def nearby_distance(points,parts,radius):
    path=line(points);b=C._box(path);best=(999.,None)
    for name,shape in parts.items():
        if not C._hit(b,C._box(shape),radius+4.): continue
        gap=C.distance(path,shape)-radius
        if gap<best[0]: best=(gap,name)
    return best


def main():
    entry=C.load_entry()
    import layout_model as m
    parts=m.build_parts(catalog=False)
    C.log('head parts built')
    report=C.Report('check_d107_neck')
    import re
    physical={n:d['shape'] for n,d in parts.items() if d['kind']=='physical' and not any(re.fullmatch(p,n) for p in entry.DROID_REMOVES)}
    frames={n:d['frame'] for n,d in parts.items()}
    skin='main_octagonal_skin_lower'
    cut=U.opening()
    cut_hits=[(n,round(C.common(cut,s),4)) for n,s in physical.items()
              if C._hit(C._box(cut),C._box(s)) and C.common(cut,s)>1e-4]
    report.check('opening_cuts_lower_skin_only',len(cut_hits)==1 and cut_hits[0][0]==skin,hits=cut_hits)
    opened=physical[skin]-cut
    edited=opened+U.collar()
    upper=physical['main_octagonal_skin']+U.head_camera_mount()
    report.check('lower_skin_and_collar_fused',edited.is_valid and len(edited.solids())==1,
                 solids=len(edited.solids()),valid=bool(edited.is_valid),volume_delta_mm3=C.volume(edited)-C.volume(physical[skin]))
    report.check('head_camera_mount_fused_to_roof',upper.is_valid and len(upper.solids())==1,
                 solids=len(upper.solids()),valid=bool(upper.is_valid))
    # The collar is an intentional cable contact. The opening edge itself is
    # checked with the cut skin, including the whole cable and both endpoints.
    physical[skin]=opened
    physical['main_octagonal_skin']=upper
    for n in ('C2_removable_open_rear_tray','C2_tray_M2_-39','C2_tray_M2_-19'):
        physical.pop(n,None)
    data=U.route_data()
    head=Head(dict(origin=np.asarray(entry.HEAD_ORIGIN_IN_CHASSIS),
                   pitch_axis=np.array([m.PITCH_AXIS.position.X,0,m.PITCH_AXIS.position.Z]),
                   roll_axis=np.array([0,m.ROLL_AXIS.position.Y,m.ROLL_AXIS.position.Z]),
                   yaw_axis_x=np.array([m.YAW_AXIS.position.X])))
    pools={f:{n:s for n,s in physical.items() if frames[n]==f} for f in ('Y','P','R')}
    minima={f:(999.,None,None) for f in pools}
    opening_min=(999.,None)
    for row in data['routes']:
        q,r=row['pitch'],row['roll'];points=np.asarray(row['points'])
        for f,pool in pools.items():
            local=head.to_frame(points,f,0,q,r)
            gap,name=nearby_distance(local,pool,U.RADIUS)
            if gap<minima[f][0]: minima[f]=(round(gap,4),name,(q,r))
        local=head.to_frame(points,'R',0,q,r)
        gap=C.distance(line(local),opened)-U.RADIUS
        if gap<opening_min[0]: opening_min=(round(gap,4),(q,r))
    report.check('neck_clear_of_head_over_45_poses',all(v[0]>=3 for v in minima.values()),
                 minima=minima,poses=len(data['routes']),radius_mm=U.RADIUS,
                 note='exact OCC distance from every piecewise-linear centreline segment minus bundle radius; yaw symmetry about the bore')
    report.check('opening_edge_margin',opening_min[0]>=2.,minimum_mm=opening_min,opening=U.OPENING)
    chord=max(row['chord'] for row in data['rows'])
    report.check('free_length_slack',U.FREE_LENGTH>=1.1*chord,free_mm=U.FREE_LENGTH,
                 longest_span_mm=chord,margin_pct=100*(U.FREE_LENGTH/chord-1),
                 bend_radius_min_mm=min(bend_radius(np.asarray(r['points'])) for r in data['routes']),
                 twist_deg_per_mm=61/U.FREE_LENGTH,
                 solver_residual=data['summary']['resid_max'],note='solver force/torque are estimates, not an equilibrium certificate')
    restored=('pitch_trunnion_D6x12_pin','pitch_trunnion_bearing_MR106ZZ','pitch_trunnion_retainer',
              'pitch_trunnion_retainer_M2x4_240','pitch_trunnion_retainer_M2x4_300')
    report.check('d051_pivot_restored',all(n in physical and not any(re.fullmatch(p,n) for p in entry.DROID_REMOVES) for n in restored),
                 labels=list(restored),leg_channel_edits=any(p=='yaw_yoke_leg_-55' for p,_ in entry.DROID_CUTS+entry.DROID_ADDS))
    # Camera and collar motion against the other frames (own seating is excluded).
    additions={**{f'B0091_{n}':s for n,s in U.camera_parts(U.HEAD_BOARD).items()},
               'B0091_RETAINING_TIE':U.camera_tie(U.HEAD_BOARD,True),
               'CLAMP_BAR':U.clamp_bar(),'COLLAR':U.collar(),
               **{f'CLAMP_SCREW_{i}':s for i,s in enumerate(U.clamp_screws())},
               **{f'CLAMP_INSERT_{i}':s for i,s in enumerate(U.clamp_inserts())},
               **{f'GHR_{n}':s for n,s in U.pcb12_plugs().items()}}
    closest=(999.,None,None);hits=[]
    for row in data['routes']:
        q,r=row['pitch'],row['roll']
        for name,shape in additions.items():
            posed=shape.rotate(m.ROLL_AXIS,r).rotate(m.PITCH_AXIS,q)
            for f in ('P','Y'):
                for other,obstacle in pools[f].items():
                    target=obstacle.rotate(m.PITCH_AXIS,q) if f=='P' else obstacle
                    if not C._hit(C._box(posed),C._box(target),4.): continue
                    gap=C.distance(posed,target)
                    if gap<closest[0]: closest=(round(gap,4),f'{name}/{other}',(q,r))
                    if gap<.2: hits.append((name,other,q,r,round(C.common(posed,target),4)))
    report.check('camera_and_clamp_clear_of_pitch_and_yaw',not hits,minimum_mm=closest,clashes=hits[:30])
    grip_min=min(C.distance(line(head.to_frame(np.asarray(row['points']),'R',0,row['pitch'],row['roll'])),
                            U.clamp_bar())-U.RADIUS for row in data['routes'])
    tools=[U.xc(1.3,U.CLAMP[0]+3,U.CLAMP[0]+18,y,4.) for y in (-9.5,9.5)]
    tool_hits=[n for tool in tools for n,s in pools['R'].items()
               if C._hit(C._box(tool),C._box(s)) and C.common(tool,s)>1e-4]
    report.check('clamp_grip_and_tool_access',grip_min>=0 and not tool_hits,
                 hard_jaw_min_mm=grip_min,tool_diameter_mm=2.6,tool_reach_mm=15,clashes=tool_hits,
                 note='soft silicone pads grip a bundle repacked/taped to6.8 +/-0.05mm; actual grip requires physical acceptance; remove front jaw along +X')
    # Actual PCB-12 parts replace its proxy before internal wire checks.
    import pcb_integration as P
    physical.pop('C2_ESP32_S3_Zero_23_5x18_footprint',None)
    pools['R'].pop('C2_ESP32_S3_Zero_23_5x18_footprint',None)
    loc=P.placements(12,entry._body,(0,0,0))[0][1]
    for name,sh in P.raw_parts(12):pools['R']['PCB12_'+name]=P.placed_copy(sh,loc)
    # Internal fan-outs: static in R, the servo lead in P, and a fixed
    # 30 mm loose loop between the two frames. Mating contact at the servo
    # port is excluded only over the last 3 mm of that lead.
    import head_harness as H
    for n,sh in U.camera_parts(U.HEAD_BOARD).items(): pools['R']['B0091_'+n]=sh
    pools['R']['B0091_RETAINING_TIE']=U.camera_tie(U.HEAD_BOARD,True)
    pools['R']['CLAMP_JAW']=U.clamp_bar()
    pools['R']['CLAMP_COLLAR']=U.collar()
    for n,sh in U.pcb12_plugs().items():pools['R']['GHR_'+n]=sh
    paths=H.lead_paths()
    static=[]
    for name,points in paths.items():
        radius=.8 if name=='PCB12_J2_BRANCH' else (1.8 if name=='HEAD_CAMERA_HDMI' else (1. if name=='DISPLAY_POWER' else 1.5))
        near=(999.,None,None)
        for row in data['routes']:
            q,roll=row['pitch'],row['roll']
            world=head.to_world(points,'R',0,q,roll)
            for f,pool in pools.items():
                local=head.to_frame(world,f,0,q,roll)
                own={'PCB12_J1':'GHR_J1','PCB12_J2_BRANCH':'GHR_J2',
                     'HEAD_CAMERA_HDMI':'B0091_HDMI_MATED_PLUG_E'}.get(name)
                gap,other=nearby_distance(local,{n:s for n,s in pool.items() if n!=own},radius)
                if f=='R' and own and name!='HEAD_CAMERA_HDMI':
                    # Exclude only the final 2.5 mm seated in its own connector.
                    trimmed=trim_end(local,2.5)
                    own_gap=C.distance(line(trimmed),pool[own])-radius
                    if own_gap<gap:gap,other=own_gap,own
                if gap<near[0]:near=(round(gap,4),other,(q,roll))
        static.append((name,near))
    plug=U.camera_parts(U.HEAD_BOARD)['HDMI_MATED_PLUG_E']
    port=H.lead_paths()['HEAD_CAMERA_HDMI']
    overlap=C.common(U.tube(port[-2:],1.8),plug)
    report.check('head_hdmi_lead_seated_in_plug',overlap>1.,
                 terminal_overlap_mm3=overlap,terminal=port[-1],
                 note='plug is an E housing envelope; received cable exit and strain relief still need checking')
    report.check('internal_roll_frame_leads_clear',all(x[1][0]>=.2 for x in static),minima=static)
    ffc_hits=[]
    for i,sh in enumerate(H.head_ffc()):
        for row in data['routes']:
            q,roll=row['pitch'],row['roll']
            posed=sh.rotate(m.ROLL_AXIS,roll).rotate(m.PITCH_AXIS,q)
            for f,pool in pools.items():
                if f=='R' and (q!=0 or roll!=0):continue
                for n,s in pool.items():
                    if i==0 and n=='B0091_CSI15_SOCKET_E':continue
                    target=s.rotate(m.ROLL_AXIS,roll).rotate(m.PITCH_AXIS,q) if f=='R' else (s.rotate(m.PITCH_AXIS,q) if f=='P' else s)
                    if C._hit(C._box(posed),C._box(target)) and C.common(posed,target)>1e-4:ffc_hits.append((i,n,q,roll))
    report.check('head_static_camera_ribbon_clear',not ffc_hits,clashes=ffc_hits[:30],poses=len(data['routes']))
    servo_min=(999.,None,None);loop_min=(999.,None,None);loop_radius=999.
    for row in data['routes']:
        q,roll=row['pitch'],row['roll']
        loop=H.servo_loop(roll,(0,m.ROLL_AXIS.position.Y,m.ROLL_AXIS.position.Z))
        loop_radius=min(loop_radius,bend_radius(loop))
        for f,pool in pools.items():
            world=head.to_world(loop,'P',0,q,roll)
            local=head.to_frame(world,f,0,q,roll)
            gap,other=nearby_distance(local,pool,1.5)
            if gap<loop_min[0]:loop_min=(round(gap,4),other,(q,roll))
            p=np.asarray(H.SERVO_P_PATH,float).copy()
            end=p[-1];direction=(end-p[-2])/np.linalg.norm(end-p[-2]);p[-1]=end-3*direction
            world=head.to_world(p,'P',0,q,roll);local=head.to_frame(world,f,0,q,roll)
            gap,other=nearby_distance(local,pool,1.5)
            if gap<servo_min[0]:servo_min=(round(gap,4),other,(q,roll))
    report.check('servo_roll_crossing_and_pitch_lead_clear',servo_min[0]>=.2 and loop_min[0]>=.2,
                 pitch_lead=servo_min,roll_loop=loop_min,loop_length_mm=H.SERVO_LOOP_LENGTH,loop_min_bend_radius_mm=loop_radius)
    report.finish()


if __name__=='__main__': main()
