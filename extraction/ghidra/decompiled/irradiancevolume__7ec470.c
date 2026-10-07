// _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEbENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS5_SB_EERKS5_.constprop.1285 @ 007ec470

void _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEbENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS5_SB_EERKS5__constprop_1285
               (undefined4 *param_1,int *param_2,int *param_3)

{
  uint uVar1;
  undefined4 *puVar2;
  int *piVar3;
  int *piVar4;
  int *piVar5;
  int *piVar6;
  int iVar7;
  uint uVar8;
  int *piVar9;
  int iVar10;
  int *piVar11;
  bool bVar12;
  int local_28;
  int iStack_24;
  
  piVar5 = (int *)param_1[1];
  piVar3 = (int *)param_1[2];
  if (piVar5 == piVar3) {
    piVar3 = (int *)*param_1;
    uVar8 = (int)piVar5 - (int)piVar3 >> 3;
    if (uVar8 == 0) {
      iVar7 = 8;
      uVar8 = 1;
    }
    else {
      uVar1 = uVar8 * 2;
      if (uVar1 < uVar8) {
        iVar7 = -8;
        uVar8 = 0x1fffffff;
      }
      else {
        uVar8 = 0x1fffffff;
        if (uVar1 < 0x1fffffff) {
          uVar8 = uVar1;
        }
        iVar7 = uVar8 << 3;
      }
    }
    iVar10 = (int)param_2 - (int)piVar3;
    if (uVar8 == 0) {
      piVar9 = (int *)&DAT_00000008;
      piVar6 = (int *)0x0;
    }
    else {
      piVar6 = (int *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(iVar7,0);
      piVar3 = (int *)*param_1;
      piVar5 = (int *)param_1[1];
      piVar9 = piVar6 + 2;
    }
    piVar11 = piVar6 + (iVar10 >> 3) * 2;
    if (piVar11 != (int *)0x0) {
      iVar10 = param_3[1];
      *piVar11 = *param_3;
      piVar11[1] = iVar10;
    }
    piVar4 = piVar6;
    piVar11 = piVar3;
    if (param_2 != piVar3) {
      do {
        if (piVar4 != (int *)0x0) {
          iVar10 = piVar11[1];
          *piVar4 = *piVar11;
          piVar4[1] = iVar10;
        }
        piVar11 = piVar11 + 2;
        piVar4 = piVar4 + 2;
      } while (param_2 != piVar11);
      piVar9 = (int *)((int)piVar6 + ((int)param_2 - (int)(piVar3 + 2) & 0xfffffff8U) + 0x10);
    }
    piVar4 = piVar9;
    piVar11 = param_2;
    if (param_2 != piVar5) {
      do {
        if (piVar4 != (int *)0x0) {
          iVar10 = piVar11[1];
          *piVar4 = *piVar11;
          piVar4[1] = iVar10;
        }
        piVar11 = piVar11 + 2;
        piVar4 = piVar4 + 2;
      } while (piVar5 != piVar11);
      piVar9 = (int *)((int)piVar9 + ((int)piVar5 - (int)(param_2 + 2) & 0xfffffff8U) + 8);
    }
    if (piVar3 != (int *)0x0) {
      _Z10GlitchFreePv(piVar3);
    }
    *param_1 = piVar6;
    param_1[1] = piVar9;
    param_1[2] = (int)piVar6 + iVar7;
  }
  else {
    bVar12 = piVar5 != (int *)0x0;
    if (bVar12) {
      piVar6 = piVar5 + -2;
    }
    else {
      piVar6 = (int *)&DAT_fffffff8;
    }
    puVar2 = param_1;
    if (bVar12) {
      puVar2 = (undefined4 *)*piVar6;
      piVar3 = (int *)piVar6[1];
    }
    iVar7 = (int)piVar6 - (int)param_2 >> 3;
    if (bVar12) {
      *piVar5 = (int)puVar2;
      piVar5[1] = (int)piVar3;
    }
    local_28 = *param_3;
    iStack_24 = param_3[1];
    param_1[1] = piVar5 + 2;
    piVar3 = piVar6;
    if (0 < iVar7) {
      do {
        piVar6 = piVar6 + -2;
        memcpy(piVar3,piVar6,5);
        iVar7 = iVar7 + -1;
        piVar3 = piVar3 + -2;
      } while (iVar7 != 0);
    }
    memcpy(param_2,&local_28,5);
  }
  return;
}


