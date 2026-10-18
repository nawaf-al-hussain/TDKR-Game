// S33 T4 v2: per-trigger coroutine; known stubs + auto-stub fallback that
// logs MISSING APIs; Wait = scheduler yield; reports completion + call log.
'use strict';
const fs = require('fs');
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;

const picked = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s33lua/picked10.json', 'utf8'));

const KNOWN = new Set(['Wait', 'Enable', 'Disable', 'ShowMessage', 'ShowObject',
  'HideObject', 'ActorSetState', 'HideOccluder', 'ShowOccluder', 'Show', 'Hide',
  'GetVariable', 'Random', 'GetActor', 'IsInside']);

const results = [];
for (const e of picked) {
  // fresh state per trigger (isolated)
  const L = lauxlib.luaL_newstate();
  lualib.luaL_openlibs(L);
  const calls = [], missing = new Set();
  function pushStub(Ls, name, isMissing) {
    if (isMissing) missing.add(name);
    lua.lua_pushcfunction(Ls, function(Ls2) {
      const n = lua.lua_gettop(Ls2);
      const args = [];
      for (let i = 1; i <= n; i++) {
        const t = lua.lua_type(Ls2, i);
        if (t === lua.LUA_TNUMBER) args.push(+lua.lua_tonumber(Ls2, i).toFixed(4));
        else if (t === lua.LUA_TSTRING) args.push(JSON.stringify(to_jsstring(lua.lua_tolstring(Ls2, i))));
        else if (t === lua.LUA_TBOOLEAN) args.push(!!lua.lua_toboolean(Ls2, i));
        else args.push(`<${lua.lua_type(Ls2, i) === lua.LUA_TTABLE ? 'table' : 'ptr'}>`);
      }
      calls.push(`${isMissing ? 'MISSING:' : ''}${name}(${args.join(', ')})`);
      if (name === 'Wait') return lua.lua_yield(Ls2, 0);
      if (name === 'GetVariable' || name === 'Random' || name === 'GetActor') {
        lua.lua_pushnumber(Ls2, 1); return 1;
      }
      if (name === 'IsInside' || name === 'ActorIsInStateType') {
        lua.lua_pushboolean(Ls2, 1); return 1;
      }
      return 0;
    });
    lua.lua_setglobal(Ls, to_luastring(name));
  }
  for (const k of KNOWN) pushStub(L, k, false);
  // auto-stub: pre-scan the script for called globals not in KNOWN
  for (const m of e.script.matchAll(/(?<![\w.:])([A-Za-z_][A-Za-z0-9_]*)\s*\(/g)) {
    const nm = m[1];
    if (nm === 'function' || nm === 'if' || nm === 'for' || nm === 'while' ||
        nm === 'print' || nm === 'return') continue;
    if (/^Obj\d+_/.test(nm)) continue;   // script's own handlers
    if (new RegExp('function\\s+' + nm + '\\s*\\(').test(e.script)) continue;
    if (!KNOWN.has(nm)) pushStub(L, nm, true);
  }
  pushStub(L, 'print', false);
  // print goes to console (not logged as API call)
  lua.lua_pushcfunction(L, function() { return 0; });
  lua.lua_setglobal(L, to_luastring('print'));

  // load + run in a thread
  const TH = lua.lua_newthread(L);
  let rc = lauxlib.luaL_dostring(TH, to_luastring(e.script));
  if (rc !== lua.LUA_OK) {
    results.push({ objId: e.objId, loaded: false, error: to_jsstring(lua.lua_tostring(TH, -1)) });
    lua.lua_close(L);
    continue;
  }
  const entry = /function\s+Obj\d+_OnEnter/.test(e.script) ? 'OnEnter'
    : (/OnReach/.test(e.script) ? 'OnReach' : 'OnEnter');
  lua.lua_getglobal(TH, to_luastring(`Obj${e.objId}_${entry}`));
  let status;
  if (lua.lua_isfunction(TH, -1) === 0) {
    results.push({ objId: e.objId, loaded: true, error: `no handler Obj${e.objId}_${entry}` });
    lua.lua_close(L);
    continue;
  }
  lua.lua_pushnumber(TH, e.objId);        // arg 1: object id (as the engine passes)
  lua.lua_pushnumber(TH, 7777);           // arg 2: the capsule/actor id entering
  const t0 = calls.length;
  let ticks = 0;
  status = lua.lua_resume(TH, null, 2);
  while (status === lua.LUA_YIELD && ticks < 64) {
    status = lua.lua_resume(TH, null, 0);
    ticks++;
  }
  const rec = { objId: e.objId, entry, loaded: true };
  if (status === lua.LUA_OK) {
    rec.ok = true;
    rec.schedulerTicks = ticks;
    rec.waits = calls.slice(t0).filter(c => c === 'Wait()' || c.startsWith('Wait(')).length;
  } else {
    rec.error = to_jsstring(lua.lua_tostring(TH, -1));
  }
  rec.apiCalls = calls.slice(t0);
  rec.missing = [...missing];
  results.push(rec);
  lua.lua_close(L);
}
const okN = results.filter(r => r.ok).length;
console.log(JSON.stringify(results, null, 1));
console.error(`\nSUMMARY: ${okN}/10 ran to completion`);
console.error('missing APIs across the 10:', [...new Set(results.flatMap(r => r.missing || []))].join(', '));
