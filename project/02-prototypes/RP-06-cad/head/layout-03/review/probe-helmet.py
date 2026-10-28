"""Layout 03 exhaustive cross-frame sampling and targeted physical requirements."""
import json,itertools,sys,hashlib
from pathlib import Path
from build123d import *
import layout_model as m
from harness import routes
from optics import cone
from inspection_scene import posed,group_for
HERE=Path(__file__).resolve().parents[1]
inputs={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ['layout_model.py','details.py','layout_axes.py','harness.py','optics.py']}
p=m.build_parts(catalog=False)
def overlap(a,b):
    aa,bb=a.bounding_box(),b.bounding_box()
    if any(tuple(aa.max)[i]<=tuple(bb.min)[i]+1e-6 or tuple(bb.max)[i]<=tuple(aa.min)[i]+1e-6 for i in range(3)):return 0.
    return sum(max(0,s.volume) for s in m.pieces(a.intersect(b)))
physical={n:d for n,d in p.items() if d['kind']=='physical' and group_for(n,d)!='fasteners'}
valid={n:dict(valid=d['shape'].is_valid,solids=len(d['shape'].solids()),volume=d['shape'].volume) for n,d in p.items()}
intended={frozenset(['pitch_XC330_1to1_reference','pitch_trunnion_49'])}
pairs=[(a,b) for a,b in itertools.combinations(physical,2) if physical[a]['frame']!=physical[b]['frame'] and frozenset([a,b]) not in intended]
static=[]
for a,b in itertools.combinations(physical,2):
    if physical[a]['frame']==physical[b]['frame']:
        v=overlap(p[a]['shape'],p[b]['shape'])
        if v>1e-4:static.append(dict(a=a,b=b,volume_mm3=v))
h,gaps=routes();jackets={n:d for n,d in h.items() if d['kind']=='jacket'}
prior=None
if '--service-only' in sys.argv:
    prior=json.loads((HERE/'revision-checks.json').read_text())
    assert prior['source_sha256']==inputs and prior['axes']==m.AXES
    assert prior['poses']==56 and not prior['motion_hits'] and not prior['harness_pinches']
    (HERE/'review/motion-before-service-path-repair.json').write_text(json.dumps(prior,indent=2)+'\n')
rolls=[-18];pitches=[-22]
if '--neutral' in sys.argv:rolls=[0];pitches=[0]
if prior:rolls=[];pitches=[]
hits=prior['motion_hits'] if prior else [];pinches=prior['harness_pinches'] if prior else []
for r,q in itertools.product(rolls,pitches):
    shapes={n:posed(d['shape'],d['frame'],r,q,0) for n,d in physical.items()}
    for a,b in pairs:
        v=overlap(shapes[a],shapes[b])
        if v>1e-4:hits.append(dict(roll=r,pitch=q,a=a,b=b,volume_mm3=round(v,5)))
    for n,d in jackets.items():
        s=posed(d['shape'],d['frame'],r,q,0)
        for a,t in shapes.items():
            v=overlap(s,t)
            if v>1e-4:pinches.append(dict(roll=r,pitch=q,branch=n,part=a,volume_mm3=round(v,5)))
    print(f'pose {r:+}/{q:+}: mechanism hits {len(hits)}, jacket hits {len(pinches)}',flush=True)

print(json.dumps(dict(hits=hits,pinches=pinches,static=static),indent=2))

for hit in hits:
 v=shapes[hit["a"]].intersect(shapes[hit["b"]]);print("hit bounds",hit, v.bounding_box())
