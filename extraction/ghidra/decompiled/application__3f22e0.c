// _ZN11Application17RegisterForUpdateEP10IUpdatable @ 003f22e0

void _ZN11Application17RegisterForUpdateEP10IUpdatable(int param_1,int param_2)

{
  int *piVar1;
  int iVar2;
  undefined4 *puVar3;
  
  if (param_2 == 0) {
    return;
  }
  piVar1 = (int *)_Znwj(0xc);
  if (piVar1 != (int *)&DAT_fffffff8) {
    piVar1[2] = param_2;
  }
  iVar2 = *(int *)((int)&__DT_SYMTAB[0x1de].st_size + param_1);
  *piVar1 = param_1 + 0x11ef8;
  piVar1[1] = iVar2;
  puVar3 = *(undefined4 **)((int)&__DT_SYMTAB[0x1de].st_size + param_1);
  *(int **)((int)&__DT_SYMTAB[0x1de].st_size + param_1) = piVar1;
  *puVar3 = piVar1;
  return;
}


