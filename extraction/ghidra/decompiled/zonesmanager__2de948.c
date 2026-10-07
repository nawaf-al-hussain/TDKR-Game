// _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4_.constprop.2910 @ 002de948

int _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_2910
              (int param_1,int param_2,int param_3,int *param_4)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  bool bVar5;
  int *piVar6;
  
  if (param_2 == 0) {
    if (param_3 == param_1 + 4) {
      bVar5 = true;
    }
    else {
      bVar5 = *param_4 < *(int *)(param_3 + 0x10);
    }
  }
  else {
    bVar5 = true;
  }
  piVar6 = param_4;
  iVar1 = _Znwj(0x24);
  if ((int *)(iVar1 + 0x10) != (int *)0x0) {
    iVar2 = param_4[1];
    iVar3 = param_4[2];
    iVar4 = param_4[3];
    *(int *)(iVar1 + 0x10) = *param_4;
    *(int *)(iVar1 + 0x14) = iVar2;
    *(int *)(iVar1 + 0x18) = iVar3;
    *(int *)(iVar1 + 0x1c) = iVar4;
    *(int *)(iVar1 + 0x20) = param_4[4];
  }
  _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
            (bVar5,iVar1,param_3,param_1 + 4,piVar6);
  *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
  return iVar1;
}


