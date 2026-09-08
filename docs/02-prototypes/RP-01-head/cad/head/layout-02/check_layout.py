"""Deterministic full-size packaging checks; no continuous-motion certificate."""
import json,itertools,math,sys
from pathlib import Path
import layout_model as m
from build123d import CenterOf
HERE=Path(__file__).parent
parts=m.build_parts(catalog=False)
def overlap(a,b):
    aa,bb=a.bounding_box(),b.bounding_box()
    if any(tuple(aa.max)[i]<=tuple(bb.min)[i]+1e-7 or tuple(bb.max)[i]<=tuple(aa.min)[i]+1e-7 for i in range(3)):return 0.
    return sum(max(0,c.volume) for c in m.pieces(a.intersect(b)))
def pose(s,f,r,p):
    if f=='R':s=s.rotate(m.ROLL_AXIS,r)
    if f in 'RP':s=s.rotate(m.PITCH_AXIS,p)
    return s
dimensions={n:dict(min=list(d['shape'].bounding_box().min),max=list(d['shape'].bounding_box().max),solids=len(d['shape'].solids()),valid=d['shape'].is_valid,volume=d['shape'].volume) for n,d in parts.items()}
# Catalog and electronics silhouettes are conservatively bounding envelopes.
external=[n for n,d in parts.items() if d['owner']=='M019a']
moving=external+['display_module_1to1_envelope','display_connector_and_flashing_access_reserve','camera_module_3_wide_1to1','removable_camera_edge_bracket_trial','C2_ESP32_S3_Zero_23_5x18_footprint','C2_installed_components_reserve','connected_rolling_cradle_flange_ear_stalks']
supports=['yaw_yoke_leg_-55','yaw_yoke_leg_55','yaw_yoke_spindle_bridge','pitch_servo_to_yoke_adapter_trial','pitch_XC330_1to1_reference','connected_pitch_frame_roll_servo_saddle','bearing_cartridge_trial','roll_XC330_1to1_reference']
pairs=list(itertools.product(moving,supports))
# Pitch-only moving parts must also clear the yaw-carried yoke and servo.
pairs += list(itertools.product(['connected_pitch_frame_roll_servo_saddle','bearing_cartridge_trial','roll_XC330_1to1_reference'],['yaw_yoke_leg_-55','yaw_yoke_leg_55','yaw_yoke_spindle_bridge','pitch_servo_to_yoke_adapter_trial','pitch_XC330_1to1_reference']))
hits=[];minz=[]
rolls=[-18,-15,-6,0,6,15,18];pitches=[-22,-15,-5,0,10,20,30,40]
if '--neutral' in sys.argv:rolls=[0];pitches=[0]
for r,p in itertools.product(rolls,pitches):
    posed={n:pose(d['shape'],d['frame'],r,p) for n,d in parts.items()}
    for a,b in pairs:
        v=overlap(posed[a],posed[b])
        if v>1e-4:hits.append(dict(roll=r,pitch=p,a=a,b=b,volume_mm3=round(v,4)))
    minz.append(min(posed[n].bounding_box().min.Z for n in external))
    print(f'pose roll={r} pitch={p}: {len(hits)} cumulative hits',flush=True)
# Static shell, aperture and packages: no designed physical overlap permitted.
static=[]
for a,b in itertools.product(external,['display_module_1to1_envelope','camera_module_3_wide_1to1','addressable_status_LED_package_reserve','removable_camera_edge_bracket_trial']):
    v=overlap(parts[a]['shape'],parts[b]['shape'])
    if v>1e-4:static.append(dict(a=a,b=b,volume_mm3=round(v,4)))
active=parts['active_display_95_04x53_86']['shape']
visible=m.prism(99,11,69,3,-4,0)
screen_excluded=active.volume-overlap(active,visible)
outer_caps={}
for sign in [-1,1]:
    s=parts[f'ear_{sign}_hollow_removable_cap']['shape']
    outer_caps[str(sign)]=sum(f.area for f in s.faces() if f.bounding_box().size.Y<1e-5 and abs(f.center().Y-sign*75)<1e-5)
worst={}
for h in hits:
    k=h['a']+' / '+h['b']
    if k not in worst or h['volume_mm3']>worst[k]['volume_mm3']:worst[k]=h
result=dict(method='Conservative 1:1 package BREP overlaps; 56 discrete poses (7 roll × 8 pitch), distinct from relief design samples. Intended bearing/shaft contacts omitted.',axes=m.AXES,poses=len(rolls)*len(pitches),pairs_per_pose=len(pairs),hits=hits,worst_by_pair=worst,static_package_hits=static,active_area_excluded_mm3=screen_excluded,outer_cap_face_area_mm2=outer_caps,lowest_sampled_shell_z=min(minz),bounds=dimensions,limitations=['No continuous sweep, cable flex, optical field of view, body/yaw model, manufacturing tolerance or structural certification.','Servo references remain unselected. Board depth, LED installed package, connector and service envelopes are assumptions.'])
(HERE/('neutral-checks.json' if '--neutral' in sys.argv else 'fit-checks.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['poses','pairs_per_pose','worst_by_pair','static_package_hits','active_area_excluded_mm3','outer_cap_face_area_mm2','lowest_sampled_shell_z']},indent=2))
