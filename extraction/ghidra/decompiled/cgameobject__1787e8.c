// _Z22CGetWeaponCachesInZoneP11CGameObjectfRSt6vectorIS0_SaIS0_EE @ 001787e8

int _Z22CGetWeaponCachesInZoneP11CGameObjectfRSt6vectorIS0_SaIS0_EE
              (int param_1,undefined4 param_2,int *param_3)

{
  undefined4 uVar1;
  int iVar2;
  void *__dest;
  undefined4 *puVar3;
  undefined4 *puVar4;
  size_t __n;
  int iVar6;
  uint uVar7;
  void *__src;
  undefined4 uVar8;
  undefined4 *local_2c;
  undefined4 *local_28;
  undefined4 local_24;
  undefined4 *puVar5;
  
  local_2c = (undefined4 *)0x0;
  local_28 = (undefined4 *)0x0;
  local_24 = 0;
  if (param_1 == 0) {
    return 0;
  }
  if (*(int *)(param_1 + 0xbc) == 0) {
    return 0;
  }
  uVar1 = _ZN6CLevel8GetLevelEv();
  _ZN6CLevel27GetObjects_fromTypeAndRangeEPSt6vectorIP11CGameObjectSaIS2_EEifS2_
            (uVar1,&local_2c,0x4c728,param_2,param_1);
  __src = (void *)*param_3;
  iVar6 = param_3[1] - (int)__src >> 2;
  iVar2 = (int)local_28 - (int)local_2c >> 2;
  uVar7 = iVar2 + iVar6;
  if (0x3fffffff < uVar7) {
                    /* WARNING: Subroutine does not return */
    _ZSt20__throw_length_errorPKc((int)&DAT_001789d8 + DAT_001789d8);
  }
  if ((uint)(param_3[2] - (int)__src >> 2) < uVar7) {
    if (uVar7 == 0) {
      __dest = (void *)0x0;
      iVar2 = 0;
    }
    else {
      iVar2 = uVar7 * 4;
      __dest = (void *)_Znwj(iVar2);
    }
    if (iVar6 == 0) {
      __n = 0;
    }
    else {
      __n = iVar6 << 2;
      memmove(__dest,__src,__n);
    }
    if (*param_3 != 0) {
      _ZdlPv();
    }
    *param_3 = (int)__dest;
    param_3[1] = (int)__dest + __n;
    param_3[2] = (int)__dest + iVar2;
    if ((int)local_28 - (int)local_2c >> 2 == 0) {
      iVar6 = 0;
      goto LAB_001788bc;
    }
  }
  else {
    iVar6 = 0;
    if (iVar2 == 0) goto LAB_001788bc;
  }
  iVar6 = 0;
  puVar4 = local_2c;
  if (local_2c != local_28) {
    do {
      puVar5 = puVar4 + 1;
      iVar2 = (**(code **)(*(int *)*puVar4 + 0x54))();
      if (iVar2 != 0) {
        uVar8 = *(undefined4 *)(param_1 + 0xbc);
        uVar1 = (**(code **)(*(int *)*puVar4 + 0x18))();
        iVar2 = _ZN15CNpcAIComponent19NPCTestForPathExactERKN6glitch4core8vector3dIfEE(uVar8,uVar1);
        if (iVar2 != 0) {
          puVar3 = (undefined4 *)param_3[1];
          if (puVar3 == (undefined4 *)param_3[2]) {
            _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                      (param_3,puVar3,puVar4);
          }
          else {
            iVar2 = 0;
            if (puVar3 != (undefined4 *)0x0) {
              *puVar3 = *puVar4;
              iVar2 = param_3[1];
            }
            param_3[1] = iVar2 + 4;
          }
          iVar6 = iVar6 + 1;
        }
      }
      puVar4 = puVar5;
    } while (puVar5 != local_28);
  }
LAB_001788bc:
  if (local_2c != (undefined4 *)0x0) {
    _ZdlPv();
  }
  return iVar6;
}

