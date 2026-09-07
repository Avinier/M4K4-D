"""Reproduce bounded packaging checks with CAD runtime; not a continuous collision certificate."""
import importlib.util,json,itertools
from pathlib import Path
from build123d import Axis
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('layout',HERE/'head-layout.step.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
parts=m.build_parts(catalog=False)
ra=Axis((0,m.ROLL_Y,m.ROLL_Z),(1,0,0))
pa=Axis((m.PITCH_X,0,m.PITCH_Z),(0,1,0))
def pose(s,f,r,p):
    if f=='R':s=s.rotate(ra,r)
    if f in 'RP':s=s.rotate(pa,p)
    return s
def overlap(a,b):
    aa,bb=a.bounding_box(),b.bounding_box()
    if any(tuple(aa.max)[i]<=tuple(bb.min)[i] or tuple(bb.max)[i]<=tuple(aa.min)[i] for i in range(3)):return 0.
    c=a.intersect(b)
    return (c.volume if hasattr(c,'volume') else sum(s.volume for s in c)) if c else 0.

# These pairings deliberately exclude designed shaft/bearing/hub contacts.
pairs=[]
for ear in ['rolling_ear_-1','rolling_ear_1']:
    for fixed in ['yaw_yoke_leg_-55','yaw_yoke_leg_55','pitch_servo_envelope']:
        pairs.append((ear,fixed))
for moving in ['main_skin_with_trial_neck_reliefs','display_board_glass_envelope','C2_board_mount_reserve']:
    for fixed in ['yaw_yoke_leg_-55','yaw_yoke_leg_55','pitch_servo_envelope','bearing_cartridge_reserve','pitch_frame_crossmember']:
        pairs.append((moving,fixed))
hits=[]; mins=[]
roll_samples=[-18,-15,-6,0,6,15,18]
pitch_samples=[-22,-15,-5,0,10,20,30,40]
for roll,pitch in itertools.product(roll_samples,pitch_samples):
    placed={n:pose(s,f,roll,pitch) for n,(s,f) in parts.items()}
    for a,b in pairs:
        v=overlap(placed[a],placed[b])
        if v>1e-4: hits.append(dict(roll_deg=roll,pitch_deg=pitch,a=a,b=b,overlap_mm3=round(v,3)))
    mins.append(dict(roll_deg=roll,pitch_deg=pitch,head_min_z_mm=min(s.bounding_box().min.Z for n,s in placed.items() if parts[n][1]=='R')))
dimensions={n:{'min':[round(v,4) for v in s.bounding_box().min],'max':[round(v,4) for v in s.bounding_box().max]} for n,(s,f) in parts.items()}
ear_caps={}
for sign in [-1,1]:
    ear=parts['rolling_ear_'+str(sign)][0]
    ear_caps[str(sign)]=sum(f.area for f in ear.faces() if abs(f.center().Y-sign*75)<1e-5 and f.bounding_box().size.Y<1e-5)
result={'method':'BREP intersection of documented envelopes at 56 roll/pitch poses, including positions independent of the relief construction samples; no yaw/body mesh/cable swept-solid validation.',
 'pairs_per_pose':len(pairs),'poses':len(roll_samples)*len(pitch_samples),'hits':hits,'head_z_samples':mins,'component_bounds':dimensions,
 'outer_ear_face_area_mm2':ear_caps,
 'neutral_gaps_mm':{'display_to_camera_PCB_vertical':4,'display_reserve_to_C2':2,'roll_servo_to_rear_cover':7.3,'bearing_center_spacing':22},
 'cautions':['Some supports and covers remain unconnected or overlapping reservations, not detailed load paths.','Zero sampled overlap is not continuous swept clearance.','C2 and connector reservations are assumptions, not selected parts.']}
(HERE/'fit-checks.json').write_text(json.dumps(result,indent=2)+'\n')
worst={}
for h in hits:
    k=h['a']+' / '+h['b']
    if k not in worst or h['overlap_mm3']>worst[k]['overlap_mm3']:worst[k]=h
print(json.dumps({'colliding_pairs':worst,'minimum_sampled_head_z_mm':min(x['head_min_z_mm'] for x in mins),'hits':len(hits)},indent=2))
