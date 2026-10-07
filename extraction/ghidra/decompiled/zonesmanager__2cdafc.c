// _ZN13CZonesManager23SetBatchNodesVisibilityEb @ 002cdafc

void _ZN13CZonesManager23SetBatchNodesVisibilityEb(int param_1,undefined4 param_2)

{
  int *piVar1;
  int *piVar2;
  int *piVar3;
  
  piVar1 = *(int **)(param_1 + 0x84);
  piVar3 = *(int **)(param_1 + 0x80);
  if ((uint)((int)piVar1 - (int)piVar3) >> 2 == 0) {
    return;
  }
  do {
    piVar2 = piVar3;
    if (piVar3 == piVar1) {
      return;
    }
    while( true ) {
      piVar3 = piVar2 + 1;
      piVar2 = *(int **)(*piVar2 + 0x194);
      if (piVar2 == (int *)0x0) break;
      (**(code **)(*piVar2 + 0x4c))(piVar2,param_2);
      piVar1 = *(int **)(param_1 + 0x84);
      piVar2 = piVar3;
      if (piVar3 == piVar1) {
        return;
      }
    }
  } while( true );
}


