"""Layout 03 service interfaces. Nominal fits remain trial pending purchased SKUs."""
import math
from build123d import *
import layout_model as m

INSERT_R,INSERT_DEPTH=1.6,3.0
INSERT_BREAKTHROUGH=0.4
# Boss/receiver insertion faces from layout_model axial seats; open the Ø3.2 pocket through.
FRONT_INSERT_FACE_X=-8.8
REAR_INSERT_FACE_X=-112.3
FRONT_INSERT_X=FRONT_INSERT_FACE_X+INSERT_BREAKTHROUGH-INSERT_DEPTH/2
REAR_INSERT_X=REAR_INSERT_FACE_X-INSERT_BREAKTHROUGH+INSERT_DEPTH/2

def slot(axis,radius,pin_radius,start,end,centre,length):
    """Circular-centreline slot with exact circular ends and fine polygon flanks.

    Stop contacts are defined by the endpoint circles, not the flank tessellation.
    """
    angles=[start+(end-start)*i/124 for i in range(125)]
    pts=[((radius+pin_radius)*math.cos(math.radians(a)),(radius+pin_radius)*math.sin(math.radians(a))) for a in angles]
    pts += [((radius-pin_radius)*math.cos(math.radians(a)),(radius-pin_radius)*math.sin(math.radians(a))) for a in reversed(angles)]
    s=extrude(Polygon(*pts,align=None),amount=length).moved(Location((0,0,-length/2)))
    for a in [start,end]:s=s+Cylinder(pin_radius,length).moved(Location((radius*math.cos(math.radians(a)),radius*math.sin(math.radians(a)),0)))
    if axis=='x':s=s.rotate(Axis.Y,90)  # local x -> -Z, local y -> Y
    elif axis=='y':s=s.rotate(Axis.X,90) # local x -> X, local y -> Z; extrusion -> -Y
    return s.moved(Location(centre))

