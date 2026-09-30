"""Fast J07/J08 checks (D-011): the nose rows of check_layout.py on the nose parts only, about 30 s.

Run from this folder with the text-to-cad 0.4.28 runtime: python check_nose_joints.py
"""
import sys, json; sys.path.insert(0,'.')
import body_chassis_model as M
from build123d import Location
def _vol(s): return 0.0 if s is None else s.volume
def leaves(s):
    k=getattr(s,'children',None); return [l for c in k for l in leaves(c)] if k else [s]
def by_label(ss,l): return next(s for s in ss if s.label==l)
frame=M.chassis_frame()
ball_parts=leaves(M.ball_transfer())
pod_parts=leaves(next(c for c in frame.children if c.label=="BALL_POD"))
front_crossmember=next(c for c in frame.children if c.label=="FRONT_CROSSMEMBER")
sens=M.sensors()
nose_parts=leaves(next(c for c in sens.children if c.label=="BALL_NOSE_CONCEALED_CONTACT_MODULE"))
gp2y=[c for c in sens.children if c.label.startswith("GP2Y") and c.label!="GP2Y_OPTICAL_AXIS"]
flange=by_label(ball_parts,"BALL_TRANSFER_PURCHASED_3HOLE_FLANGE"); pod_seat=by_label(pod_parts,"BALL_POD_PRINTED_SEAT")
cap=by_label(nose_parts,"BALL_NOSE_TOUCH_CAP"); travel=by_label(nose_parts,"BALL_NOSE_3MM_TRAVEL_RESERVE")
springs=[p for p in nose_parts if p.label.startswith("BALL_NOSE_RETURN_SPRING")]
hall=by_label(nose_parts,"BALL_NOSE_HALL_DRV5055A3_SOT23"); magnet=by_label(nose_parts,"BALL_NOSE_MAGNET_D3X1P5_N35")
R={}
# J07 thread
eng={}
for sh in (p for p in pod_parts if p.label.startswith("BALL_M3_SHANK")):
    i=sh.label.rsplit("_",1)[1]; ins=by_label(pod_parts,f"BALL_SEAT_HEATSET_INSERT_{i}")
    sb,ib=sh.bounding_box(),ins.bounding_box()
    co=abs(sb.center().X-ib.center().X)<1e-3 and abs(sb.center().Y-ib.center().Y)<1e-3
    eng[sh.label]=round(min(sb.max.Z,ib.max.Z)-max(sb.min.Z,ib.min.Z),3) if co and _vol(ins&pod_seat)>1e-3 else 0.0
heads={p.label:(round(p.distance_to(by_label(ball_parts,"BALL_TRANSFER_POM_BALL")),3),round(_vol(p&flange),3)) for p in pod_parts if p.label.startswith("BALL_M3_HEAD")}
R["ball_screws_thread_into_seat_inserts"]=(len(eng)==3 and all(v>=4.5 for v in eng.values()) and all(a>=0.3 and b<1e-3 for a,b in heads.values()), eng, heads)
ii={p.label:round(_vol(p&(pod_seat if p.label.startswith("BALL_SEAT") else front_crossmember)),3) for p in pod_parts if "HEATSET_INSERT" in p.label}
R["heat_set_bores_give_interference"]=(len(ii)==5 and all(v>1e-3 for v in ii.values()), ii)
R["ball_flange_seats_on_pod"]=(flange.distance_to(pod_seat)<1e-6 and _vol(flange&pod_seat)<1e-3,)
# nose clashes
solids=[*ball_parts,*pod_parts,front_crossmember,*gp2y,*[p for p in nose_parts if p is not travel]]
ok_pairs=({"BALL_POD_M3_SHANK","BALL_POD_HEATSET_INSERT"},{"BALL_POD_HEATSET_INSERT","FRONT"},{"BALL_M3_SHANK","BALL_SEAT_HEATSET_INSERT"},{"BALL_SEAT_HEATSET_INSERT","BALL_POD_PRINTED"},{"BALL_POD_LID_M2X8_CSK","BALL_POD_PRINTED"})
cl={}
for i,a in enumerate(solids):
    for b in solids[i+1:]:
        if {a.label.rsplit("_",1)[0],b.label.rsplit("_",1)[0]} in ok_pairs: continue
        v=_vol(a&b)
        if v>1e-3: cl[f"{a.label} x {b.label}"]=round(v,3)
