// _ZN13CAIController11Script_StopEiiP11CGameObject @ 0018c7ac

void _ZN13CAIController11Script_StopEiiP11CGameObject
               (int param_1,int param_2,int param_3,int *param_4)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int *piVar8;
  int iVar9;
  
  if (-1 < param_3) {
    if (0x18 < param_3) {
      return;
    }
    uVar4 = *(undefined4 *)(DAT_0018c900 + 0x18c7f0);
    uVar3 = *(undefined4 *)(*(int *)(param_1 + 0x74) + (param_2 * 0x19 + param_3) * 4);
    uVar1 = (**(code **)(*param_4 + 0x14))(param_4);
    _ZN17CLuaScriptManager12StopFunctionEii(uVar4,uVar3,uVar1,param_4);
    return;
  }
  iVar7 = 0;
  piVar8 = (int *)(DAT_0018c904 + 0x18c824);
  do {
    iVar5 = *piVar8;
    iVar9 = *(int *)(*(int *)(param_1 + 0x74) + param_2 * 100 + iVar7);
    iVar2 = (**(code **)(*param_4 + 0x14))(param_4);
    if (-1 < iVar9) {
      iVar6 = *(int *)(iVar5 + 0x54);
      iVar5 = 100;
      do {
        if ((iVar9 == *(int *)(iVar6 + 0x20)) && (iVar2 == *(int *)(iVar6 + 0x28))) {
          if ((*(int *)(iVar6 + 0xc) == 4) || (iVar2 = *(int *)(iVar6 + 8), iVar2 == 4)) {
            _ZN16EventManagerBase6detachEjP10IEventRecv
                      (**(undefined4 **)(DAT_0018c908 + 0x18c8f4),*(undefined4 *)(iVar6 + 0x14),
                       iVar6);
            iVar2 = *(int *)(iVar6 + 8);
          }
          if ((iVar2 != 0) && (*(char *)(iVar6 + 4) == '\0')) {
            *(undefined4 *)(iVar6 + 8) = 0;
            *(int *)(iVar6 + 0xc) = iVar2;
            *(undefined4 *)(iVar6 + 0x10) = 0;
            luaL_unref(*(undefined4 *)(iVar6 + 0x1c),0xffffd8f0,*(undefined4 *)(iVar6 + 0x24));
          }
          *(undefined4 *)(iVar6 + 0xc) = 0;
          break;
        }
        iVar5 = iVar5 + -1;
        iVar6 = iVar6 + 0x3c;
      } while (iVar5 != 0);
    }
    iVar7 = iVar7 + 4;
    if (iVar7 == 100) {
      return;
    }
  } while( true );
}

