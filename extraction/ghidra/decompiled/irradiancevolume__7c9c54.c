// _ZNK6glitch10irradiance17CIrradianceVolume17getLinearPointLowERKNS_4core8vector3dIfEEi @ 007c9c54

void _ZNK6glitch10irradiance17CIrradianceVolume17getLinearPointLowERKNS_4core8vector3dIfEEi
               (float *param_1,int param_2,float *param_3,int param_4)

{
  bool bVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  int iVar5;
  uint uVar6;
  int iVar7;
  uint uVar8;
  uint uVar9;
  float *pfVar10;
  uint uVar11;
  uint uVar12;
  uint uVar13;
  uint uVar14;
  uint uVar15;
  float *pfVar16;
  float *pfVar17;
  float *pfVar18;
  uint uVar19;
  int iVar20;
  uint in_fpscr;
  float fVar21;
  float fVar22;
  float fVar23;
  float fVar24;
  float fVar25;
  float fVar26;
  float fVar27;
  float fVar28;
  float fVar29;
  float fVar30;
  float fVar31;
  float fVar32;
  float fVar33;
  float fVar34;
  float fVar35;
  uint uVar36;
  float fVar37;
  float fVar38;
  float fVar39;
  float fVar40;
  float fVar41;
  float fVar42;
  float fVar43;
  float fVar44;
  float fVar45;
  float fVar46;
  float fVar47;
  float fVar48;
  float fVar49;
  uint uVar50;
  float fVar51;
  uint uVar52;
  float fVar53;
  float fVar54;
  float fVar55;
  float fVar56;
  float fVar57;
  float fVar58;
  float fVar59;
  float fVar60;
  float fVar61;
  
  iVar7 = *(int *)(param_2 + 0x40);
  iVar5 = *(int *)(param_2 + 0x3c);
  uVar6 = iVar7 - 1;
  uVar8 = iVar5 - 1;
  iVar20 = *(int *)(param_2 + 0x38);
  uVar12 = iVar20 - 1;
  fVar31 = *(float *)(param_2 + 0x30) * 0.5;
  iVar2 = *(int *)(*(int *)(param_2 + 0xc) + param_4 * 4);
  fVar32 = (float)VectorSignedToFloat(uVar6,(byte)(in_fpscr >> 0x16) & 3);
  fVar35 = (float)VectorSignedToFloat(uVar8,(byte)(in_fpscr >> 0x16) & 3);
  fVar44 = (float)VectorSignedToFloat(uVar12,(byte)(in_fpscr >> 0x16) & 3);
  fVar43 = 1.0 / *(float *)(param_2 + 0x30);
  fVar48 = ((fVar32 * fVar31 - (*(float *)(param_2 + 0x20) + *(float *)(param_2 + 0x2c)) * 0.5) +
           param_3[2]) * fVar43;
  fVar32 = ((fVar35 * fVar31 - (*(float *)(param_2 + 0x1c) + *(float *)(param_2 + 0x28)) * 0.5) +
           param_3[1]) * fVar43;
  fVar43 = ((fVar44 * fVar31 - (*(float *)(param_2 + 0x18) + *(float *)(param_2 + 0x24)) * 0.5) +
           *param_3) * fVar43;
  uVar50 = (uint)fVar48;
  uVar52 = (uint)fVar32;
  uVar3 = uVar50 & ~((int)uVar50 >> 0x1f);
  uVar4 = uVar50 + 1 & ~((int)(uVar50 + 1) >> 0x1f);
  uVar9 = uVar3;
  if (iVar7 <= (int)uVar3) {
    uVar9 = uVar6;
  }
  uVar36 = (uint)fVar43;
  uVar19 = uVar52 & ~((int)uVar52 >> 0x1f);
  uVar14 = uVar4;
  if (iVar7 <= (int)uVar4) {
    uVar14 = uVar6;
  }
  uVar13 = uVar8;
  if ((int)uVar19 < iVar5) {
    uVar13 = uVar19;
  }
  fVar31 = (float)VectorSignedToFloat(uVar50,(byte)(in_fpscr >> 0x16) & 3);
  uVar50 = uVar36 & ~((int)uVar36 >> 0x1f);
  uVar11 = uVar12;
  if ((int)uVar50 < iVar20) {
    uVar11 = uVar50;
  }
  fVar48 = fVar48 - fVar31;
  pfVar10 = (float *)(iVar2 + ((uVar9 * iVar5 + uVar13) * iVar20 + uVar11) * 0x24);
  pfVar17 = (float *)(iVar2 + ((uVar14 * iVar5 + uVar13) * iVar20 + uVar11) * 0x24);
  fVar35 = pfVar10[3] + fVar48 * (pfVar17[3] - pfVar10[3]);
  fVar31 = pfVar10[4] + fVar48 * (pfVar17[4] - pfVar10[4]);
  fVar45 = pfVar10[5] + fVar48 * (pfVar17[5] - pfVar10[5]);
  fVar44 = pfVar10[6] + fVar48 * ((float)*(undefined8 *)(pfVar17 + 6) - pfVar10[6]);
  fVar37 = fVar35 * fVar35 + fVar31 * fVar31 + fVar45 * fVar45;
  uVar9 = in_fpscr & 0xfffffff | (uint)(fVar37 == 0.0) << 0x1e;
  bVar1 = SUB41(uVar9 >> 0x1e,0);
  if (!bVar1) {
    fVar37 = 1.0 / SQRT(fVar37);
  }
  fVar27 = pfVar10[7] +
           fVar48 * ((float)((ulonglong)*(undefined8 *)(pfVar17 + 6) >> 0x20) - pfVar10[7]);
  if (!bVar1) {
    fVar35 = fVar35 * fVar37;
  }
  if (!bVar1) {
    fVar31 = fVar31 * fVar37;
    fVar45 = fVar45 * fVar37;
  }
  if (iVar5 <= (int)uVar19) {
    uVar19 = uVar8;
  }
  uVar14 = uVar3;
  if (iVar7 <= (int)uVar3) {
    uVar14 = uVar6;
  }
  uVar13 = uVar4;
  if (iVar7 <= (int)uVar4) {
    uVar13 = uVar6;
  }
  uVar11 = uVar36 + 1 & ~((int)(uVar36 + 1) >> 0x1f);
  uVar15 = uVar12;
  if ((int)uVar11 < iVar20) {
    uVar15 = uVar11;
  }
  fVar46 = pfVar10[8] + fVar48 * (pfVar17[8] - pfVar10[8]);
  pfVar18 = (float *)(iVar2 + ((uVar14 * iVar5 + uVar19) * iVar20 + uVar15) * 0x24);
  pfVar16 = (float *)(iVar2 + ((uVar13 * iVar5 + uVar19) * iVar20 + uVar15) * 0x24);
  fVar38 = pfVar18[3] + fVar48 * (pfVar16[3] - pfVar18[3]);
  fVar33 = pfVar18[4] + fVar48 * (pfVar16[4] - pfVar18[4]);
  fVar37 = (float)VectorSignedToFloat(uVar36,(byte)(uVar9 >> 0x16) & 3);
  fVar47 = (float)VectorSignedToFloat(uVar52,(byte)(uVar9 >> 0x16) & 3);
  fVar43 = fVar43 - fVar37;
  fVar32 = fVar32 - fVar47;
  fVar47 = *pfVar10 + (*pfVar17 - *pfVar10) * fVar48;
  fVar21 = pfVar10[1] + (pfVar17[1] - pfVar10[1]) * fVar48;
  fVar22 = pfVar10[2] + (pfVar17[2] - pfVar10[2]) * fVar48;
  fVar49 = pfVar18[5] + fVar48 * (pfVar16[5] - pfVar18[5]);
  fVar37 = pfVar18[6] + fVar48 * (pfVar16[6] - pfVar18[6]);
  fVar23 = pfVar18[7] + fVar48 * (pfVar16[7] - pfVar18[7]);
  fVar24 = pfVar18[8] + fVar48 * (pfVar16[8] - pfVar18[8]);
  fVar39 = fVar38 * fVar38 + fVar33 * fVar33 + fVar49 * fVar49;
  fVar28 = *pfVar18 + (*pfVar16 - *pfVar18) * fVar48;
  fVar29 = pfVar18[1] + (pfVar16[1] - pfVar18[1]) * fVar48;
  fVar30 = pfVar18[2] + (pfVar16[2] - pfVar18[2]) * fVar48;
  if (fVar39 != 0.0) {
    fVar39 = 1.0 / SQRT(fVar39);
    fVar38 = fVar38 * fVar39;
    fVar33 = fVar33 * fVar39;
    fVar49 = fVar49 * fVar39;
  }
  uVar9 = uVar3;
  if (iVar7 <= (int)uVar3) {
    uVar9 = uVar6;
  }
  uVar52 = uVar52 + 1 & ~((int)(uVar52 + 1) >> 0x1f);
  uVar14 = uVar4;
  if (iVar7 <= (int)uVar4) {
    uVar14 = uVar6;
  }
  uVar19 = uVar8;
  if ((int)uVar52 < iVar5) {
    uVar19 = uVar52;
  }
  if (iVar20 <= (int)uVar50) {
    uVar50 = uVar12;
  }
  pfVar17 = (float *)(iVar2 + ((uVar9 * iVar5 + uVar19) * iVar20 + uVar50) * 0x24);
  pfVar10 = (float *)(iVar2 + ((uVar14 * iVar5 + uVar19) * iVar20 + uVar50) * 0x24);
  fVar39 = pfVar17[3] + fVar48 * (pfVar10[3] - pfVar17[3]);
  fVar34 = pfVar17[4] + fVar48 * (pfVar10[4] - pfVar17[4]);
  fVar53 = pfVar17[5] + fVar48 * (pfVar10[5] - pfVar17[5]);
  fVar40 = fVar39 * fVar39 + fVar34 * fVar34 + fVar53 * fVar53;
  if (fVar40 != 0.0) {
    fVar40 = 1.0 / SQRT(fVar40);
    fVar39 = fVar39 * fVar40;
    fVar34 = fVar34 * fVar40;
    fVar53 = fVar53 * fVar40;
  }
  if (iVar5 <= (int)uVar52) {
    uVar52 = uVar8;
  }
  if (iVar7 <= (int)uVar3) {
    uVar3 = uVar6;
  }
  if (iVar7 <= (int)uVar4) {
    uVar4 = uVar6;
  }
  if (iVar20 <= (int)uVar11) {
    uVar11 = uVar12;
  }
  pfVar18 = (float *)(iVar2 + ((uVar3 * iVar5 + uVar52) * iVar20 + uVar11) * 0x24);
  pfVar16 = (float *)(iVar2 + ((uVar4 * iVar5 + uVar52) * iVar20 + uVar11) * 0x24);
  fVar54 = pfVar18[7];
  fVar51 = pfVar18[8];
  fVar60 = pfVar16[7];
  fVar59 = pfVar16[8];
  fVar55 = pfVar18[6];
  fVar61 = pfVar16[6];
  fVar25 = pfVar16[1];
  fVar58 = pfVar16[2];
  fVar40 = pfVar18[1];
  fVar26 = pfVar18[2];
  fVar41 = pfVar18[3] + fVar48 * (pfVar16[3] - pfVar18[3]);
  fVar57 = pfVar18[4] + fVar48 * (pfVar16[4] - pfVar18[4]);
  fVar56 = pfVar18[5] + fVar48 * (pfVar16[5] - pfVar18[5]);
  fVar42 = fVar41 * fVar41 + fVar57 * fVar57 + fVar56 * fVar56;
  if (fVar42 != 0.0) {
    fVar42 = 1.0 / SQRT(fVar42);
    fVar41 = fVar41 * fVar42;
    fVar57 = fVar57 * fVar42;
    fVar56 = fVar56 * fVar42;
  }
  fVar35 = fVar35 + fVar32 * (fVar39 - fVar35);
  fVar31 = fVar31 + fVar32 * (fVar34 - fVar31);
  fVar45 = fVar45 + fVar32 * (fVar53 - fVar45);
  fVar39 = fVar35 * fVar35 + fVar31 * fVar31 + fVar45 * fVar45;
  fVar44 = fVar44 + fVar32 * ((pfVar17[6] + fVar48 * (pfVar10[6] - pfVar17[6])) - fVar44);
  fVar27 = fVar27 + fVar32 * ((pfVar17[7] + fVar48 * (pfVar10[7] - pfVar17[7])) - fVar27);
  fVar46 = fVar46 + fVar32 * ((pfVar17[8] + fVar48 * (pfVar10[8] - pfVar17[8])) - fVar46);
  fVar47 = fVar47 + ((*pfVar17 - fVar47) + (*pfVar10 - *pfVar17) * fVar48) * fVar32;
  fVar21 = fVar21 + ((pfVar17[1] - fVar21) + (pfVar10[1] - pfVar17[1]) * fVar48) * fVar32;
  fVar22 = fVar22 + ((pfVar17[2] - fVar22) + (pfVar10[2] - pfVar17[2]) * fVar48) * fVar32;
  if (fVar39 != 0.0) {
    fVar39 = 1.0 / SQRT(fVar39);
    fVar35 = fVar35 * fVar39;
    fVar31 = fVar31 * fVar39;
    fVar45 = fVar45 * fVar39;
  }
  fVar38 = fVar38 + fVar32 * (fVar41 - fVar38);
  fVar33 = fVar33 + fVar32 * (fVar57 - fVar33);
  fVar49 = fVar49 + fVar32 * (fVar56 - fVar49);
  fVar39 = fVar38 * fVar38 + fVar33 * fVar33 + fVar49 * fVar49;
  if (fVar39 != 0.0) {
    fVar39 = 1.0 / SQRT(fVar39);
    fVar38 = fVar38 * fVar39;
    fVar33 = fVar33 * fVar39;
    fVar49 = fVar49 * fVar39;
  }
  fVar35 = fVar35 + fVar43 * (fVar38 - fVar35);
  fVar31 = fVar31 + fVar43 * (fVar33 - fVar31);
  fVar45 = fVar45 + fVar43 * (fVar49 - fVar45);
  fVar33 = fVar35 * fVar35 + fVar31 * fVar31 + fVar45 * fVar45;
  *param_1 = fVar47 + ((fVar28 - fVar47) +
                      ((*pfVar18 - fVar28) + (*pfVar16 - *pfVar18) * fVar48) * fVar32) * fVar43;
  param_1[1] = fVar21 + ((fVar29 - fVar21) +
                        ((fVar40 - fVar29) + (fVar25 - fVar40) * fVar48) * fVar32) * fVar43;
  param_1[2] = fVar22 + ((fVar30 - fVar22) +
                        ((fVar26 - fVar30) + (fVar58 - fVar26) * fVar48) * fVar32) * fVar43;
  param_1[6] = fVar44 + fVar43 * ((fVar37 + fVar32 * ((fVar55 + fVar48 * (fVar61 - fVar55)) - fVar37
                                                     )) - fVar44);
  param_1[7] = fVar27 + fVar43 * ((fVar23 + fVar32 * ((fVar54 + fVar48 * (fVar60 - fVar54)) - fVar23
                                                     )) - fVar27);
  param_1[8] = fVar46 + fVar43 * ((fVar24 + fVar32 * ((fVar51 + fVar48 * (fVar59 - fVar51)) - fVar24
                                                     )) - fVar46);
  if (fVar33 != 0.0) {
    fVar32 = 1.0 / SQRT(fVar33);
    fVar35 = fVar35 * fVar32;
    fVar31 = fVar31 * fVar32;
    fVar45 = fVar45 * fVar32;
  }
  param_1[3] = fVar35;
  param_1[4] = fVar31;
  param_1[5] = fVar45;
  return;
}


