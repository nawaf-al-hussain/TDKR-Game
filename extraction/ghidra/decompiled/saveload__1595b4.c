// _ZN17CLuaScriptManager8SaveLoadEP13CMemoryStreamb @ 001595b4

/* WARNING: Removing unreachable block (ram,0x00a59180) */

void _ZN17CLuaScriptManager8SaveLoadEP13CMemoryStreamb(int param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  int iVar4;
  
  _ZN17CLuaScriptManager11StopThreadsEv();
  iVar4 = 0;
  lua_settop(*(undefined4 *)(param_1 + 0x50),0);
  lua_getfield(*(undefined4 *)(param_1 + 0x50),0xffffd8ee,DAT_00159668 + 0x1595ec);
  _ZN13CMemoryStream8ReadCharEv(param_2);
  _ZN17CLuaScriptManager22ReadLuaTableFromStreamEP9lua_StateP13CMemoryStream
            (param_1,*(undefined4 *)(param_1 + 0x50),param_2);
  lua_settop(*(undefined4 *)(param_1 + 0x50),0xfffffffe);
  _ZN13CMemoryStream7ReadIntEv(param_2);
  do {
    iVar1 = *(int *)(param_1 + 0x54) + iVar4;
    iVar4 = iVar4 + 0x3c;
    *(undefined4 *)(iVar1 + 0x1c) = *(undefined4 *)(param_1 + 0x50);
    _ZN9LuaThread8SaveLoadEP13CMemoryStream(iVar1,param_2);
  } while (iVar4 != 6000);
  if (param_3 == 0) {
    _ZN17CLuaScriptManager18ResetLuaGlobalVarsEP9lua_State(param_1,*(undefined4 *)(param_1 + 0x50));
  }
  iVar4 = *(int *)(param_1 + 0x50);
  uVar2 = *(uint *)(iVar4 + 0xc);
  for (uVar3 = *(uint *)(iVar4 + 8); uVar3 < uVar2; uVar3 = uVar3 + 8) {
    *(undefined4 *)(uVar3 + 4) = 0;
  }
  *(uint *)(iVar4 + 8) = uVar2;
  return;
}


