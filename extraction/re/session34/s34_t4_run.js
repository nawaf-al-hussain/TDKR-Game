// S34 T4: run ALL extracted Lua scripts in fengari, fresh state per script.
'use strict';
const fs = require('fs');
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;

const D = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s34_t4_scripts.json', 'utf8'));
const scripts = D.all_scripts;

// version scan
const V51 = [['setfenv', /\bsetfenv\s*\(/], ['getfenv', /\bgetfenv\s*\(/],
  ['unpack', /(^|[^\w.])unpack\s*\(/], ['loadstring', /\bloadstring\s*\(/],
  ['table.getn', /table\.getn\s*\(/], ['math.mod', /math\.mod\s*\(/],
  ['string.gfind', /string\.gfind\s*\(/], ['arg.n', /\barg\.n\b/]];
const v51hits = {};
for (const [name, re] of V51) {
  const n = scripts.filter(s => re.test(s.script)).length;
  if (n) v51hits[name] = n;
}
let intdiv = 0, tostring_fmt = 0, setmeta = 0, goto_kw = 0;
for (const s of scripts) {
  if (/[^\/\w]\/\s*\d/.test(s.script)) intdiv++;
  if (/tostring\s*\(/.test(s.script)) tostring_fmt++;
  if (/\bsetmetatable\b/.test(s.script)) setmeta++;
  if (/\bgoto\b/.test(s.script)) goto_kw++;
}
console.log(`scripts: ${scripts.length}; 5.1-only census: ${JSON.stringify(v51hits)}`);
console.log(`division-use: ${intdiv}; tostring-use: ${tostring_fmt}; setmetatable: ${setmeta}; goto: ${goto_kw}`);

const calls = [];
const apiCount = {};

function freshState() {
  const L = lauxlib.luaL_newstate();
  lualib.luaL_openlibs(L);
  const stub = (name, fn) => {
    lua.lua_pushcfunction(L, function(Ls) {
      const n = lua.lua_gettop(Ls);
      const args = [];
      for (let i = 1; i <= n; i++) {
        const t = lua.lua_type(Ls, i);
        if (t === lua.LUA_TNUMBER) args.push(lua.lua_tonumber(Ls, i));
        else if (t === lua.LUA_TSTRING) args.push(to_jsstring(lua.lua_tolstring(Ls, i)));
        else if (t === lua.LUA_TBOOLEAN) args.push(lua.lua_toboolean(Ls, i));
        else args.push('ptr');
      }
      calls.push({ api: name, args });
      apiCount[name] = (apiCount[name] || 0) + 1;
      if (fn) return fn(Ls, args);
      return 0;
    });
    lua.lua_setglobal(L, to_luastring(name));
  };
  // semantic value-returners
  stub('ActorIsInStateType', (Ls, a) => {
    const id = typeof a[0] === 'number' ? a[0] : 0;
    lua.lua_pushboolean(L, (Math.floor(id / 1000) % 2) === 0); return 1;
  });
  stub('IsDead', (Ls) => { lua.lua_pushboolean(L, false); return 1; });
  stub('ActorIsDead', (Ls) => { lua.lua_pushboolean(L, false); return 1; });
  stub('ObjectGetPosition', (Ls) => {
    lua.lua_pushnumber(L, -470.09); lua.lua_pushnumber(L, -960.2);
    lua.lua_pushnumber(L, -3.91); return 3;
  });
  stub('GetDistFromMC', (Ls) => { lua.lua_pushnumber(L, 12.5); return 1; });
  stub('Random', (Ls, a) => {
    const hi = a.length > 1 ? a[1] : (a[0] || 100);
    const lo = a.length > 1 ? a[0] : 0;
    lua.lua_pushnumber(L, Math.floor((lo + hi) / 2)); return 1;
  });
  stub('GetActorFromObject', (Ls) => { lua.lua_pushlightuserdata(L, null); return 1; });
  stub('ActorGetState', (Ls) => { lua.lua_pushnumber(L, 1); return 1; });
  stub('ObjectGetInt', (Ls) => { lua.lua_pushnumber(L, 0); return 1; });
  stub('Wait', (Ls) => { return lua.lua_yield(Ls, 0); });
  for (const nm of ['Enable', 'Disable', 'ShowObject', 'HideObject', 'ShowMessage',
    'HideOccluder', 'ShowOccluder', 'DisableHideObject', 'StartCinematicObject',
    'StartFadeOut', 'StartFadeIn', 'RequireLoadLevel', 'ObjectiveAdd', 'ObjectiveRemove',
    'ShowObjectiveMessage', 'StartSound', 'StopSound', 'SetRotateControlEnable',
    'SetMoveControlEnable', 'CameraLookAt', 'ActorLookTo', 'SetQuestFailed',
    'SetQuestEnabled', 'MissionFailedAutoReload', 'StartPipeGame', 'NextMission',
    'StopSideMissionManager', 'EnableHotSpotManager', 'ActorSetState', 'SpawnObject',
    'SetStateType', 'ActivateDistrictZone', 'ObjectiveCompleted', 'SetActorInvincible',
    'FreezePlayer', 'UnfreezePlayer', 'SetCameraMode', 'PrintDebug', 'SetTimer',
    'KillTimer', 'ActorPlayAnim', 'SetCollisionEnable', 'AttachObject', 'DetachObject',
    'SetPos', 'SetObjectPos', 'PlaySound', 'CineStart', 'CineStop', 'SetSky',
    'SetObjectiveComplete', 'AddScore', 'SetHealth', 'GiveWeapon', 'SetBrightness',
    'ShowMissionBar', 'HideMissionBar', 'SetFadeColor', 'ReturnToHub', 'SetTimerMS']) {
    stub(nm);
  }
  stub('print', (Ls, a) => { calls.push({ api: 'print', args: a.join(' ') }); return 0; });
  stub('GetTime', (Ls) => { lua.lua_pushnumber(L, 1000 * (Date.now() % 100000)); return 1; });
  stub('IsEnabled', (Ls) => { lua.lua_pushboolean(L, true); return 1; });
  stub('GetDistBetweenObjects', (Ls) => { lua.lua_pushnumber(L, 25.0); return 1; });
  stub('IsCopAIEnabled', (Ls) => { lua.lua_pushboolean(L, false); return 1; });
  stub('IsLowEndDevice', (Ls) => { lua.lua_pushboolean(L, false); return 1; });
  stub('GetGlobalVar', (Ls) => { lua.lua_pushnumber(L, 0); return 1; });
  stub('IsCameraFacing', (Ls) => { lua.lua_pushboolean(L, true); return 1; });
  stub('GetCurrentInteractionObjectID', (Ls) => { lua.lua_pushnumber(L, 0); return 1; });
  for (const nm of ['KillActor', 'GiveDamage', 'SetActorSpeedWalk', 'SetActorSpeedRun',
    'SetActorSpeedGlide', 'StartMainStoryFromQuestId', 'NPCSetSniper', 'NPCSetStance',
    'TeleportPlayerToZone', 'NPCGoToWaypointWithNavmesh', 'NPCAttackTarget', 'NPCGoToPath',
    'ClearObjectiveMessage', 'NPCStandGroundTarget', 'NPCPatrolArea', 'NPCGoToWaypoint',
    'fz_sandbox_enable_all_first_island', 'fz_sandbox_disable_all', 'fz_sandbox_enable_ALL',
    'StartEventAtObjectNode', 'EnableShowObject', 'SetJumpControlEnable',
    'RemoveGenericObjectFromMap', 'EnableRain', 'EnableMainStory', 'SetQuestCompleted',
    'QTE_GrapplingSetTarget', 'ResetSlowMotion', 'SetRopeVisible', 'PostProcessingEffectAdd',
    'EnableInteractionForObject', 'EnterBatPod', 'EnableControls', 'SetZFar', 'r_map',
    'StopMusic', 'DisableInteractionForObject', 'PlayAnimation', 'StopCurrentSFXAtObject',
    'StartEffect', 'PlayEffectOnObject', 'SetQuestDisabled', 'Traffic_SpawnerEnable',
    'ResetAllIgnoredControls', 'SaveGame', 'MissionFailed']) {
    stub(nm);
  }
  return L;
}

const results = [];
let idx = 0;
function runOne() {
  if (idx >= scripts.length) { finish(); return; }
  const s = scripts[idx];
  calls.length = 0;
  const L = freshState();
  let outcome, err = null, resumes = 0;
  const status = lauxlib.luaL_loadstring(L, to_luastring(s.script));
  if (status !== lua.LUA_OK) {
    outcome = 'load_error';
    const eb = lua.lua_tostring(L, -1);
    err = eb ? to_jsstring(eb) : 'load_error';
    lua.lua_pop(L, 1);
  } else {
    const co = lua.lua_newthread(L);
    // stack: [chunk, thread]; push chunk value onto co:
    lua.lua_pushvalue(L, 1);      // copy chunk to top
    lua.lua_xmove(L, co, 1);      // move the copy to co
    lua.lua_pop(L, 1);            // pop the thread from L (keep chunk for reuse)
    let res = lua.lua_resume(co, L, 0);   // defines the handler globals
    if (res === lua.LUA_OK && s.fn) {
      // call the entry handler with a fake actor object
      lua.lua_getglobal(co, to_luastring(s.fn));
      if (lua.lua_isfunction(co, -1)) {
        lua.lua_pushlightuserdata(co, null);   // fake actor/self
        res = lua.lua_resume(co, L, 1);
        while (res === lua.LUA_YIELD && resumes < 64) {
          resumes++;
          res = lua.lua_resume(co, L, 0);
        }
      } else lua.lua_pop(co, 1);
    }
    if (res === lua.LUA_OK) outcome = 'completes';
    else if (res === lua.LUA_YIELD) outcome = 'yield_incomplete';
    else {
      outcome = 'runtime_error';
      const t = lua.lua_type(co, -1);
      const eb = lua.lua_tostring(co, -1);
      if (eb && !(eb instanceof Uint8Array) && typeof eb !== 'string') {
        err = 'RAW:' + Array.from(eb).join(',');
      } else {
        err = eb ? to_jsstring(eb) : ('nonstr:' + lua.lua_typename(co, t));
      }
    }
  }
  results.push({ i: idx, fn: s.fn, obj: s.obj_id, outcome,
                 err: err ? err.slice(0, 140) : null, nApi: calls.length, resumes });
  idx++;
  if (idx % 120 === 0) console.log(`... ${idx}/${scripts.length}`);
  setImmediate(runOne);
}
function finish() {
  fs.writeFileSync('/home/z/my-project/scripts/s34_t4_results.json',
    JSON.stringify({ results, apiCount, v51hits, intdiv, tostring_fmt, setmeta, goto_kw }, null, 1));
  const cnt = {};
  for (const r of results) cnt[r.outcome] = (cnt[r.outcome] || 0) + 1;
  console.log('OUTCOMES:', JSON.stringify(cnt));
  const ranked = Object.entries(apiCount).sort((a, b) => b[1] - a[1]);
  console.log('TOP APIS:', ranked.slice(0, 16).map(([k, v]) => `${k}:${v}`).join(' '));
  const errs = {};
  for (const r of results) if (r.err) errs[r.err] = (errs[r.err] || 0) + 1;
  console.log('TOP ERRORS:', Object.entries(errs).sort((a, b) => b[1] - a[1]).slice(0, 5)
    .map(([k, v]) => `${v}x ${k.slice(0, 70)}`).join(' | '));
}
runOne();
