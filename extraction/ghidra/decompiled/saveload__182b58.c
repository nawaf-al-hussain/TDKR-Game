// _ZN14CScriptGlobals14SaveLoadGlobalEP13CMemoryStream @ 00182b58

/* WARNING: Restarted to delay deadcode elimination for space: stack */

void _ZN14CScriptGlobals14SaveLoadGlobalEP13CMemoryStream(int param_1,int param_2)

{
  int iVar1;
  undefined4 uVar2;
  void *pvVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  uint uVar9;
  uint uVar10;
  uint uVar11;
  int *piVar12;
  uint *puVar13;
  int iVar14;
  uint uVar15;
  size_t sVar16;
  void *pvVar17;
  uint uVar18;
  int iVar19;
  uint *puVar20;
  void *pvVar21;
  int extraout_r12;
  bool bVar22;
  byte bVar23;
  uint uStack_e4;
  undefined4 uStack_e0;
  uint auStack_dc [2];
  uint *puStack_d4;
  uint *puStack_d0;
  undefined4 uStack_cc;
  int *piStack_c4;
  int iStack_c0;
  undefined4 uStack_bc;
  int iStack_b8;
  uint uStack_b4;
  int iStack_b0;
  int iStack_ac;
  int iStack_a8;
  int *piStack_a4;
  void *local_a0;
  void **local_9c;
  int local_98;
  size_t local_94;
  uint local_90;
  int local_8c;
  int local_84;
  undefined4 local_80;
  undefined1 auStack_7c [4];
  undefined4 local_78;
  void *local_74 [2];
  void *local_6c [2];
  void *local_64 [2];
  int local_5c [2];
  int local_54 [2];
  int local_4c [2];
  void *local_44;
  undefined4 *local_40;
  undefined4 *local_3c;
  undefined1 auStack_38 [4];
  int local_34;
  undefined4 local_30;
  undefined4 local_2c;
  
  pvVar17 = (void *)(param_1 + 4);
  _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE8_M_eraseEPSt13_Rb_tree_nodeISB_E
            (param_1,*(undefined4 *)(param_1 + 8));
  *(void **)(param_1 + 0xc) = pvVar17;
  *(undefined4 *)(param_1 + 8) = 0;
  *(void **)(param_1 + 0x10) = pvVar17;
  *(undefined4 *)(param_1 + 0x14) = 0;
  iVar1 = _ZN13CMemoryStream9ReadShortEv(param_2);
  if (0 < iVar1) {
    sVar16 = 1;
    local_94 = iVar1 + 1;
    local_98 = *(int *)(DAT_00183378 + 0x182bb0) + 0xc;
    do {
      local_84 = local_98;
      _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,&local_84);
      uVar2 = _ZN13CMemoryStream7ReadIntEv(param_2);
      pvVar21 = pvVar17;
      pvVar3 = *(void **)(param_1 + 8);
      while (pvVar3 != (void *)0x0) {
        iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                          ((int)pvVar3 + 0x10,&local_84);
        if (iVar1 < 0) {
          pvVar3 = *(void **)((int)pvVar3 + 0xc);
        }
        else {
          pvVar21 = pvVar3;
          pvVar3 = *(void **)((int)pvVar3 + 8);
        }
      }
      if ((pvVar17 == pvVar21) ||
         (iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                            (&local_84,(int)pvVar21 + 0x10), iVar1 < 0)) {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                  (auStack_7c,&local_84);
        local_78 = 0;
        if (pvVar17 == pvVar21) {
          if (*(int *)(param_1 + 0x14) != 0) {
            pvVar3 = *(void **)(param_1 + 0x10);
            iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                              ((int)pvVar3 + 0x10,auStack_7c);
            if (iVar1 < 0) {
              if (pvVar17 == pvVar3) {
                local_90 = 1;
              }
              else {
                local_90 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                                     (auStack_7c,(int)pvVar3 + 0x10);
                local_90 = local_90 >> 0x1f;
              }
              pvVar21 = (void *)_Znwj(0x18);
              uVar15 = local_90;
              if ((int)pvVar21 + 0x10 != 0) {
                _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                          ((int)pvVar21 + 0x10,auStack_7c);
                *(undefined4 *)((int)pvVar21 + 0x14) = local_78;
                uVar15 = local_90;
              }
LAB_001830f4:
              _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
                        (uVar15,pvVar21,pvVar3,pvVar17);
              *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
              goto LAB_00182ce8;
            }
          }
          _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB__constprop_3064
                    (local_74,param_1,auStack_7c);
          pvVar21 = local_74[0];
        }
        else {
          iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                            (auStack_7c,(int)pvVar21 + 0x10);
          if (iVar1 < 0) {
            if (*(void **)(param_1 + 0xc) == pvVar21) {
              pvVar21 = (void *)_ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE10_M_insert_EPKSt18_Rb_tree_node_baseSK_RKSB__constprop_3297
                                          (param_1,pvVar21,pvVar21,auStack_7c);
            }
            else {
              local_a0 = (void *)_ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(pvVar21);
              iVar19 = (int)local_a0 + 0x10;
              iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                                (iVar19,auStack_7c);
              if (iVar1 < 0) {
                if (*(int *)((int)local_a0 + 0xc) == 0) {
                  if (pvVar17 == local_a0) {
                    uVar15 = 1;
                  }
                  else {
                    uVar15 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                                       (auStack_7c,iVar19);
                    uVar15 = uVar15 >> 0x1f;
                  }
                  pvVar21 = (void *)_Znwj(0x18);
                  pvVar3 = local_a0;
                  if ((int)pvVar21 + 0x10 != 0) {
                    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                              ((int)pvVar21 + 0x10,auStack_7c,local_a0);
                    *(undefined4 *)((int)pvVar21 + 0x14) = local_78;
                    pvVar3 = local_a0;
                  }
                  goto LAB_001830f4;
                }
                pvVar3 = (void *)_Znwj(0x18);
                if ((int)pvVar3 + 0x10 != 0) {
                  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                            ((int)pvVar3 + 0x10,auStack_7c);
                  *(undefined4 *)((int)pvVar3 + 0x14) = local_78;
                }
                _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
                          (1,pvVar3,pvVar21,pvVar17);
                *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
                pvVar21 = pvVar3;
              }
              else {
                _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB__constprop_3064
                          (local_6c,param_1,auStack_7c);
                pvVar21 = local_6c[0];
              }
            }
          }
          else {
            iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                              ((int)pvVar21 + 0x10,auStack_7c);
            if (iVar1 < 0) {
              if (*(void **)(param_1 + 0x10) == pvVar21) {
                pvVar21 = (void *)_ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE10_M_insert_EPKSt18_Rb_tree_node_baseSK_RKSB__constprop_3297
                                            (param_1,0,pvVar21,auStack_7c);
              }
              else {
                pvVar3 = (void *)_ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(pvVar21);
                iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                                  (auStack_7c,(int)pvVar3 + 0x10);
                if (iVar1 < 0) {
                  if (*(int *)((int)pvVar21 + 0xc) != 0) {
                    pvVar21 = (void *)_Znwj(0x18);
                    if ((int)pvVar21 + 0x10 != 0) {
                      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                                ((int)pvVar21 + 0x10,auStack_7c);
                      *(undefined4 *)((int)pvVar21 + 0x14) = local_78;
                    }
                    uVar15 = 1;
                    goto LAB_001830f4;
                  }
                  pvVar21 = (void *)_ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE10_M_insert_EPKSt18_Rb_tree_node_baseSK_RKSB__constprop_3297
                                              (param_1,0,pvVar21,auStack_7c);
                }
                else {
                  _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE16_M_insert_uniqueERKSB__constprop_3064
                            (local_64,param_1,auStack_7c);
                  pvVar21 = local_64[0];
                }
              }
            }
          }
        }
LAB_00182ce8:
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (auStack_7c);
      }
      *(undefined4 *)((int)pvVar21 + 0x14) = uVar2;
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (&local_84);
      sVar16 = sVar16 + 1;
    } while (sVar16 != local_94);
  }
  local_8c = param_1 + 0x18;
  iVar1 = _ZN13CMemoryStream9ReadShortEv(param_2);
  iVar19 = param_1 + 0x1c;
  _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_St6vectorIiSaIiEEESt10_Select1stISE_ESt4lessIS8_ESaISE_EE8_M_eraseEPSt13_Rb_tree_nodeISE_E
            (local_8c,*(undefined4 *)(param_1 + 0x20));
  *(int *)(param_1 + 0x24) = iVar19;
  *(undefined4 *)(param_1 + 0x20) = 0;
  *(int *)(param_1 + 0x28) = iVar19;
  *(undefined4 *)(param_1 + 0x2c) = 0;
  if (0 < iVar1) {
    local_90 = iVar1 + 1;
    piVar12 = &local_84;
    iVar1 = 1;
    local_9c = &local_44;
    local_98 = *(int *)(DAT_0018337c + 0x182d74);
    do {
      local_44 = (void *)0x0;
      local_84 = local_98 + 0xc;
      local_40 = (undefined4 *)0x0;
      local_3c = (undefined4 *)0x0;
      _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,piVar12);
      iVar4 = _ZN13CMemoryStream9ReadShortEv(param_2);
      if (0 < iVar4) {
        iVar14 = 0;
        do {
          while (local_80 = _ZN13CMemoryStream7ReadIntEv(param_2), local_40 != local_3c) {
            iVar14 = iVar14 + 1;
            if (local_40 != (undefined4 *)0x0) {
              *local_40 = local_80;
            }
            local_40 = local_40 + 1;
            if (iVar4 <= iVar14) goto LAB_00182e04;
          }
          iVar14 = iVar14 + 1;
          _ZNSt6vectorIiSaIiEE9push_backERKi_part_2184(&local_44,&local_80);
        } while (iVar14 < iVar4);
      }
LAB_00182e04:
      iVar4 = iVar19;
      iVar14 = *(int *)(param_1 + 0x20);
      while (iVar14 != 0) {
        iVar5 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                          (iVar14 + 0x10,piVar12);
        if (iVar5 < 0) {
          iVar14 = *(int *)(iVar14 + 0xc);
        }
        else {
          iVar4 = iVar14;
          iVar14 = *(int *)(iVar14 + 8);
        }
      }
      if ((iVar19 == iVar4) ||
         (iVar14 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                             (piVar12,iVar4 + 0x10), iVar14 < 0)) {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                  (auStack_38,piVar12);
        local_34 = 0;
        local_2c = 0;
        local_30 = 0;
        if (iVar19 == iVar4) {
          if (*(int *)(param_1 + 0x2c) != 0) {
            iVar4 = *(int *)(param_1 + 0x28);
            iVar14 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                               (iVar4 + 0x10,auStack_38);
            if (iVar14 < 0) goto LAB_0018314c;
          }
          _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_St6vectorIiSaIiEEESt10_Select1stISE_ESt4lessIS8_ESaISE_EE16_M_insert_uniqueERKSE__constprop_3380
                    (local_5c,local_8c,auStack_38);
          iVar4 = local_5c[0];
LAB_00182edc:
          if (local_34 != 0) {
            _ZdlPv();
          }
        }
        else {
          iVar14 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                             (auStack_38,iVar4 + 0x10);
          if (iVar14 < 0) {
            iVar14 = iVar4;
            if (*(int *)(param_1 + 0x24) == iVar4) {
LAB_00182ec4:
              iVar4 = _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_St6vectorIiSaIiEEESt10_Select1stISE_ESt4lessIS8_ESaISE_EE10_M_insert_EPKSt18_Rb_tree_node_baseSN_RKSE__constprop_3261
                                (local_8c,iVar14,iVar14,auStack_38);
            }
            else {
              iVar4 = _ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(iVar4);
              iVar5 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                                (iVar4 + 0x10,auStack_38);
              if (iVar5 < 0) {
                if (*(int *)(iVar4 + 0xc) != 0) goto LAB_00182ec4;
                iVar4 = _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_St6vectorIiSaIiEEESt10_Select1stISE_ESt4lessIS8_ESaISE_EE10_M_insert_EPKSt18_Rb_tree_node_baseSN_RKSE__constprop_3261
                                  (local_8c,0,iVar4,auStack_38);
              }
              else {
                _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_St6vectorIiSaIiEEESt10_Select1stISE_ESt4lessIS8_ESaISE_EE16_M_insert_uniqueERKSE__constprop_3380
                          (local_54,local_8c,auStack_38);
                iVar4 = local_54[0];
              }
            }
            goto LAB_00182edc;
          }
          iVar14 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                             (iVar4 + 0x10,auStack_38);
          if (iVar14 < 0) {
            if (*(int *)(param_1 + 0x28) != iVar4) {
              iVar14 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar4);
              iVar5 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                                (auStack_38,iVar14 + 0x10);
              if (-1 < iVar5) {
                _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_St6vectorIiSaIiEEESt10_Select1stISE_ESt4lessIS8_ESaISE_EE16_M_insert_uniqueERKSE__constprop_3380
                          (local_4c,local_8c,auStack_38);
                iVar4 = local_4c[0];
                goto LAB_00182edc;
              }
              if (*(int *)(iVar4 + 0xc) != 0) goto LAB_00182ec4;
            }
LAB_0018314c:
            iVar4 = _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_St6vectorIiSaIiEEESt10_Select1stISE_ESt4lessIS8_ESaISE_EE10_M_insert_EPKSt18_Rb_tree_node_baseSN_RKSE__constprop_3261
                              (local_8c,0,iVar4,auStack_38);
            goto LAB_00182edc;
          }
        }
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (auStack_38);
      }
      if (local_9c != (void **)(iVar4 + 0x14)) {
        pvVar17 = *(void **)(iVar4 + 0x14);
        iVar14 = (int)local_40 - (int)local_44;
        uVar15 = iVar14 >> 2;
        if ((uint)(*(int *)(iVar4 + 0x1c) - (int)pvVar17 >> 2) < uVar15) {
          if (uVar15 == 0) {
            pvVar17 = (void *)0x0;
            local_94 = 0;
          }
          else {
            bVar23 = 0x3ffffffe < uVar15;
            bVar22 = uVar15 == 0x3fffffff;
            if (0x3fffffff < uVar15) {
              iVar5 = _ZSt17__throw_bad_allocv();
              if (bVar22) {
                param_2 = iVar1 + extraout_r12 * 4 + (uint)bVar23;
                piVar12 = (int *)(iVar1 + (iVar14 >> 0x1f) + (uint)bVar23);
              }
              piStack_a4 = &DAT_00183378;
              uStack_bc = 0;
              piStack_c4 = piVar12;
              iStack_c0 = param_2;
              iStack_b8 = iVar4;
              uStack_b4 = uVar15;
              iStack_b0 = iVar1;
              iStack_ac = param_1;
              iStack_a8 = iVar19;
              _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_iESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE8_M_eraseEPSt13_Rb_tree_nodeIS4_E
                        (iVar5,*(undefined4 *)(iVar5 + 8));
              uVar15 = iVar5 + 4;
              *(undefined4 *)(iVar5 + 8) = 0;
              *(uint *)(iVar5 + 0xc) = uVar15;
              *(uint *)(iVar5 + 0x10) = uVar15;
              *(undefined4 *)(iVar5 + 0x14) = 0;
              puStack_d4 = (uint *)0x0;
              puStack_d0 = (uint *)0x0;
              uStack_cc = 0;
              uVar2 = _ZN6CLevel8GetLevelEv();
              _ZN6CLevel19GetObjects_fromTypeEPSt6vectorIP11CGameObjectSaIS2_EEi
                        (uVar2,&puStack_d4,0x4c727);
              puVar13 = puStack_d4;
              puVar20 = puStack_d0;
              if (puStack_d4 == puStack_d0) goto LAB_001834e0;
              goto LAB_001833e8;
            }
            local_94 = uVar15 << 2;
            local_a0 = local_44;
            pvVar17 = (void *)_Znwj(local_94);
            pvVar21 = local_a0;
            if (uVar15 != 0) {
              local_a0 = pvVar17;
              memmove(pvVar17,pvVar21,local_94);
              pvVar17 = local_a0;
            }
          }
          if (*(int *)(iVar4 + 0x14) != 0) {
            local_a0 = pvVar17;
            _ZdlPv();
            pvVar17 = local_a0;
          }
          *(void **)(iVar4 + 0x14) = pvVar17;
          pvVar17 = (void *)((int)pvVar17 + local_94);
          *(void **)(iVar4 + 0x1c) = pvVar17;
        }
        else {
          pvVar21 = *(void **)(iVar4 + 0x18);
          uVar8 = (int)pvVar21 - (int)pvVar17 >> 2;
          if (uVar8 < uVar15) {
            pvVar3 = (void *)((int)local_44 + uVar8 * 4);
            if (uVar8 != 0) {
              memmove(pvVar17,local_44,uVar8 * 4);
              pvVar21 = *(void **)(iVar4 + 0x18);
              pvVar17 = *(void **)(iVar4 + 0x14);
              pvVar3 = (void *)((int)local_44 + ((int)pvVar21 - (int)pvVar17 & 0xfffffffcU));
            }
            iVar14 = (int)local_40 - (int)pvVar3 >> 2;
            if (iVar14 == 0) {
              pvVar17 = (void *)((int)pvVar17 + uVar15 * 4);
            }
            else {
              memmove(pvVar21,pvVar3,iVar14 << 2);
              pvVar17 = (void *)(*(int *)(iVar4 + 0x14) + uVar15 * 4);
            }
          }
          else if (uVar15 != 0) {
            memmove(pvVar17,local_44,uVar15 * 4);
            pvVar17 = (void *)(*(int *)(iVar4 + 0x14) + uVar15 * 4);
          }
        }
        *(void **)(iVar4 + 0x18) = pvVar17;
      }
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (piVar12);
      if (local_44 != (void *)0x0) {
        _ZdlPv();
      }
      iVar1 = iVar1 + 1;
    } while (iVar1 != local_90);
  }
  return;
