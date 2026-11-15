"""Regenerate D-107 95 mm centreline candidates from the retained study cloud.

This generates routing input, not a fit certificate. check_d107_neck.py tests
these candidates against the actual edited parts, including every endpoint.
"""
import hashlib
import json
import numpy as np
from pathlib import Path
import d107_umbilical as U
from study_umbilical_span import Head, neck_trees, run_neck, pose_order, summarise
HERE=Path(__file__).resolve().parent
NPZ=HERE/"__cadgen__/umbilical-study.npz"
def main():
    data=np.load(NPZ);head=Head(data)
    poses=pose_order((0.,),(-25.,-17.,-8.5,0.,8.5,17.,26.,34.5,43.),(-21.,-10.5,0.,10.5,21.))
    # Actual opening relative to yaw axis, with the collar outside it.
    trees=neck_trees(data,head,opening=(U.OPENING[0]+42.4,U.OPENING[1]+42.4,*U.OPENING[2:]))
    rows,shapes=run_neck(head,trees,-8.,95.,2000.,3.5,poses,keep_shapes=True,anchor=np.asarray(U.CLAMP))
    out=dict(clamp=list(U.CLAMP),opening=list(U.OPENING),length_mm=95.,radius_mm=3.5,cloud_sha256=hashlib.sha256(NPZ.read_bytes()).hexdigest(),
             note="geometric route candidates; EI and load are estimates; solver residual retained, no equilibrium certification",
             summary=summarise(rows),rows=rows,
             routes=[dict(pitch=q,roll=r,points=np.round(x,6).tolist()) for (y,q,r),x in shapes.items()])
    (HERE/"d107-routes.json").write_text(json.dumps(out,indent=1)+"\n")
    print(json.dumps(out["summary"]),flush=True)
if __name__=="__main__":main()
