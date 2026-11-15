"""W47 clearance to the final-owned D102 PCB12 bosses and screw heads.

The neck check uses the conservative source cradle. These additions are
checked separately so they cannot be lost behind a source-only head check.
"""
import numpy as np
from build123d import Wire
import module_checks as C
import d107_umbilical as U
import head_harness as H
from study_umbilical_span import rot


def line(p):return Wire.make_polygon([tuple(x) for x in p],close=False)


def main():
    e=C.load_entry();r=C.Report('check_d107_controller_mount')
    import layout_model as m
    hardware={f'{kind}_{i}':sh for kind in ('boss','screws') for i,sh in enumerate(e.pcb12_local(kind))}
    gaps=[]
    for n,p in H.lead_paths().items():
        radius=.8 if n=='PCB12_J2_BRANCH' else (1.8 if n=='HEAD_CAMERA_HDMI' else (1. if n=='DISPLAY_POWER' else 1.5))
        gaps.extend((n,k,C.distance(line(p),sh)-radius) for k,sh in hardware.items())
    axis=np.array([0,m.ROLL_AXIS.position.Y,m.ROLL_AXIS.position.Z])
    screw_loop=[]
    for roll in np.arange(-21.,21.01,.5):
        lp=H.servo_loop(roll,axis)
        local=axis+(lp-axis)@rot('x',-roll).T
        p=axis+(np.asarray(H.SERVO_P_PATH)-axis)@rot('x',-roll).T
        for n,path in [('servo_roll_loop',local),('servo_pitch_lead',p)]:
            gaps.extend((f'{n}/{roll}',k,C.distance(line(path),sh)-1.5) for k,sh in hardware.items())
        screw_loop.extend((roll,k,C.distance(line(local),sh)-1.5) for k,sh in hardware.items() if k.startswith('screws'))
    best=min(gaps,key=lambda row:row[2])
    r.check('w47_clear_of_added_controller_bosses_and_screws',best[2]>=.1,
            minimum=best,required_nominal_gap_mm=.1,rolls=85,
            note='same 0.1 mm nominal wire clearance gate as the body check; received-wire dress and tolerance remain physical gates; relative P/R placement depends only on roll')
    closest=min(screw_loop,key=lambda row:row[2])
    r.check('roll_loop_screw_clearance_at_least_1mm',closest[2]>=1.,minimum=closest,roll_step_deg=.5,
            below_1mm_poses=sum(any(rr==x and d<1 for x,k,d in screw_loop) for rr in np.arange(-21.,21.01,.5)),
            roll_anchor_R=H.SERVO_R_ANCHOR)
    r.finish()


if __name__=='__main__':main()
