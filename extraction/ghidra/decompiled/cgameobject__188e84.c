// _ZN13CAIController17GetEnemiesInRangeEPSt6vectorIP11CGameObjectSaIS2_EEifi @ 00188e84

void _ZN13CAIController17GetEnemiesInRangeEPSt6vectorIP11CGameObjectSaIS2_EEifi
               (int param_1,undefined4 *param_2,undefined4 param_3,float param_4,int param_5)

{
  undefined8 uVar1;
  undefined4 uVar2;
  int *piVar3;
  float *pfVar4;
  int iVar5;
  undefined4 *puVar6;
  int iVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  
  param_2[1] = *param_2;
  uVar2 = _ZN6CLevel8GetLevelEv();
  piVar3 = (int *)_ZN6CLevel20FindObjectOrWaypointEi(uVar2,param_3);
  if (piVar3 != (int *)0x0) {
    pfVar4 = (float *)(**(code **)(*piVar3 + 0xc))();
    fVar10 = *pfVar4;
    uVar1 = *(undefined8 *)(pfVar4 + 1);
    for (iVar7 = *(int *)(param_1 + 0xb8); param_1 + 0xb0 != iVar7;
        iVar7 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar7)) {
      iVar5 = (**(code **)(**(int **)(iVar7 + 0x10) + 0x54))();
      if ((iVar5 != 0) &&
         ((param_5 == -1 ||
          (iVar5 = _ZN11CGameObject13GetAIBehaviorEv(*(undefined4 *)(iVar7 + 0x10)),
          iVar5 == param_5)))) {
        pfVar4 = (float *)(**(code **)(**(int **)(iVar7 + 0x10) + 0x18))();
        fVar8 = pfVar4[1] - (float)uVar1;
        fVar9 = pfVar4[2] - (float)((ulonglong)uVar1 >> 0x20);
        if ((*pfVar4 - fVar10) * (*pfVar4 - fVar10) + fVar8 * fVar8 + fVar9 * fVar9 <
            param_4 * param_4) {
          puVar6 = (undefined4 *)param_2[1];
          if (puVar6 == (undefined4 *)param_2[2]) {
            _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                      (param_2,puVar6,iVar7 + 0x10);
          }
          else {
            iVar5 = 0;
            if (puVar6 != (undefined4 *)0x0) {
              *puVar6 = *(undefined4 *)(iVar7 + 0x10);
              iVar5 = param_2[1];
            }
            param_2[1] = iVar5 + 4;
          }
        }
      }
    }
  }
  return;
}

