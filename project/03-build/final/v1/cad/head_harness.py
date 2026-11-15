"""D-107 W47: twelve loose wires and stripped HDMI pairs, no hose.

Nominal neutral route. Dynamic candidates and all clearances are checked by
check_d107_neck.py; connector dress and cable life require physical acceptance.
"""
import math
from build123d import Compound, Location
import d107_umbilical as U

WIRES = [
    ("+6V3_HEAD_PR",22,.75,"#c93a35"),("+5V_C2",26,.5,"#da8642"),
    ("+5V_DISPLAY",26,.5,"#d0ba42"),("GND_HEAD",22,.75,"#272b31"),
    ("GND_C2",26,.5,"#42474a"),("GND_DISPLAY",26,.5,"#63686b"),
    ("GND_SIG",28,.4,"#777e85"),("C0TX_P",28,.4,"#69a989"),
    ("C0TX_N",28,.4,"#b8cfbd"),("C2TX_N",28,.4,"#8aacc7"),
    ("C2TX_P",28,.4,"#4376a4"),("SERVO_DATA",28,.4,"#c59bd7")]

# The candidate router produces these static roll-frame paths. Exact solids,
# including the new mounts and adapter, are the acceptance check.
import json
import numpy as np
from pathlib import Path
from study_umbilical_span import bezier_guess, rot
SERVO_R_ANCHOR=(-28.,-12.,46.)
SERVO_P_ANCHOR=(-33.,-18.,64.)
SERVO_P_PATH=[SERVO_P_ANCHOR,(-45.8,-8.2,67.8),
              (-39.5,14.2,65.2),(-35.8,18.,61.5)]
SERVO_LOOP_LENGTH=30.
HEAD_FFC_LENGTH=150.       # separate15-way1mm-pitch camera ribbon
BODY_FFC_LENGTH=150.       # Arducam B0210-class15-way to22-way camera FPC
FFC_INSERTION_ALLOWANCE=10.  # two5mm ends, E until received
FFC_SERVICE_ALLOWANCE=15.

BODY_POWER=[(22.42,-36.,117.5),(26.,-32.,118.),(26.,-27.,118.),(28.,-24.,118.)]
BODY_SIGNALS=[(-6.,-35.,125.),(-6.,-35.,125.5),(22.,-35.,125.5),
              (26.,-31.,118.),(26.,-27.,118.),(28.,-24.,118.)]
BODY_HDMI=[(53.,5.915,120.),(53.,14.,120.),(42.,14.,118.),(28.,8.,118.),(28.,-16.,118.)]


def ribbon_segment(a,b,width_axis,width,thickness=.3):
    from build123d import Box,Plane,Vector
    a,b=Vector(*a),Vector(*b);along=(b-a).normalized();across=Vector(*width_axis)
    normal=along.cross(across).normalized()
    return Box((b-a).length,width,thickness).moved(Plane(origin=(a+b)*.5,x_dir=along,z_dir=normal).location)


HEAD_FFC_POINTS=[(-67.,-33.915,72.6),(-67.,-25.,83.),(-67.,10.,83.),(-35.,10.,83.),(-35.,0.,83.),(-14.5,0.,83.)]
BODY_FFC_POINTS=[(53.,-43.915,117.),(53.,-48.,117.),(53.,-48.,109.5),(53.,-39.,109.5),
                 (37.4,-39.,109.5),(37.4,-24.72,109.5),(37.4,-24.72,100.)]


def head_ffc():
    p=HEAD_FFC_POINTS
    axes=[(1,0,0),(1,0,0),(0,1,0),(1,0,0),(0,1,0)]
    return [ribbon_segment(a,b,w,16.) for a,b,w in zip(p,p[1:],axes)]


def body_ffc():
    """One continuous, mitered FPC envelope with a tapered adapter tail.

    Each section follows the mean incoming/outgoing tangent. This removes the
    disconnected rectangular plates at bends and shows the change from the
    15-way end to the 22-way end. The exact received fold geometry is still U.
    """
    from build123d import Vector, Wire, Solid
    p=[Vector(*x) for x in BODY_FFC_POINTS]
    axes=[Vector(*x) for x in ((1,0,0),(1,0,0),(1,0,0),
                               (1,1,0),(1,1,0),(1,1,0),(0,1,0))]
    widths=(16.,16.,16.,14.,12.,12.,12.)
    sections=[]
    for i,c in enumerate(p):
        incoming=(p[i]-p[i-1]).normalized() if i else (p[1]-p[0]).normalized()
        outgoing=(p[i+1]-p[i]).normalized() if i<len(p)-1 else incoming
        tangent=(incoming+outgoing).normalized()
        across=(axes[i]-tangent*axes[i].dot(tangent)).normalized()
        normal=tangent.cross(across).normalized()
        a=across*widths[i]/2.;b=normal*.15
        sections.append(Wire.make_polygon([c-a-b,c+a-b,c+a+b,c-a+b],close=True))
    return [Solid.make_loft(sections,ruled=True)]

