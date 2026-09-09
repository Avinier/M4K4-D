// Exercise the actual installed viewer feature resolver, not a mock selector parser.
import fs from 'node:fs';
import {fileURLToPath,pathToFileURL} from 'node:url';
import path from 'node:path';
import {normalizeStepModuleDefinition,resolveStepModuleFeatures,stepModuleTargetPartIds} from '/Users/avinier/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad-viewer/scripts/viewer/packages/cadjs/src/common/stepModule.js';
const here=path.dirname(fileURLToPath(import.meta.url));
const raw=JSON.parse(fs.readFileSync(path.join(here,'__cadgen__/models/head-layout.step.py/assembly.json')));
const expectedAxes=JSON.parse(fs.readFileSync(path.join(here,'axes.json')));
const parameterText=fs.readFileSync(path.join(here,'head-layout.params.js'),'utf8');
const encodedAxes=JSON.parse(parameterText.match(/const axes=(.*);/)[1]);
if(JSON.stringify(encodedAxes)!==JSON.stringify(expectedAxes))throw Error('Viewer axes are stale');
const module=(await import(pathToFileURL(path.join(here,'head-layout.params.js')))).default;
const definition=normalizeStepModuleDefinition(module);
const meshData={parts:raw.occurrences.map(o=>({...o,occurrenceId:o.id}))};
const features=resolveStepModuleFeatures(definition,{meshData});
for(const [id,f] of Object.entries(features))if(f.missing||!f.partIds.length)throw Error('Unresolved feature '+id);
const defaults=Object.fromEntries(Object.entries(module.manifest.parameters).map(([id,d])=>[id,d.default]));
function evaluate(params){
 const visible=new Map(),transforms=new Map();
 module.update({params:{...defaults,...params},effects:{
  transform(target,spec){for(const id of stepModuleTargetPartIds(target,features,meshData))transforms.set(id,(transforms.get(id)||0)+1);},
  visible(target,value){for(const id of stepModuleTargetPartIds(target,features,meshData))visible.set(id,value);}
 }});
 return {visible,transforms};
}
for(let bits=0;bits<16;bits++){
 const params=Object.fromEntries(['physical','physics','harness','annotations'].map((s,i)=>['show_'+s,Boolean(bits&(1<<i))]));
 const result=evaluate(params);
 for(const key of ['physical','physics','harness','annotations']){
  for(const id of features[key].partIds)if(result.visible.get(id)!==params['show_'+key])throw Error('Master visibility mismatch '+key+' '+id);
 }
}
for(const values of [{},{roll_deg:18,pitch_deg:-22,yaw_deg:55},{roll_deg:-18,pitch_deg:40,yaw_deg:-55}]){
 const result=evaluate(values);
 for(const key of ['frame_R','frame_P','frame_Y'])for(const id of features[key].partIds)if(result.transforms.get(id)!==1)throw Error('Missing or doubled frame transform '+id);
}
const result={passed:true,occurrences:raw.occurrences.length,features:Object.fromEntries(Object.entries(features).map(([k,f])=>[k,f.partIds.length])),visibility_combinations:16,poses:3,defaults};
fs.writeFileSync(path.join(here,'review/viewer-checks.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
