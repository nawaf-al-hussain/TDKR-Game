// _ZN11Application15SetExitRootMenuEPc @ 003f6ae8

/* WARNING: Removing unreachable block (ram,0x002f8ae8) */
/* WARNING: Type propagation algorithm not settling */

byte * _ZN11Application15SetExitRootMenuEPc
                 (int param_1,char *param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  size_t __n;
  char *__dest;
  undefined4 uVar2;
  byte *pbVar3;
  undefined4 uVar4;
  int iVar5;
  uint uVar6;
  char *pcVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  undefined4 unaff_r4;
  uint uVar16;
  undefined4 unaff_r5;
  uint extraout_r12;
  bool bVar17;
  undefined8 uVar18;
  
  pbVar3 = &__DT_SYMTAB[0x1e9].st_info + param_1;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE9_M_mutateEjjj
            (pbVar3,0,*(undefined4 *)(*(int *)(&__DT_SYMTAB[0x1e9].st_info + param_1) + -0xc),0,
             param_4);
  __n = strlen(param_2);
  if (__n == 0) {
    return pbVar3;
  }
  pcVar7 = *(char **)pbVar3;
  iVar5 = *(int *)(pcVar7 + -0xc);
  bVar17 = __n == 0x3ffffffcU - iVar5;
  if (0x3ffffffcU - iVar5 <= __n && !bVar17) {
    uVar18 = _ZSt20__throw_length_errorPKc((int)&DAT_002f8ae4 + DAT_002f8ae8);
    iVar5 = (int)((ulonglong)uVar18 >> 0x20);
    uVar2 = (undefined4)uVar18;
                    /* WARNING: Could not recover jumptable at 0x002f8ae4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    if (!bVar17) {
      while( true ) {
        iVar1 = (int)((ulonglong)uVar18 >> 0x20);
        if (iVar5 == 0) break;
        iVar5 = *(int *)(iVar1 + 0xc);
        while (iVar5 != 0) {
          iVar15 = *(int *)(iVar5 + 0xc);
          while (iVar15 != 0) {
            iVar14 = *(int *)(iVar15 + 0xc);
            while (iVar14 != 0) {
              iVar13 = *(int *)(iVar14 + 0xc);
              while (iVar13 != 0) {
                iVar12 = *(int *)(iVar13 + 0xc);
                while (iVar12 != 0) {
                  iVar11 = *(int *)(iVar12 + 0xc);
                  while (iVar11 != 0) {
                    iVar10 = *(int *)(iVar11 + 0xc);
                    while (iVar10 != 0) {
                      iVar9 = *(int *)(iVar10 + 0xc);
                      while (iVar9 != 0) {
                        _ZNSt8_Rb_treeIP16AI_EventReceiverSt4pairIKS1_P11CGameObjectESt10_Select1stIS6_ESt4lessIS1_ESaIS6_EE8_M_eraseEPSt13_Rb_tree_nodeIS6_E
                                  (uVar2,*(undefined4 *)(iVar9 + 0xc));
                        iVar8 = *(int *)(iVar9 + 8);
                        _ZdlPv(iVar9);
                        iVar9 = iVar8;
                      }
                      iVar9 = *(int *)(iVar10 + 8);
                      _ZdlPv(iVar10);
                      iVar10 = iVar9;
                    }
                    iVar10 = *(int *)(iVar11 + 8);
                    _ZdlPv(iVar11);
                    iVar11 = iVar10;
                  }
                  iVar11 = *(int *)(iVar12 + 8);
                  _ZdlPv(iVar12);
                  iVar12 = iVar11;
                }
                iVar12 = *(int *)(iVar13 + 8);
                _ZdlPv(iVar13);
                iVar13 = iVar12;
              }
              iVar13 = *(int *)(iVar14 + 8);
              _ZdlPv(iVar14);
              iVar14 = iVar13;
            }
            iVar14 = *(int *)(iVar15 + 8);
            _ZdlPv(iVar15);
            iVar15 = iVar14;
          }
          iVar15 = *(int *)(iVar5 + 8);
          _ZdlPv(iVar5);
          iVar5 = iVar15;
        }
        iVar5 = *(int *)(iVar1 + 8);
        uVar4 = _ZdlPv(iVar1);
        uVar18 = CONCAT44(iVar5,uVar4);
      }
      return (byte *)uVar18;
    }
    pbVar3 = (byte *)(*(code *)(iVar5 + (extraout_r12 >> 4 | extraout_r12 << 0x1c)))();
    return pbVar3;
  }
  uVar6 = *(uint *)(pcVar7 + -8);
  uVar16 = __n + iVar5;
  if ((uVar6 < uVar16) || (0 < *(int *)(pcVar7 + -4))) {
    if ((pcVar7 <= param_2) && (__dest = pcVar7 + iVar5, param_2 <= __dest)) {
      iVar5 = (int)param_2 - (int)pcVar7;
      if ((uVar16 != uVar6) || (uVar6 = *(uint *)(pcVar7 + -4), 0 < (int)uVar6)) {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                  (pbVar3,uVar16,uVar6,pcVar7,param_4,unaff_r4,unaff_r5);
        pcVar7 = *(char **)pbVar3;
        __dest = pcVar7 + *(int *)(pcVar7 + -0xc);
      }
      param_2 = pcVar7 + iVar5;
      goto joined_r0x002f8aa0;
    }
    if ((uVar16 != uVar6) || (uVar6 = *(uint *)(pcVar7 + -4), 0 < (int)uVar6)) {
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                (pbVar3,uVar16,uVar6,pcVar7,param_4,unaff_r4,unaff_r5);
      __dest = (char *)(*(int *)pbVar3 + *(int *)(*(int *)pbVar3 + -0xc));
      goto joined_r0x002f8aa0;
    }
  }
  __dest = pcVar7 + iVar5;
joined_r0x002f8aa0:
  if (__n == 1) {
    *__dest = *param_2;
  }
  else {
    memcpy(__dest,param_2,__n);
  }
  iVar5 = *(int *)pbVar3;
  if (iVar5 + -0xc != *(int *)(DAT_002f8ae4 + 0x2f8a50)) {
    *(uint *)(iVar5 + -0xc) = uVar16;
    *(undefined4 *)(iVar5 + -4) = 0;
    *(undefined1 *)(iVar5 + uVar16) = 0;
  }
  return pbVar3;
}


