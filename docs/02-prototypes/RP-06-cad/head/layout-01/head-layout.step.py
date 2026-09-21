"""RP-01 Layout 01: component envelopes and support reservations, not print parts.
Origin front-bottom centre; +X forward, +Y left, +Z up; mm.
Static placements deliberately use explicit documented datums for this study.
"""
from pathlib import Path
from build123d import Box, Cylinder, Compound, Location, Plane, Polygon, extrude, Axis
from cadgen import srgb
from cadgen.step_scene import import_step
from layout_data import ROLL_Y, ROLL_Z, PITCH_X, PITCH_Z

HERE=Path(__file__).parent
MAIN_W, MAIN_H, MAIN_D, SKIN = 130.,95.,115.,1.2
EAR_D, EAR_T =45.,10.
CAMERA_BOARD_BOTTOM, CAMERA_PLANE_X =81.,-10.805
ROLL_BEARING_CENTRES=(-43.,-65.)

def block(x0,x1,y0,y1,z0,z1):
    return Box(x1-x0,y1-y0,z1-z0).moved(Location(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)))

def axial(radius,length,center,axis='x'):
    s=Cylinder(radius,length)
    if axis=='x': s=s.rotate(Axis.Y,90)
    elif axis=='y':s=s.rotate(Axis.X,90)
    return s.moved(Location(center))

def tint(s,name,color,alpha=1):
    s.label=name
    if s.children:
        for c in s.children: tint(c,c.label or 'catalog_part',color,alpha)
    else: s.color=srgb(color,alpha)
    return s

