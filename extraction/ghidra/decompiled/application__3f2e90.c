// _ZN11Application16DeleteCheckPointEi @ 003f2e90

void _ZN11Application16DeleteCheckPointEi(int param_1,int param_2)

{
  uint uVar1;
  int iVar2;
  int *piVar3;
  char acStack_8c [128];
  int local_c;
  
  piVar3 = *(int **)(DAT_003f2ef4 + 0x3f2eac);
  local_c = *piVar3;
  if (param_2 < 0) {
    param_2 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1);
  }
  sprintf(acStack_8c,(char *)(DAT_003f2ef8 + 0x3f2eb0),param_2);
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


