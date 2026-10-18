// S33 T4: run 10 extracted TDKR Lua trigger scripts in fengari with stubbed
// API + logging; Wait = scheduler (coroutine yield); fire OnEnter with a
// fake actor; tick the scheduler to completion; report per-script results.
'use strict';
const fs = require('fs');
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;

const picked = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s33lua/picked10.json', 'utf8'));

const L = lauxlib.luaL_newstate();
lualib.luaL_openlibs(L);

const calls = [];           // global call log
let waitCount = 0;

function stub(name, extra) {
  lua.lua_pushcfunction(L, function(Ls) {
    const n = lua.lua_gettop(Ls);
    const args = [];
    for (let i = 1; i <= n; i++) {
      const t = lua.lua_type(Ls, i);
      if (t === lua.LUA_TNUMBER) args.push(lua.lua_tonumber(Ls, i));
      else if (t === lua.LUA_TSTRING) args.push(to_jsstring(lua.lua_tolstring(Ls, i)));
      else if (t === lua.LUA_TBOOLEAN) args.push(lua.lua_toboolean(Ls, i));
      else args.push('ptr:' + lua.lua_type(Ls, i));
    }
    calls.push({ api: name, args });
    if (extra) return extra(Ls, args);
    return 0;
  });
  lua.lua_setglobal(L, to_luastring(name));
}

// Wait: yields (scheduler resumes); records the wait duration
stub('Wait', (Ls, args) => {
  waitCount++;
  return lua.lua_yield(Ls, 0);
});
// Enable/Disable: (objId) or (objId, state)
stub('Enable'); stub('Disable');
stub('ShowMessage'); stub('ShowObject'); stub('HideObject');
stub('ActorSetState'); stub('SpawnObject'); stub('KillActor');
stub('ActorLookTo'); stub('SetActorSpeedWalk'); stub('NPCGoToPath');
stub('StartFadeOut'); stub('StartFadeIn');
stub('ObjectiveAdd'); stub('ObjectiveRemove'); stub('ShowObjectiveMessage');
stub('CameraFollowObject'); stub('HideOccluder'); stub('ShowOccluder');
stub('Show'); stub('Hide'); stub('PlaySound'); stub('StopSound');
stub('SetVariable'); stub('GetVariable', (Ls) => {
  lua.lua_pushnumber(Ls, 0); return 1;
});
stub('Random', (Ls) => { lua.lua_pushnumber(Ls, 1); return 1; });
stub('GetActor', (Ls) => { lua.lua_pushnumber(Ls, 1); return 1; });
stub('IsInside', (Ls) => { lua.lua_pushboolean(Ls, 1); return 1; });

// minimal scheduler: resume yields up to N ticks
function callHandle(fn, objId) {
  lua.lua_getglobal(L, to_luastring(fn));
  if (lua.lua_isfunction(L, -1) === 0) { lua.lua_pop(L, 1); return null; }
  lua.lua_pushnumber(L, objId);      // arg: the trigger/object id
  let status = lua.lua_pcall(L, 1, 0, 0);
  if (status !== lua.LUA_OK) {
    const err = to_jsstring(lua.lua_tostring(L, -1));
    lua.lua_pop(L, 1);
    return { error: err };
  }
  return { ok: true };
}

function resumeThread() {
  // after a yield inside pcall, the main coroutine status = LUA_YIELD
  let status = lua.lua_status(L);
  let ticks = 0;
  while (status === lua.LUA_YIELD && ticks < 100) {
    status = lua.lua_resume(L, null, 0);
    ticks++;
  }
  return { ticks, status };
}

const results = [];
for (const e of picked) {
  const pre = calls.length;
  const w0 = waitCount;
  let r;
  const load = lauxlib.luaL_dostring(L, to_luastring(e.script));
  if (load !== lua.LUA_OK) {
    results.push({ objId: e.objId, loaded: false,
      error: to_jsstring(lua.lua_tostring(L, -1)) });
    lua.lua_pop(L, 1);
    continue;
  }
  const entry = /function\s+Obj(\d+)_OnEnter/.test(e.script) ? 'OnEnter'
    : (/OnReach/.test(e.script) ? 'OnReach' : 'OnEnter');
  r = callHandle(`Obj${e.objId}_${entry}`, e.objId);
  let sched = null;
  if (r && r.ok) sched = resumeThread();
  if (r === null) {
    results.push({ objId: e.objId, loaded: true, error: `no Obj${e.objId}_${entry}` });
  } else if (r.error) {
    results.push({ objId: e.objId, loaded: true, error: r.error });
  } else {
    results.push({
      objId: e.objId, loaded: true, ok: true,
      entry, schedulerTicks: sched.ticks,
      finalStatus: sched.status === lua.LUA_OK ? 'LUA_OK' : String(sched.status),
      apiCalls: calls.slice(pre).map(c => `${c.api}(${c.args.join(', ')})`),
      waits: waitCount - w0,
    });
  }
}
console.log(JSON.stringify(results, null, 1));
const okN = results.filter(r => r.ok).length;
console.error(`\nSUMMARY: ${okN}/10 ran to completion; ` +
  `errors: ${results.filter(r => r.error).map(r => r.objId + ': ' + r.error).join(' | ')}`);
