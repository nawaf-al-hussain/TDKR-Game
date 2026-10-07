// _ZN11Application25RequireLoadChapterMissionEii @ 003edefc

void _ZN11Application25RequireLoadChapterMissionEii(int param_1,int param_2,int param_3)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  int iVar4;
  
  piVar3 = *(int **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
  iVar1 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) - (int)piVar3 >> 2;
  if (iVar1 == 0) {
    piVar2 = (int *)0x0;
  }
  else {
    piVar2 = (int *)*piVar3;
    if (param_2 != *piVar2) {
      iVar4 = 0;
      do {
        iVar4 = iVar4 + 1;
        if (iVar4 == iVar1) {
          piVar2 = (int *)0x0;
          break;
        }
        piVar2 = (int *)piVar3[iVar4];
      } while (param_2 != *piVar2);
    }
  }
  piVar3 = (int *)piVar2[3];
  iVar1 = piVar2[4] - (int)piVar3 >> 2;
  if (iVar1 == 0) {
    piVar2 = (int *)0x0;
  }
  else {
    piVar2 = (int *)*piVar3;
    if (param_3 != *piVar2) {
      iVar4 = 0;
      do {
        iVar4 = iVar4 + 1;
        if (iVar4 == iVar1) {
          piVar2 = (int *)0x0;
          break;
        }
        piVar2 = (int *)piVar3[iVar4];
      } while (param_3 != *piVar2);
    }
  }
  if (-1 < piVar2[1]) {
    *(int *)((int)&__DT_SYMTAB[0x1e7].st_size + param_1) = piVar2[1];
    *(undefined4 *)(&__DT_SYMTAB[0x1e7].st_info + param_1) = 0xffffffff;
  }
  return;
}


