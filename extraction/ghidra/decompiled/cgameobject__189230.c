// _ZN13CAIController33GetAwareActiveEnemiesInRangeStatsEP11CGameObjectfRN6glitch4core8vector3dIfEES6_S6_RfS7_ @ 00189230

uint _ZN13CAIController33GetAwareActiveEnemiesInRangeStatsEP11CGameObjectfRN6glitch4core8vector3dIfEES6_S6_RfS7_
               (int param_1,int *param_2,float param_3,float *param_4,float *param_5,float *param_6,
               float *param_7,float *param_8)

{
  uint uVar1;
  float *pfVar2;
  int iVar3;
  int *piVar4;
  float *pfVar5;
  int iVar6;
  int *piVar7;
  uint uVar8;
  bool bVar9;
  uint in_fpscr;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  
  pfVar2 = (float *)(**(code **)(*param_2 + 0x18))(param_2);
  fVar18 = *pfVar2;
  fVar17 = pfVar2[1];
  fVar16 = pfVar2[2];
  *param_4 = 0.0;
  param_4[1] = 0.0;
  param_4[2] = 0.0;
  iVar3 = _ZNK11CGameObject14GetMeleeTargetEv(param_2);
  if (iVar3 == 0) {
    fVar14 = 0.0;
    fVar15 = param_3 * param_3;
  }
  else {
    piVar4 = (int *)_ZNK11CGameObject14GetMeleeTargetEv(param_2);
    pfVar2 = (float *)(**(code **)(*piVar4 + 0x18))();
    pfVar5 = (float *)(**(code **)(*param_2 + 0x18))(param_2);
    fVar14 = (*pfVar2 - *pfVar5) * (*pfVar2 - *pfVar5) +
             (pfVar2[1] - pfVar5[1]) * (pfVar2[1] - pfVar5[1]) +
             (pfVar2[2] - pfVar5[2]) * (pfVar2[2] - pfVar5[2]);
    piVar4 = (int *)_ZNK11CGameObject14GetMeleeTargetEv(param_2);
    pfVar2 = (float *)(**(code **)(*piVar4 + 0x18))();
    *param_5 = *pfVar2;
    param_5[1] = pfVar2[1];
    param_5[2] = pfVar2[2];
    piVar4 = (int *)_ZNK11CGameObject14GetMeleeTargetEv(param_2);
    pfVar2 = (float *)(**(code **)(*piVar4 + 0x18))();
    *param_6 = *pfVar2;
    param_6[1] = pfVar2[1];
    param_6[2] = pfVar2[2];
    piVar4 = (int *)_ZNK11CGameObject14GetMeleeTargetEv(param_2);
    pfVar2 = (float *)(**(code **)(*piVar4 + 0x18))();
    *param_4 = *param_4 + *pfVar2;
    param_4[1] = param_4[1] + pfVar2[1];
    param_4[2] = param_4[2] + pfVar2[2];
    fVar15 = fVar14;
  }
  uVar8 = (uint)(iVar3 != 0);
  for (iVar3 = *(int *)(param_1 + 0x100); param_1 + 0xf8 != iVar3;
      iVar3 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar3)) {
    piVar7 = *(int **)(iVar3 + 0x10);
    piVar4 = (int *)_ZNK11CGameObject14GetMeleeTargetEv(param_2);
    if (((piVar7 != piVar4) && (iVar6 = (**(code **)(*piVar7 + 0x54))(piVar7), iVar6 != 0)) &&
       (*(int *)(piVar7[0x2b] + 0x18) == 3)) {
      pfVar2 = (float *)(**(code **)(*piVar7 + 0x18))(piVar7);
      fVar12 = *pfVar2;
      fVar11 = pfVar2[1];
      fVar10 = pfVar2[2];
      fVar13 = (fVar18 - fVar12) * (fVar18 - fVar12) + (fVar17 - fVar11) * (fVar17 - fVar11) +
               (fVar16 - fVar10) * (fVar16 - fVar10);
      uVar1 = in_fpscr & 0xfffffff;
      in_fpscr = uVar1 | (uint)(param_3 * param_3 < fVar13) << 0x1f;
      if (!SUB41(in_fpscr >> 0x1f,0)) {
        uVar8 = uVar8 + 1;
        in_fpscr = uVar1 | (uint)(fVar14 < fVar13) << 0x1f;
        if (fVar13 < fVar15) {
          *param_5 = fVar12;
          param_5[1] = fVar11;
          param_5[2] = fVar10;
          fVar15 = fVar13;
        }
        bVar9 = SUB41(in_fpscr >> 0x1f,0);
        if (bVar9) {
          *param_6 = fVar12;
          param_6[1] = fVar11;
          param_6[2] = fVar10;
        }
        if (bVar9) {
          fVar14 = fVar13;
        }
        *param_4 = *param_4 + fVar12;
        param_4[1] = param_4[1] + fVar11;
        param_4[2] = param_4[2] + fVar10;
      }
    }
  }
  if (uVar8 != 0) {
    fVar16 = (float)VectorSignedToFloat(uVar8,(byte)(in_fpscr >> 0x16) & 3);
    fVar16 = 1.0 / fVar16;
    *param_4 = *param_4 * fVar16;
    param_4[1] = param_4[1] * fVar16;
    param_4[2] = param_4[2] * fVar16;
    *param_7 = SQRT(fVar15);
    *param_8 = SQRT(fVar14);
  }
  return uVar8;
}

