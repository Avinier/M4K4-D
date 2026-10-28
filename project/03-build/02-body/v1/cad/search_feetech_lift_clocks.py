"""Solid screen of lifted HS against frame, yaw cartridge and bay reservations."""
import json
from pathlib import Path
from build123d import Axis, import_step
import body_v1_model as b

HERE=Path(__file__).parent
source=import_step(HERE/'purchased/waveshare_feetech_st3215_hs_servo.step')
frame=b.body_primary_frame()-b._block(*b.YAW_SERVO_BRACKET)
targets={
    'frame_without_XC330_pad':frame,
    'yaw_housing':b._yaw_housing(),
    'yaw_clamp_ring':b._yaw_clamp_ring(),
    'yaw_cassette_stator':b._yaw_cassette_stator(),
    'yaw_hub':b._yaw_hub(),
    'PCB09':b._c0_link_adapter(),
    'fan_web':b._block(*b.FAN_WEB_X,*b.FAN_WEB_Y,*b.FAN_WEB_Z),
}

def q(s):
    bb=s.bounding_box()
    return tuple((getattr(bb.min,k),getattr(bb.max,k)) for k in 'XYZ')

def hit(a,c):
    return all(lo<hi2 and lo2<hi for (lo,hi),(lo2,hi2) in zip(q(a),q(c)))

def vol(a,c):
    total=0.0
    for sa in a.solids():
        for sc in c.solids():
            if hit(sa,sc):
                v=sa & sc
                if v is not None: total+=v.volume
    return round(total,3)

rows=[]
for lift in (12,15):
    for clock in (0,90,180,270):
        s=source.rotate(Axis.X,-90).rotate(Axis.Z,clock)
        s=s.translate((b.BODY_AXIS_X+b.YAW_PINION_CENTER[0],
            b.YAW_PINION_CENTER[1],b.YAW_SERVO_TOP_Z+lift-s.bounding_box().max.Z))
        r={'lift_mm':lift,'clock_deg':clock,'bounds_mm':q(s),'overlap_mm3':{}}
        for name,t in targets.items():
            if hit(s,t):
                v=vol(s,t)
                if v>.001:r['overlap_mm3'][name]=v
        rows.append(r)
        print(lift,clock,r['overlap_mm3'],flush=True)
(HERE/'generated/feetech-yaw-lift-clock-screen.json').write_text(json.dumps(rows,indent=2)+'\n')
