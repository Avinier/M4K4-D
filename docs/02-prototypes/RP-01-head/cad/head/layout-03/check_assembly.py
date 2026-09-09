"""Publish neutral/catalog checks from the final revision and dimensions evidence.

Run check_revision.py and write_dimensions.py first. This does not substitute
for those geometric checks and refuses stale model evidence.
"""
import json,hashlib
from pathlib import Path
HERE=Path(__file__).parent
r=json.loads((HERE/'revision-checks.json').read_text())
d=json.loads((HERE/'dimensions.json').read_text())
import layout_axes
assert d['axes']==r['axes']==layout_axes.AXES
assert all(hashlib.sha256((HERE/n).read_bytes()).hexdigest()==sha for n,sha in r['source_sha256'].items())
out=dict(same_frame_non_fastener_intersections=r['same_frame_hits'],C2_service_hits=r['C2_service_hits'],authored_positive_valid_solids=r['solids'],checks=dict(camera_display_gap_mm=d['camera_display_gap_mm'],crown_inclusive_height_mm=d['crown_height_mm'],physical_bounds_mm=d['physical_bounds'],roll_bearing_spacing_mm=22),evidence='Source BREP checks from final revision-checks.json; actual imported bounds in dimensions.json; full imported topology checked separately by validate_geometry.py.',passed=r['passed'])
(HERE/'assembly-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print('Neutral/package report:',out['passed'])
assert out['passed']
