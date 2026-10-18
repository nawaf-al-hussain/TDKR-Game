// S35 T5: corrected run — stubs push onto Ls (coroutine), three-way
// completeness (semantic / void / none), error objects decoded properly,
// plus 5.1-faithful shim comparisons for scripts using risky constructs.
'use strict';
const fs = require('fs');
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;

const D = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s34_t4_scripts.json', 'utf8'));
const scripts = D.all_scripts;

const decode = (u8) => Array.from(u8).map(c => String.fromCharCode(c)).join('');

const VOID_APIS = new Set();
function makeState(mode) {
  // mode: 'semantic' | 'void' | 'none'
  const L = lauxlib.luaL_newstate();
  lualib.luaL_openlibs(L);
  if (mode === 'none') return L;
  const calls = [];
  const stub = (name, fn) => {
    lua.lua_pushcfunction(L, function(Ls) {
      const n = lua.lua_gettop(Ls);
      VOID_APIS.add(name);
      if (mode === 'void' || !fn) return 0;   // void: exist but return nothing
      return fn(Ls, n);
    });
    lua.lua_setglobal(L, to_luastring(name));
  };
  stub('ActorIsInStateType', (Ls) => { lua.lua_pushboolean(Ls, true); return 1; });
  stub('IsDead', (Ls) => { lua.lua_pushboolean(Ls, false); return 1; });
  stub('ActorIsDead', (Ls) => { lua.lua_pushboolean(Ls, false); return 1; });
  stub('ObjectGetPosition', (Ls) => {
    lua.lua_pushnumber(Ls, -470.09); lua.lua_pushnumber(Ls, -960.2);
    lua.lua_pushnumber(Ls, -3.91); return 3;
  });
  stub('GetDistFromMC', (Ls) => { lua.lua_pushnumber(Ls, 12.5); return 1; });
  stub('Random', (Ls) => { lua.lua_pushnumber(Ls, 1); return 1; });
  stub('GetActorFromObject', (Ls) => { lua.lua_pushlightuserdata(Ls, null); return 1; });
  stub('ActorGetState', (Ls) => { lua.lua_pushnumber(Ls, 1); return 1; });
  stub('ObjectGetInt', (Ls) => { lua.lua_pushnumber(Ls, 0); return 1; });
  stub('GetTime', (Ls) => { lua.lua_pushnumber(Ls, 1000); return 1; });   // FIX: Ls
  stub('IsEnabled', (Ls) => { lua.lua_pushboolean(Ls, true); return 1; });
  stub('GetDistBetweenObjects', (Ls) => { lua.lua_pushnumber(Ls, 25.0); return 1; });
  stub('IsCopAIEnabled', (Ls) => { lua.lua_pushboolean(Ls, false); return 1; });
  stub('IsLowEndDevice', (Ls) => { lua.lua_pushboolean(Ls, false); return 1; });
  stub('GetGlobalVar', (Ls) => { lua.lua_pushnumber(Ls, 0); return 1; });
  stub('IsCameraFacing', (Ls) => { lua.lua_pushboolean(Ls, true); return 1; });
  stub('GetCurrentInteractionObjectID', (Ls) => { lua.lua_pushnumber(Ls, 0); return 1; });
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
    'ShowMissionBar', 'HideMissionBar', 'SetFadeColor', 'ReturnToHub', 'SetTimerMS',
    'KillActor', 'GiveDamage', 'SetActorSpeedWalk', 'SetActorSpeedRun',
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
    'ResetAllIgnoredControls', 'SaveGame', 'MissionFailed', 'ActorSetTarget',
    'NPCGoTo', 'SetObjectiveText', 'ObjectiveShow', 'ObjectiveHide', 'SetCurrentActor',
    'ActorWalkTo', 'ActorRunTo', 'ActorTeleportTo', 'CameraFade', 'SetWorldPause']) {
    stub(nm);
  }
  stub('print', () => 0);
  return L;
}

