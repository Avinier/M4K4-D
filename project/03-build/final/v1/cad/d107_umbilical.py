"""D-107 centre umbilical: final-assembly-owned geometry, mm.

Camera and mating-plug bodies are documented envelopes, not vendor solids.
The replaceable wire route is a checked-in solver candidate; the geometry
check independently measures it against the edited head and body.
"""
import json
from pathlib import Path
from build123d import Box, Compound, Cone, Cylinder, Location, Plane, Solid, Sphere, Vector

HERE = Path(__file__).resolve().parent
CLAMP = (-50.4, 0., 6.)
OPENING = (-65.3, -31.3, -15.8, 14.4)  # initial oblique-passage allowance
RADIUS, FREE_LENGTH = 3.5, 95.
YAW_X = -42.41874076877715
HEAD_BOARD = (-67., -20., 69.)
BODY_BOARD = (53., -30., 113.)
BOARD_SIZE = (25.2, 27.83, 1.6)


def block(x0,x1,y0,y1,z0,z1):
    return Box(x1-x0,y1-y0,z1-z0).moved(Location(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)))


def zc(r,z0,z1,x=0.,y=0.):
    return Cylinder(r,z1-z0).moved(Location((x,y,(z0+z1)/2)))


def tube(points,radius):
    """Connected, closed cable-envelope solids with rounded sample joints."""
    pieces=[]
    for a,b in zip(points,points[1:]):
        a,b=Vector(*a),Vector(*b);v=b-a
        if v.length>1e-7:
            pieces.append(Solid.make_cylinder(radius,v.length,Plane(origin=a,z_dir=v)))
    pieces.extend(Sphere(radius).moved(Location(tuple(p))) for p in points[1:-1])
    return Compound(children=pieces)


def route_data():
    return json.loads((HERE/'d107-routes.json').read_text())


def neutral_points(origin):
    row=next(r for r in route_data()['routes'] if r['pitch']==0 and r['roll']==0)
    return [tuple(p[k]-origin[k] for k in range(3)) for p in row['points']]


def opening():
    return block(*OPENING,-1.,4.)


def xc(r,x0,x1,y,z):
    return Solid.make_cylinder(r,x1-x0,Plane(origin=(x0,y,z),z_dir=(1,0,0)))


def grip_bore():
    x,y,z=CLAMP
    # The rod's final2mm and the outgoing fan-out are straight. A bell
    # beneath the3mm grip accommodates the bend before that straight land.
    return zc(3.6,4.,8.,x,y)+Cone(6.,3.6,3.).moved(Location((x,y,2.5)))


def collar():
    x0,x1,y0,y1=OPENING;x,y,z=CLAMP
    ring=block(x0-2,x1+2,y0-2,y1+2,.6,3.)-block(x0,x1,y0,y1,-1,4)
    back=block(x-7,x,-13,13,1.,7.)-grip_bore()
    for yy in (-14.,14.):back+=block(x-7,x,yy-2,yy+2,.6,3.)
    for yy in (-9.5,9.5):
        back-=xc(1.6,x-3.,x+.1,yy,4.)
        back-=xc(1.1,x-5.2,x-2.9,yy,4.)
    return ring+back


def clamp_bar():
    x,y,z=CLAMP
    jaw=block(x,x+7,-13,13,1.,7.)-grip_bore()
    for yy in (-9.5,9.5):
        jaw-=xc(1.1,x-.1,x+3.,yy,4.)
        jaw-=xc(1.95,x+3.,x+7.1,yy,4.)
    return jaw


def clamp_screws():
    x,y,z=CLAMP
    # Heads recessed in the front jaw; one8mm-long shank reaches the
    # M2x3 insert in the integral back half. Tools enter from the opening.
    return [xc(1.,x-5.,x+3.,yy,4.)+xc(1.9,x+3.,x+4.3,yy,4.) for yy in (-9.5,9.5)]


def clamp_inserts():
    x,y,z=CLAMP
    return [xc(1.8,x-3.,x,yy,4.)-xc(1.,x-3.1,x+.1,yy,4.) for yy in (-9.5,9.5)]


def grip_pads():
    x,y,z=CLAMP
    ring=zc(3.6,4.,7.,x,y)-zc(3.35,3.9,7.1,x,y)
    return [ring & block(x-4,x,-4,4,3.9,7.1),ring & block(x,x+4,-4,4,3.9,7.1)]


def bushing(origin):
    x=YAW_X;oz=origin[2]
    part=zc(10.4,144.6-oz,155.-oz,x)+zc(12.,155.-oz,156.-oz,x)
    bore=zc(9.,143.-oz,157.-oz,x)
    # Flared entrance and exit, a 1.4 mm throat wall. Final edge finishing
    # and material compliance remain physical assembly checks.
    bore+=Cone(9.,10.3,3.).moved(Location((x,0,154.5-oz)))
    bore+=Cone(10.1,9.,2.).moved(Location((x,0,145.6-oz)))
    return part-bore


