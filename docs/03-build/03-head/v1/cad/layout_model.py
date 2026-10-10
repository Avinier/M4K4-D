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
from motion_envelope import ROLL_STOP, PITCH_STOP
import feetech as fe

HERE=Path(__file__).parent
CATALOG=HERE/'purchased'
# SKIN is the inset in the YZ section. The rear taper leans the side facets
# about 19 deg, so 1.3 keeps the normal wall >= 1.2 mm (fabrication audit).
MAIN_W, MAIN_D, MAIN_H, CROWN_H, SKIN=130.,115.,86.,104.,1.3
# Inner 45 deg chamfer leg reduction that gives the same normal wall as SKIN.
SKIN_CHAMFER_RELIEF=SKIN*(2-math.sqrt(2))
EAR_R, EAR_X, EAR_Z=30.,-43.,42.
EAR_PAD_TOP=69.2
DISPLAY_BOTTOM, CAMERA_BOTTOM=6.,77.
LED_Y, LED_Z=15.2,91.8
# Side screws at |Y| 56.4 keep >= 1.2 mm from their counterbores to the
# bezel side and from their bores to the 106 mm window seat.
FRONT_SCREWS=[(-56.4,16),(56.4,16),(-56.4,64),(56.4,64),(-32,78),(32,78)]
REAR_SCREWS=[(-44,26),(44,26),(-44,65),(44,65)]
ROLL_Y,ROLL_Z,PITCH_X,PITCH_Z=[AXES[k] for k in ('roll_y','roll_z','pitch_x','pitch_z')]
ROLL_AXIS=Axis((0,ROLL_Y,ROLL_Z),(1,0,0))
PITCH_AXIS=Axis((PITCH_X,0,PITCH_Z),(0,1,0))
# Layout 04 yaw stage: a turntable disc replaces the 24 mm spindle stack.
# Hard stops sit 3 deg beyond usable travel (roll +/-21, pitch -25/+43); the
# full stop grid sweeps to about Z-30.3, so the disc top at Z-34.5 keeps >=4 mm
# with no firmware roll/pitch limit. The disc stands YAW_DISC_PROUD above the
# body top: the RP-06 stack (plate, bearing, 1:1 spur pair) starts 10.5 mm
# above the Pi 5 cooler. Its rim skirts down to a 1 mm running gap.
YAW_DISC_TOP_Z=-34.5
SWEEP_FLOOR_Z=YAW_DISC_TOP_Z+4.
YAW_DISC_PROUD=15.
BODY_TOP_Z=YAW_DISC_TOP_Z-YAW_DISC_PROUD
NECK=-BODY_TOP_Z
YAW_DISC_THICKNESS=YAW_DISC_PROUD-1.
YAW_DISC_PLATE=4.
YAW_DISC_R=62.5
YAW_DISC_RIM_FOOT_R=58.5   # D-050 tapered rim
YAW_DISC_TOP_CHAMFER=.6
YAW_BORE_R=7.
# Body v1 BO-045 has three M3 inserts at R22, clocked away from its pinion.
# Counterbores keep the button heads below the disc top and preserve the
# measured 4 mm moving-head clearance above the disc.
YAW_HUB_BOLT_R=22.
YAW_HUB_BOLT_DEG=(210.,270.,330.)
YAW_HUB_BOLT_CLEARANCE_R=1.7
YAW_HUB_BOLT_HEAD_R=3.0
YAW_HUB_BOLT_RECESS=1.8
YAW_INTERFACE_Z=BODY_TOP_Z
YAW_AXIS=Axis((PITCH_X,0,YAW_INTERFACE_Z),(0,0,1))

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

# Helmet refinement: broad ear mounting belt, inward-sloping shoulders,
# narrower stern and lifted lower rim. Hardware and front carrier stay 1:1.
HELMET_SHOULDER_START_X=-26.
HELMET_SHOULDER_FULL_X=-60.
HELMET_REAR_TAPER_START_X=-78.
HELMET_REAR_WIDTH=104.
HELMET_REAR_BOTTOM=10.
HELMET_REAR_TOP=84.

def stern_section_values(x):
    shoulder=max(0,min(1,(HELMET_SHOULDER_START_X-x)/(HELMET_SHOULDER_START_X-HELMET_SHOULDER_FULL_X)))
    rear=max(0,min(1,(HELMET_REAR_TAPER_START_X-x)/(MAIN_D+HELMET_REAR_TAPER_START_X)))
    return (MAIN_W+(HELMET_REAR_WIDTH-MAIN_W)*rear,HELMET_REAR_BOTTOM*rear,MAIN_H+(HELMET_REAR_TOP-MAIN_H)*rear,
            14+10*shoulder-14*rear,14-2*rear)

def stern(x0,x1,inside=False,wall=SKIN):
    """Planar helmet facets. Different top/bottom corner depths preserve belt."""
    def section(x):
        width,bottom,top,upper,lower=stern_section_values(x)
        w=wall if inside else 0
        a=width/2-w;bottom+=w;top-=w
        upper-=w*(2-math.sqrt(2));lower-=w*(2-math.sqrt(2))
        points=[(-a+lower,bottom),(a-lower,bottom),(a,bottom+lower),
                (a,top-upper),(a-upper,top),(-a+upper,top),
                (-a,top-upper),(-a,bottom+lower)]
        return (Plane.YZ*Polygon(*points,align=None)).moved(Location((x,0,0)))
    xs=sorted(set([x0,x1]+[x for x in [HELMET_REAR_TAPER_START_X,HELMET_SHOULDER_FULL_X,HELMET_SHOULDER_START_X] if x0<x<x1]))
    return loft([section(x) for x in xs],ruled=True)

def pieces(s):
    return ([s] if hasattr(s,'volume') else list(s)) if s else []

def tint(s,name,color,alpha=1):
    s.label=name
    if s.children:
        for c in s.children:tint(c,c.label or name,color,alpha)
    else:s.color=srgb(color,alpha)
    return s

def button_screw(x,y,z,axis='x',sign=1,shank_length=6):
    # Local +Z points outwards; origin at under-head seat. Smooth major thread.
    h=1.3;r=1.75;R=(r*r+h*h)/(2*h)
    cap=Sphere(R).moved(Location((0,0,h-R))) & Box(6,6,h).moved(Location((0,0,h/2)))
    shank=Cylinder(1,shank_length).moved(Location((0,0,-shank_length/2)))
    socket=extrude(RegularPolygon(1.3/math.sqrt(3),6),amount=1).moved(Location((0,0,.6)))
    screw=(cap+shank)-socket
    if axis=='x':screw=screw.rotate(Axis.Y,90*sign)
    elif axis=='y':screw=screw.rotate(Axis.X,-90*sign)
    return screw.moved(Location((x,y,z)))

def socket_screw(x,y,z,axis='z',sign=1,shank_length=25):
    # ISO 4762 M2: Ø3.8 x 2 head, 1.5 hex key. Origin at the under-head seat,
    # local +Z outwards, smooth major-diameter shank.
    head=Cylinder(1.9,2).moved(Location((0,0,1)))
    shank=Cylinder(1,shank_length).moved(Location((0,0,-shank_length/2)))
    socket=extrude(RegularPolygon(1.5/math.sqrt(3),6),amount=1.2).moved(Location((0,0,.8)))
    screw=(head+shank)-socket
    if axis=='x':screw=screw.rotate(Axis.Y,90*sign)
    elif axis=='y':screw=screw.rotate(Axis.X,-90*sign)
    elif sign<0:screw=screw.rotate(Axis.X,180)
    return screw.moved(Location((x,y,z)))

