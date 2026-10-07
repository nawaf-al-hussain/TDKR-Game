// _ZN11Application4QuitEv @ 003ea744

void _ZN11Application4QuitEv(int param_1)

{
  undefined4 uVar1;
  undefined4 extraout_r0;
  int iVar2;
  int *piVar3;
  int iVar4;
  int *piVar5;
  undefined4 *puVar6;
  uint in_fpscr;
  float __x;
  undefined1 auStack_50 [56];
  
  iVar2 = DAT_003ea9f8 + 0x3ea768;
  if (*(int *)(DAT_003ea9f4 + 0x3ea754) != 0) {
    _ZN13CMemoryStreamC1Ei(auStack_50,0x400);
    _ZN13CMemoryStream8WriteIntEi
              (auStack_50,*(undefined4 *)((int)&__DT_SYMTAB[0x1e0].st_size + param_1));
    uVar1 = _ZN3glf22AndroidGetMillisecondsEv();
    VectorSignedToFloat(uVar1,(byte)(in_fpscr >> 0x16) & 3);
    floorf(__x);
    _ZN13CMemoryStream10WriteFloatEf(auStack_50,extraout_r0);
    _ZN11Application14EncryptAndSaveEPKciP13CMemoryStream
              (param_1,DAT_003ea9fc + 0x3ea7c4,3,auStack_50);
    _ZN13CMemoryStreamD2Ev(auStack_50);
  }
  uVar1 = *(undefined4 *)(iVar2 + DAT_003eaa00);
  _ZN3glf12TaskDirector10StopThreadERNS0_10ThreadListE(uVar1,DAT_003eaa04 + 0x3ea7e4);
  _ZN3glf12TaskDirector7CleanUpEv(uVar1);
  piVar3 = *(int **)(iVar2 + DAT_003eaa08);
  _ZN12gxStateStack15ClearStateStackEv(*piVar3 + 4);
  _ZN12gxStateStack16DeleteStatesListEv(*piVar3 + 4);
  piVar3 = *(int **)(iVar2 + DAT_003eaa0c);
  _ZN13CGameSettings4SaveEv(*piVar3);
  iVar4 = *piVar3;
  if (iVar4 != 0) {
    _ZN13CGameSettingsD1Ev(iVar4);
    _ZdlPv(iVar4);
  }
  iVar4 = *(int *)((int)&__DT_SYMTAB[0x1df].st_name + param_1);
  if (iVar4 != 0) {
    _ZN8CStringsD1Ev(iVar4);
    _ZdlPv(iVar4);
    *(undefined4 *)((int)&__DT_SYMTAB[0x1df].st_name + param_1) = 0;
  }
  iVar4 = *(int *)((int)&__DT_SYMTAB[0x1df].st_value + param_1);
  if (iVar4 != 0) {
    _ZN8CStringsD1Ev(iVar4);
    _ZdlPv(iVar4);
    *(undefined4 *)((int)&__DT_SYMTAB[0x1df].st_value + param_1) = 0;
  }
  iVar4 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + param_1) = 0;
  if (iVar4 != 0) {
    _ZN13CMemoryStreamD2Ev(iVar4);
    _ZdlPv(iVar4);
    *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1) = 0;
  }
  piVar5 = (int *)(DAT_003eaa10 + 0x3ea8d8);
  piVar3 = (int *)*piVar5;
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 8))();
    *piVar5 = 0;
  }
  iVar4 = _ZN11Application11GetInstanceEv();
  (**(code **)(**(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar4) + 8) + 0x9c))();
  if (*(int **)(DAT_003eaa14 + 0x3ea920) != (int *)0x0) {
    (**(code **)(**(int **)(DAT_003eaa14 + 0x3ea920) + 4))();
  }
  piVar5 = *(int **)(iVar2 + DAT_003eaa18);
  piVar3 = (int *)*piVar5;
  if (piVar3 != (int *)0x0) {
    for (puVar6 = *(undefined4 **)((int)&__DT_SYMTAB[0x1de].st_value + param_1);
        puVar6 != (undefined4 *)((int)&__DT_SYMTAB[0x1de].st_value + param_1);
        puVar6 = (undefined4 *)*puVar6) {
      if (piVar3 == (int *)puVar6[2]) {
        _ZNSt8__detail15_List_node_base9_M_unhookEv(puVar6);
        _ZdlPv(puVar6);
        piVar3 = (int *)*piVar5;
        if (piVar3 == (int *)0x0) goto LAB_003ea980;
        break;
      }
    }
    (**(code **)(*piVar3 + 4))();
  }
