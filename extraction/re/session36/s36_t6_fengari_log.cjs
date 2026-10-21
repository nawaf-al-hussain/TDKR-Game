// s36_t6_fengari_log.cjs — run 10 OnEnter scripts in fengari with FULL call
// logging (name + args) for the Lua 5.1 comparison (identical stubs in lupa).
'use strict';
const fs = require('fs');
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;

const D = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s34_t4_scripts.json', 'utf8'));
const onEnter = D.all_scripts.filter(s => (s.fn || '').includes('_OnEnter')).slice(0, 10);

const SEMANTIC = {
  ActorIsInStateType: (a) => { lua.lua_pushboolean(L, true); return 1; },
};

function makeLogged() {
  const L = lauxlib.luaL_newstate();
  lualib.luaL_openlibs(L);
  const calls = [];
  const log = (name, Ls, n) => {
    const args = [];
    for (let i = 1; i <= n; i++) {
      const t = lua.lua_type(Ls, i);
      if (t === lua.LUA_TNUMBER) args.push(lua.lua_tonumber(Ls, i));
      else if (t === lua.LUA_TSTRING) args.push(to_jsstring(lua.lua_tostring(Ls, i)));
      else if (t === lua.LUA_TBOOLEAN) args.push(lua.lua_toboolean(Ls, i) ? true : false);
      else args.push(':' + lua.lua_typename(Ls, t));
    }
    calls.push([name].concat(args));
  };
  const stub = (name, fn) => {
    lua.lua_pushcfunction(L, function(Ls) {
      const n = lua.lua_gettop(Ls);
      log(name, Ls, n);
      if (name === 'Wait') return lua.lua_yield(Ls, 0);
      if (!fn) return 0;
      return fn(Ls, n);
    });
    lua.lua_setglobal(L, to_luastring(name));
  };
  // identical values everywhere (r35/r26 semantic stubs)
  stub('GetTime', (Ls) => { lua.lua_pushnumber(Ls, 1000); return 1; });
  stub('IsEnabled', (Ls) => { lua.lua_pushboolean(Ls, true); return 1; });
  stub('GetDistBetweenObjects', (Ls) => { lua.lua_pushnumber(Ls, 25.0); return 1; });
  stub('IsCopAIEnabled', (Ls) => { lua.lua_pushboolean(Ls, false); return 1; });
  stub('IsLowEndDevice', (Ls) => { lua.lua_pushboolean(Ls, false); return 1; });
  stub('GetGlobalVar', (Ls) => { lua.lua_pushnumber(Ls, 0); return 1; });
  stub('IsCameraFacing', (Ls) => { lua.lua_pushboolean(Ls, true); return 1; });
  stub('GetCurrentInteractionObjectID', (Ls) => { lua.lua_pushnumber(Ls, 0); return 1; });
  stub('ActorIsInStateType', (Ls) => { lua.lua_pushboolean(Ls, true); return 1; });
  stub('IsDead', (Ls) => { lua.lua_pushboolean(Ls, false); return 1; });
  stub('ActorIsDead', (Ls) => { lua.lua_pushboolean(Ls, false); return 1; });
  stub('ObjectGetPosition', (Ls) => { lua.lua_pushnumber(Ls, -470.09); lua.lua_pushnumber(Ls, -960.2); lua.lua_pushnumber(Ls, -3.91); return 3; });
  stub('GetDistFromMC', (Ls) => { lua.lua_pushnumber(Ls, 12.5); return 1; });
  stub('Random', (Ls) => { lua.lua_pushnumber(Ls, 1); return 1; });
  stub('Wait', null);
  stub('GetActorFromObject', (Ls) => { lua.lua_pushlightuserdata(Ls, null); return 1; });
  stub('ActorGetState', (Ls) => { lua.lua_pushnumber(Ls, 1); return 1; });
  const VOID = ('Enable Disable ShowObject HideObject ShowMessage HideOccluder ShowOccluder DisableHideObject ' +
    'StartCinematicObject StartFadeOut StartFadeIn RequireLoadLevel ObjectiveAdd ObjectiveRemove ' +
    'ShowObjectiveMessage StartSound StopSound SetRotateControlEnable SetMoveControlEnable CameraLookAt ' +
    'ActorLookTo SetQuestFailed SetQuestEnabled MissionFailedAutoReload StartPipeGame NextMission ' +
    'StopSideMissionManager EnableHotSpotManager ActorSetState SpawnObject SetStateType ActivateDistrictZone ' +
    'ObjectiveCompleted SetActorInvincible FreezePlayer UnfreezePlayer SetCameraMode PrintDebug SetTimer ' +
    'KillTimer ActorPlayAnim SetCollisionEnable AttachObject DetachObject SetPos SetObjectPos PlaySound ' +
    'CineStart CineStop SetSky SetObjectiveComplete AddScore SetHealth GiveWeapon SetBrightness ' +
    'ShowMissionBar HideMissionBar SetFadeColor ReturnToHub SetTimerMS KillActor GiveDamage ' +
    'SetActorSpeedWalk SetActorSpeedRun SetActorSpeedGlide StartMainStoryFromQuestId NPCSetSniper ' +
    'NPCSetStance TeleportPlayerToZone NPCGoToWaypointWithNavmesh NPCAttackTarget NPCGoToPath ' +
    'ClearObjectiveMessage NPCStandGroundTarget NPCPatrolArea NPCGoToWaypoint print ' +
    'fz_sandbox_enable_before_pit PlayCameraAnim r_RandomChoice fz_RandomChoice TurretSetActive ' +
    'PostProcessingEffectRemove QTE_EnableControl DisableCopAI CameraShake StartSoundAtWaypoint ' +
    'EnableShowObject StartEventAtObjectNode ObjectiveShow SetCurrentActor ActorWa RemoveGenericObjectFromMap EnableRain SetObjectiveText ObjectiveHide ActorWalkTo ActorRunTolkTo ActorRunTo').split(/\s+/);
  for (const nm of VOID) stub(nm);
  lua.lua_pushnumber(L, 40.0);
  lua.lua_setglobal(L, to_luastring('MC_MAX_DISTANCE'));
  return { L, calls };
}

const out = [];
for (const s of onEnter) {
  const { L, calls } = makeLogged();
  const co = lua.lua_newthread(L);
  let outcome = 'completes', err = null;
  let st = lauxlib.luaL_loadstring(co, to_luastring(s.script));
  if (st !== lua.LUA_OK) { outcome = 'load_error'; }
  else {
    st = lua.lua_resume(co, L, 0);   // runs the definition chunk
    if (st === lua.LUA_OK) {
      lua.lua_getglobal(co, to_luastring(s.fn));
      lua.lua_pushnumber(co, s.obj_id || 0);
      lua.lua_pushnumber(co, 0);     // capsule id placeholder
      st = lua.lua_resume(co, L, 2); // calls the handler
      let resumes = 0;
      while (st === lua.LUA_YIELD && resumes < 16) {
        st = lua.lua_resume(co, L, 0);
        resumes++;
      }
    }
    if (st !== lua.LUA_OK && st !== lua.LUA_YIELD) {
      outcome = 'runtime_error';
      err = to_jsstring(lua.lua_tostring(co, -1) || 'unknown');
    }
  }
  out.push({ fn: s.fn, obj: s.obj_id, outcome, err, calls, resumes: Math.min(16, out.length ? 0 : 0) });
  console.log(`${s.fn}: ${outcome} (${calls.length} calls)`);
}
fs.writeFileSync('/home/z/my-project/scripts/s36_t6_fengari_logs.json', JSON.stringify(out, null, 1));
console.log('saved s36_t6_fengari_logs.json');