R["ball_nose_parts_do_not_interfere"]=(not cl, cl)
tb={s.label:round(_vol(travel&s),3) for s in [*ball_parts,*pod_parts,*gp2y,*[p for p in nose_parts if p is not travel and p not in springs]] if _vol(travel&s)>1e-3}
R["touch_cap_travel_reserve_is_clear"]=(not tb, tb)
rigid=[*ball_parts,*pod_parts,*gp2y]
R["rigid_nose_stays_behind_cap_travel"]=(max(s.bounding_box().max.X for s in rigid)<=M.TACTILE_CAP_INNER_X-M.TACTILE_NOSE_TRAVEL+1e-6,)
sweep={}
for step in range(1,31):
    mv=cap.moved(Location((-0.1*step,0,0)))
    for s in rigid:
        if _vol(mv&s)>1e-3: sweep.setdefault(s.label,round(0.1*step,2))
stop=_vol(cap.moved(Location((-M.TACTILE_NOSE_TRAVEL-0.1,0,0)))&pod_seat)>1e-3
ret=_vol(cap.moved(Location((0.1,0,0)))&pod_seat)>1e-3
gap=magnet.bounding_box().min.X-hall.bounding_box().max.X
mhits={s.label:round(_vol(magnet.moved(Location((-M.TACTILE_NOSE_TRAVEL,0,0)))&s),3) for s in rigid+[hall] if _vol(magnet.moved(Location((-M.TACTILE_NOSE_TRAVEL,0,0)))&s)>1e-3}
R["touch_cap_sweeps_3mm_rearward"]=(not sweep and stop and ret and not mhits and gap-M.TACTILE_NOSE_TRAVEL>=0.05, sweep, stop, ret, {"magnet_gap_rest":round(gap,3),"at_stop":round(gap-M.TACTILE_NOSE_TRAVEL,3)}, mhits)
hz=M._block(M.TACTILE_SNAP_HOOK_X[0]-0.01,M.TACTILE_SNAP_HOOK_X[2]+0.01,-30,30,M.TACTILE_SNAP_HOOK_Z[0]-0.01,M.TACTILE_SNAP_HOOK_Z[1]+0.01)
run=min((cap-hz).distance_to(s) for s in (pod_seat,by_label(pod_parts,"BALL_POD_SENSOR_LID")))
R["touch_cap_running_clearance"]=(run>=M.TACTILE_CAP_CLEARANCE-0.01, round(run,3))
R["touch_cap_stops_at_pod_seat"]=(abs(cap.bounding_box().min.Z-M.BALL_POD_Z0)<1e-3,)
R["ball_nose_is_lean"]=(cap.bounding_box().size.Y<=42.0, round(cap.bounding_box().size.Y,2))
shell=M.body_shell()
shell=next((c for c in leaves(shell) if c.label=="BODY_SHELL"),shell)
ov={s.label:round(_vol(s&shell),3) for s in pod_parts if _vol(s&shell)>1e-3}
R["ball_pod_passes_shell_notch"]=(not ov, ov)
p=M.mass_properties(); a=9.81*p['com_mm'][0]/p['com_mm'][2]
R["com_forward_of_physics_margin_line"]=(a>=9.81*20/124, round(p['mass_g'],1), [round(v,2) for v in p['com_mm']], round(a,3))
for k,v in R.items(): print("PASS" if v[0] else "FAIL", k, *v[1:])
