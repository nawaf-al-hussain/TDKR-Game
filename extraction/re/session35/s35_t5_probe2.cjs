// S35 T5: exact r34 flow reproduction for a failing script
'use strict';
const fs = require('fs');
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;

const D = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s34_t4_scripts.json', 'utf8'));
const s = D.all_scripts[33];   // Obj315304_Always (one of the 55)

const L = lauxlib.luaL_newstate();
lualib.luaL_openlibs(L);
const stub = (name, fn) => {
  lua.lua_pushcfunction(L, function(Ls) {
    if (fn) return fn(Ls);
    return 0;
  });
  lua.lua_setglobal(L, to_luastring(name));
};
stub('Wait', (Ls) => { return lua.lua_yield(Ls, 0); });
stub('IsCopAIEnabled', (Ls) => { lua.lua_pushboolean(L, false); return 1; });
stub('print', () => 0);

const status = lauxlib.luaL_loadstring(L, to_luastring(s.script));
const co = lua.lua_newthread(L);
lua.lua_pushvalue(L, 1);
lua.lua_xmove(L, co, 1);
lua.lua_pop(L, 1);
let res = lua.lua_resume(co, L, 0);
console.log('resume1:', res, '(0=OK,1=YIELD)');
console.log('global fn type:', lua.lua_type(co, -1));
lua.lua_settop(co, 0);
if (res === lua.LUA_OK) {
  lua.lua_getglobal(co, to_luastring(s.fn));
  const ft = lua.lua_type(co, -1);
  console.log('handler type:', ft);
  if (lua.lua_isfunction(co, -1)) {
    lua.lua_pushlightuserdata(co, null);
    res = lua.lua_resume(co, L, 1);
    let resumes = 0;
    while (res === lua.LUA_YIELD && resumes < 64) {
      resumes++;
      res = lua.lua_resume(co, L, 0);
    }
    console.log('final res:', res, 'after', resumes, 'resumes');
    if (res !== lua.LUA_OK && res !== lua.LUA_YIELD) {
      const t = lua.lua_type(co, -1);
      const tn = lua.lua_typename(co, t);
      console.log('error obj type:', t, 'typename bytes:', Array.from(tn).map(c => String.fromCharCode(c)).join(''));
      const eb = lua.lua_tostring(co, -1);
      console.log('lua_tostring:', eb ? Array.from(eb).map(c => String.fromCharCode(c)).join('') : '(null, not a string)');
      if (t === lua.LUA_TFUNCTION) {
        console.log('>>> error object IS a function: fengari raises the C function itself?');
        // check if it is one of our stubs
        lua.lua_getglobal(co, to_luastring('Wait'));
        console.log('is it Wait?', lua.lua_rawequal(co, -1, -2));
      }
    }
  }
}
