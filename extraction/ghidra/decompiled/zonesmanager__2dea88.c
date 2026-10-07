// _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4_.constprop.2915 @ 002dea88

int _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4__constprop_2915
              (int param_1,int param_2,int *param_3)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int *piVar7;
  bool bVar8;
  int *piVar9;
  int local_38 [2];
  int local_30 [2];
  int local_28 [3];
  
  iVar5 = param_1 + 4;
  if (param_2 == iVar5) {
    if ((*(int *)(param_1 + 0x14) == 0) ||
       (iVar6 = *(int *)(param_1 + 0x10), *param_3 <= *(int *)(iVar6 + 0x10))) {
      _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE16_M_insert_uniqueERKS4__constprop_2806
                (local_28,param_1,param_3);
      return local_28[0];
    }
    bVar8 = iVar6 == param_2;
    iVar1 = _Znwj(0x24);
    iVar5 = param_2;
    if ((int *)(iVar1 + 0x10) != (int *)0x0) {
      iVar2 = param_3[1];
      iVar3 = param_3[2];
      iVar4 = param_3[3];
      *(int *)(iVar1 + 0x10) = *param_3;
      *(int *)(iVar1 + 0x14) = iVar2;
      *(int *)(iVar1 + 0x18) = iVar3;
      *(int *)(iVar1 + 0x1c) = iVar4;
      *(int *)(iVar1 + 0x20) = param_3[4];
    }
LAB_002deb18:
    _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(bVar8,iVar1,iVar6,iVar5);
    *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
  }
  else {
    iVar6 = *param_3;
    if (iVar6 < *(int *)(param_2 + 0x10)) {
      iVar1 = param_2;
      if (param_2 != *(int *)(param_1 + 0xc)) {
        iVar1 = _ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(param_2);
        if (iVar6 <= *(int *)(iVar1 + 0x10)) {
          _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE16_M_insert_uniqueERKS4__constprop_2806
                    (local_30,param_1,param_3);
          return local_30[0];
        }
        if (*(int *)(iVar1 + 0xc) == 0) {
          iVar5 = _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_2910
                            (param_1,0,iVar1,param_3);
          return iVar5;
        }
        iVar1 = _Znwj(0x24);
        piVar7 = (int *)(iVar1 + 0x10);
        piVar9 = (int *)0x0;
        if (piVar7 != (int *)0x0) {
          iVar6 = *param_3;
          iVar2 = param_3[1];
          iVar3 = param_3[2];
          iVar4 = param_3[3];
          param_3 = param_3 + 4;
          *piVar7 = iVar6;
          *(int *)(iVar1 + 0x14) = iVar2;
          *(int *)(iVar1 + 0x18) = iVar3;
          *(int *)(iVar1 + 0x1c) = iVar4;
          piVar9 = (int *)(iVar1 + 0x20);
        }
        bVar8 = true;
        iVar6 = param_2;
        if (piVar7 != (int *)0x0) {
          *piVar9 = *param_3;
        }
        goto LAB_002deb18;
      }
    }
    else {
      if (iVar6 <= *(int *)(param_2 + 0x10)) {
        return param_2;
      }
      if (param_2 != *(int *)(param_1 + 0x10)) {
        iVar1 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(param_2);
        if (*(int *)(iVar1 + 0x10) <= iVar6) {
          _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE16_M_insert_uniqueERKS4__constprop_2806
                    (local_38,param_1,param_3);
          return local_38[0];
        }
        if (*(int *)(param_2 + 0xc) != 0) {
          iVar6 = _Znwj(0x24);
          if ((int *)(iVar6 + 0x10) != (int *)0x0) {
            iVar2 = param_3[1];
            iVar3 = param_3[2];
            iVar4 = param_3[3];
            *(int *)(iVar6 + 0x10) = *param_3;
            *(int *)(iVar6 + 0x14) = iVar2;
            *(int *)(iVar6 + 0x18) = iVar3;
            *(int *)(iVar6 + 0x1c) = iVar4;
            *(int *)(iVar6 + 0x20) = param_3[4];
          }
          _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(1,iVar6,iVar1,iVar5);
          *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
          return iVar6;
        }
        iVar5 = _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_2910
                          (param_1,0,param_2,param_3);
        return iVar5;
      }
      iVar1 = 0;
    }
    iVar1 = _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_2910
                      (param_1,iVar1,param_2,param_3);
  }
  return iVar1;
}


