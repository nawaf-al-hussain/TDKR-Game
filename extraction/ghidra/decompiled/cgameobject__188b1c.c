// _ZN13CAIController16Alliance_ClosestEPP11CGameObject11AI_ALLIANCES1_ @ 00188b1c

void _ZN13CAIController16Alliance_ClosestEPP11CGameObject11AI_ALLIANCES1_
               (int param_1,int *param_2,uint param_3,int *param_4)

{
  float *pfVar1;
  int *piVar2;
  int iVar3;
  bool bVar4;
  float fVar5;
  float unaff_s16;
  float fVar6;
  float fVar7;
  float fVar8;
  
  *param_2 = 0;
  pfVar1 = (float *)(**(code **)(*param_4 + 0x18))(param_4);
  bVar4 = (param_3 & 1) != 0;
  if (bVar4) {
    param_1 = param_1 + 0xdc;
  }
  fVar8 = *pfVar1;
  fVar7 = pfVar1[1];
  fVar6 = pfVar1[2];
  if (!bVar4) {
    if ((param_3 & 2) == 0) {
      return;
    }
    param_1 = param_1 + 0xac;
  }
  if (param_1 != 0) {
    for (iVar3 = *(int *)(param_1 + 0xc); param_1 + 4 != iVar3;
        iVar3 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar3)) {
      piVar2 = *(int **)(iVar3 + 0x10);
      if (param_4 != piVar2) {
        pfVar1 = (float *)(**(code **)(*piVar2 + 0x18))(piVar2);
        fVar5 = (fVar8 - *pfVar1) * (fVar8 - *pfVar1) + (fVar7 - pfVar1[1]) * (fVar7 - pfVar1[1]) +
                (fVar6 - pfVar1[2]) * (fVar6 - pfVar1[2]);
        if ((*param_2 == 0) || (fVar5 < unaff_s16)) {
          *param_2 = *(int *)(iVar3 + 0x10);
          unaff_s16 = fVar5;
        }
      }
    }
  }
  return;
}

