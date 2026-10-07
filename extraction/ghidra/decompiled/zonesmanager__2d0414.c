// _ZN13CZonesManager6UpdateEf @ 002d0414

void _ZN13CZonesManager6UpdateEf(int param_1,undefined4 param_2)

{
  int *piVar1;
  int *__dest;
  int *piVar2;
  int *piVar3;
  undefined4 extraout_r1;
  undefined4 uVar4;
  undefined4 extraout_r1_00;
  int iVar5;
  int *piVar6;
  int iVar7;
  int iVar8;
  int *piVar9;
  int *piVar10;
  int *piVar11;
  int *piVar12;
  int *piVar13;
  int *piVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  undefined8 uVar19;
  float local_48;
  float local_44;
  float local_40;
  float local_3c;
  float local_38;
  float local_34;
  
  piVar2 = *(int **)(param_1 + 0x84);
  piVar9 = *(int **)(param_1 + 0x80);
  if (*(int **)(param_1 + 0x80) != piVar2) {
    do {
      piVar11 = piVar9 + 1;
      iVar8 = *piVar9;
      piVar14 = *(int **)(iVar8 + 0x140);
      piVar12 = *(int **)(iVar8 + 0x14c);
      piVar2 = *(int **)(iVar8 + 0x148);
      piVar9 = *(int **)(iVar8 + 0x13c);
      if (piVar14 != *(int **)(iVar8 + 0x13c)) {
        do {
          piVar10 = piVar9 + 1;
          iVar5 = (int)piVar12 - (int)piVar2;
          iVar7 = iVar5 >> 4;
          piVar3 = piVar2;
          if (0 < iVar7) {
            iVar5 = *piVar9;
            __dest = piVar2;
            if (*piVar2 != iVar5) {
              if (iVar5 == piVar2[1]) {
                __dest = piVar2 + 1;
              }
              else if (iVar5 == piVar2[2]) {
                __dest = piVar2 + 2;
              }
              else {
                piVar6 = piVar2;
                if (iVar5 == piVar2[3]) {
                  __dest = piVar2 + 3;
                }
                else {
                  do {
                    iVar7 = iVar7 + -1;
                    piVar3 = piVar6 + 4;
                    if (iVar7 == 0) {
                      iVar5 = (int)piVar12 - (int)piVar3;
                      goto LAB_002d0518;
                    }
                    piVar13 = piVar6 + 7;
                    __dest = piVar3;
                  } while ((((iVar5 != piVar6[4]) && (__dest = piVar6 + 5, iVar5 != piVar6[5])) &&
                           (__dest = piVar6 + 6, iVar5 != piVar6[6])) &&
                          (piVar1 = piVar6 + 7, piVar6 = piVar3, __dest = piVar13, iVar5 != *piVar1)
                          );
                }
              }
            }
            goto joined_r0x002d0820;
          }
LAB_002d0518:
          iVar5 = iVar5 >> 2;
          if (iVar5 == 2) {
            iVar7 = *piVar9;
LAB_002d0898:
            __dest = piVar3;
            if (*piVar3 != iVar7) {
              piVar3 = piVar3 + 1;
LAB_002d0874:
              __dest = piVar3;
              if (*piVar3 != iVar7) {
                __dest = piVar12;
              }
            }
          }
          else if (iVar5 == 3) {
            iVar7 = *piVar9;
            __dest = piVar3;
            if (*piVar3 != iVar7) {
              piVar3 = piVar3 + 1;
              goto LAB_002d0898;
            }
          }
          else {
            __dest = piVar12;
            if (iVar5 == 1) {
              iVar7 = *piVar9;
              goto LAB_002d0874;
            }
          }
joined_r0x002d0820:
          if (__dest == piVar12) {
            iVar7 = *piVar9;
            _ZN23ObjManager_BinarySearch15AddObjectToListEP11CGameObjectb
                      (*(undefined4 *)(iVar8 + 0x138),iVar7,0);
            _ZN11ObjManagers16AddObjectToListsEP11CGameObjectt
                      (*(undefined4 *)(iVar8 + 0x134),iVar7,*(undefined2 *)(iVar7 + 0x104));
            piVar12 = *(int **)(iVar8 + 0x14c);
            piVar14 = *(int **)(iVar8 + 0x140);
            piVar2 = *(int **)(iVar8 + 0x148);
          }
          else {
            piVar9 = __dest + 1;
            if ((piVar9 != piVar12) && (iVar7 = (int)piVar12 - (int)piVar9 >> 2, iVar7 != 0)) {
              memmove(__dest,piVar9,iVar7 << 2);
              piVar12 = *(int **)(iVar8 + 0x14c);
              piVar14 = *(int **)(iVar8 + 0x140);
              piVar2 = *(int **)(iVar8 + 0x148);
            }
            piVar12 = piVar12 + -1;
            *(int **)(iVar8 + 0x14c) = piVar12;
          }
          piVar9 = piVar10;
        } while (piVar14 != piVar10);
      }
      *(undefined4 *)(iVar8 + 0x140) = *(undefined4 *)(iVar8 + 0x13c);
      for (; piVar2 != piVar12; piVar2 = piVar2 + 1) {
        iVar7 = *piVar2;
        _ZN23ObjManager_BinarySearch20RemoveObjectFromListEP11CGameObject
                  (*(undefined4 *)(iVar8 + 0x138),iVar7);
        _ZN11ObjManagers21RemoveObjectFromListsEP11CGameObject(*(undefined4 *)(iVar8 + 0x134),iVar7)
        ;
        piVar12 = *(int **)(iVar8 + 0x14c);
      }
      *(undefined4 *)(iVar8 + 0x14c) = *(undefined4 *)(iVar8 + 0x148);
      piVar2 = *(int **)(param_1 + 0x84);
      piVar9 = piVar11;
    } while (piVar11 != piVar2);
  }
  piVar9 = *(int **)(param_1 + 0x80);
LAB_002d05c4:
  piVar11 = piVar9;
  if (piVar9 != piVar2) {
    while( true ) {
      piVar9 = piVar11 + 1;
      iVar8 = *piVar11;
      if (*(char *)(iVar8 + 0x17d) == '\0') break;
      *(undefined1 *)(iVar8 + 0x1e4) = 1;
      if (*(int *)(iVar8 + 0x154) != 0) {
        if (*(int *)(iVar8 + 0x158) == 0) {
          *(int *)(iVar8 + 0x158) = *(int *)(iVar8 + 0x154);
        }
        _ZN11ObjManagers6UpdateEfb(*(undefined4 *)(iVar8 + 0x134),param_2,1);
        piVar2 = *(int **)(param_1 + 0x84);
        goto LAB_002d05c4;
      }
      if (*(int *)(iVar8 + 0x158) != 0) {
        *(undefined4 *)(iVar8 + 0x158) = 0;
      }
      piVar11 = piVar9;
      if (piVar9 == piVar2) goto LAB_002d060c;
    }
    *(undefined1 *)(iVar8 + 0x1e4) = 0;
    goto LAB_002d05c4;
  }
LAB_002d060c:
  piVar11 = *(int **)(DAT_002d09a8 + 0x2d061c);
  _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv(&local_3c,*(undefined4 *)(*piVar11 + 0xe4));
  local_48 = local_3c;
  local_44 = local_38;
  local_40 = local_34;
  piVar2 = (int *)_ZN13CZonesManager17GetZoneByWorldBoxEN6glitch4core8vector3dIfEEP5CZone
                            (param_1,&local_48,*(undefined4 *)(param_1 + 0x6c));
  piVar9 = *(int **)(param_1 + 0x6c);
  if (((piVar2 == (int *)0x0) || (piVar2 == piVar9)) || (*(char *)((int)piVar2 + 0x17d) != '\0')) {
    if (piVar9 == (int *)0x0) goto LAB_002d0758;
    iVar7 = piVar9[0x55];
    *(undefined1 *)(piVar9 + 0x79) = 1;
    iVar8 = piVar9[0x56];
    if (iVar7 == 0) goto LAB_002d068c;
LAB_002d0920:
    if (iVar8 == 0) {
      piVar9[0x56] = iVar7;
    }
    _ZN11ObjManagers6UpdateEfb(piVar9[0x4d],param_2,1);
  }
  else {
    *(int **)(param_1 + 0x6c) = piVar2;
    iVar7 = piVar2[0x55];
    *(undefined1 *)(piVar2 + 0x79) = 1;
    iVar8 = piVar2[0x56];
    piVar9 = piVar2;
    if (iVar7 != 0) goto LAB_002d0920;
LAB_002d068c:
    if (iVar8 != 0) {
      piVar9[0x56] = 0;
    }
  }
  fVar18 = (float)piVar9[0x60] * (float)piVar9[0x60];
  _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv(&local_3c,*(undefined4 *)(*piVar11 + 0xe4));
  piVar2 = (int *)piVar9[0x59];
  piVar11 = (int *)piVar9[0x58];
LAB_002d06b8:
  piVar12 = piVar11;
  if (piVar11 != piVar2) {
    while( true ) {
      piVar11 = piVar12 + 1;
      iVar8 = *piVar12;
      if (*(char *)(iVar8 + 8) == '\0') break;
      piVar2 = *(int **)(iVar8 + 0x78);
      if (piVar9 == piVar2) {
        piVar2 = *(int **)(iVar8 + 0x7c);
      }
      iVar8 = (**(code **)(*piVar2 + 0x54))(piVar2);
      if ((iVar8 == 0) || ((char)piVar2[0x79] != '\0')) {
LAB_002d074c:
        piVar2 = (int *)piVar9[0x59];
      }
      else {
        if (fVar18 == 0.0) {
          *(undefined1 *)(piVar2 + 0x79) = 1;
          iVar8 = piVar2[0x56];
          if (piVar2[0x55] == 0) {
LAB_002d08ec:
            if (iVar8 == 0) goto LAB_002d074c;
            piVar2[0x56] = 0;
            piVar2 = (int *)piVar9[0x59];
          }
          else {
            if (iVar8 == 0) {
              piVar2[0x56] = piVar2[0x55];
            }
            _ZN11ObjManagers6UpdateEfb(piVar2[0x4d],param_2,1);
            piVar2 = (int *)piVar9[0x59];
          }
          break;
        }
        iVar8 = *piVar12;
        fVar17 = *(float *)(iVar8 + 0x6c) - local_3c;
        fVar15 = *(float *)(iVar8 + 0x70) - local_38;
        fVar16 = *(float *)(iVar8 + 0x74) - local_34;
        if (fVar18 <= fVar17 * fVar17 + fVar15 * fVar15 + fVar16 * fVar16) goto LAB_002d074c;
        *(undefined1 *)(piVar2 + 0x79) = 1;
        iVar8 = piVar2[0x56];
        if (piVar2[0x55] == 0) goto LAB_002d08ec;
        if (iVar8 == 0) {
          piVar2[0x56] = piVar2[0x55];
        }
        _ZN11ObjManagers6UpdateEfb(piVar2[0x4d],param_2,1);
        piVar2 = (int *)piVar9[0x59];
      }
      piVar12 = piVar11;
      if (piVar11 == piVar2) goto LAB_002d0758;
    }
    goto LAB_002d06b8;
  }
LAB_002d0758:
  _ZN19CActorBaseComponent21CheckActorsCollisionsEPSt6vectorIP11CGameObjectSaIS2_EE(param_1 + 0x54);
  piVar9 = *(int **)(param_1 + 0x80);
  uVar4 = extraout_r1;
LAB_002d0764:
  do {
    piVar2 = piVar9;
    if (*(int **)(param_1 + 0x84) == piVar9) {
LAB_002d07c0:
      *(undefined1 *)(*(int *)(param_1 + 100) + 0x20) = 0;
      _ZN13CZonesManager24HandleZoneUnloadRequestsEv(param_1);
      _ZN13CZonesManager22HandleZoneLoadRequestsEb(param_1,1);
      _ZN13CZonesManager20RefreshAllActorsPoolEv(param_1);
      *(undefined1 *)(*(int *)(param_1 + 100) + 0x20) = 1;
      return;
    }
    while( true ) {
      piVar9 = piVar2 + 1;
      uVar19 = (**(code **)(*(int *)*piVar2 + 0x54))((int *)*piVar2,uVar4);
      uVar4 = (undefined4)((ulonglong)uVar19 >> 0x20);
      if (((int)uVar19 == 0) || (iVar8 = *piVar2, *(char *)(iVar8 + 0x1e4) != '\0'))
      goto LAB_002d0764;
      if (*(int *)(iVar8 + 0x154) != 0) break;
      if (*(int *)(iVar8 + 0x158) != 0) {
        *(undefined4 *)(iVar8 + 0x158) = 0;
      }
      uVar4 = param_2;
      piVar2 = piVar9;
      if (*(int **)(param_1 + 0x84) == piVar9) goto LAB_002d07c0;
    }
    if (*(int *)(iVar8 + 0x158) == 0) {
      *(int *)(iVar8 + 0x158) = *(int *)(iVar8 + 0x154);
    }
    _ZN11ObjManagers6UpdateEfb(*(undefined4 *)(iVar8 + 0x134));
    uVar4 = extraout_r1_00;
  } while( true );
}