def build_parts(catalog=True):
    out={}
    def add(n,s,frame,color,alpha=1): out[n]=(tint(s,n,color,alpha),frame)
    # Window opening shows the active screen. Mounts and tolerances remain open.
    front=block(-3,0,-65,65,0,95)-block(-4,1,-49.5,49.5,14,72)-axial(9,6,(-1,0,95.4))
    add('front_bezel',front,'R','#9b7354')
    sleeve=block(-113.8,-3,-65,65,0,95)-block(-115,-2,-63.8,63.8,1.2,93.8)
    sleeve=sleeve-block(-25,-2,-28,28,93,97)
    # Initial hidden underside entry slots; full compound sweep is still a gate.
    sleeve=sleeve-[block(-72,-12,40,67,-1,26),block(-72,-12,-67,-40,-1,26)]
    add('main_skin_with_trial_neck_reliefs',sleeve,'R','#b29973',.24)
    add('removable_rear_cover',block(-115,-113.8,-65,65,0,95),'R','#9b7354',.25)
    outer=extrude(Plane.YZ*Polygon((-29,94),(29,94),(19,109),(-19,109),align=None),amount=24).moved(Location((-24,0,0)))
    inner=extrude(Plane.YZ*Polygon((-27,92),(27,92),(17.5,107.8),(-17.5,107.8),align=None),amount=23).moved(Location((-24.5,0,0)))
    crown=outer-inner-axial(9,5,(-1,0,95.4))
    add('camera_crown_trial',crown,'R','#9b7354',.65)
    add('window_mask_reserve',block(-2.8,-1.3,-55,55,10,76),'R','#243442',.35)
    add('display_board_glass_envelope',block(-14.4,-3.8,-53.05,53.05,9,77),'R','#327b85')
    add('display_active_area',block(-3.75,-3.55,-47.52,47.52,16.07,69.93),'R','#182830')
    add('display_rear_connector_reserve',block(-18,-14.4,-53.05,53.05,9,77),'R','#72b5bf',.25)
    if catalog:
        cam=import_step(str(HERE/'parts/camera-module-3-wide.step')).rotate(Axis.Y,-90).moved(Location((CAMERA_PLANE_X,-12.5,CAMERA_BOARD_BOTTOM)))
        add('camera_module_3_wide_catalog',cam,'R','#458b65')
    else:
        add('camera_module_envelope',block(-14.4,-2,-12.5,12.5,81,105),'R','#458b65')
    add('camera_CSI_exit_reserve',block(-24,-14.5,-11,11,79,91),'R','#77b87f',.35)
    add('status_light_reserve',axial(2.5,5,(-5,20,94)),'R','#dfa744')
    add('C2_board_mount_reserve',block(-35,-20,-47.5,-12.5,37.5,62.5),'R','#ab7bc2')
    add('C2_plug_withdrawal_reserve',block(-48,-35,-47.5,-12.5,37.5,62.5),'R','#ab7bc2',.2)
    # Representative cradle ribs stay away from the C2 pocket.
    for y in [-52,52]: add('cradle_rib_'+str(y),block(-38,-19,y-1.5,y+1.5,20,70),'R','#6e8d99')
    add('rolling_flange',axial(15,4,(-38,ROLL_Y,ROLL_Z)),'R','#6e8d99')
    add('rolling_spindle',axial(3,32,(-56,ROLL_Y,ROLL_Z)),'R','#bbc2c7')
    for i,x in enumerate(ROLL_BEARING_CENTRES):
        ring=axial(8,6,(x,ROLL_Y,ROLL_Z))-axial(3.1,8,(x,ROLL_Y,ROLL_Z))
        add('bearing_reserve_'+str(i+1),ring,'P','#bbc2c7')
    cartridge=block(-69,-39,ROLL_Y-12,ROLL_Y+12,ROLL_Z-12,ROLL_Z+12)-axial(8.3,32,(-54,ROLL_Y,ROLL_Z))
    add('bearing_cartridge_reserve',cartridge,'P','#cc8546',.55)
    add('coaxial_coupling_reserve',axial(6,8.5,(-73.25,ROLL_Y,ROLL_Z)),'R','#bbc2c7')
    if catalog:
        servo=import_step(str(HERE/'parts/xc330.stp'))
        roll=servo.rotate(Axis.X,90).rotate(Axis.Z,90).moved(Location((-84,ROLL_Y,ROLL_Z)))
        pitch=servo.rotate(Axis.X,-90).rotate(Axis.Y,270).moved(Location((PITCH_X,47,PITCH_Z)))
        add('roll_XC330_catalog',roll,'P','#c48b3e')
        add('pitch_XC330_catalog',pitch,'Y','#c48b3e')
    else:
        add('roll_servo_envelope',block(-106.5,-77.5,ROLL_Y-10,ROLL_Y+10,ROLL_Z-24.5,ROLL_Z+9.5),'P','#c48b3e')
        add('pitch_servo_envelope',block(PITCH_X-24.5,PITCH_X+9.5,24.5,53.5,PITCH_Z-10,PITCH_Z+10),'Y','#c48b3e')
    # Indicative pitch frame supports the cartridge and roll actuator.
    for y in [-49,49]:
        add('pitch_frame_arm_'+str(y),block(-74,PITCH_X+4,y-2,y+2,ROLL_Z-20,ROLL_Z-16),'P','#cc8546')
        add('pitch_frame_upright_'+str(y),block(PITCH_X-4,PITCH_X+4,y-2,y+2,ROLL_Z-16,PITCH_Z+4),'P','#cc8546')
        add('pitch_trunnion_reserve_'+str(y),axial(4,9,(PITCH_X,y,PITCH_Z),'y'),'P','#bbc2c7')
    add('pitch_frame_crossmember',block(-74,-39,-49,49,ROLL_Z-20,ROLL_Z-16),'P','#cc8546',.45)
    add('cartridge_seat_reserve',block(-69,-39,ROLL_Y-12,ROLL_Y+12,ROLL_Z-16,ROLL_Z-12),'P','#cc8546')
    for y in [-55,55]:
        # Rearward knee clears the lower display as the head pitches up.
        leg=extrude(Plane.XZ*Polygon((-74,-32),(-64,-32),(PITCH_X+4,PITCH_Z-8),(PITCH_X+4,PITCH_Z+6),(PITCH_X-6,PITCH_Z+6),(PITCH_X-6,PITCH_Z-6),align=None),amount=6).moved(Location((0,y+3,0)))
        add('yaw_yoke_leg_'+str(y),leg,'Y','#617286')
        # Ears are solid keepout envelopes; detail hollow cosmetic caps later.
    add('yaw_yoke_bridge',block(-74,-64,-58,58,-36,-32),'Y','#617286')
    add('yaw_spindle_bridge_reserve',block(-74,PITCH_X+4,-7,7,-36,-32),'Y','#617286')
    add('yaw_spindle_reserve',axial(4,24,(PITCH_X,0,-48),'z'),'Y','#bbc2c7')
    for sign in [-1,1]:
        ear=axial(EAR_D/2,EAR_T,(-43,sign*70,48),'y')-axial(EAR_D/2-1.2,10,(-43,sign*68.8,48),'y')
        add('rolling_ear_'+str(sign),ear,'R','#9b7354')
    # Bounds of sampled support intersections, expanded 1.5 mm, define reliefs.
    # This is a proposed opening, not a continuous-motion/tolerance certificate.
    ra=Axis((0,ROLL_Y,ROLL_Z),(1,0,0))
    pa=Axis((PITCH_X,0,PITCH_Z),(0,1,0))
    tool_groups=[]
    for y in [-55,55]:
        support=out['yaw_yoke_leg_'+str(y)][0]
        tools=[]
        for r in [-18,-9,0,9,18]:
            for p in [-22,0,20,40]:
                tools.append(support.rotate(pa,-p).rotate(ra,-r))
        tool_groups.append(tools)
    for n in ['main_skin_with_trial_neck_reliefs','rolling_ear_-1','rolling_ear_1']:
        s,f=out[n]
        cutters=[]
        # Bound actual sweep intersections per side into simple service reliefs.
        # This avoids fragile overlapping boolean cutters and leaves flat edges.
        for tools in tool_groups:
            bounds=[]
            for tool in tools:
                c=s.intersect(tool)
                for piece in ([c] if hasattr(c,'volume') else c or []):
                    if piece.volume>1e-5: bounds.append(piece.bounding_box())
            if bounds:
                lo=[min(tuple(b.min)[i] for b in bounds)-1.5 for i in range(3)]
                hi=[max(tuple(b.max)[i] for b in bounds)+1.5 for i in range(3)]
                cutters.append(block(lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]))
        cut=s.cut(*cutters) if cutters else s
        add(n,cut,f,'#b29973' if n.startswith('main') else '#9b7354',.24 if n.startswith('main') else 1)
    return out

def gen_step():
    p=build_parts()
    groups=[]
    for frame,label in [('R','rolling_face_and_ears'),('P','pitch_carried_mechanism'),('Y','yaw_yoke_and_pitch_actuator')]:
        groups.append(Compound(label=label,children=[s for s,f in p.values() if f==frame]))
    return Compound(label='RP01_layout_01_PROVISIONAL',children=groups)
