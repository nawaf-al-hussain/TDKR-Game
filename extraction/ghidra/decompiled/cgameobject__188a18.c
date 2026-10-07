// _ZN13CAIController16Alliance_InRangeEPSt6vectorIP11CGameObjectSaIS2_EE11AI_ALLIANCERKN6glitch4core8vector3dIfEEf @ 00188a18

void _ZN13CAIController16Alliance_InRangeEPSt6vectorIP11CGameObjectSaIS2_EE11AI_ALLIANCERKN6glitch4core8vector3dIfEEf
               (int param_1,undefined4 *param_2,uint param_3,float *param_4,float param_5)

{
  int iVar1;
  float *pfVar2;
  undefined4 *puVar3;
  int iVar4;
  int unaff_r6;
  bool bVar5;
  
  bVar5 = (param_3 & 1) != 0;
  if (bVar5) {
    unaff_r6 = param_1 + 0xdc;
  }
  param_2[1] = *param_2;
  if (!bVar5) {
    if ((param_3 & 2) == 0) {
      return;
    }
    unaff_r6 = param_1 + 0xac;
  }
  if (unaff_r6 != 0) {
    for (iVar4 = *(int *)(unaff_r6 + 0xc); unaff_r6 + 4 != iVar4;
        iVar4 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar4)) {
      iVar1 = (**(code **)(**(int **)(iVar4 + 0x10) + 0x54))();
      if ((iVar1 != 0) &&
         (pfVar2 = (float *)(**(code **)(**(int **)(iVar4 + 0x10) + 0x18))(),
         (*param_4 - *pfVar2) * (*param_4 - *pfVar2) +
         (param_4[1] - pfVar2[1]) * (param_4[1] - pfVar2[1]) +
         (param_4[2] - pfVar2[2]) * (param_4[2] - pfVar2[2]) < param_5 * param_5)) {
        puVar3 = (undefined4 *)param_2[1];
        if (puVar3 == (undefined4 *)param_2[2]) {
          _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                    (param_2,puVar3,iVar4 + 0x10);
        }
        else {
          iVar1 = 0;
          if (puVar3 != (undefined4 *)0x0) {
            *puVar3 = *(undefined4 *)(iVar4 + 0x10);
            iVar1 = param_2[1];
          }
          param_2[1] = iVar1 + 4;
        }
      }
    }
  }
  return;
}

