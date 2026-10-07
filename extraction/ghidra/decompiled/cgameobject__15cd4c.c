// _Z30FindRoadWaypointsFromPositionsP11CGameObjectPN6glitch4core8vector3dIfEEPP11TrafficNodeS8_S8_ @ 0015cd4c

/* WARNING: Type propagation algorithm not settling */

undefined1
_Z30FindRoadWaypointsFromPositionsP11CGameObjectPN6glitch4core8vector3dIfEEPP11TrafficNodeS8_S8_
          (int *param_1,float *param_2,undefined4 *param_3,undefined4 *param_4,undefined4 *param_5)

{
  undefined8 *puVar1;
  int *piVar2;
  int iVar3;
  int *piVar4;
  int iVar5;
  undefined4 *puVar6;
  int iVar7;
  undefined4 *puVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  float fVar19;
  float fVar20;
  float fVar21;
  float fVar22;
  float local_54;
  float local_50;
  float local_4c;
  float local_48;
  float local_44;
  float local_40;
  float local_3c;
  float local_38;
  float local_34;
  
  puVar1 = (undefined8 *)(**(code **)(*param_1 + 0x18))();
  iVar12 = *(int *)(DAT_0015d158 + 0x15cd80);
  local_34 = *(float *)(puVar1 + 1);
  piVar2 = *(int **)(iVar12 + 8);
  if (piVar2 == (int *)0x0) {
    return 0;
  }
  fVar20 = (float)*puVar1;
  fVar22 = (float)((ulonglong)*puVar1 >> 0x20);
  if (param_2 == (float *)0x0) {
    iVar9 = 0;
    piVar4 = piVar2;
    fVar13 = DAT_0015d154;
    do {
      iVar3 = *piVar4;
      fVar15 = fVar20 - *(float *)(iVar3 + 0x50);
      piVar4 = (int *)piVar4[1];
      fVar18 = fVar22 - *(float *)(iVar3 + 0x54);
      fVar14 = local_34 - *(float *)(iVar3 + 0x58);
      fVar18 = fVar15 * fVar15 + fVar18 * fVar18 + fVar14 * fVar14;
      if (fVar18 < fVar13) {
        fVar13 = fVar18;
        iVar9 = iVar3;
      }
    } while (piVar4 != (int *)0x0);
    iVar3 = 0;
  }
  else {
    iVar3 = 0;
    iVar9 = 0;
    piVar4 = piVar2;
    fVar13 = DAT_0015d154;
    fVar18 = DAT_0015d154;
    do {
      iVar7 = *piVar4;
      fVar19 = *param_2 - *(float *)(iVar7 + 0x50);
      piVar4 = (int *)piVar4[1];
      fVar21 = fVar20 - *(float *)(iVar7 + 0x50);
      fVar14 = param_2[1] - *(float *)(iVar7 + 0x54);
      fVar15 = fVar22 - *(float *)(iVar7 + 0x54);
      fVar16 = param_2[2] - *(float *)(iVar7 + 0x58);
      fVar17 = local_34 - *(float *)(iVar7 + 0x58);
      fVar14 = fVar19 * fVar19 + fVar14 * fVar14 + fVar16 * fVar16;
      fVar15 = fVar21 * fVar21 + fVar15 * fVar15 + fVar17 * fVar17;
      if (fVar14 < fVar18) {
        fVar18 = fVar14;
        iVar3 = iVar7;
      }
      if (fVar15 < fVar13) {
        fVar13 = fVar15;
        iVar9 = iVar7;
      }
    } while (piVar4 != (int *)0x0);
  }
  iVar7 = 0;
  fVar13 = DAT_0015d154;
  do {
    iVar5 = *piVar2;
    fVar15 = fVar20 - *(float *)(iVar5 + 0x50);
    fVar18 = fVar22 - *(float *)(iVar5 + 0x54);
    fVar14 = local_34 - *(float *)(iVar5 + 0x58);
    fVar14 = fVar15 * fVar15 + fVar18 * fVar18 + fVar14 * fVar14;
    iVar10 = iVar7;
    fVar18 = fVar13;
    if ((fVar14 < fVar13) && (iVar5 != iVar9)) {
      for (piVar4 = *(int **)(iVar9 + 0x18); piVar4 != (int *)0x0; piVar4 = (int *)piVar4[1]) {
        iVar10 = iVar5;
        fVar18 = fVar14;
        if (iVar5 == *piVar4) goto LAB_0015ce9c;
      }
      piVar4 = *(int **)(iVar5 + 0x18);
      iVar10 = iVar7;
      fVar18 = fVar13;
      if (piVar4 != (int *)0x0) {
        iVar11 = *piVar4;
        while ((iVar10 = iVar5, fVar18 = fVar14, iVar11 != iVar9 &&
               (piVar4 = (int *)piVar4[1], iVar10 = iVar7, fVar18 = fVar13, piVar4 != (int *)0x0)))
        {
          iVar11 = *piVar4;
        }
      }
    }
LAB_0015ce9c:
    piVar2 = (int *)piVar2[1];
    iVar7 = iVar10;
    fVar13 = fVar18;
  } while (piVar2 != (int *)0x0);
  if (iVar9 == 0 || iVar10 == 0) {
    return 0;
  }
  if (param_2 != (float *)0x0) {
    if (iVar3 == 0) {
      piVar2 = (int *)0x0;
    }
    else {
      puVar8 = *(undefined4 **)(iVar12 + 0x50);
      if (puVar8 == (undefined4 *)0x0) {
        piVar2 = (int *)0x0;
      }
      else {
        do {
          piVar2 = (int *)*puVar8;
          if (*piVar2 == iVar3) goto LAB_0015cef4;
          puVar8 = (undefined4 *)puVar8[2];
        } while (puVar8 != (undefined4 *)0x0);
        piVar2 = (int *)0x0;
      }
    }
LAB_0015cef4:
    *param_5 = piVar2;
  }
  puVar8 = *(undefined4 **)(iVar12 + 0x50);
  if (puVar8 != (undefined4 *)0x0) {
    piVar2 = (int *)*puVar8;
    iVar3 = *piVar2;
    puVar6 = puVar8;
    piVar4 = piVar2;
    iVar12 = iVar3;
    while (iVar12 != iVar9) {
      puVar6 = (undefined4 *)puVar6[2];
      if (puVar6 == (undefined4 *)0x0) {
        piVar4 = (int *)0x0;
        break;
      }
      piVar4 = (int *)*puVar6;
      iVar12 = *piVar4;
    }
    do {
      if (iVar10 == iVar3) goto LAB_0015cf74;
      puVar8 = (undefined4 *)puVar8[2];
      if (puVar8 == (undefined4 *)0x0) {
        piVar2 = (int *)0x0;
        goto LAB_0015cf74;
      }
      piVar2 = (int *)*puVar8;
      iVar3 = *piVar2;
    } while( true );
  }
  piVar2 = (int *)0x0;
  piVar4 = (int *)0x0;
LAB_0015cf74:
  local_50 = (float)param_1[0x14];
  local_4c = (float)param_1[0x15];
  local_54 = (float)param_1[0x13];
  _ZN6glitch4core8vector3dIfE9normalizeEv(&local_54);
  local_48 = *(float *)(iVar9 + 0x50) - fVar20;
  local_44 = *(float *)(iVar9 + 0x54) - fVar22;
  local_40 = *(float *)(iVar9 + 0x58) - local_34;
  _ZN6glitch4core8vector3dIfE9normalizeEv(&local_48);
  local_3c = *(float *)(iVar10 + 0x50) - fVar20;
  local_38 = *(float *)(iVar10 + 0x54) - fVar22;
  local_34 = *(float *)(iVar10 + 0x58) - local_34;
  _ZN6glitch4core8vector3dIfE9normalizeEv(&local_3c);
  fVar22 = local_54 * local_48 + local_50 * local_44 + local_4c * local_40;
  fVar20 = local_54 * local_3c + local_50 * local_38 + local_4c * local_34;
  if (fVar22 < 0.0) {
    iVar12 = -1;
  }
  else {
    iVar12 = 1;
  }
  if (fVar20 < 0.0) {
    iVar9 = -1;
  }
  else {
    iVar9 = 1;
  }
  if (iVar12 == iVar9) {
    fVar20 = ABS(fVar20);
    if (fVar22 < 0.0) {
      if (ABS(fVar22) <= fVar20) goto LAB_0015d0c8;
    }
    else if (fVar20 < ABS(fVar22)) {
LAB_0015d0c8:
      *param_4 = piVar2;
      *param_3 = piVar4;
      goto LAB_0015d064;
    }
  }
  else if (fVar22 < 0.0) goto LAB_0015d0c8;
  *param_4 = piVar4;
  *param_3 = piVar2;
  piVar4 = piVar2;
LAB_0015d064:
  return piVar4 != (int *)0x0;
}

