"""Head cable-passage study: can a wire bundle get from PCB-16 (yaw frame) to the pitch and roll frames?

Free space per frame from surface-sampled parts (0.7 mm samples on every head part, PCB-12/16 and
their screws) at 234 envelope poses (roll 3.5 deg x pitch 4 deg steps, clamped), on a 1.25 mm
grid, as Euclidean distance maps. A route segment riding a frame must stay where no part of any
frame reaches at any pose; a joint crossing needs space free in both neighbouring frames. Then
the reachability chain PCB-16 -> yaw -> pitch -> roll -> PCB-12 at several clearances.

Finding (2026-11-10): reachable only at the bare minimum (1.25 mm) and only through yaw/pitch
crossings about 50 mm from the pitch axis at the grid's edge, outside the head shell; none at 2 mm
or more. Pitch/roll crossings exist within 0.5 mm of the roll axis. The head has no cable passage
across the pitch joint. Run with the legacy runtime, PYTHONPATH 03-head/v1/cad first; about 8 min.
"""

import sys, math, time, numpy as np
sys.path.insert(0, "/Users/avinier/robotics/makad/project/03-build/final/v1/cad")
from scipy import ndimage
import module_checks as C
from cadgen.step_scene import import_step
import check_pcb12_fit as F12, check_pcb16_fit as F16
t0=time.time()
entry=C.load_entry()
import layout_model as m, motion_envelope as env
parts=m.build_parts(catalog=False)
shapes={n:(d["shape"],d["frame"]) for n,d in parts.items() if d["kind"]=="physical" and n not in F12.REMOVED}
cr="connected_rolling_cradle_flange_ear_stalks"; dk="yaw_turntable_disc_flush"
s=shapes[cr][0]
for sh in entry.pcb12_local("pocket"): s=s-sh
for sh in entry.pcb12_local("boss"): s=s+sh
shapes[cr]=(s,"R")
s12=import_step(str(F12.STEP)); k12=[c for c in s12.children if c.solids()]
core=next(c for c in k12 if not c.children); loc=F12.board_location(C._box(core)[5]-C._box(core)[2])
for c in k12: shapes["PCB12_"+c.label]=(c.moved(loc),"R")
for i,sc in enumerate(entry.pcb12_local("screws")): shapes[f"PCB12_S{i}"]=(sc,"R")
for c in (c for c in import_step(str(F16.STEP)).children if c.solids()): shapes["PCB16_"+c.label]=(c.moved(F16.board_location()),"Y")
for i,sc in enumerate(entry.pcb16_local("screws")): shapes[f"PCB16_S{i}"]=(sc,"Y")
print("parts",len(shapes),round(time.time()-t0))
# sample surfaces
SP=0.7
samples={"Y":[],"P":[],"R":[]}
for n,(s,f) in shapes.items():
    try:
        verts,tris=s.tessellate(0.2,0.5)
    except Exception as e:
        print("tess fail",n,e); continue
    V=np.array([[v.X,v.Y,v.Z] for v in verts]); T=np.array(tris)
    if len(T)==0: continue
    A,B,Cc=V[T[:,0]],V[T[:,1]],V[T[:,2]]
    pts=[V]
    for a,b,c in zip(A,B,Cc):
        L=max(np.linalg.norm(b-a),np.linalg.norm(c-a),np.linalg.norm(c-b))
        k=int(math.ceil(L/SP))
        if k<=1: pts.append(((a+b+c)/3)[None]); continue
        u,v=np.meshgrid(np.arange(k+1),np.arange(k+1)); msk=(u+v)<=k
        u,v=u[msk]/k,v[msk]/k
        pts.append(a+np.outer(u,b-a)+np.outer(v,c-a))
    samples[f if f in samples else "Y"].append(np.vstack(pts))
for f in samples: samples[f]=np.vstack(samples[f]) if samples[f] else np.zeros((0,3)); print(f,len(samples[f]))
print("sampled",round(time.time()-t0))
S=1.25
X=np.arange(-82,-5,S); Y=np.arange(-62,62.1,S); Z=np.arange(-36,78.1,S)
sh=(len(X),len(Y),len(Z))
def rot(P,axis,deg):
    o=np.array([axis.position.X,axis.position.Y,axis.position.Z]); d=np.array([axis.direction.X,axis.direction.Y,axis.direction.Z])
    th=math.radians(deg); V=P-o
    return o+V*math.cos(th)+np.cross(d,V)*math.sin(th)+np.outer(V@d,d)*(1-math.cos(th))
