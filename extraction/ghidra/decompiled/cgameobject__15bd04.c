// _ZN9LuaThread5StartEP9lua_StateiiP11ScriptParamP15CGameObjectBaseiii @ 0015bd04

undefined4
_ZN9LuaThread5StartEP9lua_StateiiP11ScriptParamP15CGameObjectBaseiii
          (int param_1,undefined4 param_2,undefined4 param_3,int param_4,char *param_5,
          undefined4 param_6,undefined4 param_7,undefined4 param_8,undefined4 param_9)

{
  char *pcVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  
  *(undefined4 *)(param_1 + 0x1c) = param_2;
  iVar4 = 0;
  *(undefined4 *)(param_1 + 0x28) = param_7;
  *(undefined1 *)(param_1 + 4) = 0;
  *(undefined4 *)(param_1 + 8) = 1;
  *(undefined4 *)(param_1 + 0x2c) = param_6;
  *(undefined4 *)(param_1 + 0x24) = 0xfffffffe;
  *(undefined4 *)(param_1 + 0x30) = param_8;
  *(undefined4 *)(param_1 + 0x10) = 0;
  *(undefined4 *)(param_1 + 0x34) = param_9;
  uVar2 = lua_newthread(param_2);
  *(undefined4 *)(param_1 + 0x18) = uVar2;
  uVar2 = luaL_ref(param_2,0xffffd8f0);
  *(undefined4 *)(param_1 + 0x20) = param_3;
  *(undefined4 *)(param_1 + 0x24) = uVar2;
  lua_rawgeti(*(undefined4 *)(param_1 + 0x18),0xffffd8f0,param_3);
  iVar3 = lua_type(*(undefined4 *)(param_1 + 0x18),0xffffffff);
  if (iVar3 == 0) {
    lua_settop(*(undefined4 *)(param_1 + 0x18),0xfffffffe);
    luaL_unref(*(undefined4 *)(param_1 + 0x1c),0xffffd8f0,*(undefined4 *)(param_1 + 0x24));
    *(undefined4 *)(param_1 + 8) = 0;
    return 1;
  }
  if (0 < param_4) {
    do {
      while (*param_5 != '\0') {
        if (*param_5 == '\x01') {
          lua_pushnumber(*(undefined4 *)(param_1 + 0x18),*(undefined4 *)(param_5 + 4));
        }
        iVar4 = iVar4 + 1;
        param_5 = param_5 + 8;
        if (iVar4 == param_4) goto LAB_0015bdf8;
      }
      pcVar1 = param_5 + 4;
      iVar4 = iVar4 + 1;
      param_5 = param_5 + 8;
      lua_pushinteger(*(undefined4 *)(param_1 + 0x18),*(undefined4 *)pcVar1);
    } while (iVar4 != param_4);
  }
LAB_0015bdf8:
  _ZN9LuaThread6ResumeEi(param_1,param_4);
  return 0;
}

