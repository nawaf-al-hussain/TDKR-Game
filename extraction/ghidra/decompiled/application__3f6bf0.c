// _ZN11Application12EnterTwitterEv @ 003f6bf0

void _ZN11Application12EnterTwitterEv(int param_1)

{
  int iVar1;
  char *pcVar2;
  size_t sVar3;
  undefined4 uVar4;
  int iVar5;
  int iVar6;
  int *piVar7;
  int iVar8;
  int iVar9;
  undefined1 auStack_428 [4];
  char *local_424;
  undefined1 auStack_420 [4];
  char acStack_41c [1024];
  int local_1c;
  
  piVar7 = *(int **)(DAT_003f6ef4 + 0x3f6c0c);
  local_1c = *piVar7;
  iVar1 = hasConnectivity();
  if (iVar1 == 0) {
    iVar1 = _ZN11Application11GetInstanceEv();
    iVar5 = *(int *)(*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) + 8);
    iVar8 = *(int *)(*(int *)(*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) + 0xc) + 0x1304);
    iVar1 = _ZN11Application11GetInstanceEv();
    iVar6 = *(int *)(*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) + 8);
    iVar9 = *(int *)(*(int *)(*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) + 0xc) + 0x1300);
    iVar1 = _ZN11Application11GetInstanceEv();
    showAlertUTF16(iVar5 + iVar8 * 2,iVar6 + iVar9 * 2,
                   *(int *)(*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) + 8) +
                   *(int *)(*(int *)(*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) + 0xc) + 0x1150)
                   * 2,0,3,0);
  }
  else {
    _ZNSsC1EPKcRKSaIcE(&local_424,DAT_003f6ef8 + 0x3f6c30,auStack_428);
    _ZNSs6assignEPKcj(&local_424,DAT_003f6efc + 0x3f6c44,0x86);
    pcVar2 = (char *)_ZN3glf14AndroidGetUDIDEb(0);
    sVar3 = strlen(pcVar2);
    _ZNSs6appendEPKcj(&local_424,pcVar2,sVar3);
    iVar1 = _ZNKSs4findEPKcjj(&local_424,DAT_003f6f00 + 0x3f6c78,0,6);
    if (iVar1 != -1) {
      uVar4 = _ZNSs7replaceEjjPKcj(&local_424,iVar1,6,DAT_003f6f04 + 0x3f6ca0,4);
      _ZNSs6assignERKSs(&local_424,uVar4);
    }
    iVar1 = _ZNKSs4findEPKcjj(&local_424,DAT_003f6f08 + 0x3f6cc8,0,4);
    if (iVar1 != -1) {
      pcVar2 = (char *)(**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + param_1) + 0x38))();
      sVar3 = strlen(pcVar2);
      uVar4 = _ZNSs7replaceEjjPKcj(&local_424,iVar1,4,pcVar2,sVar3);
      _ZNSs6assignERKSs(&local_424,uVar4);
    }
    iVar1 = _ZNKSs4findEPKcjj(&local_424,DAT_003f6f0c + 0x3f6d30,0,6);
    if (iVar1 != -1) {
      pcVar2 = (char *)(**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + param_1) + 0x34))();
      sVar3 = strlen(pcVar2);
      uVar4 = _ZNSs7replaceEjjPKcj(&local_424,iVar1,6,pcVar2,sVar3);
      _ZNSs6assignERKSs(&local_424,uVar4);
    }
    iVar1 = _ZNKSs4findEPKcjj(&local_424,DAT_003f6f10 + 0x3f6d98,0,8);
    if (iVar1 != -1) {
      pcVar2 = (char *)(**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + param_1) + 0x40))();
      sVar3 = strlen(pcVar2);
      uVar4 = _ZNSs7replaceEjjPKcj(&local_424,iVar1,8,pcVar2,sVar3);
      _ZNSs6assignERKSs(&local_424,uVar4);
    }
    _ZN11Application16FillRedirectLinkERKSs_constprop_2499(auStack_420,&local_424);
    _ZNSs6assignERKSs(&local_424,auStack_420);
    _ZNSsD1Ev(auStack_420);
    strcpy(acStack_41c,local_424);
    __android_log_print(4,DAT_003f6f14 + 0x3f6e28,DAT_003f6f18 + 0x3f6e30,acStack_41c);
    iVar1 = _ZN3glf3App11GetInstanceEv();
    (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1) + 0x24))
              (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1),acStack_41c);
    _ZNSsD1Ev(&local_424);
  }
  if (local_1c == *piVar7) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}


