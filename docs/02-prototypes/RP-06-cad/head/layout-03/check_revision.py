"""Layout 03 exhaustive cross-frame sampling and targeted physical requirements."""
import json,itertools,sys,hashlib
from pathlib import Path
from build123d import *
import layout_model as m
from harness import routes
from optics import cone
from inspection_scene import posed,group_for
HERE=Path(__file__).parent
inputs={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ['layout_model.py','details.py','layout_axes.py','harness.py','optics.py']}
p=m.build_parts(catalog=False)
def overlap(a,b):
    aa,bb=a.bounding_box(),b.bounding_box()
    if any(tuple(aa.max)[i]<=tuple(bb.min)[i]+1e-6 or tuple(bb.max)[i]<=tuple(aa.min)[i]+1e-6 for i in range(3)):return 0.
    return sum(max(0,s.volume) for s in m.pieces(a.intersect(b)))
physical={n:d for n,d in p.items() if d['kind']=='physical' and group_for(n,d)!='fasteners'}
valid={n:dict(valid=d['shape'].is_valid,solids=len(d['shape'].solids()),volume=d['shape'].volume) for n,d in p.items()}
intended={frozenset(['pitch_XC330_1to1_reference','pitch_trunnion_49'])}
pairs=[(a,b) for a,b in itertools.combinations(physical,2) if physical[a]['frame']!=physical[b]['frame'] and frozenset([a,b]) not in intended]
static=[]
for a,b in itertools.combinations(physical,2):
    if physical[a]['frame']==physical[b]['frame']:
        v=overlap(p[a]['shape'],p[b]['shape'])
        if v>1e-4:static.append(dict(a=a,b=b,volume_mm3=v))
h,gaps=routes();jackets={n:d for n,d in h.items() if d['kind']=='jacket'}
prior=None
if '--service-only' in sys.argv:
    prior=json.loads((HERE/'revision-checks.json').read_text())
    assert prior['source_sha256']==inputs and prior['axes']==m.AXES
    assert prior['poses']==56 and not prior['motion_hits'] and not prior['harness_pinches']
    (HERE/'review/motion-before-service-path-repair.json').write_text(json.dumps(prior,indent=2)+'\n')
rolls=[-18,-15,-6,0,6,15,18];pitches=[-22,-15,-5,0,10,20,30,40]
if '--neutral' in sys.argv:rolls=[0];pitches=[0]
if prior:rolls=[];pitches=[]
hits=prior['motion_hits'] if prior else [];pinches=prior['harness_pinches'] if prior else []
for r,q in itertools.product(rolls,pitches):
    shapes={n:posed(d['shape'],d['frame'],r,q,0) for n,d in physical.items()}
    for a,b in pairs:
        v=overlap(shapes[a],shapes[b])
        if v>1e-4:hits.append(dict(roll=r,pitch=q,a=a,b=b,volume_mm3=round(v,5)))
    for n,d in jackets.items():
        s=posed(d['shape'],d['frame'],r,q,0)
        for a,t in shapes.items():
            v=overlap(s,t)
            if v>1e-4:pinches.append(dict(roll=r,pitch=q,branch=n,part=a,volume_mm3=round(v,5)))
    print(f'pose {r:+}/{q:+}: mechanism hits {len(hits)}, jacket hits {len(pinches)}',flush=True)
# Conservative field includes rectangular image corners and finite pupil extent.
fov=cone(m.CAMERA_BOTTOM+14.4);optics=[]
for r,q in itertools.product([-18,0,18],[-22,0,40]):
    c=posed(fov,'R',r,q,0)
    for name in ['front_bezel_integral_camera_crown','window_opaque_mask_110mm','window_clear_optical_area','main_octagonal_skin','crown_status_light_diffuser']:
        v=overlap(c,posed(p[name]['shape'],'R',r,q,0))
        optics.append(dict(roll=r,pitch=q,part=name,intersection_mm3=v))
# Baseline hole at new camera location, prior to optical flare: independent
# 2 mm thick front sheet with old Ø17.2 hole, clipped to crown envelope.
oldrim=m.block(-2,0,-17,17,m.CAMERA_BOTTOM+5,m.CROWN_H)-m.axial(8.6,6,(-1,0,m.CAMERA_BOTTOM+14.4))
oldhit=overlap(fov,oldrim)
stops=[]
for axis,limits,pin,fixed in [('roll',[-18,18],'roll_hard_stop_pin',['bearing_cartridge_trial','roll_bearing_retainer_39.5']),('pitch',[-22,40],'pitch_hard_stop_pin',['yaw_yoke_leg_-55'])]:
    for angle in limits:
        for extra in [0,1]:
            value=angle+(extra if angle>0 else -extra)
            shape=p[pin]['shape'].rotate(m.ROLL_AXIS if axis=='roll' else m.PITCH_AXIS,value)
            volume=sum(overlap(shape,p[n]['shape']) for n in fixed)
            dist=min(shape.distance_to(p[n]['shape']) for n in fixed)
            stops.append(dict(axis=axis,angle=value,at_limit=extra==0,overlap_mm3=volume,distance_mm=dist))
# Access paths: rear tool corridor and top plug corridor vs mechanism, skin excluded
# only for explicitly removed rear cover; do not remove unrelated hardware.
service=[]
for reserve in ['C2_USB_C_installed_plug_reserve','C2_USB_C_withdrawal_BOOT_RESET_service_reserve','C2_BOOT_RESET_rear_tool_access_reserve']:
    for n,d in physical.items():
        if n=='removable_octagonal_rear_cover':continue
        v=overlap(p[reserve]['shape'],d['shape'])
        if v>1e-4:service.append(dict(reserve=reserve,part=n,overlap_mm3=v))
