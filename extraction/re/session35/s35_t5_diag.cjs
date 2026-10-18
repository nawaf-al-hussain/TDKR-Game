// S35 T5: diagnose all 55 failing scripts with deep error introspection
'use strict';
const fs = require('fs');
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;

const D = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s34_t4_scripts.json', 'utf8'));
const R = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s34_t4_results.json', 'utf8'));
const badIdx = R.results.filter(r => (r.err || '').startsWith('nonstr:102')).map(r => r.i);
console.log('failing indices:', badIdx.length);

function decode(u8) { return Array.from(u8).map(c => String.fromCharCode(c)).join(''); }

let summary = {};
for (const i of badIdx.slice(0, 12)) {
  const s = D.all_scripts[i];
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
  stub('ActorSetState');
  stub('GetTime', (Ls) => { lua.lua_pushnumber(L, 1000); return 1; });
  stub('ActorLookTo');
  stub('GetDistFromMC', (Ls) => { lua.lua_pushnumber(L, 5); return 1; });
  stub('Random', (Ls) => { lua.lua_pushnumber(L, 1); return 1; });

  let res = lauxlib.luaL_loadstring(L, to_luastring(s.script));
  const co = lua.lua_newthread(L);
  lua.lua_pushvalue(L, 1);
  lua.lua_xmove(L, co, 1);
  lua.lua_pop(L, 1);
  res = lua.lua_resume(co, L, 0);
  const where = res === lua.LUA_OK ? 'handler' : 'definition';
  let diag = { where, res };
  if (res === lua.LUA_OK && s.fn) {
    lua.lua_getglobal(co, to_luastring(s.fn));
    if (lua.lua_isfunction(co, -1)) {
      lua.lua_pushlightuserdata(co, null);
      res = lua.lua_resume(co, L, 1);
      let resumes = 0;
      while (res === lua.LUA_YIELD && resumes < 64) {
        resumes++;
        res = lua.lua_resume(co, L, 0);
      }
      diag.resumes = resumes;
    } else {
      diag.fn_missing = true;
      res = lua.LUA_OK;
    }
  }
  if (res !== lua.LUA_OK && res !== lua.LUA_YIELD) {
    const t = lua.lua_type(co, -1);
    diag.errtype = t;
    diag.errtypename = decode(lua.lua_typename(co, t));
    const eb = lua.lua_tostring(co, -1);
    diag.errstr = eb ? decode(eb).slice(0, 90) : null;
    if (t === lua.LUA_TFUNCTION) {
      // which function? compare against stubs
      for (const nm of ['Wait', 'IsCopAIEnabled', 'print', 'ActorSetState', 'GetTime']) {
        lua.lua_getglobal(co, to_luastring(nm));
        diag.isStub = lua.lua_rawequal(co, -1, -2) ? nm : (diag.isStub || null);
        lua.lua_pop(co, 1);
      }
    }
  }
  summary[i] = { fn: s.fn, hasWait: /\bWait\s*\(/.test(s.script), ...diag };
  lua.lua_close(L);
}
for (const [i, d] of Object.entries(summary)) {
  console.log(i, JSON.stringify(d));
}
