// _ZN13CZonesManager24HandleZoneUnloadRequestsEv @ 002d09b0

void _ZN13CZonesManager24HandleZoneUnloadRequestsEv(int param_1)

{
  int *piVar1;
  int *__dest;
  int iVar2;
  undefined4 uVar3;
  int *piVar4;
  int *__dest_00;
  int *piVar5;
  int iVar6;
  int *piVar7;
  int *piVar8;
  code *pcVar9;
  int iVar10;
  int *piVar11;
  int *piVar12;
  int *piVar13;
  int *piVar14;
  int *piVar15;
  int *piVar16;
  int *local_34;
  
  local_34 = *(int **)(param_1 + 0x40);
  piVar16 = *(int **)(param_1 + 0x44);
  if (local_34 != piVar16) {
    do {
      piVar13 = *(int **)(param_1 + 0x80);
      piVar5 = *(int **)(param_1 + 0x84);
      piVar8 = piVar13;
      do {
        __dest_00 = piVar8;
        if (__dest_00 == piVar5) goto LAB_002d0a18;
        piVar12 = (int *)*__dest_00;
        piVar8 = __dest_00 + 1;
      } while (piVar12[2] != *local_34);
      if (piVar13 != piVar5) {
        do {
          piVar8 = piVar13 + 1;
          iVar2 = *piVar13;
          piVar15 = *(int **)(iVar2 + 0x140);
          piVar5 = *(int **)(iVar2 + 0x14c);
          piVar13 = *(int **)(iVar2 + 0x148);
          piVar16 = *(int **)(iVar2 + 0x13c);
          if (piVar15 != *(int **)(iVar2 + 0x13c)) {
            do {
              piVar11 = piVar16 + 1;
              iVar6 = (int)piVar5 - (int)piVar13;
              iVar10 = iVar6 >> 4;
              piVar4 = piVar13;
              if (0 < iVar10) {
                iVar6 = *piVar16;
                __dest = piVar13;
                if (*piVar13 != iVar6) {
                  if (iVar6 == piVar13[1]) {
                    __dest = piVar13 + 1;
                  }
                  else if (iVar6 == piVar13[2]) {
                    __dest = piVar13 + 2;
                  }
                  else {
                    piVar7 = piVar13;
                    if (iVar6 == piVar13[3]) {
                      __dest = piVar13 + 3;
                    }
                    else {
                      do {
                        iVar10 = iVar10 + -1;
                        piVar4 = piVar7 + 4;
                        if (iVar10 == 0) {
                          iVar6 = (int)piVar5 - (int)piVar4;
                          goto LAB_002d0b90;
                        }
                        piVar14 = piVar7 + 7;
                        __dest = piVar4;
                      } while ((((piVar7[4] != iVar6) && (__dest = piVar7 + 5, piVar7[5] != iVar6))
                               && (__dest = piVar7 + 6, piVar7[6] != iVar6)) &&
                              (piVar1 = piVar7 + 7, piVar7 = piVar4, __dest = piVar14,
                              *piVar1 != iVar6));
                    }
                  }
                }
                goto joined_r0x002d0d70;
              }
LAB_002d0b90:
              iVar6 = iVar6 >> 2;
              if (iVar6 == 2) {
                iVar10 = *piVar16;
LAB_002d0de8:
                __dest = piVar4;
                if (*piVar4 != iVar10) {
                  piVar4 = piVar4 + 1;
LAB_002d0dc4:
                  __dest = piVar4;
                  if (*piVar4 != iVar10) {
                    __dest = piVar5;
                  }
                }
              }
              else if (iVar6 == 3) {
                iVar10 = *piVar16;
                __dest = piVar4;
                if (*piVar4 != iVar10) {
                  piVar4 = piVar4 + 1;
                  goto LAB_002d0de8;
                }
              }
              else {
                __dest = piVar5;
                if (iVar6 == 1) {
                  iVar10 = *piVar16;
                  goto LAB_002d0dc4;
                }
              }
joined_r0x002d0d70:
              if (__dest == piVar5) {
                iVar10 = *piVar16;
                _ZN23ObjManager_BinarySearch15AddObjectToListEP11CGameObjectb
                          (*(undefined4 *)(iVar2 + 0x138),iVar10,0);
                _ZN11ObjManagers16AddObjectToListsEP11CGameObjectt
                          (*(undefined4 *)(iVar2 + 0x134),iVar10,*(undefined2 *)(iVar10 + 0x104));
                piVar5 = *(int **)(iVar2 + 0x14c);
                piVar15 = *(int **)(iVar2 + 0x140);
                piVar13 = *(int **)(iVar2 + 0x148);
              }
              else {
                piVar16 = __dest + 1;
                if ((piVar16 != piVar5) && (iVar10 = (int)piVar5 - (int)piVar16 >> 2, iVar10 != 0))
                {
                  memmove(__dest,piVar16,iVar10 << 2);
                  piVar5 = *(int **)(iVar2 + 0x14c);
                  piVar15 = *(int **)(iVar2 + 0x140);
                  piVar13 = *(int **)(iVar2 + 0x148);
                }
                piVar5 = piVar5 + -1;
                *(int **)(iVar2 + 0x14c) = piVar5;
              }
              piVar16 = piVar11;
            } while (piVar15 != piVar11);
          }
          *(undefined4 *)(iVar2 + 0x140) = *(undefined4 *)(iVar2 + 0x13c);
          for (; piVar13 != piVar5; piVar13 = piVar13 + 1) {
            iVar10 = *piVar13;
            _ZN23ObjManager_BinarySearch20RemoveObjectFromListEP11CGameObject
                      (*(undefined4 *)(iVar2 + 0x138),iVar10);
            _ZN11ObjManagers21RemoveObjectFromListsEP11CGameObject
                      (*(undefined4 *)(iVar2 + 0x134),iVar10);
            piVar5 = *(int **)(iVar2 + 0x14c);
          }
          *(undefined4 *)(iVar2 + 0x14c) = *(undefined4 *)(iVar2 + 0x148);
          piVar5 = *(int **)(param_1 + 0x84);
          piVar13 = piVar8;
        } while (piVar8 != piVar5);
      }
      piVar16 = *(int **)(param_1 + 0x80);
      while (piVar16 != piVar5) {
        while( true ) {
          iVar2 = *piVar16;
          piVar16 = piVar16 + 1;
          iVar2 = *(int *)(iVar2 + 0x138);
          if (*(int *)(iVar2 + 0x10) < 1) break;
          iVar10 = 0;
          do {
            iVar6 = iVar10 * 4;
            iVar10 = iVar10 + 1;
            _ZN11CGameObject19CleanContactHistoryEv(*(undefined4 *)(*(int *)(iVar2 + 0xc) + iVar6));
          } while (iVar10 < *(int *)(iVar2 + 0x10));
          piVar5 = *(int **)(param_1 + 0x84);
          if (piVar16 == piVar5) goto LAB_002d0c94;
        }
      }
LAB_002d0c94:
      uVar3 = _ZN6CLevel8GetLevelEv();
      _ZN6CLevel12OnZoneUnloadEP5CZone(uVar3,piVar12);
      _ZN22GameObjectCacheManager9RemoveAllEP5CZone(*(undefined4 *)(param_1 + 0x68),piVar12);
      piVar8 = *(int **)(param_1 + 0x84);
      piVar16 = __dest_00 + 1;
      if ((piVar16 != piVar8) && (iVar2 = (int)piVar8 - (int)piVar16 >> 2, iVar2 != 0)) {
        memmove(__dest_00,piVar16,iVar2 << 2);
        piVar8 = *(int **)(param_1 + 0x84);
      }
      *(int **)(param_1 + 0x84) = piVar8 + -1;
      if (*(int **)(param_1 + 0x6c) == piVar12) {
        *(undefined4 *)(param_1 + 0x6c) = 0;
      }
      iVar2 = _ZN6CLevel8GetLevelEv();
      piVar8 = *(int **)(iVar2 + 0xec);
      piVar16 = (int *)(**(code **)(*piVar8 + 0xa0))(piVar8);
      if (piVar12 == piVar16) {
        iVar2 = *(int *)(param_1 + 0x6c);
        if (iVar2 == 0) {
          uVar3 = (**(code **)(*piVar8 + 0x18))(piVar8);
          iVar2 = _ZN13CZonesManager14GetZoneFromPosERKN6glitch4core8vector3dIfEE(param_1,uVar3);
          if ((iVar2 == 0) || (*(char *)(iVar2 + 0x17d) == '\0')) {
            *(int *)(param_1 + 0x6c) = iVar2;
          }
          else {
            iVar2 = *(int *)(param_1 + 0x6c);
          }
        }
        _ZN11CGameObject7SetZoneEP5CZoneb(piVar8,iVar2,1);
      }
      pcVar9 = *(code **)(*piVar12 + 4);
      *(undefined1 *)(param_1 + 0x50) = 1;
      (*pcVar9)(piVar12);
      piVar16 = *(int **)(param_1 + 0x44);
      *(undefined1 *)(param_1 + 0x50) = 0;
LAB_002d0a18:
      local_34 = local_34 + 1;
    } while (local_34 != piVar16);
  }
  if (*(char *)(param_1 + 0x7d) == '\0') {
    if ((uint)((int)local_34 - *(int *)(param_1 + 0x40)) >> 2 == 0) {
      *(int *)(param_1 + 0x44) = *(int *)(param_1 + 0x40);
      return;
    }
    _ZN11CHUDDisplay12OnZoneUnloadEv(**(undefined4 **)(DAT_002d0edc + 0x2d0e44));
    *(undefined4 *)(param_1 + 0x44) = *(undefined4 *)(param_1 + 0x40);
    if (*(char *)(param_1 + 0x7d) == '\0') {
      return;
    }
  }
  else {
    *(undefined4 *)(param_1 + 0x44) = *(undefined4 *)(param_1 + 0x40);
  }
  *(undefined1 *)(param_1 + 0x7d) = 0;
  iVar2 = _ZN6CLevel8GetLevelEv();
  if (*(int *)(iVar2 + 0xec) != 0) {
    _ZN6CLevel8GetLevelEv();
    iVar2 = _ZNK6CLevel18GetPlayerComponentEv();
    if ((*(int *)(iVar2 + 0x26c) != -1) &&
       (*(char *)(*(int *)(DAT_002d0ed8 + 0x2d0a78) + 0x7d) == '\0')) {
      uVar3 = _ZN13CZonesManager10FindObjectEit
                        (*(int *)(DAT_002d0ed8 + 0x2d0a78),*(int *)(iVar2 + 0x26c),8);
      _ZN15PlayerComponent8SaveGameEP17CSpawnPointObject(iVar2,uVar3);
      *(undefined4 *)(iVar2 + 0x26c) = 0xffffffff;
    }
  }
  return;
}


