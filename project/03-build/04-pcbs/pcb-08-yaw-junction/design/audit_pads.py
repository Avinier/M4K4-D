"""Reproduce the pad-pattern audit independently of allowed graphics copies."""
import hashlib,json
from pathlib import Path
from layout_pcb08 import K,BOARD,HERE,LIB


def pads(n,rotation=0.):
    rows=[]
    for p in K.find_all(n,'pad'):
        at=K.find(p,'at');angle=((float(at[3]) if len(at)>3 else 0.)-rotation)%360
        # Circular pads have no meaningful orientation; rectangle symmetry180.
        angle=0. if p[3]=='circle' else angle%180
        def prop(key):
            v=K.find(p,key)
            if not v:return None
            return [round(float(x),5) if x.replace('.','',1).replace('-','',1).isdigit() else x for x in v[1:]]
        rows.append([p[1:4],[round(float(x),5) for x in at[1:3]],round(angle,5),
                     prop('size'),prop('drill'),prop('layers'),prop('roundrect_rratio')])
    return sorted(rows,key=repr)


def main():
    b=K.Board(BOARD);rows=[]
    for raw in b.blocks('footprint'):
        n=K.parse(raw);ref=next(p[2] for p in K.find_all(n,'property') if p[1]=='Reference')
        folder,name=n[1].split(':')
        library=(HERE.parents[1]/'lib/pcb08.pretty' if folder=='pcb08' else LIB/(folder+'.pretty'))/(name+'.kicad_mod')
        match=pads(n,b.fp(ref)['rot'])==pads(K.parse(library.read_text()))
        rows.append(dict(ref=ref,library=str(library),pads_match=match))
    out=dict(rows=rows,scope='Pad number/type/shape, local position/angle, size, drill, layers and roundrect ratio; rotation normalized; graphics/model differences remain library warnings.',
             board_sha256=hashlib.sha256(BOARD.read_bytes()).hexdigest(),passed=all(r['pads_match'] for r in rows))
    (HERE/'footprint-pad-audit.json').write_text(json.dumps(out,indent=2)+'\n')
    assert out['passed'],rows
    print('PASS',len(rows),'footprint pad patterns')


if __name__=='__main__':main()
