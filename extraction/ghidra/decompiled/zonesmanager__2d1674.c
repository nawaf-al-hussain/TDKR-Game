// _ZN13CZonesManager19CleanContactHistoryEv @ 002d1674

void _ZN13CZonesManager19CleanContactHistoryEv(int param_1)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  int iVar4;
  int *piVar5;
  
  piVar2 = *(int **)(param_1 + 0x84);
  piVar5 = *(int **)(param_1 + 0x80);
  do {
    if (piVar5 == piVar2) {
      return;
    }
    while( true ) {
      iVar3 = *piVar5;
      piVar5 = piVar5 + 1;
      iVar3 = *(int *)(iVar3 + 0x138);
      if (*(int *)(iVar3 + 0x10) < 1) break;
      iVar4 = 0;
      do {
        iVar1 = iVar4 * 4;
        iVar4 = iVar4 + 1;
        _ZN11CGameObject19CleanContactHistoryEv(*(undefined4 *)(*(int *)(iVar3 + 0xc) + iVar1));
      } while (iVar4 < *(int *)(iVar3 + 0x10));
      piVar2 = *(int **)(param_1 + 0x84);
      if (piVar5 == piVar2) {
        return;
      }
    }
  } while( true );
}


