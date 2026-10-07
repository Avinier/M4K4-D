"""Packaging check for the provisional HS cradle and shifted compute parts."""
import json
from pathlib import Path
from build123d import Axis, Location, import_step
import body_v1_model as b
from feetech_yaw_cradle import parts

HERE=Path(__file__).parent
servo=import_step(HERE/'purchased/waveshare_feetech_st3215_hs_servo.step').rotate(Axis.X,-90)
servo=servo.translate((b.BODY_AXIS_X+b.YAW_PINION_CENTER[0],
    b.YAW_PINION_CENTER[1],b.YAW_SERVO_TOP_Z-servo.bounding_box().max.Z))
shift=-6.0
pi=b.raspberry_pi5().moved(Location((0,shift,0)))
pcb=b._c0_link_adapter(main_x_shift=6.0).moved(Location((0,shift,0)))
frame=b.body_primary_frame()-b._block(*b.YAW_SERVO_BRACKET)
fan_web=b._block(*b.FAN_WEB_X,*b.FAN_WEB_Y,*b.FAN_WEB_Z)
targets={'servo':servo,'Pi':pi,'PCB09':pcb,'frame_without_pad':frame,
         'yaw_housing':b._yaw_housing(),'cassette':b._yaw_cassette_stator(),
         'shell':b.body_shell(),'fan_web_intended_anchor':fan_web}

def box(s):
    q=s.bounding_box();return tuple((getattr(q.min,k),getattr(q.max,k)) for k in 'XYZ')

def broad(a,c):
    return all(a0<c1 and c0<a1 for (a0,a1),(c0,c1) in zip(box(a),box(c)))

def volume(a,c):
    v=0.0
    for x in a.solids():
        for y in c.solids():
            if broad(x,y):
                z=x & y
                if z is not None:v+=z.volume
    return round(v,3)

result={'compute_shift_y_mm':shift,'pcb09_main_shift_x_mm':6.0,
        'cradle':{}}
mount_parts=parts()
for name,part in mount_parts.items():
    record={'solids':len(part.solids()),'valid':all(s.is_valid for s in part.solids()),
            'overlap_mm3':{}}
    for target,t in targets.items():
        record['overlap_mm3'][target]=volume(part,t) if broad(part,t) else 0.0
        if record['overlap_mm3'][target] > 0.001 and target in ('frame_without_pad','cassette'):
            record.setdefault('regions_mm',{})[target]=[]
            for a in part.solids():
                for c in t.solids():
                    if broad(a,c):
                        h=a & c
                        if h is not None and h.volume>.001:
                            record['regions_mm'][target].append({'volume_mm3':round(h.volume,3),
                                'bounds_mm':box(h)})
    result['cradle'][name]=record
    print(name,record,flush=True)
integrated=frame+mount_parts['cradle']
result['integrated_frame']={'solids':len(integrated.solids()),
    'valid':all(s.is_valid for s in integrated.solids()),
    'servo_overlap_mm3':volume(integrated,servo),
    'Pi_overlap_mm3':volume(integrated,pi),
    'PCB09_overlap_mm3':volume(integrated,pcb)}
print('integrated frame',result['integrated_frame'],flush=True)
(HERE/'generated/feetech-yaw-cradle-fit.json').write_text(json.dumps(result,indent=2)+'\n')
