"""Emit Layout 02 per-part bounding boxes from the parametric model.

This is a Layout 02 logging artifact, not a Layout 03 change and not a
fabrication drawing. Neutral pose. Catalog STEP is not imported: camera and
servo rows use the same placed envelopes as the fit checkers.
"""
import json, sys, types
from pathlib import Path

# layout_model imports cadgen only for colour/catalog; catalog=False needs a stub.
if 'cadgen' not in sys.modules:
    cadgen = types.ModuleType('cadgen')
    def srgb(color, alpha=1):
        return color
    cadgen.srgb = srgb
    sys.modules['cadgen'] = cadgen
    step_scene = types.ModuleType('cadgen.step_scene')
    step_scene.import_step = lambda path: None
    sys.modules['cadgen.step_scene'] = step_scene

from build123d import CenterOf
import layout_model as m

HERE = Path(__file__).parent
PURCHASED = {
    'active_display_95_04x53_86',
    'display_module_1to1_envelope',
    'camera_module_3_wide_1to1',
    'C2_ESP32_S3_Zero_23_5x18_footprint',
    'roll_XC330_1to1_reference',
    'pitch_XC330_1to1_reference',
}


def r3(v):
    return [round(float(x), 3) for x in v]


def measure(shape):
    box = shape.bounding_box()
    lo, hi = list(box.min), list(box.max)
    size = [hi[i] - lo[i] for i in range(3)]
    geom = [(lo[i] + hi[i]) / 2 for i in range(3)]
    try:
        mass_centre = list(shape.center(CenterOf.MASS))
    except Exception:
        mass_centre = geom
    return dict(
        min_mm=r3(lo),
        max_mm=r3(hi),
        size_dxdydz_mm=r3(size),
        geometric_centre_mm=r3(geom),
        volume_centre_mm=r3(mass_centre),
    )


def classify(name, d):
    owner = d.get('owner') or ''
    if d.get('kind') == 'reserve' or 'reserve' in name:
        return 'reserve'
    if owner in ('M021a', 'M021-R') or '_M2_' in name or name.startswith(('front_M2', 'rear_M2')):
        return 'fastener'
    if name in PURCHASED:
        return 'purchased_1to1'
    if name.startswith('ear_') or name in (
        'front_bezel_integral_camera_crown',
        'main_octagonal_skin',
        'removable_octagonal_rear_cover',
        'window_opaque_mask_110mm',
        'window_clear_optical_area',
        'crown_status_light_diffuser',
    ):
        return 'skin_ears'
    if owner in ('M010', 'M010-P', 'M011-P', 'M011-Y', 'M012', 'M013-15-R', 'M013-15-P', 'M016-18-R', 'M016-18-P', 'M016-18-Y'):
        return 'mechanism'
    return 'authored'


def basis(name, kind):
    if name.startswith(('front_M2', 'rear_M2')) or '_M2_' in name:
        return 'E: modelled M2 button-head geometry; thread is a major-diameter cylinder; not a purchased kit drawing'
    if name in PURCHASED:
        return 'D: placed 1:1 envelope from the construction brief / manufacturer drawing or catalog outline; catalog STEP not re-imported here'
    if kind == 'reserve':
        return 'E: empty keep-out or trial hardware volume; not material'
    if kind == 'skin_ears':
        return 'E: authored PLA solid bounding box at 1.2 mm skin; reliefs included'
    return 'E: authored layout solid bounding box; trial if labelled trial'


parts = m.build_parts(catalog=False)
rows = []
for name, d in parts.items():
    kind = classify(name, d)
    row = dict(
        name=name,
        frame=d['frame'],
        owner=d.get('owner'),
        kind=kind,
        model_kind=d.get('kind'),
        basis=basis(name, kind),
        **measure(d['shape']),
    )
    rows.append(row)

