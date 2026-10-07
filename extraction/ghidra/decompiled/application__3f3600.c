// _ZN11Application22EnableMissionInChapterEii @ 003f3600

void _ZN11Application22EnableMissionInChapterEii(int param_1,int param_2,int param_3)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  int *piVar4;
  
  puVar3 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
  iVar1 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) - (int)puVar3 >> 2;
  if (iVar1 == 0) {
    piVar4 = (int *)0x0;
  }
  else {
    piVar4 = (int *)*puVar3;
    if (param_2 != *piVar4) {
      iVar2 = 0;
      do {
        iVar2 = iVar2 + 1;
        if (iVar2 == iVar1) {
          piVar4 = (int *)0x0;
          break;
        }
        piVar4 = (int *)puVar3[iVar2];
      } while (param_2 != *piVar4);
    }
  }
  puVar3 = (undefined4 *)piVar4[3];
  iVar1 = piVar4[4] - (int)puVar3 >> 2;
  if (iVar1 != 0) {
    piVar4 = (int *)*puVar3;
    if (param_3 != *piVar4) {
      iVar2 = 0;
      do {
        iVar2 = iVar2 + 1;
        if (iVar1 == iVar2) {
          return;
        }
        piVar4 = (int *)puVar3[iVar2];
      } while (param_3 != *piVar4);
    }
    *(undefined1 *)(piVar4 + 6) = 1;
  }
  return;
}


