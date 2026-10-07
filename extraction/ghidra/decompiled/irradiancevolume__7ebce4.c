// _ZNK6glitch10irradiance18CIrradianceManager10getVolumesERKNS_4core8vector3dIfEERSt6vectorISt4pairIPNS0_17CIrradianceVolumeEfENS2_10SAllocatorISB_LNS_6memory13E_MEMORY_HINTE0EEEE.constprop.1283 @ 007ebce4

/* WARNING: Removing unreachable block (ram,0x007ebf7c) */
/* WARNING: Restarted to delay deadcode elimination for space: stack */

int * _ZNK6glitch10irradiance18CIrradianceManager10getVolumesERKNS_4core8vector3dIfEERSt6vectorISt4pairIPNS0_17CIrradianceVolumeEfENS2_10SAllocatorISB_LNS_6memory13E_MEMORY_HINTE0EEEE_constprop_1283
                (int param_1,float *param_2,int *param_3)

{
  uint uVar1;
  int *piVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int *piVar7;
  undefined4 extraout_r2;
  int *piVar8;
  int *piVar9;
  undefined4 extraout_r3;
  int *piVar10;
  code *pcVar11;
  int iVar12;
  int *piVar13;
  int *piVar14;
  int *piVar15;
  int *piVar16;
  int *piVar17;
  int *piVar18;
  bool bVar19;
  float fVar20;
  float fVar21;
  float fVar22;
  float fVar23;
  float fVar24;
  float fVar25;
  undefined8 uVar26;
  int iStack_9c;
  int iStack_98;
  int iStack_94;
  int iStack_90;
  undefined1 auStack_8c [4];
  int iStack_88;
  int iStack_84;
  int iStack_80;
  int iStack_7c;
  int *piStack_78;
  int *piStack_74;
  int *piStack_70;
  int *piStack_6c;
  int *piStack_68;
  int local_4c;
  float local_48;
  int local_44;
  float local_40;
  int *local_3c;
  int *local_38;
  int *local_34;
  
  fVar25 = DAT_007ec0a0;
  piVar13 = *(int **)(param_1 + 0x20);
  local_3c = (int *)0x0;
  local_38 = (int *)0x0;
  local_34 = (int *)0x0;
  if (*(int **)(param_1 + 0x1c) != piVar13) {
    piVar8 = *(int **)(param_1 + 0x1c);
    do {
      piVar17 = piVar8 + 1;
      iVar6 = *piVar8;
      fVar24 = *param_2;
      if (((((fVar24 < *(float *)(iVar6 + 0x18)) || (*(float *)(iVar6 + 0x24) < fVar24)) ||
           (param_2[1] < *(float *)(iVar6 + 0x1c))) ||
          ((*(float *)(iVar6 + 0x28) < param_2[1] || (param_2[2] < *(float *)(iVar6 + 0x20))))) ||
         (*(float *)(iVar6 + 0x2c) < param_2[2])) {
        if ((*(byte *)(param_1 + 0x14) & 8) != 0) {
          fVar23 = *(float *)(iVar6 + 0x18) - fVar24;
          fVar24 = fVar24 - *(float *)(iVar6 + 0x24);
          fVar20 = *(float *)(iVar6 + 0x1c) - param_2[1];
          fVar21 = param_2[1] - *(float *)(iVar6 + 0x28);
          if (fVar23 < fVar24) {
            fVar23 = fVar24;
          }
          if (fVar23 < 0.0) {
            fVar23 = fVar25;
          }
          fVar22 = *(float *)(iVar6 + 0x20) - param_2[2];
          fVar24 = param_2[2] - *(float *)(iVar6 + 0x2c);
          if (fVar21 <= fVar20) {
            fVar21 = fVar20;
          }
          if (fVar21 < 0.0) {
            fVar21 = fVar25;
          }
          if (fVar24 <= fVar22) {
            fVar24 = fVar22;
          }
          fVar20 = DAT_007ec0a0;
          if (0.0 < fVar24) {
            fVar20 = fVar24 * fVar24;
          }
          fVar24 = SQRT(fVar23 * fVar23 + fVar21 * fVar21 + fVar20);
          if (fVar24 <= *(float *)(iVar6 + 0x48)) {
            local_4c = iVar6;
            local_48 = fVar24;
            if (local_38 == local_34) {
              _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEfENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE9push_backERKS5__part_772_constprop_1306
                        (&local_3c,&local_4c);
            }
            else {
              if (local_38 != (int *)0x0) {
                *local_38 = iVar6;
                local_38[1] = (int)fVar24;
              }
              local_38 = local_38 + 2;
            }
          }
        }
      }
      else {
        piVar8 = (int *)param_3[1];
        local_40 = fVar25;
        local_44 = iVar6;
        if (piVar8 == (int *)param_3[2]) {
          _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEfENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE9push_backERKS5__part_772_constprop_1306
                    (param_3,&local_44);
        }
        else {
          if (piVar8 != (int *)0x0) {
            *piVar8 = iVar6;
            piVar8[1] = (int)fVar25;
          }
          param_3[1] = (int)(piVar8 + 2);
          local_40 = fVar25;
        }
      }
      piVar8 = piVar17;
    } while (piVar13 != piVar17);
  }
  piVar17 = local_38;
  piVar8 = local_3c;
  piVar10 = (int *)*param_3;
  if ((piVar10 != (int *)param_3[1]) || (local_38 == local_3c)) {
LAB_007ebe94:
    if (local_3c != (int *)0x0) {
      _Z10GlitchFreePv(local_3c);
    }
    return param_3;
  }
  uVar1 = (int)local_38 - (int)local_3c >> 3;
  piVar9 = piVar10;
  if (uVar1 <= (uint)(param_3[2] - (int)piVar10 >> 3)) {
    do {
      if (piVar9 != (int *)0x0) {
        iVar6 = piVar8[1];
        *piVar9 = *piVar8;
        piVar9[1] = iVar6;
      }
      piVar8 = piVar8 + 2;
      piVar9 = piVar9 + 2;
    } while (local_38 != piVar8);
    param_3[1] = (int)(piVar10 + uVar1 * 2);
    goto LAB_007ebe94;
  }
  if (uVar1 < 0x20000000) {
    piVar13 = piVar8;
    if (uVar1 == 0) {
      piVar2 = (int *)0x0;
      iVar6 = 0;
      piVar15 = (int *)0x0;
      piVar18 = piVar10;
      piVar14 = (int *)0x0;
    }
    else {
      iVar6 = uVar1 << 3;
      piVar2 = (int *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(iVar6,0);
      piVar16 = (int *)*param_3;
      piVar18 = (int *)param_3[1];
      piVar7 = piVar16;
      piVar15 = piVar2;
      piVar14 = piVar2;
      if (piVar10 != piVar16) {
        do {
          if (piVar15 != (int *)0x0) {
            iVar5 = piVar7[1];
            *piVar15 = *piVar7;
            piVar15[1] = iVar5;
          }
          piVar7 = piVar7 + 2;
          piVar15 = piVar15 + 2;
        } while (piVar10 != piVar7);
        piVar15 = (int *)((int)piVar2 + ((int)piVar10 - (int)(piVar16 + 2) & 0xfffffff8U) + 8);
        piVar9 = piVar16;
        piVar14 = piVar15;
      }
    }
    do {
      if (piVar15 != (int *)0x0) {
        iVar5 = piVar13[1];
        *piVar15 = *piVar13;
        piVar15[1] = iVar5;
      }
      piVar13 = piVar13 + 2;
      piVar15 = piVar15 + 2;
    } while (piVar17 != piVar13);
    piVar14 = (int *)((int)piVar14 + ((int)piVar17 - (int)(piVar8 + 2) & 0xfffffff8U) + 8);
    piVar13 = piVar10;
    piVar8 = piVar14;
    if (piVar10 != piVar18) {
      do {
        if (piVar8 != (int *)0x0) {
          iVar5 = piVar13[1];
          *piVar8 = *piVar13;
          piVar8[1] = iVar5;
        }
        piVar13 = piVar13 + 2;
        piVar8 = piVar8 + 2;
      } while (piVar18 != piVar13);
      piVar14 = (int *)((int)piVar14 + ((int)piVar18 - (int)(piVar10 + 2) & 0xfffffff8U) + 8);
    }
    if (piVar9 != (int *)0x0) {
      _Z10GlitchFreePv(piVar9);
    }
    *param_3 = (int)piVar2;
    param_3[1] = (int)piVar14;
    param_3[2] = (int)piVar2 + iVar6;
    goto LAB_007ebe94;
  }
  uVar26 = _ZSt20__throw_length_errorPKc((int)&DAT_007ec0a0 + DAT_007ec0a4);
  iVar6 = DAT_007ec468;
  iVar5 = (int)((ulonglong)uVar26 >> 0x20);
  piVar9 = (int *)uVar26;
  piStack_6c = piVar17;
  piVar17 = *(int **)(*(int *)(iVar5 + 0x20) + 0x28);
  iStack_9c = 0;
  pcVar11 = *(code **)(*piVar17 + 0x38);
  piStack_78 = param_3;
  piStack_74 = piVar8;
  piStack_70 = piVar10;
  piStack_68 = piVar13;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_732
            (&iStack_7c,extraout_r2);
  (*pcVar11)(&iStack_98,piVar17,&iStack_7c);
  iVar6 = *(int *)(iVar6 + 0x7ec100);
  if (iStack_7c + -0xc != iVar6) {
    piVar13 = (int *)(iStack_7c + -4);
    DataMemoryBarrier(0xf);
    do {
      iVar4 = *piVar13;
      bVar19 = (bool)hasExclusiveAccess(piVar13);
    } while (!bVar19);
    *piVar13 = iVar4 + -1;
    DataMemoryBarrier(0xf);
    if (iVar4 < 1) {
      _Z10GlitchFreePv();
    }
  }
  iVar12 = iVar5 + 0x28;
  _ZN3glf18ReadWriteMutexLock8readLockEj(iVar12,0);
  _ZN6glitch7collada15CResFileManager3getEPKc(&iStack_80,iVar5,iStack_98);
  iVar4 = iStack_80;
  if (iStack_80 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_80 + 4);
  }
  iVar3 = iStack_9c;
  iStack_9c = iVar4;
  if (iVar3 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  if (iStack_80 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  iVar4 = iStack_9c;
  if (iStack_9c != 0) {
    *piVar9 = iStack_9c;
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_9c + 4);
    _ZN3glf18ReadWriteMutexLock10readUnlockEv(iVar12);
    goto LAB_007ec180;
  }
  _ZN3glf18ReadWriteMutexLock10readUnlockEv(iVar12);
  iStack_94 = iVar4;
  _ZN3glf18ReadWriteMutexLock9writeLockEj(iVar12,0);
  _ZN6glitch7collada15CResFileManager3getEPKc(&iStack_84,iVar5,iStack_98);
  iVar4 = iStack_84;
  if (iStack_84 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_84 + 4);
  }
  iVar3 = iStack_9c;
  iStack_9c = iVar4;
  if (iVar3 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  if (iStack_84 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  if (iStack_9c == 0) {
    piVar13 = *(int **)(*(int *)(iVar5 + 0x20) + 0x28);
    (**(code **)(*piVar13 + 0xc))(&iStack_88,piVar13,iStack_98);
    iVar4 = iStack_88;
    if (iStack_88 != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_88 + 4);
    }
    iVar3 = iStack_94;
    iStack_94 = iVar4;
    if (iVar3 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (iStack_88 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    iVar4 = iStack_98;
    if (iStack_94 == 0) {
      _ZN6glitch2os7Printer4logfENS_11E_LOG_LEVELEPKcz(2,DAT_007ec46c + 0x7ec3e8,iStack_98);
      *piVar9 = 0;
      goto LAB_007ec224;
    }
    iVar3 = _Znwj(0x5c);
    _ZN6glitch7collada8CResFileC1EPKcRKN5boost13intrusive_ptrINS_2io9IReadFileEEEb
              (iVar3,iVar4,&iStack_94,0);
    if (iVar3 != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar3 + 4);
    }
    bVar19 = iStack_9c != 0;
    iStack_9c = iVar3;
    if (bVar19) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (iStack_9c == 0) {
      *piVar9 = 0;
      goto LAB_007ec224;
    }
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_732
              (auStack_8c,iStack_98);
    piVar13 = (int *)_ZNSt3mapISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEN5boost13intrusive_ptrINS2_7collada8CResFileEEESt4lessIS8_ENS4_ISt4pairIKS8_SD_ELS6_0EEEEixERSH__constprop_1260
                               (iVar5 + 8,auStack_8c);
    iVar4 = iStack_9c;
    if (iStack_9c != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_9c + 4);
    }
    iVar3 = *piVar13;
    *piVar13 = iVar4;
    if (iVar3 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_8c);
    _ZN3glf18ReadWriteMutexLock11writeUnlockEv(iVar12);
    if (*(int *)(*(int *)(iStack_9c + 0x10) + 0x14) == 0) {
      _ZN6glitch7collada15CResFileManager11getReadFileERKN5boost13intrusive_ptrINS_2io9IReadFileEEE
                (&iStack_90,iVar5,&iStack_94);
      iVar4 = _ZN6glitch7collada15CResFileManager15postLoadProcessERKN5boost13intrusive_ptrINS0_8CResFileEEEPNS0_16CColladaDatabaseERKNS3_INS_2io9IReadFileEEE
                        (iVar5,&iStack_9c,extraout_r3,&iStack_90);
      if (iStack_90 != 0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      if (iVar4 == 0) goto LAB_007ec35c;
      _ZN6glitch7collada15CResFileManager6unloadEPKcb(iVar5,iStack_98,0);
      *piVar9 = 0;
    }
    else {
LAB_007ec35c:
      *piVar9 = iStack_9c;
      if (iStack_9c != 0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_9c + 4);
      }
    }
  }
  else {
    *piVar9 = iStack_9c;
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iStack_9c + 4);
LAB_007ec224:
    _ZN3glf18ReadWriteMutexLock11writeUnlockEv(iVar12);
  }
  if (iStack_94 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
LAB_007ec180:
  if (iStack_98 + -0xc != iVar6) {
    piVar13 = (int *)(iStack_98 + -4);
    DataMemoryBarrier(0xf);
    do {
      iVar6 = *piVar13;
      bVar19 = (bool)hasExclusiveAccess(piVar13);
    } while (!bVar19);
    *piVar13 = iVar6 + -1;
    DataMemoryBarrier(0xf);
    if (iVar6 < 1) {
      _Z10GlitchFreePv();
    }
  }
  if (iStack_9c != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  return piVar9;
}


