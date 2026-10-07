"""Trial HS at the original gear height with the Pi/PCB-09 shifted -Y.

This checks purchased solids, not tray fasteners, cable paths or assembly.
"""
import json
import sys
from pathlib import Path
from build123d import Axis, Compound, Location, import_step
import body_v1_model as b

HERE=Path(__file__).parent
servo=import_step(HERE/'purchased/waveshare_feetech_st3215_hs_servo.step')
servo=servo.rotate(Axis.X,-90)
servo=servo.translate((b.BODY_AXIS_X+b.YAW_PINION_CENTER[0],
    b.YAW_PINION_CENTER[1],b.YAW_SERVO_TOP_Z-servo.bounding_box().max.Z))
dy=float(sys.argv[1]) if len(sys.argv)>1 else -6.0
pi=b.raspberry_pi5().moved(Location((0,dy,0)))
tray=b.compute_tray_print(pi_y_shift=dy)
pcb=b._c0_link_adapter(main_x_shift=6.0).moved(Location((0,dy,0)))
cooler=b._purchased_step('Heatsink+fan RPi-5.STEP','PI5_ACTIVE_COOLER_STEP',[(Axis.X,90.0)])
posts=sorted((s for s in cooler.solids() if 100<s.volume<140),key=lambda s:s.bounding_box().center().X)
post_a=posts[0].bounding_box().center()
plate_z0=max(cooler.solids(),key=lambda s:s.volume).bounding_box().min.Z
cooler=cooler.moved(Location((b.PI_COOLER_HOLE_A[0]-post_a.X,
    b.PI_COOLER_HOLE_A[1]+dy-post_a.Y,b.PI_SOC_TOP_Z-plate_z0)))
cooler=Compound(children=list(cooler.solids()))
frame=b.body_primary_frame()-b._block(*b.YAW_SERVO_BRACKET)
targets={'frame_without_XC330_pad':frame,'tray_with_shifted_Pi_bosses':tray,
         'Pi_shifted':pi,'cooler_shifted':cooler,
         'PCB09_shifted':pcb,'yaw_housing':b._yaw_housing(),
         'cassette':b._yaw_cassette_stator(),
         'fan_web':b._block(*b.FAN_WEB_X,*b.FAN_WEB_Y,*b.FAN_WEB_Z),
         'C3_carrier':b._block(*b.C3_CARRIER_BOARD),
         'shell':b.body_shell()}

def bb(s):
    q=s.bounding_box();return tuple((getattr(q.min,k),getattr(q.max,k)) for k in 'XYZ')

def overlap(a,c):
    return all(a0<c1 and c0<a1 for (a0,a1),(c0,c1) in zip(bb(a),bb(c)))

def volume(a,c):
    v=0.0
    for x in a.solids():
        for y in c.solids():
            if overlap(x,y):
                z=x & y
                if z is not None:v+=z.volume
    return round(v,3)

result={'pi_pcb_shift_y_mm':dy,'pcb09_main_shift_x_mm':6.0,
        'servo_bounds_mm':bb(servo),'overlap_mm3':{},
        'separation_mm':{}}
for name,s in targets.items():
    result['overlap_mm3'][name]=volume(servo,s) if overlap(servo,s) else 0.0
    if name in ('Pi_shifted','cooler_shifted','PCB09_shifted','frame_without_XC330_pad',
                'fan_web','shell'):
        result['separation_mm'][name]=round(servo.distance_to(s),3)
    print(name,result['overlap_mm3'][name],flush=True)
result['pcb09_vs_frame_mm3']=volume(pcb,frame)
result['pcb09_vs_shell_mm3']=volume(pcb,targets['shell'])
result['shifted_pi_vs_tray_mm3']=volume(pi,tray)
result['shifted_pi_vs_tray_regions']=[]
for leaf in pi.solids():
    if overlap(leaf,tray):
        common=leaf & tray
        if common is not None and common.volume>0.001:
            result['shifted_pi_vs_tray_regions'].append({
                'volume_mm3':round(common.volume,3),'bounds_mm':bb(common)})
result['shifted_cooler_vs_tray_mm3']=volume(cooler,tray)
result['shifted_pcb09_vs_tray_mm3']=volume(pcb,tray)
print('PCB09 versus frame/shell',result['pcb09_vs_frame_mm3'],
      result['pcb09_vs_shell_mm3'],flush=True)
out=HERE/('generated/feetech-yaw-compute-shift.json' if len(sys.argv)==1
          else f'generated/feetech-yaw-compute-shift-{abs(dy):g}mm.json')
out.write_text(json.dumps(result,indent=2)+'\n')
