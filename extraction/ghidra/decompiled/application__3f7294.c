// _ZN11Application10EnterPromoEv @ 003f7294

void _ZN11Application10EnterPromoEv(void)

{
  int iVar1;
  undefined4 uVar2;
  int *piVar3;
  undefined1 auStack_428 [4];
  undefined1 auStack_424 [4];
  char *local_420;
  int local_41c;
  undefined1 auStack_418 [4];
  char acStack_414 [1024];
  int local_14;
  
  piVar3 = *(int **)(DAT_003f73bc + 0x3f72b4);
  local_14 = *piVar3;
  _ZNSsC1EPKcRKSaIcE(&local_420,DAT_003f73c0 + 0x3f72bc,auStack_428);
  iVar1 = _ZNKSs4findEPKcjj(&local_420,DAT_003f73c4 + 0x3f72e0,0,0xc);
  if (iVar1 != -1) {
    _ZNSsC1EPKcRKSaIcE(&local_41c,DAT_003f73c8 + 0x3f7300,auStack_424);
    uVar2 = _ZNSs7replaceEjjPKcj(&local_420,iVar1,0xc,local_41c,*(undefined4 *)(local_41c + -0xc));
    _ZNSs6assignERKSs(&local_420,uVar2);
    _ZNSsD1Ev(&local_41c);
  }
  _ZN11Application16FillRedirectLinkERKSs_constprop_2499(auStack_418,&local_420);
  _ZNSs6assignERKSs(&local_420,auStack_418);
  _ZNSsD1Ev(auStack_418);
  strcpy(acStack_414,local_420);
  __android_log_print(4,DAT_003f73cc + 0x3f7370,DAT_003f73d0 + 0x3f7378,acStack_414);
  iVar1 = _ZN3glf3App11GetInstanceEv();
  (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1) + 0x24))
            (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1),acStack_414);
  _ZNSsD1Ev(&local_420);
  if (local_14 == *piVar3) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}


