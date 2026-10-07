// _ZN13CZonesManager8SaveSaveEP13CMemoryStream @ 002d16dc

void _ZN13CZonesManager8SaveSaveEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int *piVar1;
  int *__dest;
  int *piVar2;
  int *piVar3;
  undefined4 extraout_r1;
  undefined4 uVar4;
  int iVar5;
  int *piVar6;
  int iVar7;
  undefined4 *puVar8;
  int *piVar9;
  int iVar10;
  int *piVar11;
  int *piVar12;
  int *piVar13;
  int *piVar14;
  int *piVar15;
  
  piVar3 = *(int **)(param_1 + 0x80);
  if (*(int **)(param_1 + 0x80) != *(int **)(param_1 + 0x84)) {
    do {
      piVar11 = piVar3 + 1;
      iVar7 = *piVar3;
      piVar15 = *(int **)(iVar7 + 0x140);
      piVar13 = *(int **)(iVar7 + 0x14c);
      piVar12 = *(int **)(iVar7 + 0x148);
      piVar3 = *(int **)(iVar7 + 0x13c);
      if (piVar15 != *(int **)(iVar7 + 0x13c)) {
        do {
          piVar9 = piVar3 + 1;
          iVar5 = (int)piVar13 - (int)piVar12;
          iVar10 = iVar5 >> 4;
          piVar2 = piVar12;
          if (0 < iVar10) {
            iVar5 = *piVar3;
            __dest = piVar12;
            if (*piVar12 != iVar5) {
              if (iVar5 == piVar12[1]) {
                __dest = piVar12 + 1;
              }
              else if (iVar5 == piVar12[2]) {
                __dest = piVar12 + 2;
              }
              else {
                piVar6 = piVar12;
                if (iVar5 == piVar12[3]) {
                  __dest = piVar12 + 3;
                }
                else {
                  do {
                    iVar10 = iVar10 + -1;
                    piVar2 = piVar6 + 4;
                    if (iVar10 == 0) {
                      iVar5 = (int)piVar13 - (int)piVar2;
                      goto LAB_002d17dc;
                    }
                    piVar14 = piVar6 + 7;
                    __dest = piVar2;
                  } while ((((piVar6[4] != iVar5) && (__dest = piVar6 + 5, piVar6[5] != iVar5)) &&
                           (__dest = piVar6 + 6, piVar6[6] != iVar5)) &&
                          (piVar1 = piVar6 + 7, piVar6 = piVar2, __dest = piVar14, *piVar1 != iVar5)
                          );
                }
              }
            }
            goto joined_r0x002d199c;
          }
LAB_002d17dc:
          iVar5 = iVar5 >> 2;
          if (iVar5 == 2) {
            iVar10 = *piVar3;
LAB_002d1a14:
            __dest = piVar2;
            if (*piVar2 != iVar10) {
              piVar2 = piVar2 + 1;
LAB_002d19f0:
              __dest = piVar2;
              if (*piVar2 != iVar10) {
                __dest = piVar13;
              }
            }
          }
          else if (iVar5 == 3) {
            iVar10 = *piVar3;
            __dest = piVar2;
            if (*piVar2 != iVar10) {
              piVar2 = piVar2 + 1;
              goto LAB_002d1a14;
            }
          }
          else {
            __dest = piVar13;
            if (iVar5 == 1) {
              iVar10 = *piVar3;
              goto LAB_002d19f0;
            }
          }
joined_r0x002d199c:
          if (__dest == piVar13) {
            iVar10 = *piVar3;
            _ZN23ObjManager_BinarySearch15AddObjectToListEP11CGameObjectb
                      (*(undefined4 *)(iVar7 + 0x138),iVar10,0);
            _ZN11ObjManagers16AddObjectToListsEP11CGameObjectt
                      (*(undefined4 *)(iVar7 + 0x134),iVar10,*(undefined2 *)(iVar10 + 0x104));
            piVar13 = *(int **)(iVar7 + 0x14c);
            piVar15 = *(int **)(iVar7 + 0x140);
            piVar12 = *(int **)(iVar7 + 0x148);
          }
          else {
            piVar3 = __dest + 1;
            if ((piVar3 != piVar13) && (iVar10 = (int)piVar13 - (int)piVar3 >> 2, iVar10 != 0)) {
              memmove(__dest,piVar3,iVar10 << 2);
              piVar13 = *(int **)(iVar7 + 0x14c);
              piVar15 = *(int **)(iVar7 + 0x140);
              piVar12 = *(int **)(iVar7 + 0x148);
            }
            piVar13 = piVar13 + -1;
            *(int **)(iVar7 + 0x14c) = piVar13;
          }
          piVar3 = piVar9;
        } while (piVar15 != piVar9);
      }
      *(undefined4 *)(iVar7 + 0x140) = *(undefined4 *)(iVar7 + 0x13c);
      for (; piVar12 != piVar13; piVar12 = piVar12 + 1) {
        iVar10 = *piVar12;
        _ZN23ObjManager_BinarySearch20RemoveObjectFromListEP11CGameObject
                  (*(undefined4 *)(iVar7 + 0x138),iVar10);
        _ZN11ObjManagers21RemoveObjectFromListsEP11CGameObject
                  (*(undefined4 *)(iVar7 + 0x134),iVar10);
        piVar13 = *(int **)(iVar7 + 0x14c);
      }
      *(undefined4 *)(iVar7 + 0x14c) = *(undefined4 *)(iVar7 + 0x148);
      piVar3 = piVar11;
    } while (piVar11 != *(int **)(param_1 + 0x84));
  }
  _ZN13CMemoryStream5WriteEi(param_2,*(undefined4 *)(param_1 + 0x4c));
  piVar3 = *(int **)(param_1 + 0x6c);
  if (piVar3 == (int *)0x0) {
    uVar4 = 0xffffffff;
  }
  else {
    uVar4 = (**(code **)(*piVar3 + 0x14))(piVar3,extraout_r1);
  }
  _ZN13CMemoryStream5WriteEi(param_2,uVar4);
  _ZN13CMemoryStream5WriteEt
            (param_2,(*(int *)(param_1 + 0x84) - *(int *)(param_1 + 0x80) & 0x3ffffU) >> 2);
  for (puVar8 = *(undefined4 **)(param_1 + 0x80); *(undefined4 **)(param_1 + 0x84) != puVar8;
      puVar8 = puVar8 + 1) {
    uVar4 = (**(code **)(*(int *)*puVar8 + 0x14))();
    _ZN13CMemoryStream8WriteIntEi(param_2,uVar4);
    _ZN13CMemoryStream18WriteBlockStartIntEv(param_2);
    (**(code **)(*(int *)*puVar8 + 0x90))((int *)*puVar8,param_2);
    _ZN13CMemoryStream16WriteBlockEndIntEv(param_2);
  }
  piVar11 = *(int **)(DAT_002d1a38 + 0x2d1940);
  _ZN13CMemoryStream5WriteEt(param_2,(piVar11[1] - *piVar11 & 0x3ffffU) >> 2);
  for (piVar3 = (int *)*piVar11; piVar3 != (int *)piVar11[1]; piVar3 = piVar3 + 1) {
    _ZN13CMemoryStream5WriteEb(param_2,*(undefined1 *)(*piVar3 + 8));
  }
  return;
}


