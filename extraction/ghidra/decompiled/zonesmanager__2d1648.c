// _ZN13CZonesManager12FindWayPointEi @ 002d1648

int _ZN13CZonesManager12FindWayPointEi(undefined4 param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  
  if (param_2 < 0) {
    return 0;
  }
  iVar1 = _ZN6CLevel8GetLevelEv();
  iVar6 = *(int *)(iVar1 + 0xdc);
  iVar4 = *(int *)(iVar1 + 0xe0) - iVar6 >> 2;
  if (*(int *)(iVar1 + 0xd8) != iVar4) {
    _ZSt4sortIN9__gnu_cxx17__normal_iteratorIPP15CWayPointObjectSt6vectorIS3_SaIS3_EEEEPFbS3_S3_EEvT_SB_T0__constprop_916
              (iVar6);
    iVar6 = *(int *)(iVar1 + 0xdc);
    iVar4 = *(int *)(iVar1 + 0xe0) - iVar6 >> 2;
    *(int *)(iVar1 + 0xd8) = iVar4;
  }
  iVar4 = iVar4 + -1;
  if (iVar4 < 0) {
    return 0;
  }
  iVar1 = iVar4 >> 1;
  iVar2 = *(int *)(iVar6 + iVar1 * 4);
  iVar5 = *(int *)(iVar2 + 8);
  if (iVar5 == param_2) {
    return iVar2;
  }
  iVar2 = 0;
  while( true ) {
    if (iVar5 < param_2) {
      iVar2 = iVar1 + 1;
    }
    else {
      iVar4 = iVar1 + -1;
    }
    iVar1 = iVar4 + iVar2 >> 1;
    if (iVar4 < iVar2) break;
    iVar3 = *(int *)(iVar6 + iVar1 * 4);
    iVar5 = *(int *)(iVar3 + 8);
    if (iVar5 == param_2) {
      return iVar3;
    }
  }
  return 0;
}


