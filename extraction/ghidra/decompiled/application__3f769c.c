// _ZN11Application14OnGLLiveClosedEv @ 003f769c

/* WARNING: Removing unreachable block (ram,0x00447f60) */
/* WARNING: Removing unreachable block (ram,0x002f8ae8) */
/* WARNING: Type propagation algorithm not settling */

byte * _ZN11Application14OnGLLiveClosedEv(void)

{
  int iVar1;
  size_t __n;
  char *__dest;
  undefined4 uVar2;
  byte *pbVar3;
  undefined4 uVar4;
  int *piVar5;
  int iVar6;
  char *__s;
  uint uVar7;
  undefined1 *puVar8;
  char *pcVar9;
  int iVar10;
  undefined4 in_r3;
  int iVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  int iVar16;
  int iVar17;
  undefined4 unaff_r4;
  uint uVar18;
  undefined4 unaff_r5;
  undefined4 unaff_r6;
  int *piVar19;
  undefined4 unaff_r7;
  uint extraout_r12;
  undefined4 unaff_lr;
  bool bVar20;
  undefined8 uVar21;
  
  piVar5 = (int *)_ZN12gxStateStack12CurrentStateEv(**(int **)(DAT_003f76d8 + 0x3f76ac) + 4);
  iVar6 = (**(code **)(*piVar5 + 8))(piVar5,0x17);
  if (iVar6 == 0) {
    return (byte *)0x0;
  }
  puVar8 = (undefined1 *)(DAT_00447f7c + 0x447e88);
  *(undefined1 *)(DAT_00447f78 + 0x447e84) = 0;
  *puVar8 = 0;
  piVar19 = *(int **)(DAT_00447f80 + 0x447ea0);
  _ZN12gxStateStack15ClearStateStackEv(*piVar19 + 4);
  *(undefined4 *)(DAT_00447f84 + 0x447ebc) = 0xffffffff;
  piVar5 = (int *)_Znwj(0xc4);
  _ZN11gxGameStateC1Ev();
  iVar6 = DAT_00447f88;
  piVar5[4] = 0;
  *(undefined1 *)((int)piVar5 + 0x15) = 1;
  piVar5[6] = 0;
  *piVar5 = iVar6 + 0x447ee8;
  _ZN7gameswf15CharacterHandleC1EPNS_9CharacterE(piVar5 + 7,0);
  _ZN7gameswf15CharacterHandleC1EPNS_9CharacterE(piVar5 + 0x1c,0);
  _ZN11gxGameState13ResetControlsEv(piVar5);
  _ZN12gxStateStack10ResetTouchEv(*piVar19 + 4);
  _ZN12gxStateStack9PushStateEP11gxGameState(*piVar19 + 4,piVar5);
  iVar6 = _ZN11Application11GetInstanceEv();
  pbVar3 = &__DT_SYMTAB[0x1e9].st_info + iVar6;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE9_M_mutateEjjj
            (pbVar3,0,*(undefined4 *)(*(int *)(&__DT_SYMTAB[0x1e9].st_info + iVar6) + -0xc),0);
  __s = (char *)(DAT_00447f8c + 0x447f5c);
  __n = strlen(__s);
  if (__n == 0) {
    return pbVar3;
  }
  pcVar9 = *(char **)pbVar3;
  iVar6 = *(int *)(pcVar9 + -0xc);
  bVar20 = __n == 0x3ffffffcU - iVar6;
  if (0x3ffffffcU - iVar6 <= __n && !bVar20) {
    uVar21 = _ZSt20__throw_length_errorPKc((int)&DAT_002f8ae4 + DAT_002f8ae8);
    iVar6 = (int)((ulonglong)uVar21 >> 0x20);
    uVar2 = (undefined4)uVar21;
                    /* WARNING: Could not recover jumptable at 0x002f8ae4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    if (!bVar20) {
      while( true ) {
        iVar1 = (int)((ulonglong)uVar21 >> 0x20);
        if (iVar6 == 0) break;
        iVar6 = *(int *)(iVar1 + 0xc);
        while (iVar6 != 0) {
          iVar17 = *(int *)(iVar6 + 0xc);
          while (iVar17 != 0) {
            iVar16 = *(int *)(iVar17 + 0xc);
            while (iVar16 != 0) {
              iVar15 = *(int *)(iVar16 + 0xc);
              while (iVar15 != 0) {
                iVar14 = *(int *)(iVar15 + 0xc);
                while (iVar14 != 0) {
                  iVar13 = *(int *)(iVar14 + 0xc);
                  while (iVar13 != 0) {
                    iVar12 = *(int *)(iVar13 + 0xc);
                    while (iVar12 != 0) {
                      iVar11 = *(int *)(iVar12 + 0xc);
                      while (iVar11 != 0) {
                        _ZNSt8_Rb_treeIP16AI_EventReceiverSt4pairIKS1_P11CGameObjectESt10_Select1stIS6_ESt4lessIS1_ESaIS6_EE8_M_eraseEPSt13_Rb_tree_nodeIS6_E
                                  (uVar2,*(undefined4 *)(iVar11 + 0xc));
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
              iVar15 = *(int *)(iVar16 + 8);
              _ZdlPv(iVar16);
              iVar16 = iVar15;
            }
            iVar16 = *(int *)(iVar17 + 8);
            _ZdlPv(iVar17);
            iVar17 = iVar16;
          }
          iVar17 = *(int *)(iVar6 + 8);
          _ZdlPv(iVar6);
          iVar6 = iVar17;
        }
        iVar6 = *(int *)(iVar1 + 8);
        uVar4 = _ZdlPv(iVar1);
        uVar21 = CONCAT44(iVar6,uVar4);
      }
      return (byte *)uVar21;
    }
    pbVar3 = (byte *)(*(code *)(iVar6 + (extraout_r12 >> 4 | extraout_r12 << 0x1c)))();
    return pbVar3;
  }
  uVar7 = *(uint *)(pcVar9 + -8);
  uVar18 = __n + iVar6;
  if ((uVar7 < uVar18) || (0 < *(int *)(pcVar9 + -4))) {
    if ((pcVar9 <= __s) && (__dest = pcVar9 + iVar6, __s <= __dest)) {
      iVar6 = (int)__s - (int)pcVar9;
      if ((uVar18 != uVar7) || (uVar7 = *(uint *)(pcVar9 + -4), 0 < (int)uVar7)) {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                  (pbVar3,uVar18,uVar7,pcVar9,in_r3,unaff_r4,unaff_r5,unaff_r6,unaff_r7,unaff_lr);
        pcVar9 = *(char **)pbVar3;
        __dest = pcVar9 + *(int *)(pcVar9 + -0xc);
      }
      __s = pcVar9 + iVar6;
      goto joined_r0x002f8aa0;
    }
    if ((uVar18 != uVar7) || (uVar7 = *(uint *)(pcVar9 + -4), 0 < (int)uVar7)) {
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7reserveEj_part_1341
                (pbVar3,uVar18,uVar7,pcVar9,in_r3,unaff_r4,unaff_r5,unaff_r6,unaff_r7,unaff_lr);
      __dest = (char *)(*(int *)pbVar3 + *(int *)(*(int *)pbVar3 + -0xc));
      goto joined_r0x002f8aa0;
    }
  }
  __dest = pcVar9 + iVar6;
joined_r0x002f8aa0:
  if (__n == 1) {
    *__dest = *__s;
  }
  else {
    memcpy(__dest,__s,__n);
  }
  iVar6 = *(int *)pbVar3;
  if (iVar6 + -0xc != *(int *)(DAT_002f8ae4 + 0x2f8a50)) {
    *(uint *)(iVar6 + -0xc) = uVar18;
    *(undefined4 *)(iVar6 + -4) = 0;
    *(undefined1 *)(iVar6 + uVar18) = 0;
  }
  return pbVar3;
}


