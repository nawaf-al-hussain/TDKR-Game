// S34 T3/T4: spatial trigger firing demo — capsule walks a straight line
// through the world; when it enters a trigger's decoded volume (position from
// the 54-B component record, vertical extent = stored H), fire its Lua
// OnEnter/OnReach handler in fengari and log the API calls. Data-determined:
// the walk line passes through a trigger position taken from the records.
'use strict';
const fs = require('fs');
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;

const D = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s34_t4_scripts.json', 'utf8'));
const trigs = D.triggers.filter(t => t.script);

// pick the trigger with the most OnEnter-like chain (data-determined):
// use the FIRST trigger whose id ends in the r23-fired one's neighborhood,
// or simply the one with the richest script
const cands = trigs.filter(t => /OnEnter/.test(t.fn || '') &&
  t.script.length > 300 && t.script.length < 1500 &&
  (t.script.match(/\b(Enable|Disable|ShowMessage|Wait|StartFadeOut|ShowObject)\b/g) || []).length >= 3);
cands.sort((a, b) => a.script.length - b.script.length);
const tg = cands[0] || trigs.find(t => /OnEnter|OnReach/.test(t.fn || '')) || trigs[0];
console.log(`target trigger: id ${tg.rec_id}, fn ${tg.fn}, pos ` +
            `[${tg.f9.slice(0, 3).map(v => +v.toFixed(1)).join(', ')}], ` +
            `H-field f9[6]=${tg.f9[6]}, script ${tg.script.length} B`);
console.log(`script: ${tg.script.slice(0, 160).replace(/\n/g, ' | ')}...`);

// capsule walk: from 30 m south of the trigger position toward north through it
const px = tg.f9[0], py = tg.f9[1], pz = tg.f9[2];
const path = [];
for (let d = -30; d <= 30; d += 0.5) path.push([px, py + d, pz]);
// capsule radius r=0.45, height 1.8; volume = OBB at (px,py,pz), vertical half-extent
// = stored H (fallback 10 m horizontal approx if H=0: the engine default OBB)
const H = Math.max(tg.f9[6], 2.0);
let fired = null;
for (const [x, y, z] of path) {
  const dh = Math.hypot(x - px, y - py);
  const dz = Math.abs(z - pz);
  // decoded volume: horizontal half-extent = engine default (approx 10 m,
  // r21/r23); vertical = H. Enter when inside.
  if (dh < 10 && dz < H) { fired = { x, y, z, dh, step: path.indexOf([x, y, z]) }; break; }
}
if (!fired) { console.log('NO FIRE'); process.exit(1); }
console.log(`capsule entered volume at [${fired.x.toFixed(1)}, ${fired.y.toFixed(1)}, ${fired.z.toFixed(1)}] ` +
            `(dist ${fired.dh.toFixed(2)} m) -> firing ${tg.fn}`);

// fengari run
const L = lauxlib.luaL_newstate();
lualib.luaL_openlibs(L);
const calls = [];
const stub = (name, fn) => {
  lua.lua_pushcfunction(L, function(Ls) {
    const n = lua.lua_gettop(Ls);
    const args = [];
    for (let i = 1; i <= n; i++) {
      const t = lua.lua_type(Ls, i);
      if (t === lua.LUA_TNUMBER) args.push(+lua.lua_tonumber(Ls, i).toFixed(2));
      else if (t === lua.LUA_TSTRING) args.push(to_jsstring(lua.lua_tolstring(Ls, i)));
      else if (t === lua.LUA_TBOOLEAN) args.push(lua.lua_toboolean(Ls, i));
      else args.push('ptr');
    }
    calls.push({ api: name, args });
    if (fn) return fn(Ls, args);
    return 0;
  });
  lua.lua_setglobal(L, to_luastring(name));
};
stub('Wait', (Ls) => { return lua.lua_yield(Ls, 0); });
for (const nm of ['Enable', 'Disable', 'ShowObject', 'HideObject', 'ShowMessage',
  'HideOccluder', 'ShowOccluder', 'DisableHideObject', 'StartCinematicObject',
  'StartFadeOut', 'StartFadeIn', 'RequireLoadLevel', 'ObjectiveAdd', 'ObjectiveRemove',
  'ShowObjectiveMessage', 'StartSound', 'ActorSetState', 'ActorLookTo', 'SetActorSpeedWalk',
  'GetTime', 'KillActor', 'SetQuestEnabled', 'NextMission', 'EnableShowObject',
  'StartMainStoryFromQuestId', 'PrintDebug', 'SetTimer', 'TeleportPlayerToZone',
  'NPCGoToWaypointWithNavmesh', 'ClearObjectiveMessage', 'StartEventAtObjectNode',
  'SetMoveControlEnable', 'SetRotateControlEnable', 'ObjectiveCompleted', 'SaveGame']) {
  stub(nm);
}
stub('IsCopAIEnabled', (Ls) => { lua.lua_pushboolean(L, false); return 1; });
stub('print', () => 0);
const GVAR = {};
stub('GetGlobalVar', (Ls, a) => {
  const v = GVAR[a[0]] || 0; lua.lua_pushnumber(L, typeof v === 'number' ? v : 0); return 1;
});
stub('RegisterGlobalVar', (Ls, a) => { GVAR[a[0]] = a[1] !== undefined ? a[1] : 0; return 0; });
stub('SetGlobalVar', (Ls, a) => { GVAR[a[0]] = a[1]; return 0; });
stub('DisableCopAI', () => 0);

let status = lauxlib.luaL_loadstring(L, to_luastring(tg.script));
if (status !== lua.LUA_OK) { console.log('LOAD FAIL'); process.exit(1); }
const co = lua.lua_newthread(L);
lua.lua_pushvalue(L, 1);
lua.lua_xmove(L, co, 1);
lua.lua_pop(L, 1);
let res = lua.lua_resume(co, L, 0);
if (res === lua.LUA_OK && tg.fn) {
  lua.lua_getglobal(co, to_luastring(tg.fn));
  if (lua.lua_isfunction(co, -1)) {
    lua.lua_pushlightuserdata(co, null);   // the capsule actor
    res = lua.lua_resume(co, L, 1);
    let resumes = 0;
    while (res === lua.LUA_YIELD && resumes < 32) {
      resumes++;
      console.log(`  [scheduler] Wait yield #${resumes} -> resume`);
      res = lua.lua_resume(co, L, 0);
    }
  }
}
console.log(`handler ${tg.fn}: ${res === lua.LUA_OK ? 'COMPLETED' : (res === lua.LUA_YIELD ? 'still yielding' : 'ERROR')}`);
console.log(`CALL LOG (${calls.length}):`);
for (const c of calls) console.log(`  ${c.api}(${(c.args || []).join(', ')})`);
fs.writeFileSync('/home/z/my-project/scripts/s34_t3_firelog.json',
  JSON.stringify({ trigger: tg.rec_id, fn: tg.fn, pos: tg.f9.slice(0, 3),
                   entered_at: fired, calls }, null, 1));
