// _ZN11Application25DeleteLevelInitCheckPointEi @ 003f32c0

void _ZN11Application25DeleteLevelInitCheckPointEi(int param_1)

{
  uint uVar1;
  int iVar2;
  int *piVar3;
  char acStack_8c [128];
  int local_c;
  
  piVar3 = *(int **)(DAT_003f3320 + 0x3f32e0);
  local_c = *piVar3;
  sprintf(acStack_8c,(char *)(DAT_003f3324 + 0x3f32e8),
          *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1));
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