function runScript(s, mode, shim51) {
  const L = makeState(mode);
  if (shim51) {
    // Lua 5.1-faithful overrides on the fengari (5.3) core:
    // tostring(1.0) = "1"; string.format('%d', 3.5) = 3 (via C cast);
    // '/' on integers = float division (already 5.3-float-compatible);
    // setfenv/getfenv/unpack/loadstring/table.getn/math.mod/string.gfind
    const shim = `
local __tostring53 = tostring
local __format53 = string.format
_G.tostring = function(v)
  local t = type(v)
  if t == 'number' and math.floor(v) == v and math.abs(v) < 2^53 then
    return __format53('%d', v)
  end
  return __tostring53(v)
end
string.format = function(f, ...)
  local args = {}
  for i = 1, select('#', ...) do
    local v = select(i, ...)
    if type(v) == 'number' and math.floor(v) == v and string.find(tostring(f), '%%d') then
      v = math.floor(v)
    end
    args[i] = v
  end
  return __format53(f, unpack(args))
end
_G.unpack = table.unpack or unpack
_G.loadstring = load or loadstring
table.getn = function(t) return #t end
math.mod = math.fmod
`;
    if (lauxlib.luaL_dostring(L, to_luastring(shim)) !== lua.LUA_OK) {
      return { outcome: 'shim_error', err: 'shim failed' };
    }
  }
  let res = lauxlib.luaL_loadstring(L, to_luastring(s.script));
  if (res !== lua.LUA_OK) {
    const eb = lua.lua_tostring(L, -1);
    lua.lua_close(L);
    return { outcome: 'load_error', err: eb ? to_jsstring(eb) : 'load' };
  }
  const co = lua.lua_newthread(L);
  lua.lua_pushvalue(L, 1);
  lua.lua_xmove(L, co, 1);
  lua.lua_pop(L, 1);
  res = lua.lua_resume(co, L, 0);
  let resumes = 0;
  if (res === lua.LUA_OK && s.fn) {
    lua.lua_getglobal(co, to_luastring(s.fn));
    if (lua.lua_isfunction(co, -1)) {
      lua.lua_pushlightuserdata(co, null);
      res = lua.lua_resume(co, L, 1);
      while (res === lua.LUA_YIELD && resumes < 64) {
        resumes++;
        res = lua.lua_resume(co, L, 0);
      }
    } else lua.lua_pop(co, 1);
  }
  let out, err = null;
  if (res === lua.LUA_OK) out = 'completes';
  else if (res === lua.LUA_YIELD) out = 'yield_incomplete';
  else {
    out = 'runtime_error';
    const t = lua.lua_type(co, -1);
    const eb = lua.lua_tostring(co, -1);
    err = eb ? to_jsstring(eb) : ('nonstr:' + decode(lua.lua_typename(co, t)) +
          (t === lua.LUA_TFUNCTION ? ' (C-stub value leaked: harness artifact)' : ''));
  }
  lua.lua_close(L);
  return { outcome: out, err: err ? err.slice(0, 120) : null };
}

// risky-construct census for the 5.1 shim pass
function risky(s) {
  return /\btostring\s*\(/.test(s.script) ||
         /string\.format\s*\(\s*["'][^"']*%d/.test(s.script) ||
         /[^\/\w.]\/\s*[\d\w]/.test(s.script) ||
         /\bunpack\s*\(/.test(s.script) || /\bsetfenv\b/.test(s.script);
}

const results = [];
let idx = 0;
function pass(mode, label, onlyRisky) {
  const rows = [];
  for (const s of scripts) {
    if (onlyRisky && !risky(s)) { rows.push(null); continue; }
    rows.push(runScript(s, mode, label === 'shim51'));
  }
  return rows;
}

console.log(`scripts: ${scripts.length}`);
const sem = pass('semantic', 'semantic');
const voi = pass('void', 'void');
const non = pass('none', 'none');
const riskyIdx = scripts.map((s, i) => risky(s) ? i : -1).filter(i => i >= 0);
console.log(`risky-construct scripts (tostring/%d/division/unpack/setfenv): ${riskyIdx.length}`);
const shim = pass('semantic', 'shim51', true);

function tally(rows) {
  const c = {};
  for (const r of rows) { if (r) c[r.outcome] = (c[r.outcome] || 0) + 1; }
  return c;
}
console.log('semantic:', JSON.stringify(tally(sem)));
console.log('void-stubs:', JSON.stringify(tally(voi)));
console.log('no-stubs:', JSON.stringify(tally(non)));
console.log('shim51(risky only):', JSON.stringify(tally(shim.filter(x => x))));

// three-way classification
const three = { no_stubs_needed: 0, needs_stub_presence: 0, needs_semantic_values: 0, errors: 0 };
for (let i = 0; i < scripts.length; i++) {
  if (non[i] && non[i].outcome === 'completes') three.no_stubs_needed++;
  else if (voi[i] && voi[i].outcome === 'completes') three.needs_stub_presence++;
  else if (sem[i] && sem[i].outcome === 'completes') three.needs_semantic_values++;
  else three.errors++;
}
console.log('THREE-WAY:', JSON.stringify(three));

// shim vs no-shim on risky scripts: outcome differences
let diffs = 0;
for (let k = 0; k < riskyIdx.length; k++) {
  const i = riskyIdx[k];
  const a = sem[i].outcome, b = shim[k] ? shim[k].outcome : null;
  if (a !== b) { diffs++; if (diffs <= 8) console.log(`shim diff idx ${i} (${scripts[i].fn}): ${a} -> ${b}`); }
}
console.log(`shim-vs-53 outcome diffs on risky scripts: ${diffs}/${riskyIdx.length}`);

fs.writeFileSync('/home/z/my-project/scripts/s35_t5_results.json',
  JSON.stringify({ semantic: sem, void: voi, none: non, shim: shim, riskyIdx, three }, null, 1));
console.log('saved s35_t5_results.json');
