// _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEfENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIN9__gnu_cxx17__normal_iteratorIPS5_SB_EEEEvSG_T_SH_St20forward_iterator_tag @ 007f8dd8

/* WARNING: Control flow encountered bad instruction data */

void _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEfENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIN9__gnu_cxx17__normal_iteratorIPS5_SB_EEEEvSG_T_SH_St20forward_iterator_tag
               (undefined4 *param_1,undefined4 *param_2,undefined4 *param_3,undefined4 *param_4)

{
  uint uVar1;
  undefined4 *puVar2;
  int *piVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined4 *extraout_r2;
  undefined4 *puVar6;
  int iVar7;
  undefined4 *extraout_r3;
  undefined4 *puVar8;
  uint uVar9;
  undefined4 *puVar10;
  undefined4 *puVar11;
  int iVar12;
  undefined4 *puVar13;
  undefined8 uVar14;
  
  if (param_3 == param_4) {
    return;
  }
  puVar8 = (undefined4 *)param_1[1];
  uVar9 = (int)param_4 - (int)param_3 >> 3;
  if (uVar9 <= (uint)(param_1[2] - (int)puVar8 >> 3)) {
    uVar1 = (int)puVar8 - (int)param_2 >> 3;
    if (uVar1 <= uVar9) {
      puVar2 = puVar8;
      for (puVar13 = param_3 + uVar1 * 2; param_4 != puVar13; puVar13 = puVar13 + 2) {
        if (puVar2 != (undefined4 *)0x0) {
          uVar5 = puVar13[1];
          *puVar2 = *puVar13;
          puVar2[1] = uVar5;
        }
        puVar2 = puVar2 + 2;
      }
      puVar6 = puVar8 + (uVar9 - uVar1) * 2;
      param_1[1] = puVar6;
      puVar2 = puVar6;
      for (puVar13 = param_2; puVar8 != puVar13; puVar13 = puVar13 + 2) {
        if (puVar2 != (undefined4 *)0x0) {
          uVar5 = puVar13[1];
          *puVar2 = *puVar13;
          puVar2[1] = uVar5;
        }
        puVar2 = puVar2 + 2;
      }
      param_1[1] = puVar6 + uVar1 * 2;
      iVar12 = (int)(param_3 + uVar1 * 2) - (int)param_3 >> 3;
      if (iVar12 < 1) {
        return;
      }
      iVar7 = 0;
      do {
        puVar8 = (undefined4 *)((int)param_3 + iVar7);
        puVar13 = (undefined4 *)((int)param_2 + iVar7);
        iVar12 = iVar12 + -1;
        iVar7 = iVar7 + 8;
        uVar5 = puVar8[1];
        *puVar13 = *puVar8;
        puVar13[1] = uVar5;
      } while (iVar12 != 0);
      return;
    }
    puVar6 = puVar8 + uVar9 * -2;
    puVar2 = puVar8;
    for (puVar13 = puVar6; puVar8 != puVar13; puVar13 = puVar13 + 2) {
      if (puVar2 != (undefined4 *)0x0) {
        uVar5 = puVar13[1];
        *puVar2 = *puVar13;
        puVar2[1] = uVar5;
      }
      puVar2 = puVar2 + 2;
    }
    param_1[1] = puVar8 + uVar9 * 2;
    iVar12 = (int)puVar6 - (int)param_2 >> 3;
    if (0 < iVar12) {
      do {
        iVar12 = iVar12 + -1;
        uVar5 = puVar6[-1];
        puVar8[-2] = puVar6[-2];
        puVar8[-1] = uVar5;
        puVar6 = puVar6 + -2;
        puVar8 = puVar8 + -2;
      } while (iVar12 != 0);
    }
    if ((int)uVar9 < 1) {
      return;
    }
    iVar12 = 0;
    do {
      puVar8 = (undefined4 *)((int)param_3 + iVar12);
      puVar13 = (undefined4 *)((int)param_2 + iVar12);
      uVar9 = uVar9 - 1;
      iVar12 = iVar12 + 8;
      uVar5 = puVar8[1];
      *puVar13 = *puVar8;
      puVar13[1] = uVar5;
    } while (uVar9 != 0);
    return;
  }
  puVar13 = (undefined4 *)*param_1;
  uVar1 = (int)puVar8 - (int)puVar13 >> 3;
  if (0x1fffffff - uVar1 < uVar9) {
    uVar14 = _ZSt20__throw_length_errorPKc((int)&DAT_007f90c0 + DAT_007f90c0);
    puVar8 = (undefined4 *)((ulonglong)uVar14 >> 0x20);
    piVar3 = (int *)uVar14;
    if (extraout_r2 != (undefined4 *)0x0) {
      puVar13 = (undefined4 *)piVar3[1];
      if ((undefined4 *)(piVar3[2] - (int)puVar13 >> 2) < extraout_r2) {
        iVar12 = *piVar3;
        puVar2 = (undefined4 *)0x3fffffff;
        puVar13 = (undefined4 *)((int)puVar13 - iVar12 >> 2);
        if ((undefined4 *)(0x3fffffff - (int)puVar13) < extraout_r2) {
          _ZSt20__throw_length_errorPKc((int)&DAT_007f935c + DAT_007f935c);
                    /* WARNING: Bad instruction - Truncating control flow here */
          halt_baddata();
        }
        if (puVar13 < extraout_r2) {
          puVar6 = (undefined4 *)((int)puVar13 + (int)extraout_r2);
        }
        else {
          puVar6 = (undefined4 *)((int)puVar13 * 2);
        }
        if (puVar6 < puVar13) {
          iVar7 = -4;
        }
        else {
          if (puVar6 < (undefined4 *)0x3fffffff) {
            puVar2 = puVar6;
          }
          iVar7 = (int)puVar2 << 2;
        }
        puVar13 = (undefined4 *)0x0;
        if (puVar2 != (undefined4 *)0x0) {
          puVar13 = (undefined4 *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(iVar7,0);
        }
        puVar6 = puVar13 + ((int)puVar8 - iVar12 >> 2);
        puVar2 = extraout_r2;
        do {
          if (puVar6 != (undefined4 *)0x0) {
            *puVar6 = *extraout_r3;
          }
          puVar2 = (undefined4 *)((int)puVar2 + -1);
          puVar6 = puVar6 + 1;
        } while (puVar2 != (undefined4 *)0x0);
        puVar4 = (undefined4 *)*piVar3;
        puVar2 = puVar4;
        puVar6 = puVar13;
        if (puVar4 != puVar8) {
          do {
            if (puVar6 != (undefined4 *)0x0) {
              *puVar6 = *puVar2;
            }
            puVar2 = puVar2 + 1;
            puVar6 = puVar6 + 1;
          } while (puVar2 != puVar8);
          puVar6 = (undefined4 *)
                   ((int)puVar13 + ((int)puVar8 - (int)(puVar4 + 1) & 0xfffffffcU) + 4);
        }
        puVar10 = (undefined4 *)piVar3[1];
        puVar6 = puVar6 + (int)extraout_r2;
        puVar2 = puVar8;
        puVar4 = puVar6;
        if (puVar10 != puVar8) {
          do {
            if (puVar4 != (undefined4 *)0x0) {
              *puVar4 = *puVar2;
            }
            puVar2 = puVar2 + 1;
            puVar4 = puVar4 + 1;
          } while (puVar10 != puVar2);
          puVar6 = (undefined4 *)
                   ((int)puVar6 + ((int)puVar10 - (int)(puVar8 + 1) & 0xfffffffcU) + 4);
        }
        if (*piVar3 != 0) {
          _Z10GlitchFreePv();
        }
        *piVar3 = (int)puVar13;
        piVar3[1] = (int)puVar6;
        piVar3[2] = (int)puVar13 + iVar7;
      }
      else {
        uVar5 = *extraout_r3;
        puVar2 = (undefined4 *)((int)puVar13 - (int)puVar8 >> 2);
        if (extraout_r2 < puVar2) {
          puVar4 = puVar13 + -(int)extraout_r2;
          puVar2 = puVar4;
          puVar6 = puVar13;
          if (puVar13 != puVar4) {
            do {
              if (puVar6 != (undefined4 *)0x0) {
                *puVar6 = *puVar2;
              }
              puVar2 = puVar2 + 1;
              puVar6 = puVar6 + 1;
            } while (puVar13 != puVar2);
            puVar6 = (undefined4 *)piVar3[1];
          }
          piVar3[1] = (int)(puVar6 + (int)extraout_r2);
          iVar12 = (int)puVar4 - (int)puVar8 >> 2;
          if (iVar12 != 0) {
            memmove(puVar13 + -iVar12,puVar8,iVar12 * 4);
          }
          puVar13 = puVar8 + (int)extraout_r2;
          for (; puVar13 != puVar8; puVar8 = puVar8 + 1) {
            *puVar8 = uVar5;
          }
        }
        else {
          iVar7 = (int)extraout_r2 - (int)puVar2;
          iVar12 = iVar7;
          puVar6 = puVar13;
          if (iVar7 != 0) {
            do {
              if (puVar6 != (undefined4 *)0x0) {
                *puVar6 = uVar5;
              }
              iVar12 = iVar12 + -1;
              puVar6 = puVar6 + 1;
            } while (iVar12 != 0);
            puVar6 = (undefined4 *)piVar3[1];
          }
          puVar6 = puVar6 + iVar7;
          if (puVar13 == puVar8) {
            puVar2 = puVar6 + (int)puVar2;
          }
          piVar3[1] = (int)puVar6;
          puVar4 = puVar8;
          if (puVar13 == puVar8) {
            piVar3[1] = (int)puVar2;
          }
          else {
            do {
              if (puVar6 != (undefined4 *)0x0) {
                *puVar6 = *puVar4;
              }
              puVar4 = puVar4 + 1;
              puVar6 = puVar6 + 1;
            } while (puVar13 != puVar4);
            piVar3[1] = piVar3[1] + (int)puVar2 * 4;
            do {
              puVar2 = puVar8 + 1;
              *puVar8 = uVar5;
              puVar8 = puVar2;
            } while (puVar13 != puVar2);
          }
        }
      }
    }
    return;
  }
  if (uVar1 < uVar9) {
    uVar9 = uVar1 + uVar9;
  }
  else {
    uVar9 = uVar1 * 2;
  }
  if ((uVar9 < uVar1) || (0x1fffffff < uVar9)) {
    iVar12 = -8;
  }
  else {
    if (uVar9 == 0) {
      puVar2 = (undefined4 *)0x0;
      iVar12 = 0;
      goto LAB_007f8fb8;
    }
    iVar12 = uVar9 << 3;
  }
  puVar2 = (undefined4 *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(iVar12,0);
  puVar13 = (undefined4 *)*param_1;
  puVar8 = (undefined4 *)param_1[1];
LAB_007f8fb8:
  puVar4 = param_3;
  puVar6 = puVar13;
  puVar10 = puVar2;
  puVar11 = puVar2;
  if (puVar13 != param_2) {
    do {
      if (puVar10 != (undefined4 *)0x0) {
        uVar5 = puVar6[1];
        *puVar10 = *puVar6;
        puVar10[1] = uVar5;
      }
      puVar6 = puVar6 + 2;
      puVar10 = puVar10 + 2;
    } while (puVar6 != param_2);
    puVar10 = (undefined4 *)((int)puVar2 + ((int)param_2 - (int)(puVar13 + 2) & 0xfffffff8U) + 8);
    puVar11 = puVar10;
  }
  do {
    if (puVar10 != (undefined4 *)0x0) {
      uVar5 = puVar4[1];
      *puVar10 = *puVar4;
      puVar10[1] = uVar5;
    }
    puVar4 = puVar4 + 2;
    puVar10 = puVar10 + 2;
  } while (param_4 != puVar4);
  puVar11 = (undefined4 *)((int)puVar11 + ((int)param_4 - (int)(param_3 + 2) & 0xfffffff8U) + 8);
  puVar6 = param_2;
  puVar4 = puVar11;
  if (param_2 != puVar8) {
    do {
      if (puVar4 != (undefined4 *)0x0) {
        uVar5 = puVar6[1];
        *puVar4 = *puVar6;
        puVar4[1] = uVar5;
      }
      puVar6 = puVar6 + 2;
      puVar4 = puVar4 + 2;
    } while (puVar8 != puVar6);
    puVar11 = (undefined4 *)((int)puVar11 + ((int)puVar8 - (int)(param_2 + 2) & 0xfffffff8U) + 8);
  }
  if (puVar13 != (undefined4 *)0x0) {
    _Z10GlitchFreePv(puVar13);
  }
  *param_1 = puVar2;
  param_1[1] = puVar11;
  param_1[2] = (int)puVar2 + iVar12;
  return;
}


