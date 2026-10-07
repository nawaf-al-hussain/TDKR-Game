// _ZN13CAIController22Alliance_RegisterEnemyEP11CGameObject @ 00188580

void _ZN13CAIController22Alliance_RegisterEnemyEP11CGameObject(int param_1,uint param_2)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  undefined4 uVar5;
  uint local_1c [2];
  
  iVar3 = param_1 + 0xb0;
  iVar1 = *(int *)(param_1 + 0xb4);
  iVar4 = iVar3;
  local_1c[0] = param_2;
  if (*(int *)(param_1 + 0xb4) != 0) {
    do {
      iVar4 = iVar1;
      uVar2 = *(uint *)(iVar4 + 0x10);
      if (param_2 < uVar2) {
        iVar1 = *(int *)(iVar4 + 8);
      }
      else {
        iVar1 = *(int *)(iVar4 + 0xc);
      }
    } while (iVar1 != 0);
    if (uVar2 <= param_2) {
      if (param_2 <= uVar2) {
        return;
      }
      goto LAB_00188608;
    }
  }
  if (*(int *)(param_1 + 0xb8) == iVar4) {
    _ZNSt8_Rb_treeIP11CGameObjectS1_St9_IdentityIS1_ESt4lessIS1_ESaIS1_EE10_M_insert_EPKSt18_Rb_tree_node_baseSA_RKS1_
              (param_1 + 0xac,0,iVar4,local_1c);
    return;
  }
  iVar1 = _ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(iVar4);
  if (local_1c[0] <= *(uint *)(iVar1 + 0x10)) {
    return;
  }
LAB_00188608:
  if (iVar3 == iVar4) {
    uVar5 = 1;
  }
  else if (local_1c[0] < *(uint *)(iVar4 + 0x10)) {
    uVar5 = 1;
  }
  else {
    uVar5 = 0;
  }
  iVar1 = _Znwj(0x14);
  if (iVar1 != -0x10) {
    *(uint *)(iVar1 + 0x10) = local_1c[0];
  }
  _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(uVar5,iVar1,iVar4,iVar3);
  *(int *)(param_1 + 0xc0) = *(int *)(param_1 + 0xc0) + 1;
  return;
}

