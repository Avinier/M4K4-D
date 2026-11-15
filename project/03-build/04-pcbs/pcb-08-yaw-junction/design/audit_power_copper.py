"""Audit saved PCB08 power fills and estimate their sheet resistance.

Finite-difference resistor sheet, not a thermal solution. It excludes barrel,
solder and contact resistance. PO requires >=35um finished inner copper;
17.5um is an adverse comparison, never an acceptable substitute.
"""
import json
import hashlib
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from shapely import contains_xy
from shapely.geometry import Polygon,Point
from shapely.ops import unary_union
from layout_pcb08 import K,BOARD,HERE


def sheet_squares(geometry,source,target,step=.1):
    # Solid-connect PTH electrodes; the pad interiors are equipotential.
    g=unary_union([geometry,Point(source).buffer(.75),Point(target).buffer(.75)]).buffer(0)
    x0,y0,x1,y1=g.bounds
    xx,yy=np.meshgrid(np.arange(x0+step/2,x1,step),np.arange(y0+step/2,y1,step))
    mask=contains_xy(g,xx,yy);labels,_=ndimage.label(mask)
    s=((xx-source[0])**2+(yy-source[1])**2<.65**2)&mask
    t=((xx-target[0])**2+(yy-target[1])**2<.65**2)&mask
    component=int(np.bincount(labels[s]).argmax());assert component and np.any(t&(labels==component))
    mask&=labels==component;s&=mask;t&=mask
    fixed=s|t;unknown=mask&~fixed;index=np.full(mask.shape,-1,int);index[unknown]=np.arange(unknown.sum())
    degree=np.zeros(mask.shape);rhs=np.zeros(mask.shape);rr=[];cc=[]
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        neighbour=np.roll(mask,(dy,dx),(0,1));ns=np.roll(s,(dy,dx),(0,1));ni=np.roll(index,(dy,dx),(0,1))
        if dy==1:neighbour[0]=False
        if dy==-1:neighbour[-1]=False
        if dx==1:neighbour[:,0]=False
        if dx==-1:neighbour[:,-1]=False
        degree+=neighbour;rhs+=ns
        a=unknown&neighbour&(ni>=0);rr.extend(index[a]);cc.extend(ni[a])
    matrix=sparse.diags(degree[unknown])-sparse.coo_matrix((np.ones(len(rr)),(rr,cc)),shape=(unknown.sum(),unknown.sum())).tocsr()
    v=np.zeros(mask.shape);v[s]=1;v[unknown]=spsolve(matrix,rhs[unknown])
    amps=0.
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        nm=np.roll(mask,(dy,dx),(0,1));nv=np.roll(v,(dy,dx),(0,1));ns=np.roll(s,(dy,dx),(0,1))
        edge=s&nm&~ns;amps+=float((1-nv[edge]).sum())
    return 1/amps


def main():
    b=K.Board(BOARD);rows=[]
    for name,layer,net,pin in [('HEAD_POSITIVE_FILL','In1.Cu','/+6V3_HEAD_PR','1'),('HEAD_RETURN_FILL','In2.Cu','/GND_HEAD','4')]:
        zone=next(K.parse(raw) for raw in b.blocks('zone') if K.find(K.parse(raw),'name')==['name',name])
        assert K.find(zone,'net')==['net',net] and K.find(zone,'layer')==['layer',layer]
        assert K.find(zone,'connect_pads')[1]=='yes','power thermals are not allowed'
        fill=unary_union([Polygon([(float(p[1]),float(p[2])) for p in K.find(fp,'pts')[1:]]).buffer(0)
                          for fp in K.find_all(zone,'filled_polygon')])
        source=b.pad('J1',pin)['at'];target=b.pad('J3',pin)['at']
        assert fill.area>=400,(name,fill.area)
        squares=sheet_squares(fill,source,target)
        scenarios=[]
        for um in (35.,17.5):
            resistance=squares*1.724e-8/(um*1e-6)*(1+.00393*40)
            scenarios.append(dict(copper_um=um,resistance_at60C_ohm=resistance,drop_at2_4A_V=resistance*2.4,joule_heat_at2_4A_W=resistance*2.4**2,approved_copper=um>=35))
        rows.append(dict(name=name,net=net,layer=layer,filled_area_mm2=fill.area,solid_pad_connection=True,sheet_squares=squares,grid_mm=.1,scenarios=scenarios))
    width={net:min(float(K.find(K.parse(s),'width')[1]) for s in b.blocks('segment') if K.find(K.parse(s),'net')==['net',net] and K.find(K.parse(s),'layer')==['layer',layer])
           for net,layer in [('/+11V1_YAW','B.Cu'),('/GND_SIG','F.Cu')]}
    # GND_SIG includes low-current0.3/0.2mm spurs. Check the high-current J5-J6
    # chain as eight wide segments; independent route-end connectivity
    # remains the KiCad DRC/net audit.
    yaw_return=[K.parse(s) for s in b.blocks('segment') if K.find(K.parse(s),'net')==['net','/GND_SIG'] and float(K.find(K.parse(s),'width')[1])>=1.5]
    assert width['/+11V1_YAW']>=1.5 and len(yaw_return)>=8
    stack=K.find(K.parse(b.blocks('setup')[0]),'stackup')
    for layer in ('In1.Cu','In2.Cu'):
        record=next(x for x in K.find_all(stack,'layer') if x[1]==layer)
        assert float(K.find(record,'thickness')[1])>=.035
    out=dict(result='PASS',board_sha256=hashlib.sha256(BOARD.read_bytes()).hexdigest(),head_power=rows,
             yaw_supply_min_width_mm=width['/+11V1_YAW'],yaw_return_wide_segments=len(yaw_return),yaw_return_width_mm=1.5,
             minimum_finished_inner_copper_um=35,half_copper_substitution_permitted=False,
             limitations='Resistor sheet estimate only; no temperature prediction. Prototype load/temperature test and fab written stack-up acceptance remain required.')
    (HERE/'power-copper-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
