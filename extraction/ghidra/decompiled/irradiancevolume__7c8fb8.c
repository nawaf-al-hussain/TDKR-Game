// _ZN6glitch10irradiance17CIrradianceVolumeD1Ev @ 007c8fb8

int * _ZN6glitch10irradiance17CIrradianceVolumeD1Ev(int *param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  
  iVar3 = *param_1;
  iVar1 = param_1[1] - iVar3 >> 2;
  if (0 < iVar1) {
    iVar4 = 0;
    while( true ) {
      iVar2 = iVar4 * 4;
      iVar4 = iVar4 + 1;
      if (*(int *)(iVar3 + iVar2) != 0) {
        _ZdaPv();
      }
      if (iVar4 == iVar1) break;
      iVar3 = *param_1;
    }
  }
  iVar3 = param_1[3];
  iVar1 = param_1[4] - iVar3 >> 2;
  if (0 < iVar1) {
    iVar4 = 0;
    do {
      iVar2 = iVar4 * 4;
      iVar4 = iVar4 + 1;
      if (*(int *)(iVar3 + iVar2) != 0) {
        _ZdaPv();
        iVar3 = param_1[3];
      }
    } while (iVar4 != iVar1);
  }
  if (iVar3 != 0) {
    _ZdlPv(iVar3);
  }
  if (*param_1 != 0) {
    _ZdlPv();
  }
  return param_1;
}


