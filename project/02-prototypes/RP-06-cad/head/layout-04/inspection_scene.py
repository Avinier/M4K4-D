"""Occurrence tree and rigid R/P/Y inspection overlays, source-derived datums."""
import json
from pathlib import Path
from build123d import *
import layout_model as m
from write_dimensions import measure
from harness import routes,rod
from optics import cone

def group_for(n,d):
    owner=d.get('owner') or ''
    if owner.startswith('M021') or '_M2' in n:return 'fasteners'
    if d['frame']=='Y':return 'pitch_actuator' if 'pitch' in n else 'yoke'
    if d['frame']=='P':return 'roll_drive' if any(s in n for s in ['bearing','roll_XC','retainer']) else 'pitch_frame'
    if n.startswith('C2'):return 'c2'
    if owner=='M019a':return 'skin_ears'
    if any(s in n for s in ['display','camera','window','LED','diffuser']):return 'display_camera'
    return 'cradle'

def posed(s,frame,roll,pitch,yaw):
    if frame=='R':s=s.rotate(m.ROLL_AXIS,roll)
    if frame in ('R','P'):s=s.rotate(m.PITCH_AXIS,pitch)
    if frame in ('R','P','Y'):s=s.rotate(m.YAW_AXIS,yaw)
    return s

def triad(point,length,label):
    result=[]
    for i,(axis,color) in enumerate(zip('XYZ',['#df5353','#61a663','#5683cb'])):
        q=list(point);q[i]+=length
        result.append(m.tint(rod(point,q,.22),f'{axis}_global_{point[i]:.3f}_mm',color))
    return Compound(label=label,children=result)

def scene(parts,internals=False,roll=0,pitch=0,yaw=0):
    manifests={};frames={'R':[],'P':[],'Y':[],'G':[]}
    def remember(label,frame):frames[frame].append(label)
    roots=[]
    phys=[]
    for f,flabel in [('R','rolling'),('P','pitch_carried'),('Y','yaw_carried')]:
        groups={}
        for n,d in parts.items():
            if d['frame']!=f:continue
            if internals and d['owner'] in ['M019a','M021a']:continue
            key=group_for(n,d);groups.setdefault(key,[]).append(d['shape'])
        children=[]
        for key,shapes in groups.items():
            label=f'physical_{flabel}_{key}';remember(label,f)
            children.append(posed(Compound(label=label,children=shapes),f,roll,pitch,yaw))
        phys.append(Compound(label=flabel,children=children))
    roots.append(Compound(label='physical',children=phys))
    # CoMs from exactly the same mass rows used by the A0 solver, no eye placement.
    from mass_layout import rows_for,com
    rows=rows_for(parts);physics={k:[] for k in ['axes','com','other']}
    def overlay(n,s,frame,group,color,alpha=1):
        remember(n,frame);s=m.tint(s,n,color,alpha);physics[group].append(posed(s,frame,roll,pitch,yaw))
    physics['axes'].append(triad((0,0,0),20,'layout_origin_XYZ'))
    overlay('roll_axis_through_A0',m.axial(.45,150,(-55,m.ROLL_Y,m.ROLL_Z)),'P','axes','#e15656')
    overlay('pitch_axis_through_A0',m.axial(.45,160,(m.PITCH_X,0,m.PITCH_Z),'y'),'Y','axes','#63b868')
    overlay('yaw_axis',m.axial(.45,170,(m.PITCH_X,0,20),'z'),'G','axes','#6784d2')
    for f,fs,c in [('R','R','#e2bd49'),('P','RP','#dc79b6'),('Y','RPY','#62b6c8')]:
        pos=com(rows,fs)['center_mm']
        overlay(f'estimated_CoM_{fs}',Sphere(1.7).moved(Location(pos)),f,'com',c)
    centre=com(rows,'RPY')['center_mm'];end=[centre[0],centre[1],centre[2]-15]
    overlay('gravity_minus_Z_neutral',rod(centre,end,.55)+Cone(0,2.1,4).moved(Location((end[0],end[1],end[2]+2))),'G','other','#353c46')
    for name,fs,target,f in [('roll','R',(None,m.ROLL_Y,m.ROLL_Z),'R'),('pitch','RP',(m.PITCH_X,None,m.PITCH_Z),'P')]:
        c=com(rows,fs)['center_mm'];q=[c[i] if target[i] is None else target[i] for i in range(3)]
        if (Vector(c)-Vector(q)).length>1e-5:overlay(name+'_A0_residual',rod(c,q,.15),f,'other','#f04b48')
    overlay('camera_102deg_FOV_corner_envelope',cone(m.CAMERA_BOTTOM+14.4),'R','other','#75bb9d',.10)
    roots.append(Compound(label='physics',children=[Compound(label=k,children=v) for k,v in physics.items()]))
    h,gaps=routes();branches={}
    for n,d in h.items():
        remember(n,d['frame']);branches.setdefault(d['branch'],[]).append(posed(d['shape'],d['frame'],roll,pitch,yaw))
    roots.append(Compound(label='harness',children=[Compound(label=k,children=v) for k,v in branches.items()]))
    annotations={}
    for n,d in parts.items():
        if d['kind']!='physical' or group_for(n,d)=='fasteners':continue
        r=measure(d['shape']);p=r['geometric_centre_mm'];sz=r['size_dxdydz_mm']
        bars=[]
        for i in range(3):
            q=list(p);q[i]+=sz[i]/2;start=list(p);start[i]-=sz[i]/2
            bars.append(m.tint(rod(start,q,.15),f'delta_{"XYZ"[i]}_{sz[i]:.3f}_mm','#a6a6a6'))
        label='annotation_'+n;remember(label,d['frame'])
        dims=Compound(label='dimensions_'+('_x_'.join(f'{v:.3f}' for v in sz)),children=bars)
        item=Compound(label=label,children=[triad(p,5,'frame_xyz_'+('_'.join(f'{v:.3f}' for v in p))),dims])
        annotations.setdefault(group_for(n,d),[]).append(posed(item,d['frame'],roll,pitch,yaw))
    roots.append(Compound(label='annotations',children=[Compound(label=k,children=v) for k,v in annotations.items()]))
    return Compound(label='RP01_Layout03',children=roots)
