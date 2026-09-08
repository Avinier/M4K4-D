"""Parametric appearance/packaging layout; NOT fabrication release.

R rolls, pitches, yaws; P pitches/yaws; Y yaws. All transforms are explicit
named component/joint datums, not visual placements. Catalog models are 1:1.
"""
from pathlib import Path
import json, math
from build123d import (Box, Cylinder, Cone, Sphere, Compound, Location, Plane,
                      Polygon, RegularPolygon, extrude, loft, Axis, CenterOf)
from cadgen import srgb
from cadgen.step_scene import import_step
from layout_axes import AXES

HERE=Path(__file__).parent
CATALOG=HERE.parent/'layout-01'/'parts'
MAIN_W, MAIN_D, MAIN_H, CROWN_H, SKIN=130.,115.,86.,102.,1.2
EAR_R, EAR_X, EAR_Z=30.,-43.,42.
DISPLAY_BOTTOM, CAMERA_BOTTOM=6.,75.
LED_Y, LED_Z=15.2,91.8
FRONT_SCREWS=[(-57.4,16),(57.4,16),(-57.4,64),(57.4,64),(-32,78),(32,78)]
REAR_SCREWS=[(-56,19),(56,19),(-56,67),(56,67)]
ROLL_Y,ROLL_Z,PITCH_X,PITCH_Z=[AXES[k] for k in ('roll_y','roll_z','pitch_x','pitch_z')]
ROLL_AXIS=Axis((0,ROLL_Y,ROLL_Z),(1,0,0))
PITCH_AXIS=Axis((PITCH_X,0,PITCH_Z),(0,1,0))
YAW_AXIS=Axis((PITCH_X,0,-60),(0,0,1))

def block(x0,x1,y0,y1,z0,z1):
    return Box(x1-x0,y1-y0,z1-z0).moved(Location(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)))

def axial(r,h,c,axis='x'):
    s=Cylinder(r,h)
    if axis=='x':s=s.rotate(Axis.Y,90)
    elif axis=='y':s=s.rotate(Axis.X,-90)
    return s.moved(Location(c))

def oct_points(w,z0,z1,c):
    a=w/2
    return [(-a+c,z0),(a-c,z0),(a,z0+c),(a,z1-c),(a-c,z1),(-a+c,z1),(-a,z1-c),(-a,z0+c)]

def profile(w,z0,z1,c,x=0):
    return (Plane.YZ*Polygon(*oct_points(w,z0,z1,c),align=None)).moved(Location((x,0,0)))

def prism(w,z0,z1,c,x0,x1):
    return extrude(profile(w,z0,z1,c,x0),amount=x1-x0)

def pieces(s):
    return ([s] if hasattr(s,'volume') else list(s)) if s else []

def tint(s,name,color,alpha=1):
    s.label=name
    if s.children:
        for c in s.children:tint(c,c.label or name,color,alpha)
    else:s.color=srgb(color,alpha)
    return s

def button_screw(x,y,z,axis='x',sign=1):
    # Local +Z points outwards; origin at under-head seat. Smooth major thread.
    h=1.3;r=1.75;R=(r*r+h*h)/(2*h)
    cap=Sphere(R).moved(Location((0,0,h-R))) & Box(6,6,h).moved(Location((0,0,h/2)))
    shank=Cylinder(1,6).moved(Location((0,0,-3)))
    socket=extrude(RegularPolygon(1.3/math.sqrt(3),6),amount=1).moved(Location((0,0,.6)))
    screw=(cap+shank)-socket
    if axis=='x':screw=screw.rotate(Axis.Y,90*sign)
    elif axis=='y':screw=screw.rotate(Axis.X,-90*sign)
    return screw.moved(Location((x,y,z)))

def clean_catalog(path):
    # Discard STEP annotation/open-shell children, preserve all closed solids.
    raw=import_step(str(path))
    solids=[]
    for i,s in enumerate(raw.solids()):
        if s.is_valid and s.volume>1e-8:
            s.label=f'{path.stem}_solid_{i+1:03}'
            solids.append(s)
    return Compound(label=path.stem,children=solids)

