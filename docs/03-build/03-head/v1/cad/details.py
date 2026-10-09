"""Layout 04 service interfaces. Nominal fits remain trial pending purchased SKUs."""
import math
from build123d import *
import layout_model as m
import feetech as fe

INSERT_R,INSERT_DEPTH=1.6,3.0
INSERT_BREAKTHROUGH=0.4
# One M2 heat-set article for every printed receiver: Ø3.2 pilot, 3 mm long.
# min_engagement is the shank length that must sit inside the insert.
TIP_RELIEF_R=1.1
LAND_DOUBLER=.5
RETAINER_T,RETAINER_RELIEF=1.2,1.4
RETAINER_SCREW_R=10.5
RETAINER_SCREW_DEG=(225,315)
# Rear pair moved forward with the rear bearing (D-049, was X-62).
CARTRIDGE_SCREW_X=fe.CARTRIDGE_SCREW_X
EAR_CAP_SCREW_DEG=(30,150)
EAR_RECEIVER_FACE=71.6
CAMERA_SCREW_Y=16
M2_INSERT=dict(spec='M2 x 3 brass heat-set insert, Ø3.2 pilot',pilot_d=2*INSERT_R,length=INSERT_DEPTH,min_engagement=2.4)
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
FRONT_INSERT_FACE_X=-5.0
REAR_INSERT_FACE_X=-112.3
# Front/rear pockets are 3.5 mm deep in plastic (insert plus 0.5 melt room),
# plus the 0.4 mm open mouth; the old 3 mm cut left only 2.6 mm in plastic.
INSERT_POCKET=INSERT_DEPTH+.5
FRONT_INSERT_X=FRONT_INSERT_FACE_X+INSERT_BREAKTHROUGH-(INSERT_POCKET+INSERT_BREAKTHROUGH)/2
REAR_INSERT_X=REAR_INSERT_FACE_X-INSERT_BREAKTHROUGH+(INSERT_POCKET+INSERT_BREAKTHROUGH)/2

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
    # The opening follows the crown cavity, so the sloped sides and roof keep
    # their full wall (a +/-18 box notched them to 0.45 mm).
    rear_opening=[(y,max(z,75.)) for y,z in m.crown_inner()]
    face=face-extrude(Plane.YZ*Polygon(*rear_opening,align=None),amount=3).moved(Location((-25,0,0)))-b(-25,-17,-3,3,78,82)
    setshape(name,face)
    # M2 heat-set receivers. Recut after bridges so the union cannot fill them.
    n='main_octagonal_skin';skin=out[n]['shape']
    # Ø2.2 tip reliefs beyond each pocket: the M2 x 8 front and M2 x 6 rear
    # screws pass 1.2 / 1.3 mm beyond theirs.
    for y,z in m.FRONT_SCREWS:
        skin=skin-a(INSERT_R,INSERT_POCKET+INSERT_BREAKTHROUGH,(FRONT_INSERT_X,y,z))
        skin=skin-a(TIP_RELIEF_R,2,(FRONT_INSERT_FACE_X-INSERT_POCKET-1,y,z))
    for y,z in m.REAR_SCREWS:
        skin=skin-a(INSERT_R,INSERT_POCKET+INSERT_BREAKTHROUGH,(REAR_INSERT_X,y,z))
        skin=skin-a(TIP_RELIEF_R,2,(REAR_INSERT_FACE_X+INSERT_POCKET+1,y,z))
    # Two integral recessed stern lands: match the tapered plane, retain >=0.8 wall.
    for sign in [-1,1]:
        land=b(-104,-84,min(sign*50,sign*64),max(sign*50,sign*64),27,59)
        outer=m.stern(-104,-84);inner=m.stern(-104,-84,inside=True)
        # Shallow offsets on tapered sides via translated outer cutter.
        shifted=outer.moved(Location((0,-sign*.35,0)))
        shallow=(outer-shifted).intersect(land)
        if shallow:
            # 0.5 mm inner doubler behind the recess keeps >= 1.2 mm normal wall.
            doubler=(inner-m.stern(-104,-84,inside=True,wall=m.SKIN+LAND_DOUBLER)).intersect(land)
            skin=skin+doubler-shallow
    setshape(n,skin)
    for sign in [-1,1]:
        n=f'ear_{sign}_ridged_inner_mount';s=out[n]['shape']
        for angle in EAR_CAP_SCREW_DEG:
            t=math.radians(angle);x=m.EAR_X+25*math.cos(t);z=m.EAR_Z+25*math.sin(t)
            # Pocket from the receiver face (|Y| 71.6) inward, 0.4 mm open above it.
            s=s-a(INSERT_R,INSERT_DEPTH+INSERT_BREAKTHROUGH,(x,sign*(EAR_RECEIVER_FACE-INSERT_DEPTH/2+INSERT_BREAKTHROUGH/2),z),'y')
            s=s-a(TIP_RELIEF_R,1.6,(x,sign*(EAR_RECEIVER_FACE-INSERT_DEPTH-.8),z),'y')
        setshape(n,s)
        n='connected_rolling_cradle_flange_ear_stalks';s=out[n]['shape']
        for dz in [-4,4]:
            top=m.EAR_PAD_TOP
            s=s-a(INSERT_R,INSERT_DEPTH+.2,(-20.5,sign*(top+.1-INSERT_DEPTH/2),m.EAR_Z+dz),'y')
            s=s-a(TIP_RELIEF_R,1.5,(-20.5,sign*(top-INSERT_DEPTH-.75),m.EAR_Z+dz),'y')
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
    tray=tray-b(-34.1,-24.9,-38.1,-19.9,27.9,51.6)-b(-33.1,-23.5,-35.1,-22.9,51.5,55)
    # PCB edge keepers: rear jaws at the castellated Y margins, corner caps above
    # the USB-end corners (outside Y −35…−23). Board drop-in snaps past the caps.
    for y0,y1 in [(-38.45,-36.9),(-21.1,-19.55)]:
        tray=tray+b(-27.95,-26.70,y0,y1,28.15,51.35)
    tray=tray+b(-26.70,-24.80,-38.45,-35.15,51.60,52.90)
    tray=tray+b(-26.70,-24.80,-22.85,-19.55,51.60,52.90)
    add('C2_removable_open_rear_tray',tray,owner='M008')
    add('C2_USB_C_installed_plug_reserve',b(-33,-24,-35,-23,51.5,61.5),owner=None,kind='reserve',color='#b58ed0',alpha=.18)
    # Split the former single corridor into installed plug and withdrawal.
    setshape('C2_USB_C_withdrawal_BOOT_RESET_service_reserve',b(-33,-24,-35,-23,61.5,81.5))
    add('C2_BOOT_RESET_rear_tool_access_reserve',b(-114,-34,-36,-22,33,49),owner=None,kind='reserve',color='#b58ed0',alpha=.12)
    # Bearing cartridge: two 696-2Z seats 22 mm apart; the Ø12 central
    # clearance leaves shoulders on the outer race only.
    cx0,cx1=fe.CARTRIDGE_X
    cartridge=b(cx0,cx1,m.ROLL_Y-12,m.ROLL_Y+12,m.ROLL_Z-12,m.ROLL_Z+12)-a(6,cx1-cx0+2,((cx0+cx1)/2,m.ROLL_Y,m.ROLL_Z))
    for x in fe.ROLL_BEARING_X:cartridge=cartridge-a(BEARING_SEAT_R,BEARING_SEAT_L,(x,m.ROLL_Y,m.ROLL_Z))
    # End counterbores and split removable plates give axial assembly access.
    cartridge=cartridge-a(BEARING_SEAT_R,3,(cx1-.5,m.ROLL_Y,m.ROLL_Z))-a(BEARING_SEAT_R,3,(cx0+.5,m.ROLL_Y,m.ROLL_Z))
    # Retainer plates are 1.2 mm prints in 1.4 mm deep end reliefs, 0.2 mm off
    # the bearing outer race. Their two M2 x 4 screws sit on the lower
    # diagonals at R10.5: at the old R9 on +/-Y the Ø3.2 insert pockets broke
    # 0.15 mm into the Ø15.1 bearing seats. Here they keep 1.35 mm to the
    # seat and 3 mm to the cartridge faces, and their swept head pockets in
    # the rolling flange stay clear of the roll stop pin.
    hole_yz=[(m.ROLL_Y+RETAINER_SCREW_R*math.cos(math.radians(p)),m.ROLL_Z+RETAINER_SCREW_R*math.sin(math.radians(p))) for p in RETAINER_SCREW_DEG]
    for face,out_dir in [(fe.CARTRIDGE_X[1],1),(fe.CARTRIDGE_X[0],-1)]:
        xc=face-out_dir*(.1+RETAINER_T/2)
        plate=a(10,RETAINER_T,(xc,m.ROLL_Y,m.ROLL_Z))
        relief=a(10.2,RETAINER_RELIEF,(face-out_dir*RETAINER_RELIEF/2,m.ROLL_Y,m.ROLL_Z))
        for y,z in hole_yz:
            plate=plate+a(2.4,RETAINER_T,(xc,y,z))
            relief=relief+a(2.6,RETAINER_RELIEF,(face-out_dir*RETAINER_RELIEF/2,y,z))
        # Housing relieved for the separate retainer; centre boss does not grab shaft.
        cartridge=cartridge-relief
        plate=plate-a(6,2,(xc,m.ROLL_Y,m.ROLL_Z))
        floor=face-out_dir*RETAINER_RELIEF
        for y,z in hole_yz:
            plate=plate-a(1.15,2,(xc,y,z))
            cartridge=cartridge-a(INSERT_R,INSERT_DEPTH,(floor-out_dir*INSERT_DEPTH/2,y,z))
        if out_dir>0:plate=plate-slot('x',10.5,ROLL_STOP_PIN['d']/2,180+m.ROLL_STOP[0],180+m.ROLL_STOP[1],(xc,m.ROLL_Y,m.ROLL_Z),2)
        name=f'{abs(face+out_dir*-.5):g}'
        add(f'roll_bearing_retainer_{name}',plate,'P','M010-P','#c38a47')
        for (y,z),deg in zip(hole_yz,RETAINER_SCREW_DEG):
            add(f'bearing_retainer_M2x4_{name}_{deg}',m.button_screw(face-out_dir*.1,y,z,'x',out_dir,4),'P','M021-P','#555b5a')
    # Four vertical ISO 4762 M2 x 25 cartridge fixing screws into the
    # pitch-frame slab. 2 mm side-open spot faces drop the heads flush with
    # the cartridge top, so 3 mm of shank sits in the slab insert. The slab
    # widens to +/-13 at each pair so the insert keeps 1.4 mm of side wall.
    frame=out['connected_pitch_frame_roll_servo_saddle']['shape']
    for x in CARTRIDGE_SCREW_X:
        frame=frame+b(x-3,x+3,m.ROLL_Y-13,m.ROLL_Y+13,m.ROLL_Z-16,m.ROLL_Z-12)
        for dy in [-10,10]:
            y=m.ROLL_Y+dy
            cartridge=cartridge-a(1.15,26,(x,y,m.ROLL_Z),'z')
            cartridge=cartridge-b(x-2.3,x+2.3,*sorted((y-math.copysign(2.3,dy),m.ROLL_Y+math.copysign(12.1,dy))),m.ROLL_Z+10,m.ROLL_Z+12.1)
            frame=frame-a(INSERT_R,4,(x,y,m.ROLL_Z-14),'z')
            add(f'cartridge_M2x25_{abs(x):g}_{dy:g}',m.socket_screw(x,y,m.ROLL_Z+10,'z',1,25),'P','M021-P','#555b5a')
    setshape('connected_pitch_frame_roll_servo_saddle',frame)
    setshape('bearing_cartridge_trial',cartridge)
    # Roll pin: Ø2 x 5 dowel pressed through the whole 3 mm flange, its tip in
    # a sector slot in the cartridge front wall at radius 10.5; neutral +Z.
    R=10.5;pr=ROLL_STOP_PIN['d']/2
    pin=a(pr,ROLL_STOP_PIN['l'],(-40.8+ROLL_STOP_PIN['l']/2,m.ROLL_Y,m.ROLL_Z+R))
    add('roll_hard_stop_pin',pin,owner='M016-18-R',color='#cc5750')
    setshape('connected_rolling_cradle_flange_ear_stalks',out['connected_rolling_cradle_flange_ear_stalks']['shape']-pin)
    # Swept pockets in the flange's back face for the two front retainer screw
    # heads (radius 10.5 on the lower diagonals).
    # This removes the Layout 03 audit's 5.53 mm3 screw/flange overlaps.
    sweep=m.ROLL_STOP[1]+1
    head_r=1.75+FLANGE_POCKET_CLEAR
    x0=-39.6;length=FLANGE_POCKET_BACK_X-x0
    cradle=out['connected_rolling_cradle_flange_ear_stalks']['shape']
    # slot() local angle = YZ angle from +Y plus 90 deg.
    for centre in [deg+90 for deg in RETAINER_SCREW_DEG]:
        cradle=cradle-slot('x',RETAINER_SCREW_R,head_r,centre-sweep,centre+sweep,(x0+length/2,m.ROLL_Y,m.ROLL_Z),length)
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
    cut=slot('y',10,1,*pitch_slot,(m.PITCH_X,-53,m.PITCH_Z),4)
    setshape('yaw_yoke_leg_-55',(leg+ring)-cut)
    # The shell reliefs use the pre-D-049 leg with the same ring and slot.
    tool=out['yaw_yoke_leg_-55']['relief_tool']
    out['yaw_yoke_leg_-55']['relief_tool']=(tool+ring)-cut
    # Ø2 x 8 dowel: 2 mm in the yoke slot ring, 5 mm pressed into the root lug.
    add('pitch_hard_stop_pin',a(PITCH_STOP_PIN['d']/2,PITCH_STOP_PIN['l'],(m.PITCH_X-10,-54+PITCH_STOP_PIN['l']/2,m.PITCH_Z),'y'),'P','M016-18-P','#cc5750')
    # Pin root lug joins the pitch frame side arm. It extends 3 mm past the
    # pin centre on X and Z, leaving a 2 mm ligament round the Ø2 bore (the
    # old lug ended tangent to the bore: zero wall, non-manifold STL).
    frame=out['connected_pitch_frame_roll_servo_saddle']['shape']
    lug=b(m.PITCH_X-13,m.PITCH_X-4,-51,-46,m.PITCH_Z-3,m.PITCH_Z+3)
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
    # Receivers at Y +/-16 with R2.8 bosses leave 1.2 mm round the Ø3.2
    # insert and 0.7 mm to the camera PCB edge; bracket bosses are R2.4.
    for y in [-CAMERA_SCREW_Y,CAMERA_SCREW_Y]:
        z=78.5
        boss=a(2.8,12.8,(-8.2,y,z))-a(INSERT_R,3.2,(-13.2,y,z))-a(TIP_RELIEF_R,1,(-11.1,y,z))
        face=face+boss
        bracket=bracket+a(2.4,2.2,(-15.9,y,z))
        bracket=bracket-a(1.15,4,(-15.9,y,z))
        add(f'camera_bracket_M2_{y}',m.button_screw(-17,y,z,'x',-1),'R','M021-R','#555b5a')
    setshape('front_bezel_integral_camera_crown',face)
    setshape('removable_camera_edge_bracket_trial',bracket)
    # CSI guide saddle contacts the existing inner roof. The passage gives the
    # trial OD2 jacket 0.4 mm diametral clearance and is open in both directions.
    guide=b(-49,-45,-4,4,78.6,m.MAIN_H-m.SKIN)-a(1.2,6,(-47,0,80))
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
# D-049: the pitch servo's collar replaces the +Y side web and trunnion arm.
WEB_SIDES=(-1,)
C2_NOTCH_Y=(-37.,-21.)      # C2 BOOT/RESET rear tool corridor is Y -36..-22, Z >= 33
C2_NOTCH_TOP_Z=32.7          # absolute, as the reserve is
# Balance trim (RP-01 P08): removable mass at four seats. Ear caps carry
# tungsten Ø12 slugs (roll, lever ~71 mm). The rear cover carries two brass
# Ø14 washer stacks at Y = roll axis +/-30, 22 mm above it (pitch, lever
# ~70 mm); built equal, the pair has no roll moment. D-049 moved them off the
# axis, where the roll servo now sits 1 mm from the cover, and above the C2
# BOOT/RESET tool corridor (Y -36..-22, Z 33..49).
EAR_SLUG=dict(r=6.,max_len=2.5,density=19.3e-3)
EAR_TRIM_INNER_FACE=69.3
REAR_STACK=dict(r=7.,max_len=3.,density=8.5e-3,dy=(-30.,30.),dz=22.)
TRIM_NOMINAL_FRACTION=.5

