// _ZN11Application15ResetGlobalDataEi @ 003f3a2c

void _ZN11Application15ResetGlobalDataEi(int param_1,int param_2)

{
  uint uVar1;
  int iVar2;
  int *piVar3;
  char acStack_8c [128];
  int local_c;
  
  piVar3 = *(int **)(DAT_003f3a90 + 0x3f3a48);
  local_c = *piVar3;
  if (param_2 < 0) {
    param_2 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1);
  }
  sprintf(acStack_8c,(char *)(DAT_003f3a94 + 0x3f3a4c),param_2);
  uVar1 = unlink(acStack_8c);
  iVar2 = 1 - uVar1;
  if (1 < uVar1) {
    iVar2 = 0;
  }
  if (local_c != *piVar3) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail(iVar2);
  }
  return;
}