def build_parts(catalog=True,reliefs=True):
    out={}
    def add(n,s,f,color='#e3ddc9',kind='physical',alpha=1,owner=None):
        out[n]=dict(shape=tint(s,n,color,alpha),frame=f,kind=kind,owner=owner)
    # Planar front ring and sloping depth band; crown fuses into this one part.
    outer=prism(120,2,84,10,-2,0)+loft([profile(120,2,84,10,-2),profile(130,0,86,14,-8)],ruled=True)
    cp=[(-23,73),(23,73),(23,85),(17,102),(-17,102),(-23,85)]
    crown=extrude(Plane.YZ*Polygon(*cp,align=None),amount=24).moved(Location((-24,0,0)))
    outer=outer+crown
    # Inside of the depth band provides a truthful full-size display pocket.
    inner=prism(127.6,1.2,84.8,13.3,-25,-8.2)+loft([profile(127.6,1.2,84.8,13.3,-8.2),profile(117.6,3.2,82.8,8.3,-2.8)],ruled=True)
    ci=[(-21.8,72),(21.8,72),(21.8,84.8),(16.15,100.8),(-16.15,100.8),(-21.8,84.8)]
    inner=inner+extrude(Plane.YZ*Polygon(*ci,align=None),amount=20.8).moved(Location((-22.8,0,0)))
    face=outer-inner-prism(99,11,69,3,-5,1)
    # Full-size board corner clearance and a separate shallow window seat.
    face=face-block(-14.7,-3.5,-53.35,53.35,5.7,74.3)
    face=face-prism(110.6,7.7,72.3,4,-2.9,-.95)
    # Wide-angle optical path remains a clearance trial, not FOV certification.
    face=face-axial(8.6,6,(-1,0,CAMERA_BOTTOM+14.4))-axial(1.8,5,(-1,LED_Y,LED_Z))
    # Recessed perimeter lands and real screw seats. Upper screws avoid camera.
    for y,z in FRONT_SCREWS:
        pad=axial(2.3,5,(-2.5,y,z))
        face=face+pad
        face=face-axial(1.15,9,(-3,y,z))-axial(2.1,2,(-.7,y,z))
    # Integral visual panel lines: shallow, not through-cracks.
    for y in [-38,38]:face=face-block(-.5,.1,y-.35,y+.35,70,84)
    # Viewer material is translucent so the real 1:1 internal packaging remains
    # inspectable while the shell stays present in the assembly view.
    add('front_bezel_integral_camera_crown',face,'R',alpha=.28,owner='M019a')
    # Thin side shell and separate octagonal rear cover with real 0.8 seam.
    skin=prism(130,0,86,14,-112.6,-8.8)-prism(127.6,1.2,84.8,13.3,-114,-8)
    skin=skin-block(-24.8,-8,-23.8,23.8,84.2,90)
    # Underside access is necessary for the fixed yoke and external cable loop.
    # Integral panel steps add the required 0.4 mm relief without extra joints.
    for sign in [-1,1]:
        # Recessed rectangular side lands stay clear of the round ear mount.
        tool=block(-103,-82,63.8,65.1,24,62) if sign==1 else block(-103,-82,-65.1,-63.8,24,62)
        recess=tool.intersect(block(-104,-81,64.6,66,23,63) if sign==1 else block(-104,-81,-66,-64.6,23,63))
        if recess:skin=skin-recess
    # Front receivers rooted in shell wall, not in the display envelope.
    for y,z in FRONT_SCREWS:
        boss=axial(3.2,7,(-12.3,y,z))-axial(.8,8,(-12.3,y,z))
        # Upper bosses reach the roof; side bosses reach the sidewall.
        bridge=block(-15.8,-9, min(y,math.copysign(64.5,y))-1,max(y,math.copysign(64.5,y))+1,z-2,z+2) if abs(y)>50 else block(-15.8,-9,y-2,y+2,z,85.2)
        bridge=bridge & prism(130,0,86,14,-16,-8)
        skin=skin+boss+bridge
    rear=prism(130,0,86,14,-115,-113.4)
    for y,z in REAR_SCREWS:
        # cover local reinforcement + receivers attached to shell sidewall
        rear=rear+axial(3.3,2.7,(-113.65,y,z))
        rear=rear-axial(1.15,7,(-113,y,z))-axial(2.1,2.2,(-114.6,y,z))
        receiver=axial(3.2,5,(-109.8,y,z))-axial(.8,6,(-109.8,y,z))
        bridge=block(-112.3,-107.3,min(y,math.copysign(64,y))-2,max(y,math.copysign(64,y))+2,z-2,z+2) & prism(130,0,86,14,-113,-107)
        skin=skin+receiver+bridge
    add('main_octagonal_skin',skin,'R',alpha=.28,owner='M019a')
    add('removable_octagonal_rear_cover',rear,'R',alpha=.28,owner='M019a')
    # A 110-wide opaque border masks all glass outside the aperture.
    mask=prism(110,8,72,4,-2.65,-1.15)-prism(99,11,69,3,-3,-1)
    add('window_opaque_mask_110mm',mask,'R','#202728',owner='M003')
    add('window_clear_optical_area',prism(99,11,69,3,-2.65,-1.15),'R','#8b9a9d',alpha=.12,owner='M003')
    # Transparent glazing is represented by its perimeter, with image surface.
    add('active_display_95_04x53_86',block(-3.75,-3.55,-47.52,47.52,13.07,66.93),'R','#111f24',owner='M002')
    add('display_module_1to1_envelope',block(-14.4,-3.8,-53.05,53.05,6,74),'R','#245967',owner='M002')
    add('display_connector_and_flashing_access_reserve',block(-18,-14.4,-53.05,53.05,6,74),'R','#49adbe','reserve',.25)
    if catalog:
        camera=clean_catalog(CATALOG/'camera-module-3-wide.step').rotate(Axis.Y,-90).moved(Location((-10.805,-12.5,CAMERA_BOTTOM)))
    else:camera=block(-14.4,-2,-12.5,12.5,CAMERA_BOTTOM,CAMERA_BOTTOM+24)
    add('camera_module_3_wide_1to1',camera,'R','#2d5949',owner='M005')
    add('camera_CSI_exit_and_bend_reserve',block(-24,-14.5,-11,11,73,85),'R','#61a384','reserve',.3)
    # Separately removable U bracket: top/bottom edge clamp, behind camera PCB.
    camera_bracket=block(-17,-14.8,-15,15,74,100)-block(-18,-14,-12.9,12.9,76,98)
    add('removable_camera_edge_bracket_trial',camera_bracket,'R','#8c9e9a',owner='M005')
    add('addressable_status_LED_package_reserve',block(-8,-5,LED_Y-2.5,LED_Y+2.5,LED_Z-2.5,LED_Z+2.5),'R','#d3922d','reserve',.7,owner='M007')
    add('crown_status_light_diffuser',axial(1.7,2.9,(-3.55,LED_Y,LED_Z)),'R','#e4b35b',owner='M007')
    # C2 footprint is exact; installed height/USB socket are clearly reserved.
    add('C2_ESP32_S3_Zero_23_5x18_footprint',block(-26.6,-25,-38,-20,28,51.5),'R','#67559a',owner='M008')
    add('C2_installed_components_reserve',block(-34,-26.6,-38,-20,28,51.5),'R','#a58ac4','reserve',.35)
    add('C2_USB_C_withdrawal_BOOT_RESET_service_reserve',block(-33,-24,-35,-23,51.5,81.5),'R','#a58ac4','reserve',.18)
    # One connected rolling cradle: perimeter rails + cross + 4 flange struts.
    cradle=prism(116,2.5,76,8,-23.5,-21)-prism(110,5.5,73,6,-24,-20)
    cradle=cradle+block(-23.5,-21,-57,57,ROLL_Z-2.5,ROLL_Z+2.5)+block(-23.5,-21,ROLL_Y-3,ROLL_Y+3,3,75)
    flange=axial(17,3,(-37.5,ROLL_Y,ROLL_Z))+axial(5,3,(-38.5,ROLL_Y,ROLL_Z))
    for yoff in [-10,10]:
        for zoff in [-10,10]:
            cradle=cradle+axial(2.5,14,(-29,ROLL_Y+yoff,ROLL_Z+zoff))
            cradle=cradle+block(-23.5,-21,ROLL_Y+yoff-2.5,ROLL_Y+yoff+2.5,ROLL_Z-11,ROLL_Z+11)
    cradle=cradle+flange
    # Stalks run ahead of the pitch pins and connect to ear inner front rim.
    for sign in [-1,1]:
        stalk=block(-23.5,-15,sign*61-7,sign*61+7,EAR_Z-2,EAR_Z+2)
        pad=block(-23.5,-18,65,70.5,EAR_Z-7,EAR_Z+7)
        if sign==-1:pad=pad.moved(Location((0,-135.5,0)))
        stalk=stalk+pad
        for zoff in [-4,4]:stalk=stalk-axial(.8,10,(-20.5,sign*68,EAR_Z+zoff),'y')
        cradle=cradle+stalk
    # Lower rail notches follow the independently observed extreme-pose corner
    # clearance, while the middle rail stays connected through the central spine.
    cradle=cradle-block(-24,-20,38,48,1,5)-block(-24,-20,-48,-38,1,5)
    cradle=cradle-block(-24,-20,57,60,29,34)-block(-24,-20,-60,-57,29,34)
    add('connected_rolling_cradle_flange_ear_stalks',cradle,'R','#718d95',owner='M010')
    skin=out['main_octagonal_skin']['shape']
    for sign in [-1,1]:
        port=block(-24,-14.5,62,67,EAR_Z-7.5,EAR_Z+7.5)
        if sign==-1:port=port.moved(Location((0,-129,0)))
        skin=skin-port
    out['main_octagonal_skin']['shape']=tint(skin,'main_octagonal_skin','#e3ddc9')
    add('rolling_spindle_6mm',axial(3,32,(-56,ROLL_Y,ROLL_Z)),'R','#b7bfc0',owner='M016-18-R')
    for i,x in enumerate([-43,-65]):
        add(f'roll_bearing_{i+1}_16x6_reserve',axial(8,6,(x,ROLL_Y,ROLL_Z))-axial(3.1,8,(x,ROLL_Y,ROLL_Z)),'P','#acb5b9',owner='M016-18-P')
    cartridge=block(-69,-39,ROLL_Y-12,ROLL_Y+12,ROLL_Z-12,ROLL_Z+12)-axial(8.3,32,(-54,ROLL_Y,ROLL_Z))
    add('bearing_cartridge_trial',cartridge,'P','#c38a47',owner='M010-P')
    add('coaxial_coupling_trial',axial(6,8.5,(-73.25,ROLL_Y,ROLL_Z))-axial(3.1,10,(-73.25,ROLL_Y,ROLL_Z)),'R','#b7bfc0',owner='M013-15-R')
    if catalog:
        servo=clean_catalog(CATALOG/'xc330.stp')
        roll=servo.rotate(Axis.X,90).rotate(Axis.Z,90).moved(Location((-84,ROLL_Y,ROLL_Z)))
        pitch=servo.rotate(Axis.X,-90).rotate(Axis.Y,270).moved(Location((PITCH_X,40,PITCH_Z)))
    else:
        roll=block(-106.5,-77.5,ROLL_Y-10,ROLL_Y+10,ROLL_Z-24.5,ROLL_Z+9.5)
        pitch=block(PITCH_X-24.5,PITCH_X+9.5,17.5,46.5,PITCH_Z-10,PITCH_Z+10)
    add('roll_XC330_1to1_reference',roll,'P','#a36f38',owner='M013-15-roll')
    add('pitch_XC330_1to1_reference',pitch,'Y','#a36f38',owner='M013-15-pitch')
    # Connected pitch frame, with relieved crossbar and an actuator saddle.
    frame=block(-73,-39,-49,49,ROLL_Z-20,ROLL_Z-16)-block(-68,-44,-40,47,ROLL_Z-21,ROLL_Z-15)
    for y in [-49,49]:
        frame=frame+block(-74,PITCH_X+4,y-2,y+2,ROLL_Z-20,ROLL_Z-16)
        frame=frame+block(PITCH_X-6,PITCH_X+6,y-2,y+2,ROLL_Z-16,PITCH_Z+6)
        frame=frame-axial(4.2,6,(PITCH_X,y,PITCH_Z),'y')
        add(f'pitch_trunnion_{y}',axial(4,9,(PITCH_X,y,PITCH_Z),'y'),'P','#b7bfc0',owner='M016-18-P')
    frame=frame+block(-69,-39,ROLL_Y-12,ROLL_Y+12,ROLL_Z-16,ROLL_Z-12)
    saddle=block(-108,-75,ROLL_Y-12,ROLL_Y+12,ROLL_Z-27.5,ROLL_Z-24.8)
    for off in [-11.5,11.5]:
        saddle=saddle+block(-107,-74,ROLL_Y+off-1.3,ROLL_Y+off+1.3,ROLL_Z-26,ROLL_Z-12)
    saddle=saddle+block(-77,-70,ROLL_Y-13,ROLL_Y+13,ROLL_Z-25,ROLL_Z-16)
    frame=frame+saddle
    # Open the positive-Y front crossbar below the fixed pitch servo's sweep;
    # the rear crossbar, side arms and central cartridge seat remain connected.
    frame=frame-block(-46,-37,16,47,ROLL_Z-21,ROLL_Z-15)
    add('connected_pitch_frame_roll_servo_saddle',frame,'P','#c38a47',owner='M011-P')
    for y in [-55,55]:
        leg=extrude(Plane.XZ*Polygon((-74,-32),(-64,-32),(PITCH_X+4,PITCH_Z-8),(PITCH_X+4,PITCH_Z+6),(PITCH_X-6,PITCH_Z+6),(PITCH_X-6,PITCH_Z-6),align=None),amount=6).moved(Location((0,y+3,0)))
        leg=leg-axial(4.2,8,(PITCH_X,y,PITCH_Z),'y')
        add(f'yaw_yoke_leg_{y}',leg,'Y','#647787',owner='M011-Y')
    bridge=block(-74,-64,-58,58,-36,-32)+block(-74,PITCH_X+4,-7,7,-36,-32)
    add('yaw_yoke_spindle_bridge',bridge,'Y','#647787',owner='M012')
    # Fixed over-top adapter reservation ties pitch actuator location to yoke.
    # Exact XC330 mounting-hole pattern remains a detailing gate.
    adapter=block(PITCH_X-26,PITCH_X+4,17,55,PITCH_Z+11,PITCH_Z+13)
    adapter=adapter+block(PITCH_X-26,PITCH_X-24.8,17,41,PITCH_Z-11,PITCH_Z+13)
    adapter=adapter+block(PITCH_X-5,PITCH_X+3,52,58,PITCH_Z+6,PITCH_Z+13)
    add('pitch_servo_to_yoke_adapter_trial',adapter,'Y','#647787',owner='M011-Y')
    add('yaw_spindle_interface_reserve',axial(4,24,(PITCH_X,0,-48),'z'),'Y','#b7bfc0',owner='M016-18-Y')
    # Distinct layered ear rims and removable, hollow tapered caps.
    for sign in [-1,1]:
        c=(EAR_X,sign*66.5,EAR_Z)
        rim=axial(30,3,c,'y')-axial(28.8,5,c,'y')
        # thin concentric ribs on the dark inner ring
        for yy in [65.3,66.5,67.7]:rim=rim+axial(30,.35,(EAR_X,sign*yy,EAR_Z),'y')-axial(28.8,.7,(EAR_X,sign*yy,EAR_Z),'y')
        # Inboard reliefs must not leave isolated receiving bosses: an annular
        # web inside the hollow cap connects their far ends above the openings.
        rim=rim+(axial(26.5,1.6,(EAR_X,sign*71.3,EAR_Z),'y')-axial(20.3,2,(EAR_X,sign*71.3,EAR_Z),'y'))
        cap=Cone(30,27,6.2).rotate(Axis.X,-90*sign).moved(Location((EAR_X,sign*71.9,EAR_Z)))
        hollow=Cone(28.8,26.3,5.0).rotate(Axis.X,-90*sign).moved(Location((EAR_X,sign*70.9,EAR_Z)))
        cap=cap-hollow
        # Recessed centre leaves a 1.2 mm back wall, not an enormous solid disc.
        cap=cap-axial(22.5,.8,(EAR_X,sign*75,EAR_Z),'y')
        # Four actual cap screws and thickened receiving pads, cut after unions.
        screw_positions=[]
        for angle in [45,135,225,315]:
            a=math.radians(angle);xx=EAR_X+25*math.cos(a);zz=EAR_Z+25*math.sin(a)
            screw_positions.append((xx,zz))
            cap=cap+axial(2.6,3,(xx,sign*73.1,zz),'y')
            rim=rim+axial(2.6,4.4,(xx,sign*69.4,zz),'y')
            # connect the receiver to the circular ring behind the cap
            # radial bridge includes both boss and annular wall
            outerx=EAR_X+29.4*math.cos(a);outerz=EAR_Z+29.4*math.sin(a)
            rim=rim+block(min(xx,outerx)-1.4,max(xx,outerx)+1.4,65.8,68.5,min(zz,outerz)-1.4,max(zz,outerz)+1.4).moved(Location((0,0 if sign==1 else -134.3,0)))
        rim=rim & axial(30,9,(EAR_X,sign*68.5,EAR_Z),'y')
        for xx,zz in screw_positions:
            cap=cap-axial(1.15,8,(xx,sign*73,zz),'y')-axial(2.1,2.2,(xx,sign*74.6,zz),'y')
            cap=cap-axial(2.9,4.4,(xx,sign*69.4,zz),'y')
            rim=rim-axial(.8,6,(xx,sign*69.3,zz),'y')
            rim=rim-axial(2.9,1,(xx,sign*72.1,zz),'y')
            add(f'ear_{sign}_M2_{len([n for n in out if n.startswith(f"ear_{sign}_M2")])+1}',button_screw(xx,sign*73.5,zz,'y',sign),'R','#555b5a',owner='M021a')
        for zoff in [-4,4]:
            zz=EAR_Z+zoff
            rim=rim-axial(1.15,4,(-20.5,sign*71,zz),'y')
            rim=rim-axial(2.1,2,(-20.5,sign*72.6,zz),'y')
            add(f'ear_{sign}_hidden_mount_M2_{zoff}',button_screw(-20.5,sign*71.6,zz,'y',sign),'R','#535957',owner='M021-R')
        # Ear enclosure parts use the same inspection/X-ray material as the
        # front, side and rear skins; hardware and moving structure stay opaque.
        add(f'ear_{sign}_ridged_inner_mount',rim,'R','#303a3c',alpha=.20,owner='M019a')
        add(f'ear_{sign}_hollow_removable_cap',cap,'R',alpha=.20,owner='M019a')
        ring=axial(21.8,.18,(EAR_X,sign*74.69,EAR_Z),'y')-axial(21.1,.4,(EAR_X,sign*74.69,EAR_Z),'y')
        inset=axial(21,.15,(EAR_X,sign*74.675,EAR_Z),'y')
        add(f'ear_{sign}_amber_inlay',ring,'R','#b88636',alpha=.20,owner='M019a')
        add(f'ear_{sign}_dark_centre',inset,'R','#3d484a',alpha=.20,owner='M019a')
    # Front screws need an 8 mm reach from the -1.7 seat into shell receivers.
    # Model 10 mm shanks by extending the 6 mm reference only for these seats.
    for i,(y,z) in enumerate(FRONT_SCREWS):
        screw=button_screw(-1.7,y,z)+axial(1,4,(-9.7,y,z))
        add(f'front_M2x10_{i+1}',screw,'R','#535957',owner='M021a')
    for i,(y,z) in enumerate(REAR_SCREWS):
        add(f'rear_M2x6_{i+1}',button_screw(-113.5,y,z,'x',-1),'R','#535957',owner='M021a')
    if reliefs:
        # Window construction samples deliberately differ from verification.
        tools_by_side=[]
        for support_name in ['yaw_yoke_leg_-55','yaw_yoke_leg_55','yaw_yoke_spindle_bridge']:
            support=out[support_name]['shape']
            tools_by_side.append([support.rotate(PITCH_AXIS,-p).rotate(ROLL_AXIS,-r) for r in [-18,-12,0,12,18] for p in [-22,-10,0,20,40]])
        for name in ['main_octagonal_skin','ear_-1_ridged_inner_mount','ear_1_ridged_inner_mount','ear_-1_hollow_removable_cap','ear_1_hollow_removable_cap','connected_rolling_cradle_flange_ear_stalks']:
            s=out[name]['shape'];cuts=[]
            for tools in tools_by_side:
                bounds=[]
                for t in tools:
                    for c in pieces(s.intersect(t)):
                        if c.volume>1e-5:bounds.append(c.bounding_box())
                if bounds:
                    lo=[min(tuple(b.min)[i] for b in bounds)-2 for i in range(3)]
                    hi=[max(tuple(b.max)[i] for b in bounds)+2 for i in range(3)]
                    cuts.append(block(lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]))
            if cuts:out[name]['shape']=tint(s.cut(*cuts),name,'#718d95' if 'cradle' in name else '#e3ddc9' if 'cap' in name or 'skin' in name else '#303a3c')
    return out

def assembly(internals=False,roll=0,pitch=0,yaw=0):
    parts=build_parts()
    groups=[]
    for frame,label in [('R','rolling_face_and_large_ears'),('P','pitch_carried_roll_mechanism'),('Y','yaw_yoke_and_pitch_actuator')]:
        shapes=[]
        for n,d in parts.items():
            if d['frame']!=frame:continue
            if internals and d['owner']=='M019a':continue
            if internals and d['owner']=='M021a':continue
            if not internals and d['kind']=='reserve':continue
            s=d['shape']
            if frame=='R':s=s.rotate(ROLL_AXIS,roll)
            if frame in 'RP':s=s.rotate(PITCH_AXIS,pitch)
            s=s.rotate(YAW_AXIS,yaw)
            shapes.append(s)
        groups.append(Compound(label=label,children=shapes))
    return Compound(label='RP01_Layout02_1to1_PROVISIONAL',children=groups)
