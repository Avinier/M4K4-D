"""Layout 04 service interfaces. Nominal fits remain trial pending purchased SKUs."""
import math
from build123d import *
import layout_model as m

INSERT_R,INSERT_DEPTH=1.6,3.0
INSERT_BREAKTHROUGH=0.4
# Roll bearings: 696-2Z (ISO 619/6-2Z), d6 x D15 x B5, a stock deep-groove
# size. Seats are D + 0.1 mm diametral trial slip fit, B + 0.2 mm long;
# retention is the end plates, preload is a printed-fit item for the bench.
ROLL_BEARING=dict(sku='696-2Z (ISO 619/6-2Z)',d=6.,D=15.,B=5.)
BEARING_SEAT_R=ROLL_BEARING['D']/2+.05
BEARING_SEAT_L=ROLL_BEARING['B']+.2
# Hard-stop pins: ISO 8734 hardened steel dowels, press fit in printed bores.
ROLL_STOP_PIN=dict(d=2.,l=5.)
PITCH_STOP_PIN=dict(d=2.,l=8.)
# Front retainer screw heads ride under the rolling flange: swept pockets
# cover the stop travel plus 1 deg overtravel and 0.5 mm radial clearance.
FLANGE_POCKET_CLEAR=.5
FLANGE_POCKET_BACK_X=-37.3
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
    # Bearing cartridge: two 696-2Z seats 22 mm apart; the Ø12 central
    # clearance leaves shoulders on the outer race only.
    cartridge=b(-69,-39,m.ROLL_Y-12,m.ROLL_Y+12,m.ROLL_Z-12,m.ROLL_Z+12)-a(6,32,(-54,m.ROLL_Y,m.ROLL_Z))
    for x in [-43,-65]:cartridge=cartridge-a(BEARING_SEAT_R,BEARING_SEAT_L,(x,m.ROLL_Y,m.ROLL_Z))
    # End counterbores and split removable plates give axial assembly access.
    cartridge=cartridge-a(BEARING_SEAT_R,3,(-39.5,m.ROLL_Y,m.ROLL_Z))-a(BEARING_SEAT_R,3,(-68.5,m.ROLL_Y,m.ROLL_Z))
    for x in [-39.5,-68.5]:
        plate=a(10,.8,(x,m.ROLL_Y,m.ROLL_Z))-a(6,2,(x,m.ROLL_Y,m.ROLL_Z))
        # Housing relieved for the separate retainer; centre boss does not grab shaft.
        cartridge=cartridge-a(10.2,1,(x,m.ROLL_Y,m.ROLL_Z))
        for dy in [-9,9]:
            plate=plate-a(1.15,2,(x,m.ROLL_Y+dy,m.ROLL_Z))
            cartridge=cartridge-a(INSERT_R,3,(x+(-2 if x>-50 else 2),m.ROLL_Y+dy,m.ROLL_Z))
        if x>-50:plate=plate-slot('x',10.5,ROLL_STOP_PIN['d']/2,180+m.ROLL_STOP[0],180+m.ROLL_STOP[1],(x,m.ROLL_Y,m.ROLL_Z),2)
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
    # Roll pin: Ø2 x 5 dowel pressed through the whole 3 mm flange, its tip in
    # a sector slot in the cartridge front wall at radius 10.5; neutral +Z.
    R=10.5;pr=ROLL_STOP_PIN['d']/2
    pin=a(pr,ROLL_STOP_PIN['l'],(-40.8+ROLL_STOP_PIN['l']/2,m.ROLL_Y,m.ROLL_Z+R))
    add('roll_hard_stop_pin',pin,owner='M016-18-R',color='#cc5750')
    setshape('connected_rolling_cradle_flange_ear_stalks',out['connected_rolling_cradle_flange_ear_stalks']['shape']-pin)
    # Swept pockets in the flange's back face for the two front retainer screw
    # heads (radius 9 on +/-Y; local angle 90 is +Y after the Y rotation).
    # This removes the Layout 03 audit's 5.53 mm3 screw/flange overlaps.
    sweep=m.ROLL_STOP[1]+1
    head_r=1.75+FLANGE_POCKET_CLEAR
    x0=-39.6;length=FLANGE_POCKET_BACK_X-x0
    cradle=out['connected_rolling_cradle_flange_ear_stalks']['shape']
    for centre in [90,270]:
        cradle=cradle-slot('x',9,head_r,centre-sweep,centre+sweep,(x0+length/2,m.ROLL_Y,m.ROLL_Z),length)
    setshape('connected_rolling_cradle_flange_ear_stalks',cradle)
    cartridge=out['bearing_cartridge_trial']['shape']
    # local angle 180 places the radial centre on +Z after the Y rotation.
    # Slot ends are the roll hard stops, 3 deg beyond usable travel.
    cartridge=cartridge-slot('x',R,pr,180+m.ROLL_STOP[0],180+m.ROLL_STOP[1],(-40,m.ROLL_Y,m.ROLL_Z),3)
    setshape('bearing_cartridge_trial',cartridge)
    # Pitch sector at the passive (-Y) trunnion, clear of the one-sided actuator.
    # Annular plate grows from the yoke, with rearward neutral pin at X-axis -10.
    ring=a(14,2,(m.PITCH_X,-53,m.PITCH_Z),'y')-a(4.2,3,(m.PITCH_X,-53,m.PITCH_Z),'y')
    # Slot ends are the pitch hard stops (chin-down end first), 3 deg beyond usable travel.
    pitch_slot=(180-m.PITCH_STOP[1],180-m.PITCH_STOP[0])
    ring=ring-slot('y',10,1,*pitch_slot,(m.PITCH_X,-53,m.PITCH_Z),4)
    leg=out['yaw_yoke_leg_-55']['shape']
    setshape('yaw_yoke_leg_-55',(leg+ring)-slot('y',10,1,*pitch_slot,(m.PITCH_X,-53,m.PITCH_Z),4))
    # Ø2 x 8 dowel: 2 mm in the yoke slot ring, 5 mm pressed into the root lug.
    add('pitch_hard_stop_pin',a(PITCH_STOP_PIN['d']/2,PITCH_STOP_PIN['l'],(m.PITCH_X-10,-54+PITCH_STOP_PIN['l']/2,m.PITCH_Z),'y'),'P','M016-18-P','#cc5750')
    # Pin root lug joins the pitch frame side arm.
    frame=out['connected_pitch_frame_roll_servo_saddle']['shape']
    lug=b(m.PITCH_X-11,m.PITCH_X-4,-51,-46,m.PITCH_Z-2,m.PITCH_Z+2)
    frame=(frame+lug)-out['pitch_hard_stop_pin']['shape']
    # Roll stops at +/-21 swing the C2 castellated exit (R-frame, OD2 trial
    # jacket) onto the lower rail; relieve the rail with 0.4 mm clearance.
    c2_exit=a(1.4,30,(-50,-29,42))
    for r in [19,20,21]:frame=frame-c2_exit.rotate(m.ROLL_AXIS,r)
    setshape('connected_pitch_frame_roll_servo_saddle',frame)
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
    stiffen_and_trim(out,add,setshape)

