"""Trial installed straight branches; unqualified bends terminate at named reserves.

No guessed CSI flex loop is represented as a working connection. R/P/Y islands
are individually anchored; gaps at joints are explicitly recorded, never closed
by a rigid line that stretches under pose. M006/M020 already own cable mass.
"""
import json
from pathlib import Path
from build123d import *
import layout_model as m

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
      ('roll_servo_bus_30mm_straight_P','servo_bus','P',(-100,m.ROLL_Y-14,m.ROLL_Z-9),(-100,m.ROLL_Y-44,m.ROLL_Z-9),1.2,'#cb8750'),
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
    gaps.append(dict(branch='led_local',reason='Crown depth cannot accept a 30 mm rearward straight exit. Keep-out only until the on-hand LED exit drawing permits a shorter or differently oriented lead.'))
    # Layout 04: the yaw branch drops through the turntable centre bore into the
    # body-side clock-spring reserve (RP-06). On the Y side it lies flush in the
    # disc-top groove and stops at a keep-out below the +Y leg; the riser to the
    # pitch-carried frame remains an unqualified transition.
    x,d=m.PITCH_X,m.YAW_DISC_TOP_Z
    jacket=rod((x,0,d-m.YAW_DISC_THICKNESS),(x,0,d-1.8),1.5)+rod((x,0,d-1.8),(x,44,d-1.8),1.5)
    put('yaw_branch_bore_and_disc_groove_OD3_Y',jacket,'Y','yaw_service_loop',color='#d3a860')
    put('yaw_branch_leg_riser_UNROUTED',m.block(x-3,x+3,44,50,d-3,d+8),'Y','yaw_service_loop','keepout','#d3a860')
    put('CAD05_yaw_plane_demating_reserve',m.block(x-6,x+6,-6,6,d-m.YAW_DISC_THICKNESS-6,d-m.YAW_DISC_THICKNESS),'Y','yaw_service_loop','keepout','#b488cf')
    gaps.append(dict(branch='yaw_service_loop',reason='Y-side branch ends below the +Y leg; riser to the pitch frame is unrouted. Yaw twist is taken by the RP-06 body-side clock-spring reserve under the disc, not qualified for cycles or bend radius.'))
    return items,gaps
