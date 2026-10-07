// _ZN13CZonesManager4InitEb @ 002cfac4

void _ZN13CZonesManager4InitEb(int param_1,int param_2)

{
  int iVar1;
  int *piVar2;
  int *__dest;
  int *piVar3;
  int extraout_r1;
  int extraout_r1_00;
  int *piVar4;
  int *piVar5;
  int iVar6;
  undefined4 *puVar7;
  int *piVar8;
  int iVar9;
  int *piVar10;
  undefined4 *puVar11;
  int *piVar12;
  int iVar13;
  int *piVar14;
  int iVar15;
  int *piVar16;
  int *piVar17;
  
  _ZN22GameObjectCacheManager4InitEb(*(undefined4 *)(param_1 + 0x68));
  iVar13 = extraout_r1;
  if (param_2 != 0) {
    puVar11 = *(undefined4 **)(DAT_002cfe2c + 0x2cfe10);
    for (puVar7 = (undefined4 *)*puVar11; puVar7 != (undefined4 *)puVar11[1]; puVar7 = puVar7 + 1) {
      _ZN11CZonePortal4InitEb_constprop_2830(*puVar7);
      iVar13 = extraout_r1_00;
    }
  }
  piVar4 = *(int **)(param_1 + 0x84);
  piVar8 = *(int **)(param_1 + 0x80);
  if (piVar4 != *(int **)(param_1 + 0x80)) {
    do {
      piVar12 = piVar8 + 1;
      iVar9 = *piVar8;
      _ZN11ObjManagers9InitBeginEv(*(undefined4 *)(iVar9 + 0x134),iVar13);
      _ZN5CZone20UpdateAddRemoveListsEv(iVar9);
      iVar13 = *(int *)(*(int *)(iVar9 + 0x134) + 0xc);
      iVar15 = *(int *)(iVar13 + 0x10);
      if (0 < iVar15) {
        iVar6 = 0;
        do {
          iVar1 = iVar6 * 4;
          iVar6 = iVar6 + 1;
          (**(code **)(**(int **)(*(int *)(iVar13 + 0xc) + iVar1) + 0x74))();
        } while (iVar6 != iVar15);
      }
      for (puVar7 = *(undefined4 **)(iVar9 + 0x1b8); puVar7 != *(undefined4 **)(iVar9 + 0x1bc);
          puVar7 = puVar7 + 1) {
        (**(code **)(*(int *)*puVar7 + 0x40))();
      }
      *(undefined4 *)(iVar9 + 0x1d4) = *(undefined4 *)(iVar9 + 0x1d0);
      piVar4 = *(int **)(param_1 + 0x84);
      iVar13 = iVar9;
      piVar8 = piVar12;
    } while (piVar4 != piVar12);
  }
  for (piVar8 = *(int **)(param_1 + 0x80); piVar8 != piVar4; piVar8 = piVar8 + 1) {
    _ZN5CZone5Init2Ev(*piVar8);
    piVar4 = *(int **)(param_1 + 0x84);
  }
  piVar8 = *(int **)(param_1 + 0x80);
  if (*(int **)(param_1 + 0x80) != piVar4) {
    do {
      piVar4 = piVar8 + 1;
      iVar13 = *piVar8;
      piVar17 = *(int **)(iVar13 + 0x140);
      piVar14 = *(int **)(iVar13 + 0x14c);
      piVar12 = *(int **)(iVar13 + 0x148);
      piVar8 = *(int **)(iVar13 + 0x13c);
      if (piVar17 != *(int **)(iVar13 + 0x13c)) {
        do {
          piVar10 = piVar8 + 1;
          iVar15 = (int)piVar14 - (int)piVar12;
          iVar9 = iVar15 >> 4;
          piVar3 = piVar12;
          if (0 < iVar9) {
            iVar15 = *piVar8;
            __dest = piVar12;
            if (*piVar12 != iVar15) {
              if (iVar15 == piVar12[1]) {
                __dest = piVar12 + 1;
              }
              else if (iVar15 == piVar12[2]) {
                __dest = piVar12 + 2;
              }
              else {
                piVar5 = piVar12;
                if (iVar15 == piVar12[3]) {
                  __dest = piVar12 + 3;
                }
                else {
                  do {
                    iVar9 = iVar9 + -1;
                    piVar3 = piVar5 + 4;
                    if (iVar9 == 0) {
                      iVar15 = (int)piVar14 - (int)piVar3;
                      goto LAB_002cfc9c;
                    }
                    piVar16 = piVar5 + 7;
                    __dest = piVar3;
                  } while ((((piVar5[4] != iVar15) && (__dest = piVar5 + 5, piVar5[5] != iVar15)) &&
                           (__dest = piVar5 + 6, piVar5[6] != iVar15)) &&
                          (piVar2 = piVar5 + 7, piVar5 = piVar3, __dest = piVar16, *piVar2 != iVar15
                          ));
                }
              }
            }
            goto joined_r0x002cfd68;
          }
LAB_002cfc9c:
          iVar15 = iVar15 >> 2;
          if (iVar15 == 2) {
            iVar9 = *piVar8;
LAB_002cfde0:
            __dest = piVar3;
            if (*piVar3 != iVar9) {
              piVar3 = piVar3 + 1;
LAB_002cfdbc:
              __dest = piVar3;
              if (*piVar3 != iVar9) {
                __dest = piVar14;
              }
            }
          }
          else if (iVar15 == 3) {
            iVar9 = *piVar8;
            __dest = piVar3;
            if (*piVar3 != iVar9) {
              piVar3 = piVar3 + 1;
              goto LAB_002cfde0;
            }
          }
          else {
            __dest = piVar14;
            if (iVar15 == 1) {
              iVar9 = *piVar8;
              goto LAB_002cfdbc;
            }
          }
joined_r0x002cfd68:
          if (__dest == piVar14) {
            iVar9 = *piVar8;
            _ZN23ObjManager_BinarySearch15AddObjectToListEP11CGameObjectb
                      (*(undefined4 *)(iVar13 + 0x138),iVar9,0);
            _ZN11ObjManagers16AddObjectToListsEP11CGameObjectt
                      (*(undefined4 *)(iVar13 + 0x134),iVar9,*(undefined2 *)(iVar9 + 0x104));
            piVar14 = *(int **)(iVar13 + 0x14c);
            piVar17 = *(int **)(iVar13 + 0x140);
            piVar12 = *(int **)(iVar13 + 0x148);
          }
          else {
            piVar8 = __dest + 1;
            if ((piVar8 != piVar14) && (iVar9 = (int)piVar14 - (int)piVar8 >> 2, iVar9 != 0)) {
              memmove(__dest,piVar8,iVar9 << 2);
              piVar14 = *(int **)(iVar13 + 0x14c);
              piVar17 = *(int **)(iVar13 + 0x140);
              piVar12 = *(int **)(iVar13 + 0x148);
            }
            piVar14 = piVar14 + -1;
            *(int **)(iVar13 + 0x14c) = piVar14;
          }
          piVar8 = piVar10;
        } while (piVar17 != piVar10);
      }
      *(undefined4 *)(iVar13 + 0x140) = *(undefined4 *)(iVar13 + 0x13c);
      for (; piVar12 != piVar14; piVar12 = piVar12 + 1) {
        iVar9 = *piVar12;
        _ZN23ObjManager_BinarySearch20RemoveObjectFromListEP11CGameObject
                  (*(undefined4 *)(iVar13 + 0x138),iVar9);
        _ZN11ObjManagers21RemoveObjectFromListsEP11CGameObject
                  (*(undefined4 *)(iVar13 + 0x134),iVar9);
        piVar14 = *(int **)(iVar13 + 0x14c);
      }
      *(undefined4 *)(iVar13 + 0x14c) = *(undefined4 *)(iVar13 + 0x148);
      piVar8 = piVar4;
    } while (piVar4 != *(int **)(param_1 + 0x84));
  }
  return;
}