def lead_paths():
    doc=json.loads((Path(__file__).parent/'d107-internal-routes.json').read_text())
    paths={}
    for name,points in doc['paths'].items():
        if points is None: raise ValueError(f'unrouted D-107 internal lead: {name}')
        pts=[list(U.CLAMP),[U.CLAMP[0],0.,9.]]+points[1:]
        # Clear the top of the jaw before the fan-out turns down to the floor.
        if pts[2][2]<9.:pts[2][2]=9.
        paths[name]=pts
    paths['SERVO_ROLL']=paths['SERVO_ROLL'][:-2]+[[-28.,-12.,44.],list(SERVO_R_ANCHOR)]
    # The routed lead used to stop 3.1 mm beyond the modeled plug face.
    # Seat its last segment into the B0091 head HDMI plug envelope.
    paths['HEAD_CAMERA_HDMI']=paths['HEAD_CAMERA_HDMI'][:-2]+[[-67.,14.5,71.],[-67.,15.5,75.]]
    paths['PCB12_J1']=[list(U.CLAMP),[-50.4,0.,10.],[-44.5,-6.5,10.],[-44.5,-16.,10.],
                       [-44.5,-23.,6.5],[-39.,-29.4,11.75]]
    paths['PCB12_J1'].append([-32.485,-29.4,11.75])
    paths['PCB12_J2_BRANCH']=[list(U.CLAMP),[U.CLAMP[0],0,9],[-44.5,-6.5,9],[-44.5,-23,6.5],
                              [-33.6,-29.4,8.],[-33.6,-38.8,8.],[-33.6,-38.8,19.55],[-32.485,-38.8,19.55]]
    return paths

def servo_loop(roll,roll_axis):
    o=np.asarray(roll_axis);p0=o+(np.asarray(SERVO_R_ANCHOR)-o)@rot('x',roll).T
    p1=np.asarray(SERVO_P_ANCHOR)
    # A fixed-length circular arc with free end tangents. Loose internal
    # wires have strain-relief points, not the neck solver's fixed headings.
    # This avoids a cubic hairpin whose apparent clearance hides a sub-mm kink.
    length=SERVO_LOOP_LENGTH;d=np.linalg.norm(p1-p0);u=(p1-p0)/d
    v=np.array([-.3,-1.,0.]);v-=u*np.dot(v,u);v/=np.linalg.norm(v)
    lo,hi=1e-6,2*math.pi-1e-6
    for _ in range(60):
        theta=(lo+hi)/2
        if 2*math.sin(theta/2)/theta>d/length:lo=theta
        else:hi=theta
    theta=(lo+hi)/2;radius=length/theta;t=np.linspace(-theta/2,theta/2,40)
    centre=(p0+p1)/2-v*radius*math.cos(theta/2)
    return centre+radius*(np.sin(t)[:,None]*u+np.cos(t)[:,None]*v)


def body_wire_paths(origin=None,include_neck=False):
    body=list(reversed(U.body_path()))
    neck=U.neutral_points((0,0,0)) if include_neck else []
    path=body+neck[1:] if include_neck else body
    out=[]
    for i,(name,awg,radius,colour) in enumerate(WIRES):
        a=2*math.pi*i/len(WIRES);dx,dy=2.35*math.cos(a),2.35*math.sin(a)
        fan=BODY_POWER if i<6 else BODY_SIGNALS
        port=(22.42,(-33.,-36.,-39.)[i%3],115.85 if i<3 else 118.85) if i<6 else (-6.,-38.125+1.25*(i-6),125.)
        pts=[port,*fan[1:-1]]+[(x+dx,y+dy,z) for x,y,z in path]
        out.append((f"W47_{name}_AWG{awg}",pts,radius,colour))
    cam=BODY_HDMI+body[2:]+neck[1:] if include_neck else BODY_HDMI+body[2:]
    out.append(("W47_STRIPPED_HDMI_INNER_PAIRS_E",cam,1.45,"#b7b1a4"))
    return out


def build_head_harness(entry):
    origin=entry.HEAD_ORIGIN_IN_CHASSIS
    wires=[entry._tag(U.tube([(x-origin[0],y-origin[1],z-origin[2]) for x,y,z in pts],radius),name,colour)
           for name,pts,radius,colour in body_wire_paths(origin,include_neck=True)]
    leads=[entry._tag(U.tube(p,.8 if name=='PCB12_J2_BRANCH' else (1.8 if name=='HEAD_CAMERA_HDMI' else (1. if name=='DISPLAY_POWER' else 1.5))),
                      f"W47_LEAD_{name}","#bb925f") for name,p in lead_paths().items()]
    axis=(0.,entry.layout_model.ROLL_AXIS.position.Y,entry.layout_model.ROLL_AXIS.position.Z)
    leads.extend([entry._tag(U.tube(servo_loop(0.,axis),1.5),"W47_THREE_SERVO_WIRES_ROLL_LOOP","#b48d6a"),
                  entry._tag(U.tube(SERVO_P_PATH,1.5),"W47_THREE_SERVO_WIRES_PITCH_FRAME","#b48d6a")])
    leads.extend(entry._tag(sh,f'W47_CAMERA_HEAD_STATIC_FFC_{i}','#d6b480') for i,sh in enumerate(head_ffc(),1))
    leads.extend(entry._tag(sh.moved(Location(tuple(-v for v in origin))),f'W47_CAMERA_BODY_STATIC_FFC_{i}','#d6b480') for i,sh in enumerate(body_ffc(),1))
    return Compound(label="Harness",children=[Compound(label="Head wires",children=[
        Compound(label="W47 twelve loose wires and camera pairs",children=wires),
        Compound(label="W47 head fan-out",children=leads)])])
