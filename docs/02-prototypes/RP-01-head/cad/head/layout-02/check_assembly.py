"""Neutral assembly fit, catalog integrity and specification checks."""
import json,itertools
from pathlib import Path
from build123d import CenterOf
import layout_model as m
HERE=Path(__file__).parent
p=m.build_parts(catalog=False)
def volume_intersection(x,y):
    a,b=x.bounding_box(),y.bounding_box()
    if any(tuple(a.max)[i]<=tuple(b.min)[i]+1e-6 or tuple(b.max)[i]<=tuple(a.min)[i]+1e-6 for i in range(3)):return 0.
    return sum(max(0,c.volume) for c in m.pieces(x.intersect(y)))
names=[n for n,d in p.items() if d['kind']=='physical' and not (d['owner'] or '').startswith('M021')]
hits=[]
for a,b in itertools.combinations(names,2):
    if p[a]['frame']!=p[b]['frame']:continue
    v=volume_intersection(p[a]['shape'],p[b]['shape'])
    if v>1e-4:hits.append(dict(a=a,b=b,volume_mm3=v))
service=p['C2_USB_C_withdrawal_BOOT_RESET_service_reserve']['shape']
service_hits=[]
for n in names:
    v=volume_intersection(service,p[n]['shape'])
    if v>1e-4:service_hits.append(dict(part=n,volume_mm3=v))
camera_gap=m.CAMERA_BOTTOM-(m.DISPLAY_BOTTOM+68)
catalog=[]
for filename in ['camera-module-3-wide.step','xc330.stp']:
    raw=m.import_step(str(m.CATALOG/filename));solids=list(raw.solids())
    bad=[i for i,s in enumerate(solids) if not s.is_valid or s.volume<=1e-8]
    clean=m.clean_catalog(m.CATALOG/filename)
    catalog.append(dict(file='../layout-01/parts/'+filename,raw_solid_count=len(solids),retained_solid_count=len(clean.solids()),discarded_invalid_solid_indices=bad,raw_bounds=dict(min=list(raw.bounding_box().min),max=list(raw.bounding_box().max)),retained_bounds=dict(min=list(clean.bounding_box().min),max=list(clean.bounding_box().max)),note='Only closed positive-volume solids are used; imported non-solid annotation/open-surface geometry is excluded. All transforms rigid, scale 1.'))
single_solid={n:len(d['shape'].solids())==1 and d['shape'].is_valid for n,d in p.items()}
result=dict(same_frame_non_fastener_intersections=hits,C2_top_exit_service_reserve_neutral_hits=service_hits,authored_single_valid_solid=single_solid,catalog=catalog,checks=dict(main_shell_HWD_mm=[86,130,115],crown_inclusive_HWD_mm=[102,150,115],camera_board_to_display_vertical_gap_mm=camera_gap,display_active_rect_corner_margin_to_aperture_diagonal_mm=(1.98+2.07-3)/2**.5,roll_bearing_centres_mm=[-43,-65],roll_bearing_spacing_mm=22,ear_diameter_mm=60,LED_package_above_main_roof_mm=m.LED_Z-2.5-m.MAIN_H),notes=['Screw major cylinders intentionally occupy pilot-hole thread material; fasteners excluded from neutral overlap pairs.','Service volume is for stationary maintenance with rear cover removed; it is not a moving USB cable or sealed recovery connector model.','Camera bracket fasteners, C2 clips/antenna clearance, servo mount holes, final inserts, shaft retention, optics and cable paths remain fabrication gates.'])
(HERE/'assembly-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='authored_single_valid_solid'},indent=2))
print('single solids',all(single_solid.values()))