def trim_capacity():
    ear=math.pi*EAR_SLUG['r']**2*EAR_SLUG['max_len']*EAR_SLUG['density']
    rear=len(REAR_STACK['dy'])*math.pi*REAR_STACK['r']**2*REAR_STACK['max_len']*REAR_STACK['density']
    return dict(ear_slug_max_g=ear,rear_stack_max_g=rear)

def stiffen_and_trim(out,add,setshape):
    b,a=m.block,m.axial
    rz,ry=m.ROLL_Z,m.ROLL_Y
    n='connected_pitch_frame_roll_servo_saddle';frame=out[n]['shape']
    z0,z1=rz+BOX_DZ[0],rz+BOX_DZ[1]
    box=b(BOX_X[0],BOX_X[1],-BOX_HALF_Y,BOX_HALF_Y,z0,z1)
    webs=[b(BOX_X[0],m.PITCH_X+4,s*(BOX_HALF_Y-WEB_T/2)-WEB_T/2,s*(BOX_HALF_Y-WEB_T/2)+WEB_T/2,z0,m.PITCH_Z-6) for s in WEB_SIDES]
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
    frame=roll_servo_mount(frame,add,z1)
    frame=pitch_servo_collar(frame,add,z0,z1)
    setshape(n,frame)
    # Ear-cap trim seats: long inward bosses leave a full ligament behind
    # each M2 insert. The 2.5 mm maximum trim stack clears the pitch yoke at
    # both roll stops; a 4 mm stack collides at the negative/positive stop.
    # The stack has an actual screw hole and
    # retaining M2x6, so service and motion checks include the hardware.
    for sign in (-1,1):
        cn=f'ear_{sign}_hollow_removable_cap';cap=out[cn]['shape']
        c=(m.EAR_X,sign*71.4,m.EAR_Z)
        cap=cap+a(3.5,4.2,c,'y')
        cap=cap-a(INSERT_R,3,(m.EAR_X,sign*70.8,m.EAR_Z),'y')
        setshape(cn,cap)
        slug_c=sign*(EAR_TRIM_INNER_FACE-EAR_SLUG['max_len']/2)
        slug=a(EAR_SLUG['r'],EAR_SLUG['max_len'],(m.EAR_X,slug_c,m.EAR_Z),'y')
        slug=slug-a(1.15,EAR_SLUG['max_len']+.2,(m.EAR_X,slug_c,m.EAR_Z),'y')
        add(f'ear_{sign}_trim_slug_stack_max',slug,'R','M022-R','#8d8f93')
        # M2 x 5: 2.5 mm through the stack, 2.5 mm in the insert. The stack is
        # always built to 2.5 mm (tungsten plus spacer discs) so it cannot bottom.
        add(f'ear_{sign}_trim_M2x5',m.button_screw(m.EAR_X,sign*(EAR_TRIM_INNER_FACE-EAR_SLUG['max_len']),m.EAR_Z,'y',-sign,5),'R','M021-R','#555b5a')
    # Rear-cover seats: M3 insert bosses, brass washer stacks (screw not drawn).
    cn='removable_octagonal_rear_cover';cover=out[cn]['shape']
    for dy in REAR_STACK['dy']:
        z=rz+REAR_STACK['dz']
        cover=cover+a(4.5,2.5,(-112.15,ry+dy,z))
        cover=cover-a(2.,3.5,(-112.65,ry+dy,z))
        stack=a(REAR_STACK['r'],REAR_STACK['max_len'],(-110.9+REAR_STACK['max_len']/2,ry+dy,z))
        add(f'rear_pitch_trim_washer_stack_max_{dy:+g}',stack,'R','M022-R','#b88636')
    setshape(cn,cover)