LAB_001833e8:
  uVar18 = *(uint *)(iVar5 + 8);
  uVar11 = *puVar13;
  uVar8 = uVar15;
  uVar7 = uVar18;
  while (uVar7 != 0) {
    if (*(uint *)(uVar7 + 0x10) < uVar11) {
      uVar7 = *(uint *)(uVar7 + 0xc);
    }
    else {
      uVar8 = uVar7;
      uVar7 = *(uint *)(uVar7 + 8);
    }
  }
  if ((uVar15 != uVar8) && (*(uint *)(uVar8 + 0x10) <= uVar11)) goto LAB_001834d0;
  uStack_e0 = 0;
  uVar7 = uVar15;
  uStack_e4 = uVar11;
  if (uVar15 == uVar8) {
    uVar6 = 0;
    if (*(int *)(iVar5 + 0x14) != 0) {
      uVar10 = *(uint *)(iVar5 + 0x10);
      uVar6 = *(uint *)(uVar10 + 0x10);
      if (uVar6 < uVar11) {
LAB_00183628:
        bVar22 = uVar15 == uVar10;
        uVar8 = _Znwj(0x18);
        if ((uint *)(uVar8 + 0x10) != (uint *)0x0) {
          *(uint *)(uVar8 + 0x10) = uStack_e4;
          *(undefined4 *)(uVar8 + 0x14) = uStack_e0;
        }
        goto LAB_0018355c;
      }
    }
    if (uVar18 == 0) {
LAB_001836e4:
      if (*(uint *)(iVar5 + 0xc) == uVar7) {
        uVar8 = _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_iESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3306
                          (iVar5,0,uVar7,&uStack_e4);
        puVar20 = puStack_d0;
        goto LAB_001834d0;
      }
      uVar8 = _ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(uVar7);
      uVar9 = *(uint *)(uVar8 + 0x10);
    }
    else {
      do {
        uVar8 = uVar18;
        uVar9 = *(uint *)(uVar8 + 0x10);
        if (uVar11 < uVar9) {
          uVar6 = *(uint *)(uVar8 + 8);
        }
        if (uVar9 <= uVar11) {
          uVar6 = *(uint *)(uVar8 + 0xc);
        }
        uVar18 = uVar6;
      } while (uVar6 != 0);
      uVar7 = uVar8;
      if (uVar9 > uVar11) goto LAB_001836e4;
    }
joined_r0x001835c8:
    uVar10 = uVar7;
    if (uVar9 < uVar11) {
      if (uVar15 == uVar10) {
        bVar22 = true;
      }
      else if (uVar11 < *(uint *)(uVar10 + 0x10)) {
        bVar22 = true;
      }
      else {
        bVar22 = false;
      }
      uVar8 = _Znwj(0x18);
      if ((uint *)(uVar8 + 0x10) != (uint *)0x0) {
        *(uint *)(uVar8 + 0x10) = uStack_e4;
        *(undefined4 *)(uVar8 + 0x14) = uStack_e0;
      }
LAB_0018355c:
      _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(bVar22,uVar8,uVar10,uVar15);
      *(int *)(iVar5 + 0x14) = *(int *)(iVar5 + 0x14) + 1;
      puVar20 = puStack_d0;
    }
  }
  else if (uVar11 < *(uint *)(uVar8 + 0x10)) {
    uVar10 = *(uint *)(iVar5 + 0xc);
    if (uVar10 == uVar8) {
      uVar8 = _Znwj(0x18);
      if ((uint *)(uVar8 + 0x10) != (uint *)0x0) {
        *(uint *)(uVar8 + 0x10) = uStack_e4;
        *(undefined4 *)(uVar8 + 0x14) = uStack_e0;
      }
      bVar22 = true;
      goto LAB_0018355c;
    }
    uVar6 = _ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(uVar8);
    if (*(uint *)(uVar6 + 0x10) < uVar11) {
      uVar10 = uVar6;
      if (*(int *)(uVar6 + 0xc) == 0) goto LAB_00183628;
      uVar7 = _Znwj(0x18);
      if ((uint *)(uVar7 + 0x10) != (uint *)0x0) {
        *(uint *)(uVar7 + 0x10) = uStack_e4;
        *(undefined4 *)(uVar7 + 0x14) = uStack_e0;
      }
      uVar2 = 1;
LAB_001834b0:
      _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(uVar2,uVar7,uVar8,uVar15);
      *(int *)(iVar5 + 0x14) = *(int *)(iVar5 + 0x14) + 1;
      uVar8 = uVar7;
      puVar20 = puStack_d0;
    }
    else {
      if (uVar18 != 0) {
        do {
          uVar8 = uVar18;
          uVar9 = *(uint *)(uVar8 + 0x10);
          if (uVar11 < uVar9) {
            uVar18 = *(uint *)(uVar8 + 8);
          }
          else {
            uVar18 = *(uint *)(uVar8 + 0xc);
          }
        } while (uVar18 != 0);
        uVar7 = uVar8;
        if (uVar9 <= uVar11) goto joined_r0x001835c8;
      }
      if (uVar10 != uVar7) {
        uVar8 = _ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(uVar7);
        uVar9 = *(uint *)(uVar8 + 0x10);
        goto joined_r0x001835c8;
      }
      uVar8 = _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_iESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3306
                        (iVar5,0,uVar10,&uStack_e4);
      puVar20 = puStack_d0;
    }
  }
  else if (*(uint *)(uVar8 + 0x10) < uVar11) {
    if (*(uint *)(iVar5 + 0x10) == uVar8) {
      uVar8 = _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_iESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3306
                        (iVar5,0,uVar8,&uStack_e4);
      puVar20 = puStack_d0;
    }
    else {
      uVar10 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(uVar8);
      if (uVar11 < *(uint *)(uVar10 + 0x10)) {
        if (*(int *)(uVar8 + 0xc) == 0) {
          uVar7 = _Znwj(0x18);
          if ((uint *)(uVar7 + 0x10) != (uint *)0x0) {
            *(uint *)(uVar7 + 0x10) = uStack_e4;
            *(undefined4 *)(uVar7 + 0x14) = uStack_e0;
          }
          uVar2 = 0;
          goto LAB_001834b0;
        }
        uVar8 = _Znwj(0x18);
        if ((uint *)(uVar8 + 0x10) != (uint *)0x0) {
          *(uint *)(uVar8 + 0x10) = uStack_e4;
          *(undefined4 *)(uVar8 + 0x14) = uStack_e0;
        }
        bVar22 = true;
        goto LAB_0018355c;
      }
      _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_iESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE16_M_insert_uniqueERKS4__constprop_3374
                (auStack_dc,iVar5,&uStack_e4);
      uVar8 = auStack_dc[0];
      puVar20 = puStack_d0;
    }
  }
LAB_001834d0:
  puVar13 = puVar13 + 1;
  *(undefined4 *)(uVar8 + 0x14) = 0;
  if (puVar13 == puVar20) {
LAB_001834e0:
    if (puStack_d4 != (uint *)0x0) {
      _ZdlPv();
    }
    return;
  }
  goto LAB_001833e8;
}


