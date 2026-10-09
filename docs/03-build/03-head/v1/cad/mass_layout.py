"""CAD-volume PLA and explicit D/E allocations; never measured W evidence.

--solve iterates A0 to the current estimated mass distribution, then writes
axes.json. R/P/Y membership matches the assembly. No row is added twice.
"""
import json,sys,importlib,math
from pathlib import Path
from build123d import CenterOf
import layout_model as m
import feetech as fe
import layout_axes
HERE=Path(__file__).parent
# C2 is selected (Waveshare ESP32-S3-Zero on the rolling face), but M008 is
# still an unweighed installed assembly. Use 20 g as the nominal E case while
# retaining the pre-existing sensitivity range until board + mount +
# connectors + assigned local harness are weighed together.
C2_NOMINAL_G=20.0
C2_SENSITIVITY_G=(10.0,20.0,35.0)
# D-049: STS3045M (HD-001), 34.8 g (D, Feetech). Its CoM and tensor are not
# published: rows take the drawing envelope's uniform-density centroid and
# inertia (E). Purchased metal from its CAD volume: goBILDA coupler and the
# horn at 2.70 g/cm3 aluminium, spindle and modelled D-049 screws/washers at
# 7.85 g/cm3 steel (E densities, D geometry except the E horn).
STS3045M_MASS_G=34.8
ALUMINIUM,STEEL=2.70e-3,7.85e-3
D049_HARDWARE=('roll_servo_ear_','pitch_servo_ear_','pitch_horn_to_leg_','pitch_horn_centre_','roll_coupler_centre_','roll_coupler_clamp_')

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
        if d['owner'] in ['M019a','M010','M010-P','M011-P','M011-Y','M012']:
            s=d['shape'];add(d['owner'],name,d['frame'],s.volume*.00124,None,shape=s,basis='E: authored solid volume × PLA 1.24 g/cm3; no infill or printer measurement')
        elif d['owner']=='M021a':
            s=d['shape'];add('M021a',name,d['frame'],.35,None,shape=s,basis='E: existing 0.35 g/visible screw planning allowance, NOT CAD steel density')
    shell=[r for r in rows if r['owner']=='M019a'];sm=sum(r['mass_g'] for r in shell)
    sc=[sum(r['mass_g']*r['center_mm'][i] for r in shell)/sm for i in range(3)]
    # Finish/misc remain separate from CAD shell mass, no obsolete crown add-on.
    add('M019b-M019a','finish allowance','R',29,sc,(100,130,86))
    add('M019c-M019b','retained inserts/adhesive allowance','R',10,sc,(100,100,70))
    add('M002','display + retention allowance','R',133,(-10,0,40),(10.6,106.1,68))
    add('M003','window + full-width mask','R',15,(-2.25,0,40),(1.5,106,64))
    add('M005','camera + bracket allowance','R',10,(-10,0,m.CAMERA_BOTTOM+14),(12.4,25,24))
    add('M006','CSI cable + strain relief','R',8,(-30,10,65),(20,20,20))
    add('M007','addressable LED installed allowance','R',5,(-6,m.LED_Y,m.LED_Z),(5,5,5))
    add('M008','C2 installed allowance','R',c2,(-29.5,-29,39.75),(9,18,23.5))
    # Servos: both pitch-carried (D-049; the pitch case turns round its horn).
    for name,label in [('roll_STS3045M_reference','STS3045M roll (HD-001)'),('pitch_STS3045M_reference','STS3045M pitch (HD-001)')]:
        d=parts[name]
        add(d['owner'],label,d['frame'],STS3045M_MASS_G,None,shape=d['shape'],basis='D: 34.8 g Feetech; E: uniform-density drawing envelope for CoM/inertia')
    d=parts['roll_coupler_goBILDA_4001_0025_0006']
    add(d['owner'],'goBILDA 4001-0025-0006 roll coupler','R',d['shape'].volume*ALUMINIUM,None,shape=d['shape'],basis='D: official STEP volume; E: 2.70 g/cm3 (listing 6 g with screw)')
    d=parts['pitch_horn_25T_disc']
    add(d['owner'],'25T aluminium pitch horn (HD-002)','Y',d['shape'].volume*ALUMINIUM,None,shape=d['shape'],basis='E: listing-dimension horn at 2.70 g/cm3; HD-002 hold')
    d=parts['rolling_spindle_6mm']
    add('M016-18-R','Ø6 roll spindle','R',d['shape'].volume*STEEL,None,shape=d['shape'],basis='E: Ø6 x 34.6 steel at 7.85 g/cm3')
    for name,d in parts.items():
        if name.startswith(D049_HARDWARE):
            add(d['owner'],name,d['frame'],d['shape'].volume*STEEL,None,shape=d['shape'],basis='E: D-049 modelled screw/washer volume at 7.85 g/cm3')
    # Balance trim at half capacity, so it can be added or removed (details.py).
    from details import trim_capacity,TRIM_NOMINAL_FRACTION,EAR_SLUG,EAR_TRIM_INNER_FACE,REAR_STACK
    cap=trim_capacity();f=TRIM_NOMINAL_FRACTION
    for sign in (-1,1):
        add('M022-R',f'ear {sign} tungsten trim slugs (nominal half)','R',cap['ear_slug_max_g']*f,(m.EAR_X,sign*(EAR_TRIM_INNER_FACE-EAR_SLUG['max_len']*f/2),m.EAR_Z),(12,EAR_SLUG['max_len']*f,12),basis='E: half the Ø12 x 2.5 mm tungsten seat capacity at 19.3 g/cm3')
    n=len(REAR_STACK['dy'])
    for dy in REAR_STACK['dy']:
        add('M022-R',f'rear-cover brass trim washers {dy:+g} (nominal half)','R',cap['rear_stack_max_g']*f/n,(-110.9+REAR_STACK['max_len']*f/2,m.ROLL_Y+dy,m.ROLL_Z+REAR_STACK['dz']),(REAR_STACK['max_len']*f,14,14),basis='E: half the Ø14 x 3 mm brass seat capacity at 8.5 g/cm3')
    bx=sum(fe.ROLL_BEARING_X)/2
    add('M016-18-P','pitch-carried bearing portions','P',8,(bx,m.ROLL_Y,m.ROLL_Z),(28,16,16))
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
            # feetech.py copies the axes at import: reload it before the layout.
            importlib.reload(fe)
            m=importlib.reload(m)
            if error<.02:break

    from cad_cache import load_parts
    parts=load_parts(catalog=False,bypass='--solve' in sys.argv);rows=rows_for(parts,C2_NOMINAL_G)
    scenarios=[]
    for c2 in C2_SENSITIVITY_G:
        scenario_rows=rows_for(parts,c2)
        case=dict(c2_g=c2)
        for label,frames,index,origin in [('roll','R',0,(0,m.ROLL_Y,m.ROLL_Z)),('pitch','RP',1,(m.PITCH_X,0,m.PITCH_Z)),('yaw','RPY',2,(m.PITCH_X,0,m.YAW_INTERFACE_Z))]:
            group=[r for r in scenario_rows if r['frame'] in frames]
            inertia=sum(r['intrinsic_diagonal_g_mm2'][index]+r['mass_g']*sum((r['center_mm'][i]-origin[i])**2 for i in range(3) if i!=index) for r in group)
            case[label]=com(scenario_rows,frames)|dict(estimated_inertia_kg_m2=inertia*1e-9)
        scenarios.append(case)
    working=next(case for case in scenarios if case['c2_g']==C2_NOMINAL_G)
    result=dict(method='CAD-volume PLA at 1.24 g/cm3 + listed D/E allowances. C2 hardware is selected but M008 installed mass remains U. A0 is solved around the nominal 20 g E case; 10/20/35 g sensitivity cases remain until the complete M008 assembly is weighed. Uniform geometry/box intrinsic inertia and parallel-axis terms; NOT measured mass, torque or servo approval.',axes=m.AXES,rows=rows,working=working,scenarios=scenarios,visible_M2_count=sum(r['owner']=='M021a' for r in rows),notes=['Display 133 g already includes 15 g retention; camera 10 g includes bracket; nominal C2 20 g E and LED installed allowances include their mounts. Do not add modeled visual envelopes again.','M008 remains U in the physical mass register. The sensitivity cases are analytical inputs only and do not constitute W evidence.','M012 is the modeled flush yaw turntable disc (authored PLA volume); the body-side slew bearing, ring gear and yaw servo belong to RP-06. Bearing rows own shaft/trunnion metal.','Old M019c=148 g and CROWN=6 g replaced by current skin/ear geometry +29 g finish +10 g misc; no double counting.','Density uses solid CAD walls/ribs. Print process, insert choice, finish, candidate-specific servo mass and actual modules must be weighed/recalculated before actuator freeze.'])
    (HERE/'mass-placement.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(axes=m.AXES,working=working,scenarios=scenarios),indent=2))
