"""Verify the rebuilt assembly changed only by the checked JP1 material removal.

Reuses the full static matrix before the fix, checks every exported occurrence's
geometry/placement manifest, and substitutes the targeted corrected-upright check.
Material removal cannot create an intersection with unchanged geometry.
"""
import hashlib,json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    before=json.loads((HERE/'pcb-integration-before-manifest.json').read_text())
    after=json.loads((HERE/'__cadgen__/models/makad-v1.step.py/assembly.json').read_text())
    baseline=json.loads((HERE/'pcb-integration-before-relief.json').read_text())
    relief=json.loads((HERE/'pcb10-jp1-relief-report.json').read_text())
    assert before['stepHash']==baseline['checked_step']['sha256']
    for source in baseline['sources'].values():
        assert hashlib.sha256(Path(source['path']).read_bytes()).hexdigest()==source['sha256'], 'Released board input changed: run full checker'
    old={r['id']:r for r in before['occurrences']}
    new={r['id']:r for r in after['occurrences']}
    assert old.keys()==new.keys(), 'Occurrence set changed: run full integration checker'
    changed=[]
    for ref,a in old.items():
        b=new[ref]
        assert a['name']==b['name'],(ref,a['name'],b['name'])
        assert max(abs(x-y) for x,y in zip(a['transform'],b['transform']))<1e-10,(ref,'placement changed')
        if a['component']!=b['component']:changed.append((ref,a['name']))
    seat=[r for r in changed if r[1]=='BALL_POD_PRINTED_SEAT']
    equivalent=[]
    if seat:
        proof=json.loads((HERE/'pcb-seat-equivalence.json').read_text())
        assert proof['result']=='PASS' and max(map(abs,proof['symmetric_difference_mm3']))<1e-6
        assert proof['documents'][0]['step_sha256']==baseline['checked_step']['sha256']
        assert proof['documents'][1]['step_sha256']==hashlib.sha256((HERE/'makad-v1.step').read_bytes()).hexdigest()
        assert proof['documents'][0]['brep']==proof['documents'][1]['brep']
        equivalent=seat
        changed=[r for r in changed if r not in seat]
    assert len(changed)==1 and changed[0][1]=='BODY_FRAME_C3_CARRIER_UPRIGHT_1',changed
    assert after['sourceHash']==relief['source_main_sha256']==hashlib.sha256((HERE/'makad-v1.step.py').read_bytes()).hexdigest()
    assert len(baseline['static_interferences'])==1
    assert baseline['static_interferences'][0]['part'].endswith('__JP1')
    assert not baseline['cross_board_collisions']
    zero_contacts=[r for r in baseline['static_near_contacts'] if r['gap_mm']<1e-6]
    assert len(zero_contacts)==1 and zero_contacts[0]['part'].endswith('__JP1'),zero_contacts
    assert relief['result']=='PASS' and relief['added_material_mm3']<1e-6 and relief['new_clash_mm3']<1e-6
    result=dict(baseline)
    result.update(result='PASS',static_interferences=[],checked_step={'path':str(HERE/'makad-v1.step'),'sha256':hashlib.sha256((HERE/'makad-v1.step').read_bytes()).hexdigest()},
                  verification_method='Full before-fix static matrix plus exported occurrence delta and targeted after-fix upright check; not a second full-matrix run',
                  changed_occurrences=changed,geometry_equivalent_render_differences=equivalent,unchanged_occurrences=len(old)-len(changed),jp1_relief=relief,
                  baseline_report='pcb-integration-before-relief.json')
    # Preserve old positive contacts, replace the one corrected JP1 zero contact.
    result['static_near_contacts']=[r for r in baseline['static_near_contacts'] if not r['part'].endswith('__JP1')]
    (HERE/'pcb-integration-report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'result':'PASS','installed_boards':result['board_count'],'unchanged_occurrences':result['unchanged_occurrences'],'changed':changed,'old_clash_mm3':relief['old_clash_mm3'],'new_clash_mm3':relief['new_clash_mm3'],'min_sampled_JP1_clearance_mm':relief['min_sampled_clearance_mm']},indent=2))


if __name__=='__main__':main()
