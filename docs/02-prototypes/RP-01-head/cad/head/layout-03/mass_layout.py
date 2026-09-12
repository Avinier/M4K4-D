"""CAD-volume PLA and explicit D/E allocations; never measured W evidence.

--solve iterates A0 to the current estimated mass distribution, then writes
axes.json. R/P/Y membership matches the assembly. No row is added twice.
"""
import json,sys,importlib,math
from pathlib import Path
from build123d import CenterOf
import layout_model as m
import layout_axes
HERE=Path(__file__).parent
# C2 is selected (Waveshare ESP32-S3-Zero on the rolling face), but M008 is
# still an unweighed installed assembly. Use 20 g as the nominal E case while
# retaining the pre-existing sensitivity range until board + mount +
# connectors + assigned local harness are weighed together.
C2_NOMINAL_G=20.0
C2_SENSITIVITY_G=(10.0,20.0,35.0)
def rows_for(parts,c2=C2_NOMINAL_G):
    rows=[]
    def add(owner,name,frame,mass,centre,size=(0,0,0),shape=None,basis='D/E allocation; uniform bounding-box inertia approximation'):
        if shape is not None:
            centre=list(shape.center(CenterOf.MASS))
            intrinsic=[shape.matrix_of_inertia[i][i]*mass/shape.volume for i in range(3)]
        else:
            a,b,c=size;intrinsic=[mass*(b*b+c*c)/12,mass*(a*a+c*c)/12,mass*(a*a+b*b)/12]
        rows.append(dict(owner=owner,name=name,frame=frame,mass_g=mass,center_mm=list(centre),intrinsic_diagonal_g_mm2=intrinsic,basis=basis))
    # These are authored PLA solids; imported/electronic volumes are NOT PLA.
    for name,d in parts.items():
        if d['owner'] in ['M019a','M010','M010-P','M011-P','M011-Y']:
            s=d['shape'];add(d['owner'],name,d['frame'],s.volume*.00124,None,shape=s,basis='E: authored solid volume × PLA 1.24 g/cm3; no infill or printer measurement')
        elif d['owner']=='M021a':
            s=d['shape'];add('M021a',name,d['frame'],.35,None,shape=s,basis='E: existing 0.35 g/visible screw planning allowance, NOT CAD steel density')
    shell=[r for r in rows if r['owner']=='M019a'];sm=sum(r['mass_g'] for r in shell)
    sc=[sum(r['mass_g']*r['center_mm'][i] for r in shell)/sm for i in range(3)]
    # Finish/misc remain separate from CAD shell mass, no obsolete crown add-on.
    add('M019b-M019a','finish allowance','R',29,sc,(100,130,86))
    add('M019c-M019b','retained inserts/adhesive allowance','R',10,sc,(100,100,70))
    add('M002','display + retention allowance','R',133,(-10,0,40),(10.6,106.1,68))
    add('M003','window + full-width mask','R',15,(-2,0,40),(1.5,110,64))
    add('M005','camera + bracket allowance','R',10,(-10,0,m.CAMERA_BOTTOM+14),(12.4,25,24))
    add('M006','CSI cable + strain relief','R',8,(-30,10,65),(20,20,20))
    add('M007','addressable LED installed allowance','R',5,(-6,m.LED_Y,m.LED_Z),(5,5,5))
    add('M008','C2 installed allowance','R',c2,(-29.5,-29,39.75),(9,18,23.5))
    add('M012','yaw moving interface incl. modeled bridge','Y',20,(-56,0,-34),(40,116,5))
    add('M013-15-roll','XC330 roll reference','P',23,(-92,m.ROLL_Y,m.ROLL_Z-7.5),(29,20,34))
    add('M013-15-pitch','XC330 pitch reference','Y',23,(m.PITCH_X-7.5,32,m.PITCH_Z),(34,29,20))
    add('M013-15-R','rolling hub/coupling allowance','R',4,(-73.25,m.ROLL_Y,m.ROLL_Z),(8.5,12,12))
    add('M013-15-P','pitch horn allowance','P',2,(m.PITCH_X,49,m.PITCH_Z),(8,5,8))
    add('M016-18-R','rotating shaft portions','R',6,(-55,m.ROLL_Y,m.ROLL_Z),(32,6,6))
    add('M016-18-P','pitch-carried bearing portions','P',8,(-54,m.ROLL_Y,m.ROLL_Z),(28,16,16))
    add('M016-18-Y','yaw-carried bearing portions','Y',8,(m.PITCH_X,0,-5),(8,100,45))
    for frame,mass,centre,size in [('R',8,(-32,8,38),(30,35,30)),('P',4,(-65,0,32),(30,20,20)),('Y',3,(-52,0,-10),(20,15,40))]:
        add('M020-'+frame,'non-camera harness',frame,mass,centre,size)
    for frame,mass,centre in [('R',3,(-30,0,40)),('P',3,(-55,0,35)),('Y',2,(-45,0,0))]:
        add('M021-'+frame,'hidden hardware allowance',frame,mass,centre,(20,30,30))
    return rows

