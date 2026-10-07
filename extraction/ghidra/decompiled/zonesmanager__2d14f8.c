// _ZN13CZonesManager7AddZoneEP5CZone @ 002d14f8

void _ZN13CZonesManager7AddZoneEP5CZone(int param_1,int param_2)

{
  bool bVar1;
  int *piVar2;
  int iVar3;
  code *pcVar4;
  int local_14;
  int *local_10;
  int *local_c [2];
  
  piVar2 = *(int **)(param_1 + 0x84);
  local_14 = param_2;
  if (piVar2 == *(int **)(param_1 + 0x88)) {
    _ZNSt6vectorIP5CZoneSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
              (param_1 + 0x80,piVar2,&local_14);
  }
  else {
    iVar3 = 0;
    if (piVar2 != (int *)0x0) {
      *piVar2 = param_2;
      iVar3 = *(int *)(param_1 + 0x84);
    }
    *(int *)(param_1 + 0x84) = iVar3 + 4;
  }
  local_10 = *(int **)(**(int **)(DAT_002d15f8 + 0x2d1534) + 0x17c);
  if (local_10 != (int *)0x0) {
    piVar2 = (int *)((int)local_10 + *(int *)(*local_10 + -0x10) + 4);
    DataMemoryBarrier(0xf);
    do {
      bVar1 = (bool)hasExclusiveAccess(piVar2);
    } while (!bVar1);
    *piVar2 = *piVar2 + 1;
    DataMemoryBarrier(0xf);
  }
  local_c[0] = *(int **)(local_14 + 0x1dc);
  pcVar4 = *(code **)(*local_10 + 0x68);
  if (local_c[0] != (int *)0x0) {
    piVar2 = (int *)((int)local_c[0] + *(int *)(*local_c[0] + -0x10) + 4);
    DataMemoryBarrier(0xf);
    do {
      bVar1 = (bool)hasExclusiveAccess(piVar2);
    } while (!bVar1);
    *piVar2 = *piVar2 + 1;
    DataMemoryBarrier(0xf);
  }
  (*pcVar4)(local_10,local_c);
  _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(local_c);
  _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(&local_10);
  return;
}


