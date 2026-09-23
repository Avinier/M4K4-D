"""Run the matching plugin's baseline, authored-solid and catalog validation."""
import json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
CLI=Path('/Users/avinier/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts')
target=HERE/'head-layout.step.py'
a=json.loads((HERE/'__cadgen__/models/head-layout.step.py/assembly.json').read_text())
authored=[o['id'] for o in a['occurrences'] if not o['name'].startswith(('camera-module-3-wide_solid_','xc330_solid_'))]
commands=[
 ('refs-final.json',['refs',str(target),'--facts','--planes','--positioning']),
 ('validate-authored.json',['validate',str(target),'--refs',','.join(authored)]),
 ('validate-all-topology.json',['validate',str(target),'--skip-self-intersection']),
 ('bearing-spacing.json',['measure',str(target),'--from','#roll_bearing_1_16x6_reserve','--to','#roll_bearing_2_16x6_reserve','--axis','x']),
]
for filename,args in commands:
    result=subprocess.run(['rtk','proxy',sys.executable,str(CLI/'inspect'),*args],capture_output=True,text=True)
    if result.stderr:print(result.stderr,file=sys.stderr,end='')
    data=json.loads(result.stdout)
    # Publish complete JSON atomically so readers never see a half-written report.
    report=HERE/'review'/filename
    temporary=report.with_suffix('.json.tmp')
    temporary.write_text(result.stdout)
    temporary.replace(report)
    print(filename,'exit',result.returncode,'ok',data.get('ok'),'keys',list(data),flush=True)
    if result.returncode:raise SystemExit(result.returncode)
    if data.get('ok') is not True:raise SystemExit(1)
print('Authored occurrences fully checked:',len(authored),flush=True)
