// _ZN11Application12IsInChaptersEi @ 003ecf70

undefined4 _ZN11Application12IsInChaptersEi(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  
  puVar3 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
  iVar1 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) - (int)puVar3 >> 2;
  if (iVar1 == 0) {
    return 0;
  }
  if (*(int *)*puVar3 == param_2) {
    return 1;
  }
  iVar2 = 0;
  do {
    iVar2 = iVar2 + 1;
    if (iVar2 == iVar1) {
      return 0;
    }
  } while (*(int *)puVar3[iVar2] != param_2);
  return 1;
}


