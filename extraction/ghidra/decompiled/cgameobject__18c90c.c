// _ZN13CAIController16Script_IsRunningEiiP11CGameObject @ 0018c90c

undefined4
_ZN13CAIController16Script_IsRunningEiiP11CGameObject
          (int param_1,int param_2,int param_3,int *param_4)

{
  undefined4 uVar1;
  int iVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int *piVar9;
  
  if (-1 < param_3) {
    if (0x18 < param_3) {
      return 0;
    }
    uVar5 = *(undefined4 *)(DAT_0018ca0c + 0x18c958);
    uVar4 = *(undefined4 *)(*(int *)(param_1 + 0x74) + (param_2 * 0x19 + param_3) * 4);
    uVar1 = (**(code **)(*param_4 + 0x14))(param_4);
    uVar1 = _ZN17CLuaScriptManager17IsFunctionRunningEii(uVar5,uVar4,uVar1);
    return uVar1;
  }
  iVar8 = 0;
  piVar9 = (int *)(DAT_0018ca10 + 0x18c988);
  do {
    iVar7 = *piVar9;
    iVar6 = *(int *)(*(int *)(param_1 + 0x74) + param_2 * 100 + iVar8);
    iVar2 = (**(code **)(*param_4 + 0x14))(param_4);
    if (-1 < iVar6) {
      iVar3 = *(int *)(iVar7 + 0x54);
      iVar7 = 0;
      do {
        iVar7 = iVar7 + 1;
        if (((*(int *)(iVar3 + 8) != 0) && (iVar6 == *(int *)(iVar3 + 0x20))) &&
           (iVar2 == *(int *)(iVar3 + 0x28))) {
          return 1;
        }
        iVar3 = iVar3 + 0x3c;
      } while (iVar7 != 100);
    }
    iVar8 = iVar8 + 4;
    if (iVar8 == 100) {
      return 0;
    }
  } while( true );
}

