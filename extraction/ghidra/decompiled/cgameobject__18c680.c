// _ZN13CAIController12Script_StartESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEP11CGameObjectiP11ScriptParami @ 0018c680

int _ZN13CAIController12Script_StartESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEP11CGameObjectiP11ScriptParami
              (undefined4 param_1,undefined4 *param_2,int *param_3,undefined4 param_4,
              undefined4 param_5,undefined4 param_6)

{
  int iVar1;
  undefined4 uVar2;
  int *piVar3;
  int iVar4;
  int *piVar5;
  
  piVar3 = (int *)(DAT_0018c728 + 0x18c6a0);
  iVar4 = *piVar3;
  lua_getfield(*(undefined4 *)(iVar4 + 0x50),0xffffd8ee,*param_2);
  iVar1 = luaL_ref(*(undefined4 *)(iVar4 + 0x50),0xffffd8f0);
  lua_settop(*(undefined4 *)(iVar4 + 0x50),0);
  if (-1 < iVar1) {
    if (param_3 == (int *)0x0) {
      piVar5 = (int *)0x0;
    }
    else {
      piVar5 = param_3 + 0xd;
    }
    iVar4 = *piVar3;
    uVar2 = (**(code **)(*param_3 + 0x14))(param_3);
    iVar1 = _ZN17CLuaScriptManager13StartFunctionEiiP11ScriptParamP15CGameObjectBaseiii_constprop_3137
                      (iVar4,iVar1,param_4,param_5,piVar5,uVar2,param_6);
  }
  return iVar1;
}

