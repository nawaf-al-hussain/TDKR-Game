// _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE16_M_insert_uniqueERKS4_.constprop.2806 @ 002dbb74

int * _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE16_M_insert_uniqueERKS4__constprop_2806
                (int *param_1,int param_2,int *param_3)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  undefined4 uVar6;
  int iVar7;
  
  iVar5 = param_2 + 4;
  iVar4 = iVar5;
  if (*(int *)(param_2 + 8) != 0) {
    iVar7 = *param_3;
    iVar1 = *(int *)(param_2 + 8);
    do {
      iVar4 = iVar1;
      iVar2 = *(int *)(iVar4 + 0x10);
      if (iVar7 < iVar2) {
        iVar1 = *(int *)(iVar4 + 8);
      }
      else {
        iVar1 = *(int *)(iVar4 + 0xc);
      }
    } while (iVar1 != 0);
    if (iVar2 <= iVar7) {
      if (iVar7 <= iVar2) {
        *param_1 = iVar4;
        *(undefined1 *)(param_1 + 1) = 0;
        return param_1;
      }
      goto LAB_002dbc24;
    }
  }
  if (*(int *)(param_2 + 0xc) == iVar4) {
    iVar4 = _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_2910
                      (param_2,0,iVar4,param_3);
    *(undefined1 *)(param_1 + 1) = 1;
    *param_1 = iVar4;
  }
  else {
    iVar1 = _ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(iVar4);
    iVar7 = *param_3;
    if (*(int *)(iVar1 + 0x10) < iVar7) {
LAB_002dbc24:
      if (iVar5 == iVar4) {
        uVar6 = 1;
      }
      else if (iVar7 < *(int *)(iVar4 + 0x10)) {
        uVar6 = 1;
      }
      else {
        uVar6 = 0;
      }
      iVar1 = _Znwj(0x24);
      if ((int *)(iVar1 + 0x10) != (int *)0x0) {
        iVar7 = param_3[1];
        iVar2 = param_3[2];
        iVar3 = param_3[3];
        *(int *)(iVar1 + 0x10) = *param_3;
        *(int *)(iVar1 + 0x14) = iVar7;
        *(int *)(iVar1 + 0x18) = iVar2;
        *(int *)(iVar1 + 0x1c) = iVar3;
        *(int *)(iVar1 + 0x20) = param_3[4];
      }
      _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(uVar6,iVar1,iVar4,iVar5);
      iVar4 = *(int *)(param_2 + 0x14);
      *param_1 = iVar1;
      *(undefined1 *)(param_1 + 1) = 1;
      *(int *)(param_2 + 0x14) = iVar4 + 1;
      return param_1;
    }
    *param_1 = iVar1;
    *(undefined1 *)(param_1 + 1) = 0;
  }
  return param_1;
}


