"""One dimension source for the log and annotation construction geometry."""
import json
from pathlib import Path

def measure(shape):
    box=shape.bounding_box();lo=list(box.min);hi=list(box.max)
    return dict(min_mm=lo,max_mm=hi,size_dxdydz_mm=[hi[i]-lo[i] for i in range(3)],geometric_centre_mm=[(hi[i]+lo[i])/2 for i in range(3)])

def rows_for(parts):
    return [dict(name=n,frame=d['frame'],owner=d['owner'],kind=d['kind'],**measure(d['shape'])) for n,d in parts.items()]

def write(parts=None):
    import layout_model as m
    if parts is None:parts=m.build_parts(catalog=True)
    rows=rows_for(parts);physical=[r for r in rows if r['kind']=='physical']
    lo=[min(r['min_mm'][i] for r in physical) for i in range(3)];hi=[max(r['max_mm'][i] for r in physical) for i in range(3)]
    result=dict(layout='03',units='mm',frame='+X forward,+Y left,+Z up; origin front/bottom centre',pose='neutral',axes=m.AXES,parts=rows,physical_bounds=dict(min=lo,max=hi,size=[hi[i]-lo[i] for i in range(3)]),camera_display_gap_mm=m.CAMERA_BOTTOM-74,crown_height_mm=m.CROWN_H,yoke=dict(visible_below_head_mm=32,pitch_to_knee_mm=m.PITCH_Z+32,yaw_interface_z_mm=-60),note='AABB centres, not centres of mass. Catalog camera/servo use their actual placed manufacturer solids in this log. Annotation geometry uses this same measure function on the actual displayed part.')
    here=Path(__file__).parent;(here/'dimensions.json').write_text(json.dumps(result,indent=2)+'\n')
    fmt=lambda v:' × '.join(f'{x:.3f}' for x in v)
    lines=['# Layout 03 dimensions','',result['frame'],'',f"Physical envelope ΔX × ΔY × ΔZ: {fmt(result['physical_bounds']['size'])} mm (includes 60 mm neck). Crown {m.CROWN_H:g} mm; camera/display gap {m.CAMERA_BOTTOM-74:g} mm. Rear section {m.HELMET_REAR_WIDTH:g} × {m.HELMET_REAR_TOP-m.HELMET_REAR_BOTTOM:g} mm (Z{m.HELMET_REAR_BOTTOM:g}…{m.HELMET_REAR_TOP:g}); full face/ears section unchanged.",'',f'Visible yoke 32 mm; pitch to knee {m.PITCH_Z+32:.3f} mm. A0: `{m.AXES}`.','', '| Named component | Frame | Centre global XYZ (mm) | ΔX × ΔY × ΔZ (mm) |','|---|:---:|---|---|']
    for r in rows:lines.append(f"| `{r['name']}` | {r['frame']} | {fmt(r['geometric_centre_mm'])} | {fmt(r['size_dxdydz_mm'])} |")
    lines+=['','Generated from source. Nominal trial fits; no manufacturing drawing or freeze.']
    (here/'dimensions.md').write_text('\n'.join(lines)+'\n');return result
if __name__=='__main__':
    r=write();print(json.dumps({k:v for k,v in r.items() if k!='parts'},indent=2))
