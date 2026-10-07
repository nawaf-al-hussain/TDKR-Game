// _ZN13CAIController16Alliance_InRangeEPSt6vectorIP11CGameObjectSaIS2_EE11AI_ALLIANCES2_f @ 001888f4

void _ZN13CAIController16Alliance_InRangeEPSt6vectorIP11CGameObjectSaIS2_EE11AI_ALLIANCES2_f
               (int param_1,undefined4 *param_2,uint param_3,int *param_4,float param_5)

{
  float *pfVar1;
  int iVar2;
  undefined4 *puVar3;
  int iVar4;
  bool bVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  
  iVar4 = *param_4;
  param_2[1] = *param_2;
  pfVar1 = (float *)(**(code **)(iVar4 + 0x18))(param_4);
  bVar5 = (param_3 & 1) != 0;
  if (bVar5) {
    param_1 = param_1 + 0xdc;
  }
  fVar8 = *pfVar1;
  fVar7 = pfVar1[1];
  fVar6 = pfVar1[2];
  if (!bVar5) {
    if ((param_3 & 2) == 0) {
      return;
    }
    param_1 = param_1 + 0xac;
  }
  if (param_1 != 0) {
    for (iVar4 = *(int *)(param_1 + 0xc); param_1 + 4 != iVar4;
        iVar4 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar4)) {
      iVar2 = (**(code **)(**(int **)(iVar4 + 0x10) + 0x54))();
      if (((iVar2 != 0) && (param_4 != *(int **)(iVar4 + 0x10))) &&
         (pfVar1 = (float *)(**(code **)(**(int **)(iVar4 + 0x10) + 0x18))(),
         (fVar8 - *pfVar1) * (fVar8 - *pfVar1) + (fVar7 - pfVar1[1]) * (fVar7 - pfVar1[1]) +
         (fVar6 - pfVar1[2]) * (fVar6 - pfVar1[2]) < param_5 * param_5)) {
        puVar3 = (undefined4 *)param_2[1];
        if (puVar3 == (undefined4 *)param_2[2]) {
          _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                    (param_2,puVar3,iVar4 + 0x10);
        }
        else {
          iVar2 = 0;
          if (puVar3 != (undefined4 *)0x0) {
            *puVar3 = *(undefined4 *)(iVar4 + 0x10);
            iVar2 = param_2[1];
          }
          param_2[1] = iVar2 + 4;
        }
      }
    }
  }
  return;
}