# Structure revision 2026-09-25 (RP-01 P07). The Layout 03 audit screened the
# open pitch frame at 1.1-2.5 N*m/rad: pitch torque from the +Y trunnion ran
# through 4 x 4 mm rails in bending and a 5 x 4 mm rear rail in torsion. It now
# runs trunnion arm -> deep side web -> hollow rear torsion box -> cartridge
# slab and saddle. The roll servo also bolts its case to the box through the
# two lower front-face M2 holes of the official ROBOTIS drawing (16 mm apart,
# 22.5 mm below the output axis), so roll reaction no longer twists the open
# saddle. Stiffness is a hand screen in RP-01 fullproofmath.md sec. 12.1.
BOX_X=(-80.5,-68.)          # rear wall on the servo case face; front clear of the pitch servo sweep
BOX_DZ=(-26.5,-12.5)        # below ROLL_Z; top clears the cartridge by 0.5 mm
BOX_HALF_Y=51.
BOX_WALL=3.
WEB_T=4.
KEEL_X=(-69.,-39.)          # the cartridge slab's X span; overlaps the box front wall by 1 mm
KEEL_HALF_Y=12.
CASE_SCREW_DY,CASE_SCREW_DZ=8.,-22.5
C2_NOTCH_Y=(-37.,-21.)      # C2 BOOT/RESET rear tool corridor is Y -36..-22, Z >= 33
C2_NOTCH_TOP_Z=32.7          # absolute, as the reserve is
# Balance trim (RP-01 P08): removable mass at three seats. Ear caps carry
# tungsten Ø12 slugs (roll, lever ~71 mm); the rear cover carries brass Ø20
# washers on the roll axis (pitch, lever ~70 mm; coaxial, so no roll effect).
EAR_SLUG=dict(r=6.,max_len=4.,density=19.3e-3)
REAR_STACK=dict(r=10.,max_len=3.,density=8.5e-3)
TRIM_NOMINAL_FRACTION=.5

