// _ZN11Application22ResetInventoryFromFileEPKci @ 003f3e80

void _ZN11Application22ResetInventoryFromFileEPKci(int param_1,char *param_2,int param_3)

{
  uint uVar1;
  int iVar2;
  int *piVar3;
  char acStack_8c [128];
  int local_c;
  
  piVar3 = *(int **)(DAT_003f3edc + 0x3f3e98);
  local_c = *piVar3;
  if (param_3 < 0) {
    param_3 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1);
  }
  sprintf(acStack_8c,param_2,param_3);
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