# Rigid extraction checks with only the documented service parts removed.
extraction=[]
tray_names=['C2_removable_open_rear_tray','C2_ESP32_S3_Zero_23_5x18_footprint']
for dx,dz in [(0,z) for z in [5,15,27]]+[(-x,27) for x in [5,15,30,60,100]]:
    for n in tray_names:
        moving=p[n]['shape'].moved(Location((dx,0,dz)))
        for other,d in physical.items():
            if other in tray_names+['removable_octagonal_rear_cover']:continue
            v=overlap(moving,d['shape'])
            if v>1e-4:extraction.append(dict(service='C2 lift +Z27 then rearward',moving=n,other=other,translation=[dx,0,dz],intersection_mm3=v))
for dx in [-3,-10,-25,-40]:
    for n in ['camera_module_3_wide_1to1','removable_camera_edge_bracket_trial']:
        v=overlap(p[n]['shape'].moved(Location((dx,0,0))),p['front_bezel_integral_camera_crown']['shape'])
        if v>1e-4:extraction.append(dict(service='camera on removed front carrier',moving=n,translation=[dx,0,0],intersection_mm3=v))
# Positive retention: a 0.4 mm nudge of the module into its mount must hit plastic.
retention=[]
cam,br=p['camera_module_3_wide_1to1']['shape'],p['removable_camera_edge_bracket_trial']['shape']
pcb,tray=p['C2_ESP32_S3_Zero_23_5x18_footprint']['shape'],p['C2_removable_open_rear_tray']['shape']
gap=cam.distance_to(br)
if gap>0.25:retention.append(dict(service='camera nearest bracket',distance_mm=gap))
for moving,fixed,label,shifts in [
    (cam,br,'camera in bracket',[(-.4,0,0),(.4,0,0),(0,.4,0),(0,-.4,0),(0,0,.4)]),
    (pcb,tray,'C2 PCB in tray',[(-.4,0,0),(0,.4,0),(0,-.4,0),(0,0,.4)]),
]:
    for dx,dy,dz in shifts:
        v=overlap(moving.moved(Location((dx,dy,dz))),fixed)
        if v<=1e-4:retention.append(dict(service=label,translation=[dx,dy,dz],intersection_mm3=v))
# Insert pockets must open through the receiver faces; no leftover membrane.
from details import INSERT_R,FRONT_INSERT_FACE_X,REAR_INSERT_FACE_X
insert_mouths=[]
skin=p['main_octagonal_skin']['shape']
for y,z in m.FRONT_SCREWS:
    v=overlap(skin,m.axial(INSERT_R,.2,(FRONT_INSERT_FACE_X,y,z)))
    if v>1e-4:insert_mouths.append(dict(side='front',y=y,z=z,plastic_mm3=v))
for y,z in m.REAR_SCREWS:
    v=overlap(skin,m.axial(INSERT_R,.2,(REAR_INSERT_FACE_X,y,z)))
    if v>1e-4:insert_mouths.append(dict(side='rear',y=y,z=z,plastic_mm3=v))
result=dict(motion_evidence_reused=bool(prior),motion_poses_executed_this_run=len(rolls)*len(pitches),C2_extraction_path='Neutral service pose; unplug and unfasten, lift 27mm in +Z, then withdraw rearward in -X with rear cover removed. PCB stay-with-tray keepers are integral to the tray.',axes=m.AXES,source_sha256=inputs,service_extraction_hits=extraction,retention_misses=retention,insert_mouth_plastic=insert_mouths,intended_pair_exclusions=[sorted(x) for x in intended],poses=prior['poses'] if prior else len(rolls)*len(pitches),mechanism_pairs_per_pose=len(pairs),jacket_pairs_per_pose=len(jackets)*len(physical),same_frame_hits=static,motion_hits=hits,harness_pinches=pinches,optical_pose_checks=optics,old_aperture_conservative_vignetting_mm3=oldhit,optics_assumption='102° horizontal, vertical tangent from 16:9; pupil at X−8 and entrance half-size3mm, front of lens X−2; no entrance-pupil measurement or optical certification.',hard_stops=stops,C2_service_hits=service,solids=valid,harness_gaps=gaps,limitations=['Discrete poses, no continuous-sweep or tolerance certificate.','Rigid harness islands stop before unqualified transitions; no electrical continuity or cable flex/endurance claim.','Yaw loop R8 is a visible trial, not a selected cable bend radius; body anchor absent.','Camera and C2 keepers are trial printed snaps/channels, not purchased hardware or certified retention.'])
errors=bool(extraction or retention or insert_mouths or static or hits or pinches or service or any(x['intersection_mm3']>1e-4 for x in optics) or any(not d['valid'] or d['solids']!=1 or d['volume']<=0 for d in valid.values()) or any((s['overlap_mm3']>1e-4 or s['distance_mm']>.01) if s['at_limit'] else s['overlap_mm3']<1e-4 for s in stops))
result['passed']=not errors
path=HERE/('revision-neutral.json' if '--neutral' in sys.argv else 'revision-checks.json');path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['passed','service_extraction_hits','retention_misses','insert_mouth_plastic','same_frame_hits','motion_hits','harness_pinches','C2_service_hits','hard_stops','old_aperture_conservative_vignetting_mm3']},indent=2))
raise SystemExit(1 if errors else 0)
