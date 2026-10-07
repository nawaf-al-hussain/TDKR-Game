// _ZN11Application14ResetInventoryEi @ 003f4118

void _ZN11Application14ResetInventoryEi(void)

{
  uint uVar1;
  int iVar2;
  int *piVar3;
  char acStack_8c [128];
  int local_c;
  
  piVar3 = *(int **)(DAT_003f4170 + 0x3f4138);
  local_c = *piVar3;
  sprintf(acStack_8c,(char *)(DAT_003f4174 + 0x3f413c),0);
  uVar1 = unlink(acStack_8c);
  iVar2 = 1 - uVar1;
  if (1 < uVar1) {
    iVar2 = 0;
  }
  if (local_c == *piVar3) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(iVar2);
}


