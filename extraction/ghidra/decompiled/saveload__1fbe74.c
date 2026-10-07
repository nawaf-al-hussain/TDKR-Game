// _ZN22GameObjectCacheManager11GetSaveLoadEiiiRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE @ 001fbe74

int * _ZN22GameObjectCacheManager11GetSaveLoadEiiiRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (int *param_1,int param_2,int param_3,undefined4 param_4,undefined4 param_5)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  int iVar3;
  int *piVar4;
  int iVar5;
  int iVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  int *local_2c [2];
  
  uVar7 = _ZN13CZonesManager8FindZoneEi(**(undefined4 **)(DAT_001fc010 + 0x1fbe84),param_4);
  uVar1 = (undefined4)((ulonglong)uVar7 >> 0x20);
  iVar3 = param_1[1];
  iVar5 = param_1[2] - iVar3 >> 2;
  iVar6 = iVar5 + -1;
  if (-1 < iVar6) {
    iVar5 = (iVar5 + 0x3fffffff) * 4;
    while( true ) {
      piVar4 = *(int **)(iVar3 + iVar5);
      iVar5 = iVar5 + -4;
      if (param_3 == piVar4[0x39]) {
        uVar8 = (**(code **)(*piVar4 + 0xa0))(piVar4,uVar1);
        uVar1 = (int)((ulonglong)uVar8 >> 0x20);
        if ((int)uVar8 == 0) {
          iVar3 = _ZN11CGameObject11CanBeReusedEv(piVar4);
          uVar1 = param_5;
          if (iVar3 != 0) {
            uVar8 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                              (piVar4 + 0x3f);
            uVar1 = (undefined4)((ulonglong)uVar8 >> 0x20);
            if ((int)uVar8 == 0) {
              (**(code **)(*piVar4 + 0x24))(piVar4,param_2);
              iVar5 = *param_1;
              if (iVar5 < param_2) {
                iVar5 = param_2;
              }
              *param_1 = iVar5 + 1;
              _ZN11CGameObject7SetZoneEP5CZoneb(piVar4,(int)uVar7,0);
              _ZN11CGameObject6ReInitEb(piVar4,1);
              (**(code **)(*piVar4 + 0x78))(piVar4);
              return piVar4;
            }
          }
        }
      }
      iVar6 = iVar6 + -1;
      if (iVar6 < 0) break;
      iVar3 = param_1[1];
    }
  }
  iVar5 = _ZN6CLevel8GetLevelEv();
  piVar4 = (int *)_ZN18CGameObjectManager23CreateObjectFromLibraryEiP5CZoneRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS4_6memory13E_MEMORY_HINTE0EEEE
                            (*(undefined4 *)(iVar5 + 0xa94),param_3,(int)uVar7,param_5);
  (**(code **)(*piVar4 + 0x24))(piVar4,param_2);
  iVar5 = *param_1;
  if (iVar5 < param_2) {
    iVar5 = param_2;
  }
  iVar3 = *piVar4;
  *param_1 = iVar5 + 1;
  (**(code **)(iVar3 + 0x74))(piVar4);
  puVar2 = (undefined4 *)param_1[2];
  if (puVar2 == (undefined4 *)param_1[3]) {
    local_2c[0] = piVar4;
    _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
              (param_1 + 1,puVar2,local_2c);
  }
  else {
    if (puVar2 == (undefined4 *)0x0) {
      iVar5 = 0;
    }
    else {
      *puVar2 = piVar4;
      iVar5 = param_1[2];
    }
    param_1[2] = iVar5 + 4;
  }
  return piVar4;
}


