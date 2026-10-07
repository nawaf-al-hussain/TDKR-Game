// _ZN13CZonesManager16LoadIndexZoneMapEPKc @ 002cd468

void _ZN13CZonesManager16LoadIndexZoneMapEPKc(int param_1)

{
  byte *pbVar1;
  void *pvVar2;
  int *piVar3;
  undefined4 uVar4;
  int *piVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  uint uVar9;
  uint *puVar10;
  uint **__n;
  uint uVar11;
  int iVar12;
  uint *unaff_r5;
  code *pcVar13;
  int iVar14;
  uint *unaff_r6;
  void *pvVar15;
  int *piVar16;
  uint *__dest;
  int iVar17;
  bool bVar18;
  uint *local_70;
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
  __dest = (uint *)local_70[-3];
  if (__dest != (uint *)0x0) {
    pvVar15 = (void *)(DAT_002cd9b4 + 0x2cd78c);
    puVar10 = (uint *)((int)local_70 + (int)((int)__dest + -1));
    unaff_r6 = __dest;
    do {
      pvVar2 = memchr(pvVar15,(int)(char)*puVar10,1);
      unaff_r6 = (uint *)((int)unaff_r6 + -1);
      unaff_r5 = (uint *)((int)puVar10 + -1);
      if (pvVar2 != (void *)0x0) {
        if (unaff_r6 < __dest) goto LAB_002cd490;
        break;
      }
      puVar10 = unaff_r5;
    } while (unaff_r6 != (uint *)0x0);
  }
  puVar10 = (uint *)((int)local_70 + (int)__dest);
LAB_002cd490:
  if (local_70 == puVar10) {
    unaff_r5 = *(uint **)(DAT_002cd9b8 + 0x2cd8c4);
    __dest = unaff_r5 + 3;
    goto LAB_002cd51c;
  }
  __n = (uint **)((int)puVar10 - (int)local_70);
  if ((uint **)0x3ffffffc < __n) goto LAB_002cd984;
  if (__n == (uint **)0x0 || (int)__n + 0x1dU < 0x1001) {
    unaff_r6 = (uint *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE((int)__n + 0xd,0);
    unaff_r6[1] = (uint)__n;
    unaff_r6[2] = 0;
    __dest = unaff_r6 + 3;
    if (__n != (uint **)0x1) goto LAB_002cd4fc;
    *(char *)(unaff_r6 + 3) = (char)*local_70;
  }
  else {
    uVar9 = (int)__n + (0x1000 - ((int)__n + 0x1dU & 0xfff));
    if (0x3ffffffb < uVar9) {
      uVar9 = 0x3ffffffc;
    }
    unaff_r6 = (uint *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(uVar9 + 0xd,0);
    __dest = unaff_r6 + 3;
    unaff_r6[1] = uVar9;
    unaff_r6[2] = 0;
LAB_002cd4fc:
    memcpy(__dest,local_70,(size_t)__n);
  }
  unaff_r5 = *(uint **)(DAT_002cd9a4 + 0x2cd518);
  if (unaff_r6 != unaff_r5) goto LAB_002cd990;
LAB_002cd51c:
  while( true ) {
    __n = &local_6c;
    local_6c = __dest;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (&local_70,__n);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev(__n);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (&local_68,&local_70);
    iVar7 = *(int *)((int)local_68 + -0xc);
    if (5 < 0x3ffffffcU - iVar7) break;
    _ZSt20__throw_length_errorPKc(DAT_002cd9c4 + 0x2cd984);
LAB_002cd984:
    _ZSt20__throw_length_errorPKc(DAT_002cd9c8 + 0x2cd990);
LAB_002cd990:
    *unaff_r6 = (uint)__n;
    unaff_r6[2] = 0;
    *(char *)((int)__dest + (int)__n) = '\0';
  }
  uVar9 = *(uint *)((int)local_68 + -8);
  uVar11 = iVar7 + 6;
  if ((uVar9 < uVar11) || (0 < *(int *)((int)local_68 + -4))) {
    pvVar15 = (void *)(DAT_002cd9a8 + 0x2cd588);
    if ((pvVar15 < local_68) || (pvVar2 = (void *)((int)local_68 + iVar7), pvVar2 < pvVar15)) {
      if ((uVar11 == uVar9) && (*(int *)((int)local_68 + -4) < 1)) {
        pvVar2 = (void *)((int)local_68 + iVar7);
        pvVar15 = (void *)(DAT_002cd9c0 + 0x2cd914);
      }
      else {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                  (&local_68,uVar11);
        pvVar15 = (void *)(DAT_002cd9ac + 0x2cd5b4);
        pvVar2 = (void *)((int)local_68 + *(int *)((int)local_68 + -0xc));
      }
    }
    else {
      iVar7 = (int)pvVar15 - (int)local_68;
      if ((uVar11 == uVar9) && (*(int *)((int)local_68 + -4) < 1)) {
        pvVar15 = (void *)((int)local_68 + iVar7);
      }
      else {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                  (&local_68,uVar11);
        pvVar2 = (void *)((int)local_68 + *(int *)((int)local_68 + -0xc));
        pvVar15 = (void *)((int)local_68 + iVar7);
      }
    }
  }
  else {
    pvVar2 = (void *)((int)local_68 + iVar7);
    pvVar15 = (void *)(DAT_002cd9bc + 0x2cd8d8);
  }
  memcpy(pvVar2,pvVar15,6);
  if ((uint *)((int)local_68 + -0xc) != unaff_r5) {
    *(uint *)((int)local_68 + -0xc) = uVar11;
    *(undefined4 *)((int)local_68 + -4) = 0;
    *(undefined1 *)((int)local_68 + uVar11) = 0;
  }
  piVar3 = (int *)_Z9GetDevicev();
  (**(code **)(**(int **)(*piVar3 + 0x28) + 0xc))(&local_64,*(int **)(*piVar3 + 0x28),local_68);
  *(undefined4 *)(param_1 + 0x60) = 0;
  if (local_64 == (int *)0x0) {
    *(undefined4 *)(param_1 + 0x60) = 0xffffffff;
  }
  else {
    uVar4 = (**(code **)(*local_64 + 0x20))();
    piVar5 = (int *)_ZnajPKci(uVar4,DAT_002cd9b0 + 0x2cd630,0x102);
    piVar3 = local_64;
    if (piVar5 != (int *)0x0) {
      pcVar13 = *(code **)(*local_64 + 0xc);
      uVar4 = (**(code **)(*local_64 + 0x20))(local_64);
      (*pcVar13)(piVar3,piVar5,uVar4);
      if (0 < *piVar5) {
        piVar16 = piVar5 + 1;
        piVar3 = (int *)((int)piVar16 + *piVar5 * 0xd);
        iVar7 = param_1 + 0x20;
        do {
          pbVar1 = (byte *)(piVar16 + 3);
          uVar9 = (uint)*pbVar1;
          iVar14 = *piVar16;
          bVar18 = uVar9 == 0;
          local_5c = piVar16[1];
          local_58 = piVar16[2];
          piVar16 = (int *)((int)piVar16 + 0xd);
          if (bVar18) {
            uVar9 = *(uint *)(param_1 + 0x60);
          }
          local_54 = (ushort)*pbVar1;
          if (bVar18) {
            *(uint *)(param_1 + 0x60) = uVar9 + 1;
          }
          local_40 = CONCAT22(local_40._2_2_,local_54);
          local_2c = local_40;
          iVar6 = *(int *)(param_1 + 0x24);
          iVar12 = iVar7;
          local_60 = iVar14;
          local_50 = iVar14;
          local_4c = iVar14;
          iStack_48 = local_5c;
          iStack_44 = local_58;
          local_38 = iVar14;
          iStack_34 = local_5c;
          iStack_30 = local_58;
          if (*(int *)(param_1 + 0x24) == 0) {
LAB_002cd820:
            iVar17 = *(int *)(param_1 + 0x28);
            if (iVar17 == iVar12) {
              if (iVar7 == iVar12) {
                bVar18 = true;
              }
              else {
                bVar18 = iVar14 < *(int *)(iVar12 + 0x10);
              }
              iVar6 = _Znwj(0x24);
              if ((undefined4 *)(iVar6 + 0x10) != (undefined4 *)0x0) {
                *(undefined4 *)(iVar6 + 0x10) = local_3c;
                *(int *)(iVar6 + 0x14) = local_38;
                *(int *)(iVar6 + 0x18) = iStack_34;
                *(int *)(iVar6 + 0x1c) = iStack_30;
                *(undefined4 *)(iVar6 + 0x20) = local_2c;
                *(int *)(iVar6 + 0x10) = iVar14;
              }
            }
            else {
              iVar6 = _ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(iVar12);
              iVar17 = iVar12;
              if (iVar14 <= *(int *)(iVar6 + 0x10)) goto LAB_002cd738;
LAB_002cd840:
              if (iVar7 == iVar17) {
                bVar18 = true;
              }
              else {
                bVar18 = iVar14 < *(int *)(iVar17 + 0x10);
              }
              iVar6 = _Znwj(0x24);
              if ((undefined4 *)(iVar6 + 0x10) != (undefined4 *)0x0) {
                *(undefined4 *)(iVar6 + 0x10) = local_3c;
                *(int *)(iVar6 + 0x14) = local_38;
                *(int *)(iVar6 + 0x18) = iStack_34;
                *(int *)(iVar6 + 0x1c) = iStack_30;
                *(undefined4 *)(iVar6 + 0x20) = local_2c;
                *(int *)(iVar6 + 0x10) = iVar14;
              }
            }
            _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
                      (bVar18,iVar6,iVar17,iVar7);
            *(int *)(param_1 + 0x30) = *(int *)(param_1 + 0x30) + 1;
          }
          else {
            do {
              iVar17 = iVar6;
              iVar8 = *(int *)(iVar17 + 0x10);
              if (iVar14 < iVar8) {
                iVar6 = *(int *)(iVar17 + 8);
              }
              else {
                iVar6 = *(int *)(iVar17 + 0xc);
              }
            } while (iVar6 != 0);
            iVar12 = iVar17;
            if (iVar14 < iVar8) goto LAB_002cd820;
            if (iVar8 < iVar14) goto LAB_002cd840;
          }
LAB_002cd738:
        } while (piVar16 != piVar3);
      }
      _ZdaPv(piVar5);
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


