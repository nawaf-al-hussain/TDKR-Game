// S37 T5: fengari side - run 30 OnEnter/OnReach scripts with LOGGING stubs
// (semantic values identical to the r36/r37 5.1 side); emit call logs JSON.
'use strict';
const fs = require('fs');
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;

const D = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s34_t4_scripts.json', 'utf8'));
const pool = D.all_scripts.filter(s => /_OnEnter|_OnReach/.test(s.fn || ''));
const sel = [];
const seen = new Set();
for (const want of ['OnEnter', 'OnReach']) {
  for (const s of pool) {
    if (sel.length >= 100) break;
    if ((s.fn || '').includes(want) && !seen.has(s.obj_id)) { sel.push(s); seen.add(s.obj_id); }
  }
  if (sel.length >= 100) break;
}
console.error(`selected ${sel.length} scripts (OnEnter+OnReach, s38 100-script)`);

const SEMANTIC = {
  GetTime: ['n', 1000], IsEnabled: ['b', true], GetDistBetweenObjects: ['n', 25.0],
  IsCopAIEnabled: ['b', false], IsLowEndDevice: ['b', false], GetGlobalVar: ['n', 0],
  IsCameraFacing: ['b', true], GetCurrentInteractionObjectID: ['n', 0],
  ActorIsInStateType: ['b', true], IsDead: ['b', false], ActorIsDead: ['b', false],
  ObjectGetPosition: ['3n', -470.09, -960.2, -3.91], GetDistFromMC: ['n', 12.5],
  Random: ['n', 1], ActorGetState: ['n', 1], ObjectGetInt: ['n', 0],
  GetActorFromObject: ['u', null], ActorGetPodPos: ['3n', 0, 0, 0],
};
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
  'ClearObjectiveMessage NPCStandGroundTarget NPCPatrolArea NPCGoToWaypoint print RemoveGenericObjectFromMap ' +
  'EnableRain SetObjectiveText ObjectiveHide StartEventAtObjectNode SetCurrentActor ActorWalkTo ActorRunTo ' +
  'fz_sandbox_enable_before_pit PlayCameraAnim r_RandomChoice fz_RandomChoice TurretSetActive ' +
  'PostProcessingEffectRemove QTE_EnableControl DisableCopAI CameraShake StartSoundAtWaypoint ' +
  'ObjectiveShow SetObjectiveText2 EnableShowObject SetJumpControlEnable RemoveGenericObjectFromMap2 ' +
  'StartEffect PlayEffectOnObject SetQuestDisabled Traffic_SpawnerEnable ResetAllIgnoredControls ' +
  'SaveGame MissionFailed ActorSetTarget NPCGoTo ActorTeleportTo CameraFade SetWorldPause ' +
  'fz_sandbox_enable_all_first_island fz_sandbox_disable_all fz_sandbox_enable_ALL EnableMainStory ' +
  'SetQuestCompleted QTE_GrapplingSetTarget ResetSlowMotion SetRopeVisible PostProcessingEffectAdd ' +
  'EnableInteractionForObject EnterBatPod EnableControls SetZFar r_map StopMusic ' +
  'DisableInteractionForObject PlayAnimation StopCurrentSFXAtObject StopSideMissionManager2').split(/\s+/)
  .filter(x => x && !x.endsWith('2'));

