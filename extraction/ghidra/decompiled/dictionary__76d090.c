// _ZN6glitch7collada20CAnimationDictionaryC1EPKNS0_17CAnimationPackageERKNS0_9anim_pack20SAnimationDictionaryEPKS1_ @ 0076d090

int * _ZN6glitch7collada20CAnimationDictionaryC1EPKNS0_17CAnimationPackageERKNS0_9anim_pack20SAnimationDictionaryEPKS1_
                (int *param_1,int param_2,int *param_3,int param_4)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  int iVar4;
  int *piVar5;
  int iVar6;
  undefined4 uVar7;
  undefined4 extraout_r3;
  int iVar8;
  undefined4 *puVar9;
  uint uVar10;
  int iVar11;
  char *pcVar12;
  int iVar13;
  undefined1 *puVar14;
  bool bVar15;
  undefined8 uVar16;
  undefined1 auStack_50 [4];
  int local_4c;
  undefined4 *local_48;
  undefined4 *local_44;
  int local_40;
  int local_3c;
  int *local_38;
  int local_34;
  undefined4 local_30;
  undefined4 local_2c;
  
  puVar14 = auStack_50;
  iVar13 = *(int *)(param_2 + 0xc);
  iVar1 = DAT_0076d484 + 0x76d0c8;
  iVar4 = DAT_0076d484 + 0x76d0ec;
  param_1[0xd] = 0;
  *param_1 = iVar1;
  param_1[0xc] = iVar4;
  param_1[2] = iVar13;
  local_40 = param_2;
  if (iVar13 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar13 + 4);
  }
  iVar1 = DAT_0076d48c;
  iVar8 = 0;
  iVar4 = *(int *)(local_40 + 0x10);
  iVar13 = DAT_0076d488 + 0x76d104;
  *param_1 = DAT_0076d48c + 0x76d114;
  param_1[1] = iVar13;
  param_1[8] = (int)param_3;
  local_38 = (int *)(local_40 + 0x24);
  iVar13 = *param_3;
  param_1[3] = iVar4;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 0;
  param_1[0xc] = iVar1 + 0x76d138;
  param_1[9] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[1] = iVar13;
  if (param_4 == 0) {
    uVar10 = param_3[2];
    param_1[7] = (int)param_3;
    bVar15 = uVar10 == 0x1fffffff;
    if (0x1fffffff < uVar10) {
      uVar16 = _ZSt20__throw_length_errorPKc((int)&DAT_0076d484 + DAT_0076d494);
      piVar5 = (int *)((ulonglong)uVar16 >> 0x20);
      piVar3 = (int *)uVar16;
      if (bVar15) {
        puVar14 = (undefined1 *)
                  ((int)(ZEXT48(auStack_50) + (ulonglong)uVar10 >> 0x20) + (int)piVar3 * -0x400);
      }
      *(int **)(puVar14 + -4) = &DAT_0076d484;
      *(undefined4 *)(puVar14 + -8) = 0;
      *(int **)(puVar14 + -0xc) = param_1;
      *(undefined4 *)(puVar14 + -0x10) = extraout_r3;
      iVar4 = *piVar5;
      iVar1 = piVar3[9];
      *piVar3 = iVar4;
      *(int *)((int)piVar3 + *(int *)(iVar4 + -0xc)) = piVar5[3];
      if (iVar1 != 0) {
        _Z10GlitchFreePv();
      }
      _ZN6glitch7collada16CColladaDatabaseD1Ev(piVar3 + 2);
      iVar1 = piVar5[1];
      *piVar3 = iVar1;
      *(int *)((int)piVar3 + *(int *)(iVar1 + -0xc)) = piVar5[2];
      return piVar3;
    }
    if (uVar10 != 0) {
      _ZNSt6vectorIN6glitch7collada16SAnimationClipIDENS0_4core10SAllocatorIS2_LNS0_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_899
                (param_1 + 9,uVar10);
      piVar3 = local_38;
      iVar1 = local_40;
      iVar4 = param_1[8];
      iVar13 = *(int *)(iVar4 + 8);
      if (0 < iVar13) {
        iVar8 = 0;
        iVar6 = 0;
        while( true ) {
          uVar7 = _ZNK6glitch7collada20CAnimationDictionary18resolveAnimationIDEPKNS0_17CAnimationPackageEPKc
                            (param_1,iVar1,*(undefined4 *)(*(int *)(iVar4 + 0xc) + iVar8 + 4));
          pcVar12 = *(char **)(*(int *)(param_1[8] + 0xc) + iVar8 + 8);
          if (pcVar12 == (char *)0x0) {
            local_2c = 0;
          }
          else if (*pcVar12 == '\0') {
            local_2c = 0;
          }
          else {
            local_2c = _ZNK6glitch7collada20CAnimationDictionary13resolveClipIDERKN5boost13intrusive_ptrINS0_13CAnimationSetEEEiPKc_part_130
                                 (piVar3,uVar7);
          }
          puVar9 = (undefined4 *)param_1[10];
          local_30 = uVar7;
          if (puVar9 == (undefined4 *)param_1[0xb]) {
            _ZNSt6vectorIN6glitch7collada16SAnimationClipIDENS0_4core10SAllocatorIS2_LNS0_6memory13E_MEMORY_HINTE0EEEE9push_backERKS2__part_1154_constprop_1339
                      (param_1 + 9,&local_30);
          }
          else {
            if (puVar9 != (undefined4 *)0x0) {
              *puVar9 = uVar7;
              puVar9[1] = local_2c;
            }
            param_1[10] = (int)(puVar9 + 2);
          }
          iVar6 = iVar6 + 1;
          iVar8 = iVar8 + 0xc;
          if (iVar6 == iVar13) break;
          iVar4 = param_1[8];
        }
      }
    }
  }
  else {
    param_1[7] = *(int *)(param_4 + 0x1c);
    _ZNSt6vectorIN6glitch7collada16SAnimationClipIDENS0_4core10SAllocatorIS2_LNS0_6memory13E_MEMORY_HINTE0EEEEaSERKS8_
              (param_1 + 9,param_4 + 0x24);
    iVar1 = param_1[8];
    local_3c = *(int *)(iVar1 + 8);
    if (0 < local_3c) {
      iVar4 = 0;
      local_34 = DAT_0076d490 + 0x76d188;
      do {
        iVar13 = *(int *)(param_1[7] + 8);
        local_4c = *(int *)(iVar1 + 0xc) + iVar8;
        pcVar12 = *(char **)(*(int *)(iVar1 + 0xc) + iVar8);
        puVar9 = *(undefined4 **)(param_1[7] + 0xc);
        local_48 = puVar9 + iVar13 * 3;
        local_44 = puVar9;
        for (iVar1 = (iVar13 * 0xc >> 2) * -0x55555555; 0 < iVar1; iVar1 = (iVar1 - iVar13) + -1) {
          while( true ) {
            iVar13 = iVar1 >> 1;
            iVar6 = strcmp((char *)puVar9[iVar13 * 3],pcVar12);
            if (iVar6 < 0) break;
            iVar1 = iVar13;
            if (iVar13 == 0) goto LAB_0076d218;
          }
          puVar9 = puVar9 + iVar13 * 3 + 3;
        }
LAB_0076d218:
        if ((local_48 == puVar9) || (iVar1 = strcmp((char *)*puVar9,pcVar12), iVar1 != 0)) {
          iVar1 = -8;
        }
        else {
          iVar1 = ((int)puVar9 - (int)local_44 >> 2) * 0x55555558;
        }
        iVar13 = _ZNK6glitch7collada20CAnimationDictionary18resolveAnimationIDEPKNS0_17CAnimationPackageEPKc
                           (param_1,local_40,*(undefined4 *)(local_4c + 4));
        local_4c = param_1[9] + iVar1;
        *(int *)(param_1[9] + iVar1) = iVar13;
        pcVar12 = *(char **)(*(int *)(param_1[8] + 0xc) + iVar8 + 8);
        if (pcVar12 == (char *)0x0) {
          iVar1 = 0;
LAB_0076d308:
          *(int *)(local_4c + 4) = iVar1;
          if (iVar4 + 1 == local_3c) {
            return param_1;
          }
        }
        else {
          iVar1 = 0;
          if (*pcVar12 == '\0') goto LAB_0076d308;
          iVar6 = *(int *)(*local_38 + 0x44);
          iVar1 = *(int *)(iVar6 + iVar13 * 0x14);
          iVar11 = *(int *)(*(int *)(*(int *)(iVar1 + 0x10) + 0x20) + 0x38);
          if (0 < iVar11) {
            iVar1 = 0;
            do {
              puVar9 = (undefined4 *)
                       _ZNK6glitch7collada16CColladaDatabase16getAnimationClipEi
                                 (iVar6 + iVar13 * 0x14,iVar1);
              iVar2 = strcmp(pcVar12,(char *)*puVar9);
              if (iVar2 == 0) goto LAB_0076d308;
              iVar1 = iVar1 + 1;
            } while (iVar1 != iVar11);
            iVar1 = *(int *)(*(int *)(*(int *)(local_40 + 0x24) + 0x44) + iVar13 * 0x14);
          }
          uVar7 = 0;
          if (iVar1 != 0) {
            uVar7 = *(undefined4 *)(iVar1 + 0xc);
          }
          _ZN6glitch2os7Printer4logfENS_11E_LOG_LEVELEPKcz(3,local_34,pcVar12,uVar7);
          *(undefined4 *)(local_4c + 4) = 0;
          if (iVar4 + 1 == local_3c) {
            return param_1;
          }
        }
        iVar4 = iVar4 + 1;
        iVar8 = iVar8 + 0xc;
        iVar1 = param_1[8];
      } while( true );
    }
  }
  return param_1;
}


