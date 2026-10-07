// _ZN11Application23ResetGlobalDataFromFileEPKci.constprop.2441 @ 00461e04

void _ZN11Application23ResetGlobalDataFromFileEPKci_constprop_2441(int param_1,char *param_2)

{
  uint uVar1;
  int iVar2;
  int *piVar3;
  char acStack_8c [128];
  int local_c;
  
  piVar3 = *(int **)(DAT_00461e5c + 0x461e20);
  local_c = *piVar3;
  sprintf(acStack_8c,param_2,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1));
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