def mark(grid,P):
    I=np.floor((P-[X[0]-S/2,Y[0]-S/2,Z[0]-S/2])/S).astype(int)
    ok=(I[:,0]>=0)&(I[:,0]<sh[0])&(I[:,1]>=0)&(I[:,1]<sh[1])&(I[:,2]>=0)&(I[:,2]<sh[2])
    I=I[ok]; grid[I[:,0],I[:,1],I[:,2]]=True
table=env.load()
rolls=np.arange(-21,21.01,3.5); pitches=np.arange(-25,43.01,4)
poses=sorted({(float(env.clamp_roll(table,r,q)),float(q)) for q in pitches for r in rolls})
print("poses",len(poses))
blocked={o:np.zeros(sh,bool) for o in "YPR"}
mark(blocked["Y"],samples["Y"]); mark(blocked["P"],samples["P"]); mark(blocked["R"],samples["R"])
for r,q in poses:
    # observer Y: P parts pitch(q); R parts pitch(q) roll(r)
    mark(blocked["Y"],rot(samples["P"],m.PITCH_AXIS,q))
    mark(blocked["Y"],rot(rot(samples["R"],m.ROLL_AXIS,r),m.PITCH_AXIS,q))
    # observer P: Y parts pitch(-q); R parts roll(r)
    mark(blocked["P"],rot(samples["Y"],m.PITCH_AXIS,-q))
    mark(blocked["P"],rot(samples["R"],m.ROLL_AXIS,r))
    # observer R: P parts roll(-r); Y parts roll(-r) pitch(-q)
    mark(blocked["R"],rot(samples["P"],m.ROLL_AXIS,-r))
    mark(blocked["R"],rot(rot(samples["Y"],m.PITCH_AXIS,-q),m.ROLL_AXIS,-r))
print("marked",round(time.time()-t0))
dist={o:ndimage.distance_transform_edt(~ndimage.binary_dilation(blocked[o]))*S for o in "YPR"}

# ---- reachability chain
import json
from pathlib import Path
D = {"Y": dist["Y"], "P": dist["P"], "R": dist["R"]}
st = np.ones((3, 3, 3))
PA = np.array([-42.4187, 0, 45.5515]); RA = np.array([0, -1.0266, 48.1565])
def box(xr, yr, zr):
    return (X[:, None, None] >= xr[0]) & (X[:, None, None] <= xr[1]) & (Y[None, :, None] >= yr[0]) & (Y[None, :, None] <= yr[1])         & (Z[None, None, :] >= zr[0]) & (Z[None, None, :] <= zr[1])
start_box, goal_box = box((-47.5, -34.5), (54, 57), (-30, -20)), box((-36, -27), (-44, -20), (6, 24))
G = np.stack(np.meshgrid(X, Y, Z, indexing="ij"), -1)
rows = []
for need in (1.25, 2.0, 2.5, 3.0):
    mY, mP, mR = D["Y"] >= need, D["P"] >= need, D["R"] >= need
    lY, _ = ndimage.label(mY, st); reachY = np.isin(lY, list(set(np.unique(lY[start_box & mY])) - {0}))
    cYP = reachY & mP
    lP, _ = ndimage.label(mP, st); reachP = np.isin(lP, list(set(np.unique(lP[cYP])) - {0}))
    cPR = reachP & mR
    lR, _ = ndimage.label(mR, st); reachR = np.isin(lR, list(set(np.unique(lR[cPR])) - {0}))
    dp = np.hypot(G[..., 0] - PA[0], G[..., 2] - PA[2]); dr = np.hypot(G[..., 1] - RA[1], G[..., 2] - RA[2])
    rows.append(dict(clearance_mm=need, yaw_reachable_voxels=int(reachY.sum()), yaw_pitch_crossings=int(cYP.sum()),
                     nearest_yaw_pitch_crossing_to_pitch_axis_mm=float(dp[cYP].min()) if cYP.any() else None,
                     pitch_roll_crossings=int(cPR.sum()),
                     nearest_pitch_roll_crossing_to_roll_axis_mm=float(dr[mP & mR].min()) if (mP & mR).any() else None,
                     reaches_pcb12=bool((reachR & goal_box).any())))
    print(rows[-1])
Path(__file__).with_name("study_head_cable_passage-report.json").write_text(json.dumps(dict(poses=len(poses), grid_mm=S, rows=rows), indent=1) + "\n")
