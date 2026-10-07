// _ZN13CAIController31RemoveFromCombatBatarangTargetsEP11CGameObject @ 0018e854

void _ZN13CAIController31RemoveFromCombatBatarangTargetsEP11CGameObject(int param_1,int param_2)

{
  int iVar1;
  int *piVar2;
  int *__dest;
  int *piVar3;
  
  piVar3 = *(int **)(param_1 + 0x16c);
  piVar2 = *(int **)(param_1 + 0x168);
  do {
    __dest = piVar2;
    if (__dest == piVar3) {
      return;
    }
    piVar2 = __dest + 1;
  } while (*__dest != param_2);
  piVar2 = __dest + 1;
  if ((piVar2 != piVar3) && (iVar1 = (int)piVar3 - (int)piVar2 >> 2, iVar1 != 0)) {
    memmove(__dest,piVar2,iVar1 << 2);
    *(int *)(param_1 + 0x16c) = *(int *)(param_1 + 0x16c) + -4;
    return;
  }
  *(int **)(param_1 + 0x16c) = piVar3 + -1;
  return;
}

