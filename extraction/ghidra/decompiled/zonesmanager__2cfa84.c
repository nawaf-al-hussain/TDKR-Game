// _ZN13CZonesManager21GetCurrentMissionZoneEv @ 002cfa84

int _ZN13CZonesManager21GetCurrentMissionZoneEv(int param_1)

{
  int iVar1;
  int *piVar2;
  
  if (*(int *)(param_1 + 0x4c) == -1) {
    return 0;
  }
  piVar2 = *(int **)(param_1 + 0x80);
  do {
    if (*(int **)(param_1 + 0x84) == piVar2) {
      return 0;
    }
    iVar1 = *piVar2;
    piVar2 = piVar2 + 1;
  } while (*(int *)(param_1 + 0x4c) != *(int *)(iVar1 + 8));
  return iVar1;
}


