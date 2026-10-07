// _ZN7gameswf12ASDictionary11getIdentityERKNS_7ASValueEPNS_6StringE @ 00738634

void _ZN7gameswf12ASDictionary11getIdentityERKNS_7ASValueEPNS_6StringE
               (undefined4 param_1,char *param_2,char *param_3)

{
  undefined4 uVar1;
  size_t sVar2;
  char *pcVar3;
  int iVar4;
  int *piVar5;
  undefined1 local_d8;
  undefined1 local_d7;
  undefined3 local_98;
  byte bStack_95;
  char acStack_94 [128];
  int local_14;
  
  piVar5 = *(int **)(DAT_00738724 + 0x738650);
  local_14 = *piVar5;
  if (*param_2 == '\x05') {
    sprintf(acStack_94,(char *)(DAT_00738728 + 0x7386d4),*(undefined4 *)(param_2 + 4));
    sVar2 = strlen(acStack_94);
    _ZN7gameswf6String6resizeEi(param_3,sVar2);
    iVar4 = (int)*param_3;
    if (iVar4 == -1) {
      iVar4 = *(int *)(param_3 + 4);
      pcVar3 = *(char **)(param_3 + 0xc);
    }
    else {
      pcVar3 = param_3 + 1;
    }
    _ZN7gameswf8Strcpy_sEPcjPKc(pcVar3,iVar4,acStack_94);
    *(uint *)(param_3 + 0x40) = *(uint *)(param_3 + 0x40) & 0xff000000 | 0xffffff;
  }
  else {
    local_d8 = 1;
    local_d7 = 0;
    _local_98 = CONCAT13((byte)((uint)_local_98 >> 0x18) & 0xfe,0xffffff);
    uVar1 = _ZNK7gameswf7ASValue8toStringERNS_6StringE(param_2,&local_d8);
    _ZN7gameswf6StringaSERKS0_(param_3,uVar1);
    _ZN7gameswf6StringD1Ev(&local_d8);
  }
  if (local_14 != *piVar5) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}


