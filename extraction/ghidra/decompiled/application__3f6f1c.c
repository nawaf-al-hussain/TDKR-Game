// _ZN11Application17EnterCustomerCareEv @ 003f6f1c

void _ZN11Application17EnterCustomerCareEv(void)

{
  char *__s;
  size_t sVar1;
  int iVar2;
  int *piVar3;
  undefined1 auStack_420 [4];
  char *local_41c;
  undefined1 auStack_418 [4];
  char acStack_414 [1024];
  int local_14;
  
  piVar3 = *(int **)(DAT_003f7010 + 0x3f6f3c);
  local_14 = *piVar3;
  _ZNSsC1EPKcRKSaIcE(&local_41c,DAT_003f7014 + 0x3f6f44,auStack_420);
  _ZNSs6assignEPKcj(&local_41c,DAT_003f7018 + 0x3f6f60,0x4d);
  __s = (char *)_ZN3glf14AndroidGetUDIDEb(1);
  sVar1 = strlen(__s);
  _ZNSs6appendEPKcj(&local_41c,__s,sVar1);
  _ZN11Application16FillRedirectLinkERKSs_constprop_2499(auStack_418,&local_41c);
  _ZNSs6assignERKSs(&local_41c,auStack_418);
  _ZNSsD1Ev(auStack_418);
  strcpy(acStack_414,local_41c);
  __android_log_print(4,DAT_003f701c + 0x3f6fc0,DAT_003f7020 + 0x3f6fc8,acStack_414);
  iVar2 = _ZN3glf3App11GetInstanceEv();
  (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar2) + 0x24))
            (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar2),acStack_414);
  _ZNSsD1Ev(&local_41c);
  if (local_14 == *piVar3) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}


