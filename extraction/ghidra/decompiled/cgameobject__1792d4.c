// _Z17RemoveUnwantedCopRSt17_Rb_tree_iteratorISt4pairIKP11CGameObjectbEE @ 001792d4

/* WARNING: Restarted to delay deadcode elimination for space: stack */

void _Z17RemoveUnwantedCopRSt17_Rb_tree_iteratorISt4pairIKP11CGameObjectbEE(int *param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  int iVar5;
  int iVar6;
  uint uVar7;
  bool bVar8;
  uint local_40;
  uint local_3c;
  int local_38 [2];
  int local_30 [2];
  int local_28 [2];
  
  _ZN15CNpcAIComponent16EndRecordingPathEv(*(undefined4 *)(*(int *)(*param_1 + 0x10) + 0xbc));
  _ZN6CLevel8GetLevelEv();
  iVar1 = _ZNK6CLevel25GetWantedManagerComponentEv();
  uVar7 = *(uint *)(*param_1 + 0x10);
  iVar6 = iVar1 + 0x90;
  iVar5 = *(int *)(iVar1 + 0x94);
  iVar3 = iVar6;
  while (iVar5 != 0) {
    if (*(uint *)(iVar5 + 0x10) < uVar7) {
      iVar5 = *(int *)(iVar5 + 0xc);
    }
    else {
      iVar5 = *(int *)(iVar5 + 8);
      iVar3 = iVar5;
    }
  }
  if ((iVar6 != iVar3) && (*(uint *)(iVar3 + 0x10) <= uVar7)) goto LAB_001793dc;
  iVar5 = iVar1 + 0x8c;
  local_3c = local_3c & 0xffffff00;
  local_40 = uVar7;
  if (iVar3 == iVar6) {
    if ((*(int *)(iVar1 + 0xa0) == 0) ||
       (iVar2 = *(int *)(iVar1 + 0x9c), uVar7 <= *(uint *)(iVar2 + 0x10))) {
      _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_bESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE16_M_insert_uniqueERKS4__constprop_3362
                (local_38,iVar5,&local_40);
      iVar3 = local_38[0];
      goto LAB_001793dc;
    }
    bVar8 = iVar3 == iVar2;
    iVar5 = _Znwj(0x18);
    if ((uint *)(iVar5 + 0x10) != (uint *)0x0) {
      *(uint *)(iVar5 + 0x10) = local_40;
      *(uint *)(iVar5 + 0x14) = local_3c;
    }
  }
  else {
    uVar4 = *(uint *)(iVar3 + 0x10);
    if (uVar7 > uVar4 || uVar4 == uVar7) {
      if (uVar7 <= uVar4) goto LAB_001793dc;
      if (iVar3 != *(int *)(iVar1 + 0x9c)) {
        iVar2 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar3);
        if (*(uint *)(iVar2 + 0x10) <= uVar7) {
          _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_bESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE16_M_insert_uniqueERKS4__constprop_3362
                    (local_28,iVar5,&local_40);
          iVar3 = local_28[0];
          goto LAB_001793dc;
        }
        if (*(int *)(iVar3 + 0xc) != 0) {
          iVar3 = _Znwj(0x18);
          if ((uint *)(iVar3 + 0x10) != (uint *)0x0) {
            *(uint *)(iVar3 + 0x10) = local_40;
            *(uint *)(iVar3 + 0x14) = local_3c;
          }
          _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(1,iVar3,iVar2,iVar6);
          *(int *)(iVar1 + 0xa0) = *(int *)(iVar1 + 0xa0) + 1;
          goto LAB_001793dc;
        }
      }
      iVar3 = _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_bESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3342
                        (iVar5,0,iVar3,&local_40);
      goto LAB_001793dc;
    }
    if (iVar3 == *(int *)(iVar1 + 0x98)) {
      iVar3 = _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_bESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3342
                        (iVar5,iVar3,iVar3,&local_40);
      goto LAB_001793dc;
    }
    iVar2 = _ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(iVar3);
    if (uVar7 <= *(uint *)(iVar2 + 0x10)) {
      _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_bESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE16_M_insert_uniqueERKS4__constprop_3362
                (local_30,iVar5,&local_40);
      iVar3 = local_30[0];
      goto LAB_001793dc;
    }
    if (*(int *)(iVar2 + 0xc) == 0) {
      iVar3 = _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_bESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_3342
                        (iVar5,0,iVar2,&local_40);
      goto LAB_001793dc;
    }
    iVar5 = _Znwj(0x18);
    if ((uint *)(iVar5 + 0x10) != (uint *)0x0) {
      *(uint *)(iVar5 + 0x10) = local_40;
      *(uint *)(iVar5 + 0x14) = local_3c;
    }
    bVar8 = true;
    iVar2 = iVar3;
    iVar3 = iVar6;
  }
  _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(bVar8,iVar5,iVar2,iVar3);
  *(int *)(iVar1 + 0xa0) = *(int *)(iVar1 + 0xa0) + 1;
  iVar3 = iVar5;
LAB_001793dc:
  iVar6 = *param_1;
  *(undefined1 *)(iVar3 + 0x14) = 1;
  iVar5 = _ZSt18_Rb_tree_incrementPSt18_Rb_tree_node_base(iVar6);
  *param_1 = iVar5;
  _ZSt28_Rb_tree_rebalance_for_erasePSt18_Rb_tree_node_baseRS_(iVar6,iVar1 + 0x78);
  _ZdlPv();
  *(int *)(iVar1 + 0x88) = *(int *)(iVar1 + 0x88) + -1;
  return;
}

