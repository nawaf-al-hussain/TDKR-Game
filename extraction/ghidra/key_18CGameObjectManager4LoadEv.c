// _ZN18CGameObjectManager4LoadEv @ 00375780

void _ZN18CGameObjectManager4LoadEv(int param_1)

{
  undefined1 uVar1;
  undefined1 uVar2;
  int iVar3;
  int *piVar4;
  int iVar5;
  int iVar6;
  undefined4 *puVar7;
  int iVar8;
  int *piVar9;
  undefined4 uVar10;
  undefined1 *puVar11;
  int iVar12;
  undefined4 extraout_r1;
  undefined4 *puVar13;
  undefined1 *puVar14;
  undefined1 *extraout_r3;
  undefined1 *puVar15;
  int iVar16;
  int iVar17;
  int iVar18;
  int iVar19;
  undefined1 *puVar20;
  undefined8 uVar21;
  undefined8 uVar22;
  int local_b4;
  int *local_98;
  undefined4 local_94;
  int local_90;
  undefined4 local_8c;
  int local_88;
  undefined4 local_84;
  int local_80 [2];
  int local_78 [2];
  int local_70 [2];
  int local_68;
  undefined4 *local_64;
  undefined4 *local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined1 *local_50;
  undefined1 *local_4c;
  undefined1 *local_48;
  undefined4 *local_44;
  undefined4 *local_40;
  undefined4 *local_3c;
  int local_38;
  int local_34;
  undefined4 local_30;
  undefined4 local_2c;
  
  piVar4 = (int *)_Z9GetDevicev();
  (**(code **)(**(int **)(*piVar4 + 0x28) + 0xc))
            (&local_98,*(int **)(*piVar4 + 0x28),DAT_00375f78 + 0x37579c);
  if (local_98 != (int *)0x0) {
    iVar19 = 1;
    iVar17 = DAT_00375f7c + 0x3757d8;
    iVar5 = (**(code **)(*local_98 + 0x20))();
    iVar6 = _ZnajPKci(iVar5,iVar17,0xa9);
    (**(code **)(*local_98 + 0xc))(local_98,iVar6,iVar5);
    piVar4 = (int *)_ZnwjPKci(0x38,iVar17,0xae);
    piVar4[4] = 0;
    piVar4[5] = 0;
    piVar4[6] = 0;
    piVar4[7] = 0;
    piVar4[8] = 0;
    piVar4[9] = 0;
    piVar4[10] = 0;
    piVar4[0xb] = 0;
    piVar4[0xc] = 0;
    piVar4[1] = iVar5;
    piVar4[2] = iVar5;
    piVar4[3] = 0;
    *piVar4 = iVar6;
    *(undefined1 *)((int)piVar4 + 0x35) = 1;
    *(undefined1 *)(piVar4 + 0xd) = 1;
    iVar5 = _ZN13CMemoryStream7ReadIntEv();
    if (iVar5 == 0x44494354) {
      _ZN13CMemoryStream9BeginReadEv_part_2551(piVar4);
      iVar6 = piVar4[3];
      iVar19 = iVar6 + 1;
      iVar5 = iVar6 + 2;
    }
    else {
      iVar5 = 2;
      iVar6 = 0;
      piVar4[3] = 0;
      *(undefined1 *)(piVar4 + 0xd) = 0;
    }
    iVar17 = *piVar4;
    uVar1 = *(undefined1 *)(iVar17 + iVar6);
    piVar4[3] = iVar19;
    uVar2 = *(undefined1 *)(iVar17 + iVar19);
    piVar4[3] = iVar5;
    if (CONCAT11(uVar1,uVar2) == 0x474f) {
      uVar1 = *(undefined1 *)(iVar17 + iVar5);
      piVar4[3] = iVar6 + 3;
      uVar2 = *(undefined1 *)(iVar17 + iVar6 + 3);
      piVar4[3] = iVar6 + 4;
      if (CONCAT11(uVar1,uVar2) == 3) {
        iVar6 = 0;
        iVar5 = _ZN13CMemoryStream7ReadIntEv(piVar4);
        local_68 = 0;
        local_64 = (undefined4 *)0x0;
        local_60 = (undefined4 *)0x0;
        if (iVar5 < 1) {
          _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE8_M_eraseEPSt13_Rb_tree_nodeISB_E
                    (param_1 + 0x30,*(undefined4 *)(param_1 + 0x38));
          *(undefined4 *)(param_1 + 0x38) = 0;
          *(int *)(param_1 + 0x3c) = param_1 + 0x34;
          *(int *)(param_1 + 0x40) = param_1 + 0x34;
          *(undefined4 *)(param_1 + 0x44) = 0;
        }
        else {
          do {
            local_94 = _ZN13CMemoryStream7ReadIntEv(piVar4);
            if (local_64 == local_60) {
              _ZNSt6vectorIiSaIiEE9push_backERKi_part_2276(&local_68,&local_94);
            }
            else {
              if (local_64 != (undefined4 *)0x0) {
                *local_64 = local_94;
              }
              local_64 = local_64 + 1;
            }
            iVar19 = DAT_00375f80;
            iVar6 = iVar6 + 1;
          } while (iVar6 != iVar5);
          iVar6 = param_1 + 0x18;
          _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE8_M_eraseEPSt13_Rb_tree_nodeISB_E
                    (param_1 + 0x30,*(undefined4 *)(param_1 + 0x38));
          iVar19 = *(int *)(iVar19 + 0x3759bc);
          puVar13 = (undefined4 *)(DAT_00375f84 + 0x3759c8);
          local_b4 = 0;
          *(undefined4 *)(param_1 + 0x38) = 0;
          *(int *)(param_1 + 0x3c) = param_1 + 0x34;
          *(int *)(param_1 + 0x40) = param_1 + 0x34;
          *(undefined4 *)(param_1 + 0x44) = 0;
          do {
            piVar4[3] = *(int *)(local_68 + local_b4 * 4);
            local_90 = _ZN13CMemoryStream7ReadIntEv(piVar4);
            puVar7 = (undefined4 *)
                     _ZNSt3mapIiSt6vectorIiSaIiEESt4lessIiESaISt4pairIKiS2_EEEixERS6_
                               (iVar6,&local_90);
            local_5c = 0;
            local_58 = 0;
            local_54 = 0;
            if (puVar7 != &local_5c) {
              puVar7[1] = *puVar7;
            }
            uVar21 = _ZN13CMemoryStream7ReadIntEv(piVar4);
            uVar22 = CONCAT44((int)((ulonglong)uVar21 >> 0x20),local_8c);
            if (0 < (int)uVar21) {
              iVar17 = 0;
              iVar18 = param_1 + 0x1c;
              do {
                iVar3 = local_90;
                iVar12 = (int)((ulonglong)uVar22 >> 0x20);
                local_8c = (undefined4)uVar22;
                iVar8 = iVar18;
                iVar16 = *(int *)(param_1 + 0x20);
                while (iVar16 != 0) {
                  iVar12 = *(int *)(iVar16 + 0x10);
                  if (iVar12 < local_90) {
                    iVar16 = *(int *)(iVar16 + 0xc);
                  }
                  else {
                    iVar8 = iVar16;
                    iVar16 = *(int *)(iVar16 + 8);
                  }
                }
                if ((iVar18 == iVar8) || (local_90 < *(int *)(iVar8 + 0x10))) {
                  local_38 = local_90;
                  local_34 = 0;
                  local_2c = 0;
                  local_30 = 0;
                  if (iVar8 == iVar18) {
                    if ((*(int *)(param_1 + 0x2c) == 0) ||
                       (local_90 <= *(int *)(*(int *)(param_1 + 0x28) + 0x10))) {
                      _ZNSt8_Rb_treeIiSt4pairIKiSt6vectorIiSaIiEEESt10_Select1stIS5_ESt4lessIiESaIS5_EE16_M_insert_uniqueERKS5__constprop_3170
                                (local_80,iVar6,&local_38);
                      iVar8 = local_80[0];
                    }
                    else {
                      iVar8 = _ZNSt8_Rb_treeIiSt4pairIKiSt6vectorIiSaIiEEESt10_Select1stIS5_ESt4lessIiESaIS5_EE10_M_insert_EPKSt18_Rb_tree_node_baseSE_RKS5__constprop_3157
                                        (iVar6,0,*(int *)(param_1 + 0x28),&local_38);
                    }
                  }
                  else if (local_90 < *(int *)(iVar8 + 0x10)) {
                    iVar16 = iVar8;
                    if (iVar8 == *(int *)(param_1 + 0x24)) {
LAB_00375af4:
                      iVar8 = _ZNSt8_Rb_treeIiSt4pairIKiSt6vectorIiSaIiEEESt10_Select1stIS5_ESt4lessIiESaIS5_EE10_M_insert_EPKSt18_Rb_tree_node_baseSE_RKS5__constprop_3157
                                        (iVar6,iVar16,iVar16,&local_38);
                    }
                    else {
                      iVar8 = _ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(iVar8);
                      if (*(int *)(iVar8 + 0x10) < iVar3) {
                        if (*(int *)(iVar8 + 0xc) != 0) goto LAB_00375af4;
                        iVar8 = _ZNSt8_Rb_treeIiSt4pairIKiSt6vectorIiSaIiEEESt10_Select1stIS5_ESt4lessIiESaIS5_EE10_M_insert_EPKSt18_Rb_tree_node_baseSE_RKS5__constprop_3157
                                          (iVar6,0,iVar8,&local_38);
                      }
                      else {
                        _ZNSt8_Rb_treeIiSt4pairIKiSt6vectorIiSaIiEEESt10_Select1stIS5_ESt4lessIiESaIS5_EE16_M_insert_uniqueERKS5__constprop_3170
                                  (local_78,iVar6,&local_38);
                        iVar8 = local_78[0];
                      }
                    }
                  }
                  else {
                    if (local_90 <= *(int *)(iVar8 + 0x10)) goto LAB_00375b18;
                    if (iVar8 != *(int *)(param_1 + 0x28)) {
                      iVar16 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar8,iVar12);
                      if (*(int *)(iVar16 + 0x10) <= iVar3) {
                        _ZNSt8_Rb_treeIiSt4pairIKiSt6vectorIiSaIiEEESt10_Select1stIS5_ESt4lessIiESaIS5_EE16_M_insert_uniqueERKS5__constprop_3170
                                  (local_70,iVar6,&local_38);
                        iVar8 = local_70[0];
                        goto LAB_00375b0c;
                      }
                      if (*(int *)(iVar8 + 0xc) != 0) goto LAB_00375af4;
                    }
                    iVar8 = _ZNSt8_Rb_treeIiSt4pairIKiSt6vectorIiSaIiEEESt10_Select1stIS5_ESt4lessIiESaIS5_EE10_M_insert_EPKSt18_Rb_tree_node_baseSE_RKS5__constprop_3157
                                      (iVar6,0,iVar8,&local_38);
                  }
LAB_00375b0c:
                  if (local_34 != 0) {
                    _ZdlPv();
                  }
                }
LAB_00375b18:
                uVar22 = _ZN13CMemoryStream7ReadIntEv(piVar4);
                local_8c = (undefined4)uVar22;
                puVar7 = *(undefined4 **)(iVar8 + 0x18);
                if (puVar7 == *(undefined4 **)(iVar8 + 0x1c)) {
                  _ZNSt6vectorIiSaIiEE9push_backERKi_part_2276(iVar8 + 0x14,&local_8c);
                  uVar22 = CONCAT44(extraout_r1,local_8c);
                }
                else {
                  if (puVar7 != (undefined4 *)0x0) {
                    *puVar7 = local_8c;
                  }
                  *(undefined4 **)(iVar8 + 0x18) = puVar7 + 1;
                }
                local_8c = (undefined4)uVar22;
                iVar17 = iVar17 + 1;
              } while (iVar17 != (int)uVar21);
            }
            iVar17 = piVar4[3];
            uVar1 = *(undefined1 *)(*piVar4 + iVar17);
            piVar4[3] = iVar17 + 1;
            local_88 = iVar19 + 0xc;
            uVar2 = *(undefined1 *)(*piVar4 + iVar17 + 1);
            piVar4[3] = iVar17 + 2;
            _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                      (piVar4,&local_88);
            puVar20 = (undefined1 *)(int)CONCAT11(uVar1,uVar2);
            piVar9 = (int *)_ZNSt3mapISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEiSt4lessIS8_ESaISt4pairIKS8_iEEEixERSC_
                                      (param_1 + 0x30,&local_88);
            *piVar9 = local_90;
            uVar10 = _ZNSt3mapIiSt6vectorIN18CGameObjectManager11TObjectDataESaIS2_EESt4lessIiESaISt4pairIKiS4_EEEixERS8_
                               (param_1,&local_90);
            local_48 = (undefined1 *)0x0;
            local_50 = (undefined1 *)0x0;
            puVar15 = extraout_r3;
            if (puVar20 == (undefined1 *)0x0) {
              puVar15 = (undefined1 *)0x0;
            }
            local_4c = (undefined1 *)0x0;
            if (puVar20 == (undefined1 *)0x0) {
              local_48 = (undefined1 *)0x0;
            }
            else {
              if (&DAT_15555555 < puVar20) {
                    /* WARNING: Subroutine does not return */
                _ZSt17__throw_bad_allocv();
              }
              local_50 = (undefined1 *)_Znwj((int)puVar20 * 0xc);
              puVar15 = local_50 + (int)puVar20 * 0xc;
              puVar11 = local_50;
              puVar14 = puVar20;
              do {
                if (puVar11 != (undefined1 *)0x0) {
                  *puVar11 = 0;
                  *(undefined4 *)(puVar11 + 4) = 0;
                }
                puVar14 = puVar14 + -1;
                puVar11 = puVar11 + 0xc;
                local_48 = puVar15;
              } while (puVar14 != (undefined1 *)0x0);
            }
            local_4c = puVar15;
            _ZNSt6vectorIN18CGameObjectManager11TObjectDataESaIS1_EEaSERKS3__constprop_3127
                      (uVar10,&local_50);
            if (local_50 != (undefined1 *)0x0) {
              _ZdlPv();
            }
            piVar9 = (int *)_ZNSt3mapIiSt6vectorIN18CGameObjectManager11TObjectDataESaIS2_EESt4lessIiESaISt4pairIKiS4_EEEixERS8_
                                      (param_1,&local_90);
            local_44 = (undefined4 *)0x0;
            local_40 = (undefined4 *)0x0;
            local_3c = (undefined4 *)0x0;
            if ((undefined1 *)0x3fffffff < puVar20) {
                    /* WARNING: Subroutine does not return */
              _ZSt20__throw_length_errorPKc(DAT_00375f88 + 0x375f74);
            }
            if (puVar20 != (undefined1 *)0x0) {
              puVar7 = (undefined4 *)_Znwj((int)puVar20 * 4);
              if (local_44 != (undefined4 *)0x0) {
                _ZdlPv();
              }
              local_3c = puVar7 + (int)puVar20;
              local_40 = puVar7;
            }
            local_44 = local_40;
            if (0 < (int)puVar20) {
              iVar17 = 0;
              iVar18 = 0;
              do {
                local_84 = _ZN13CMemoryStream7ReadIntEv(piVar4);
                if (local_40 == local_3c) {
                  _ZNSt6vectorIiSaIiEE9push_backERKi_part_2276(&local_44,&local_84);
                }
                else {
                  if (local_40 != (undefined4 *)0x0) {
                    *local_40 = local_84;
                  }
                  local_40 = local_40 + 1;
                }
                iVar16 = piVar4[3];
                iVar8 = *piVar9;
                puVar7 = local_44 + iVar18;
                iVar12 = *piVar4;
                iVar18 = iVar18 + 1;
                *(undefined4 *)(iVar8 + iVar17 + 8) = *puVar7;
                uVar1 = *(undefined1 *)(iVar12 + iVar16);
                piVar4[3] = iVar16 + 1;
                uVar2 = *(undefined1 *)(iVar12 + iVar16 + 1);
                piVar4[3] = iVar16 + 2;
                *(bool *)(iVar8 + iVar17) = CONCAT11(uVar1,uVar2) != 0;
                iVar17 = iVar17 + 0xc;
              } while (iVar18 < (int)puVar20);
              iVar18 = 0;
              iVar17 = 0;
              do {
                uVar10 = _Z25GenerateComponentTemplateiP13CMemoryStream(local_44[iVar17],piVar4);
                iVar17 = iVar17 + 1;
                iVar8 = *piVar9 + iVar18;
                iVar18 = iVar18 + 0xc;
                *(undefined4 *)(iVar8 + 4) = uVar10;
              } while (iVar17 < (int)puVar20);
            }
            if (local_90 == 0x163a6) {
              _ZN15CEffectsManager8LoadLODsEP20CComponentEffectsLOD
                        (*puVar13,*(undefined4 *)(*piVar9 + 4));
            }
            if (local_44 != (undefined4 *)0x0) {
              _ZdlPv();
            }
            local_b4 = local_b4 + 1;
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                      (&local_88);
          } while (local_b4 != iVar5);
        }
        _ZN13CMemoryStream7EndReadEv(piVar4);
        for (iVar5 = *(int *)(param_1 + 0xc); param_1 + 4 != iVar5;
            iVar5 = _ZSt18_Rb_tree_incrementPSt18_Rb_tree_node_base(iVar5)) {
          _ZN18CGameObjectManager19CheckObjectCategoryEi(param_1,*(undefined4 *)(iVar5 + 0x10));
        }
        _ZN13CMemoryStreamD2Ev(piVar4);
        _ZdlPv(piVar4);
        if (local_68 != 0) {
          _ZdlPv();
        }
      }
    }
    if (local_98 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
  }
  return;
}

