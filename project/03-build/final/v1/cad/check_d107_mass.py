"""D-107 mass ledger and conservative yaw/pitch/roll tipping screen.

Starts at the recorded D-095 state, before PCB-14/16 and D-104/105 deltas.
Therefore neither the bracket nor hollow trunnion is subtracted twice.
Component/cable masses are E; printed volumes are authored CAD, not weighed.
"""
import json
import math
from pathlib import Path
from build123d import Compound
import module_checks as C
import d107_umbilical as U
import check_d095_mass as D
import pcb_integration as P

HERE=Path(__file__).resolve().parent


def main():
    e=C.load_entry();M=e._body;r=C.Report('check_d107_mass_d109' if __import__('os').environ.get('MAKAD_D109_MASS') else 'check_d107_mass')
    rep={x['check']:x for x in json.loads((HERE/'check_d095_mass-report.json').read_text())['rows']}
    removed={n for n,g in rep['removed_rows']['rows']}
    base=[(n,g,tuple(c)) for n,g,c,_ in M.MASS_ROWS if n not in removed]
    base += [(n,g,tuple(c)) for n,g,c,_ in rep['added_rows']['rows']]
    delta=[];moving=[];origin=e.HEAD_ORIGIN_IN_CHASSIS
    def add(n,g,c,why,head=False):
        row=(n,g,tuple(c));delta.append((*row,why))
        if head: moving.append(row)
    def printed(n,shape,head=False):
        v,c=D.centroid(shape)
        if head:c=tuple(c[k]+origin[k] for k in range(3))
        add(n,v*D.PETG_BODY/1000,c,'E authored volume × PETG 1.20; complete mounting envelope conservatively counted',head)
    # Remove the old body-side cassette parts from BODY_YAW_STAGE.
    v,c=D.centroid(M._yaw_cassette_stator())
    add('cassette stator removed',-v*D.PETG_BODY/1000,c,'E CAD volume × PETG 1.20')
    add('cassette FFCs removed',-4.5,(16,0,127),'E D-044 register allowance')
    add('PCB14 x3 and six sockets removed',-3.93,(16,-1,142.3),'E D-052 register: 3×0.51 + 6×0.4')
    # Source posts are removed without adding D-101 replacement posts.
    rotor=next(p for p in M.yaw_drive_moving_parts() if p.label=='YAW_ROTOR_CLAMP_DRUM_AND_STOP_DOG')
    edited=e._apply_droid_cuts(Compound(children=[rotor]),strict=False).children[0]
    va,ca=D.centroid(edited);vb,cb=D.centroid(rotor);dv=va-vb
    cc=tuple((va*ca[k]-vb*cb[k])/dv for k in range(3))
    add('source PCB14 rotor posts removed',dv*D.PETG_BODY/1000,cc,'E exact edited-minus-source volume')
    add('cassette screws removed',-.6,(16,0,135),'E three M2×6')
    # No PCB-16, D-104 or D-105 rows exist in the D-095 baseline.
    core=next(sh for label,sh in P.raw_parts(8) if label.endswith('_PCB'))
    v08=C.volume(core);m08=v08*1.85/1000
    j88=sum(g for n,g,c,w in rep['added_rows']['rows'] if n=='YAW_JUNCTION_J8_8_FEETECH_5264_3P_HEADER')
    add('PCB08 rev B replaces existing allowance',m08+3.+.5+.4+.02+.42-3.-j88,(-5,-33.5,116),
        'E measured FR4 core + two 1.5 g Micro-Fits + two .25 g GH + .4 g SPOX + .02 g R1 + .42 g isolated inner fills; replaces 3 g plus D-095 header')
    printed('body camera cradle',U.body_camera_mount())
    printed('body strain relief',U.body_clamp())
    printed('PCB08 edge cradle',U.pcb08_cradle())
    printed('PCB08 removable keeper',U.pcb08_keeper())
    add('PCB08 keeper screw',.15,(6.5,-19,114),'E M2×4')
    add('B0091 body board and static HDMI share',10.8,U.BODY_BOARD,'E 4.3 g populated adapter + .5 g 150mm Pi FPC + 6 g of the HDMI lead')
    # M006 already owns 8 g of CSI cable/relief. Replace this allowance with
    # the adapter, 150mm ribbon and a conservative half-cable share.
    old=(origin[0]-30,10,origin[2]+65)
    add('M006 prior CSI allowance removed',-8.,old,'E existing head mass-placement.json allowance',True)
    add('B0091 head board, ribbon and HDMI share',11.8,tuple(U.HEAD_BOARD[k]+origin[k] for k in range(3)),
        'E 4.3 g adapter + .5 g static ribbon + 7 g HDMI share',True)
    # Use exact lower-skin delta recorded by the geometry check; retaining
    # its old centroid for this tiny delta is explicitly an E placement.
    neck={x['check']:x for x in json.loads((HERE/'check_d107_neck-report.json').read_text())['rows']}
    add('lower skin opening and collar',neck['lower_skin_and_collar_fused']['volume_delta_mm3']*1.2/1000,
        (origin[0]-50.4,0,origin[2]+2),'E exact signed CAD volume change at collar centre',True)
    for n,s in [('roof camera cradle',U.head_camera_mount()),('head clamp jaw',U.clamp_bar()),
                ('disc bore bushing',U.bushing(origin)),('rotor liner',U.rotor_liner(origin))]:
        printed(n,s,True)
    add('head clamp screws and inserts',.7,(origin[0]-50.4,0,origin[2]+4),'E two M2×8 plus two M2×3 brass inserts',True)
    add('head clamp silicone liners',.03,(origin[0]-50.4,0,origin[2]+5.5),'E two thin silicone half liners',True)
    add('B0091 retaining ties',.1,U.BODY_BOARD,'E one 2.5 mm nylon tie')
    add('B0091 head retaining tie',.1,tuple(U.HEAD_BOARD[k]+origin[k] for k in range(3)),'E one 2.5 mm nylon tie',True)
    # Retain the full 15 g M020 allowance for W47 and its internal fan-out.
    # This exceeds the copper/silicone estimate (~9.4 g for 350 mm of all
    # twelve wires) and includes plugs; no extra wire mass is added twice.
    import os
    if os.environ.get('MAKAD_D109_MASS'):
        # D-109: routed body-harness rows (check_d109_mass) move out of the 95 g allowance.
        d109=json.loads((HERE/'check_d109_mass-report.json').read_text())
        d109=next(x for x in d109['rows'] if x['check']=='mass rows')['rows']
        for n,g,c in d109:
            add(f'D-109 {n}',g,tuple(c),'E routed body harness (check_d109_mass)')
        add('D-109 share of HARNESS_AND_FASTENERS allowance',-sum(g for n,g,c in d109),(20.,0.,88.),'E')
    # D-125: aluminium fixed pinion half and its steel pre-wind peg (check_d125_pinion_dbore).
    d125=json.loads((HERE/'check_d125_pinion_dbore-report.json').read_text())
    for n,g,c in next(x for x in d125['rows'] if x['check']=='mass rows')['rows']:
        add(f'D-125 {n}',g,tuple(c),'E CAD volume × density (check_d125_pinion_dbore)')
    rows=base+[(n,g,c) for n,g,c,w in delta]
    bal=e.D105_BALLAST
    copper_g=M.BALLAST_BAR_G*(bal['density']/bal['was_density']-1)
    copper=('copper ballast delta',copper_g,(sum(M.BALLAST_X)/2,0,sum(M.BALLAST_Z)/2))
    def sweep(extra,extra_camera_g=0.):
        import numpy as np
        from study_umbilical_span import Head
        ht=json.loads((M.HEAD_DIR/'mass-placement.json').read_text());a=ht['axes']
        # Recompute the actual signed head moments instead of adding the
        # absolute radii of removed and added components to a worst-case bound.
        # That bound counts the same relocated mass twice and can falsely fail.
        head_rows=[(x['name'],x['mass_g'],tuple(x['center_mm']),x['frame']) for x in ht['rows']]
        for n,g,c in moving:
            f='Y' if n in ('disc bore bushing','rotor liner') else 'R'
            head_rows.append((n,g,tuple(c[k]-origin[k] for k in range(3)),f))
        if extra_camera_g:head_rows.append(('camera extra mass',extra_camera_g,tuple(U.HEAD_BOARD),'R'))
        assert abs(sum(x['mass_g'] for x in ht['rows'])-M.HEAD_MASS_G)<.01
        # The full moving mass replaces the HEAD_V1 root row. Every other
        # D-095/body delta stays stationary; no nested head double counting.
        stationary=[row for row in rows if row[0]!='HEAD_V1' and row[0] not in {n for n,g,c in moving}]+extra
        mass=sum(g for n,g,c in stationary)+sum(g for n,g,c,f in head_rows)
        moment=np.sum([g*np.asarray(c) for n,g,c in stationary],axis=0)
        h=Head(dict(origin=np.asarray(origin),pitch_axis=np.array([a['pitch_x'],0,a['pitch_z']]),
                    roll_axis=np.array([0,a['roll_y'],a['roll_z']]),yaw_axis_x=np.array([a['pitch_x']])))
        groups=[]
        for f in ('Y','P','R'):
            sub=[(g,np.asarray(c)) for n,g,c,fr in head_rows if fr==f]
            g=sum(g for g,c in sub);c=sum((g*c for g,c in sub),np.zeros(3))/g
            groups.append((f,g,c))
        yaw=np.radians(np.arange(360));cc,ss=np.cos(yaw),np.sin(yaw)
        axis=np.array([origin[0]+a['pitch_x'],0,0]);gm=sum(g for f,g,c in groups)
        best=(1e9,None);neutral=None
        for q in sorted(set(range(-25,44))|{0}):
            for roll in range(-21,22):
                hm=sum((g*h.to_world(c,f,0,q,roll)[0] for f,g,c in groups),np.zeros(3))
                rel=hm-gm*axis
                mx=moment[0]+gm*axis[0]+cc*rel[0]-ss*rel[1]
                mz=moment[2]+hm[2]
                tip=9.81*mx/mz
                k=int(np.argmin(tip));candidate=(float(tip[k]),(int(k),q,roll))
                if candidate[0]<best[0]:best=candidate
                if q==roll==0:neutral=(moment+hm)/mass
        return dict(mass_g=mass,com_mm=neutral.tolist(),worst_yaw_a_tip=best[0],pose_yaw_pitch_roll=best[1],
                    margin_pct=100*(best[0]/D.A_TIP_MIN-1),poses=360*69*43,
                    method='actual frame centroids over 1 degree pitch/roll grid to hard stops, full 360 degree yaw')
    def legacy_bound(extra_camera_g=0.):
        # Exact reproduction of D095's older register calculation. It retains
        # the source head radii and treats final delta centroids as stationary;
        # use the actual moving-frame sweep for current geometry/sensitivity.
        trial=rows+([('extra camera mass',extra_camera_g,tuple(U.HEAD_BOARD[k]+origin[k] for k in range(3)))] if extra_camera_g else [])
        out=D.tip(trial,M)
        out.update(margin_pct=100*(out['worst_pose_a_tip']/D.A_TIP_MIN-1),extra_camera_g=extra_camera_g,
                   method='D095 original register bound, unchanged source-head radii; final delta centroids stationary')
        return out
    steel=sweep([]);cu=sweep([copper])
    r.check('mass_rows',True,rows=delta,net_delta_g=sum(g for n,g,c,w in delta),
            retained_allowances='M008 C2 20 g; M020 wires and fanout 15 g; neither double counted',
            note='D/E estimates only; D-095 baseline before D-104/105; full 360° yaw and actual 1° pitch/roll centroid sweep')
    r.check('mass_and_tipping',steel['margin_pct']>=1.5,steel=steel,copper=cu,minimum=D.A_TIP_MIN,
            ballast_choice='steel restored' if steel['margin_pct']>=3 else 'retain copper',
            required_margin_pct=1.5,steel_release_margin_pct=3.)
    legacy=legacy_bound();legacy10=legacy_bound(10.);adverse=sweep([],10.)
    r.check('original_register_bound_and_camera_mass_sensitivity',legacy['margin_pct']>=3. and adverse['margin_pct']>=3. and legacy10['margin_pct']>=1.5,
            original_register_bound=legacy,original_register_extra10g=legacy10,
            actual_moving_frame_extra10g=adverse,steel_release_margin_pct=3.,
            original_register_extra10g_clears_3pct=legacy10['margin_pct']>=3.,
            physical_release='HOLD: original register all10g-in-head sensitivity is below3%; weigh/dress actual cable and validate physical tipping',
            note='PASS records nominal>=3%, moving-frame adverse>=3% and legacy adverse>=1.5% operating minimum; it does NOT assert every method/scenario clears3%')
    r.finish()


if __name__=='__main__':main()
