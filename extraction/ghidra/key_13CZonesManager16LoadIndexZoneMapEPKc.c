// _ZN13CZonesManager16LoadIndexZoneMapEPKc @ 002cd468

void _ZN13CZonesManager16LoadIndexZoneMapEPKc(int param_1)

{
  byte *pbVar1;
  uint *puVar2;
  void *pvVar3;
  int *piVar4;
  undefined4 uVar5;
  int *piVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  uint uVar10;
  char *pcVar11;
  int iVar12;
  uint *puVar13;
  code *pcVar14;
  int iVar15;
  void *pvVar16;
  int *piVar17;
  uint uVar18;
  uint *__dest;
  int iVar19;
  bool bVar20;
  char *local_70;
  uint *local_6c;
  void *local_68;
  int *local_64;
  int local_60;
  int local_5c;
  int local_58;
  ushort local_54;
  undefined2 uStack_52;
  int local_50;
  int local_4c;
  int iStack_48;
  int iStack_44;
  undefined4 local_40;
  undefined4 local_3c;
  int local_38;
  int iStack_34;
  int iStack_30;
  undefined4 local_2c;
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1896
            (&local_70);
  uVar18 = *(uint *)(local_70 + -0xc);
  if (uVar18 != 0) {
    pvVar16 = (void *)(DAT_002cd9b4 + 0x2cd78c);
    pcVar11 = local_70 + (uVar18 - 1);
    uVar10 = uVar18;
    do {
      pvVar3 = memchr(pvVar16,(int)*pcVar11,1);
      uVar10 = uVar10 - 1;
      if (pvVar3 != (void *)0x0) {
        if (uVar10 < uVar18) goto LAB_002cd490;
        break;
      }
      pcVar11 = pcVar11 + -1;
    } while (uVar10 != 0);
  }
  pcVar11 = local_70 + uVar18;
LAB_002cd490:
  if (local_70 == pcVar11) {
    puVar13 = *(uint **)(DAT_002cd9b8 + 0x2cd8c4);
    __dest = puVar13 + 3;
    goto LAB_002cd51c;
  }
  uVar18 = (int)pcVar11 - (int)local_70;
  if (0x3ffffffc < uVar18) {
                    /* WARNING: Subroutine does not return */
    _ZSt20__throw_length_errorPKc(DAT_002cd9c8 + 0x2cd990);
  }
  if (uVar18 == 0 || uVar18 + 0x1d < 0x1001) {
    puVar2 = (uint *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(uVar18 + 0xd,0);
    puVar2[1] = uVar18;
    puVar2[2] = 0;
    __dest = puVar2 + 3;
    if (uVar18 != 1) goto LAB_002cd4fc;
    *(char *)(puVar2 + 3) = *local_70;
  }
  else {
    uVar10 = (uVar18 + 0x1000) - (uVar18 + 0x1d & 0xfff);
    if (0x3ffffffb < uVar10) {
      uVar10 = 0x3ffffffc;
    }
    puVar2 = (uint *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(uVar10 + 0xd,0);
    __dest = puVar2 + 3;
    puVar2[1] = uVar10;
    puVar2[2] = 0;
LAB_002cd4fc:
    memcpy(__dest,local_70,uVar18);
  }
  puVar13 = *(uint **)(DAT_002cd9a4 + 0x2cd518);
  if (puVar2 != puVar13) {
    *puVar2 = uVar18;
    puVar2[2] = 0;
    *(undefined1 *)((int)__dest + uVar18) = 0;
  }
LAB_002cd51c:
  local_6c = __dest;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
            (&local_70,&local_6c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_6c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (&local_68,&local_70);
  iVar8 = *(int *)((int)local_68 + -0xc);
  if (0x3ffffffcU - iVar8 < 6) {
                    /* WARNING: Subroutine does not return */
    _ZSt20__throw_length_errorPKc(DAT_002cd9c4 + 0x2cd984);
  }
  uVar18 = *(uint *)((int)local_68 + -8);
  uVar10 = iVar8 + 6;
  if ((uVar18 < uVar10) || (0 < *(int *)((int)local_68 + -4))) {
    pvVar16 = (void *)(DAT_002cd9a8 + 0x2cd588);
    if ((pvVar16 < local_68) || (pvVar3 = (void *)((int)local_68 + iVar8), pvVar3 < pvVar16)) {
      if ((uVar10 == uVar18) && (*(int *)((int)local_68 + -4) < 1)) {
        pvVar3 = (void *)((int)local_68 + iVar8);
        pvVar16 = (void *)(DAT_002cd9c0 + 0x2cd914);
      }
      else {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                  (&local_68,uVar10);
        pvVar16 = (void *)(DAT_002cd9ac + 0x2cd5b4);
        pvVar3 = (void *)((int)local_68 + *(int *)((int)local_68 + -0xc));
      }
    }
    else {
      iVar8 = (int)pvVar16 - (int)local_68;
      if ((uVar10 == uVar18) && (*(int *)((int)local_68 + -4) < 1)) {
        pvVar16 = (void *)((int)local_68 + iVar8);
      }
      else {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                  (&local_68,uVar10);
        pvVar3 = (void *)((int)local_68 + *(int *)((int)local_68 + -0xc));
        pvVar16 = (void *)((int)local_68 + iVar8);
      }
    }
  }
  else {
    pvVar3 = (void *)((int)local_68 + iVar8);
    pvVar16 = (void *)(DAT_002cd9bc + 0x2cd8d8);
  }
  memcpy(pvVar3,pvVar16,6);
  if ((uint *)((int)local_68 + -0xc) != puVar13) {
    *(uint *)((int)local_68 + -0xc) = uVar10;
    *(undefined4 *)((int)local_68 + -4) = 0;
    *(undefined1 *)((int)local_68 + uVar10) = 0;
  }
  piVar4 = (int *)_Z9GetDevicev();
  (**(code **)(**(int **)(*piVar4 + 0x28) + 0xc))(&local_64,*(int **)(*piVar4 + 0x28),local_68);
  *(undefined4 *)(param_1 + 0x60) = 0;
  if (local_64 == (int *)0x0) {
    *(undefined4 *)(param_1 + 0x60) = 0xffffffff;
  }
  else {
    uVar5 = (**(code **)(*local_64 + 0x20))();
    piVar6 = (int *)_ZnajPKci(uVar5,DAT_002cd9b0 + 0x2cd630,0x102);
    piVar4 = local_64;
    if (piVar6 != (int *)0x0) {
      pcVar14 = *(code **)(*local_64 + 0xc);
      uVar5 = (**(code **)(*local_64 + 0x20))(local_64);
      (*pcVar14)(piVar4,piVar6,uVar5);
      if (0 < *piVar6) {
        piVar17 = piVar6 + 1;
        piVar4 = (int *)((int)piVar17 + *piVar6 * 0xd);
        iVar8 = param_1 + 0x20;
        do {
          pbVar1 = (byte *)(piVar17 + 3);
          uVar18 = (uint)*pbVar1;
          iVar15 = *piVar17;
          bVar20 = uVar18 == 0;
          local_5c = piVar17[1];
          local_58 = piVar17[2];
          piVar17 = (int *)((int)piVar17 + 0xd);
          if (bVar20) {
            uVar18 = *(uint *)(param_1 + 0x60);
          }
          local_54 = (ushort)*pbVar1;
          if (bVar20) {
            *(uint *)(param_1 + 0x60) = uVar18 + 1;
          }
          local_40 = CONCAT22(local_40._2_2_,local_54);
          local_2c = local_40;
          iVar7 = *(int *)(param_1 + 0x24);
          iVar12 = iVar8;
          local_60 = iVar15;
          local_50 = iVar15;
          local_4c = iVar15;
          iStack_48 = local_5c;
          iStack_44 = local_58;
          local_38 = iVar15;
          iStack_34 = local_5c;
          iStack_30 = local_58;
          if (*(int *)(param_1 + 0x24) == 0) {
LAB_002cd820:
            iVar19 = *(int *)(param_1 + 0x28);
            if (iVar19 == iVar12) {
              if (iVar8 == iVar12) {
                bVar20 = true;
              }
              else {
                bVar20 = iVar15 < *(int *)(iVar12 + 0x10);
              }
              iVar7 = _Znwj(0x24);
              if ((undefined4 *)(iVar7 + 0x10) != (undefined4 *)0x0) {
                *(undefined4 *)(iVar7 + 0x10) = local_3c;
                *(int *)(iVar7 + 0x14) = local_38;
                *(int *)(iVar7 + 0x18) = iStack_34;
                *(int *)(iVar7 + 0x1c) = iStack_30;
                *(undefined4 *)(iVar7 + 0x20) = local_2c;
                *(int *)(iVar7 + 0x10) = iVar15;
              }
            }
            else {
              iVar7 = _ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(iVar12);
              iVar19 = iVar12;
              if (iVar15 <= *(int *)(iVar7 + 0x10)) goto LAB_002cd738;
LAB_002cd840:
              if (iVar8 == iVar19) {
                bVar20 = true;
              }
              else {
                bVar20 = iVar15 < *(int *)(iVar19 + 0x10);
              }
              iVar7 = _Znwj(0x24);
              if ((undefined4 *)(iVar7 + 0x10) != (undefined4 *)0x0) {
                *(undefined4 *)(iVar7 + 0x10) = local_3c;
                *(int *)(iVar7 + 0x14) = local_38;
                *(int *)(iVar7 + 0x18) = iStack_34;
                *(int *)(iVar7 + 0x1c) = iStack_30;
                *(undefined4 *)(iVar7 + 0x20) = local_2c;
                *(int *)(iVar7 + 0x10) = iVar15;
              }
            }
            _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
                      (bVar20,iVar7,iVar19,iVar8);
            *(int *)(param_1 + 0x30) = *(int *)(param_1 + 0x30) + 1;
          }
          else {
            do {
              iVar19 = iVar7;
              iVar9 = *(int *)(iVar19 + 0x10);
              if (iVar15 < iVar9) {
                iVar7 = *(int *)(iVar19 + 8);
              }
              else {
                iVar7 = *(int *)(iVar19 + 0xc);
              }
            } while (iVar7 != 0);
            iVar12 = iVar19;
            if (iVar15 < iVar9) goto LAB_002cd820;
            if (iVar9 < iVar15) goto LAB_002cd840;
          }
LAB_002cd738:
        } while (piVar17 != piVar4);
      }
      _ZdaPv(piVar6);
    }
    if (local_64 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_68);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_70);
  return;
}