def rotor_liner(origin):
    oz=origin[2]
    # The flange seats on the rotor's Z137 upper face. The hub bore above
    # it has R13.15 clearance, so R12.4 gives a positive bearing land while
    # preserving0.75mm radial clearance to the hub. Remove the disc bushing
    # first and lift the liner upward; it cannot fall through the R11 rotor.
    outer=zc(10.8,120.-oz,144.6-oz,YAW_X)+zc(12.4,137.-oz,138.-oz,YAW_X)
    return outer-zc(9.,119.-oz,146.-oz,YAW_X)


def camera_parts(centre):
    """B0091 core/jack and slim straight plug; socket mouth faces +Y."""
    x,y,z=centre;w,l,t=BOARD_SIZE
    return {
        'BOARD':block(x-w/2,x+w/2,y-l/2,y+l/2,z,z+t),
        'HDMI_SOCKET':block(x-7.5,x+7.5,y+l/2-15.,y+l/2,z+t,z+12.62),
        'HDMI_MATED_PLUG_E':block(x-8.,x+8.,y+l/2,y+l/2+22.,z+3.,z+10.),
        'CSI15_SOCKET_E':block(x-9.,x+9.,y-l/2,y-l/2+4.,z+t,z+t+2.),
    }


def head_camera_mount():
    x,y,z=HEAD_BOARD;w,l,t=BOARD_SIZE
    # Slide-in edge cradle hangs from the inner roof (84.7 mm). The rear
    # cover provides access to the latch; no unknown board-hole pattern.
    part=None
    for side in (-1,1):
        xx=x+side*(w/2+1.)
        wall=block(xx-1,xx+1,y-l/2-1,y+l/2+1,z-1,85.1)
        lip=block(xx-2,xx+2,y-l/2-1,y+l/2+1,z-1,z)
        part=wall+lip if part is None else part+wall+lip
    # Rear stop links both rails and prevents insertion into the FFC socket.
    part+=block(x-w/2-2,x+w/2+2,y-l/2-2,y-l/2-1,z-1,z+2)
    return part-block(x-w/2-3,x+w/2+3,-28.5,-25.5,70.5,71.3)


def body_camera_mount():
    x,y,z=BODY_BOARD;w,l,t=BOARD_SIZE
    part=block(x-w/2-2,x+w/2+2,y-l/2-2,y+l/2+2,z-1,z)-block(x-w/2+1,x+w/2-1,y-l/2+1,y+l/2-1,z-2,z+1)
    for side in (-1,1):
        xx=x+side*(w/2+1.)
        part+=block(xx-1,xx+1,-26,-18,z-1,134.2)
    return part


def camera_tie(centre,head=False):
    """2.5 mm retaining tie through head rail slots / around body ledge.

    The edge lips support the PCB; this tie prevents forward withdrawal.
    The small ratchet head and actual nylon compliance remain E.
    """
    x,y,z=centre;w=BOARD_SIZE[0];yy=-27. if head else -36.
    extra=4. if head else 3.  # head lips project1mm farther than body ledge
    outer=block(x-w/2-extra,x+w/2+extra,yy-1.25,yy+1.25,z-1.5,z+2.1)
    inner=block(x-w/2-extra+.5,x+w/2+extra-.5,yy-1.4,yy+1.4,z-1.,z+1.6)
    return outer-inner


def body_clamp():
    # Open saddle for a wrap-around tie; mounted below the yaw plate.
    base=block(22,34,-22,-12,113.,116.)-block(24,32,-23,-11,114.,119.)
    # The support reaches the stationary plate outside its R28 bore and
    # outside the rotating R27 clamp ring. Posts inside the bore would float.
    base+=block(26,37,-32,-29,111.5,113.5)
    base+=block(26,30,-32,-14,111.5,113.5)
    base+=block(26,30,-18,-14,111.5,116.)
    # Broad side gusset into the PCB08 web; its top is cut back around
    # the complete rotating stop-dog envelope, rather than a thin post.
    brace=block(32.,38.4,-32,-14,111.5,135.2)
    brace-=zc(31.,120.9,146.,16.)
    base+=brace
    return base-block(24,32,-23,-11,114.,121.)


def pcb08_cradle():
    """Edge retention without changing the routed board's land patterns.

    The rear channel captures X and Z; a removable front keeper closes Y.
    A rib hangs from the stationary plate outside both the bore and rotor.
    """
    rail=block(5.6,7.4,-48,-18,110.5,112.)
    # Main hanger9.6×18, rather than the former2×2 post. Two deep beams
    # close the cradle load path; the upper tie also reaches the original
    # rear crossrail (X−36..−28,Z126..134). No new PCB holes are assumed.
    rail+=block(28.8,38.4,-47.,-29.,110.5,135.2)
    rail+=block(-26.,38.4,-48.5,-46.15,102.,112.)
    rail+=block(5.6,38.4,-20.8,-18.,109.,117.)
    rail-=block(24,32,-23,-11,114.,121.)
    tie=block(-32.,38.4,-33.,-30.,126.,134.2)-zc(31.,120.9,146.,16.)
    rail+=tie
    rail+=block(-26.,16.,-48,-44.8,110.5,112.)
    rail+=block(-26.,16.,-47.2,-46.3,111.,114.5)
    for x0,x1 in ((-26.,-22.15),(12.15,16.)):
        rail+=block(x0,x1,-47.2,-43.,110.5,114.5)
    for x0,x1 in ((-20.,-16.),(4.,7.4)):
        rail+=block(x0,x1,-47.2,-45.4,113.8,114.5)
    rail+=block(4.5,9.,-20.85,-18,111.,113.8)
    rail-=zc(.8,110.5,114.,6.5,-19.)
    rail-=block(4.4,9.1,-22.,-17.9,113.8,118.)  # keeper remains removable
    rail-=block(37.2,38.5,-37.4,-34.6,111.3,115.3)  # body-camera tie passage
    rail-=block(36.9,37.9,-31.,-18.,108.7,110.)  # Pi CSI tail below front beam
    return rail


