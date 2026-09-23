// Check body-chassis.params.js against the installed viewer's own feature
// resolver and transform composition (stepModuleEffects.js), then verify the
// pivots kinematically: fixed points stay fixed, gears mesh, wheels roll.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const VIEWER = path.join(process.env.HOME, '.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad-viewer/scripts/viewer/packages/cadjs/src/common');
const {normalizeStepModuleDefinition, resolveStepModuleFeatures} = await import(path.join(VIEWER, 'stepModule.js'));
const {createStepModuleEffectsApi} = await import(path.join(VIEWER, 'stepModuleEffects.js'));

// Column-major Matrix4 with the subset of the three.js API the viewer uses.
class Matrix4 {
  constructor() { this.elements = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]; }
  set(...r) { const e = this.elements; for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) e[j * 4 + i] = r[i * 4 + j]; return this; }
  identity() { return this.set(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1); }
  clone() { const m = new Matrix4(); m.elements = [...this.elements]; return m; }
  static mul(a, b) {
    const m = new Matrix4(), ae = a.elements, be = b.elements;
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
      let s = 0; for (let k = 0; k < 4; k++) s += ae[k * 4 + i] * be[j * 4 + k];
      m.elements[j * 4 + i] = s;
    }
    return m;
  }
  multiply(b) { this.elements = Matrix4.mul(this, b).elements; return this; }
  premultiply(a) { this.elements = Matrix4.mul(a, this).elements; return this; }
  makeTranslation(x, y, z) { return this.set(1, 0, 0, x, 0, 1, 0, y, 0, 0, 1, z, 0, 0, 0, 1); }
  makeScale(x, y, z) { return this.set(x, 0, 0, 0, 0, y, 0, 0, 0, 0, z, 0, 0, 0, 0, 1); }
  makeRotationAxis(v, a) {
    const c = Math.cos(a), s = Math.sin(a), t = 1 - c, {x, y, z} = v;
    return this.set(t * x * x + c, t * x * y - s * z, t * x * z + s * y, 0,
      t * x * y + s * z, t * y * y + c, t * y * z - s * x, 0,
      t * x * z - s * y, t * y * z + s * x, t * z * z + c, 0, 0, 0, 0, 1);
  }
  apply([x, y, z]) { const e = this.elements; return [0, 1, 2].map(i => e[i] * x + e[4 + i] * y + e[8 + i] * z + e[12 + i]); }
}
class Vector3 {
  constructor(x = 0, y = 0, z = 0) { Object.assign(this, {x, y, z}); }
  set(x, y, z) { Object.assign(this, {x, y, z}); return this; }
  lengthSq() { return this.x ** 2 + this.y ** 2 + this.z ** 2; }
  normalize() { const l = Math.sqrt(this.lengthSq()) || 1; this.x /= l; this.y /= l; this.z /= l; return this; }
}
const THREE = {Matrix4, Vector3};

const here = path.dirname(fileURLToPath(import.meta.url));
const raw = JSON.parse(fs.readFileSync(path.join(here, '__cadgen__/models/body-chassis.step.py/assembly.json')));
const module = (await import(pathToFileURL(path.join(here, 'body-chassis.params.js')))).default;
const geo = JSON.parse(fs.readFileSync(path.join(here, 'body-chassis.params.js'), 'utf8').match(/const geo = (.*);/)[1]);
const definition = normalizeStepModuleDefinition(module);
const leaves = raw.occurrences.filter(o => !raw.occurrences.some(c => c.id.startsWith(o.id + '.')));
const meshData = {parts: leaves.map(o => ({...o, occurrenceId: o.id}))};
const features = resolveStepModuleFeatures(definition, {meshData});
const counts = {};
for (const [id, f] of Object.entries(features)) {
  if (f.missing || !f.partIds.length) throw Error('Unresolved feature ' + id);
  counts[id] = f.partIds.length;
}
const moving = ['frame_R', 'frame_P', 'frame_Y', 'yaw_pinion', 'wheel_L', 'wheel_R'];
const owner = new Map();
for (const key of moving) for (const id of features[key].partIds) {
  if (owner.has(id)) throw Error(`part ${id} in both ${owner.get(id)} and ${key}`);
  owner.set(id, key);
}

const defaults = Object.fromEntries(Object.entries(module.manifest.parameters).map(([id, d]) => [id, d.default]));
function pose(params) {
  const effectsByPartId = new Map();
  const effects = createStepModuleEffectsApi(THREE, {meshData, features, runtime: {}, effectsByPartId});
  module.update({params: {...defaults, ...params}, effects});
  const matrixOf = key => {
    const ms = features[key].partIds.map(id => effectsByPartId.get(id)?.matrix || new Matrix4());
    for (const m of ms) if (m.elements.some((v, i) => Math.abs(v - ms[0].elements[i]) > 1e-9)) throw Error('non-rigid ' + key);
    return ms[0];
  };
  const bodyId = features.shell.partIds[0];
  return {matrixOf, body: effectsByPartId.get(bodyId)?.matrix || new Matrix4(), effectsByPartId};
}
const near = (a, b, tol = 1e-6) => a.every((v, i) => Math.abs(v - b[i]) <= tol);
const dist = (a, b) => Math.hypot(...a.map((v, i) => v - b[i]));
const checks = [];
function check(name, ok, detail) {
  checks.push({name, passed: Boolean(ok), ...(detail ? {detail} : {})});
  if (!ok) throw Error(name + ' ' + JSON.stringify(detail ?? ''));
}
const P = geo.pivots;