def com(rows,frames):
    a=[r for r in rows if r['frame'] in frames];mass=sum(r['mass_g'] for r in a)
    return dict(mass_g=mass,center_mm=[sum(r['mass_g']*r['center_mm'][i] for r in a)/mass for i in range(3)])

if __name__=='__main__':
    if '--solve' in sys.argv:
        for iteration in range(6):
            p=m.build_parts(catalog=False);rows=rows_for(p)
            r=com(rows,'R');q=com(rows,'RP')
            target=dict(roll_y=r['center_mm'][1],roll_z=r['center_mm'][2],pitch_x=q['center_mm'][0],pitch_z=q['center_mm'][2])
            error=max(abs(target[k]-m.AXES[k]) for k in target)
            print('A0 iteration',iteration,'maximum change mm',round(error,5),target,flush=True)
            (HERE/'axes.json').write_text(json.dumps(target,indent=2)+'\n')
            (HERE/'layout_axes.py').write_text('"""Generated A0 datums, mm. Refresh through mass_layout.py --solve."""\nAXES = '+repr(target)+'\n')
            importlib.reload(layout_axes)
            m=importlib.reload(m)
            if error<.02:break

    parts=m.build_parts(catalog=False);rows=rows_for(parts,C2_NOMINAL_G)
    scenarios=[]
    for c2 in C2_SENSITIVITY_G:
        scenario_rows=rows_for(parts,c2)
        case=dict(c2_g=c2)
        for label,frames,index,origin in [('roll','R',0,(0,m.ROLL_Y,m.ROLL_Z)),('pitch','RP',1,(m.PITCH_X,0,m.PITCH_Z)),('yaw','RPY',2,(m.PITCH_X,0,-60))]:
            group=[r for r in scenario_rows if r['frame'] in frames]
            inertia=sum(r['intrinsic_diagonal_g_mm2'][index]+r['mass_g']*sum((r['center_mm'][i]-origin[i])**2 for i in range(3) if i!=index) for r in group)
            case[label]=com(scenario_rows,frames)|dict(estimated_inertia_kg_m2=inertia*1e-9)
        scenarios.append(case)
    working=next(case for case in scenarios if case['c2_g']==C2_NOMINAL_G)
    result=dict(method='CAD-volume PLA at 1.24 g/cm3 + listed D/E allowances. C2 hardware is selected but M008 installed mass remains U. A0 is solved around the nominal 20 g E case; 10/20/35 g sensitivity cases remain until the complete M008 assembly is weighed. Uniform geometry/box intrinsic inertia and parallel-axis terms; NOT measured mass, torque or servo approval.',axes=m.AXES,rows=rows,working=working,scenarios=scenarios,visible_M2_count=sum(r['owner']=='M021a' for r in rows),notes=['Display 133 g already includes 15 g retention; camera 10 g includes bracket; nominal C2 20 g E and LED installed allowances include their mounts. Do not add modeled visual envelopes again.','M008 remains U in the physical mass register. The sensitivity cases are analytical inputs only and do not constitute W evidence.','M012 includes the modeled yaw bridge; bearing rows own shaft/trunnion metal.','Old M019c=148 g and CROWN=6 g replaced by current skin/ear geometry +29 g finish +10 g misc; no double counting.','Density uses solid CAD walls/ribs. Print process, insert choice, finish, candidate-specific servo mass and actual modules must be weighed/recalculated before actuator freeze.'])
    (HERE/'mass-placement.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(axes=m.AXES,working=working,scenarios=scenarios),indent=2))
