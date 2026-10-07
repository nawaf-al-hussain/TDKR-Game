// _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEbENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIN9__gnu_cxx17__normal_iteratorIPS5_SB_EEEEvSG_T_SH_St20forward_iterator_tag @ 007f8ae8

/* WARNING: Control flow encountered bad instruction data */

void _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEbENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIN9__gnu_cxx17__normal_iteratorIPS5_SB_EEEEvSG_T_SH_St20forward_iterator_tag
               (undefined4 *param_1,undefined4 *param_2,undefined4 *param_3,undefined4 *param_4)

{
  uint uVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  int *piVar4;
  undefined4 uVar5;
  undefined4 *extraout_r2;
  undefined4 *extraout_r2_00;
  undefined4 *extraout_r3;
  int iVar6;
  undefined4 *extraout_r3_00;
  undefined4 *puVar7;
  undefined4 *puVar8;
  uint uVar9;
  int iVar10;
  undefined4 *puVar11;
  undefined4 *puVar12;
  undefined4 *puVar13;
  undefined4 *puVar14;
  undefined4 *puVar15;
  undefined8 uVar16;
  
  if (param_3 == param_4) {
    return;
  }
  puVar8 = (undefined4 *)param_1[1];
  uVar9 = (int)param_4 - (int)param_3 >> 3;
  if (uVar9 <= (uint)(param_1[2] - (int)puVar8 >> 3)) {
    uVar1 = (int)puVar8 - (int)param_2 >> 3;
    if (uVar1 <= uVar9) {
      puVar2 = puVar8;
      for (puVar15 = param_3 + uVar1 * 2; param_4 != puVar15; puVar15 = puVar15 + 2) {
        if (puVar2 != (undefined4 *)0x0) {
          uVar5 = puVar15[1];
          *puVar2 = *puVar15;
          puVar2[1] = uVar5;
        }
        puVar2 = puVar2 + 2;
      }
      puVar7 = puVar8 + (uVar9 - uVar1) * 2;
      param_1[1] = puVar7;
      puVar2 = puVar7;
      for (puVar15 = param_2; puVar8 != puVar15; puVar15 = puVar15 + 2) {
        if (puVar2 != (undefined4 *)0x0) {
          uVar5 = puVar15[1];
          *puVar2 = *puVar15;
          puVar2[1] = uVar5;
        }
        puVar2 = puVar2 + 2;
      }
      param_1[1] = puVar7 + uVar1 * 2;
      iVar10 = (int)(param_3 + uVar1 * 2) - (int)param_3 >> 3;
      if (iVar10 < 1) {
        return;
      }
      do {
        memcpy(param_2,param_3,5);
        iVar10 = iVar10 + -1;
        param_3 = param_3 + 2;
        param_2 = param_2 + 2;
      } while (iVar10 != 0);
      return;
    }
    puVar7 = puVar8 + uVar9 * -2;
    puVar2 = puVar8;
    for (puVar15 = puVar7; puVar8 != puVar15; puVar15 = puVar15 + 2) {
      if (puVar2 != (undefined4 *)0x0) {
        uVar5 = puVar15[1];
        *puVar2 = *puVar15;
        puVar2[1] = uVar5;
      }
      puVar2 = puVar2 + 2;
    }
    param_1[1] = puVar8 + uVar9 * 2;
    iVar10 = (int)puVar7 - (int)param_2 >> 3;
    if (0 < iVar10) {
      do {
        puVar8 = puVar8 + -2;
        puVar7 = puVar7 + -2;
        memcpy(puVar8,puVar7,5);
        iVar10 = iVar10 + -1;
      } while (iVar10 != 0);
    }
    if ((int)uVar9 < 1) {
      return;
    }
    do {
      memcpy(param_2,param_3,5);
      uVar9 = uVar9 - 1;
      param_2 = param_2 + 2;
      param_3 = param_3 + 2;
    } while (uVar9 != 0);
    return;
  }
  puVar15 = (undefined4 *)*param_1;
  uVar1 = (int)puVar8 - (int)puVar15 >> 3;
  if (0x1fffffff - uVar1 < uVar9) {
    uVar16 = _ZSt20__throw_length_errorPKc((int)&DAT_007f8dd4 + DAT_007f8dd4);
    puVar15 = (undefined4 *)((ulonglong)uVar16 >> 0x20);
    puVar8 = (undefined4 *)uVar16;
    if (extraout_r2 == extraout_r3) {
      return;
    }
    puVar2 = (undefined4 *)puVar8[1];
    uVar9 = (int)extraout_r3 - (int)extraout_r2 >> 3;
    if (uVar9 <= (uint)(puVar8[2] - (int)puVar2 >> 3)) {
      uVar1 = (int)puVar2 - (int)puVar15 >> 3;
      if (uVar9 < uVar1) {
        puVar11 = puVar2 + uVar9 * -2;
        puVar3 = puVar2;
        for (puVar7 = puVar11; puVar2 != puVar7; puVar7 = puVar7 + 2) {
          if (puVar3 != (undefined4 *)0x0) {
            uVar5 = puVar7[1];
            *puVar3 = *puVar7;
            puVar3[1] = uVar5;
          }
          puVar3 = puVar3 + 2;
        }
        puVar8[1] = puVar2 + uVar9 * 2;
        iVar10 = (int)puVar11 - (int)puVar15 >> 3;
        if (0 < iVar10) {
          do {
            iVar10 = iVar10 + -1;
            uVar5 = puVar11[-1];
            puVar2[-2] = puVar11[-2];
            puVar2[-1] = uVar5;
            puVar11 = puVar11 + -2;
            puVar2 = puVar2 + -2;
          } while (iVar10 != 0);
        }
        if ((int)uVar9 < 1) {
          return;
        }
        iVar10 = 0;
        do {
          puVar8 = (undefined4 *)((int)extraout_r2 + iVar10);
          puVar2 = (undefined4 *)((int)puVar15 + iVar10);
          uVar9 = uVar9 - 1;
          iVar10 = iVar10 + 8;
          uVar5 = puVar8[1];
          *puVar2 = *puVar8;
          puVar2[1] = uVar5;
        } while (uVar9 != 0);
        return;
      }
      puVar3 = puVar2;
      for (puVar7 = extraout_r2 + uVar1 * 2; extraout_r3 != puVar7; puVar7 = puVar7 + 2) {
        if (puVar3 != (undefined4 *)0x0) {
          uVar5 = puVar7[1];
          *puVar3 = *puVar7;
          puVar3[1] = uVar5;
        }
        puVar3 = puVar3 + 2;
      }
      puVar11 = puVar2 + (uVar9 - uVar1) * 2;
      puVar8[1] = puVar11;
      puVar3 = puVar11;
      for (puVar7 = puVar15; puVar2 != puVar7; puVar7 = puVar7 + 2) {
        if (puVar3 != (undefined4 *)0x0) {
          uVar5 = puVar7[1];
          *puVar3 = *puVar7;
          puVar3[1] = uVar5;
        }
        puVar3 = puVar3 + 2;
      }
      puVar8[1] = puVar11 + uVar1 * 2;
      iVar10 = (int)(extraout_r2 + uVar1 * 2) - (int)extraout_r2 >> 3;
      if (iVar10 < 1) {
        return;
      }
      iVar6 = 0;
      do {
        puVar8 = (undefined4 *)((int)extraout_r2 + iVar6);
        puVar2 = (undefined4 *)((int)puVar15 + iVar6);
        iVar10 = iVar10 + -1;
        iVar6 = iVar6 + 8;
        uVar5 = puVar8[1];
        *puVar2 = *puVar8;
        puVar2[1] = uVar5;
      } while (iVar10 != 0);
      return;
    }
    puVar7 = (undefined4 *)*puVar8;
    uVar1 = (int)puVar2 - (int)puVar7 >> 3;
    if (0x1fffffff - uVar1 < uVar9) {
      uVar16 = _ZSt20__throw_length_errorPKc((int)&DAT_007f90c0 + DAT_007f90c0);
      puVar8 = (undefined4 *)((ulonglong)uVar16 >> 0x20);
      piVar4 = (int *)uVar16;
      if (extraout_r2_00 != (undefined4 *)0x0) {
        puVar15 = (undefined4 *)piVar4[1];
        if ((undefined4 *)(piVar4[2] - (int)puVar15 >> 2) < extraout_r2_00) {
          iVar10 = *piVar4;
          puVar2 = (undefined4 *)0x3fffffff;
          puVar15 = (undefined4 *)((int)puVar15 - iVar10 >> 2);
          if ((undefined4 *)(0x3fffffff - (int)puVar15) < extraout_r2_00) {
            _ZSt20__throw_length_errorPKc((int)&DAT_007f935c + DAT_007f935c);
                    /* WARNING: Bad instruction - Truncating control flow here */
            halt_baddata();
          }
          if (puVar15 < extraout_r2_00) {
            puVar7 = (undefined4 *)((int)puVar15 + (int)extraout_r2_00);
          }
          else {
            puVar7 = (undefined4 *)((int)puVar15 * 2);
          }
          if (puVar7 < puVar15) {
            iVar6 = -4;
          }
          else {
            if (puVar7 < (undefined4 *)0x3fffffff) {
              puVar2 = puVar7;
            }
            iVar6 = (int)puVar2 << 2;
          }
          puVar15 = (undefined4 *)0x0;
          if (puVar2 != (undefined4 *)0x0) {
            puVar15 = (undefined4 *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(iVar6,0);
          }
          puVar7 = puVar15 + ((int)puVar8 - iVar10 >> 2);
          puVar2 = extraout_r2_00;
          do {
            if (puVar7 != (undefined4 *)0x0) {
              *puVar7 = *extraout_r3_00;
            }
            puVar2 = (undefined4 *)((int)puVar2 + -1);
            puVar7 = puVar7 + 1;
          } while (puVar2 != (undefined4 *)0x0);
          puVar3 = (undefined4 *)*piVar4;
          puVar2 = puVar3;
          puVar7 = puVar15;
          if (puVar3 != puVar8) {
            do {
              if (puVar7 != (undefined4 *)0x0) {
                *puVar7 = *puVar2;
              }
              puVar2 = puVar2 + 1;
              puVar7 = puVar7 + 1;
            } while (puVar2 != puVar8);
            puVar7 = (undefined4 *)
                     ((int)puVar15 + ((int)puVar8 - (int)(puVar3 + 1) & 0xfffffffcU) + 4);
          }
          puVar11 = (undefined4 *)piVar4[1];
          puVar7 = puVar7 + (int)extraout_r2_00;
          puVar2 = puVar8;
          puVar3 = puVar7;
          if (puVar11 != puVar8) {
            do {
              if (puVar3 != (undefined4 *)0x0) {
                *puVar3 = *puVar2;
              }
              puVar2 = puVar2 + 1;
              puVar3 = puVar3 + 1;
            } while (puVar11 != puVar2);
            puVar7 = (undefined4 *)
                     ((int)puVar7 + ((int)puVar11 - (int)(puVar8 + 1) & 0xfffffffcU) + 4);
          }
          if (*piVar4 != 0) {
            _Z10GlitchFreePv();
          }
          *piVar4 = (int)puVar15;
          piVar4[1] = (int)puVar7;
          piVar4[2] = (int)puVar15 + iVar6;
        }
        else {
          uVar5 = *extraout_r3_00;
          puVar2 = (undefined4 *)((int)puVar15 - (int)puVar8 >> 2);
          if (extraout_r2_00 < puVar2) {
            puVar3 = puVar15 + -(int)extraout_r2_00;
            puVar2 = puVar3;
            puVar7 = puVar15;
            if (puVar15 != puVar3) {
              do {
                if (puVar7 != (undefined4 *)0x0) {
                  *puVar7 = *puVar2;
                }
                puVar2 = puVar2 + 1;
                puVar7 = puVar7 + 1;
              } while (puVar15 != puVar2);
              puVar7 = (undefined4 *)piVar4[1];
            }
            piVar4[1] = (int)(puVar7 + (int)extraout_r2_00);
            iVar10 = (int)puVar3 - (int)puVar8 >> 2;
            if (iVar10 != 0) {
              memmove(puVar15 + -iVar10,puVar8,iVar10 * 4);
            }
            puVar15 = puVar8 + (int)extraout_r2_00;
            for (; puVar15 != puVar8; puVar8 = puVar8 + 1) {
              *puVar8 = uVar5;
            }
          }
          else {
            iVar6 = (int)extraout_r2_00 - (int)puVar2;
            iVar10 = iVar6;
            puVar7 = puVar15;
            if (iVar6 != 0) {
              do {
                if (puVar7 != (undefined4 *)0x0) {
                  *puVar7 = uVar5;
                }
                iVar10 = iVar10 + -1;
                puVar7 = puVar7 + 1;
              } while (iVar10 != 0);
              puVar7 = (undefined4 *)piVar4[1];
            }
            puVar7 = puVar7 + iVar6;
            if (puVar15 == puVar8) {
              puVar2 = puVar7 + (int)puVar2;
            }
            piVar4[1] = (int)puVar7;
            puVar3 = puVar8;
            if (puVar15 == puVar8) {
              piVar4[1] = (int)puVar2;
            }
            else {
              do {
                if (puVar7 != (undefined4 *)0x0) {
                  *puVar7 = *puVar3;
                }
                puVar3 = puVar3 + 1;
                puVar7 = puVar7 + 1;
              } while (puVar15 != puVar3);
              piVar4[1] = piVar4[1] + (int)puVar2 * 4;
              do {
                puVar2 = puVar8 + 1;
                *puVar8 = uVar5;
                puVar8 = puVar2;
              } while (puVar15 != puVar2);
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
      iVar10 = -8;
    }
    else {
      if (uVar9 == 0) {
        puVar3 = (undefined4 *)0x0;
        iVar10 = 0;
        goto LAB_007f8fb8;
      }
      iVar10 = uVar9 << 3;
    }
    puVar3 = (undefined4 *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(iVar10,0);
    puVar7 = (undefined4 *)*puVar8;
    puVar2 = (undefined4 *)puVar8[1];
LAB_007f8fb8:
    puVar12 = extraout_r2;
    puVar11 = puVar7;
    puVar13 = puVar3;
    puVar14 = puVar3;
    if (puVar7 != puVar15) {
      do {
        if (puVar13 != (undefined4 *)0x0) {
          uVar5 = puVar11[1];
          *puVar13 = *puVar11;
          puVar13[1] = uVar5;
        }
        puVar11 = puVar11 + 2;
        puVar13 = puVar13 + 2;
      } while (puVar11 != puVar15);
      puVar13 = (undefined4 *)((int)puVar3 + ((int)puVar15 - (int)(puVar7 + 2) & 0xfffffff8U) + 8);
      puVar14 = puVar13;
    }
    do {
      if (puVar13 != (undefined4 *)0x0) {
        uVar5 = puVar12[1];
        *puVar13 = *puVar12;
        puVar13[1] = uVar5;
      }
      puVar12 = puVar12 + 2;
      puVar13 = puVar13 + 2;
    } while (extraout_r3 != puVar12);
    puVar14 = (undefined4 *)
              ((int)puVar14 + ((int)extraout_r3 - (int)(extraout_r2 + 2) & 0xfffffff8U) + 8);
    puVar11 = puVar15;
    puVar12 = puVar14;
    if (puVar15 != puVar2) {
      do {
        if (puVar12 != (undefined4 *)0x0) {
          uVar5 = puVar11[1];
          *puVar12 = *puVar11;
          puVar12[1] = uVar5;
        }
        puVar11 = puVar11 + 2;
        puVar12 = puVar12 + 2;
      } while (puVar2 != puVar11);
      puVar14 = (undefined4 *)((int)puVar14 + ((int)puVar2 - (int)(puVar15 + 2) & 0xfffffff8U) + 8);
    }
    if (puVar7 != (undefined4 *)0x0) {
      _Z10GlitchFreePv(puVar7);
    }
    *puVar8 = puVar3;
    puVar8[1] = puVar14;
    puVar8[2] = (int)puVar3 + iVar10;
    return;
  }
  if (uVar1 < uVar9) {
    uVar9 = uVar1 + uVar9;
  }
  else {
    uVar9 = uVar1 * 2;
  }
  if ((uVar9 < uVar1) || (0x1fffffff < uVar9)) {
    iVar10 = -8;
  }
  else {
    if (uVar9 == 0) {
      puVar2 = (undefined4 *)0x0;
      iVar10 = 0;
      goto LAB_007f8ccc;
    }
    iVar10 = uVar9 << 3;
  }
  puVar2 = (undefined4 *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(iVar10,0);
  puVar15 = (undefined4 *)*param_1;
  puVar8 = (undefined4 *)param_1[1];
LAB_007f8ccc:
  puVar11 = puVar2;
  puVar3 = param_3;
  puVar7 = puVar15;
  puVar12 = puVar2;
  if (puVar15 != param_2) {
    do {
      if (puVar11 != (undefined4 *)0x0) {
        uVar5 = puVar7[1];
        *puVar11 = *puVar7;
        puVar11[1] = uVar5;
      }
      puVar7 = puVar7 + 2;
      puVar11 = puVar11 + 2;
    } while (puVar7 != param_2);
    puVar11 = (undefined4 *)((int)puVar2 + ((int)param_2 - (int)(puVar15 + 2) & 0xfffffff8U) + 8);
    puVar12 = puVar11;
  }
  do {
    if (puVar11 != (undefined4 *)0x0) {
      uVar5 = puVar3[1];
      *puVar11 = *puVar3;
      puVar11[1] = uVar5;
    }
    puVar3 = puVar3 + 2;
    puVar11 = puVar11 + 2;
  } while (param_4 != puVar3);
  puVar12 = (undefined4 *)((int)puVar12 + ((int)param_4 - (int)(param_3 + 2) & 0xfffffff8U) + 8);
  puVar7 = param_2;
  puVar3 = puVar12;
  if (param_2 != puVar8) {
    do {
      if (puVar3 != (undefined4 *)0x0) {
        uVar5 = puVar7[1];
        *puVar3 = *puVar7;
        puVar3[1] = uVar5;
      }
      puVar7 = puVar7 + 2;
      puVar3 = puVar3 + 2;
    } while (puVar8 != puVar7);
    puVar12 = (undefined4 *)((int)puVar12 + ((int)puVar8 - (int)(param_2 + 2) & 0xfffffff8U) + 8);
  }
  if (puVar15 != (undefined4 *)0x0) {
    _Z10GlitchFreePv(puVar15);
  }
  *param_1 = puVar2;
  param_1[1] = puVar12;
  param_1[2] = (int)puVar2 + iVar10;
  return;
}