def m3_button_screw(x,y,z,axis='x',sign=1,shank_length=6):
    # ISO 7380 M3: Ø5.7 x 1.65 head, 2 mm key. Origin at the under-head seat,
    # local +Z outwards, smooth major-diameter shank.
    h=1.65;r=2.85;R=(r*r+h*h)/(2*h)
    cap=Sphere(R).moved(Location((0,0,h-R))) & Box(6.,6.,h).moved(Location((0,0,h/2)))
    shank=Cylinder(1.5,shank_length).moved(Location((0,0,-shank_length/2)))
    socket=extrude(RegularPolygon(2./math.sqrt(3),6),amount=1.).moved(Location((0,0,.7)))
    screw=(cap+shank)-socket
    if axis=='x':screw=screw.rotate(Axis.Y,90*sign)
    elif axis=='y':screw=screw.rotate(Axis.X,-90*sign)
    return screw.moved(Location((x,y,z)))

def m3_socket_screw(x,y,z,axis='x',sign=1,shank_length=5):
    # ISO 4762 M3: Ø5.5 x 3 head, 2.5 mm key; same origin convention.
    head=Cylinder(2.75,3).moved(Location((0,0,1.5)))
    shank=Cylinder(1.5,shank_length).moved(Location((0,0,-shank_length/2)))
    socket=extrude(RegularPolygon(2.5/math.sqrt(3),6),amount=1.5).moved(Location((0,0,1.5)))
    screw=(head+shank)-socket
    if axis=='x':screw=screw.rotate(Axis.Y,90*sign)
    elif axis=='y':screw=screw.rotate(Axis.X,-90*sign)
    return screw.moved(Location((x,y,z)))

def washer(x,y,z,axis='x'):
    # Plain washer from fe.WASHER (ISO 7089 M2.5, Ø2.7/Ø6 x 0.5), centred at (x,y,z).
    w=fe.WASHER
    return axial(w['r_out'],w['t'],(x,y,z),axis)-axial(w['r_in'],w['t']+.2,(x,y,z),axis)

def yspan(r,y0,y1,x=None,z=None):
    # Y-axis cylinder between y0 and y1 (either order), on the pitch axis by default.
    x=PITCH_X if x is None else x;z=PITCH_Z if z is None else z
    return axial(r,abs(y1-y0),(x,(y0+y1)/2,z),'y')

def d_section(r,flat,y0,y1):
    # Ø2r D profile on the pitch axis, its flat `flat` from the axis on +Z at neutral.
    return yspan(r,y0,y1)-block(PITCH_X-r-1,PITCH_X+r+1,min(y0,y1)-1,max(y0,y1)+1,PITCH_Z+flat,PITCH_Z+r+1)

def trunnion_screw_points():
    t=fe.TRUNNION
    return [(PITCH_X+t['screw_r']*math.cos(math.radians(a)),PITCH_Z+t['screw_r']*math.sin(math.radians(a))) for a in t['screw_deg']]

def trunnion_plate_outline(grow,y0,y1):
    # D-051 -Y retainer outline: centre disc plus a lug and bar to each screw.
    t=fe.TRUNNION;w=t['lug_r']+grow
    s=yspan(t['plate_r']+grow,y0,y1)
    for (x,z),deg in zip(trunnion_screw_points(),t['screw_deg']):
        bar=Box(t['screw_r'],abs(y1-y0),2*w).rotate(Axis.Y,-deg)
        s=s+yspan(w,y0,y1,x,z)+bar.moved(Location(((PITCH_X+x)/2,(y0+y1)/2,(PITCH_Z+z)/2)))
    return s

def trunnion_leg_cut():
    # D-051 cuts in the -Y leg pad: retainer recess, MR106ZZ seat, the lip's
    # hole (clear of the turning inner ring) and the two Ø3.2 M2 insert pockets.
    t=fe.TRUNNION;outer=-(fe.LEG_INNER_Y+6);fl=t['recess_floor_y']
    c=trunnion_plate_outline(t['recess_clear'],outer-1,fl)
    c=c+yspan(t['seat_r'],fl-.1,t['lip_y'][0])+yspan(t['lip_hole_r'],t['lip_y'][0]-.1,t['lip_y'][1]+1)
    for x,z in trunnion_screw_points():
        c=c+yspan(1.6,fl-.1,fl+t['insert_pocket'],x,z)
    return c

def sts3045m(catalog=True):
    # Drawing-based STS3045M envelope (D-049 step 0). Checks fuse the five
    # touching solids into one valid solid; the export keeps them labelled.
    raw=import_step(str(CATALOG/'sts3045m_reference.step'))
    solids=[s for s in raw.solids() if s.is_valid and s.volume>1e-8]
    if catalog:return Compound(label='sts3045m_reference',children=solids)
    out=solids[0]
    for s in solids[1:]:out=out+s
    return out

def gobilda_coupler():
    # goBILDA 4001-0025-0006 official STEP: clamping hub, then its M4 x 10.
    raw=import_step(str(CATALOG/'gobilda_4001-0025-0006.step'))
    hub,screw=sorted(raw.solids(),key=lambda s:-s.volume)
    return hub,screw

def clean_catalog(path):
    # Discard STEP annotation/open-shell children, preserve all closed solids.
    raw=import_step(str(path))
    solids=[]
    for i,s in enumerate(raw.solids()):
        if s.is_valid and s.volume>1e-8:
            s.label=f'{path.stem}_solid_{i+1:03}'
            solids.append(s)
    return Compound(label=path.stem,children=solids)

# Waveshare ESP32-S3-LCD-4.3 (SKU 30493 is the non-touch board; the Touch STEP,
# 106.1 x 68.3 mm, is used as the conservative outline). STEP local X/Y/Z map to
# head +Y/+Z/+X (rotate 120 deg about (1,1,1)); glass front on X -3.8 (the 0.2 mm active-area sheet sits ahead of it), outline
# centred on Z 40. Body behind the PCB stops 12.5 mm behind the glass except one
# 5 mm connector strip on the -Y edge (STEP X -52.4...-47.4, Y -12.5...19.1) that
# reaches 16.9 mm.
DISPLAY_FRONT_X, DISPLAY_CENTER_Z=-3.8,40.

def _flat(shape,label):
    # Flatten after transforms so booleans read world-placed solids.
    return Compound(label=label,children=list(shape.solids()))

def display_fit_proxy():
    slab=block(DISPLAY_FRONT_X-12.5,DISPLAY_FRONT_X,-53.05,53.05,DISPLAY_CENTER_Z-34.15,DISPLAY_CENTER_Z+34.15)
    strip=block(DISPLAY_FRONT_X-16.9,DISPLAY_FRONT_X-12.4,-52.4,-47.4,29.85,61.45)
    return slab+strip

def display_catalog():
    d=clean_catalog(CATALOG/'waveshare_esp32_s3_touch_lcd_4_3.stp').rotate(Axis((0,0,0),(1,1,1)),120)
    return _flat(d.moved(Location((DISPLAY_FRONT_X-4.8,-0.05,DISPLAY_CENTER_Z+2.35))),'display_module_1to1_envelope')

# Waveshare ESP32-S3-Zero V2 (bare PCB, no USB-C solid in the STEP): STEP X/Y/Z map
# to head -Y/+Z/-X so the components face -X; PCB front face on X -25.
def c2_catalog():
    c=clean_catalog(CATALOG/'waveshare_esp32_s3_zero_v2.step').rotate(Axis((0,0,0),(1,1,1)),120).rotate(Axis.Z,180)
    return _flat(c.moved(Location((-25.8,-20.,28.))),'C2_ESP32_S3_Zero_23_5x18_footprint')

# Imported Module 3 Wide groups after the existing Y−90 placement, mm.
# PCB X −10.775…−10.104 × Y±12.5 × Z77…100.862; lens toward +X; shield/components −X.
CAMERA_PCB_X=(-10.775,-10.104)

