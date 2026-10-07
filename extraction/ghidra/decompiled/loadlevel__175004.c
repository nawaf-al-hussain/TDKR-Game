// _Z16RequireLoadLevelP9lua_State @ 00175004

undefined4 _Z16RequireLoadLevelP9lua_State(undefined4 param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined1 auStack_14 [8];
  
  uVar1 = lua_tolstring(param_1,1,auStack_14);
  iVar2 = lua_gettop(param_1);
  if (iVar2 < 2) {
    uVar4 = 0xffffffff;
  }
  else {
    uVar4 = lua_tointeger(param_1,2);
  }
  uVar3 = _ZN11Application11GetInstanceEv();
  _ZN11Application16RequireLoadLevelEPKci(uVar3,uVar1,uVar4);
  return 0;
}

