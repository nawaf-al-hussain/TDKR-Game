// T6 smoke: walk the capsule through the patch area; verify trigger fire + Lua
'use strict';
const fs = require('fs');
const patch = JSON.parse(fs.readFileSync('/home/z/my-project/scripts/s35_t6_patch.json', 'utf8'));
const fengari = require('fengari');
const { lua, lauxlib, lualib, to_luastring, to_jsstring } = fengari;

// groundAt port
const G = 8.0, flat = patch.tris.flat, NT = patch.tris.n;
const grid = new Map();
for (let i = 0; i < NT; i++) {
  const ax=flat[i*9], ay=flat[i*9+1], bx=flat[i*9+3], by=flat[i*9+4], cx=flat[i*9+6], cy=flat[i*9+7];
  if (Math.abs((bx-ax)*(cy-ay)-(by-ay)*(cx-ax)) < 1e-6) continue;
  for (let gx=Math.floor(Math.min(ax,bx,cx)/G); gx<=Math.floor(Math.max(ax,bx,cx)/G); gx++)
    for (let gy=Math.floor(Math.min(ay,by,cy)/G); gy<=Math.floor(Math.max(ay,by,cy)/G); gy++) {
      const k = gx+':'+gy;
      if (!grid.has(k)) grid.set(k, []);
      grid.get(k).push(i);
    }
}
function groundAt(x, y, zref, up=1.2) {
  const gx=Math.floor(x/G), gy=Math.floor(y/G);
  let best=-1e9;
  for (let dx=-1;dx<=1;dx++) for (let dy=-1;dy<=1;dy++) {
    const cell=grid.get((gx+dx)+':'+(gy+dy)); if(!cell) continue;
    for (const i of cell) {
      const ax=flat[i*9],ay=flat[i*9+1],az=flat[i*9+2];
      const bx=flat[i*9+3],by=flat[i*9+4],bz=flat[i*9+5];
      const cx=flat[i*9+6],cy=flat[i*9+7],cz=flat[i*9+8];
      const det=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy);
      if(Math.abs(det)<1e-9) continue;
      const l1=((by-cy)*(x-cx)+(cx-bx)*(y-cy))/det;
      const l2=((cy-ay)*(x-cx)+(ax-cx)*(y-cy))/det;
      const l3=1-l1-l2;
      if(l1>=-0.02&&l2>=-0.02&&l3>=-0.02){
        const z=l1*az+l2*bz+l3*cz;
        if(z<=zref+up&&z>best)best=z;
      }
    }
  }
  return best;
}
// walk from spawn north through the batcave trigger
const spawn = patch.spawns[0].pos;
const B = 1.5;
const fired = new Set(); let steps = 0, groundOK = 0;
const luaLogTotal = [];
for (let d = 0; d < 40; d += 0.5) {
  const x = spawn[0] - 1.0 * d, y = spawn[1] - 1.0 * d;  // walk southwest
  const gz = groundAt(x, y, 5, 1.2);
  if (gz > -1e8) groundOK++;
  const z = (gz > -1e8 ? gz : spawn[2]) + 0.9;
  for (const t of patch.triggers) {
    if (!t.has_script || fired.has(t.id)) continue;
    const s = Math.max(t.scale[0], 0.2), sz = Math.max(t.scale[2], 0.2);
    const dh = Math.hypot(x - t.pos[0], y - t.pos[1]);
    const dz = Math.abs(z - 0.9 - t.pos[2]);
    if (dh < B * s && dz < B * sz) {
      fired.add(t.id);
      const luaLog = [];
      const L = lauxlib.luaL_newstate();
      lualib.luaL_openlibs(L);
      const stub = (name, fn) => {
        lua.lua_pushcfunction(L, function(Ls) {
          const n = lua.lua_gettop(Ls); const args = [];
          for (let i = 1; i <= n; i++) {
            const tp = lua.lua_type(Ls, i);
            if (tp === lua.LUA_TNUMBER) args.push(+lua.lua_tonumber(Ls, i).toFixed(2));
            else if (tp === lua.LUA_TSTRING) args.push(to_jsstring(lua.lua_tolstring(Ls, i)));
            else if (tp === lua.LUA_TBOOLEAN) args.push(!!lua.lua_toboolean(Ls, i));
          }
          luaLog.push(name + '(' + args.join(', ') + ')');
          if (fn) return fn(Ls, args);
          return 0;
        });
        lua.lua_setglobal(L, to_luastring(name));
      };
      stub('Wait', (Ls) => lua.lua_yield(Ls, 0));
      for (const nm of ['StartFadeOut','StartFadeIn','RequireLoadLevel','Enable','Disable',
        'ShowObject','HideObject','ShowMessage','ObjectiveAdd','ObjectiveRemove',
        'ShowObjectiveMessage','ClearObjectiveMessage','StartSound','ActorSetState',
        'ActorLookTo','SetActorSpeedWalk','KillActor','GiveDamage','StartMainStoryFromQuestId',
        'NextMission','SetQuestEnabled','SaveGame','MissionFailed']) stub(nm);
      stub('GetTime', (Ls) => { lua.lua_pushnumber(Ls, 1000); return 1; });
      stub('IsDead', (Ls) => { lua.lua_pushboolean(Ls, false); return 1; });
      stub('Random', (Ls) => { lua.lua_pushnumber(Ls, 1); return 1; });
      stub('IsCopAIEnabled', (Ls) => { lua.lua_pushboolean(Ls, false); return 1; });
      stub('print', () => 0);
      const co = lua.lua_newthread(L);
      if (lauxlib.luaL_dostring(co, to_luastring(t.script)) === lua.LUA_OK) {
        lua.lua_getglobal(co, to_luastring(t.fn));
        if (lua.lua_isfunction(co, -1)) {
          lua.lua_pushlightuserdata(co, null);
          let res = lua.lua_resume(co, L, 1), n = 0;
          while (res === lua.LUA_YIELD && n < 32) { n++; res = lua.lua_resume(co, L, 0); }
        }
      }
      luaLogTotal.push({ trigger: t.id, fn: t.fn, calls: luaLog });
    }
  }
  steps++;
}
console.log(`walk: ${steps} steps, ground found ${groundOK}/${steps}`);
console.log(`triggers fired: ${fired.size}: ${[...fired].join(', ')}`);
for (const f of luaLogTotal.slice(0, 4)) {
  console.log(`  ${f.fn} (${f.trigger}): ${f.calls.slice(0, 6).join(' -> ')}`);
}