def _insert_pocket(a,face,inward,centre,axis):
    """M2 heat-set pocket from a face (0.4 mm open above it) plus tip relief."""
    depth=INSERT_POCKET+INSERT_BREAKTHROUGH
    mid=face+inward*(depth/2-INSERT_BREAKTHROUGH)
    tip=face+inward*(INSERT_POCKET+1)
    def at(c):
        p=list(centre);p['xyz'.index(axis)]=c;return tuple(p)
    return a(INSERT_R,depth,at(mid),axis)+a(TIP_RELIEF_R,2,at(tip),axis)


def _ear_joint(add,name,seat,centre,axis,outward):
    """ISO 7380 M2 x 6 on an ISO 7089 washer over an open Ø4.2 servo slot."""
    t=fe.WASHER['t'];k='xyz'.index(axis)
    wc=list(centre);wc[k]=seat-outward*t/2
    sc=list(centre);sc[k]=seat
    add(f'{name}_washer',m.washer(*wc,axis),'P','M021-P','#8d8f93')
    add(f'{name}_M2x6',m.button_screw(*sc,axis,outward,6),'P','M021-P','#555b5a')


def roll_servo_mount(frame,add,box_top):
    """D-049 roll servo plate: a 5 mm YZ plate on the ears' front faces with a
    window round the case, its lower half joined to the torsion box rear wall.
    Wide side bars keep the roll reaction in plane (13.8 N per ear end at the
    0.59 N*m stall). Ear screws drive from behind with the rear cover off."""
    b,a=m.block,m.axial
    ry,rz=m.ROLL_Y,m.ROLL_Z
    face=fe.ROLL_EAR_X[1];front=face+fe.ROLL_PLATE_T
    hw,c=fe.ROLL_PLATE_HALF_Y,fe.ROLL_WINDOW_CLEAR
    zlo,zhi=fe.ROLL_PLATE_Z
    win_z=(rz-fe.CASE_X[1]-c,rz-fe.CASE_X[0]+c)
    case_top=fe.ROLL_CASE_BOTTOM_X+fe.CASE_H
    plate=b(face,front,ry-hw,ry+hw,zlo,zhi)-b(face-1,front+1,ry-fe.CASE_HALF_W-c,ry+fe.CASE_HALF_W+c,*win_z)
    k=fe.ROLL_PLATE_C2_RELIEF
    plate=plate-b(face-1,front+1,ry-hw-1,k['y_max'],k['z_min'],zhi+1)
    bridge=b(front-.1,BOX_X[0]+.5,ry-hw,ry+hw,zlo,box_top)
    bridge=bridge-b(front-1,case_top+c,ry-fe.CASE_HALF_W-c,ry+fe.CASE_HALF_W+c,win_z[0],box_top+1)
    frame=frame+plate+bridge
    for i,(x,y,z) in enumerate(fe.slots(fe.roll_local_to_head,fe.EAR_Z[1])):
        frame=frame-_insert_pocket(a,face,1,(x,y,z),'x')
        _ear_joint(add,f'roll_servo_ear_{i+1}',fe.ROLL_EAR_X[0]-fe.WASHER['t'],(x,y,z),'x',-1)
    return frame