assembly_lo = [min(r['min_mm'][i] for r in rows) for i in range(3)]
assembly_hi = [max(r['max_mm'][i] for r in rows) for i in range(3)]
result = dict(
    layout='02',
    pose='neutral',
    units='mm',
    frame='+X forward (face), +Y robot-left, +Z up; origin front/bottom centre of main head',
    method='CAD bounding boxes from layout_model.build_parts(catalog=False) at the current A0 datums. Not measured parts, not manufacturing drawings, not Layout 03 geometry.',
    axes=dict(
        roll_axis_point_mm=r3((0, m.ROLL_Y, m.ROLL_Z)),
        roll_axis_direction='+X',
        pitch_axis_point_mm=r3((m.PITCH_X, 0, m.PITCH_Z)),
        pitch_axis_direction='+Y',
        yaw_axis_point_mm=r3((m.PITCH_X, 0, -60)),
        yaw_axis_direction='+Z',
    ),
    envelope=dict(
        main_shell_HWD_mm=[m.MAIN_H, m.MAIN_W, m.MAIN_D],
        crown_inclusive_H_mm=m.CROWN_H,
        skin_thickness_mm=m.SKIN,
        ear_diameter_mm=2 * m.EAR_R,
        ear_centre_mm=r3((m.EAR_X, 66.5, m.EAR_Z)),
        display_board_Z_mm=[m.DISPLAY_BOTTOM, m.DISPLAY_BOTTOM + 68],
        camera_board_Z_mm=[m.CAMERA_BOTTOM, m.CAMERA_BOTTOM + 24],
        camera_display_vertical_gap_mm=round(m.CAMERA_BOTTOM - (m.DISPLAY_BOTTOM + 68), 3),
        LED_centre_mm=r3((-6, m.LED_Y, m.LED_Z)),
        roll_bearing_centres_X_mm=[-43, -65],
        roll_bearing_spacing_mm=22,
    ),
    yoke_derived=dict(
        pitch_axis_above_head_bottom_mm=round(m.PITCH_Z, 3),
        yoke_knee_Z_mm=-32,
        visible_yoke_below_head_bottom_mm=32,
        pitch_axis_to_knee_mm=round(m.PITCH_Z - (-32), 3),
        yaw_interface_Z_mm=-60,
        neck_allocation_mm=60,
        yoke_leg_Y_mm=[-55, 55],
        note='The ~45 mm from pitch axis to Z=0 is the A0/elevated-pivot segment. The 32 mm below Z=0 is the visible-neck/knee segment. Both are Layout 02 trial geometry.',
    ),
    assembly_bounds_mm=dict(
        min=r3(assembly_lo),
        max=r3(assembly_hi),
        size_dxdydz=r3([assembly_hi[i] - assembly_lo[i] for i in range(3)]),
    ),
    parts=rows,
    fastener_seats=dict(
        visible_M2_count=18,
        front_M2x10_YZ_mm=m.FRONT_SCREWS,
        rear_M2x6_YZ_mm=m.REAR_SCREWS,
        ear_cap_screws_per_ear=4,
        hidden_ear_mounts_per_ear=2,
    ),
    notes=[
        'Size is the axis-aligned bounding box, so rotated/octagonal/hollow parts read larger than a manufacturing stock size.',
        'Camera and XC330 rows here are the layout envelopes used by the fit checkers. Manufacturer STEP is used in the exported assembly with rigid transforms only.',
        'Receiving pilots are not approved PLA threads. Spindle, bearings, coupling and yoke section are trial.',
        'Refresh with: python write_dimensions.py from this directory.',
    ],
)

(HERE / 'dimensions.json').write_text(json.dumps(result, indent=2) + '\n')


def fmt_size(s):
    return ' × '.join(f'{v:.2f}'.rstrip('0').rstrip('.') for v in s)


def fmt_xyz(p):
    return ', '.join(f'{v:.2f}'.rstrip('0').rstrip('.') for v in p)


GROUPS = [
    ('purchased_1to1', 'Purchased / 1:1 envelopes'),
    ('skin_ears', 'Skin, window, ears'),
    ('mechanism', 'Mechanism and supports'),
    ('authored', 'Other authored solids'),
    ('reserve', 'Reserves and keep-outs'),
    ('fastener', 'Fasteners (modelled geometry)'),
]