def camera_fit_proxy():
    """One-solid conservative groups matching the imported camera, with empty Y-edge rims.

    The old 12.4 mm box occupied the air behind the PCB and forbade an edge clamp.
    """
    z0,z1=CAMERA_BOTTOM,CAMERA_BOTTOM+23.862
    pcb=block(*CAMERA_PCB_X,-12.5,12.5,z0,z1)
    lens=block(-10.25,-2,-6,6,84,98)
    shield=block(-13.4,-10.70,-11.46,11.46,93.95,100.50)
    comps=block(-12.6,-10.70,-10,10,78,88.3)
    return pcb+lens+shield+comps

def camera_edge_clamp():
    """Rear-access U with CSI window, pad to the rear shield, and PCB Y-edge C-channels.

    Side hooks sit in the empty 1 mm board rim outside the rear shield and lens.
    Lower centre stays open for the CSI exit. Nominal 0.12–0.15 mm seating gaps.
    """
    back=block(-17,-14.8,-15,15,76,102)-block(-18,-14,-12.9,12.9,76,88.8)
    pad=block(-14.9,-13.50,-11.35,11.35,94.05,100.40)
    clamp=back+pad
    for y0,y1 in [(12.65,15.0),(-15.0,-12.65)]:
        clamp=clamp+block(-14.9,-9.80,y0,y1,88.8,102.0)
    # Lips are >= 1.3 mm prints: the rear lip runs back to the bracket body
    # beside the shield (0.29 mm off it), the front lip forward to X-8.6.
    for y0,y1 in [(11.75,15.0),(-15.0,-11.75)]:
        clamp=clamp+block(-14.9,-10.92,y0,y1,88.8,100.76)
        clamp=clamp+block(-9.95,-8.6,y0,y1,88.8,100.76)
        clamp=clamp+block(-14.9,-8.6,y0,y1,100.96,102.3)
    return clamp

# Crown roof cap: a three-faced hip behind the crown. Its base is the crown's
# rear trapezoid (Y +/-23 at the roof, +/-17 at the crown top) butted against
# the crown's rear face (X-24), with no seam gap. The top edge runs back to a
# short end edge on the roof (CROWN_CAP_END_W wide), so the top face is a
# trapezoid (about 18 deg pitch);
# each slanted edge runs to one end of that edge, so the two sides are
# triangles. The end edge lands on the roof's rear-taper crease (X-78), the
# last X where the roof is flat at Z86. The top face carries a 0.4 mm recessed
# panel, like the skin's side lands. Hollow hood, open to the crown and to the
# roof it is fused into.
CROWN_CAP_X0=-24.
CROWN_CAP_END_X=HELMET_REAR_TAPER_START_X
CROWN_CAP_END_W=6.
CROWN_CAP_WALL=1.6
CROWN_CAP_PANEL_INSET,CROWN_CAP_PANEL_DEPTH=3.,.4

def crown_roof_cap():
    from build123d import Face, Wire, Shell, Solid, Vector, offset, Kind
    x0,x1,w,zb=CROWN_CAP_X0,CROWN_CAP_END_X,CROWN_CAP_END_W/2,MAIN_H-1.
    face=lambda pts:Face(Wire.make_polygon([Vector(*p) for p in pts],close=True))
    fl,fr,tr,tl=(x0,-23,zb),(x0,23,zb),(x0,17,CROWN_H),(x0,-17,CROWN_H)
    el,er=(x1,-w,zb),(x1,w,zb)
    solid=Solid(Shell([face([fl,fr,tr,tl]),face([fl,el,er,fr]),face([fr,er,tr]),face([tr,er,el,tl]),face([tl,el,fl])]))
    front=solid.faces().sort_by(Axis.X)[-1];bottom=solid.faces().sort_by(Axis.Z)[0]
    hood=offset(solid,amount=-CROWN_CAP_WALL,openings=[front,bottom],kind=Kind.INTERSECTION)
    top=[f for f in solid.faces() if abs(f.normal_at().Y)<1e-6 and f.normal_at().Z>.3][0]
    n=top.normal_at();panel=offset(top,amount=-CROWN_CAP_PANEL_INSET,kind=Kind.INTERSECTION)
    return hood-extrude(panel.moved(Location(tuple(n))),amount=1+CROWN_CAP_PANEL_DEPTH,dir=-n)

# Front bezel walls (fabrication audit 2026-10-05): every printed wall of the
# bezel, band and crown is >= BEZEL_WALL measured along its normal. The front
# chamfer is 9.5 (was 10) so the band's lower corner clears the display board
# corner with that wall; the back profile still matches the skin at X-8.
BEZEL_WALL=1.3
BEZEL_FRONT=(120,2,84,9.5)
BEZEL_BACK=(130,0,86,14)
CROWN_OUTER=[(-23,73),(23,73),(23,85),(17,104),(-17,104),(-23,85)]
# Window lip in front of the glass: 1.3 mm. The 1.5 mm glass and its mask sit
# 0.35 mm further back than before (0.55 mm ahead of the display's active
# sheet), keeping the 0.2 mm front and 0.25 mm rear seat gaps.
WINDOW_LIP_BACK_X=-BEZEL_WALL
# Glass and mask 106 mm wide (was 110): 3.5 mm per side under the lip beyond
# the 99 mm aperture, leaving room for the side screw walls.
WINDOW_W=106.
WINDOW_GLASS=(-3.0,-1.5)
WINDOW_SEAT_BACK_X=WINDOW_GLASS[0]-.25

def bezel_band_inner(x,t=BEZEL_WALL):
    """Inner octagon of the sloped band at station x, each facet offset by t along its normal."""
    (w0,b0,h0,c0),(w1,b1,h1,c1)=BEZEL_FRONT,BEZEL_BACK
    span=-8-(-2);u=(x-(-2))/span
    a=(w0+(w1-w0)*u)/2;z0=b0+(b1-b0)*u;z1=h0+(h1-h0)*u;c=c0+(c1-c0)*u
    # Section-line drift per mm of X for the side, floor/roof and chamfer facets.
    side=(w1-w0)/2/span;floor=(b1-b0)/span;roof=(h1-h0)/span
    chamfer=((w1-w0)/2-(c1-c0)-(b1-b0))/span/math.sqrt(2)
    ds=t*math.hypot(1,side);dz0=t*math.hypot(1,floor);dz1=t*math.hypot(1,roof);dc=t*math.hypot(1,chamfer)
    ai,z0i,z1i=a-ds,z0+dz0,z1-dz1
    ci=c-ds-max(dz0,dz1)+dc*math.sqrt(2)
    return 2*ai,z0i,z1i,ci

def crown_inner(t=BEZEL_WALL):
    """Crown cavity: each outer crown edge offset inward by t; open below Z72."""
    (y0,_),(y1,z1),(y2,z2)=CROWN_OUTER[1],CROWN_OUTER[2],CROWN_OUTER[3]
    side=y1-t;roof=z2-t
    ny,nz=z2-z1,y1-y2;n=math.hypot(ny,nz);ny/=n;nz/=n
    k=ny*y1+nz*z1-t
    return [(-side,72),(side,72),(side,(k-ny*side)/nz),((k-nz*roof)/ny,roof),(-(k-nz*roof)/ny,roof),(-side,(k-ny*side)/nz)]

