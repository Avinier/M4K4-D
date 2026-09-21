"""Independent masters and rigid-frame poses; STEP itself stays neutral."""
import json
from pathlib import Path
import layout_model as m
from inspection_scene import group_for
from harness import routes
parts=m.build_parts(catalog=False);h,_=routes()
frames={'R':set(),'P':set(),'Y':set()}
for n,d in parts.items():
    f=d['frame'];flabel={'R':'rolling','P':'pitch_carried','Y':'yaw_carried'}[f]
    frames[f].add(f'physical_{flabel}_{group_for(n,d)}')
    if d['kind']=='physical' and group_for(n,d)!='fasteners':frames[f].add('annotation_'+n)
for n,d in h.items():frames[d['frame']].add(n)
for f,names in [('R',['estimated_CoM_R','roll_A0_residual','camera_102deg_FOV_corner_envelope']),('P',['roll_axis_through_A0','estimated_CoM_RP','pitch_A0_residual']),('Y',['pitch_axis_through_A0','estimated_CoM_RPY'])]:frames[f].update(names)
descriptor=json.loads((Path(__file__).parent/'__cadgen__/models/head-layout.step.py/assembly.json').read_text())
nodes={}
def index(node):
    nodes[node['name']]=node['id']
    for child in node.get('children',[]):index(child)
index(descriptor['assembly']['root'])
def refs(names):
    return {'ref':'#'+','.join(nodes[n] for n in sorted(names) if n in nodes)}
features={f'frame_{f}':refs(v) for f,v in frames.items()}
for n in ['physical','physics','harness','annotations']:features[n]=refs([n])
features['fov']=refs(['camera_102deg_FOV_corner_envelope'])
features['shell']={'names':[n for n,d in parts.items() if d['owner']=='M019a']}
parameters={}
for n,lo,hi in [('roll',-18,18),('pitch',-22,40),('yaw',-55,55)]:parameters[n+'_deg']=dict(type='number',label=n.title(),unit='°',min=lo,max=hi,step=1,default=0)
for n,default in [('physical',True),('physics',True),('harness',True),('annotations',False),('fov',True),('shell',True)]:parameters['show_'+n]=dict(type='boolean',label='Show '+n,default=default)
manifest=dict(schemaVersion=1,step={'path':'head/layout-03/head-layout.step'},parameters=parameters,features=features)
code='// Generated; presentation only. Per-part scene-tree controls remain available.\nconst axes='+json.dumps(m.AXES)+';\nconst clamp=(v,a,b)=>Math.max(a,Math.min(b,Number(v)||0));\nexport default {manifest:'+json.dumps(manifest,indent=2)+''',
update({params,effects}) {
 const r={rotate:{axis:[1,0,0],origin:[0,axes.roll_y,axes.roll_z],angleDeg:clamp(params.roll_deg,-18,18)}};
 const p={rotate:{axis:[0,1,0],origin:[axes.pitch_x,0,axes.pitch_z],angleDeg:clamp(params.pitch_deg,-22,40)}};
 const y={rotate:{axis:[0,0,1],origin:[axes.pitch_x,0,-60],angleDeg:clamp(params.yaw_deg,-55,55)}};
 effects.transform('frame_R',{transforms:[r,p,y]});
 effects.transform('frame_P',{transforms:[p,y]});
 effects.transform('frame_Y',y);
 for (const key of ['physical','physics','harness','annotations']) effects.visible(key,params['show_'+key]!==false);
 effects.visible('fov',params.show_physics!==false && params.show_fov!==false);
 effects.visible('shell',params.show_physical!==false && params.show_shell!==false);
}};
'''
(Path(__file__).parent/'head-layout.params.js').write_text(code)
print('Wrote independent group controls')