lines = [
    '# Layout 02 dimensions',
    '',
    'Generated from [`write_dimensions.py`](write_dimensions.py) against the current parametric model. **Layout 02 logging only** — not a fabrication drawing, not a freeze, and not Layout 03 geometry.',
    '',
    '| Field | Value |',
    '|---|---|',
    f'| Pose | Neutral |',
    f'| Units | mm |',
    '| Frame | +X forward (face), +Y robot-left, +Z up; origin front/bottom centre |',
    f'| Assembly box | {fmt_size(result["assembly_bounds_mm"]["size_dxdydz"])} (X {result["assembly_bounds_mm"]["min"][0]:.1f}…{result["assembly_bounds_mm"]["max"][0]:.1f}, Y {result["assembly_bounds_mm"]["min"][1]:.1f}…{result["assembly_bounds_mm"]["max"][1]:.1f}, Z {result["assembly_bounds_mm"]["min"][2]:.1f}…{result["assembly_bounds_mm"]["max"][2]:.1f}) |',
    f'| Machine-readable | [dimensions.json](dimensions.json) |',
    '',
    'Mass and CoM stay in [mass-placement.json](mass-placement.json). Refresh both after geometry changes.',
    '',
    '## Datums',
    '',
    '| Datum | Point (X, Y, Z) | Direction |',
    '|---|---|---|',
    f'| Roll axis | {fmt_xyz(result["axes"]["roll_axis_point_mm"])} | +X |',
    f'| Pitch axis | {fmt_xyz(result["axes"]["pitch_axis_point_mm"])} | +Y |',
    f'| Yaw axis | {fmt_xyz(result["axes"]["yaw_axis_point_mm"])} | +Z |',
    '',
    '## Envelope constants',
    '',
    '| Item | Value |',
    '|---|---|',
    f'| Main shell H × W × D | {m.MAIN_H:.0f} × {m.MAIN_W:.0f} × {m.MAIN_D:.0f} |',
    f'| Crown-inclusive height | {m.CROWN_H:.0f} |',
    f'| Skin thickness | {m.SKIN} |',
    f'| Ear diameter / centre | Ø{2*m.EAR_R:.0f} at X {m.EAR_X:.0f}, Z {m.EAR_Z:.0f}, Y ±66.5 |',
    f'| Display board Z | {m.DISPLAY_BOTTOM:.0f}…{m.DISPLAY_BOTTOM+68:.0f} |',
    f'| Camera board Z | {m.CAMERA_BOTTOM:.0f}…{m.CAMERA_BOTTOM+24:.0f} |',
    f'| Camera–display vertical gap | {result["envelope"]["camera_display_vertical_gap_mm"]} |',
    f'| Roll bearing centres X | −43 and −65 (22 spacing) |',
    '',
    '## Yoke length (Layout 02 as modelled)',
    '',
    '| Segment | mm | Role |',
    '|---|---:|---|',
    f'| Pitch axis above head bottom | {result["yoke_derived"]["pitch_axis_above_head_bottom_mm"]} | A0 / elevated ear-pivot; do not shorten by dropping the axis |',
    f'| Visible yoke below head bottom | {result["yoke_derived"]["visible_yoke_below_head_bottom_mm"]} | Knee at Z −32; visible neck / look-up clearance |',
    f'| Pitch axis to knee | {result["yoke_derived"]["pitch_axis_to_knee_mm"]} | Structural leg length in this model |',
    f'| Yaw interface Z | {result["yoke_derived"]["yaw_interface_Z_mm"]} | 60 mm neck allocation |',
    '',
    'Yoke-leg length changes belong to [Layout 03](../layout-03-brief.md), not this file.',
    '',
]

for kind, title in GROUPS:
    group = [r for r in rows if r['kind'] == kind]
    if not group:
        continue
    lines += [
        f'## {title}',
        '',
        '| Part | Frame | Owner | Size (ΔX × ΔY × ΔZ) | Box min | Box max |',
        '|---|:---:|:---:|---|---|---|',
    ]
    for r in group:
        lines.append(
            f'| `{r["name"]}` | {r["frame"]} | {r["owner"] or "—"} | {fmt_size(r["size_dxdydz_mm"])} | {fmt_xyz(r["min_mm"])} | {fmt_xyz(r["max_mm"])} |'
        )
    lines.append('')

lines += [
    '## Fastener seats',
    '',
    'Eighteen visible M2 modelled: six front M2×10 at YZ '
    + '; '.join(f'({y}, {z})' for y, z in m.FRONT_SCREWS)
    + '. Four rear M2×6 at YZ '
    + '; '.join(f'({y}, {z})' for y, z in m.REAR_SCREWS)
    + '. Eight ear-cap M2×6 (four per ear at 45°/135°/225°/315° on a 25 mm radius). Four hidden ear-mount M2×6 (two per ear). Heads 3.5 mm diameter × 1.3 mm; 4.2 mm wells. Pilots are layout geometry, not approved PLA threads.',
    '',
    '## Limits',
    '',
]
for n in result['notes']:
    lines.append(f'- {n}')
lines.append('')

(HERE / 'dimensions.md').write_text('\n'.join(lines))
print(json.dumps(dict(parts=len(rows), assembly=result['assembly_bounds_mm'], axes=result['axes']), indent=2))
