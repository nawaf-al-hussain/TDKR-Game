// _ZN17CollisionGeometryC1EPS_P11CGameObject @ 0014813c

int * _ZN17CollisionGeometryC1EPS_P11CGameObject(int *param_1,int *param_2,int param_3)

{
  uint uVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined1 *puVar4;
  int iVar5;
  int iVar6;
  undefined4 *puVar7;
  undefined4 *puVar8;
  undefined4 *puVar9;
  uint uVar10;
  undefined4 uVar11;
  undefined1 *puVar12;
  undefined4 uVar13;
  undefined4 uVar14;
  uint uVar15;
  undefined4 *puVar16;
  bool bVar17;
  bool bVar18;
  
  iVar6 = DAT_00148884;
  iVar5 = DAT_00148880;
  *(undefined1 *)(param_1 + 1) = 0;
  param_1[3] = param_3;
  param_1[7] = 0;
  param_1[8] = 0;
  param_1[9] = 0;
  *(undefined1 *)(param_1 + 4) = 1;
  *(undefined1 *)((int)param_1 + 0x11) = 1;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xc] = 0;
  param_1[0xe] = 0;
  param_1[0xf] = 0;
  param_1[0x10] = 0;
  param_1[0x11] = 0;
  param_1[0x12] = 0;
  param_1[0x13] = 0;
  param_1[0x15] = 0;
  param_1[0x16] = 0;
  param_1[0x17] = 0;
  param_1[0x19] = 0;
  param_1[0x1a] = 0;
  param_1[0x1b] = 0;
  param_1[0x1c] = 0;
  param_1[0x1d] = 0;
  param_1[0x1e] = 0;
  param_1[0xd] = 0x3f800000;
  param_1[0x14] = 0x3f800000;
  param_1[0x1f] = 0x7f7fffff;
  param_1[0x20] = 0x7f7fffff;
  param_1[0x21] = 0x7f7fffff;
  param_1[0x22] = -0x800001;
  param_1[0x23] = -0x800001;
  param_1[0x18] = 0xffff;
  param_1[0x24] = -0x800001;
  param_1[0x2b] = 0;
  param_1[0x2c] = 0;
  *(undefined2 *)(param_1 + 6) = 0;
  param_1[0x30] = 0;
  param_1[0x31] = 0;
  param_1[0x32] = 0;
  param_1[0x33] = 0;
  param_1[0x34] = 0;
  param_1[0x35] = 0;
  param_1[0x36] = 0;
  param_1[0x37] = 0;
  param_1[0x38] = 0;
  param_1[0x41] = 0;
  *(undefined1 *)((int)param_1 + 0x109) = 0;
  *(undefined1 *)(param_1 + 0x43) = 0;
  param_1[0x44] = 0;
  param_1[0x45] = 0;
  param_1[0x46] = 0;
  param_1[0x25] = 0x7f7fffff;
  param_1[0x26] = 0x7f7fffff;
  param_1[0x27] = 0x7f7fffff;
  param_1[0x28] = -0x800001;
  param_1[0x29] = -0x800001;
  param_1[0x2a] = -0x800001;
  *param_1 = iVar5 + 0x148168;
  param_1[0x3a] = 0x7f7fffff;
  param_1[0x3b] = 0x7f7fffff;
  param_1[0x3c] = 0x7f7fffff;
  param_1[0x3d] = -0x800001;
  param_1[0x3e] = -0x800001;
  param_1[0x3f] = -0x800001;
  param_1[0x39] = iVar6 + 0x14816c;
  param_1[0x47] = 0;
  param_1[5] = 4;
  *(undefined2 *)(param_1 + 0x2f) = 0xffff;
  param_1[0x2d] = 0;
  param_1[0x2e] = 0;
  _ZNSt6vectorIcSaIcEE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPcS1_EEjRKc
            (param_1 + 0x44,0,0xf);
  if (param_1 == param_2) goto LAB_00148490;
  puVar9 = (undefined4 *)param_2[0x31];
  puVar8 = (undefined4 *)param_2[0x30];
  puVar2 = (undefined4 *)param_1[0x30];
  iVar5 = (int)puVar9 - (int)puVar8 >> 2;
  puVar4 = (undefined1 *)(iVar5 * -0x55555555);
  if ((undefined1 *)((param_1[0x32] - (int)puVar2 >> 2) * -0x55555555) < puVar4) {
    if (puVar4 == (undefined1 *)0x0) {
      puVar3 = (undefined4 *)0x0;
      iVar5 = 0;
    }
    else {
      if (&DAT_15555555 < puVar4) goto LAB_0014887c;
      iVar5 = iVar5 * 4;
      puVar3 = (undefined4 *)_Znwj(iVar5);
      puVar2 = (undefined4 *)param_1[0x30];
    }
    if (puVar9 != puVar8) {
      puVar7 = puVar8 + 3;
      uVar10 = (int)puVar9 - (int)puVar7;
      puVar9 = puVar3;
      do {
        if (puVar9 + 3 != (undefined4 *)&DAT_0000000c) {
          *puVar9 = puVar7[-3];
          puVar9[1] = puVar7[-2];
          puVar9[2] = puVar7[-1];
        }
        puVar7 = puVar7 + 3;
        puVar9 = puVar9 + 3;
      } while (puVar7 != (undefined4 *)((int)puVar8 + (uVar10 & 0xfffffffc) + 0x18));
    }
    if (puVar2 != (undefined4 *)0x0) {
      _ZdlPv();
    }
    puVar2 = (undefined4 *)((int)puVar3 + iVar5);
    param_1[0x30] = (int)puVar3;
    param_1[0x32] = (int)puVar2;
  }
  else {
    puVar3 = (undefined4 *)param_1[0x31];
    iVar6 = (int)puVar3 - (int)puVar2 >> 2;
    if ((undefined1 *)(iVar6 * -0x55555555) < puVar4) {
      puVar16 = puVar8 + iVar6;
      iVar6 = ((iVar6 << 2) >> 2) * -0x55555555;
      puVar7 = puVar2;
      if (0 < iVar6) {
        do {
          iVar6 = iVar6 + -1;
          *puVar7 = *puVar8;
          puVar7[1] = puVar8[1];
          puVar7[2] = puVar8[2];
          puVar7 = puVar7 + 3;
          puVar8 = puVar8 + 3;
        } while (iVar6 != 0);
      }
      if (puVar9 != puVar16) {
        puVar8 = puVar16 + 3;
        uVar10 = (int)puVar9 - (int)puVar8;
        do {
          if (puVar3 + 3 != (undefined4 *)&DAT_0000000c) {
            *puVar3 = puVar8[-3];
            puVar3[1] = puVar8[-2];
            puVar3[2] = puVar8[-1];
          }
          puVar8 = puVar8 + 3;
          puVar3 = puVar3 + 3;
        } while (puVar8 != (undefined4 *)((int)puVar16 + (uVar10 & 0xfffffffc) + 0x18));
      }
    }
    else {
      puVar9 = puVar2;
      if (0 < (int)puVar4) {
        do {
          puVar4 = puVar4 + -1;
          *puVar9 = *puVar8;
          puVar9[1] = puVar8[1];
          puVar9[2] = puVar8[2];
          puVar9 = puVar9 + 3;
          puVar8 = puVar8 + 3;
        } while (puVar4 != (undefined1 *)0x0);
        puVar2 = puVar2 + iVar5;
        goto LAB_001483b4;
      }
    }
    puVar2 = puVar2 + iVar5;
  }
