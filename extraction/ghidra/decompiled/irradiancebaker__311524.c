// _ZN15IrradianceBaker10BakeBufferEPvRKN6glitch4core8vector3dIfEEiiiii @ 00311524

void _ZN15IrradianceBaker10BakeBufferEPvRKN6glitch4core8vector3dIfEEiiiii
               (undefined4 *param_1,int param_2,undefined4 param_3,int param_4,int param_5,
               int param_6,undefined4 param_7,int param_8)

{
  float fVar1;
  int iVar2;
  float *pfVar3;
  uint *puVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  undefined1 auStack_e4 [4];
  float local_e0;
  float local_dc;
  float local_d8;
  float local_d4;
  float local_d0;
  float local_cc;
  float local_c8;
  float local_c4;
  float local_bc;
  float local_b8;
  float local_b4;
  float local_b0;
  float local_ac;
  float local_a8;
  float local_a4;
  float local_a0;
  float local_98;
  float local_94;
  float local_90;
  float local_8c;
  float local_88;
  float local_84;
  float local_80;
  float local_7c;
  
  fVar1 = DAT_003117c8;
  if (0 < param_8) {
    iVar2 = 0;
    pfVar3 = (float *)(param_2 + param_5);
    puVar4 = (uint *)(param_2 + param_6);
    do {
      while( true ) {
        (**(code **)(*(int *)*param_1 + 0x10))(auStack_e4,(int *)*param_1,param_2 + param_4);
        fVar10 = *pfVar3;
        fVar11 = pfVar3[1];
        fVar12 = pfVar3[2];
        if ((*puVar4 & 0xff000000) == 0) break;
LAB_003117a8:
        iVar2 = iVar2 + 1;
        *puVar4 = 1;
        if (iVar2 == param_8) {
          return;
        }
      }
      fVar5 = fVar11 * fVar10;
      fVar6 = fVar12 * fVar11;
      fVar7 = fVar12 * fVar12;
      fVar8 = fVar12 * fVar10;
      fVar9 = fVar10 * fVar10 - fVar11 * fVar11;
      fVar13 = local_d8 * fVar1 * fVar10 + local_e0 * fVar1 * fVar11 +
               local_dc * 0.32573497 * fVar12 + local_d4 * 0.2731371 * fVar5 +
               local_d0 * DAT_003117cc * fVar6 + local_cc * DAT_003117d0 * fVar7 +
               local_c8 * DAT_003117cc * fVar8 + local_c4 * DAT_003117d4 * fVar9;
      if (1.0 < fVar13) {
        fVar13 = 1.0;
      }
      if (fVar13 < DAT_003117d8) {
        fVar13 = DAT_003117d8;
      }
      if (((int)(fVar13 * DAT_003117dc) & 0xffffU) != 0) goto LAB_003117a8;
      iVar2 = iVar2 + 1;
      fVar13 = local_b4 * fVar1 * fVar10 + local_bc * fVar1 * fVar11 +
               local_b8 * 0.32573497 * fVar12 + local_b0 * 0.2731371 * fVar5 +
               local_ac * DAT_003117cc * fVar6 + local_a8 * DAT_003117d0 * fVar7 +
               local_a4 * DAT_003117cc * fVar8 + local_a0 * DAT_003117d4 * fVar9;
      fVar10 = local_90 * fVar1 * fVar10 + local_98 * fVar1 * fVar11 +
               local_94 * 0.32573497 * fVar12 + local_8c * 0.2731371 * fVar5 +
               local_88 * DAT_003117cc * fVar6 + local_84 * DAT_003117d0 * fVar7 +
               local_80 * DAT_003117cc * fVar8 + local_7c * DAT_003117d4 * fVar9;
      if (1.0 < fVar13) {
        fVar13 = 1.0;
      }
      if (1.0 < fVar10) {
        fVar10 = 1.0;
      }
      if (fVar13 < DAT_003117d8) {
        fVar13 = DAT_003117d8;
      }
      if (fVar10 < DAT_003117d8) {
        fVar10 = DAT_003117d8;
      }
      *puVar4 = (uint)((int)(fVar10 * DAT_003117dc) != 0 ||
                      ((int)(fVar13 * DAT_003117dc) & 0xffffffU) != 0);
    } while (iVar2 != param_8);
  }
  return;
}

