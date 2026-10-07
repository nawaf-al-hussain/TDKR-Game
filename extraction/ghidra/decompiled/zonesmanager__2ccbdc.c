// _ZN13CZonesManager20UpdateAddRemoveListsEv @ 002ccbdc

void _ZN13CZonesManager20UpdateAddRemoveListsEv(int param_1)

{
  int *piVar1;
  int *__dest;
  int *piVar2;
  int *piVar3;
  int *piVar4;
  int iVar5;
  int *piVar6;
  int iVar7;
  int *piVar8;
  int iVar9;
  int *piVar10;
  int *piVar11;
  int *piVar12;
  int *piVar13;
  
  piVar3 = *(int **)(param_1 + 0x80);
  if (*(int **)(param_1 + 0x84) != *(int **)(param_1 + 0x80)) {
    do {
      piVar4 = piVar3 + 1;
      iVar7 = *piVar3;
      piVar13 = *(int **)(iVar7 + 0x140);
      piVar11 = *(int **)(iVar7 + 0x14c);
      piVar10 = *(int **)(iVar7 + 0x148);
      piVar3 = *(int **)(iVar7 + 0x13c);
      if (piVar13 != *(int **)(iVar7 + 0x13c)) {
        do {
          piVar8 = piVar3 + 1;
          iVar5 = (int)piVar11 - (int)piVar10;
          iVar9 = iVar5 >> 4;
          piVar2 = piVar10;
          if (0 < iVar9) {
            iVar5 = *piVar3;
            __dest = piVar10;
            if (*piVar10 != iVar5) {
              if (iVar5 == piVar10[1]) {
                __dest = piVar10 + 1;
              }
              else if (iVar5 == piVar10[2]) {
                __dest = piVar10 + 2;
              }
              else {
                piVar6 = piVar10;
                if (iVar5 == piVar10[3]) {
                  __dest = piVar10 + 3;
                }
                else {
                  do {
                    iVar9 = iVar9 + -1;
                    piVar2 = piVar6 + 4;
                    if (iVar9 == 0) {
                      iVar5 = (int)piVar11 - (int)piVar2;
                      goto LAB_002ccce4;
                    }
                    piVar12 = piVar6 + 7;
                    __dest = piVar2;
                  } while ((((piVar6[4] != iVar5) && (__dest = piVar6 + 5, piVar6[5] != iVar5)) &&
                           (__dest = piVar6 + 6, iVar5 != piVar6[6])) &&
                          (piVar1 = piVar6 + 7, piVar6 = piVar2, __dest = piVar12, iVar5 != *piVar1)
                          );
                }
              }
            }
            goto joined_r0x002ccdb0;
          }
LAB_002ccce4:
          iVar5 = iVar5 >> 2;
          if (iVar5 == 2) {
            iVar9 = *piVar3;
LAB_002cce28:
            __dest = piVar2;
            if (*piVar2 != iVar9) {
              piVar2 = piVar2 + 1;
LAB_002cce04:
              __dest = piVar2;
              if (*piVar2 != iVar9) {
                __dest = piVar11;
              }
            }
          }
          else if (iVar5 == 3) {
            iVar9 = *piVar3;
            __dest = piVar2;
            if (*piVar2 != iVar9) {
              piVar2 = piVar2 + 1;
              goto LAB_002cce28;
            }
          }
          else {
            __dest = piVar11;
            if (iVar5 == 1) {
              iVar9 = *piVar3;
              goto LAB_002cce04;
            }
          }
joined_r0x002ccdb0:
          if (__dest == piVar11) {
            iVar9 = *piVar3;
            _ZN23ObjManager_BinarySearch15AddObjectToListEP11CGameObjectb
                      (*(undefined4 *)(iVar7 + 0x138),iVar9,0);
            _ZN11ObjManagers16AddObjectToListsEP11CGameObjectt
                      (*(undefined4 *)(iVar7 + 0x134),iVar9,*(undefined2 *)(iVar9 + 0x104));
            piVar11 = *(int **)(iVar7 + 0x14c);
            piVar13 = *(int **)(iVar7 + 0x140);
            piVar10 = *(int **)(iVar7 + 0x148);
          }
          else {
            piVar3 = __dest + 1;
            if ((piVar3 != piVar11) && (iVar9 = (int)piVar11 - (int)piVar3 >> 2, iVar9 != 0)) {
              memmove(__dest,piVar3,iVar9 << 2);
              piVar11 = *(int **)(iVar7 + 0x14c);
              piVar13 = *(int **)(iVar7 + 0x140);
              piVar10 = *(int **)(iVar7 + 0x148);
            }
            piVar11 = piVar11 + -1;
            *(int **)(iVar7 + 0x14c) = piVar11;
          }
          piVar3 = piVar8;
        } while (piVar13 != piVar8);
      }
      *(undefined4 *)(iVar7 + 0x140) = *(undefined4 *)(iVar7 + 0x13c);
      for (; piVar10 != piVar11; piVar10 = piVar10 + 1) {
        iVar9 = *piVar10;
        _ZN23ObjManager_BinarySearch20RemoveObjectFromListEP11CGameObject
                  (*(undefined4 *)(iVar7 + 0x138),iVar9);
        _ZN11ObjManagers21RemoveObjectFromListsEP11CGameObject(*(undefined4 *)(iVar7 + 0x134),iVar9)
        ;
        piVar11 = *(int **)(iVar7 + 0x14c);
      }
      *(undefined4 *)(iVar7 + 0x14c) = *(undefined4 *)(iVar7 + 0x148);
      piVar3 = piVar4;
    } while (*(int **)(param_1 + 0x84) != piVar4);
  }
  return;
}


