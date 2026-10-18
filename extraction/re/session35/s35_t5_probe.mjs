// S35 T5: reproduce the "non-string error object" failure with full introspection
'use strict';
const fs = require('fs');
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;

const D = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s34_t4_scripts.json', 'utf8'));
const s = D.all_scripts[61];   // Obj412094_OnReach — one of the 55

const L = lauxlib.luaL_newstate();
lualib.luaL_openlibs(L);
const stub = (name, fn) => {
  lua.lua_pushcfunction(L, function(Ls) {
    if (fn) return fn(Ls);
    return 0;
  });
  lua.lua_setglobal(L, to_luastring(name));
};
stub('ActorSetState');
stub('GetTime', (Ls) => { lua.lua_pushnumber(L, 1000); return 1; });
stub('Wait', (Ls) => { return lua.lua_yield(Ls, 0); });

// message handler for traceback
lua.lua_pushcfunction(L, function(Ls) {
  lauxlib.luaL_traceback(Ls, Ls, null, 0);
  const tb = lua.lua_tostring(Ls, -1);
  console.log('TRACEBACK:', tb ? to_jsstring(tb) : '(null)');
  return 1;
});
const HANDLER = lua.lua_gettop(L);

const status = lauxlib.luaL_loadstring(L, to_luastring(s.script));
console.log('load status', status);
const co = lua.lua_newthread(L);
lua.lua_pushvalue(L, 1);
lua.lua_xmove(L, co, 1);
lua.lua_pop(L, 1);
let res = lua.lua_resume(co, L, 0);
console.log('resume1', res);
if (res === lua.LUA_OK) {
  lua.lua_getglobal(co, to_luastring(s.fn));
  console.log('fn type', lua.lua_type(co, -1), lua.lua_typename(co, lua.lua_type(co, -1)));
  lua.lua_pushlightuserdata(co, null);
  // resume with error handler: put handler below args? fengari lua_resume(co, from, nargs)
  res = lua.lua_resume(co, L, 1);
  console.log('resume2', res);
  if (res !== lua.LUA_OK && res !== lua.LUA_YIELD) {
    const t = lua.lua_type(co, -1);
    console.log('error object type:', t, lua.lua_typename(co, t));
    const sv = lua.lua_tostring(co, -1);
    console.log('tostring ->', sv ? to_jsstring(sv) : null);
    if (t === lua.LUA_TSTRING) {
      const raw = lua.lua_tolstring(co, -1);
      console.log('raw bytes:', Array.from(raw).map(c => String.fromCharCode(c)).join(''));
    }
    // call tostring() on it via the base lib
    lua.lua_getglobal(co, to_luastring('tostring'));
    lua.lua_pushvalue(co, -2);
    if (lua.lua_pcall(co, 1, 1, 0) === lua.LUA_OK) {
      const s2 = lua.lua_tostring(co, -1);
      console.log('builtin tostring ->', s2 ? to_jsstring(s2) : '(null)');
    } else {
      console.log('builtin tostring errored');
    }
  }
}