LAB_001483b4:
  puVar3 = (undefined4 *)param_2[0x34];
  puVar8 = (undefined4 *)param_2[0x33];
  puVar9 = (undefined4 *)param_1[0x33];
  iVar5 = (int)puVar3 - (int)puVar8;
  param_1[0x31] = (int)puVar2;
  uVar10 = iVar5 * -0x55555555;
  if ((uint)((param_1[0x35] - (int)puVar9) * -0x55555555) < uVar10) {
    if (uVar10 == 0) {
      puVar4 = (undefined1 *)0x0;
      iVar5 = 0;
      puVar12 = puVar4;
    }
    else {
      if (0x55555555 < uVar10) {
LAB_0014887c:
                    /* WARNING: Subroutine does not return */
        _ZSt17__throw_bad_allocv();
      }
      puVar4 = (undefined1 *)_Znwj(iVar5);
      puVar12 = puVar4;
    }
    for (; puVar3 != puVar8; puVar8 = (undefined4 *)((int)puVar8 + 3)) {
      if (puVar4 != (undefined1 *)0x0) {
        *puVar4 = *(undefined1 *)puVar8;
        puVar4[1] = *(undefined1 *)((int)puVar8 + 1);
        puVar4[2] = *(undefined1 *)((int)puVar8 + 2);
      }
      puVar4 = puVar4 + 3;
    }
    if (param_1[0x33] != 0) {
      _ZdlPv();
    }
    param_1[0x33] = (int)puVar12;
    param_1[0x35] = (int)(puVar12 + iVar5);
    param_1[0x34] = (int)(puVar12 + iVar5);
    goto LAB_00148490;
  }
  puVar4 = (undefined1 *)param_1[0x34];
  if ((uint)(((int)puVar4 - (int)puVar9) * -0x55555555) < uVar10) {
    puVar2 = (undefined4 *)((int)puVar8 + ((int)puVar4 - (int)puVar9));
    uVar10 = ((int)puVar2 - (int)puVar8) * -0x55555555;
    if (0 < (int)uVar10) {
      uVar1 = uVar10 >> 2;
      bVar18 = puVar9 + 3 <= puVar8;
      bVar17 = puVar8 == puVar9 + 3;
      if (!bVar18 || bVar17) {
        bVar18 = puVar8 + 3 <= puVar9;
        bVar17 = puVar9 == puVar8 + 3;
      }
      uVar15 = uVar10;
      if (uVar1 == 0 ||
          ((uVar10 < 4 || (((uint)puVar9 | (uint)puVar8) & 3) != 0) || (!bVar18 || bVar17))) {
LAB_001487bc:
        do {
          uVar15 = uVar15 - 1;
          *(undefined1 *)puVar9 = *(undefined1 *)puVar8;
          *(undefined1 *)((int)puVar9 + 1) = *(undefined1 *)((int)puVar8 + 1);
          puVar4 = (undefined1 *)((int)puVar8 + 2);
          puVar8 = (undefined4 *)((int)puVar8 + 3);
          *(undefined1 *)((int)puVar9 + 2) = *puVar4;
          puVar9 = (undefined4 *)((int)puVar9 + 3);
        } while (0 < (int)uVar15);
      }
      else {
        uVar15 = 0;
        puVar2 = puVar9;
        puVar3 = puVar8;
        do {
          uVar14 = *puVar3;
          uVar15 = uVar15 + 1;
          uVar13 = puVar3[1];
          uVar11 = puVar3[2];
          puVar3 = puVar3 + 3;
          *puVar2 = uVar14;
          puVar2[1] = uVar13;
          puVar2[2] = uVar11;
          puVar2 = puVar2 + 3;
        } while (uVar15 < uVar1);
        uVar15 = uVar10 + uVar1 * -4;
        puVar8 = puVar8 + uVar1 * 3;
        puVar9 = puVar9 + uVar1 * 3;
        if (uVar10 != uVar1 * 4) goto LAB_001487bc;
      }
      puVar4 = (undefined1 *)param_1[0x34];
      puVar9 = (undefined4 *)param_1[0x33];
      puVar3 = (undefined4 *)param_2[0x34];
      puVar2 = (undefined4 *)(puVar4 + (param_2[0x33] - (int)puVar9));
    }
    if (puVar2 != puVar3) {
      do {
        if (puVar4 != (undefined1 *)0x0) {
          *puVar4 = *(undefined1 *)puVar2;
          puVar4[1] = *(undefined1 *)((int)puVar2 + 1);
          puVar4[2] = *(undefined1 *)((int)puVar2 + 2);
        }
        puVar2 = (undefined4 *)((int)puVar2 + 3);
        puVar4 = puVar4 + 3;
      } while (puVar2 != puVar3);
      param_1[0x34] = param_1[0x33] + iVar5;
      goto LAB_00148490;
    }
  }
  else if (0 < (int)uVar10) {
    uVar1 = uVar10 >> 2;
    bVar18 = puVar9 + 3 <= puVar8;
    bVar17 = puVar8 == puVar9 + 3;
    if (!bVar18 || bVar17) {
      bVar18 = puVar8 + 3 <= puVar9;
      bVar17 = puVar9 == puVar8 + 3;
    }
    if (uVar1 == 0 ||
        ((uVar10 < 4 || (((uint)puVar8 | (uint)puVar9) & 3) != 0) || (!bVar18 || bVar17))) {
LAB_001486ac:
      do {
        uVar10 = uVar10 - 1;
        *(undefined1 *)puVar9 = *(undefined1 *)puVar8;
        *(undefined1 *)((int)puVar9 + 1) = *(undefined1 *)((int)puVar8 + 1);
        puVar4 = (undefined1 *)((int)puVar8 + 2);
        puVar8 = (undefined4 *)((int)puVar8 + 3);
        *(undefined1 *)((int)puVar9 + 2) = *puVar4;
        puVar9 = (undefined4 *)((int)puVar9 + 3);
      } while (0 < (int)uVar10);
    }
    else {
      uVar15 = 0;
      puVar2 = puVar9;
      puVar3 = puVar8;
      do {
        uVar14 = *puVar3;
        uVar15 = uVar15 + 1;
        uVar13 = puVar3[1];
        uVar11 = puVar3[2];
        puVar3 = puVar3 + 3;
        *puVar2 = uVar14;
        puVar2[1] = uVar13;
        puVar2[2] = uVar11;
        puVar2 = puVar2 + 3;
      } while (uVar15 < uVar1);
      bVar17 = uVar10 != uVar1 * 4;
      puVar8 = puVar8 + uVar1 * 3;
      puVar9 = puVar9 + uVar1 * 3;
      uVar10 = uVar10 + uVar1 * -4;
      if (bVar17) goto LAB_001486ac;
    }
    param_1[0x34] = param_1[0x33] + iVar5;
    goto LAB_00148490;
  }
  param_1[0x34] = (int)((int)puVar9 + iVar5);
LAB_00148490:
  _ZNSt6vectorI17CollisionTriangleSaIS0_EEaSERKS2_(param_1 + 0x36,param_2 + 0x36);
  iVar6 = param_2[0x2e];
  iVar5 = param_2[6];
  param_1[0x2d] = param_2[0x2d];
  param_1[0x2e] = iVar6;
  *(short *)(param_1 + 6) = (short)iVar5;
  return param_1;
}

