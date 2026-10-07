// _ZN13CAIController17GetEnemiesInRangeEPSt6vectorIP11CGameObjectSaIS2_EEiffi @ 00188c9c

void _ZN13CAIController17GetEnemiesInRangeEPSt6vectorIP11CGameObjectSaIS2_EEiffi
               (int param_1,undefined4 *param_2,undefined4 param_3,float param_4,float param_5,
               int param_6)

{
  undefined8 uVar1;
  undefined4 uVar2;
  int *piVar3;
  undefined8 *puVar4;
  int iVar5;
  float *pfVar6;
  int *piVar7;
  int *piVar8;
  int iVar9;
  int *piVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  
  param_2[1] = *param_2;
  uVar2 = _ZN6CLevel8GetLevelEv();
  piVar3 = (int *)_ZN6CLevel20FindObjectOrWaypointEi(uVar2,param_3);
  if (piVar3 != (int *)0x0) {
    puVar4 = (undefined8 *)(**(code **)(*piVar3 + 0xc))();
    uVar1 = *puVar4;
    fVar14 = *(float *)(puVar4 + 1);
    for (iVar9 = *(int *)(param_1 + 0xb8); param_1 + 0xb0 != iVar9;
        iVar9 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar9)) {
      iVar5 = (**(code **)(**(int **)(iVar9 + 0x10) + 0x54))();
      if (iVar5 != 0) {
        pfVar6 = (float *)(**(code **)(**(int **)(iVar9 + 0x10) + 0x18))();
        fVar15 = (float)uVar1;
        fVar11 = *pfVar6 - fVar15;
        fVar16 = (float)((ulonglong)uVar1 >> 0x20);
        fVar12 = pfVar6[1] - fVar16;
        fVar11 = fVar11 * fVar11 + fVar12 * fVar12 + (pfVar6[2] - fVar14) * (pfVar6[2] - fVar14);
        if (((fVar11 < param_4 * param_4) &&
            (iVar5 = (**(code **)(**(int **)(iVar9 + 0x10) + 0x18))(),
            ABS(*(float *)(iVar5 + 8) - fVar14) <= param_5)) &&
           ((param_6 == -1 ||
            (iVar5 = _ZN11CGameObject13GetAIBehaviorEv(*(undefined4 *)(iVar9 + 0x10)),
            iVar5 == param_6)))) {
          piVar7 = (int *)param_2[1];
          piVar3 = (int *)*param_2;
          if ((uint)((int)piVar7 - (int)*param_2) >> 2 == 0) {
            if (piVar7 != (int *)param_2[2]) goto LAB_00188e58;
            _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                      (param_2,piVar7,iVar9 + 0x10);
          }
          else {
            do {
              do {
                piVar10 = piVar3;
                if (piVar7 == piVar10) goto LAB_00188e1c;
                piVar8 = (int *)*piVar10;
                piVar3 = piVar10 + 1;
              } while (piVar8 == (int *)0x0);
              pfVar6 = (float *)(**(code **)(*piVar8 + 0x18))(piVar8);
              piVar7 = (int *)param_2[1];
              fVar13 = *pfVar6 - fVar15;
              fVar12 = pfVar6[1] - fVar16;
            } while (fVar13 * fVar13 + fVar12 * fVar12 + (pfVar6[2] - fVar14) * (pfVar6[2] - fVar14)
                     <= fVar11);
LAB_00188e1c:
            if ((piVar7 == (int *)param_2[2]) || (piVar7 != piVar10)) {
              _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                        (param_2,piVar10,iVar9 + 0x10);
            }
            else {
LAB_00188e58:
              iVar5 = 0;
              if (piVar7 != (int *)0x0) {
                *piVar7 = *(int *)(iVar9 + 0x10);
                iVar5 = param_2[1];
              }
              param_2[1] = iVar5 + 4;
            }
          }
        }
      }
    }
  }
  return;
}

