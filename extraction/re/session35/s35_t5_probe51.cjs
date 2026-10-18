// S35 T5: 5.1-vs-5.3 semantics probe on fengari (documenting what WOULD differ)
'use strict';
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;
function ev(code) {
  const L = lauxlib.luaL_newstate();
  lualib.luaL_openlibs(L);
  if (lauxlib.luaL_dostring(L, to_luastring('return ' + code)) !== lua.LUA_OK) {
    const e = lua.lua_tostring(L, -1);
    const r = e ? to_jsstring(e) : '(err)';
    lua.lua_close(L); return 'ERROR: ' + r;
  }
  lua.lua_getglobal(L, to_luastring('tostring'));
  lua.lua_insert(L, -2);
  lua.lua_call(L, 1, 1);
  const sv = lua.lua_tostring(L, -1);
  const out = sv ? to_jsstring(sv) : '(nonstr type ' + lua.lua_type(L, -1) + ')';
  lua.lua_close(L); return out;
}
const probes = [
  ['tostring(1.0)', '5.1: "1"  | 5.3/fengari: ' + ev('tostring(1.0)')],
  ['string.format("%d", 3.5)', '5.1: "3"  | 5.3: ERROR  | fengari: ' + ev('string.format("%d", 3.5)')],
  ['7/2', '5.1: 3.5 | 5.3: 3.5 | fengari: ' + ev('7/2')],
  ['7//2', '5.1: nil(// is comment!) | 5.3: 3 | fengari: ' + ev('7//2')],
  ['7%3', 'both 1 | fengari: ' + ev('7%3')],
  ['#t with holes', 'both: border (unspecified) | fengari: ' + ev('(function() local t={1,nil,3} return #t>=1 end)()')],
  ['"10"+1', 'both 11 | fengari: ' + ev('"10"+1')],
  ['"0x10"+0', '5.1: ERROR | 5.3: 16 | fengari: ' + ev('"0x10"+0')],
  ['type(os)', 'game script env: engine-controlled; fengari: ' + ev('type(os)')],
  ['type(io)', 'fengari: ' + ev('type(io)')],
];
for (const [c, r] of probes) console.log(c.padEnd(28), '->', r);