def pitch_servo_collar(frame,add,box_bottom,box_top):
    """D-049 pitch servo collar: a 6 mm XZ plate under the ears, round the
    case on its rear-up side, with a web into the torsion box front wall. The
    servo reaction stays in the plate's plane. Ear screws drive from +Y before
    the frame goes into the yoke."""
    a=m.axial
    y1=fe.PITCH_EAR_Y[0];y0=y1-fe.COLLAR_T
    L=fe.pitch_local_to_head
    def slab(pts):
        # Extrusion follows the polygon's winding; place by the result's span.
        s=extrude(Plane.XZ*Polygon(*pts,align=None),amount=y1-y0)
        return s.moved(Location((0,y1-s.bounding_box().max.Y,0)))
    def prism(local_pts):
        return slab([(L(x,y,0)[0],L(x,y,0)[2]) for x,y in local_pts])
    c=fe.COLLAR_WINDOW_CLEAR;b0,b1=fe.COLLAR_BAND
    ex0,ex1=fe.EAR_X
    collar=prism([(ex0,-fe.CASE_HALF_W),(ex1,-fe.CASE_HALF_W),(ex1,b1),(ex0,b1)])
    collar=collar-prism([(fe.CASE_X[0]-c,-fe.CASE_HALF_W-1),(fe.CASE_X[1]+c,-fe.CASE_HALF_W-1),(fe.CASE_X[1]+c,b0),(fe.CASE_X[0]-c,b0)])
    # Web to the box front wall: the band's outer edge meets the box top.
    (ux,uz),(vx,vz)=fe.u_v()
    t=(box_top-m.PITCH_Z-b1*vz)/uz
    top=L(t,b1,0);corner=L(ex1,b1,0)
    web=slab([(BOX_X[1]-.5,box_bottom),(BOX_X[1]-.5,box_top),(top[0],box_top),(corner[0],corner[2])])
    # Floor under the servo from the keel to the collar: the pitch couple on
    # the cartridge seat reaches the ear seats without going round the box.
    # It stops at X-51, clear of the case's lower edge.
    fx0,fx1,fz0,fz1=fe.COLLAR_FLOOR
    floor=m.block(fx0,fx1,m.ROLL_Y+KEEL_HALF_Y-2,y0+.5,fz0,fz1)
    frame=frame+collar+web+floor
    for i,(x,y,z) in enumerate(fe.slots(L,0)):
        frame=frame-_insert_pocket(a,y1,-1,(x,0,z),'y')
        _ear_joint(add,f'pitch_servo_ear_{i+1}',fe.PITCH_EAR_Y[1]+fe.WASHER['t'],(x,0,z),'y',1)
    return frame
