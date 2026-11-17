"""D-107 camera harness qualification gaps missed by clearance checks.

Run with the legacy CAD Python from this directory. Five nominal geometry
screens are distinct from received-connector, strain-relief and electrical
validation of a modified HDMI cable.
"""

import json
import math
from pathlib import Path

from build123d import Compound, export_step
import d107_umbilical as U
import head_harness as H


def route_length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def main():
    head_plug = U.camera_parts(U.HEAD_BOARD)['HDMI_MATED_PLUG_E'].bounding_box()
    body_plug = U.camera_parts(U.BODY_BOARD)['HDMI_MATED_PLUG_E'].bounding_box()
    head_path = H.lead_paths()['HEAD_CAMERA_HDMI']
    head_before, head_end = head_path[-2:]
    body_start, body_after = H.BODY_HDMI[:2]
    head_route = route_length(H.HEAD_FFC_POINTS)
    body_route = route_length(H.BODY_FFC_POINTS)
    body_undressed = H.BODY_FFC_LENGTH - body_route - H.FFC_INSERTION_ALLOWANCE - H.FFC_SERVICE_ALLOWANCE

    checks = [
        {
            'name': 'head_hdmi_cable_approaches_from_plug_rear',
            'pass': head_before[1] > head_plug.max.Y and head_end[1] < head_plug.max.Y
                    and head_before[2] >= head_plug.min.Z and head_before[2] <= head_plug.max.Z,
            'head_plug_rear_y_mm': head_plug.max.Y,
            'preterminal_xyz_mm': head_before,
            'terminal_xyz_mm': head_end,
            'finding': 'Head lead must approach the +Y rear face along -Y with boot room.',
        },
        {
            'name': 'body_hdmi_cable_leaves_plug_rear',
            'pass': abs(body_start[1] - body_plug.max.Y) < 0.01 and body_after[1] > body_start[1],
            'body_plug_rear_y_mm': body_plug.max.Y,
            'first_two_xyz_mm': [body_start, body_after],
        },
        {
            'name': 'head_15way_envelope_is_one_continuous_part',
            'pass': len(H.head_ffc()) == 1,
            'separate_solid_count': len(H.head_ffc()),
            'finding': 'A continuous ribbon solid is required through all bends.',
        },
        {
            'name': 'body_150mm_ribbon_excess_is_dressed_in_model',
            'pass': body_undressed <= 5.0,
            'modeled_centerline_mm': body_route,
            'purchased_length_mm': H.BODY_FFC_LENGTH,
            'insertion_and_service_allowance_mm': H.FFC_INSERTION_ALLOWANCE + H.FFC_SERVICE_ALLOWANCE,
            'undressed_excess_mm': body_undressed,
            'finding': 'The 150 mm stock length must fit its fold and insertion allowance.',
        },
        {
            'name': 'head_150mm_ribbon_length_reaches_nominal_route',
            'pass': H.HEAD_FFC_LENGTH >= head_route + H.FFC_INSERTION_ALLOWANCE + H.FFC_SERVICE_ALLOWANCE,
            'modeled_centerline_mm': head_route,
            'stock_length_mm': H.HEAD_FFC_LENGTH,
            'reserve_after_allowances_mm': H.HEAD_FFC_LENGTH - head_route - H.FFC_INSERTION_ALLOWANCE - H.FFC_SERVICE_ALLOWANCE,
        },
    ]
    report = {
        'qualified': all(item['pass'] for item in checks),
        'passed': sum(item['pass'] for item in checks),
        'total': len(checks),
        'checks': checks,
        'physical_gates': [
            'Received B0091 connector positions/contact faces and board retention',
            'Actual HDMI plug/boot through finished bore and intact-cable flex performance',
            'Camera stream at all head poses after any HDMI jacket modification',
            'Received 15-way and 15-to-22 ribbon fold, contact polarity and slack dress',
        ],
    }
    focus = []
    for name, shape in U.camera_parts(U.HEAD_BOARD).items():
        shape.label = 'B0091_HEAD_' + name
        focus.append(shape)
    lead = U.tube(head_path, 1.8)
    lead.label = 'W47_LEAD_HEAD_CAMERA_HDMI'
    focus.append(lead)
    for i, shape in enumerate(H.head_ffc(), 1):
        shape.label = f'HEAD_FFC_SEGMENT_{i}'
        focus.append(shape)
    export_step(Compound(label='D107 head camera audit', children=focus), 'd107-head-camera-audit.step')
    Path('check_d107_camera_chain-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f"check_d107_camera_chain: {report['passed']}/{report['total']} pass; qualified={report['qualified']}")
    for item in checks:
        if not item['pass']:
            print('FAIL', item['name'], '-', item['finding'])
    raise SystemExit(0 if report['qualified'] else 1)


if __name__ == '__main__':
    main()
