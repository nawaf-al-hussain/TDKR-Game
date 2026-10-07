// _ZN11Application25CheckSpaceAvailableToSaveEb @ 003ee958

void _ZN11Application25CheckSpaceAvailableToSaveEb(int param_1)

{
  int iVar1;
  int *piVar2;
  char local_60 [8];
  undefined4 local_58;
  undefined4 local_54;
  undefined3 local_20;
  byte bStack_1d;
  int local_1c;
  
  piVar2 = *(int **)(DAT_003eeab8 + 0x3ee97c);
  local_1c = *piVar2;
  if (((*(char *)(DAT_003eeab4 + 0x3ee968) != '\0') && (*(float *)(DAT_003eeabc + 0x3ee994) <= 0.0))
     || (param_1 != 0)) {
    iVar1 = _ZN11Application11GetInstanceEv();
    if (*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) != 0) {
      iVar1 = _ZN11Application11GetInstanceEv();
      if (*(int *)(*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) + 8) +
          *(int *)(*(int *)(*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) + 0xc) + 0x1330) * 2 != 0)
      {
        local_60[0] = '\x01';
        local_60[1] = 0;
        _local_20 = CONCAT13((byte)((uint)_local_20 >> 0x18) & 0xfe,0xffffff);
        _ZN7gameswf6String19encodeUTF8FromWcharEPS0_PKt(local_60);
        iVar1 = _ZN11Application11GetInstanceEv();
        iVar1 = (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1) + 0x48))();
        if (iVar1 < 2) {
          *(undefined1 *)(DAT_003eeacc + 0x3eea9c) = 0;
        }
        else {
          *(undefined1 *)(DAT_003eeac0 + 0x3eea44) = 1;
        }
        if (local_60[0] == -1) {
          _ZN7gameswf13free_internalEPvj(local_54,local_58);
        }
      }
      *(undefined4 *)(DAT_003eeac4 + 0x3eea64) = 0x447a0000;
    }
    if (param_1 != 0) {
      *(undefined1 *)(DAT_003eeac8 + 0x3eea78) = 1;
    }
  }
  if (local_1c != *piVar2) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}


