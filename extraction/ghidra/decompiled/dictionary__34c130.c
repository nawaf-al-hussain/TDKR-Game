// _ZN13CMemoryStream13GetDictionaryERSt6vectorISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESaIS9_EERS0_ISbIwS1_IwENS5_IwLS7_0EEEESaISF_EERb @ 0034c130

void _ZN13CMemoryStream13GetDictionaryERSt6vectorISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESaIS9_EERS0_ISbIwS1_IwENS5_IwLS7_0EEEESaISF_EERb
               (int param_1,int *param_2,int *param_3,undefined1 *param_4)

{
  uint uVar1;
  bool bVar2;
  int iVar3;
  int iVar4;
  int *piVar5;
  int iVar6;
  int *piVar7;
  int iVar8;
  int iVar9;
  uint uVar10;
  int iVar11;
  int iVar12;
  int *piVar13;
  int iVar14;
  int iVar15;
  int *piVar16;
  int local_30;
  int local_2c [2];
  
  iVar8 = param_2[1];
  iVar9 = DAT_0034c4ec + 0x34c160;
  iVar15 = *param_2;
  for (iVar12 = iVar15; iVar12 != iVar8; iVar12 = iVar12 + 4) {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (iVar12);
  }
  piVar5 = (int *)*param_3;
  piVar13 = (int *)param_3[1];
  param_2[1] = iVar15;
  if (piVar5 == piVar13) {
    iVar12 = *(int *)(iVar9 + DAT_0034c4f0);
  }
  else {
    iVar12 = *(int *)(iVar9 + DAT_0034c4f0);
    piVar16 = piVar5;
    do {
      piVar7 = piVar16 + 1;
      if (*piVar16 + -0xc != iVar12) {
        piVar16 = (int *)(*piVar16 + -4);
        DataMemoryBarrier(0xf);
        do {
          iVar8 = *piVar16;
          bVar2 = (bool)hasExclusiveAccess(piVar16);
        } while (!bVar2);
        *piVar16 = iVar8 + -1;
        DataMemoryBarrier(0xf);
        if (iVar8 < 1) {
          _Z10GlitchFreePv();
        }
      }
      piVar16 = piVar7;
    } while (piVar13 != piVar7);
    iVar15 = param_2[1];
  }
  iVar4 = *(int *)(param_1 + 0x1c);
  iVar8 = *(int *)(param_1 + 0x20);
  iVar14 = *param_2;
  param_3[1] = (int)piVar5;
  uVar10 = iVar8 - iVar4 >> 2;
  uVar1 = iVar15 - iVar14 >> 2;
  local_30 = *(int *)(iVar9 + DAT_0034c4f4) + 0xc;
  if (uVar1 < uVar10) {
    _ZNSt6vectorISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESaIS8_EE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPS8_SA_EEjRKS8__constprop_3185
              (param_2,iVar15,uVar10 - uVar1,&local_30);
  }
  else if (uVar10 < uVar1) {
    iVar14 = iVar14 + uVar10 * 4;
    for (iVar8 = iVar14; iVar8 != iVar15; iVar8 = iVar8 + 4) {
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar8);
    }
    param_2[1] = iVar14;
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_30);
  local_2c[0] = iVar12 + 0xc;
  piVar5 = (int *)param_3[1];
  uVar10 = *(int *)(param_1 + 0x2c) - *(int *)(param_1 + 0x28) >> 2;
  uVar1 = (int)piVar5 - *param_3 >> 2;
  if (uVar1 < uVar10) {
    _ZNSt6vectorISbIwSt11char_traitsIwEN6glitch4core10SAllocatorIwLNS2_6memory13E_MEMORY_HINTE0EEEESaIS8_EE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPS8_SA_EEjRKS8__constprop_3187
              (param_3,piVar5,uVar10 - uVar1,local_2c);
  }
  else if (uVar10 < uVar1) {
    piVar16 = (int *)(*param_3 + uVar10 * 4);
    piVar13 = piVar16;
    while (piVar5 != piVar13) {
      piVar7 = piVar13 + 1;
      iVar8 = *piVar13;
      piVar13 = piVar7;
      if (iVar8 + -0xc != iVar12) {
        piVar7 = (int *)(iVar8 + -4);
        DataMemoryBarrier(0xf);
        do {
          iVar8 = *piVar7;
          bVar2 = (bool)hasExclusiveAccess(piVar7);
        } while (!bVar2);
        *piVar7 = iVar8 + -1;
        DataMemoryBarrier(0xf);
        if (iVar8 < 1) {
          _Z10GlitchFreePv();
        }
      }
    }
    param_3[1] = (int)piVar16;
  }
  if (local_2c[0] + -0xc != iVar12) {
    piVar5 = (int *)(local_2c[0] + -4);
    DataMemoryBarrier(0xf);
    do {
      iVar8 = *piVar5;
      bVar2 = (bool)hasExclusiveAccess(piVar5);
    } while (!bVar2);
    *piVar5 = iVar8 + -1;
    DataMemoryBarrier(0xf);
    if (iVar8 < 1) {
      _Z10GlitchFreePv(local_2c[0] + -0xc);
    }
  }
  iVar8 = *(int *)(param_1 + 0x1c);
  if ((uint)(*(int *)(param_1 + 0x20) - iVar8) >> 2 != 0) {
    uVar10 = 0;
    do {
      iVar9 = uVar10 * 4;
      uVar10 = uVar10 + 1;
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                (*param_2 + iVar9,iVar8 + iVar9);
      iVar8 = *(int *)(param_1 + 0x1c);
    } while (uVar10 < (uint)(*(int *)(param_1 + 0x20) - iVar8 >> 2));
  }
  iVar8 = *(int *)(param_1 + 0x28);
  iVar9 = *(int *)(param_1 + 0x2c);
  if ((uint)(iVar9 - iVar8) >> 2 != 0) {
    uVar10 = 0;
    do {
      iVar11 = *param_3;
      iVar15 = uVar10 * 4;
      iVar14 = *(int *)(iVar8 + uVar10 * 4);
      iVar3 = *(int *)(iVar11 + uVar10 * 4);
      iVar4 = iVar14 + -0xc;
      iVar6 = iVar3 + -0xc;
      if (iVar4 != iVar6) {
        if (*(int *)(iVar14 + -4) < 0) {
          iVar14 = _ZNSbIwSt11char_traitsIwEN6glitch4core10SAllocatorIwLNS1_6memory13E_MEMORY_HINTE0EEEE4_Rep8_M_cloneERKS6_j_isra_1598
                             (iVar4,0);
          iVar3 = *(int *)(iVar11 + iVar15);
          iVar6 = iVar3 + -0xc;
        }
        else if (iVar4 != iVar12) {
          piVar5 = (int *)(iVar14 + -4);
          DataMemoryBarrier(0xf);
          do {
            bVar2 = (bool)hasExclusiveAccess(piVar5);
          } while (!bVar2);
          *piVar5 = *piVar5 + 1;
          DataMemoryBarrier(0xf);
          iVar3 = *(int *)(iVar11 + iVar15);
          iVar6 = iVar3 + -0xc;
        }
        if (iVar6 != iVar12) {
          piVar5 = (int *)(iVar3 + -4);
          DataMemoryBarrier(0xf);
          do {
            iVar8 = *piVar5;
            bVar2 = (bool)hasExclusiveAccess(piVar5);
          } while (!bVar2);
          *piVar5 = iVar8 + -1;
          DataMemoryBarrier(0xf);
          if (iVar8 < 1) {
            _Z10GlitchFreePv(iVar6);
          }
        }
        iVar9 = *(int *)(param_1 + 0x2c);
        iVar8 = *(int *)(param_1 + 0x28);
        *(int *)(iVar11 + iVar15) = iVar14;
      }
      uVar10 = uVar10 + 1;
    } while (uVar10 < (uint)(iVar9 - iVar8 >> 2));
  }
  *param_4 = *(undefined1 *)(param_1 + 0x35);
  return;
}


