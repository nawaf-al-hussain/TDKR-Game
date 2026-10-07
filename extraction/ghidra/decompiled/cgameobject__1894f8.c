// _ZN13CAIController22GetAwareEnemiesInRangeEPSt6vectorIP11CGameObjectSaIS2_EEifib @ 001894f8

void _ZN13CAIController22GetAwareEnemiesInRangeEPSt6vectorIP11CGameObjectSaIS2_EEifib
               (int param_1,undefined4 *param_2,undefined4 param_3,float param_4,int param_5,
               char param_6)

{
  undefined8 uVar1;
  undefined4 uVar2;
  int *piVar3;
  float *pfVar4;
  int iVar5;
  int *piVar6;
  int iVar7;
  int *piVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  
  param_2[1] = *param_2;
  uVar2 = _ZN6CLevel8GetLevelEv();
  piVar3 = (int *)_ZN6CLevel20FindObjectOrWaypointEi(uVar2,param_3);
  pfVar4 = (float *)(**(code **)(*piVar3 + 0xc))();
  iVar7 = *(int *)(param_1 + 0x100);
  fVar13 = *pfVar4;
  uVar1 = *(undefined8 *)(pfVar4 + 1);
  do {
    if (param_1 + 0xf8 == iVar7) {
      return;
    }
    if (((((param_6 == '\0') || (*(int *)((*(int **)(iVar7 + 0x10))[0x2b] + 0x18) == 3)) &&
         (iVar5 = (**(code **)(**(int **)(iVar7 + 0x10) + 0x54))(), iVar5 != 0)) &&
        ((param_5 == -1 ||
         (iVar5 = _ZN11CGameObject13GetAIBehaviorEv(*(undefined4 *)(iVar7 + 0x10)), iVar5 == param_5
         )))) && (iVar5 = _ZN11CGameObject13GetAIBehaviorEv(*(undefined4 *)(iVar7 + 0x10)),
                 *(char *)(*(int *)(*(int *)(param_1 + 0x6c) + 4) + iVar5 * 0xc + 8) != '\0')) {
      pfVar4 = (float *)(**(code **)(**(int **)(iVar7 + 0x10) + 0x18))();
      if (*(int *)(iVar7 + 0x10) != 0) {
        fVar9 = *pfVar4 - fVar13;
        fVar14 = (float)uVar1;
        fVar10 = pfVar4[1] - fVar14;
        fVar15 = (float)((ulonglong)uVar1 >> 0x20);
        fVar11 = pfVar4[2] - fVar15;
        fVar9 = fVar9 * fVar9 + fVar10 * fVar10 + fVar11 * fVar11;
        if (fVar9 < param_4 * param_4) {
          piVar6 = (int *)param_2[1];
          piVar3 = (int *)*param_2;
          if ((uint)((int)piVar6 - (int)*param_2) >> 2 == 0) {
            if (piVar6 == (int *)param_2[2]) {
              _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                        (param_2,piVar6,iVar7 + 0x10);
            }
            else {
              iVar5 = 0;
              if (piVar6 != (int *)0x0) {
                *piVar6 = *(int *)(iVar7 + 0x10);
                iVar5 = param_2[1];
              }
              param_2[1] = iVar5 + 4;
            }
          }
          else {
            do {
              piVar8 = piVar3;
              if (piVar8 == piVar6) break;
              pfVar4 = (float *)(**(code **)(*(int *)*piVar8 + 0x18))();
              piVar6 = (int *)param_2[1];
              fVar12 = *pfVar4 - fVar13;
              fVar10 = pfVar4[1] - fVar14;
              fVar11 = pfVar4[2] - fVar15;
              piVar3 = piVar8 + 1;
            } while (fVar12 * fVar12 + fVar10 * fVar10 + fVar11 * fVar11 <= fVar9);
            if (((int *)param_2[2] == piVar6) || (piVar8 != piVar6)) {
              _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                        (param_2,piVar8,iVar7 + 0x10);
            }
            else {
              iVar5 = 0;
              if (piVar8 != (int *)0x0) {
                *piVar8 = *(int *)(iVar7 + 0x10);
                iVar5 = param_2[1];
              }
              param_2[1] = iVar5 + 4;
            }
          }
        }
      }
    }
    iVar7 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar7);
  } while( true );
}

