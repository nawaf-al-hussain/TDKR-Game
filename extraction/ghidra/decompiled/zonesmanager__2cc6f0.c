// _ZN13CZonesManagerD1Ev @ 002cc6f0

int * _ZN13CZonesManagerD1Ev(int *param_1)

{
  int *piVar1;
  bool bVar2;
  int *__dest;
  int *piVar3;
  int *piVar4;
  int iVar5;
  int *piVar6;
  undefined4 *puVar7;
  int iVar8;
  int *piVar9;
  int *piVar10;
  undefined4 *puVar11;
  undefined4 *puVar12;
  int iVar13;
  int *piVar14;
  int *piVar15;
  int *piVar16;
  int *piVar17;
  
  piVar4 = (int *)param_1[0x20];
  if ((int *)param_1[0x20] != (int *)param_1[0x21]) {
    do {
      piVar9 = piVar4 + 1;
      iVar8 = *piVar4;
      piVar17 = *(int **)(iVar8 + 0x140);
      piVar15 = *(int **)(iVar8 + 0x14c);
      piVar14 = *(int **)(iVar8 + 0x148);
      piVar4 = *(int **)(iVar8 + 0x13c);
      if (piVar17 != *(int **)(iVar8 + 0x13c)) {
        do {
          piVar10 = piVar4 + 1;
          iVar5 = (int)piVar15 - (int)piVar14;
          iVar13 = iVar5 >> 4;
          piVar3 = piVar14;
          if (0 < iVar13) {
            iVar5 = *piVar4;
            __dest = piVar14;
            if (*piVar14 != iVar5) {
              if (iVar5 == piVar14[1]) {
                __dest = piVar14 + 1;
              }
              else if (iVar5 == piVar14[2]) {
                __dest = piVar14 + 2;
              }
              else {
                piVar6 = piVar14;
                if (iVar5 == piVar14[3]) {
                  __dest = piVar14 + 3;
                }
                else {
                  do {
                    iVar13 = iVar13 + -1;
                    piVar3 = piVar6 + 4;
                    if (iVar13 == 0) {
                      iVar5 = (int)piVar15 - (int)piVar3;
                      goto LAB_002cc7f4;
                    }
                    piVar16 = piVar6 + 7;
                    __dest = piVar3;
                  } while ((((iVar5 != piVar6[4]) && (__dest = piVar6 + 5, iVar5 != piVar6[5])) &&
                           (__dest = piVar6 + 6, iVar5 != piVar6[6])) &&
                          (piVar1 = piVar6 + 7, piVar6 = piVar3, __dest = piVar16, iVar5 != *piVar1)
                          );
                }
              }
            }
            goto joined_r0x002ccad4;
          }
LAB_002cc7f4:
          iVar5 = iVar5 >> 2;
          if (iVar5 == 2) {
            iVar13 = *piVar4;
LAB_002ccb4c:
            __dest = piVar3;
            if (*piVar3 != iVar13) {
              piVar3 = piVar3 + 1;
LAB_002ccb28:
              __dest = piVar3;
              if (*piVar3 != iVar13) {
                __dest = piVar15;
              }
            }
          }
          else if (iVar5 == 3) {
            iVar13 = *piVar4;
            __dest = piVar3;
            if (*piVar3 != iVar13) {
              piVar3 = piVar3 + 1;
              goto LAB_002ccb4c;
            }
          }
          else {
            __dest = piVar15;
            if (iVar5 == 1) {
              iVar13 = *piVar4;
              goto LAB_002ccb28;
            }
          }
joined_r0x002ccad4:
          if (__dest == piVar15) {
            iVar13 = *piVar4;
            _ZN23ObjManager_BinarySearch15AddObjectToListEP11CGameObjectb
                      (*(undefined4 *)(iVar8 + 0x138),iVar13,0);
            _ZN11ObjManagers16AddObjectToListsEP11CGameObjectt
                      (*(undefined4 *)(iVar8 + 0x134),iVar13,*(undefined2 *)(iVar13 + 0x104));
            piVar15 = *(int **)(iVar8 + 0x14c);
            piVar17 = *(int **)(iVar8 + 0x140);
            piVar14 = *(int **)(iVar8 + 0x148);
          }
          else {
            piVar4 = __dest + 1;
            if ((piVar4 != piVar15) && (iVar13 = (int)piVar15 - (int)piVar4 >> 2, iVar13 != 0)) {
              memmove(__dest,piVar4,iVar13 << 2);
              piVar15 = *(int **)(iVar8 + 0x14c);
              piVar17 = *(int **)(iVar8 + 0x140);
              piVar14 = *(int **)(iVar8 + 0x148);
            }
            piVar15 = piVar15 + -1;
            *(int **)(iVar8 + 0x14c) = piVar15;
          }
          piVar4 = piVar10;
        } while (piVar17 != piVar10);
      }
      *(undefined4 *)(iVar8 + 0x140) = *(undefined4 *)(iVar8 + 0x13c);
      for (; piVar14 != piVar15; piVar14 = piVar14 + 1) {
        iVar13 = *piVar14;
        _ZN23ObjManager_BinarySearch20RemoveObjectFromListEP11CGameObject
                  (*(undefined4 *)(iVar8 + 0x138),iVar13);
        _ZN11ObjManagers21RemoveObjectFromListsEP11CGameObject
                  (*(undefined4 *)(iVar8 + 0x134),iVar13);
        piVar15 = *(int **)(iVar8 + 0x14c);
      }
      *(undefined4 *)(iVar8 + 0x14c) = *(undefined4 *)(iVar8 + 0x148);
      piVar4 = piVar9;
    } while (piVar9 != (int *)param_1[0x21]);
  }
  _ZN13CZonesManager19CleanContactHistoryEv(param_1);
  iVar8 = param_1[0x1a];
  if (iVar8 != 0) {
    _ZN22GameObjectCacheManagerD1Ev(iVar8);
    _ZdlPv(iVar8);
    param_1[0x1a] = 0;
  }
  piVar4 = (int *)param_1[0x21];
  piVar9 = (int *)param_1[0x20];
  while (piVar14 = piVar9, piVar9 != piVar4) {
    while( true ) {
      piVar9 = piVar14 + 1;
      piVar15 = (int *)*piVar14;
      if (piVar15 == (int *)0x0) break;
      (**(code **)(*piVar15 + 4))(piVar15);
      *piVar14 = 0;
      piVar4 = (int *)param_1[0x21];
      piVar14 = piVar9;
      if (piVar9 == piVar4) goto LAB_002cc900;
    }
  }
LAB_002cc900:
  piVar4 = *(int **)(DAT_002ccba4 + 0x2cc914);
  param_1[0x21] = param_1[0x20];
  param_1[0x16] = param_1[0x15];
  if (piVar4 != (int *)0x0) {
    puVar7 = (undefined4 *)piVar4[1];
    puVar11 = (undefined4 *)*piVar4;
    while (puVar12 = puVar11, puVar11 != puVar7) {
      while( true ) {
        puVar11 = puVar12 + 1;
        piVar9 = (int *)*puVar12;
        if (piVar9 == (int *)0x0) break;
        piVar14 = (int *)*piVar9;
        if (piVar14 != (int *)0x0) {
          (**(code **)(*piVar14 + 4))(piVar14);
          *piVar9 = 0;
        }
        _ZdlPv(piVar9);
        puVar7 = (undefined4 *)piVar4[1];
        puVar12 = puVar11;
        if (puVar11 == puVar7) goto LAB_002cc974;
      }
    }
LAB_002cc974:
    if (*piVar4 != 0) {
      _ZdlPv();
    }
    _ZdlPv(piVar4);
    *(undefined4 *)(DAT_002ccba8 + 0x2cc99c) = 0;
  }
  iVar8 = param_1[0x19];
  if (iVar8 != 0) {
    _ZN21SceneNodeCacheManagerD1Ev(iVar8);
    _ZdlPv(iVar8);
    param_1[0x19] = 0;
  }
  iVar8 = param_1[0x23];
  *(undefined4 *)(DAT_002ccbac + 0x2cc9d4) = 0;
  if (iVar8 != 0) {
    _ZdlPv();
  }
  if (param_1[0x20] != 0) {
    _ZdlPv();
  }
  if (param_1[0x15] != 0) {
    _ZdlPv();
  }
  if (param_1[0x10] != 0) {
    _ZdlPv();
  }
  if (param_1[0xd] != 0) {
    _ZdlPv();
  }
  _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE8_M_eraseEPSt13_Rb_tree_nodeIS4_E
            (param_1 + 7,param_1[9]);
  piVar4 = (int *)param_1[3];
  piVar9 = (int *)param_1[4];
  if (piVar4 != piVar9) {
    iVar8 = *(int *)(DAT_002ccbb0 + 0x2cca50);
    do {
      piVar14 = piVar4 + 1;
      if (*piVar4 + -0xc != iVar8) {
        piVar4 = (int *)(*piVar4 + -4);
        DataMemoryBarrier(0xf);
        do {
          iVar13 = *piVar4;
          bVar2 = (bool)hasExclusiveAccess(piVar4);
        } while (!bVar2);
        *piVar4 = iVar13 + -1;
        DataMemoryBarrier(0xf);
        if (iVar13 < 1) {
          _Z10GlitchFreePv();
        }
      }
      piVar4 = piVar14;
    } while (piVar9 != piVar14);
    piVar4 = (int *)param_1[3];
  }
  if (piVar4 != (int *)0x0) {
    _ZdlPv();
  }
  iVar8 = *param_1;
  iVar13 = param_1[1];
  if (iVar8 != iVar13) {
    do {
      iVar5 = iVar8 + 4;
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar8);
      iVar8 = iVar5;
    } while (iVar13 != iVar5);
    iVar8 = *param_1;
  }
  if (iVar8 != 0) {
    _ZdlPv(iVar8);
  }
  return param_1;
}


