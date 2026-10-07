// _ZNK6glitch10irradiance17CIrradianceVolume14getLinearPointERKNS_4core8vector3dIfEEi @ 007c92c8

void _ZNK6glitch10irradiance17CIrradianceVolume14getLinearPointERKNS_4core8vector3dIfEEi
               (int param_1,int *param_2,float *param_3,int param_4)

{
  int iVar1;
  uint uVar2;
  float *pfVar3;
  float *pfVar4;
  uint uVar5;
  int iVar6;
  uint uVar7;
  float *pfVar8;
  uint uVar9;
  int iVar10;
  int iVar11;
  uint uVar12;
  uint uVar13;
  uint uVar14;
  uint uVar15;
  int iVar16;
  uint uVar17;
  uint uVar18;
  int iVar19;
  uint uVar20;
  int iVar21;
  uint in_fpscr;
  uint uVar22;
  uint uVar23;
  uint uVar24;
  float fVar25;
  float fVar26;
  float fVar27;
  float fVar28;
  float fVar29;
  float fVar30;
  float local_33c;
  float local_338 [27];
  float local_2cc;
  float local_2c8;
  float local_2c4;
  float local_2c0;
  float local_2bc;
  float local_2b8;
  float local_2b4 [27];
  float local_248;
  float local_244;
  float local_240;
  float local_23c;
  float local_238;
  float local_234;
  float local_230 [27];
  float local_1c4;
  float local_1c0;
  float local_1bc;
  float local_1b8;
  float local_1b4;
  float local_1b0;
  float local_1ac [27];
  float local_140;
  float local_13c;
  float local_138;
  float local_134;
  float local_130;
  float local_12c;
  float local_128 [27];
  float local_bc;
  float local_b8;
  float local_b4;
  float local_b0;
  float local_ac;
  float local_a8;
  float local_a4 [27];
  float local_38;
  float local_34;
  float local_30;
  float local_2c;
  float local_28;
  float local_24;
  
  iVar11 = param_2[0x10];
  iVar10 = param_2[0xf];
  iVar21 = param_2[0xe];
  uVar12 = iVar11 - 1;
  uVar15 = iVar10 - 1;
  uVar17 = iVar21 - 1;
  fVar28 = (float)param_2[0xc] * 0.5;
  pfVar4 = &local_33c;
  iVar1 = *(int *)(*param_2 + param_4 * 4);
  fVar25 = (float)VectorSignedToFloat(uVar12,(byte)(in_fpscr >> 0x16) & 3);
  fVar26 = (float)VectorSignedToFloat(uVar15,(byte)(in_fpscr >> 0x16) & 3);
  fVar27 = (float)VectorSignedToFloat(uVar17,(byte)(in_fpscr >> 0x16) & 3);
  fVar29 = 1.0 / (float)param_2[0xc];
  fVar30 = ((fVar25 * fVar28 - ((float)param_2[8] + (float)param_2[0xb]) * 0.5) + param_3[2]) *
           fVar29;
  fVar25 = ((fVar26 * fVar28 - ((float)param_2[7] + (float)param_2[10]) * 0.5) + param_3[1]) *
           fVar29;
  fVar29 = ((fVar27 * fVar28 - ((float)param_2[6] + (float)param_2[9]) * 0.5) + *param_3) * fVar29;
  uVar23 = (uint)fVar30;
  uVar24 = (uint)fVar25;
  uVar14 = uVar23 & ~((int)uVar23 >> 0x1f);
  uVar13 = uVar23 + 1 & ~((int)(uVar23 + 1) >> 0x1f);
  uVar7 = uVar12;
  if ((int)uVar14 < iVar11) {
    uVar7 = uVar14;
  }
  uVar9 = uVar12;
  if ((int)uVar13 < iVar11) {
    uVar9 = uVar13;
  }
  uVar22 = (uint)fVar29;
  uVar20 = uVar24 & ~((int)uVar24 >> 0x1f);
  uVar2 = uVar15;
  if ((int)uVar20 < iVar10) {
    uVar2 = uVar20;
  }
  fVar26 = (float)VectorSignedToFloat(uVar24,(byte)(in_fpscr >> 0x16) & 3);
  uVar5 = uVar22 & ~((int)uVar22 >> 0x1f);
  uVar18 = uVar5;
  if (iVar21 <= (int)uVar5) {
    uVar18 = uVar17;
  }
  fVar28 = (float)VectorSignedToFloat(uVar22,(byte)(in_fpscr >> 0x16) & 3);
  fVar27 = (float)VectorSignedToFloat(uVar23,(byte)(in_fpscr >> 0x16) & 3);
  iVar16 = iVar1 + ((uVar7 * iVar10 + uVar2) * iVar21 + uVar18) * 0x84;
  iVar19 = iVar1 + ((uVar9 * iVar10 + uVar2) * iVar21 + uVar18) * 0x84;
  pfVar3 = (float *)(iVar16 + -4);
  pfVar8 = (float *)(iVar19 + -4);
  iVar6 = 0;
  fVar29 = fVar29 - fVar28;
  fVar25 = fVar25 - fVar26;
  fVar30 = fVar30 - fVar27;
  do {
    pfVar3 = pfVar3 + 1;
    pfVar8 = pfVar8 + 1;
    iVar6 = iVar6 + 1;
    pfVar4 = pfVar4 + 1;
    *pfVar4 = *pfVar3 + (*pfVar8 - *pfVar3) * fVar30;
  } while (iVar6 != 0x1b);
  local_2c8 = *(float *)(iVar16 + 0x70) +
              fVar30 * (*(float *)(iVar19 + 0x70) - *(float *)(iVar16 + 0x70));
  local_2cc = *(float *)(iVar16 + 0x6c) +
              fVar30 * (*(float *)(iVar19 + 0x6c) - *(float *)(iVar16 + 0x6c));
  local_2c4 = *(float *)(iVar16 + 0x74) +
              fVar30 * (*(float *)(iVar19 + 0x74) - *(float *)(iVar16 + 0x74));
  fVar26 = local_2cc * local_2cc + local_2c8 * local_2c8 + local_2c4 * local_2c4;
  local_2c0 = *(float *)(iVar16 + 0x78) +
              fVar30 * (*(float *)(iVar19 + 0x78) - *(float *)(iVar16 + 0x78));
  local_2bc = *(float *)(iVar16 + 0x7c) +
              fVar30 * (*(float *)(iVar19 + 0x7c) - *(float *)(iVar16 + 0x7c));
  local_2b8 = *(float *)(iVar16 + 0x80) +
              fVar30 * (*(float *)(iVar19 + 0x80) - *(float *)(iVar16 + 0x80));
  if (fVar26 != 0.0) {
    fVar26 = 1.0 / SQRT(fVar26);
    local_2cc = local_2cc * fVar26;
    local_2c8 = local_2c8 * fVar26;
    local_2c4 = local_2c4 * fVar26;
  }
  if (iVar10 <= (int)uVar20) {
    uVar20 = uVar15;
  }
  uVar7 = uVar12;
  if ((int)uVar14 < iVar11) {
    uVar7 = uVar14;
  }
  uVar23 = uVar12;
  if ((int)uVar13 < iVar11) {
    uVar23 = uVar13;
  }
  uVar9 = uVar22 + 1 & ~((int)(uVar22 + 1) >> 0x1f);
  iVar6 = 0;
  uVar2 = uVar9;
  if (iVar21 <= (int)uVar9) {
    uVar2 = uVar17;
  }
  pfVar8 = &local_2b8;
  iVar16 = iVar1 + ((uVar7 * iVar10 + uVar20) * iVar21 + uVar2) * 0x84;
  pfVar4 = (float *)(iVar16 + -4);
  iVar19 = iVar1 + ((uVar23 * iVar10 + uVar20) * iVar21 + uVar2) * 0x84;
  pfVar3 = (float *)(iVar19 + -4);
  do {
    pfVar4 = pfVar4 + 1;
    pfVar3 = pfVar3 + 1;
    iVar6 = iVar6 + 1;
    pfVar8 = pfVar8 + 1;
    *pfVar8 = *pfVar4 + (*pfVar3 - *pfVar4) * fVar30;
  } while (iVar6 != 0x1b);
  local_244 = *(float *)(iVar16 + 0x70) +
              fVar30 * (*(float *)(iVar19 + 0x70) - *(float *)(iVar16 + 0x70));
  local_248 = *(float *)(iVar16 + 0x6c) +
              fVar30 * (*(float *)(iVar19 + 0x6c) - *(float *)(iVar16 + 0x6c));
  local_240 = *(float *)(iVar16 + 0x74) +
              fVar30 * (*(float *)(iVar19 + 0x74) - *(float *)(iVar16 + 0x74));
  fVar26 = local_248 * local_248 + local_244 * local_244 + local_240 * local_240;
  local_23c = *(float *)(iVar16 + 0x78) +
              fVar30 * (*(float *)(iVar19 + 0x78) - *(float *)(iVar16 + 0x78));
  local_238 = *(float *)(iVar16 + 0x7c) +
              fVar30 * (*(float *)(iVar19 + 0x7c) - *(float *)(iVar16 + 0x7c));
  local_234 = *(float *)(iVar16 + 0x80) +
              fVar30 * (*(float *)(iVar19 + 0x80) - *(float *)(iVar16 + 0x80));
  if (fVar26 != 0.0) {
    fVar26 = 1.0 / SQRT(fVar26);
    local_248 = local_248 * fVar26;
    local_244 = local_244 * fVar26;
    local_240 = local_240 * fVar26;
  }
  iVar6 = 0;
  uVar7 = uVar12;
  if ((int)uVar14 < iVar11) {
    uVar7 = uVar14;
  }
  uVar24 = uVar24 + 1 & ~((int)(uVar24 + 1) >> 0x1f);
  uVar23 = uVar12;
  if ((int)uVar13 < iVar11) {
    uVar23 = uVar13;
  }
  uVar2 = uVar15;
  if ((int)uVar24 < iVar10) {
    uVar2 = uVar24;
  }
  if (iVar21 <= (int)uVar5) {
    uVar5 = uVar17;
  }
  pfVar8 = &local_234;
  iVar19 = iVar1 + ((uVar23 * iVar10 + uVar2) * iVar21 + uVar5) * 0x84;
  iVar16 = iVar1 + ((uVar7 * iVar10 + uVar2) * iVar21 + uVar5) * 0x84;
  pfVar4 = (float *)(iVar16 + -4);
  pfVar3 = (float *)(iVar19 + -4);
  do {
    pfVar4 = pfVar4 + 1;
    pfVar3 = pfVar3 + 1;
    iVar6 = iVar6 + 1;
    pfVar8 = pfVar8 + 1;
    *pfVar8 = *pfVar4 + (*pfVar3 - *pfVar4) * fVar30;
  } while (iVar6 != 0x1b);
  local_1c0 = *(float *)(iVar16 + 0x70) +
              fVar30 * (*(float *)(iVar19 + 0x70) - *(float *)(iVar16 + 0x70));
  local_1c4 = *(float *)(iVar16 + 0x6c) +
              fVar30 * (*(float *)(iVar19 + 0x6c) - *(float *)(iVar16 + 0x6c));
  local_1bc = *(float *)(iVar16 + 0x74) +
              fVar30 * (*(float *)(iVar19 + 0x74) - *(float *)(iVar16 + 0x74));
  fVar26 = local_1c4 * local_1c4 + local_1c0 * local_1c0 + local_1bc * local_1bc;
  local_1b8 = *(float *)(iVar16 + 0x78) +
              fVar30 * (*(float *)(iVar19 + 0x78) - *(float *)(iVar16 + 0x78));
  local_1b4 = *(float *)(iVar16 + 0x7c) +
              fVar30 * (*(float *)(iVar19 + 0x7c) - *(float *)(iVar16 + 0x7c));
  local_1b0 = *(float *)(iVar16 + 0x80) +
              fVar30 * (*(float *)(iVar19 + 0x80) - *(float *)(iVar16 + 0x80));
  if (fVar26 != 0.0) {
    fVar26 = 1.0 / SQRT(fVar26);
    local_1c4 = local_1c4 * fVar26;
    local_1c0 = local_1c0 * fVar26;
    local_1bc = local_1bc * fVar26;
  }
  iVar6 = 0;
  if (iVar10 <= (int)uVar24) {
    uVar24 = uVar15;
  }
  if (iVar11 <= (int)uVar14) {
    uVar14 = uVar12;
  }
  pfVar4 = &local_1b0;
  if (iVar11 <= (int)uVar13) {
    uVar13 = uVar12;
  }
  if (iVar21 <= (int)uVar9) {
    uVar9 = uVar17;
  }
  iVar11 = iVar1 + ((uVar14 * iVar10 + uVar24) * iVar21 + uVar9) * 0x84;
  pfVar3 = (float *)(iVar11 + -4);
  iVar1 = iVar1 + ((uVar13 * iVar10 + uVar24) * iVar21 + uVar9) * 0x84;
  pfVar8 = (float *)(iVar1 + -4);
  do {
    pfVar3 = pfVar3 + 1;
    pfVar8 = pfVar8 + 1;
    iVar6 = iVar6 + 1;
    pfVar4 = pfVar4 + 1;
    *pfVar4 = *pfVar3 + (*pfVar8 - *pfVar3) * fVar30;
  } while (iVar6 != 0x1b);
  local_13c = *(float *)(iVar11 + 0x70) +
              fVar30 * (*(float *)(iVar1 + 0x70) - *(float *)(iVar11 + 0x70));
  local_140 = *(float *)(iVar11 + 0x6c) +
              fVar30 * (*(float *)(iVar1 + 0x6c) - *(float *)(iVar11 + 0x6c));
  local_138 = *(float *)(iVar11 + 0x74) +
              fVar30 * (*(float *)(iVar1 + 0x74) - *(float *)(iVar11 + 0x74));
  fVar26 = local_140 * local_140 + local_13c * local_13c + local_138 * local_138;
  local_134 = *(float *)(iVar11 + 0x78) +
              fVar30 * (*(float *)(iVar1 + 0x78) - *(float *)(iVar11 + 0x78));
  local_130 = *(float *)(iVar11 + 0x7c) +
              fVar30 * (*(float *)(iVar1 + 0x7c) - *(float *)(iVar11 + 0x7c));
  local_12c = *(float *)(iVar11 + 0x80) +
              fVar30 * (*(float *)(iVar1 + 0x80) - *(float *)(iVar11 + 0x80));
  if (fVar26 != 0.0) {
    fVar26 = 1.0 / SQRT(fVar26);
    local_140 = local_140 * fVar26;
    local_13c = local_13c * fVar26;
    local_138 = local_138 * fVar26;
  }
  pfVar8 = &local_33c;
  pfVar4 = &local_234;
  pfVar3 = &local_12c;
  iVar1 = 0;
  do {
    pfVar8 = pfVar8 + 1;
    pfVar4 = pfVar4 + 1;
    iVar1 = iVar1 + 1;
    pfVar3 = pfVar3 + 1;
    *pfVar3 = *pfVar8 + (*pfVar4 - *pfVar8) * fVar25;
  } while (iVar1 != 0x1b);
  local_bc = local_2cc + fVar25 * (local_1c4 - local_2cc);
  local_b8 = local_2c8 + fVar25 * (local_1c0 - local_2c8);
  local_b4 = local_2c4 + fVar25 * (local_1bc - local_2c4);
  fVar26 = local_bc * local_bc + local_b8 * local_b8 + local_b4 * local_b4;
  local_b0 = local_2c0 + fVar25 * (local_1b8 - local_2c0);
  local_ac = local_2bc + fVar25 * (local_1b4 - local_2bc);
  local_a8 = local_2b8 + fVar25 * (local_1b0 - local_2b8);
  if (fVar26 != 0.0) {
    fVar26 = 1.0 / SQRT(fVar26);
    local_bc = local_bc * fVar26;
    local_b8 = local_b8 * fVar26;
    local_b4 = local_b4 * fVar26;
  }
  pfVar8 = &local_2b8;
  pfVar4 = &local_1b0;
  pfVar3 = &local_a8;
  iVar1 = 0;
  do {
    pfVar4 = pfVar4 + 1;
    pfVar8 = pfVar8 + 1;
    iVar1 = iVar1 + 1;
    pfVar3 = pfVar3 + 1;
    *pfVar3 = *pfVar8 + (*pfVar4 - *pfVar8) * fVar25;
  } while (iVar1 != 0x1b);
  local_38 = local_248 + fVar25 * (local_140 - local_248);
  local_34 = local_244 + fVar25 * (local_13c - local_244);
  local_30 = local_240 + fVar25 * (local_138 - local_240);
  fVar26 = local_38 * local_38 + local_34 * local_34 + local_30 * local_30;
  local_2c = local_23c + fVar25 * (local_134 - local_23c);
  local_28 = local_238 + fVar25 * (local_130 - local_238);
  local_24 = local_234 + fVar25 * (local_12c - local_234);
  if (fVar26 != 0.0) {
    fVar25 = 1.0 / SQRT(fVar26);
    local_38 = local_38 * fVar25;
    local_34 = local_34 * fVar25;
    local_30 = local_30 * fVar25;
  }
  pfVar8 = (float *)(param_1 + -4);
  pfVar4 = &local_12c;
  pfVar3 = &local_a8;
  iVar1 = 0x1b;
  do {
    pfVar4 = pfVar4 + 1;
    pfVar3 = pfVar3 + 1;
    iVar1 = iVar1 + -1;
    pfVar8 = pfVar8 + 1;
    *pfVar8 = *pfVar4 + (*pfVar3 - *pfVar4) * fVar29;
  } while (iVar1 != 0);
  local_bc = local_bc + fVar29 * (local_38 - local_bc);
  local_b8 = local_b8 + fVar29 * (local_34 - local_b8);
  local_b4 = local_b4 + fVar29 * (local_30 - local_b4);
  fVar25 = local_bc * local_bc + local_b8 * local_b8 + local_b4 * local_b4;
  *(float *)(param_1 + 0x78) = local_b0 + fVar29 * (local_2c - local_b0);
  *(float *)(param_1 + 0x7c) = local_ac + fVar29 * (local_28 - local_ac);
  *(float *)(param_1 + 0x80) = local_a8 + fVar29 * (local_24 - local_a8);
  if (fVar25 != 0.0) {
    fVar25 = 1.0 / SQRT(fVar25);
    local_bc = local_bc * fVar25;
    local_b8 = local_b8 * fVar25;
    local_b4 = local_b4 * fVar25;
  }
  *(float *)(param_1 + 0x6c) = local_bc;
  *(float *)(param_1 + 0x70) = local_b8;
  *(float *)(param_1 + 0x74) = local_b4;
  return;
}


