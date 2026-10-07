// _ZN13CAIController12Script_StartEiiP11CGameObjectiP11ScriptParami @ 0018c72c

int _ZN13CAIController12Script_StartEiiP11CGameObjectiP11ScriptParami
              (int param_1,int param_2,int param_3,int *param_4,undefined4 param_5,
              undefined4 param_6)

{
  undefined4 uVar1;
  int iVar2;
  
  iVar2 = *(int *)(*(int *)(param_1 + 0x74) + (param_2 * 0x19 + param_3) * 4);
  if (iVar2 < 0) {
    return iVar2;
  }
  uVar1 = *(undefined4 *)(DAT_0018c7a8 + 0x18c77c);
  (**(code **)(*param_4 + 0x14))(param_4);
  iVar2 = _ZN17CLuaScriptManager13StartFunctionEiiP11ScriptParamP15CGameObjectBaseiii_constprop_3137
                    (uVar1,iVar2,param_5,param_6);
  return iVar2;
}

