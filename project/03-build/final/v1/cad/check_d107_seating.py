"""D107 static head adapter, retaining tie and coaxial liner seating.

The neck check covers motion between frames; this checks the adapter against
its own frame and intended mounting contacts. Can reuse a built head scene.
"""
import re
from build123d import Compound, Location
import module_checks as C
import d107_umbilical as U


def check(parts,entry):
    r=C.Report('check_d107_seating')
    physical={n:d['shape'] for n,d in parts.items() if d['kind']=='physical'
              and d['frame']=='R' and not any(re.fullmatch(p,n) for p in entry.DROID_REMOVES)}
    physical['main_octagonal_skin']+=U.head_camera_mount()
    physical['main_octagonal_skin_lower']=physical['main_octagonal_skin_lower']-U.opening()+U.collar()
    physical['CLAMP_JAW']=U.clamp_bar()
    hit=[]
    for name,sh in {**U.camera_parts(U.HEAD_BOARD),'RETAINING_TIE':U.camera_tie(U.HEAD_BOARD,True)}.items():
        for other,s in physical.items():
            if not C._hit(C._box(sh),C._box(s)):continue
            v=C.common(sh,s)
            if v>1e-4:hit.append((name,other,v))
    r.check('head_adapter_and_tie_clear_of_own_frame',not hit,clashes=hit)
    import layout_model as m
    tie=U.camera_tie(U.HEAD_BOARD,True);tie_min=(999.,None,None)
    for row in U.route_data()['routes']:
        q,roll=row['pitch'],row['roll']
        posed=tie.rotate(m.ROLL_AXIS,roll).rotate(m.PITCH_AXIS,q)
        for n,d in parts.items():
            if d['kind']!='physical' or d['frame'] not in ('Y','P'):continue
            if any(re.fullmatch(p,n) for p in entry.DROID_REMOVES):continue
            target=d['shape'].rotate(m.PITCH_AXIS,q) if d['frame']=='P' else d['shape']
            if not C._hit(C._box(posed),C._box(target),3.):continue
            gap=C.distance(posed,target)
            if gap<tie_min[0]:tie_min=(gap,n,(q,roll))
    r.check('head_tie_motion_clear',tie_min[0]>=.2,minimum_mm=tie_min,poses=45)
    board=U.camera_parts(U.HEAD_BOARD)['BOARD'];mount=U.head_camera_mount()
    r.check('head_board_on_edge_lips',C.common(board,mount)<1e-4 and C.distance(board,mount)<1e-5,
            overlap_mm3=C.common(board,mount),seat_gap_mm=C.distance(board,mount))
    origin=entry.HEAD_ORIGIN_IN_CHASSIS
    disc=parts['yaw_turntable_disc_flush']['shape'];bush=U.bushing(origin);liner=U.rotor_liner(origin)
    r.check('bushing_flange_seated_on_disc',C.common(bush,disc)<1e-4 and C.distance(bush,disc)<1e-5,
            overlap_mm3=C.common(bush,disc),seat_gap_mm=C.distance(bush,disc),bushing_valid=bool(bush.is_valid))
    raw=entry._apply_droid_cuts(Compound(children=entry._body.yaw_drive_moving_parts()),strict=False)
    radial=[]
    for sh in raw.children:
        local=C.place(sh,Location(tuple(-v for v in origin)))
        if C._hit(C._box(local),C._box(liner),.3):
            radial.append((sh.label,C.common(liner,local),C.distance(liner,local)))
    r.check('liner_clear_of_rotor_and_hub',all(v<1e-4 for n,v,d in radial),measurements=radial,
            liner_valid=bool(liner.is_valid),liner_bushing_end_gap_mm=C.distance(liner,bush))
    rotor=next(sh for sh in raw.children if sh.label=='YAW_ROTOR_CLAMP_DRUM_AND_STOP_DOG')
    rotor=C.place(rotor,Location(tuple(-v for v in origin)))
    obstruction=C.common(liner.moved(Location((0,0,-.5))),rotor)
    land=C.common(liner.moved(Location((0,0,-.1))),rotor)/.1
    r.check('liner_flange_positive_downward_capture',obstruction>1 and land>50,
            downward_half_mm_obstruction_mm3=obstruction,bearing_land_mm2=land,
            flange_world_Z=[137.,138.],removal='remove disc bushing and lift liner upward through hub')
    bore=U.zc(9.,119-origin[2],157-origin[2],U.YAW_X)
    overlap=C.common(bore,bush)+C.common(bore,liner)
    r.check('finished_18mm_bore_through_both_liners',overlap<1e-4,overlap_mm3=overlap,axis_head_x=U.YAW_X)
    r.finish()


def main():
    e=C.load_entry()
    import layout_model as m
    check(m.build_parts(catalog=False),e)


if __name__=='__main__':main()