def trim_capacity():
    ear=math.pi*EAR_SLUG['r']**2*EAR_SLUG['max_len']*EAR_SLUG['density']
    rear=math.pi*REAR_STACK['r']**2*REAR_STACK['max_len']*REAR_STACK['density']
    return dict(ear_slug_max_g=ear,rear_stack_max_g=rear)

def stiffen_and_trim(out,add,setshape):
    b,a=m.block,m.axial
    rz,ry=m.ROLL_Z,m.ROLL_Y
    n='connected_pitch_frame_roll_servo_saddle';frame=out[n]['shape']
    z0,z1=rz+BOX_DZ[0],rz+BOX_DZ[1]
    box=b(BOX_X[0],BOX_X[1],-BOX_HALF_Y,BOX_HALF_Y,z0,z1)
    webs=[b(BOX_X[0],m.PITCH_X+4,s*(BOX_HALF_Y-WEB_T/2)-WEB_T/2,s*(BOX_HALF_Y-WEB_T/2)+WEB_T/2,z0,m.PITCH_Z-6) for s in (-1,1)]
    frame=frame+box
    for w in webs:frame=frame+w
    w=BOX_WALL
    # Local 2.5 mm step down under the C2 BOOT/RESET rear tool corridor
    # (Y -36..-22 from Z 33). It is on the passive -Y side, outside the +Y
    # trunnion -> centre torque path, and the section stays closed.
    ny0,ny1,nz=C2_NOTCH_Y[0],C2_NOTCH_Y[1],C2_NOTCH_TOP_Z
    cavity=b(BOX_X[0]+w,BOX_X[1]-w,-BOX_HALF_Y+w,BOX_HALF_Y-w,z0+w,z1-w)-b(BOX_X[0],BOX_X[1],ny0-w,ny1+w,nz-w,z1)
    frame=frame-cavity-b(BOX_X[0]-.1,BOX_X[1]+.1,ny0,ny1,nz,z1+.1)
    # Hollow keel under the cartridge slab, fused to the box's front wall over
    # its full height. FEA put 51% of the pitch twist in the 1 mm box-to-slab
    # strip and the 4 mm slab; |Y| < 17 here is clear of every Y-frame part.
    kx0,kx1=KEEL_X
    frame=frame+b(kx0,kx1,ry-KEEL_HALF_Y,ry+KEEL_HALF_Y,z0,rz-16)
    frame=frame-b(kx0+w,kx1-w,ry-KEEL_HALF_Y+w,ry+KEEL_HALF_Y-w,z0+w,rz-16)
    zc=rz+CASE_SCREW_DZ
    for dy in (-CASE_SCREW_DY,CASE_SCREW_DY):
        y=ry+dy
        frame=frame-a(1.15,w+2,(BOX_X[0]+w/2,y,zc))          # M2 clearance, rear wall
        frame=frame-a(2.25,w+2,(BOX_X[1]-w/2,y,zc))          # Ø4.5 driver access, front wall
        add(f'roll_servo_case_M2_{dy:g}',m.button_screw(BOX_X[0]+w,y,zc,'x',1),'P','M021-P','#555b5a')
    setshape(n,frame)
    # Ear-cap trim seats: M2 insert boss on the cap's inner back wall; slug
    # stack envelope at full capacity is a physical part so the motion grid
    # checks it.
    for sign in (-1,1):
        cn=f'ear_{sign}_hollow_removable_cap';cap=out[cn]['shape']
        c=(m.EAR_X,sign*72.4,m.EAR_Z)
        cap=cap+a(3.5,2,c,'y')
        cap=cap-a(INSERT_R,3,(m.EAR_X,sign*72.9,m.EAR_Z),'y')
        setshape(cn,cap)
        slug=a(EAR_SLUG['r'],EAR_SLUG['max_len'],(m.EAR_X,sign*(71.4-EAR_SLUG['max_len']/2),m.EAR_Z),'y')
        add(f'ear_{sign}_trim_slug_stack_max',slug,'R','M022-R','#8d8f93')
    # Rear-cover seat on the roll axis: M3 insert boss, brass washer stack.
    cn='removable_octagonal_rear_cover';cover=out[cn]['shape']
    cover=cover+a(4.5,2.5,(-112.15,ry,rz))
    cover=cover-a(2.,3.5,(-112.65,ry,rz))
    setshape(cn,cover)
    stack=a(REAR_STACK['r'],REAR_STACK['max_len'],(-110.9+REAR_STACK['max_len']/2,ry,rz))
    add('rear_pitch_trim_washer_stack_max',stack,'R','M022-R','#b88636')
