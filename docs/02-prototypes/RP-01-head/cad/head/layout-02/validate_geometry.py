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
 ('bearing-spacing.json',['measure',str(target),'--from','#o1.2.1','--to','#o1.2.2','--axis','x']),
]
for filename,args in commands:
    with (HERE/'review'/filename).open('w') as f:
        result=subprocess.run([sys.executable,str(CLI/'inspect'),*args],stdout=f)
    data=json.loads((HERE/'review'/filename).read_text())
    print(filename,'exit',result.returncode,'ok',data.get('ok'),'keys',list(data),flush=True)
    if result.returncode:raise SystemExit(result.returncode)
print('Authored occurrences fully checked:',len(authored),flush=True)
