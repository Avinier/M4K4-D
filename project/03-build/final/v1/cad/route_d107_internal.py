"""Propose static head fan-outs on a 1.5 mm occupancy grid.

This is cable routing, not PCB routing. Surface samples are dilated before
A*; exact posed-solid checks own acceptance of the saved paths.
"""
import heapq
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.ndimage import distance_transform_edt
from study_umbilical_span import Head
import d107_umbilical as U

HERE=Path(__file__).resolve().parent
GRID=1.5
LO=np.array([-109.,-56.,3.5]);HI=np.array([-18.,56.,82.])
SHAPE=tuple(np.ceil((HI-LO)/GRID).astype(int)+1)


def main():
    d=np.load(HERE/'__cadgen__/umbilical-homes.npz');s=np.load(HERE/'__cadgen__/umbilical-study.npz');h=Head(s)
    names=d['head_names'];pts=d['head_pts'];frames=d['head_frame'];labels=d['head_label']
    omit={'C2_removable_open_rear_tray','C2_tray_M2_-39','C2_tray_M2_-19','CSI_roof_straight_exit_guide'}
    keep=~np.isin(labels,[i for i,n in enumerate(names) if n in omit])
    occ=np.zeros(SHAPE,bool)
    def mark(p):
        idx=np.rint((p-LO)/GRID).astype(int)
        idx=idx[np.all((idx>=0)&(idx<np.asarray(SHAPE)),axis=1)]
        occ[tuple(idx.T)]=True
    mark(pts[keep&(frames==2)])
    P=pts[keep&(frames==1)];Y=pts[keep&(frames==0)]
    for r in (-21.,-10.5,0.,10.5,21.):
        mark(h.to_frame(h.to_world(P,'P',0,0,0),'R',0,0,r))
        for q in (-25.,-17.,-8.5,0.,8.5,17.,26.,34.5,43.):
            mark(h.to_frame(h.to_world(Y,'Y',0,0,0),'R',0,q,r))
    # New adapter and its mated plug must be obstacles too: otherwise a
    # superficially clear route can enter the back of the plug body.
    def fill_box(bb):
        ranges=[np.arange(bb[k],bb[k+3]+GRID/2,GRID/2) for k in range(3)]
        mark(np.stack(np.meshgrid(*ranges,indexing='ij'),-1).reshape(-1,3))
    for sh in U.camera_parts(U.HEAD_BOARD).values():
        bb=sh.bounding_box();fill_box((*bb.min,*bb.max))
    clearance=distance_transform_edt(~occ)*GRID
    offsets=[x for x in itertools.product((-1,0,1),repeat=3) if any(x)]
    def astar(start,end,min_gap):
        a=tuple(np.rint((np.asarray(start)-LO)/GRID).astype(int));b=tuple(np.rint((np.asarray(end)-LO)/GRID).astype(int))
        for key,p in [('start',a),('end',b)]:
            print(key,LO+GRID*np.asarray(p),'sample clearance',clearance[p],flush=True)
        allowed=clearance>=min_gap
        if not allowed[a] or not allowed[b]:return None
        g={a:0.};previous={};queue=[(mathdist(a,b),a)]
        while queue:
            _,node=heapq.heappop(queue)
            if node==b:
                path=[node]
                while node in previous:node=previous[node];path.append(node)
                path=list(reversed(path));points=[LO+GRID*np.asarray(x) for x in path]
                # Collapse only collinear steps; no untested corner cutting.
                out=[np.asarray(start)]
                for i in range(1,len(points)-1):
                    if np.linalg.norm(np.cross(points[i]-points[i-1],points[i+1]-points[i]))>1e-5:out.append(points[i])
                out.append(np.asarray(end));return np.round(out,5).tolist()
            for off in offsets:
                nxt=tuple(node[k]+off[k] for k in range(3))
                if any(nxt[k]<0 or nxt[k]>=SHAPE[k] for k in range(3)) or not allowed[nxt]:continue
                score=g[node]+mathdist(node,nxt)*(1+.3/max(clearance[nxt],1.))
                if score<g.get(nxt,float('inf')):
                    g[nxt]=score;previous[nxt]=node;heapq.heappush(queue,(score+mathdist(nxt,b),nxt))
        return None
    targets={'PCB12_J1':(-39.,-29.4,11.75),'HEAD_CAMERA_HDMI':(-67.,19.,75.),
             'SERVO_ROLL':(-25.8,-9.5,44.),'DISPLAY_POWER':(-18.,7.,26.)}
    routes={}
    for name,target in targets.items():
        path=astar(U.CLAMP,target,2.0 if name=="SERVO_ROLL" else 2.6)
        routes[name]=path
        print(name,path,flush=True)
    (HERE/'d107-internal-routes.json').write_text(json.dumps(dict(grid_mm=GRID,paths=routes),indent=1)+'\n')


def mathdist(a,b):return sum((a[k]-b[k])**2 for k in range(3))**.5


if __name__=='__main__':main()