const out = {};
for (const s of sel) {
  const L = lauxlib.luaL_newstate();
  lualib.luaL_openlibs(L);
  const calls = [];
  const argstr = (Ls, n) => {
    const a = [];
    for (let i = 1; i <= n; i++) {
      const t = lua.lua_type(Ls, i);
      if (t === lua.LUA_TNUMBER) a.push(+lua.lua_tonumber(Ls, i));
      else if (t === lua.LUA_TSTRING) a.push(to_jsstring(lua.lua_tostring(Ls, i)));
      else if (t === lua.LUA_TBOOLEAN) a.push(lua.lua_toboolean(Ls, i) ? true : false);
      else if (t === lua.LUA_TNIL) a.push(null);
      else a.push(':' + to_jsstring(lua.lua_typename(Ls, t)));
    }
    return a;
  };
  const stub = (name, fn) => {
    lua.lua_pushcfunction(L, function(Ls) {
      const n = lua.lua_gettop(Ls);
      calls.push([name, ...argstr(Ls, n)]);
      if (!fn) return 0;
      return fn(Ls, n);
    });
    lua.lua_setglobal(L, to_luastring(name));
  };
  for (const [nm, spec] of Object.entries(SEMANTIC)) {
    if (spec[0] === '3n') stub(nm, (Ls) => { lua.lua_pushnumber(Ls, spec[1]); lua.lua_pushnumber(Ls, spec[2]); lua.lua_pushnumber(Ls, spec[3]); return 3; });
    else if (spec[0] === 'b') stub(nm, (Ls) => { lua.lua_pushboolean(Ls, spec[1]); return 1; });
    else if (spec[0] === 'u') stub(nm, (Ls) => { lua.lua_pushlightuserdata(Ls, spec[1]); return 1; });
    else stub(nm, (Ls) => { lua.lua_pushnumber(Ls, spec[1]); return 1; });
  }
  for (const nm of VOID) stub(nm);
  // s38 T6: math.random DIVERGES between fengari (5.3) and real 5.1 — the shim
  // must override it; stub deterministically for the comparison
  lua.lua_getglobal(L, to_luastring('math'));
  lua.lua_pushcfunction(L, (Ls) => { calls.push(['math.random', ...argstr(Ls, lua.lua_gettop(Ls))]); lua.lua_pushnumber(Ls, 1); return 1; });
  lua.lua_setfield(L, -2, to_luastring('random'));
  lua.lua_pushcfunction(L, (Ls) => { calls.push(['math.randomseed', ...argstr(Ls, lua.lua_gettop(Ls))]); return 0; });
  lua.lua_setfield(L, -2, to_luastring('randomseed'));
  lua.lua_pop(L, 1);
  stub('Wait', (Ls) => lua.lua_yield(Ls, 0));
  lua.lua_pushnumber(L, 10.0);
  lua.lua_setglobal(L, to_luastring('MC_MAX_DISTANCE'));
  // load+run: chunk then the entry fn in a coroutine
  let outcome = 'ok', err = null;
  let res = lauxlib.luaL_loadstring(L, to_luastring(s.script));
  if (res !== lua.LUA_OK) { outcome = 'load_error'; err = to_jsstring(lua.lua_tostring(L, -1)); }
  else {
    const co = lua.lua_newthread(L);
    lua.lua_pushvalue(L, 1); lua.lua_xmove(L, co, 1); lua.lua_pop(L, 1);
    res = lua.lua_resume(co, L, 0);
    let resumes = 0;
    if (res === lua.LUA_OK && s.fn) {
      lua.lua_getglobal(co, to_luastring(s.fn));
      if (lua.lua_isfunction(co, -1)) {
        lua.lua_pushlightuserdata(co, null);
        res = lua.lua_resume(co, L, 1);
        while (res === lua.LUA_YIELD && resumes < 64) { resumes++; res = lua.lua_resume(co, L, 0); }
      } else lua.lua_pop(co, 1);
    }
    if (res === lua.LUA_YIELD) outcome = 'yield';
    else if (res !== lua.LUA_OK) { outcome = 'error'; const eb = lua.lua_tostring(co, -1); err = eb ? to_jsstring(eb).slice(0, 120) : 'nonstring'; }
  }
  lua.lua_close(L);
  out[String(s.obj_id) + ':' + s.fn] = { outcome, err, calls };
}
fs.writeFileSync('/tmp/my-project/work/TDKR-Game/extraction/re/session38/s38_t6_fengari100.json', JSON.stringify(out, null, 1));
console.error('fengari logs written for ' + Object.keys(out).length + ' scripts');
