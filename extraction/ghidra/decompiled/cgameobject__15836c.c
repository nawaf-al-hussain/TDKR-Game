// _ZN17CLuaScriptManager13StartFunctionEiiP11ScriptParamP15CGameObjectBaseiii @ 0015836c

int _ZN17CLuaScriptManager13StartFunctionEiiP11ScriptParamP15CGameObjectBaseiii
              (int param_1,int param_2,int param_3,char *param_4,undefined4 param_5,int param_6,
              undefined4 param_7,undefined4 param_8)

{
  char *pcVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  int iVar5;
  int iVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  int iVar9;
  int iVar10;
  undefined4 uVar11;
  undefined4 uVar12;
  
  if (param_2 < 0) {
    iVar9 = -3;
  }
  else {
    iVar6 = *(int *)(param_1 + 0x54);
    iVar5 = 0;
    iVar9 = -1;
    do {
      while (*(int *)(iVar6 + 8) != 0) {
        if ((*(int *)(iVar6 + 0x20) == param_2) && (*(int *)(iVar6 + 0x28) == param_6)) {
          return -2;
        }
        iVar5 = iVar5 + 1;
        iVar6 = iVar6 + 0x3c;
        if (iVar5 == 100) goto LAB_001583dc;
      }
      iVar6 = iVar6 + 0x3c;
      if (iVar9 == -1) {
        iVar9 = iVar5;
      }
      iVar5 = iVar5 + 1;
    } while (iVar5 != 100);
LAB_001583dc:
    if (iVar9 == -1) {
      lua_settop(*(undefined4 *)(param_1 + 0x50),0);
      iVar9 = -3;
    }
    else {
      lua_getfield(*(undefined4 *)(param_1 + 0x50),0xffffd8ee,DAT_00158614 + 0x1583fc);
      uVar2 = lua_tointeger(*(undefined4 *)(param_1 + 0x50),0xffffffff);
      iVar10 = 0;
      lua_getfield(*(undefined4 *)(param_1 + 0x50),0xffffd8ee,DAT_00158618 + 0x158424);
      uVar3 = lua_tointeger(*(undefined4 *)(param_1 + 0x50),0xffffffff);
      uVar12 = *(undefined4 *)(param_1 + 0x50);
      iVar6 = *(int *)(param_1 + 0x54) + iVar9 * 0x3c;
      uVar7 = *(undefined4 *)(param_1 + 0x30);
      *(int *)(param_1 + 0x30) = iVar9;
      uVar8 = *(undefined4 *)(param_1 + 0x5c);
      *(int *)(iVar6 + 0x28) = param_6;
      iVar5 = DAT_0015861c;
      *(undefined4 *)(iVar6 + 0x10) = 0;
      uVar11 = *(undefined4 *)(iVar5 + 0x158474);
      *(undefined1 *)(iVar6 + 4) = 0;
      *(undefined4 *)(iVar6 + 0x1c) = uVar12;
      *(undefined4 *)(iVar6 + 0x2c) = param_5;
      *(undefined4 *)(iVar6 + 0x30) = param_7;
      *(undefined4 *)(iVar6 + 0x34) = param_8;
      *(undefined4 *)(iVar6 + 8) = 1;
      *(undefined4 *)(iVar6 + 0x24) = 0xfffffffe;
      uVar4 = lua_newthread(uVar12);
      *(undefined4 *)(iVar6 + 0x18) = uVar4;
      uVar4 = luaL_ref(uVar12,0xffffd8f0);
      *(int *)(iVar6 + 0x20) = param_2;
      *(undefined4 *)(iVar6 + 0x24) = uVar4;
      lua_rawgeti(*(undefined4 *)(iVar6 + 0x18),0xffffd8f0,param_2);
      iVar5 = lua_type(*(undefined4 *)(iVar6 + 0x18),0xffffffff);
      if (iVar5 == 0) {
        lua_settop(*(undefined4 *)(iVar6 + 0x18),0xfffffffe);
        luaL_unref(*(undefined4 *)(iVar6 + 0x1c),0xffffd8f0,*(undefined4 *)(iVar6 + 0x24));
        *(undefined4 *)(iVar6 + 8) = 0;
      }
      else {
        if (0 < param_3) {
          do {
            while (*param_4 != '\0') {
              if (*param_4 == '\x01') {
                lua_pushnumber(*(undefined4 *)(iVar6 + 0x18),*(undefined4 *)(param_4 + 4));
              }
              iVar10 = iVar10 + 1;
              param_4 = param_4 + 8;
              if (iVar10 == param_3) goto LAB_00158544;
            }
            pcVar1 = param_4 + 4;
            iVar10 = iVar10 + 1;
            param_4 = param_4 + 8;
            lua_pushinteger(*(undefined4 *)(iVar6 + 0x18),*(undefined4 *)pcVar1);
          } while (iVar10 != param_3);
        }
LAB_00158544:
        _ZN9LuaThread6ResumeEi(iVar6,param_3);
      }
      _ZN17CLuaScriptManager9SetGlobalEPKcib(param_1,DAT_00158620 + 0x158568,uVar2,0);
      _ZN17CLuaScriptManager9SetGlobalEPKcib(param_1,DAT_00158624 + 0x15857c,uVar3,0);
      iVar5 = DAT_00158628;
      uVar2 = *(undefined4 *)(param_1 + 0x50);
      *(undefined4 *)(param_1 + 0x5c) = uVar8;
      *(undefined4 *)(iVar5 + 0x15859c) = uVar11;
      *(undefined4 *)(param_1 + 0x30) = uVar7;
      lua_settop(uVar2,0);
    }
  }
  return iVar9;
}