def build_parts(catalog=True,reliefs=True):
    out={}
    def add(n,s,f,color='#e3ddc9',kind='physical',alpha=1,owner=None):
        out[n]=dict(shape=tint(s,n,color,alpha),frame=f,kind=kind,owner=owner,color=color,alpha=alpha)
    # Planar front ring and sloping depth band; crown fuses into this one part.
    outer=prism(*BEZEL_FRONT,-2,0)+loft([profile(*BEZEL_FRONT,-2),profile(*BEZEL_BACK,-8)],ruled=True)
    crown=extrude(Plane.YZ*Polygon(*CROWN_OUTER,align=None),amount=24).moved(Location((-24,0,0)))
    outer=outer+crown
    # Inside of the depth band provides a truthful full-size display pocket.
    # The band's inner facets are offset along their own normals, so the
    # sloped sides keep BEZEL_WALL rather than a thinner YZ inset.
    inner=prism(130-2*SKIN,SKIN,MAIN_H-SKIN,14-SKIN_CHAMFER_RELIEF,-25,-8.2)+loft([profile(*bezel_band_inner(-8.2),-8.2),profile(*bezel_band_inner(-2.8),-2.8)],ruled=True)
    inner=inner+extrude(Plane.YZ*Polygon(*crown_inner(),align=None),amount=22.7-2).moved(Location((-24+BEZEL_WALL,0,0)))
    face=outer-inner-prism(99,11,69,3,-5,1)
    # Full-size board corner clearance and a separate shallow window seat.
    # The clearance corners follow the board's measured corner (max |Y|-Z
    # 46.85, |Y|+Z 126.81 in the vendor STEP) plus 0.3 mm, not a square box,
    # so the lower band chamfer keeps its wall.
    face=face-(block(-14.7,-3.5,-53.35,53.35,5.7,74.3)&prism(106.7,5.7,74.3,53.35-5.7-47.15,-14.8,-3.4))
    face=face-prism(WINDOW_W+.6,7.7,72.3,4,WINDOW_SEAT_BACK_X,WINDOW_LIP_BACK_X)
    # Wide-angle optical path remains a clearance trial, not FOV certification.
    face=face-axial(8.6,6,(-1,0,CAMERA_BOTTOM+14.4))-axial(1.8,5,(-1,LED_Y,LED_Z))
    # Recessed perimeter lands and real screw seats. Upper screws avoid camera.
    for y,z in FRONT_SCREWS:
        pad=axial(2.5,5,(-2.5,y,z))
        face=face+pad
        face=face-axial(1.15,9,(-3,y,z))-axial(2.,2,(-.7,y,z))
    # Integral visual panel lines: shallow, not through-cracks.
    for y in [-38,38]:face=face-block(-.5,.1,y-.35,y+.35,70,84)
    # Viewer material is translucent so the real 1:1 internal packaging remains
    # inspectable while the shell stays present in the assembly view.
    add('front_bezel_integral_camera_crown',face,'R',alpha=.28,owner='M019a')
    # Thin side shell and separate octagonal rear cover with real 0.8 seam.
    skin=stern(-112.6,-8.8)-stern(-114,-8,inside=True)
    skin=skin-block(-24.8,-8,-23.8,23.8,84.2,90)
    # Underside access is necessary for the fixed yoke and external cable loop.
    # Integral panel steps add the required 0.4 mm relief without extra joints.
    for sign in [-1,1]:
        # Recessed rectangular side lands stay clear of the round ear mount.
        tool=block(-103,-82,63.8,65.1,24,62) if sign==1 else block(-103,-82,-65.1,-63.8,24,62)
        recess=tool.intersect(block(-104,-81,64.6,66,23,63) if sign==1 else block(-104,-81,-66,-64.6,23,63))
        if recess:skin=skin-recess
    # Front receivers rooted in shell wall, not in the display envelope. Each
    # boss runs forward to X-5, where the bezel pad seats on it; the insert
    # sits at that face. (Ending at the skin edge, X-8.8, the lower side
    # bosses were cut to 2.9 mm by the yoke-leg motion relief.)
    for y,z in FRONT_SCREWS:
        boss=axial(3.2,10.8,(-10.4,y,z))
        # Side receivers are flatted 0.55 mm off the display board edge.
        if abs(y)>50:boss=boss-block(-16,-8,-53.6,53.6,z-4,z+4)
        # Upper bosses reach the roof; side bosses reach the sidewall.
        bridge=block(-15.8,-9, min(y,math.copysign(64.5,y))-1,max(y,math.copysign(64.5,y))+1,z-2,z+2) if abs(y)>50 else block(-15.8,-9,y-2,y+2,z,85.2)
        bridge=bridge & prism(130,0,86,14,-16,-8)
        skin=skin+boss+bridge
    # Hipped roof cap behind the crown (appearance, 2026-09-25).
    skin=skin+crown_roof_cap()
    rear=stern(-115,-113.4)
    for y,z in REAR_SCREWS:
        # cover local reinforcement + receivers attached to shell sidewall
        rear=rear+axial(3.3,2.7,(-113.65,y,z))
        rear=rear-axial(1.15,7,(-113,y,z))-axial(2.1,2.2,(-114.6,y,z))
        receiver=axial(3.2,5,(-109.8,y,z))-axial(.8,6,(-109.8,y,z))
        bridge=block(-112.3,-107.3,min(y,math.copysign(64,y))-2,max(y,math.copysign(64,y))+2,z-2,z+2) & stern(-113,-107)
        skin=skin+receiver+bridge
    add('main_octagonal_skin',skin,'R',alpha=.28,owner='M019a')
    add('removable_octagonal_rear_cover',rear,'R',alpha=.28,owner='M019a')
    # A 106-wide opaque border masks all glass outside the aperture.
    mask=prism(WINDOW_W,8,72,4,*WINDOW_GLASS)-prism(99,11,69,3,WINDOW_GLASS[0]-.5,WINDOW_GLASS[1]+.5)
    add('window_opaque_mask_106mm',mask,'R','#202728',owner='M003')
    add('window_clear_optical_area',prism(99,11,69,3,*WINDOW_GLASS),'R','#8b9a9d',alpha=.12,owner='M003')
    # Transparent glazing is represented by its perimeter, with image surface.
    add('active_display_95_04x53_86',block(-3.75,-3.55,-47.52,47.52,13.07,66.93),'R','#111f24',owner='M002')
    add('display_module_1to1_envelope',display_catalog() if catalog else display_fit_proxy(),'R','#245967',owner='M002')
    add('display_connector_and_flashing_access_reserve',block(-18,-14.4,-53.05,53.05,6,74),'R','#49adbe','reserve',.25)
    if catalog:
        camera=clean_catalog(CATALOG/'camera-module-3-wide.step').rotate(Axis.Y,-90).moved(Location((-10.805,-12.5,CAMERA_BOTTOM)))
    else:camera=camera_fit_proxy()
    add('camera_module_3_wide_1to1',camera,'R','#2d5949',owner='M005')
    add('camera_CSI_exit_and_bend_reserve',block(-24,-14.5,-11,11,75,87),'R','#61a384','reserve',.3)
    add('removable_camera_edge_bracket_trial',camera_edge_clamp(),'R','#8c9e9a',owner='M005')
    add('addressable_status_LED_package_reserve',block(-8,-5,LED_Y-2.5,LED_Y+2.5,LED_Z-2.5,LED_Z+2.5),'R','#d3922d','reserve',.7,owner='M007')
    # HEAD-CAD-12: selected WS2812B-2020-V6 on a 5 x 5 x 0.8 mm carrier (PCB-11) inside the reserve,
    # emitting +X into the diffuser; 1.36 mm air gap to the diffuser's rear face at X -5.
    add('status_LED_PCB08_carrier_5x5',block(-8,-7.2,LED_Y-2.5,LED_Y+2.5,LED_Z-2.5,LED_Z+2.5),'R','#2d8c53',owner='M007')
    add('status_LED_WS2812B_2020',block(-7.2,-6.36,LED_Y-1,LED_Y+1,LED_Z-1,LED_Z+1),'R','#f2f0e6',owner='M007')
    add('crown_status_light_diffuser',axial(1.7,2.9,(-3.55,LED_Y,LED_Z)),'R','#e4b35b',owner='M007')
    # C2 footprint is exact; installed height/USB socket are clearly reserved.
    add('C2_ESP32_S3_Zero_23_5x18_footprint',c2_catalog() if catalog else block(-26.6,-25,-38,-20,28,51.5),'R','#67559a',owner='M008')
    add('C2_installed_components_reserve',block(-34,-26.6,-37,-21,28,51.5),'R','#a58ac4','reserve',.35)
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
        stalk=block(-23.5,-16,sign*61-7,sign*61+7,EAR_Z-2,EAR_Z+2)
        # Pad top at |Y| 69.2 leaves room for a 1.2 mm seat under the hidden
        # ear-mount screw heads (the web floor there was 0.4 mm).
        pad=block(-23.5,-18,*sorted((sign*65,sign*EAR_PAD_TOP)),EAR_Z-7,EAR_Z+7)
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
    skin_style=out['main_octagonal_skin']
    skin_style['shape']=tint(skin,'main_octagonal_skin',skin_style['color'],skin_style['alpha'])
    # D-049: Ø6 spindle runs back into the roll coupler's bore, 0.5 mm short
    # of the coupler's M3 centre-screw head.
    sx0,sx1=fe.SPINDLE_X
    add('rolling_spindle_6mm',axial(3,sx1-sx0,((sx0+sx1)/2,ROLL_Y,ROLL_Z)),'R','#b7bfc0',owner='M016-18-R')
    # 696-2Z (ISO 619/6-2Z) d6 x D15 x B5; details.py owns the seats. The
    # rear bearing sits 18.2 mm behind the front one (D-049, was 22).
    for i,x in enumerate(fe.ROLL_BEARING_X):
        add(f'roll_bearing_{i+1}_696_2Z',axial(7.5,5,(x,ROLL_Y,ROLL_Z))-axial(3.1,7,(x,ROLL_Y,ROLL_Z)),'P','#acb5b9',owner='M016-18-P')
    cx0,cx1=fe.CARTRIDGE_X
    cartridge=block(cx0,cx1,ROLL_Y-12,ROLL_Y+12,ROLL_Z-12,ROLL_Z+12)-axial(8.3,cx1-cx0+2,((cx0+cx1)/2,ROLL_Y,ROLL_Z))
    add('bearing_cartridge_trial',cartridge,'P','#c38a47',owner='M010-P')
    # Roll output: goBILDA 4001-0025-0006 clamping coupler (H25T spline to
    # Ø6 bore), clamp boss up at neutral, its M4 x 10 clamp screw, and an
    # ISO 4762 M3 x 5 through the coupler floor into the servo output.
    hub,clamp=gobilda_coupler()
    add('roll_coupler_goBILDA_4001_0025_0006',fe.place_coupler(hub),'R','#b7bfc0',owner='M013-15-R')
    add('roll_coupler_clamp_M4x10',fe.place_coupler(clamp),'R','#555b5a',owner='M021-R')
    add('roll_coupler_centre_M3x5',m3_socket_screw(fe.COUPLER_FLOOR_X,ROLL_Y,ROLL_Z,'x',1,5),'R','#555b5a',owner='M021-R')
    # STS3045M servos (HD-001). Both ride on the pitch frame.
    add('roll_STS3045M_reference',fe.place_roll(sts3045m(catalog)),'P','#a36f38',owner='M013-15-roll')
    add('pitch_STS3045M_reference',fe.place_pitch(sts3045m(catalog)),'P','#a36f38',owner='M013-15-pitch')
    # Connected pitch frame, with relieved crossbar and an actuator saddle.
    frame=block(-73,-39,-49,49,ROLL_Z-20,ROLL_Z-16)-block(-68,-44,-40,47,ROLL_Z-21,ROLL_Z-15)
    # D-049: only the -Y side keeps a trunnion arm. On +Y the pitch servo's
    # spline is the pivot and its horn is screwed to the yoke leg.
    for y in [-49]:
        frame=frame+block(-74,PITCH_X+4,y-2,y+2,ROLL_Z-20,ROLL_Z-16)
        frame=frame+block(PITCH_X-6,PITCH_X+6,y-2,y+2,ROLL_Z-16,PITCH_Z+6)
    # D-051: the arm carries an inboard boss with a D-bore; the Ø6 D-shaft pin
    # turns with the frame inside the -Y leg's MR106ZZ (was a Ø8 pin, loose in
    # Ø8.4 holes, 1.5 mm into the leg and unretained).
    t=fe.TRUNNION
    frame=frame+yspan(t['boss_r'],*t['boss_y'])
    frame=frame-d_section(t['bore_r'],t['bore_flat'],t['bore_y'][0]-1,t['bore_y'][1])
    add('pitch_trunnion_D6x12_pin',d_section(t['pin_r'],t['pin_flat'],*t['pin_y']),'P','#b7bfc0',owner='M016-18-P')
    frame=frame+block(-69,-39,ROLL_Y-12,ROLL_Y+12,ROLL_Z-16,ROLL_Z-12)
    # The ring's +Y bar and front crossbar give way to the pitch servo and its
    # collar (details.py); the rear bar stays inside the torsion box.
    frame=frame-block(-68,-37,16,50,ROLL_Z-21,ROLL_Z-15)
    add('connected_pitch_frame_roll_servo_saddle',frame,'P','#c38a47',owner='M011-P')
    # D-050: both legs share one drawn outline (feetech.py): a plinth flaring
    # onto the disc, a waist at disc+23 and an arm tangent to the Ø22.4 pad,
    # with an inboard gusset, the outer-face rail and the recessed spine inlay.
    # The +Y leg adds the horn pocket and screws, the -Y leg the trunnion bore.
    d=YAW_DISC_TOP_Z
    def xz(points):
        return [(PITCH_X+dx,PITCH_Z+dz) for dx,dz in points]
    def facet(points):
        # First two points are heights above the disc top, the last two dz.
        (a0,h0),(a1,h1),(a2,z2),(a3,z3)=points
        return [(PITCH_X+a0,d+h0),(PITCH_X+a1,d+h1),(PITCH_X+a2,PITCH_Z+z2),(PITCH_X+a3,PITCH_Z+z3)]
    r_pad=fe.LEG_PAD_R
    outline=[(PITCH_X+dx,d if dz is None else PITCH_Z+dz) for dx,dz in fe.LEG_OUTLINE_DXDZ]
    for y in [-55,55]:
        s_=1 if y>0 else -1
        # Pre-D-049 leg, kept only as the relief tool for the skin, ears and
        # cradle, so the head shell volumes do not change.
        original=extrude(Plane.XZ*Polygon(
            (PITCH_X-21.5,d),(PITCH_X-5.5,d),(PITCH_X-13.5,d+10),
            (PITCH_X-13.5,PITCH_Z-30),(PITCH_X-8.7,PITCH_Z-24),
            (PITCH_X-9.3,PITCH_Z-24),(PITCH_X-9.3,PITCH_Z-20),
            (PITCH_X-6.5,PITCH_Z-17),
            (PITCH_X+4,PITCH_Z-8),(PITCH_X+4,PITCH_Z+6),
            (PITCH_X-6,PITCH_Z+6),(PITCH_X-6,PITCH_Z-6),
            (PITCH_X-21.5,PITCH_Z-30),align=None),amount=6).moved(Location((0,y+3,0)))
        outer_face=58*s_
        # Plane.XZ extrudes toward -Y. Each cutter straddles only the outer
        # face, so the inner clearance and trunnion bearing face stay intact.
        pocket_start=outer_face+0.05 if y>0 else outer_face+1.10
        old_facet=((PITCH_X-20.1,d+9),(PITCH_X-16.0,d+13),
                   (PITCH_X-16.0,PITCH_Z-38),(PITCH_X-20.1,PITCH_Z-42))
        old_recess=extrude(Plane.XZ*Polygon(*old_facet,align=None),amount=1.15).moved(Location((0,pocket_start,0)))
        rail=extrude(Plane.XZ*Polygon(
            (PITCH_X-21.3,d+3),(PITCH_X-19.9,d+3),
            (PITCH_X-19.9,PITCH_Z-32),(PITCH_X-21.3,PITCH_Z-30),
            align=None),amount=0.80).moved(Location((0,outer_face+0.75 if y>0 else outer_face+0.05,0)))
        relief_tool=original-old_recess+rail-axial(4.2,8,(PITCH_X,y,PITCH_Z),'y')
        # D-049: both rails stop lower and both legs get the ear trim-stack
        # band (feetech.py).
        rail=rail-block(PITCH_X-25,PITCH_X-15,*sorted((outer_face-s_,outer_face+2*s_)),d+fe.LEG_RAIL_TOP_ABOVE_DISC,PITCH_Z)
        yi,yo=fe.LEG_INNER_Y*s_,(fe.LEG_INNER_Y+6)*s_
        leg=extrude(Plane.XZ*Polygon(*outline,align=None),amount=6).moved(Location((0,y+3,0)))
        leg=leg+axial(r_pad,6,(PITCH_X,(yi+yo)/2,PITCH_Z),'y')
        pl=fe.LEG_PLINTH
        x0,x1,py0,py1=pl['top']
        base=(Plane.XY*Polygon(*[(PITCH_X+px,s_*py) for px,py in pl['base']],align=None)).moved(Location((0,0,d)))
        top=(Plane.XY*Polygon((PITCH_X+x0,s_*py0),(PITCH_X+x1,s_*py0),(PITCH_X+x1,s_*py1),(PITCH_X+x0,s_*py1),align=None)).moved(Location((0,0,d+pl['h'])))
        leg=leg+loft([base,top],ruled=True)
        g=fe.LEG_GUSSET
        gusset=extrude(Plane.XZ*Polygon(*xz(g['dxdz']),align=None),amount=g['y'][1]-g['y'][0])
        leg=leg+gusset.moved(Location((0,g['y'][1] if y>0 else -g['y'][0],0)))
        recess=extrude(Plane.XZ*Polygon(*facet(fe.LEG_SPINE_FACET['recess']),align=None),amount=1.15).moved(Location((0,pocket_start,0)))
        leg=leg-recess+rail
        t=fe.LEG_TRIM_RELIEF
        band=extrude(Plane.XZ*Polygon(*[(PITCH_X+dx,PITCH_Z+dz) for dx,dz in t['band']],align=None),amount=t['y'][1]-t['y'][0])
        bb=band.bounding_box()
        band=band.moved(Location((0,(t['y'][1]-bb.max.Y) if y>0 else (-t['y'][1]-bb.min.Y),0)))
        k=fe.LEG_SKIN_STEP
        leg=leg-band-block(PITCH_X+k['dx'][0],PITCH_X+k['dx'][1],*sorted(s_*v for v in k['y']),PITCH_Z+k['dz'][0],PITCH_Z+k['dz'][1])
        # D-051 foot: socket over the disc key, M2 clearance holes through the
        # plinth's inner wall and flat spot faces for the button heads.
        f=fe.LEG_KEY;c=f['clear']
        leg=leg-block(PITCH_X+f['dx'][0]-c,PITCH_X+f['dx'][1]+c,*sorted((s_*(f['y'][0]-c),s_*(f['y'][1]+c))),d-1,d+f['h']+f['top_clear'])
        for dx in f['screw_dx']:
            sx,sz=PITCH_X+dx,d+f['screw_h']
            leg=leg-yspan(1.15,s_*(f['seat_y']-1),s_*(f['y'][0]+.5),sx,sz)-yspan(f['spot_face_r'],s_*(f['seat_y']-3),s_*f['seat_y'],sx,sz)
        if y<0:leg=leg-trunnion_leg_cut()
        else:
            # D-049: +Y leg carries the pitch horn: a 0.6 mm horn pocket for
            # radial location, four M3 clearance holes with button counterbores
            # on the outer face and a centre-screw access hole.
            leg=leg-axial(fe.LEG_HORN_POCKET_R,fe.HORN_POCKET_DEPTH+.2,(PITCH_X,yi+(fe.HORN_POCKET_DEPTH-.2)/2,PITCH_Z),'y')
            leg=leg-axial(fe.LEG_CENTRE_HOLE_R,8,(PITCH_X,(yi+yo)/2,PITCH_Z),'y')
            for deg in fe.HORN['holes_deg']:
                hx=PITCH_X+fe.HORN['pcd_r']*math.cos(math.radians(deg));hz=PITCH_Z+fe.HORN['pcd_r']*math.sin(math.radians(deg))
                leg=leg-axial(fe.M3_CLEAR_R,8,(hx,(yi+yo)/2,hz),'y')
                leg=leg-axial(fe.M3_HEAD_CBORE_R,2*fe.M3_HEAD_CBORE_D,(hx,yo,hz),'y')
        add(f'yaw_yoke_leg_{y}',leg,'Y','#536b78',owner='M011-Y')
        out[f'yaw_yoke_leg_{y}']['relief_tool']=relief_tool
        # Optional contrast insert: 0.3 mm profile clearance and a 0.05 mm
        # adhesive bed in the recess, with only 0.15 mm proud of the face.
        # It can be printed flat in a second colour or the pocket can be painted.
        accent_start=outer_face+0.15 if y>0 else outer_face+1.05
        inlay=extrude(Plane.XZ*Polygon(*facet(fe.LEG_SPINE_FACET['inlay']),align=None),amount=1.2).moved(Location((0,accent_start,0)))
        add(f'yaw_yoke_spine_inlay_{y}',inlay,'Y','#c38a47',owner='M011-Y')
    # D-051 -Y pivot, yaw-carried: MR106ZZ in the leg seat, a 1.0 mm retainer
    # on the bearing's outer ring (relieved over the inner ring and pin end)
    # and two ISO 7380 M2 x 4 whose heads finish flush with the leg face.
    t=fe.TRUNNION;fl=t['recess_floor_y'];b=t['bearing']
    add('pitch_trunnion_bearing_MR106ZZ',yspan(b['D']/2,fl,t['lip_y'][0])-yspan(t['pin_r']+.05,fl-1,t['lip_y'][0]+1),'Y','#acb5b9',owner='M016-18-Y')
    plate=trunnion_plate_outline(0,fl,fl-t['plate_t'])-yspan(t['plate_relief'][0],fl+.1,fl-t['plate_relief'][1])
    for (x,z),deg in zip(trunnion_screw_points(),t['screw_deg']):
        plate=plate-yspan(1.15,fl+.1,fl-t['plate_t']-.1,x,z)
        add(f'pitch_trunnion_retainer_M2x4_{deg:g}',button_screw(x,fl-t['plate_t'],z,'y',-1,t['screw_len']),'Y','#555b5a',owner='M021-Y')
    add('pitch_trunnion_retainer',plate,'Y','#536b78',owner='M011-Y')
    # Flush turntable disc: top plate, outer rim and bearing hub, with a
    # centre cable bore and a top groove carrying the yaw branch to the +Y leg.
    # D-050: the rim tapers from R62.5 under the plate to R58.5 at its foot, a
    # 2 mm wall, and the top edge has a 0.6 mm chamfer, so the disc reads as a
    # turntable standing on the roof rather than a slab wider than it. The
    # skin, ear and cradle reliefs keep the cylindrical disc (relief_tool).
    cyl_disc=Cylinder(YAW_DISC_R,YAW_DISC_PLATE).moved(Location((PITCH_X,0,d-YAW_DISC_PLATE/2)))
    cyl_disc=cyl_disc+(Cylinder(YAW_DISC_R,YAW_DISC_THICKNESS)-Cylinder(YAW_DISC_R-2,YAW_DISC_THICKNESS+1)).moved(Location((PITCH_X,0,d-YAW_DISC_THICKNESS/2)))
    plate=Cylinder(YAW_DISC_R,YAW_DISC_PLATE-YAW_DISC_TOP_CHAMFER).moved(Location((PITCH_X,0,d-YAW_DISC_TOP_CHAMFER-(YAW_DISC_PLATE-YAW_DISC_TOP_CHAMFER)/2)))
    plate=plate+Cone(YAW_DISC_R,YAW_DISC_R-YAW_DISC_TOP_CHAMFER,YAW_DISC_TOP_CHAMFER).moved(Location((PITCH_X,0,d-YAW_DISC_TOP_CHAMFER/2)))
    rim_h=YAW_DISC_THICKNESS-YAW_DISC_PLATE
    rim=Cone(YAW_DISC_RIM_FOOT_R,YAW_DISC_R,rim_h).moved(Location((PITCH_X,0,d-YAW_DISC_PLATE-rim_h/2)))
    # Inner surface parallel to the outer one, 2 mm in radius, run 0.1 mm past
    # both ends so the cut is clean.
    taper=(YAW_DISC_R-YAW_DISC_RIM_FOOT_R)/rim_h
    rim=rim-Cone(YAW_DISC_RIM_FOOT_R-2-.1*taper,YAW_DISC_R-2+.1*taper,rim_h+.2).moved(Location((PITCH_X,0,d-YAW_DISC_PLATE-rim_h/2)))
    def hub_and_cuts(disc):
        disc=disc+(Cylinder(YAW_BORE_R+5,YAW_DISC_THICKNESS)-Cylinder(YAW_BORE_R,YAW_DISC_THICKNESS+1)).moved(Location((PITCH_X,0,d-YAW_DISC_THICKNESS/2)))
        # Only the rim and hub reach below the top plate: the RP-06 stationary
        # pinion runs under the plate between them.
        disc=disc-axial(YAW_BORE_R,YAW_DISC_THICKNESS+2,(PITCH_X,0,d-YAW_DISC_THICKNESS/2),'z')
        disc=disc-block(PITCH_X-1.8,PITCH_X+1.8,0,46,d-3.4,d+1)
        for deg in YAW_HUB_BOLT_DEG:
            theta=math.radians(deg)
            bx=PITCH_X+YAW_HUB_BOLT_R*math.cos(theta)
            by=YAW_HUB_BOLT_R*math.sin(theta)
            disc=disc-axial(YAW_HUB_BOLT_CLEARANCE_R,YAW_DISC_PLATE+1,(bx,by,d-YAW_DISC_PLATE/2),'z')
            disc=disc-axial(YAW_HUB_BOLT_HEAD_R,YAW_HUB_BOLT_RECESS,(bx,by,d-YAW_HUB_BOLT_RECESS/2),'z')
        return disc
    disc=hub_and_cuts(plate+rim)
    cyl_disc=hub_and_cuts(cyl_disc)
    # D-051 leg keys on the disc top, one under each plinth, each with two
    # Ø3.2 M2 insert pockets entered from the inboard face; the screws come in
    # through the plinth's inner wall. Hidden inside the plinth sockets, so the
    # reliefs keep the plain disc.
    f=fe.LEG_KEY
    for s_ in (1,-1):
        key=block(PITCH_X+f['dx'][0],PITCH_X+f['dx'][1],*sorted((s_*f['y'][0],s_*f['y'][1])),d-.5,d+f['h'])
        for dx in f['screw_dx']:
            sx,sz=PITCH_X+dx,d+f['screw_h']
            key=key-yspan(1.6,s_*(f['y'][0]-.1),s_*(f['y'][0]+f['insert_pocket']),sx,sz)
            add(f'yaw_leg_to_disc_M2x6_{55*s_}_{dx:g}',button_screw(sx,s_*f['seat_y'],sz,'y',-s_,f['screw_len']),'Y','#555b5a',owner='M021-Y')
        disc=disc+key
    for i,deg in enumerate(YAW_HUB_BOLT_DEG,1):
        theta=math.radians(deg)
        bx=PITCH_X+YAW_HUB_BOLT_R*math.cos(theta)
        by=YAW_HUB_BOLT_R*math.sin(theta)
        # Nominal ISO 7380 M3 x 6: 2.2 mm through the disc, 3.8 mm into
        # the body hub insert. The head finishes 0.15 mm below the disc top.
        screw=axial(1.5,6,(bx,by,d-YAW_HUB_BOLT_RECESS-3),'z')
        screw=screw+axial(2.85,1.65,(bx,by,d-YAW_HUB_BOLT_RECESS+0.825),'z')
        add(f'yaw_disc_to_body_hub_M3x6_{i}',screw,'Y','#b7bfc0',owner='M021-Y')
    add('yaw_turntable_disc_flush',disc,'Y','#647787',owner='M012')
    out['yaw_turntable_disc_flush']['relief_tool']=cyl_disc
    # D-049 pitch output: 25T aluminium disc horn (E, HD-002) on the servo
    # spline, its disc in the +Y leg's 0.6 mm pocket. ISO 4762 M3 x 5 through
    # the horn web into the output; four ISO 7380 M3 x 6 from the leg's outer
    # face into the horn's tapped holes. All yaw-carried: the case turns.
    h=fe.HORN;top=fe.HORN_TOP_Y
    horn=axial(h['disc_r'],h['disc_t'],(PITCH_X,top-h['disc_t']/2,PITCH_Z),'y')
    horn=horn+axial(h['hub_r'],h['hub_t'],(PITCH_X,top-h['disc_t']-h['hub_t']/2,PITCH_Z),'y')
    bore=top-h['web']-fe.HORN_BOTTOM_Y
    horn=horn-axial(h['bore_r'],bore+.2,(PITCH_X,fe.HORN_BOTTOM_Y+bore/2-.1,PITCH_Z),'y')
    horn=horn-axial(h['screw_r'],h['web']+.2,(PITCH_X,top-h['web']/2,PITCH_Z),'y')
    for deg in h['holes_deg']:
        hx=PITCH_X+h['pcd_r']*math.cos(math.radians(deg));hz=PITCH_Z+h['pcd_r']*math.sin(math.radians(deg))
        horn=horn-axial(1.5,h['disc_t']+.2,(hx,top-h['disc_t']/2,hz),'y')
        seat=fe.LEG_INNER_Y+6-fe.M3_HEAD_CBORE_D
        add(f'pitch_horn_to_leg_M3x6_{deg:g}',m3_button_screw(hx,seat,hz,'y',1,6),'Y','#555b5a',owner='M021-Y')
    add('pitch_horn_25T_disc',horn,'Y','#b7bfc0',owner='M013-15-P')
    add('pitch_horn_centre_M3x5',m3_socket_screw(PITCH_X,top,PITCH_Z,'y',1,5),'Y','#555b5a',owner='M021-Y')
    # Distinct layered ear rims and removable, hollow tapered caps. The caps
    # have two supported receivers and a deep enough centre floor for real
    # 1.2 mm colour inserts; the trim hardware is finished in details.py.
    for sign in [-1,1]:
        c=(EAR_X,sign*66.5,EAR_Z)
        rim=axial(30,3,c,'y')-axial(28,5,c,'y')
        # A continuous 1.8 mm annular web connects the cap receivers but
        # starts outside the cradle stalk pads, preserving outboard removal.
        rim=rim+(axial(24.8,1.8,(EAR_X,sign*71.0,EAR_Z),'y')-axial(20.3,2.2,(EAR_X,sign*71.0,EAR_Z),'y'))
        cap=Cone(30,27,6.2).rotate(Axis.X,-90*sign).moved(Location((EAR_X,sign*71.9,EAR_Z)))
        hollow=Cone(28.1,25.4,3.9).rotate(Axis.X,-90*sign).moved(Location((EAR_X,sign*70.05,EAR_Z)))
        cap=cap-hollow
        # A 1.3 mm recess leaves 1.7 mm behind the finish. The inlays below
        # are 1.2 mm prints with a 0.1 mm adhesive bed, flush to the cap.
        cap=cap-axial(22.5,2.6,(EAR_X,sign*75,EAR_Z),'y')
        # Two M2 cap screws sit on the upper semicircle: the lower quadrant
        # sweeps past the pitch yoke at the roll stops. Their receivers tie
        # into both the outer ring and internal annular web.
        screw_positions=[]
        for angle in [30,150]:
            a=math.radians(angle);xx=EAR_X+25*math.cos(a);zz=EAR_Z+25*math.sin(a)
            screw_positions.append((xx,zz))
            cap=cap+axial(2.6,3,(xx,sign*73.1,zz),'y')
            # Stepped receiver: a wider inboard foot overlaps the outer ring
            # below the cap, while the upper boss meets the annular web.
            rim=rim+axial(3.8,1.6,(xx,sign*68,zz),'y')
            rim=rim+axial(3,2.9,(xx,sign*70.15,zz),'y')
        rim=rim & axial(30,9,(EAR_X,sign*68.5,EAR_Z),'y')
        for xx,zz in screw_positions:
            cap=cap-axial(1.15,8,(xx,sign*73,zz),'y')-axial(2.1,1.6,(xx,sign*74.5,zz),'y')
            cap=cap-axial(3.3,5.8,(xx,sign*69.4,zz),'y')
            rim=rim-axial(3.3,.4,(xx,sign*72.1,zz),'y')
            add(f'ear_{sign}_M2_{len([n for n in out if n.startswith(f"ear_{sign}_M2")])+1}',button_screw(xx,sign*73.7,zz,'y',sign),'R','#555b5a',owner='M021a')
        for zoff in [-4,4]:
            zz=EAR_Z+zoff
            # Seat boss under the web: 1.2 mm of plastic under the head.
            rim=rim+axial(3,.8,(-20.5,sign*(EAR_PAD_TOP+.5),zz),'y')
            # The counterbore spans most of the web's width: close it with a
            # 1.2 mm wall on the inboard side and open it through the web's
            # outer edge, rather than leave crescent slivers on both.
            rim=rim+(axial(3.3,1.8,(-20.5,sign*71.0,zz),'y')&block(-24,-20.5,*sorted((sign*70.1,sign*71.9)),zz-3.3,zz+3.3))
            rim=rim-axial(1.15,9,(-20.5,sign*69,zz),'y')
            # Seat the hidden M2x4 head below the cap's inner roof, leaving
            # the cap back wall intact and the fastener accessible cap-off.
            rim=rim-axial(2.1,3.1,(-20.5,sign*72.05,zz),'y')-block(-20.5,-16,*sorted((sign*70.5,sign*73.6)),zz-2.1,zz+2.1)
            add(f'ear_{sign}_hidden_mount_M2_{zoff}',button_screw(-20.5,sign*70.5,zz,'y',sign,4),'R','#535957',owner='M021-R')
        # Ear enclosure parts use the same inspection/X-ray material as the
        # front, side and rear skins; hardware and moving structure stay opaque.
        add(f'ear_{sign}_ridged_inner_mount',rim,'R','#303a3c',alpha=.20,owner='M019a')
        add(f'ear_{sign}_hollow_removable_cap',cap,'R',alpha=.20,owner='M019a')
        ring=axial(21.8,1.2,(EAR_X,sign*74.4,EAR_Z),'y')-axial(20.6,1.4,(EAR_X,sign*74.4,EAR_Z),'y')
        inset=axial(20.4,1.2,(EAR_X,sign*74.4,EAR_Z),'y')
        add(f'ear_{sign}_amber_inlay',ring,'R','#b88636',alpha=.20,owner='M019a')
        add(f'ear_{sign}_dark_centre',inset,'R','#3d484a',alpha=.20,owner='M019a')
    # Front M2 x 8: 3.3 mm through the bezel pad, 3 mm in the insert, 1.7 mm
    # into the tip relief.
    for i,(y,z) in enumerate(FRONT_SCREWS):
        add(f'front_M2x8_{i+1}',button_screw(-1.7,y,z,'x',1,8),'R','#535957',owner='M021a')
    for i,(y,z) in enumerate(REAR_SCREWS):
        add(f'rear_M2x6_{i+1}',button_screw(-113.5,y,z,'x',-1),'R','#535957',owner='M021a')
    from details import detail_parts
    detail_parts(out)
    if reliefs:
        # Window construction samples deliberately differ from verification.
        # Samples are clamped into the A+ firmware envelope: poses the head
        # never reaches must not carve the helmet.
        import motion_envelope as env
        table=env.load()
        # Dense along the boundary: each relief is one union box per tool, so
        # sparse clamped samples leave gaps between them.
        samples=env.grid_poses(table,[ROLL_STOP[0],-18,-12,-6,0,6,12,18,ROLL_STOP[1]],[PITCH_STOP[0],-22,-18,-14,-10,-5,0,5,10,15,20,25,30,35,40,PITCH_STOP[1]])
        import multiprocessing
        import os
        from cad_cache import _encode
        from relief_worker import TARGETS, SUPPORTS, initialize, sample_bounds
        from run_checks import worker_cap
        encoded={name:_encode(out[name].get('relief_tool',out[name]['shape']))
                 for name in (*TARGETS,*SUPPORTS)}
        # Daemon pool workers may themselves need to build parts on a cache
        # miss. They cannot spawn children, so retain a serial fallback.
        parallel=(not multiprocessing.current_process().daemon and
                  os.environ.get('MAKAD_RELIEF_SERIAL')!='1' and len(samples)>1)
        if parallel:
            pool=multiprocessing.get_context('spawn').Pool(
                processes=min(worker_cap(),len(samples)),
                initializer=initialize,initargs=(encoded,))
            results=pool.imap(sample_bounds,samples,chunksize=1)
        else:
            initialize(encoded)
            results=map(sample_bounds,samples)
        bounds_by_pair={(name,support):[] for name in TARGETS for support in SUPPORTS}
        try:
            for result in results:
                for pair,boxes in result.items():
                    bounds_by_pair[pair].extend(boxes)
        finally:
            if parallel:
                pool.close();pool.join()
        for name in TARGETS:
            s=out[name]['shape'];cuts=[]
            for support in SUPPORTS:
                bounds=bounds_by_pair[name,support]
                if bounds:
                    lo=[min(b[0][i] for b in bounds)-2 for i in range(3)]
                    hi=[max(b[1][i] for b in bounds)+2 for i in range(3)]
                    cuts.append(block(lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]))
            if cuts:
                style=out[name]
                cut=s.cut(*cuts)
                # A relief box ending within 0.1 mm of a free edge leaves a
                # paper-thin chip; drop fragments below 5 mm3, keep real parts.
                kept=[x for x in cut.solids() if x.volume>5.]
                if len(kept)<len(cut.solids()):cut=kept[0] if len(kept)==1 else Compound(children=kept)
                style['shape']=tint(cut,name,style['color'],style['alpha'])
    return out

def assembly(internals=False,roll=0,pitch=0,yaw=0):
    from inspection_scene import scene
    return scene(build_parts(),internals=internals,roll=roll,pitch=pitch,yaw=yaw)
