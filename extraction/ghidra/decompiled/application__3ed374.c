// _ZN11Application10GetChapterEi @ 003ed374

int * _ZN11Application10GetChapterEi(int param_1,int param_2)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  undefined4 *puVar4;
  
  puVar4 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
  iVar1 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) - (int)puVar4 >> 2;
  if (iVar1 == 0) {
    piVar2 = (int *)0x0;
  }
  else {
    piVar2 = (int *)*puVar4;
    if (*piVar2 != param_2) {
      iVar3 = 0;
      do {
        iVar3 = iVar3 + 1;
        if (iVar3 == iVar1) {
          return (int *)0x0;
        }
        piVar2 = (int *)puVar4[iVar3];
      } while (*piVar2 != param_2);
    }
  }
  return piVar2;
}


