// _ZNK6glitch10irradiance18CIrradianceManager10getVolumesERKNS_4core8vector3dIfEERSt6vectorISt4pairIPNS0_17CIrradianceVolumeEfENS2_10SAllocatorISB_LNS_6memory13E_MEMORY_HINTE0EEEE @ 007c6f98

int * _ZNK6glitch10irradiance18CIrradianceManager10getVolumesERKNS_4core8vector3dIfEERSt6vectorISt4pairIPNS0_17CIrradianceVolumeEfENS2_10SAllocatorISB_LNS_6memory13E_MEMORY_HINTE0EEEE
                (int param_1,float *param_2,int *param_3)

{
  uint uVar1;
  float fVar2;
  int *piVar3;
  int *piVar4;
  int *piVar5;
  int *piVar6;
  uint uVar7;
  int *piVar8;
  int *piVar9;
  int *piVar10;
  int iVar11;
  int *piVar12;
  float fVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  int *local_5c;
  int local_54;
  int local_44;
  float local_40;
  int local_3c;
  int *local_38;
  int *local_34;
  
  fVar2 = DAT_007c7310;
  piVar8 = *(int **)(param_1 + 0x20);
  local_3c = 0;
  local_38 = (int *)0x0;
  local_34 = (int *)0x0;
  if (*(int **)(param_1 + 0x1c) != piVar8) {
    piVar10 = *(int **)(param_1 + 0x1c);
    do {
      piVar9 = piVar10 + 1;
      iVar11 = *piVar10;
      fVar17 = *param_2;
      if ((((fVar17 < *(float *)(iVar11 + 0x18)) || (*(float *)(iVar11 + 0x24) < fVar17)) ||
          (param_2[1] < *(float *)(iVar11 + 0x1c))) ||
         (((*(float *)(iVar11 + 0x28) < param_2[1] || (param_2[2] < *(float *)(iVar11 + 0x20))) ||
          (*(float *)(iVar11 + 0x2c) < param_2[2])))) {
        if ((*(byte *)(param_1 + 0x14) & 8) != 0) {
          fVar16 = *(float *)(iVar11 + 0x18) - fVar17;
          fVar17 = fVar17 - *(float *)(iVar11 + 0x24);
          fVar13 = *(float *)(iVar11 + 0x1c) - param_2[1];
          fVar14 = param_2[1] - *(float *)(iVar11 + 0x28);
          if (fVar16 < fVar17) {
            fVar16 = fVar17;
          }
          if (fVar16 < 0.0) {
            fVar16 = fVar2;
          }
          fVar15 = *(float *)(iVar11 + 0x20) - param_2[2];
          fVar17 = param_2[2] - *(float *)(iVar11 + 0x2c);
          if (fVar14 <= fVar13) {
            fVar14 = fVar13;
          }
          if (fVar14 < 0.0) {
            fVar14 = fVar2;
          }
          if (fVar17 <= fVar15) {
            fVar17 = fVar15;
          }
          fVar13 = DAT_007c7310;
          if (0.0 < fVar17) {
            fVar13 = fVar17 * fVar17;
          }
          fVar17 = SQRT(fVar16 * fVar16 + fVar14 * fVar14 + fVar13);
          if (fVar17 <= *(float *)(iVar11 + 0x48)) {
            local_44 = iVar11;
            local_40 = fVar17;
            if (local_38 == local_34) {
              _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEfENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE9push_backERKS5__part_772_constprop_1306
                        (&local_3c,&local_44);
            }
            else {
              if (local_38 != (int *)0x0) {
                *local_38 = iVar11;
                local_38[1] = (int)fVar17;
              }
              local_38 = local_38 + 2;
            }
          }
        }
      }
      else {
        piVar10 = (int *)param_3[1];
        if (piVar10 == (int *)param_3[2]) {
          uVar1 = (int)piVar10 - *param_3 >> 3;
          if (uVar1 == 0) {
            local_54 = 8;
          }
          else {
            uVar7 = uVar1 * 2;
            if (uVar7 < uVar1) {
              local_54 = -8;
            }
            else {
              if (0x1ffffffe < uVar7) {
                uVar7 = 0x1fffffff;
              }
              local_54 = uVar7 << 3;
            }
          }
          piVar3 = (int *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(local_54,0);
          piVar4 = (int *)*param_3;
          piVar12 = (int *)param_3[1];
          if (piVar3 + uVar1 * 2 != (int *)0x0) {
            piVar3[uVar1 * 2] = iVar11;
            (piVar3 + uVar1 * 2)[1] = (int)fVar2;
          }
          local_5c = piVar3 + 2;
          piVar5 = piVar3;
          piVar6 = piVar4;
          if (piVar10 != piVar4) {
            do {
              if (piVar5 != (int *)0x0) {
                iVar11 = piVar6[1];
                *piVar5 = *piVar6;
                piVar5[1] = iVar11;
              }
              piVar6 = piVar6 + 2;
              piVar5 = piVar5 + 2;
            } while (piVar10 != piVar6);
            local_5c = (int *)((int)piVar3 + ((int)piVar10 - (int)(piVar4 + 2) & 0xfffffff8U) + 0x10
                              );
          }
          piVar5 = local_5c;
          piVar6 = piVar10;
          if (piVar10 != piVar12) {
            do {
              if (piVar5 != (int *)0x0) {
                iVar11 = piVar6[1];
                *piVar5 = *piVar6;
                piVar5[1] = iVar11;
              }
              piVar6 = piVar6 + 2;
              piVar5 = piVar5 + 2;
            } while (piVar12 != piVar6);
            local_5c = (int *)((int)local_5c + ((int)piVar12 - (int)(piVar10 + 2) & 0xfffffff8U) + 8
                              );
          }
          if (piVar4 != (int *)0x0) {
            _Z10GlitchFreePv(piVar4);
          }
          *param_3 = (int)piVar3;
          param_3[1] = (int)local_5c;
          param_3[2] = (int)piVar3 + local_54;
        }
        else {
          if (piVar10 != (int *)0x0) {
            *piVar10 = iVar11;
            piVar10[1] = (int)fVar2;
          }
          param_3[1] = (int)(piVar10 + 2);
        }
      }
      piVar10 = piVar9;
    } while (piVar8 != piVar9);
  }
  if (*param_3 == param_3[1]) {
    _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEfENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIN9__gnu_cxx17__normal_iteratorIPS5_SB_EEEEvSG_T_SH_St20forward_iterator_tag
              (param_3,*param_3,local_3c,local_38,0);
  }
  if (local_3c != 0) {
    _Z10GlitchFreePv();
  }
  return param_3;
}


