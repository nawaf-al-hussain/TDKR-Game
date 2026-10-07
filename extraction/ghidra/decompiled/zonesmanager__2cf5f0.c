// _ZN13CZonesManager19FindFirstSpawnPointEv @ 002cf5f0

int _ZN13CZonesManager19FindFirstSpawnPointEv(int param_1)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  
  piVar2 = *(int **)(param_1 + 0x80);
  do {
    piVar3 = piVar2;
    if (piVar2 == *(int **)(param_1 + 0x84)) {
      return 0;
    }
    while( true ) {
      piVar2 = piVar3 + 1;
      iVar1 = *(int *)(*(int *)(*piVar3 + 0x134) + 0xc);
      if (*(int *)(iVar1 + 0x10) == 0) break;
      iVar1 = **(int **)(iVar1 + 0xc);
      if (iVar1 != 0) {
        return iVar1;
      }
      piVar3 = piVar2;
      if (piVar2 == *(int **)(param_1 + 0x84)) {
        return 0;
      }
    }
  } while( true );
}


