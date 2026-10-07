// _ZN7gameswf12ASDictionary14getMemberByKeyERKNS_7ASValueEPS1_ @ 007381d0

void _ZN7gameswf12ASDictionary14getMemberByKeyERKNS_7ASValueEPS1_
               (int *param_1,char *param_2,undefined4 param_3)

{
  undefined4 uVar1;
  int iVar2;
  size_t sVar3;
  int *piVar4;
  char local_12c [4];
  int local_128;
  char *local_120;
  uint local_ec;
  undefined1 local_e8;
  undefined1 local_e7;
  undefined3 local_a8;
  byte bStack_a5;
  char acStack_a4 [128];
  int local_24;
  
  piVar4 = *(int **)(DAT_00738354 + 0x7381f0);
  local_24 = *piVar4;
  local_12c[0] = '\x01';
  local_12c[1] = 0;
  local_ec = CONCAT13((char)(local_ec >> 0x18),0xffffff) & 0xfeffffff;
  if (*param_2 == '\x05') {
    sprintf(acStack_a4,(char *)(DAT_00738358 + 0x7382fc),*(undefined4 *)(param_2 + 4));
    sVar3 = strlen(acStack_a4);
    _ZN7gameswf6String6resizeEi(local_12c,sVar3);
    if (local_12c[0] != -1) {
      local_120 = local_12c + 1;
      local_128 = (int)local_12c[0];
    }
    _ZN7gameswf8Strcpy_sEPcjPKc(local_120,local_128,acStack_a4);
    local_ec = local_ec & 0xff000000 | 0xffffff;
  }
  else {
    local_e8 = 1;
    local_e7 = 0;
    _local_a8 = CONCAT13((byte)((uint)_local_a8 >> 0x18) & 0xfe,0xffffff);
    uVar1 = _ZNK7gameswf7ASValue8toStringERNS_6StringE(param_2,&local_e8);
    _ZN7gameswf6StringaSERKS0_(local_12c,uVar1);
    _ZN7gameswf6StringD1Ev(&local_e8);
  }
  iVar2 = _ZN7gameswf19getStandardMemberIDERKNS_7StringIE(local_12c);
  if ((iVar2 == -1) || (iVar2 = (**(code **)(*param_1 + 0x24))(param_1,iVar2,param_3), iVar2 == 0))
  {
    uVar1 = (**(code **)(*param_1 + 0x2c))(param_1,local_12c,param_3);
  }
  else {
    uVar1 = 1;
  }
  _ZN7gameswf6StringD1Ev(local_12c);
  if (local_24 == *piVar4) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(uVar1);
}


