// _ZN7gameswf12ASDictionary17deleteMemberByKeyERKNS_7ASValueE @ 007384e8

void _ZN7gameswf12ASDictionary17deleteMemberByKeyERKNS_7ASValueE(int *param_1,char *param_2)

{
  undefined4 uVar1;
  size_t sVar2;
  int *piVar3;
  char local_124 [4];
  int local_120;
  char *local_118;
  uint local_e4;
  undefined1 local_e0;
  undefined1 local_df;
  undefined3 local_a0;
  byte bStack_9d;
  char acStack_9c [128];
  int local_1c;
  
  piVar3 = *(int **)(DAT_0073862c + 0x738508);
  local_1c = *piVar3;
  local_124[0] = '\x01';
  local_124[1] = 0;
  local_e4 = CONCAT13((char)(local_e4 >> 0x18),0xffffff) & 0xfeffffff;
  if (*param_2 == '\x05') {
    sprintf(acStack_9c,(char *)(DAT_00738630 + 0x7385d4),*(undefined4 *)(param_2 + 4));
    sVar2 = strlen(acStack_9c);
    _ZN7gameswf6String6resizeEi(local_124,sVar2);
    if (local_124[0] != -1) {
      local_118 = local_124 + 1;
      local_120 = (int)local_124[0];
    }
    _ZN7gameswf8Strcpy_sEPcjPKc(local_118,local_120,acStack_9c);
    local_e4 = local_e4 & 0xff000000 | 0xffffff;
  }
  else {
    local_e0 = 1;
    local_df = 0;
    _local_a0 = CONCAT13((byte)((uint)_local_a0 >> 0x18) & 0xfe,0xffffff);
    uVar1 = _ZNK7gameswf7ASValue8toStringERNS_6StringE(param_2,&local_e0);
    _ZN7gameswf6StringaSERKS0_(local_124,uVar1);
    _ZN7gameswf6StringD1Ev(&local_e0);
  }
  uVar1 = (**(code **)(*param_1 + 0x28))(param_1,local_124);
  _ZN7gameswf6StringD1Ev(local_124);
  if (local_1c == *piVar3) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(uVar1);
}


