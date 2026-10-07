// _ZN11Application11EnterReviewEv @ 003f7030

void _ZN11Application11EnterReviewEv(int param_1)

{
  char *pcVar1;
  size_t sVar2;
  int iVar3;
  undefined4 uVar4;
  undefined1 auStack_24 [4];
  undefined1 auStack_20 [4];
  undefined4 local_1c;
  undefined1 auStack_18 [4];
  int local_14;
  
  _ZNSsC1EPKcRKSaIcE(&local_1c,DAT_003f7278 + 0x3f7048,auStack_24);
  _ZNSs6assignEPKcj(&local_1c,DAT_003f727c + 0x3f7064,0x85);
  pcVar1 = (char *)_ZN3glf14AndroidGetUDIDEb(0);
  sVar2 = strlen(pcVar1);
  _ZNSs6appendEPKcj(&local_1c,pcVar1,sVar2);
  _ZN11Application16FillRedirectLinkERKSs_constprop_2499(auStack_18,&local_1c);
  _ZNSs6assignERKSs(&local_1c,auStack_18);
  _ZNSsD1Ev(auStack_18);
  iVar3 = _ZNKSs4findEPKcjj(&local_1c,DAT_003f7280 + 0x3f70b8,0,6);
  if (iVar3 != -1) {
    _ZNSsC1EPKcRKSaIcE(&local_14,DAT_003f7284 + 0x3f70dc,auStack_20);
    uVar4 = _ZNSs7replaceEjjPKcj(&local_1c,iVar3,6,local_14,*(undefined4 *)(local_14 + -0xc));
    _ZNSs6assignERKSs(&local_1c,uVar4);
    _ZNSsD1Ev(&local_14);
  }
  iVar3 = _ZNKSs4findEPKcjj(&local_1c,DAT_003f7288 + 0x3f7124,0,4);
  if (iVar3 != -1) {
    pcVar1 = (char *)(**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + param_1) + 0x38))();
    sVar2 = strlen(pcVar1);
    uVar4 = _ZNSs7replaceEjjPKcj(&local_1c,iVar3,4,pcVar1,sVar2);
    _ZNSs6assignERKSs(&local_1c,uVar4);
  }
  iVar3 = _ZNKSs4findEPKcjj(&local_1c,DAT_003f728c + 0x3f718c,0,6);
  if (iVar3 != -1) {
    pcVar1 = (char *)(**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + param_1) + 0x34))();
    sVar2 = strlen(pcVar1);
    uVar4 = _ZNSs7replaceEjjPKcj(&local_1c,iVar3,6,pcVar1,sVar2);
    _ZNSs6assignERKSs(&local_1c,uVar4);
  }
  iVar3 = _ZNKSs4findEPKcjj(&local_1c,DAT_003f7290 + 0x3f71f4,0,8);
  if (iVar3 != -1) {
    pcVar1 = (char *)(**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + param_1) + 0x40))();
    sVar2 = strlen(pcVar1);
    uVar4 = _ZNSs7replaceEjjPKcj(&local_1c,iVar3,8,pcVar1,sVar2);
    _ZNSs6assignERKSs(&local_1c,uVar4);
  }
  iVar3 = _ZN3glf3App11GetInstanceEv();
  (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar3) + 0x24))
            (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar3),local_1c);
  _ZNSsD1Ev(&local_1c);
  return;
}


