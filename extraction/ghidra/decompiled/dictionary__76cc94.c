// _ZN6glitch7collada20CAnimationDictionaryC2EPKNS0_17CAnimationPackageERKNS0_9anim_pack20SAnimationDictionaryEPKS1_ @ 0076cc94

int * _ZN6glitch7collada20CAnimationDictionaryC2EPKNS0_17CAnimationPackageERKNS0_9anim_pack20SAnimationDictionaryEPKS1_
                (int *param_1,int *param_2,int param_3,int *param_4,int param_5)

{
  int iVar1;
  undefined4 *puVar2;
  int iVar3;
  int *piVar4;
  int *piVar5;
  int *piVar6;
  int iVar7;
  int iVar8;
  int *extraout_r2;
  int iVar9;
  int iVar10;
  int iVar11;
  undefined4 uVar12;
  int extraout_r3;
  undefined4 extraout_r3_00;
  int iVar13;
  int iVar14;
  undefined4 *puVar15;
  uint uVar16;
  int iVar17;
  char *pcVar18;
  int extraout_r12;
  undefined1 *puVar19;
  bool bVar20;
  undefined8 uVar21;
  undefined1 auStack_a0 [4];
  int iStack_9c;
  undefined4 *puStack_98;
  undefined4 *puStack_94;
  int iStack_90;
  int iStack_8c;
  int *piStack_88;
  int iStack_84;
  undefined4 uStack_80;
  undefined4 uStack_7c;
  int *piStack_74;
  undefined4 uStack_70;
  int *piStack_6c;
  int iStack_68;
  uint uStack_64;
  undefined4 local_30;
  undefined4 local_2c;
  
  iVar9 = *(int *)(param_2[1] + -0xc);
  iVar1 = *(int *)(param_3 + 0xc);
  *param_1 = param_2[1];
  *(int *)((int)param_1 + iVar9) = param_2[2];
  param_1[2] = iVar1;
  if (iVar1 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar1 + 4);
  }
  iVar1 = DAT_0076d084;
  iVar13 = 0;
  iVar9 = *(int *)(param_3 + 0x10);
  param_1[4] = 0;
  param_1[3] = iVar9;
  param_1[5] = 0;
  param_1[6] = 0;
  param_1[1] = iVar1 + 0x76cd0c;
  iVar1 = *(int *)(*param_2 + -0xc);
  *param_1 = *param_2;
  *(int *)((int)param_1 + iVar1) = param_2[3];
  param_1[8] = (int)param_4;
  iVar1 = *param_4;
  param_1[9] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[1] = iVar1;
  if (param_5 == 0) {
    uVar16 = param_4[2];
    param_1[7] = (int)param_4;
    bVar20 = uVar16 == 0x1fffffff;
    if (0x1fffffff < uVar16) {
      uVar21 = _ZSt20__throw_length_errorPKc((int)&DAT_0076d084 + DAT_0076d08c);
      iStack_90 = (int)((ulonglong)uVar21 >> 0x20);
      piVar4 = (int *)uVar21;
      if (bVar20) {
        uVar16 = (int)extraout_r2 - (extraout_r12 >> 0x11);
      }
      iStack_68 = param_5;
      uStack_70 = 0;
      puVar19 = auStack_a0;
      iVar13 = *(int *)(iStack_90 + 0xc);
      iVar1 = DAT_0076d484 + 0x76d0c8;
      iVar9 = DAT_0076d484 + 0x76d0ec;
      piVar4[0xd] = 0;
      *piVar4 = iVar1;
      piVar4[0xc] = iVar9;
      piVar4[2] = iVar13;
      piStack_74 = param_1;
      piStack_6c = param_2;
      uStack_64 = uVar16;
      if (iVar13 != 0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar13 + 4);
      }
      iVar1 = DAT_0076d48c;
      iVar7 = 0;
      iVar9 = *(int *)(iStack_90 + 0x10);
      iVar13 = DAT_0076d488 + 0x76d104;
      *piVar4 = DAT_0076d48c + 0x76d114;
      piVar4[1] = iVar13;
      piVar4[8] = (int)extraout_r2;
      piStack_88 = (int *)(iStack_90 + 0x24);
      iVar13 = *extraout_r2;
      piVar4[3] = iVar9;
      piVar4[4] = 0;
      piVar4[5] = 0;
      piVar4[6] = 0;
      piVar4[0xc] = iVar1 + 0x76d138;
      piVar4[9] = 0;
      piVar4[10] = 0;
      piVar4[0xb] = 0;
      piVar4[1] = iVar13;
      if (extraout_r3 == 0) {
        uVar16 = extraout_r2[2];
        piVar4[7] = (int)extraout_r2;
        bVar20 = uVar16 == 0x1fffffff;
        if (0x1fffffff < uVar16) {
          uVar21 = _ZSt20__throw_length_errorPKc((int)&DAT_0076d484 + DAT_0076d494);
          piVar6 = (int *)((ulonglong)uVar21 >> 0x20);
          piVar5 = (int *)uVar21;
          if (bVar20) {
            puVar19 = (undefined1 *)
                      ((int)(ZEXT48(auStack_a0) + (ulonglong)uVar16 >> 0x20) + (int)piVar5 * -0x400)
            ;
          }
          *(int **)(puVar19 + -4) = &DAT_0076d484;
          *(undefined4 *)(puVar19 + -8) = 0;
          *(int **)(puVar19 + -0xc) = piVar4;
          *(undefined4 *)(puVar19 + -0x10) = extraout_r3_00;
          iVar9 = *piVar6;
          iVar1 = piVar5[9];
          *piVar5 = iVar9;
          *(int *)((int)piVar5 + *(int *)(iVar9 + -0xc)) = piVar6[3];
          if (iVar1 != 0) {
            _Z10GlitchFreePv();
          }
          _ZN6glitch7collada16CColladaDatabaseD1Ev(piVar5 + 2);
          iVar1 = piVar6[1];
          *piVar5 = iVar1;
          *(int *)((int)piVar5 + *(int *)(iVar1 + -0xc)) = piVar6[2];
          return piVar5;
        }
        if (uVar16 != 0) {
          _ZNSt6vectorIN6glitch7collada16SAnimationClipIDENS0_4core10SAllocatorIS2_LNS0_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_899
                    (piVar4 + 9,uVar16);
          piVar5 = piStack_88;
          iVar1 = iStack_90;
          iVar9 = piVar4[8];
          iVar13 = *(int *)(iVar9 + 8);
          if (0 < iVar13) {
            iVar7 = 0;
            iVar14 = 0;
            while( true ) {
              uVar12 = _ZNK6glitch7collada20CAnimationDictionary18resolveAnimationIDEPKNS0_17CAnimationPackageEPKc
                                 (piVar4,iVar1,*(undefined4 *)(*(int *)(iVar9 + 0xc) + iVar7 + 4));
              pcVar18 = *(char **)(*(int *)(piVar4[8] + 0xc) + iVar7 + 8);
              if (pcVar18 == (char *)0x0) {
                uStack_7c = 0;
              }
              else if (*pcVar18 == '\0') {
                uStack_7c = 0;
              }
              else {
                uStack_7c = _ZNK6glitch7collada20CAnimationDictionary13resolveClipIDERKN5boost13intrusive_ptrINS0_13CAnimationSetEEEiPKc_part_130
                                      (piVar5,uVar12);
              }
              puVar2 = (undefined4 *)piVar4[10];
              uStack_80 = uVar12;
              if (puVar2 == (undefined4 *)piVar4[0xb]) {
                _ZNSt6vectorIN6glitch7collada16SAnimationClipIDENS0_4core10SAllocatorIS2_LNS0_6memory13E_MEMORY_HINTE0EEEE9push_backERKS2__part_1154_constprop_1339
                          (piVar4 + 9,&uStack_80);
              }
              else {
                if (puVar2 != (undefined4 *)0x0) {
                  *puVar2 = uVar12;
                  puVar2[1] = uStack_7c;
                }
                piVar4[10] = (int)(puVar2 + 2);
              }
              iVar14 = iVar14 + 1;
              iVar7 = iVar7 + 0xc;
              if (iVar14 == iVar13) break;
              iVar9 = piVar4[8];
            }
          }
        }
      }
      else {
        piVar4[7] = *(int *)(extraout_r3 + 0x1c);
        _ZNSt6vectorIN6glitch7collada16SAnimationClipIDENS0_4core10SAllocatorIS2_LNS0_6memory13E_MEMORY_HINTE0EEEEaSERKS8_
                  (piVar4 + 9,extraout_r3 + 0x24);
        iVar1 = piVar4[8];
        iStack_8c = *(int *)(iVar1 + 8);
        if (0 < iStack_8c) {
          iVar9 = 0;
          iStack_84 = DAT_0076d490 + 0x76d188;
          do {
            iVar13 = *(int *)(piVar4[7] + 8);
            iStack_9c = *(int *)(iVar1 + 0xc) + iVar7;
            pcVar18 = *(char **)(*(int *)(iVar1 + 0xc) + iVar7);
            puVar2 = *(undefined4 **)(piVar4[7] + 0xc);
            puStack_98 = puVar2 + iVar13 * 3;
            puStack_94 = puVar2;
            for (iVar1 = (iVar13 * 0xc >> 2) * -0x55555555; 0 < iVar1; iVar1 = (iVar1 - iVar13) + -1
                ) {
              while( true ) {
                iVar13 = iVar1 >> 1;
                iVar14 = strcmp((char *)puVar2[iVar13 * 3],pcVar18);
                if (iVar14 < 0) break;
                iVar1 = iVar13;
                if (iVar13 == 0) goto LAB_0076d218;
              }
              puVar2 = puVar2 + iVar13 * 3 + 3;
            }
LAB_0076d218:
            if ((puStack_98 == puVar2) || (iVar1 = strcmp((char *)*puVar2,pcVar18), iVar1 != 0)) {
              iVar1 = -8;
            }
            else {
              iVar1 = ((int)puVar2 - (int)puStack_94 >> 2) * 0x55555558;
            }
            iVar13 = _ZNK6glitch7collada20CAnimationDictionary18resolveAnimationIDEPKNS0_17CAnimationPackageEPKc
                               (piVar4,iStack_90,*(undefined4 *)(iStack_9c + 4));
            iStack_9c = piVar4[9] + iVar1;
            *(int *)(piVar4[9] + iVar1) = iVar13;
            pcVar18 = *(char **)(*(int *)(piVar4[8] + 0xc) + iVar7 + 8);
            if (pcVar18 == (char *)0x0) {
              iVar1 = 0;
LAB_0076d308:
              *(int *)(iStack_9c + 4) = iVar1;
              if (iVar9 + 1 == iStack_8c) {
                return piVar4;
              }
            }
            else {
              iVar1 = 0;
              if (*pcVar18 == '\0') goto LAB_0076d308;
              iVar14 = *(int *)(*piStack_88 + 0x44);
              iVar1 = *(int *)(iVar14 + iVar13 * 0x14);
              iVar8 = *(int *)(*(int *)(*(int *)(iVar1 + 0x10) + 0x20) + 0x38);
              if (0 < iVar8) {
                iVar1 = 0;
                do {
                  puVar2 = (undefined4 *)
                           _ZNK6glitch7collada16CColladaDatabase16getAnimationClipEi
                                     (iVar14 + iVar13 * 0x14,iVar1);
                  iVar10 = strcmp(pcVar18,(char *)*puVar2);
                  if (iVar10 == 0) goto LAB_0076d308;
                  iVar1 = iVar1 + 1;
                } while (iVar1 != iVar8);
                iVar1 = *(int *)(*(int *)(*(int *)(iStack_90 + 0x24) + 0x44) + iVar13 * 0x14);
              }
              uVar12 = 0;
              if (iVar1 != 0) {
                uVar12 = *(undefined4 *)(iVar1 + 0xc);
              }
              _ZN6glitch2os7Printer4logfENS_11E_LOG_LEVELEPKcz(3,iStack_84,pcVar18,uVar12);
              *(undefined4 *)(iStack_9c + 4) = 0;
              if (iVar9 + 1 == iStack_8c) {
                return piVar4;
              }
            }
            iVar9 = iVar9 + 1;
            iVar7 = iVar7 + 0xc;
            iVar1 = piVar4[8];
          } while( true );
        }
      }
      return piVar4;
    }
    if (uVar16 != 0) {
      _ZNSt6vectorIN6glitch7collada16SAnimationClipIDENS0_4core10SAllocatorIS2_LNS0_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_899
                (param_1 + 9,uVar16);
      iVar1 = param_1[8];
      iVar9 = *(int *)(iVar1 + 8);
      if (0 < iVar9) {
        iVar13 = 0;
        iVar7 = 0;
        while( true ) {
          uVar12 = _ZNK6glitch7collada20CAnimationDictionary18resolveAnimationIDEPKNS0_17CAnimationPackageEPKc
                             (param_1,param_3,*(undefined4 *)(*(int *)(iVar1 + 0xc) + iVar13 + 4));
          pcVar18 = *(char **)(*(int *)(param_1[8] + 0xc) + iVar13 + 8);
          if (pcVar18 == (char *)0x0) {
            local_2c = 0;
          }
          else if (*pcVar18 == '\0') {
            local_2c = 0;
          }
          else {
            local_2c = _ZNK6glitch7collada20CAnimationDictionary13resolveClipIDERKN5boost13intrusive_ptrINS0_13CAnimationSetEEEiPKc_part_130
                                 ((int *)(param_3 + 0x24),uVar12);
          }
          puVar2 = (undefined4 *)param_1[10];
          local_30 = uVar12;
          if (puVar2 == (undefined4 *)param_1[0xb]) {
            _ZNSt6vectorIN6glitch7collada16SAnimationClipIDENS0_4core10SAllocatorIS2_LNS0_6memory13E_MEMORY_HINTE0EEEE9push_backERKS2__part_1154_constprop_1339
                      (param_1 + 9,&local_30);
          }
          else {
            if (puVar2 != (undefined4 *)0x0) {
              *puVar2 = uVar12;
              puVar2[1] = local_2c;
            }
            param_1[10] = (int)(puVar2 + 2);
          }
          iVar7 = iVar7 + 1;
          iVar13 = iVar13 + 0xc;
          if (iVar7 == iVar9) break;
          iVar1 = param_1[8];
        }
      }
    }
  }
  else {
    param_1[7] = *(int *)(param_5 + 0x1c);
    _ZNSt6vectorIN6glitch7collada16SAnimationClipIDENS0_4core10SAllocatorIS2_LNS0_6memory13E_MEMORY_HINTE0EEEEaSERKS8_
              (param_1 + 9,param_5 + 0x24);
    iVar9 = param_1[8];
    iVar1 = *(int *)(iVar9 + 8);
    if (0 < iVar1) {
      iVar14 = 0;
      iVar7 = DAT_0076d088 + 0x76cd84;
      do {
        iVar10 = *(int *)(iVar9 + 0xc);
        iVar8 = *(int *)(param_1[7] + 8);
        pcVar18 = *(char **)(iVar10 + iVar13);
        puVar15 = *(undefined4 **)(param_1[7] + 0xc);
        puVar2 = puVar15;
        for (iVar9 = (iVar8 * 0xc >> 2) * -0x55555555; 0 < iVar9; iVar9 = (iVar9 - iVar11) + -1) {
          while( true ) {
            iVar11 = iVar9 >> 1;
            iVar17 = strcmp((char *)puVar2[iVar11 * 3],pcVar18);
            if (iVar17 < 0) break;
            iVar9 = iVar11;
            if (iVar11 == 0) goto LAB_0076ce14;
          }
          puVar2 = puVar2 + iVar11 * 3 + 3;
        }
LAB_0076ce14:
        if ((puVar15 + iVar8 * 3 == puVar2) || (iVar9 = strcmp((char *)*puVar2,pcVar18), iVar9 != 0)
           ) {
          iVar9 = -8;
        }
        else {
          iVar9 = ((int)puVar2 - (int)puVar15 >> 2) * 0x55555558;
        }
        iVar8 = _ZNK6glitch7collada20CAnimationDictionary18resolveAnimationIDEPKNS0_17CAnimationPackageEPKc
                          (param_1,param_3,*(undefined4 *)(iVar10 + iVar13 + 4));
        iVar10 = param_1[9] + iVar9;
        *(int *)(param_1[9] + iVar9) = iVar8;
        pcVar18 = *(char **)(*(int *)(param_1[8] + 0xc) + iVar13 + 8);
        if (pcVar18 == (char *)0x0) {
          iVar9 = 0;
LAB_0076cf04:
          *(int *)(iVar10 + 4) = iVar9;
        }
        else {
          iVar9 = 0;
          if (*pcVar18 == '\0') goto LAB_0076cf04;
          iVar11 = *(int *)(*(int *)(param_3 + 0x24) + 0x44);
          iVar9 = *(int *)(iVar11 + iVar8 * 0x14);
          iVar17 = *(int *)(*(int *)(*(int *)(iVar9 + 0x10) + 0x20) + 0x38);
          if (0 < iVar17) {
            iVar9 = 0;
            do {
              puVar2 = (undefined4 *)
                       _ZNK6glitch7collada16CColladaDatabase16getAnimationClipEi
                                 (iVar11 + iVar8 * 0x14,iVar9);
              iVar3 = strcmp(pcVar18,(char *)*puVar2);
              if (iVar3 == 0) goto LAB_0076cf04;
              iVar9 = iVar9 + 1;
            } while (iVar9 != iVar17);
            iVar9 = *(int *)(*(int *)(*(int *)(param_3 + 0x24) + 0x44) + iVar8 * 0x14);
          }
          uVar12 = 0;
          if (iVar9 != 0) {
            uVar12 = *(undefined4 *)(iVar9 + 0xc);
          }
          _ZN6glitch2os7Printer4logfENS_11E_LOG_LEVELEPKcz(3,iVar7,pcVar18,uVar12);
          *(undefined4 *)(iVar10 + 4) = 0;
        }
        if (iVar14 + 1 == iVar1) {
          return param_1;
        }
        iVar14 = iVar14 + 1;
        iVar13 = iVar13 + 0xc;
        iVar9 = param_1[8];
      } while( true );
    }
  }
  return param_1;
}


