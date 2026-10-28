"""Trial installed straight branches; unqualified bends terminate at named reserves.

No guessed CSI flex loop is represented as a working connection. R/P/Y islands
are individually anchored; gaps at joints are explicitly recorded, never closed
by a rigid line that stretches under pose. M006/M020 already own cable mass.
"""
import json
from pathlib import Path
from build123d import *
import layout_model as m
import feetech as fe

def rod(p,q,r):
    v=Vector(q)-Vector(p)
    return Solid.make_cylinder(r,v.length,Plane(origin=p,z_dir=v))

def routes():
    items={};gaps=[]
    def put(name,shape,frame,branch,kind='jacket',color='#c98944'):
        items[name]=dict(shape=m.tint(shape,name,color,.75 if kind=='jacket' else .14),frame=frame,branch=branch,kind=kind)
    specs=[
      ('CSI_30mm_straight_exit_R','csi','R',(-18,0,80),(-48,0,80),1.0,'#65a584'),
      ('display_link_30mm_straight_R','display_link','R',(-18,-34,65),(-48,-34,65),1.2,'#4199b6'),
      ('C2_castellated_30mm_straight_R','c2_local','R',(-35,-29,42),(-65,-29,42),1.,'#a688c8'),
    ]
    # D-049: each STS3045M lead leaves its nozzle tip (shaft-end face, near
    # the case bottom) along the case's short side. Straight runs stop at a
    # keep-out; the 5264 plug route and bus daisy chain are not yet drawn.
    (ux,uz),_=fe.u_v();zc=sum(fe.NOZZLE_Z)/2;tip=fe.NOZZLE_TIP_X-.05
    roll0=fe.roll_local_to_head(tip,0,zc)
    pitch0=fe.pitch_local_to_head(tip,0,zc)
    specs+=[
      ('roll_servo_lead_8mm_exit_P','servo_bus','P',roll0,(roll0[0],roll0[1],roll0[2]+8),1.2,'#cb8750'),
      ('pitch_servo_lead_10mm_exit_P','servo_bus','P',pitch0,(pitch0[0]-10*ux,pitch0[1],pitch0[2]-10*uz),1.2,'#cb8750'),
    ]
    for name,branch,frame,p,q,r,color in specs:
        put(name,rod(p,q,r),frame,branch,color=color)
        # Exit centreline is independently hideable with its parent branch.
        put(name+'_centreline',rod(p,q,.12),frame,branch,'centreline','#242e35')
        # Open collar at route end labels the unqualified continuation.
        collar=rod(q,(q[0]-3,q[1],q[2]),3)-rod(q,(q[0]-3,q[1],q[2]),2.5)
        put(name+'_flex_zone_UNROUTED',collar,frame,branch,'keepout',color)
        gaps.append(dict(branch=branch,from_point_mm=q,frame=frame,reason='Stop at labelled keep-out: connector exit drawing and dynamic cable radius/FFC orientation unselected; roll/pitch transition is not qualified.'))
    # LED requires a turn before the 30 mm straight reserve clears the crown.
    put('LED_30mm_exit_UNROUTED',m.block(-38,-8,12.7,17.7,89.3,94.3),'R','led_local','keepout','#d6a647')
    gaps.append(dict(branch='led_local',reason='HEAD-CAD-12: the selected WS2812B-2020 carrier takes 3 x AWG30 PTFE leads (3V3, GND, DIN) on its back pads, turned 90 deg within 2 mm, so no 30 mm straight exit is needed; the route from the crown to D1 GPIO6 (Sensor-AD PH2.0) is not yet drawn, so this keep-out stays.'))
    # D-052: the yaw branch is three stacked 22-pin 0.5 mm FFCs (power,
    # sideband, CSI). They leave the body's PCB-14 joiner boards' upper ZIFs
    # (mouths at body Z 150.7, disc - 4.3, in XZ planes at Y -2.9 / 0.4 / 3.7),
    # rise through the Ø21 disc bore, bend over toward +Y and lie flat in the
    # 12.5 x 1.5 mm disc-top channel (stack about 1.05 mm), then stop at a
    # keep-out below the +Y leg; the riser to the pitch-carried frame remains
    # an unqualified transition. The FFC ends demate through the bore with the
    # tilting assembly off; the disc can stay on.
    x,d=m.PITCH_X,m.YAW_DISC_TOP_Z
    c=m.YAW_FFC_CHANNEL;w=5.9
    floor=d-c['depth']
    put('yaw_FFC_x3_bore_riser_Y',m.block(x-w,x+w,-3.15,3.95,d-4.3,floor+.05),'Y','yaw_service_loop',color='#d3a860')
    put('yaw_FFC_x3_disc_channel_Y',m.block(x-w,x+w,-3.15,c['y1'],floor+.05,floor+1.1),'Y','yaw_service_loop',color='#d3a860')
    put('yaw_branch_leg_riser_UNROUTED',m.block(x-c['half_w'],x+c['half_w'],44,47.6,floor,d+8),'Y','yaw_service_loop','keepout','#d3a860')
    put('CAD05_yaw_plane_demating_reserve',m.block(x-8.5,x+8.5,-4.7,4.7,d-9.5,d),'Y','yaw_service_loop','keepout','#b488cf')
    gaps.append(dict(branch='yaw_service_loop',reason='Y-side branch ends below the +Y leg; riser to the pitch frame is unrouted. Yaw twist is taken by the body-side FFC clock-spring cassette (D-044/D-052), not yet qualified for cycles.'))
    return items,gaps
