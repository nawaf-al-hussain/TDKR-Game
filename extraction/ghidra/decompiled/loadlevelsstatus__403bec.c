// _ZN6CLevel16LoadLevelsStatusEP13CMemoryStream @ 00403bec

void _ZN6CLevel16LoadLevelsStatusEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  void *pvVar6;
  int iVar7;
  uint uVar8;
  uint uVar9;
  int iVar10;
  void *__s2;
  uint uVar11;
  int iVar12;
  int *local_68;
  undefined1 auStack_54 [4];
  int local_50;
  void *local_4c;
  void *local_48;
  undefined1 local_44;
  int local_40 [2];
  int local_38 [2];
  int local_30 [3];
  
  local_50 = *(int *)(DAT_00403fe4 + 0x403c0c) + 0xc;
  iVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  if (0 < iVar1) {
    iVar7 = 0;
    iVar12 = param_1 + 0xacc;
    do {
      _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,&local_50);
      iVar2 = _ZN13CMemoryStream7ReadIntEv(param_2);
      _ZNSsC1EPKcRKSaIcE(&local_4c,local_50,auStack_54);
      pvVar6 = local_4c;
      iVar10 = iVar12;
      if (*(int *)(param_1 + 0xad0) != 0) {
        uVar11 = *(uint *)((int)local_4c + -0xc);
        iVar5 = *(int *)(param_1 + 0xad0);
        do {
          uVar8 = *(uint *)((int)*(void **)(iVar5 + 0x10) + -0xc);
          uVar9 = uVar11;
          if (uVar8 <= uVar11) {
            uVar9 = uVar8;
          }
          iVar3 = memcmp(*(void **)(iVar5 + 0x10),pvVar6,uVar9);
          if (iVar3 == 0) {
            iVar3 = uVar8 - uVar11;
          }
          if (iVar3 < 0) {
            iVar3 = *(int *)(iVar5 + 0xc);
          }
          else {
            iVar3 = *(int *)(iVar5 + 8);
            iVar10 = iVar5;
          }
          iVar5 = iVar3;
        } while (iVar3 != 0);
      }
      iVar5 = iVar10;
      if (iVar12 == iVar10) {
LAB_00403d40:
        _ZNSsC1ERKSs(&local_48,&local_4c);
        pvVar6 = local_48;
        iVar3 = param_1 + 0xac8;
        local_44 = 0;
        if (iVar12 == iVar10) {
          if (*(int *)(param_1 + 0xadc) != 0) {
            iVar10 = *(int *)(param_1 + 0xad8);
            pvVar6 = *(void **)(iVar10 + 0x10);
            uVar8 = *(uint *)((int)local_48 + -0xc);
            uVar9 = *(uint *)((int)pvVar6 + -0xc);
            uVar11 = uVar8;
            if (uVar9 <= uVar8) {
              uVar11 = uVar9;
            }
            iVar5 = memcmp(pvVar6,local_48,uVar11);
            if (iVar5 == 0) {
              iVar5 = uVar9 - uVar8;
            }
            if (iVar5 < 0) {
              iVar5 = _ZNSt8_Rb_treeISsSt4pairIKSsbESt10_Select1stIS2_ESt4lessISsESaIS2_EE10_M_insert_EPKSt18_Rb_tree_node_baseSB_RKS2__constprop_2557
                                (iVar3,0,iVar10,&local_48);
              goto LAB_00403dcc;
            }
          }
          _ZNSt8_Rb_treeISsSt4pairIKSsbESt10_Select1stIS2_ESt4lessISsESaIS2_EE16_M_insert_uniqueERKS2__constprop_2585
                    (local_40,iVar3,&local_48);
          iVar5 = local_40[0];
        }
        else {
          __s2 = *(void **)(iVar10 + 0x10);
          uVar8 = *(uint *)((int)__s2 + -0xc);
          uVar9 = *(uint *)((int)local_48 + -0xc);
          uVar11 = uVar8;
          if (uVar9 <= uVar8) {
            uVar11 = uVar9;
          }
          iVar4 = memcmp(local_48,__s2,uVar11);
          if (iVar4 == 0) {
            iVar4 = uVar9 - uVar8;
          }
          if (iVar4 < 0) {
            if (*(int *)(param_1 + 0xad4) == iVar10) {
LAB_00403ed8:
              iVar5 = _ZNSt8_Rb_treeISsSt4pairIKSsbESt10_Select1stIS2_ESt4lessISsESaIS2_EE10_M_insert_EPKSt18_Rb_tree_node_baseSB_RKS2__constprop_2557
                                (iVar3);
            }
            else {
              iVar5 = _ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(iVar10);
              uVar8 = *(uint *)((int)*(void **)(iVar5 + 0x10) + -0xc);
              uVar11 = uVar8;
              if (uVar9 <= uVar8) {
                uVar11 = uVar9;
              }
              iVar4 = memcmp(*(void **)(iVar5 + 0x10),pvVar6,uVar11);
              if (iVar4 == 0) {
                iVar4 = uVar8 - uVar9;
              }
              if (iVar4 < 0) {
                if (*(int *)(iVar5 + 0xc) == 0) {
                  iVar5 = _ZNSt8_Rb_treeISsSt4pairIKSsbESt10_Select1stIS2_ESt4lessISsESaIS2_EE10_M_insert_EPKSt18_Rb_tree_node_baseSB_RKS2__constprop_2557
                                    (iVar3,0,iVar5,&local_48);
                }
                else {
                  iVar5 = _Znwj(0x18);
                  if (iVar5 + 0x10 != 0) {
                    _ZNSsC1ERKSs(iVar5 + 0x10,&local_48);
                    *(undefined1 *)(iVar5 + 0x14) = local_44;
                  }
                  _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
                            (1,iVar5,iVar10,iVar12);
                  *(int *)(param_1 + 0xadc) = *(int *)(param_1 + 0xadc) + 1;
                }
              }
              else {
                _ZNSt8_Rb_treeISsSt4pairIKSsbESt10_Select1stIS2_ESt4lessISsESaIS2_EE16_M_insert_uniqueERKS2__constprop_2585
                          (local_38,iVar3,&local_48);
                iVar5 = local_38[0];
              }
            }
          }
          else {
            iVar4 = memcmp(__s2,pvVar6,uVar11);
            if (iVar4 == 0) {
              iVar4 = uVar8 - uVar9;
            }
            if (iVar4 < 0) {
              if (*(int *)(param_1 + 0xad8) == iVar10) {
                iVar5 = _ZNSt8_Rb_treeISsSt4pairIKSsbESt10_Select1stIS2_ESt4lessISsESaIS2_EE10_M_insert_EPKSt18_Rb_tree_node_baseSB_RKS2__constprop_2557
                                  (iVar3,0,iVar10,&local_48);
              }
              else {
                iVar5 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar10);
                uVar8 = *(uint *)((int)*(void **)(iVar5 + 0x10) + -0xc);
                uVar11 = uVar8;
                if (uVar9 <= uVar8) {
                  uVar11 = uVar9;
                }
                iVar5 = memcmp(pvVar6,*(void **)(iVar5 + 0x10),uVar11);
                if (iVar5 == 0) {
                  iVar5 = uVar9 - uVar8;
                }
                if (iVar5 < 0) {
                  if (*(int *)(iVar10 + 0xc) != 0) goto LAB_00403ed8;
                  iVar5 = _ZNSt8_Rb_treeISsSt4pairIKSsbESt10_Select1stIS2_ESt4lessISsESaIS2_EE10_M_insert_EPKSt18_Rb_tree_node_baseSB_RKS2__constprop_2557
                                    (iVar3,0,iVar10,&local_48);
                }
                else {
                  _ZNSt8_Rb_treeISsSt4pairIKSsbESt10_Select1stIS2_ESt4lessISsESaIS2_EE16_M_insert_uniqueERKS2__constprop_2585
                            (local_30,iVar3,&local_48);
                  iVar5 = local_30[0];
                }
              }
            }
          }
        }
LAB_00403dcc:
        _ZNSsD1Ev(&local_48);
      }
      else {
        uVar8 = *(uint *)((int)local_4c + -0xc);
        uVar9 = *(uint *)((int)*(void **)(iVar10 + 0x10) + -0xc);
        uVar11 = uVar9;
        if (uVar8 <= uVar9) {
          uVar11 = uVar8;
        }
        iVar3 = memcmp(local_4c,*(void **)(iVar10 + 0x10),uVar11);
        if (iVar3 == 0) {
          iVar3 = uVar8 - uVar9;
        }
        if (iVar3 < 0) goto LAB_00403d40;
      }
      iVar7 = iVar7 + 1;
      *(bool *)(iVar5 + 0x14) = iVar2 != 0;
      _ZNSsD1Ev(&local_4c);
    } while (iVar7 != iVar1);
  }
  local_68 = &local_50;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (local_68);
  return;
}