def detail_parts(out):
    b,a=m.block,m.axial
    def setshape(n,s):
        d=out[n];d['shape']=m.tint(s,n,d['color'],d['alpha'])
    def add(n,s,f='R',owner='M010',color='#718d95',kind='physical',alpha=1):
        out[n]=dict(shape=m.tint(s,n,color,alpha),frame=f,kind=kind,owner=owner,color=color,alpha=alpha)
    from optics import cone
    name='front_bezel_integral_camera_crown'
    face=out[name]['shape']-cone(m.CAMERA_BOTTOM+14.4,xend=1,margin=.4)
    # Open crown rear wall for the 30 mm straight CSI exit corridor.
    face=face-b(-25,-22,-18,18,75,103)-b(-25,-17,-3,3,78,82)
    setshape(name,face)
    # M2 heat-set receivers. Recut after bridges so the union cannot fill them.
    n='main_octagonal_skin';skin=out[n]['shape']
    for y,z in m.FRONT_SCREWS:skin=skin-a(INSERT_R,INSERT_DEPTH,(FRONT_INSERT_X,y,z))
    for y,z in m.REAR_SCREWS:skin=skin-a(INSERT_R,INSERT_DEPTH,(REAR_INSERT_X,y,z))
    # Two integral recessed stern lands: match the tapered plane, retain >=0.8 wall.
    for sign in [-1,1]:
        land=b(-104,-84,min(sign*50,sign*64),max(sign*50,sign*64),27,59)
        outer=m.stern(-104,-84);inner=m.stern(-104,-84,inside=True)
        # Shallow offsets on tapered sides via translated outer cutter.
        shifted=outer.moved(Location((0,-sign*.35,0)))
        shallow=(outer-shifted).intersect(land)
        if shallow:skin=skin-shallow
    setshape(n,skin)
    for sign in [-1,1]:
        n=f'ear_{sign}_ridged_inner_mount';s=out[n]['shape']
        for angle in [45,135,225,315]:
            t=math.radians(angle);x=m.EAR_X+25*math.cos(t);z=m.EAR_Z+25*math.sin(t)
            s=s-a(INSERT_R,3,(x,sign*69.4,z),'y')
        setshape(n,s)
        n='connected_rolling_cradle_flange_ear_stalks';s=out[n]['shape']
        for dz in [-4,4]:s=s-a(INSERT_R,3,(-20.5,sign*68.8,m.EAR_Z+dz),'y')
        setshape(n,s)
    # C2 cage is open at rear and top. Board remains at the exact original seat.
    tray=b(-24.8,-23.6,-40,-18,26,54)
    tray=tray+b(-35,-24,-40,-38.3,26,54)+b(-35,-24,-19.7,-18,26,54)
    tray=tray+b(-35,-24,-40,-18,26,27.7)
    # Front seating pads support the PCB without occupying its nominal volume.
    # Carrier is screwed to the existing rolling crossbar, reachable from rear.
    cradle=out['connected_rolling_cradle_flange_ear_stalks']['shape']
    for y in [-39,-19]:
        z=m.ROLL_Z
        tray=tray+a(2.8,2.4,(-25,y,z))
        tray=tray-a(1.15,5,(-25,y,z))
        boss=a(3,3,(-22,y,z))-a(INSERT_R,3.2,(-22,y,z))
        cradle=cradle+boss
        cradle=cradle-a(INSERT_R,3.4,(-22,y,z))
        screw=m.button_screw(-26.2,y,z,'x',-1)
        add(f'C2_tray_M2_{y}',screw,owner='M021-R',color='#555b5a')
    setshape('connected_rolling_cradle_flange_ear_stalks',cradle)
    tray=tray-b(-34.1,-24.9,-38.1,-19.9,27.9,51.6)-b(-33.1,-23.9,-35.1,-22.9,51.5,55)
    # PCB edge keepers: rear jaws at the castellated Y margins, corner caps above
    # the USB-end corners (outside Y −35…−23). Board drop-in snaps past the caps.
    for y0,y1 in [(-38.45,-36.9),(-21.1,-19.55)]:
        tray=tray+b(-27.55,-26.70,y0,y1,28.15,51.35)
    tray=tray+b(-26.70,-24.80,-38.45,-35.15,51.60,52.90)
    tray=tray+b(-26.70,-24.80,-22.85,-19.55,51.60,52.90)
    add('C2_removable_open_rear_tray',tray,owner='M008')
    add('C2_USB_C_installed_plug_reserve',b(-33,-24,-35,-23,51.5,61.5),owner=None,kind='reserve',color='#b58ed0',alpha=.18)
    # Split the former single corridor into installed plug and withdrawal.
    setshape('C2_USB_C_withdrawal_BOOT_RESET_service_reserve',b(-33,-24,-35,-23,61.5,81.5))
    add('C2_BOOT_RESET_rear_tool_access_reserve',b(-114,-34,-36,-22,33,49),owner=None,kind='reserve',color='#b58ed0',alpha=.12)
    # Bearing cartridge: Ø16.2 trial seats, 6 mm long, 22 mm apart;
    # Ø12 central clearance leaves shoulders supporting only the outer race.
    cartridge=b(-69,-39,m.ROLL_Y-12,m.ROLL_Y+12,m.ROLL_Z-12,m.ROLL_Z+12)-a(6,32,(-54,m.ROLL_Y,m.ROLL_Z))
    for x in [-43,-65]:cartridge=cartridge-a(8.1,6.2,(x,m.ROLL_Y,m.ROLL_Z))
    # End counterbores and split removable plates give axial assembly access.
    cartridge=cartridge-a(8.1,3,(-39.5,m.ROLL_Y,m.ROLL_Z))-a(8.1,3,(-68.5,m.ROLL_Y,m.ROLL_Z))
    for x in [-39.5,-68.5]:
        plate=a(10,.8,(x,m.ROLL_Y,m.ROLL_Z))-a(6,2,(x,m.ROLL_Y,m.ROLL_Z))
        # Housing relieved for the separate retainer; centre boss does not grab shaft.
        cartridge=cartridge-a(10.2,1,(x,m.ROLL_Y,m.ROLL_Z))
        for dy in [-9,9]:
            plate=plate-a(1.15,2,(x,m.ROLL_Y+dy,m.ROLL_Z))
            cartridge=cartridge-a(INSERT_R,3,(x+(-2 if x>-50 else 2),m.ROLL_Y+dy,m.ROLL_Z))
        if x>-50:plate=plate-slot('x',10.5,.9,162,198,(x,m.ROLL_Y,m.ROLL_Z),2)
        add(f'roll_bearing_retainer_{abs(x):g}',plate,'P','M010-P','#c38a47')
        for dy in [-9,9]:
            sign=1 if x>-50 else -1
            add(f'bearing_retainer_M2_{abs(x):g}_{dy}',m.button_screw(x+sign*.4,m.ROLL_Y+dy,m.ROLL_Z,'x',sign),'P','M021-P','#555b5a')
    # Four vertical cartridge fixing screws into the pitch-frame support slab.
    frame=out['connected_pitch_frame_roll_servo_saddle']['shape']
    for x in [-62,-46]:
        for dy in [-10,10]:
            y=m.ROLL_Y+dy
            cartridge=cartridge-a(1.15,26,(x,y,m.ROLL_Z),'z')
            frame=frame-a(INSERT_R,4,(x,y,m.ROLL_Z-14),'z')
    setshape('connected_pitch_frame_roll_servo_saddle',frame)
    setshape('bearing_cartridge_trial',cartridge)
    # Radial opposed M3 grub screw scheme; shaft still supported by bearings.
    hub=out['coaxial_coupling_trial']['shape']
    for x in [-74.5,-71.5]:hub=hub-a(1.25,7,(x,m.ROLL_Y+4,m.ROLL_Z),'y')
    setshape('coaxial_coupling_trial',hub)
    # Roll pin protrudes from the existing flange into a sector slot in the
    # cartridge front wall at radius 10.5; neutral points toward +Z.
    R=10.5;pr=.9
    pin=a(pr,2,(-39.8,m.ROLL_Y,m.ROLL_Z+R))
    add('roll_hard_stop_pin',pin,owner='M016-18-R',color='#cc5750')
    setshape('connected_rolling_cradle_flange_ear_stalks',out['connected_rolling_cradle_flange_ear_stalks']['shape']-pin)
    cartridge=out['bearing_cartridge_trial']['shape']
    # local angle 180 places the radial centre on +Z after the Y rotation.
    cartridge=cartridge-slot('x',R,pr,162,198,(-40,m.ROLL_Y,m.ROLL_Z),3)
    setshape('bearing_cartridge_trial',cartridge)
    # Pitch sector at the passive (-Y) trunnion, clear of the one-sided actuator.
    # Annular plate grows from the yoke, with rearward neutral pin at X-axis -10.
    ring=a(14,2,(m.PITCH_X,-53,m.PITCH_Z),'y')-a(4.2,3,(m.PITCH_X,-53,m.PITCH_Z),'y')
    ring=ring-slot('y',10,1,140,202,(m.PITCH_X,-53,m.PITCH_Z),4)
    leg=out['yaw_yoke_leg_-55']['shape']
    setshape('yaw_yoke_leg_-55',(leg+ring)-slot('y',10,1,140,202,(m.PITCH_X,-53,m.PITCH_Z),4))
    add('pitch_hard_stop_pin',a(1,4,(m.PITCH_X-10,-52,m.PITCH_Z),'y'),'P','M016-18-P','#cc5750')
    # Pin root lug joins the pitch frame side arm.
    frame=out['connected_pitch_frame_roll_servo_saddle']['shape']
    lug=b(m.PITCH_X-11,m.PITCH_X-4,-51,-47,m.PITCH_Z-2,m.PITCH_Z+2)
    setshape('connected_pitch_frame_roll_servo_saddle',(frame+lug)-out['pitch_hard_stop_pin']['shape'])
    # Independent camera bracket: PCB Y-edge C-channels plus two rear-access M2
    # screws into long crown receivers. Boss centres clear the 25 mm board.
    face=out['front_bezel_integral_camera_crown']['shape']
    bracket=out['removable_camera_edge_bracket_trial']['shape']
    for y in [-15,15]:
        z=78.5
        boss=a(2.2,12.8,(-8.2,y,z))-a(INSERT_R,3.2,(-13.2,y,z))
        face=face+boss
        bracket=bracket+a(2.2,2.2,(-15.9,y,z))
        bracket=bracket-a(1.15,4,(-15.9,y,z))
        add(f'camera_bracket_M2_{y}',m.button_screw(-17,y,z,'x',-1),'R','M021-R','#555b5a')
    setshape('front_bezel_integral_camera_crown',face)
    setshape('removable_camera_edge_bracket_trial',bracket)
    # Removable roll-servo top strap, fixed to the saddle rather than drilled
    # into an unselected servo SKU. 0.3 mm liner space remains beside housing.
    yy=m.ROLL_Y;zz=m.ROLL_Z
    strap=b(-102,-98,yy-13.8,yy+13.8,zz+9.8,zz+11.8)
    for dy in [-12,12]:
        strap=strap+b(-102,-98,yy+dy-1.7,yy+dy+1.7,zz-12,zz+11.8)
        strap=strap-a(1.15,26,(-100,yy+dy,zz),'z')
    add('removable_roll_servo_saddle_strap',strap,'P','M011-P','#c38a47')
    frame=out['connected_pitch_frame_roll_servo_saddle']['shape']
    for dy in [-12,12]:frame=frame-a(INSERT_R,3,(-100,yy+dy,zz-13.5),'z')
    setshape('connected_pitch_frame_roll_servo_saddle',frame)
    # Explicit radial fasteners; nominal M3 tapped metal bores in coupling.
    for x in [-74.5,-71.5]:
        add(f'coupling_M3_radial_grub_{abs(x):g}',a(1.5,3,(x,yy+4.5,zz),'y'),'R','M021-R','#555b5a')
    # CSI guide saddle contacts the existing inner roof. The passage gives the
    # trial OD2 jacket 0.4 mm diametral clearance and is open in both directions.
    guide=b(-49,-45,-4,4,78.6,84.8)-a(1.2,6,(-47,0,80))
    add('CSI_roof_straight_exit_guide',guide,'R','M010','#678c81')