def pcb08_keeper():
    return block(4.5,9.,-21.9,-18,113.8,115.4)-zc(1.1,113.,116.,6.5,-19.)


def pcb08_keeper_screw():
    return zc(1.,111.4,115.4,6.5,-19.)+zc(1.9,115.4,116.7,6.5,-19.)


def pcb12_plugs():
    """GHR bodies, separate from the now-explicit cable bend geometry.

    JST eGH assembly layout gives 7.3 mm top-entry mated stack. Allow 7.4;
    the KiCad header rises 4.2 beyond its mounting face, leaving 3.2 proud.
    Housing width B=1.25*n+1.25 and thickness4.15 are documented. Received
    wire dress remains U; the former 9 mm box included an unspecified bend.
    """
    return {name:block(-32.485,-29.285,y-w/2,y+w/2,z-2.075,z+2.075)
            for name,y,z,w in [('J1',-29.4,11.75,10.),('J2',-38.8,19.55,3.75),('J3',-18.6,11.75,5.)]}


def body_path():
    return [(16.,0.,152.),(16.,0.,116.),(28.,0.,118.),(28.,-16.,118.),(28.,-24.,118.)]


def inserts(entry):
    """(owner-group, world shape) droid entries."""
    paint=entry._tag;origin=entry.HEAD_ORIGIN_IN_CHASSIS;loc=Location(origin)
    out=[('Yaw mount',paint(bushing(origin).moved(loc),'D107_DISC_BORE_BUSHING','\x23536b78')),
         ('Yaw mount',paint(rotor_liner(origin).moved(loc),'D107_ROTOR_SMOOTH_LINER','\x23536b78')),
         ('Shell and covers',paint(clamp_bar().moved(loc),'D107_HEAD_CLAMP_BAR','\x23536b78'))]
    out.extend([('BODY_PRIMARY_FRAME',paint(pcb08_keeper(),'D107_PCB08_REMOVABLE_KEEPER','#536b78')),
                ('BODY_PRIMARY_FRAME',paint(pcb08_keeper_screw(),'D107_PCB08_KEEPER_M2X4','#777777'))])
    out.extend(('Head controller and light',paint(sh.moved(loc),f'D107_PCB12_{name}_MATED_GHR_PLUG','#eee9dd'))
               for name,sh in pcb12_plugs().items())
    out.extend(('Fasteners',paint(sh.moved(loc),f'D107_HEAD_CLAMP_M2X8_{i}','#777777'))
               for i,sh in enumerate(clamp_screws(),1))
    out.extend(('Fasteners',paint(sh.moved(loc),f'D107_HEAD_CLAMP_M2_INSERT_{i}','#bd9462'))
               for i,sh in enumerate(clamp_inserts(),1))
    out.extend(('Shell and covers',paint(sh.moved(loc),f'D107_HEAD_CLAMP_SOFT_PAD_{i}','#777a79'))
               for i,sh in enumerate(grip_pads(),1))
    for where,centre,at in (('Camera',HEAD_BOARD,loc),('BODY_PRIMARY_FRAME',BODY_BOARD,Location())):
        for name,shape in camera_parts(centre).items():
            out.append((where,paint(shape.moved(at),f'D107_B0091_{"HEAD" if where=="Camera" else "BODY"}_{name}',
                                    '\x23085536' if name=='BOARD' else '\x236d7378')))
        out.append((where,paint(camera_tie(centre,where=='Camera').moved(at),
                               f'D107_B0091_{"HEAD" if where=="Camera" else "BODY"}_RETAINING_TIE_E','#383b3e')))
    # Swept reserve is populated from all 45 solver candidates, with endpoint
    # mounts intentionally included. It is hidden in the presentation export.
    points=[p for r in route_data()['routes'] for p in r['points']]
    lo=[min(p[k] for p in points)-RADIUS for k in range(3)]
    hi=[max(p[k] for p in points)+RADIUS for k in range(3)]
    out.append(('Yaw mount',paint(block(lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]),
                                  'HARNESS_D107_NECK_SWEPT_ENVELOPE_RESERVE','\x23d3a860',.2)))
    return out