LAB_003ea980:
  piVar3 = *(int **)(iVar2 + DAT_003eaa1c);
  iVar4 = *piVar3;
  if (iVar4 != 0) {
    for (puVar6 = *(undefined4 **)((int)&__DT_SYMTAB[0x1de].st_value + param_1);
        puVar6 != (undefined4 *)((int)&__DT_SYMTAB[0x1de].st_value + param_1);
        puVar6 = (undefined4 *)*puVar6) {
      if (iVar4 == puVar6[2]) {
        _ZNSt8__detail15_List_node_base9_M_unhookEv(puVar6);
        _ZdlPv(puVar6);
        break;
      }
    }
  }
  piVar5 = *(int **)(iVar2 + DAT_003eaa20);
  iVar4 = *piVar5;
  if (iVar4 != 0) {
    for (puVar6 = *(undefined4 **)((int)&__DT_SYMTAB[0x1de].st_value + param_1);
        puVar6 != (undefined4 *)((int)&__DT_SYMTAB[0x1de].st_value + param_1);
        puVar6 = (undefined4 *)*puVar6) {
      if (iVar4 == puVar6[2]) {
        _ZNSt8__detail15_List_node_base9_M_unhookEv(puVar6);
        _ZdlPv(puVar6);
        break;
      }
    }
  }
  iVar4 = **(int **)(iVar2 + DAT_003eaa24);
  if (iVar4 != 0) {
    _ZN15VoxSoundManagerD1Ev(iVar4);
    _ZdlPv(iVar4);
  }
  iVar4 = **(int **)(iVar2 + DAT_003eaa28);
  if (iVar4 != 0) {
    _ZN15CEffectsManagerD1Ev(iVar4);
    _ZdlPv(iVar4);
  }
  iVar4 = **(int **)(iVar2 + DAT_003eaa2c);
  if (iVar4 != 0) {
    _ZN14CGadgetManagerD1Ev(iVar4);
    _ZdlPv(iVar4);
  }
  if (*(int **)(DAT_003eaa30 + 0x3eaad8) != (int *)0x0) {
    (**(code **)(**(int **)(DAT_003eaa30 + 0x3eaad8) + 4))();
  }
  if ((int *)**(int **)(iVar2 + DAT_003eaa34) != (int *)0x0) {
    (**(code **)(*(int *)**(int **)(iVar2 + DAT_003eaa34) + 4))();
  }
  if ((int *)**(int **)(iVar2 + DAT_003eaa38) != (int *)0x0) {
    (**(code **)(*(int *)**(int **)(iVar2 + DAT_003eaa38) + 4))();
  }
  piVar3 = (int *)*piVar3;
  _ZN10IAPManager5CloseEv(piVar3);
  if (piVar3 != (int *)0x0) {
    (**(code **)(*piVar3 + 4))(piVar3);
  }
  piVar5 = (int *)*piVar5;
  _ZN17FederationManager5CloseEv(piVar5);
  if (piVar5 != (int *)0x0) {
    (**(code **)(*piVar5 + 4))(piVar5);
  }
  _ZN4glot15TrackingManager12FreeInstanceEv();
  piVar5 = (int *)(DAT_003eaa40 + 0x3eab8c);
  piVar3 = (int *)**(undefined4 **)(iVar2 + DAT_003eaa3c);
  (**(code **)(*piVar3 + 8))(piVar3,0);
  (**(code **)(*piVar3 + 4))(piVar3);
  if (*piVar5 != 0) {
    _ZdaPv();
    *piVar5 = 0;
  }
  if (*(int *)((int)&__DT_SYMTAB[0x1e9].st_value + param_1) != 0) {
    _ZdaPv();
    *(undefined4 *)((int)&__DT_SYMTAB[0x1e9].st_value + param_1) = 0;
  }
  iVar2 = **(int **)(iVar2 + DAT_003eaa44);
  if (iVar2 != 0) {
    _ZN13DeviceOptionsD1Ev(iVar2);
    _ZdlPv(iVar2);
  }
  return;
}