// Neutral: nothing moves.
{
  const {effectsByPartId} = pose({});
  check('neutral pose is identity', [...effectsByPartId.values()].every(e => !e.matrix || near(e.matrix.elements, new Matrix4().elements)));
}
// Head joints each fix their own axis and drag the frames outboard of them.
for (const [joint, axis, value] of [['roll', [1, 0, 0], 18], ['pitch', [0, 1, 0], 40], ['yaw', [0, 0, 1], 55]]) {
  const {matrixOf} = pose({[`head_${joint}_deg`]: value, drive_on_floor: false});
  const onAxis = P[joint].map((v, i) => v + 25 * axis[i]);
  const carried = {roll: ['frame_R'], pitch: ['frame_R', 'frame_P'], yaw: ['frame_R', 'frame_P', 'frame_Y']}[joint];
  for (const key of carried) check(`${joint} ${value}°: ${key} fixes its axis`, near(matrixOf(key).apply(onAxis), onAxis));
  for (const key of ['frame_R', 'frame_P', 'frame_Y'].filter(k => !carried.includes(k)))
    check(`${joint} ${value}°: ${key} stays put`, near(matrixOf(key).apply([1, 2, 3]), [1, 2, 3]));
}
// Yaw spur mesh: over a tiny step the two pitch circles carry the mesh point
// together (no slip; a reversed pinion would part them by ~6e-4 mm).
{
  const r = 18.5, eps = 1e-3;
  const mesh = [P.yaw[0] + (P.pinion[0] - P.yaw[0]) / 2, P.yaw[1] + (P.pinion[1] - P.yaw[1]) / 2, 150];
  const a = pose({head_yaw_deg: eps, drive_on_floor: false});
  const driven = a.matrixOf('frame_Y').apply(mesh), pinion = a.matrixOf('yaw_pinion').apply(mesh);
  check('yaw 1:1 spur meshes without slip', near(driven, pinion, 1e-7), {driven, pinion});
  check('mesh point sits on both pitch circles', Math.abs(dist(mesh.slice(0, 2), P.yaw.slice(0, 2)) - r) < 1e-6 && Math.abs(dist(mesh.slice(0, 2), P.pinion.slice(0, 2)) - r) < 1e-6);
}
// Wheels: spin fixes the hub; drive rolls without slip (contact point instantaneously still).
{
  const {matrixOf} = pose({wheel_L_deg: 90, wheel_R_deg: -30, drive_on_floor: false});
  for (const s of ['L', 'R']) check(`wheel ${s} spins about its hub`, near(matrixOf('wheel_' + s).apply(P['wheel_' + s]), P['wheel_' + s]));
  const eps = 1e-3;
  for (const [l, r] of [[eps, eps], [eps, 0], [0, eps], [eps, -eps]]) {
    const m = pose({wheel_L_deg: l, wheel_R_deg: r});
    for (const s of ['L', 'R']) {
      const contact = [P['wheel_' + s][0], P['wheel_' + s][1], 0];
      const moved = m.matrixOf('wheel_' + s).apply(contact);
      check(`L${l} R${r}: wheel ${s} contact does not slip`, dist(moved, contact) < 1e-7, {slip_mm: dist(moved, contact)});
    }
  }
  const full = pose({wheel_L_deg: 360, wheel_R_deg: 360});
  check('one turn each drives one circumference forward', near(full.body.apply([0, 0, 0]), [2 * Math.PI * geo.wheel_radius, 0, 0], 1e-6));
  const spin = pose({wheel_L_deg: -360, wheel_R_deg: 360});
  const heading = 2 * 2 * Math.PI * geo.wheel_radius / geo.track * 180 / Math.PI;
  const nose = spin.body.apply([100, 0, 0]);
  check('opposed wheels spin in place, left turn positive', near(spin.body.apply([0, 0, 42]), [0, 0, 42]) && Math.abs(((Math.atan2(nose[1], nose[0]) * 180 / Math.PI - heading) % 360 + 540) % 360 - 180) < 1e-6, {heading_deg: heading});
  const floor = pose({wheel_L_deg: 200, wheel_R_deg: -50, head_yaw_deg: 30});
  check('drive keeps everything on the floor plane', Math.abs(floor.body.apply([5, 7, 0])[2]) < 1e-9);
}
// Every slider extreme resolves to finite rigid transforms.
for (const [k, d] of Object.entries(module.manifest.parameters)) if (d.type === 'number') for (const v of [d.min, d.max]) {
  const {effectsByPartId} = pose({[k]: v});
  check(`${k}=${v} finite`, [...effectsByPartId.values()].every(e => !e.matrix || e.matrix.elements.every(Number.isFinite)));
}

const result = {passed: true, leaves: leaves.length, features: counts, pivots_mm: geo.pivots, checks: checks.length, failed: checks.filter(c => !c.passed).length};
fs.writeFileSync(path.join(here, 'generated/viewer-checks.json'), JSON.stringify({...result, detail: checks}, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
