// _ZNK6glitch10irradiance18CIrradianceManager10getVolumesERKNS_4core8vector3dIfEERSt6vectorISt4pairIPNS0_17CIrradianceVolumeEbENS2_10SAllocatorISB_LNS_6memory13E_MEMORY_HINTE0EEEE.constprop.1276 @ 007eb904

/* WARNING: Removing unreachable block (ram,0x007ebf7c) */
/* WARNING: Restarted to delay deadcode elimination for space: stack */

int * _ZNK6glitch10irradiance18CIrradianceManager10getVolumesERKNS_4core8vector3dIfEERSt6vectorISt4pairIPNS0_17CIrradianceVolumeEbENS2_10SAllocatorISB_LNS_6memory13E_MEMORY_HINTE0EEEE_constprop_1276
                (int param_1,float *param_2,int *param_3)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  float *pfVar5;
  int iVar6;
  int *extraout_r2;
  int *piVar7;
  int *piVar8;
  undefined4 extraout_r2_00;
  undefined4 extraout_r3;
  int *piVar9;
  int *piVar10;
  int *piVar11;
  code *pcVar12;
  int iVar13;
  int *piVar14;
  int *piVar15;
  int *unaff_r10;
  int *piVar16;
  int *piVar17;
  int *piVar18;
  int *piVar19;
  uint uVar20;
  uint extraout_r12;
  bool bVar21;
  float fVar22;
  float fVar23;
  float fVar24;
  float fVar25;
  float fVar26;
  undefined8 unaff_d8;
  undefined8 uVar27;
  int iStack_f4;
  int iStack_f0;
  int iStack_ec;
  int iStack_e8;
  undefined1 auStack_e4 [4];
  int iStack_e0;
  int iStack_dc;
  int iStack_d8;
  int aiStack_d4 [2];
  int *piStack_cc;
  int *piStack_c8;
  int *piStack_c4;
  int *piStack_c0;
  int *piStack_bc;
  int *piStack_b8;
  float *pfStack_b4;
  float fStack_b0;
  float fStack_ac;
  float fStack_a8;
  int iStack_a4;
  float fStack_a0;
  int iStack_9c;
  float fStack_98;
  int *piStack_94;
  int *piStack_90;
  int *piStack_8c;
  undefined8 uStack_84;
  int *piStack_7c;
  int *piStack_78;
  int *piStack_74;
  int *piStack_70;
  int *piStack_6c;
  int *piStack_68;
  int *piStack_64;
  uint uStack_60;
  float *pfStack_5c;
  float local_58;
  float local_54;
  float local_50;
  int local_4c;
  uint local_48;
  int local_44;
  int local_40;
  int *local_3c;
  int *local_38;
  int *local_34;
  
  fVar26 = DAT_007ebcdc;
  piVar11 = *(int **)(param_1 + 0x20);
  local_3c = (int *)0x0;
  local_38 = (int *)0x0;
  local_34 = (int *)0x0;
  if (*(int **)(param_1 + 0x1c) != piVar11) {
    unaff_r10 = &local_4c;
    unaff_d8 = CONCAT44((int)((ulonglong)unaff_d8 >> 0x20),DAT_007ebcdc);
    piVar19 = *(int **)(param_1 + 0x1c);
    do {
      piVar7 = piVar19 + 1;
      iVar6 = *piVar19;
      fVar25 = *param_2;
      if (((((fVar25 < *(float *)(iVar6 + 0x18)) || (*(float *)(iVar6 + 0x24) < fVar25)) ||
           (param_2[1] < *(float *)(iVar6 + 0x1c))) ||
          ((*(float *)(iVar6 + 0x28) < param_2[1] || (param_2[2] < *(float *)(iVar6 + 0x20))))) ||
         (*(float *)(iVar6 + 0x2c) < param_2[2])) {
        if ((*(byte *)(param_1 + 0x14) & 8) != 0) {
          fVar24 = *(float *)(iVar6 + 0x18) - fVar25;
          local_58 = fVar26;
          fVar25 = fVar25 - *(float *)(iVar6 + 0x24);
          fVar22 = *(float *)(iVar6 + 0x1c) - param_2[1];
          fVar23 = param_2[1] - *(float *)(iVar6 + 0x28);
          if (fVar24 < fVar25) {
            fVar24 = fVar25;
          }
          if (fVar24 < 0.0) {
            fVar24 = fVar26;
          }
          local_54 = *(float *)(iVar6 + 0x20) - param_2[2];
          local_50 = param_2[2] - *(float *)(iVar6 + 0x2c);
          if (fVar23 <= fVar22) {
            fVar23 = fVar22;
          }
          if (fVar23 < 0.0) {
            fVar23 = fVar26;
          }
          fVar25 = local_54;
          if (local_54 < local_50) {
            fVar25 = local_50;
          }
          fVar22 = DAT_007ebcdc;
          if (0.0 < fVar25) {
            fVar22 = fVar25 * fVar25;
          }
          if (SQRT(fVar24 * fVar24 + fVar23 * fVar23 + fVar22) <= *(float *)(iVar6 + 0x48)) {
            local_48 = local_48 & 0xffffff00;
            local_4c = iVar6;
            if (local_38 == local_34) {
              _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEbENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS5_SB_EERKS5__constprop_1285
                        (&local_3c,local_38,unaff_r10);
            }
            else {
              if (local_38 != (int *)0x0) {
                *local_38 = iVar6;
                local_38[1] = local_48;
              }
              local_38 = local_38 + 2;
            }
          }
        }
      }
      else {
        piVar19 = (int *)param_3[1];
        local_40 = CONCAT31(local_40._1_3_,1);
        local_44 = iVar6;
        if (piVar19 == (int *)param_3[2]) {
          _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEbENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS5_SB_EERKS5__constprop_1285
                    (param_3,piVar19,&local_44);
        }
        else {
          if (piVar19 != (int *)0x0) {
            *piVar19 = iVar6;
            piVar19[1] = local_40;
          }
          param_3[1] = (int)(piVar19 + 2);
        }
      }
      piVar19 = piVar7;
    } while (piVar11 != piVar7);
  }
  piVar7 = local_38;
  piVar19 = local_3c;
  piVar9 = (int *)param_3[1];
  if (local_3c == local_38) goto LAB_007ebaf8;
  uVar20 = (int)local_38 - (int)local_3c >> 3;
  piVar10 = piVar9;
  if (uVar20 <= (uint)(param_3[2] - (int)piVar9 >> 3)) {
    do {
      if (piVar10 != (int *)0x0) {
        iVar6 = piVar19[1];
        *piVar10 = *piVar19;
        piVar10[1] = iVar6;
      }
      piVar19 = piVar19 + 2;
      piVar10 = piVar10 + 2;
    } while (local_38 != piVar19);
    param_3[1] = (int)(piVar9 + uVar20 * 2);
    goto LAB_007ebaf8;
  }
  piVar10 = (int *)*param_3;
  uVar1 = (int)piVar9 - (int)piVar10 >> 3;
  bVar21 = uVar20 == 0x1fffffff - uVar1;
  if (0x1fffffff - uVar1 <= uVar20 && !bVar21) {
    uVar27 = _ZSt20__throw_length_errorPKc((int)&DAT_007ebcdc + DAT_007ebce0);
    fVar26 = DAT_007ec0a0;
    pfVar5 = (float *)((ulonglong)uVar27 >> 0x20);
    iVar6 = (int)uVar27;
    if (bVar21) {
      uVar20 = (uint)unaff_r10 ^ extraout_r12 >> ((uint)piVar19 & 0xff);
    }
    pfStack_5c = &DAT_007ebcdc;
    piVar14 = *(int **)(iVar6 + 0x20);
    piStack_94 = (int *)0x0;
    piStack_90 = (int *)0x0;
    piStack_8c = (int *)0x0;
    piVar8 = unaff_r10;
    uStack_84 = unaff_d8;
    piStack_7c = piVar9;
    piStack_78 = piVar19;
    piStack_74 = piVar10;
    piStack_70 = piVar11;
    piStack_6c = param_3;
    piStack_68 = piVar7;
    piStack_64 = unaff_r10;
    uStack_60 = uVar20;
    if (*(int **)(iVar6 + 0x1c) != piVar14) {
      piVar8 = &iStack_a4;
      piVar11 = *(int **)(iVar6 + 0x1c);
      do {
        piVar19 = piVar11 + 1;
        iVar4 = *piVar11;
        fVar25 = *pfVar5;
        if (((fVar25 < *(float *)(iVar4 + 0x18)) || (*(float *)(iVar4 + 0x24) < fVar25)) ||
           ((pfVar5[1] < *(float *)(iVar4 + 0x1c) ||
            (((*(float *)(iVar4 + 0x28) < pfVar5[1] || (pfVar5[2] < *(float *)(iVar4 + 0x20))) ||
             (*(float *)(iVar4 + 0x2c) < pfVar5[2])))))) {
          if ((*(byte *)(iVar6 + 0x14) & 8) != 0) {
            fVar24 = *(float *)(iVar4 + 0x18) - fVar25;
            fStack_b0 = fVar26;
            fVar25 = fVar25 - *(float *)(iVar4 + 0x24);
            fVar22 = *(float *)(iVar4 + 0x1c) - pfVar5[1];
            fVar23 = pfVar5[1] - *(float *)(iVar4 + 0x28);
            if (fVar24 < fVar25) {
              fVar24 = fVar25;
            }
            if (fVar24 < 0.0) {
              fVar24 = fVar26;
            }
            fStack_ac = *(float *)(iVar4 + 0x20) - pfVar5[2];
            fStack_a8 = pfVar5[2] - *(float *)(iVar4 + 0x2c);
            if (fVar23 <= fVar22) {
              fVar23 = fVar22;
            }
            if (fVar23 < 0.0) {
              fVar23 = fVar26;
            }
            fVar25 = fStack_a8;
            if (fStack_a8 <= fStack_ac) {
              fVar25 = fStack_ac;
            }
            fVar22 = DAT_007ec0a0;
            if (0.0 < fVar25) {
              fVar22 = fVar25 * fVar25;
            }
            fVar25 = SQRT(fVar24 * fVar24 + fVar23 * fVar23 + fVar22);
            if (fVar25 <= *(float *)(iVar4 + 0x48)) {
              iStack_a4 = iVar4;
              fStack_a0 = fVar25;
              if (piStack_90 == piStack_8c) {
                _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEfENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE9push_backERKS5__part_772_constprop_1306
                          (&piStack_94,piVar8);
              }
              else {
                if (piStack_90 != (int *)0x0) {
                  *piStack_90 = iVar4;
                  piStack_90[1] = (int)fVar25;
                }
                piStack_90 = piStack_90 + 2;
              }
            }
          }
        }
        else {
          piVar11 = (int *)extraout_r2[1];
          fStack_98 = fVar26;
          iStack_9c = iVar4;
          if (piVar11 == (int *)extraout_r2[2]) {
            _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEfENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE9push_backERKS5__part_772_constprop_1306
                      (extraout_r2,&iStack_9c);
          }
          else {
            if (piVar11 != (int *)0x0) {
              *piVar11 = iVar4;
              piVar11[1] = (int)fVar26;
            }
            extraout_r2[1] = (int)(piVar11 + 2);
            fStack_98 = fVar26;
          }
        }
        piVar11 = piVar19;
      } while (piVar14 != piVar19);
    }
    piVar19 = piStack_90;
    piVar11 = piStack_94;
    piVar9 = (int *)*extraout_r2;
    if ((piVar9 != (int *)extraout_r2[1]) || (piStack_90 == piStack_94)) {
LAB_007ebe94:
      if (piStack_94 != (int *)0x0) {
        _Z10GlitchFreePv(piStack_94);
      }
      return extraout_r2;
    }
    uVar20 = (int)piStack_90 - (int)piStack_94 >> 3;
    piVar10 = piVar9;
    if (uVar20 <= (uint)(extraout_r2[2] - (int)piVar9 >> 3)) {
      do {
        if (piVar10 != (int *)0x0) {
          iVar6 = piVar11[1];
          *piVar10 = *piVar11;
          piVar10[1] = iVar6;
        }
        piVar11 = piVar11 + 2;
        piVar10 = piVar10 + 2;
      } while (piStack_90 != piVar11);
      extraout_r2[1] = (int)(piVar9 + uVar20 * 2);
      goto LAB_007ebe94;
    }
    if (uVar20 < 0x20000000) {
      piVar7 = piVar11;
      if (uVar20 == 0) {
        piVar14 = (int *)0x0;
        iVar6 = 0;
        piVar15 = (int *)0x0;
        piVar16 = piVar9;
        piVar17 = (int *)0x0;
      }
      else {
        iVar6 = uVar20 << 3;
        piVar14 = (int *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(iVar6,0);
        piVar18 = (int *)*extraout_r2;
        piVar16 = (int *)extraout_r2[1];
        piVar8 = piVar18;
        piVar15 = piVar14;
        piVar17 = piVar14;
        if (piVar9 != piVar18) {
          do {
            if (piVar15 != (int *)0x0) {
              iVar4 = piVar8[1];
              *piVar15 = *piVar8;
              piVar15[1] = iVar4;
            }
            piVar8 = piVar8 + 2;
            piVar15 = piVar15 + 2;
          } while (piVar9 != piVar8);
          piVar15 = (int *)((int)piVar14 + ((int)piVar9 - (int)(piVar18 + 2) & 0xfffffff8U) + 8);
          piVar10 = piVar18;
          piVar17 = piVar15;
        }
      }
      do {
        if (piVar15 != (int *)0x0) {
          iVar4 = piVar7[1];
          *piVar15 = *piVar7;
          piVar15[1] = iVar4;
        }
        piVar7 = piVar7 + 2;
        piVar15 = piVar15 + 2;
      } while (piVar19 != piVar7);
      piVar17 = (int *)((int)piVar17 + ((int)piVar19 - (int)(piVar11 + 2) & 0xfffffff8U) + 8);
      piVar11 = piVar9;
      piVar19 = piVar17;
      if (piVar9 != piVar16) {
        do {
          if (piVar19 != (int *)0x0) {
            iVar4 = piVar11[1];
            *piVar19 = *piVar11;
            piVar19[1] = iVar4;
          }
          piVar11 = piVar11 + 2;
          piVar19 = piVar19 + 2;
        } while (piVar16 != piVar11);
        piVar17 = (int *)((int)piVar17 + ((int)piVar16 - (int)(piVar9 + 2) & 0xfffffff8U) + 8);
      }
      if (piVar10 != (int *)0x0) {
        _Z10GlitchFreePv(piVar10);
      }
      *extraout_r2 = (int)piVar14;
      extraout_r2[1] = (int)piVar17;
      extraout_r2[2] = (int)piVar14 + iVar6;
      goto LAB_007ebe94;
    }
    uVar27 = _ZSt20__throw_length_errorPKc((int)&DAT_007ec0a0 + DAT_007ec0a4);
    iVar6 = DAT_007ec468;
    iVar4 = (int)((ulonglong)uVar27 >> 0x20);
    piVar10 = (int *)uVar27;
    pfStack_b4 = &DAT_007ec0a0;
    piStack_c4 = piVar19;
    piVar19 = *(int **)(*(int *)(iVar4 + 0x20) + 0x28);
    iStack_f4 = 0;
    pcVar12 = *(code **)(*piVar19 + 0x38);
    piStack_cc = piVar11;
    piStack_c8 = piVar9;
    piStack_c0 = piVar14;
    piStack_bc = piVar7;
    piStack_b8 = piVar8;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_732
              (aiStack_d4,extraout_r2_00);
    (*pcVar12)(&iStack_f0,piVar19,aiStack_d4);
    iVar6 = *(int *)(iVar6 + 0x7ec100);
    if (aiStack_d4[0] + -0xc != iVar6) {
      piVar11 = (int *)(aiStack_d4[0] + -4);
      DataMemoryBarrier(0xf);
      do {
        iVar3 = *piVar11;
        bVar21 = (bool)hasExclusiveAccess(piVar11);
      } while (!bVar21);
      *piVar11 = iVar3 + -1;
      DataMemoryBarrier(0xf);
      if (iVar3 < 1) {
        _Z10GlitchFreePv();
      }
    }
    iVar13 = iVar4 + 0x28;
    _ZN3glf18ReadWriteMutexLock8readLockEj(iVar13,0);
    _ZN6glitch7collada15CResFileManager3getEPKc(&iStack_d8,iVar4,iStack_f0);
    iVar3 = iStack_d8;
    if (iStack_d8 != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_d8 + 4);
    }
    iVar2 = iStack_f4;
    iStack_f4 = iVar3;
    if (iVar2 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (iStack_d8 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    iVar3 = iStack_f4;
    if (iStack_f4 != 0) {
      *piVar10 = iStack_f4;
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_f4 + 4);
      _ZN3glf18ReadWriteMutexLock10readUnlockEv(iVar13);
      goto LAB_007ec180;
    }
    _ZN3glf18ReadWriteMutexLock10readUnlockEv(iVar13);
    iStack_ec = iVar3;
    _ZN3glf18ReadWriteMutexLock9writeLockEj(iVar13,0);
    _ZN6glitch7collada15CResFileManager3getEPKc(&iStack_dc,iVar4,iStack_f0);
    iVar3 = iStack_dc;
    if (iStack_dc != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_dc + 4);
    }
    iVar2 = iStack_f4;
    iStack_f4 = iVar3;
    if (iVar2 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (iStack_dc != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (iStack_f4 == 0) {
      piVar11 = *(int **)(*(int *)(iVar4 + 0x20) + 0x28);
      (**(code **)(*piVar11 + 0xc))(&iStack_e0,piVar11,iStack_f0);
      iVar3 = iStack_e0;
      if (iStack_e0 != 0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_e0 + 4);
      }
      iVar2 = iStack_ec;
      iStack_ec = iVar3;
      if (iVar2 != 0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      if (iStack_e0 != 0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      iVar3 = iStack_f0;
      if (iStack_ec == 0) {
        _ZN6glitch2os7Printer4logfENS_11E_LOG_LEVELEPKcz(2,DAT_007ec46c + 0x7ec3e8,iStack_f0);
        *piVar10 = 0;
        goto LAB_007ec224;
      }
      iVar2 = _Znwj(0x5c);
      _ZN6glitch7collada8CResFileC1EPKcRKN5boost13intrusive_ptrINS_2io9IReadFileEEEb
                (iVar2,iVar3,&iStack_ec,0);
      if (iVar2 != 0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar2 + 4);
      }
      bVar21 = iStack_f4 != 0;
      iStack_f4 = iVar2;
      if (bVar21) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      if (iStack_f4 == 0) {
        *piVar10 = 0;
        goto LAB_007ec224;
      }
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_732
                (auStack_e4,iStack_f0);
      piVar11 = (int *)_ZNSt3mapISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEN5boost13intrusive_ptrINS2_7collada8CResFileEEESt4lessIS8_ENS4_ISt4pairIKS8_SD_ELS6_0EEEEixERSH__constprop_1260
                                 (iVar4 + 8,auStack_e4);
      iVar3 = iStack_f4;
      if (iStack_f4 != 0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_f4 + 4);
      }
      iVar2 = *piVar11;
      *piVar11 = iVar3;
      if (iVar2 != 0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (auStack_e4);
      _ZN3glf18ReadWriteMutexLock11writeUnlockEv(iVar13);
      if (*(int *)(*(int *)(iStack_f4 + 0x10) + 0x14) == 0) {
        _ZN6glitch7collada15CResFileManager11getReadFileERKN5boost13intrusive_ptrINS_2io9IReadFileEEE
                  (&iStack_e8,iVar4,&iStack_ec);
        iVar3 = _ZN6glitch7collada15CResFileManager15postLoadProcessERKN5boost13intrusive_ptrINS0_8CResFileEEEPNS0_16CColladaDatabaseERKNS3_INS_2io9IReadFileEEE
                          (iVar4,&iStack_f4,extraout_r3,&iStack_e8);
        if (iStack_e8 != 0) {
          _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
        }
        if (iVar3 == 0) goto LAB_007ec35c;
        _ZN6glitch7collada15CResFileManager6unloadEPKcb(iVar4,iStack_f0,0);
        *piVar10 = 0;
      }
      else {
LAB_007ec35c:
        *piVar10 = iStack_f4;
        if (iStack_f4 != 0) {
          _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_f4 + 4);
        }
      }
    }
    else {
      *piVar10 = iStack_f4;
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_f4 + 4);
LAB_007ec224:
      _ZN3glf18ReadWriteMutexLock11writeUnlockEv(iVar13);
    }
    if (iStack_ec != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
LAB_007ec180:
    if (iStack_f0 + -0xc != iVar6) {
      piVar11 = (int *)(iStack_f0 + -4);
      DataMemoryBarrier(0xf);
      do {
        iVar6 = *piVar11;
        bVar21 = (bool)hasExclusiveAccess(piVar11);
      } while (!bVar21);
      *piVar11 = iVar6 + -1;
      DataMemoryBarrier(0xf);
      if (iVar6 < 1) {
        _Z10GlitchFreePv();
      }
    }
    if (iStack_f4 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    return piVar10;
  }
  if (uVar20 < uVar1) {
    uVar20 = uVar1 * 2;
  }
  else {
    uVar20 = uVar1 + uVar20;
  }
  if ((uVar20 < uVar1) || (0x1fffffff < uVar20)) {
    iVar6 = -8;
LAB_007ebb98:
    piVar11 = (int *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(iVar6,0);
    piVar10 = (int *)*param_3;
    piVar8 = (int *)param_3[1];
  }
  else {
    if (uVar20 != 0) {
      iVar6 = uVar20 << 3;
      goto LAB_007ebb98;
    }
    piVar11 = (int *)0x0;
    iVar6 = 0;
    piVar8 = piVar9;
  }
  piVar15 = piVar19;
  piVar14 = piVar10;
  piVar16 = piVar11;
  piVar17 = piVar11;
  if (piVar9 != piVar10) {
    do {
      if (piVar16 != (int *)0x0) {
        iVar4 = piVar14[1];
        *piVar16 = *piVar14;
        piVar16[1] = iVar4;
      }
      piVar14 = piVar14 + 2;
      piVar16 = piVar16 + 2;
    } while (piVar9 != piVar14);
    piVar16 = (int *)((int)piVar11 + ((int)piVar9 - (int)(piVar10 + 2) & 0xfffffff8U) + 8);
    piVar17 = piVar16;
  }
  do {
    if (piVar16 != (int *)0x0) {
      iVar4 = piVar15[1];
      *piVar16 = *piVar15;
      piVar16[1] = iVar4;
    }
    piVar15 = piVar15 + 2;
    piVar16 = piVar16 + 2;
  } while (piVar7 != piVar15);
  piVar17 = (int *)((int)piVar17 + ((int)piVar7 - (int)(piVar19 + 2) & 0xfffffff8U) + 8);
  piVar19 = piVar9;
  piVar7 = piVar17;
  if (piVar9 != piVar8) {
    do {
      if (piVar7 != (int *)0x0) {
        iVar4 = piVar19[1];
        *piVar7 = *piVar19;
        piVar7[1] = iVar4;
      }
      piVar19 = piVar19 + 2;
      piVar7 = piVar7 + 2;
    } while (piVar8 != piVar19);
    piVar17 = (int *)((int)piVar17 + ((int)piVar8 - (int)(piVar9 + 2) & 0xfffffff8U) + 8);
  }
  if (piVar10 != (int *)0x0) {
    _Z10GlitchFreePv(piVar10);
  }
  *param_3 = (int)piVar11;
  param_3[1] = (int)piVar17;
  param_3[2] = (int)piVar11 + iVar6;
LAB_007ebaf8:
  if (local_3c != (int *)0x0) {
    _Z10GlitchFreePv(local_3c);
  }
  return param_3;
}


