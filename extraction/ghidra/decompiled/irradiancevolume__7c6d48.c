// _ZNK6glitch10irradiance18CIrradianceManager10getVolumesERKNS_4core8vector3dIfEERSt6vectorISt4pairIPNS0_17CIrradianceVolumeEbENS2_10SAllocatorISB_LNS_6memory13E_MEMORY_HINTE0EEEE @ 007c6d48

/* WARNING: Restarted to delay deadcode elimination for space: stack */

int _ZNK6glitch10irradiance18CIrradianceManager10getVolumesERKNS_4core8vector3dIfEERSt6vectorISt4pairIPNS0_17CIrradianceVolumeEbENS2_10SAllocatorISB_LNS_6memory13E_MEMORY_HINTE0EEEE
              (int param_1,float *param_2,int param_3,int *param_4)

{
  float fVar1;
  int iVar2;
  int *piVar3;
  int *piVar4;
  int *piVar5;
  int *piVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  int local_44;
  int local_40;
  int local_3c;
  uint local_38;
  int *local_34;
  int *local_30;
  int *local_2c;
  
  fVar1 = DAT_007c6f94;
  piVar4 = *(int **)(param_1 + 0x1c);
  piVar6 = *(int **)(param_1 + 0x20);
  local_34 = (int *)0x0;
  local_30 = (int *)0x0;
  if (piVar4 == piVar6) {
    param_4 = (int *)0x0;
  }
  local_2c = (int *)0x0;
  piVar3 = param_4;
  if (piVar4 != piVar6) {
    do {
      piVar5 = piVar4 + 1;
      iVar2 = *piVar4;
      fVar11 = *param_2;
      if ((((fVar11 < *(float *)(iVar2 + 0x18)) || (*(float *)(iVar2 + 0x24) < fVar11)) ||
          (param_2[1] < *(float *)(iVar2 + 0x1c))) ||
         (((*(float *)(iVar2 + 0x28) < param_2[1] || (param_2[2] < *(float *)(iVar2 + 0x20))) ||
          (*(float *)(iVar2 + 0x2c) < param_2[2])))) {
        if ((*(byte *)(param_1 + 0x14) & 8) != 0) {
          fVar10 = *(float *)(iVar2 + 0x18) - fVar11;
          fVar11 = fVar11 - *(float *)(iVar2 + 0x24);
          fVar7 = *(float *)(iVar2 + 0x1c) - param_2[1];
          fVar8 = param_2[1] - *(float *)(iVar2 + 0x28);
          if (fVar10 < fVar11) {
            fVar10 = fVar11;
          }
          if (fVar10 < 0.0) {
            fVar10 = fVar1;
          }
          fVar9 = *(float *)(iVar2 + 0x20) - param_2[2];
          fVar11 = param_2[2] - *(float *)(iVar2 + 0x2c);
          if (fVar8 <= fVar7) {
            fVar8 = fVar7;
          }
          if (fVar8 < 0.0) {
            fVar8 = fVar1;
          }
          if (fVar11 <= fVar9) {
            fVar11 = fVar9;
          }
          fVar7 = DAT_007c6f94;
          if (0.0 < fVar11) {
            fVar7 = fVar11 * fVar11;
          }
          if (SQRT(fVar10 * fVar10 + fVar8 * fVar8 + fVar7) <= *(float *)(iVar2 + 0x48)) {
            local_38 = local_38 & 0xffffff00;
            local_3c = iVar2;
            if (local_30 == local_2c) {
              _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEbENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS5_SB_EERKS5__constprop_1285
                        (&local_34,local_30,&local_3c);
            }
            else {
              if (local_30 != (int *)0x0) {
                *local_30 = iVar2;
                local_30[1] = local_38;
              }
              local_30 = local_30 + 2;
            }
          }
        }
      }
      else {
        piVar4 = *(int **)(param_3 + 4);
        local_40 = CONCAT31(local_40._1_3_,1);
        local_44 = iVar2;
        if (piVar4 == *(int **)(param_3 + 8)) {
          _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEbENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS5_SB_EERKS5_
                    (param_3,piVar4,&local_44);
        }
        else {
          if (piVar4 != (int *)0x0) {
            *piVar4 = iVar2;
            piVar4[1] = local_40;
          }
          *(int **)(param_3 + 4) = piVar4 + 2;
        }
      }
      param_4 = local_34;
      piVar3 = local_30;
      piVar4 = piVar5;
    } while (piVar6 != piVar5);
  }
  _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEbENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIN9__gnu_cxx17__normal_iteratorIPS5_SB_EEEEvSG_T_SH_St20forward_iterator_tag
            (param_3,*(undefined4 *)(param_3 + 4),param_4,piVar3,0);
  if (local_34 != (int *)0x0) {
    _Z10GlitchFreePv();
  }
  return param_3;
}


