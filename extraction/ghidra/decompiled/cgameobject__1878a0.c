// _ZN13CAIController13SetEnemyAwareEP11CGameObject @ 001878a0

void _ZN13CAIController13SetEnemyAwareEP11CGameObject(int param_1,int *param_2)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  int iVar4;
  undefined4 uVar5;
  int *local_1c [2];
  
  iVar3 = param_1 + 0xf8;
  iVar1 = *(int *)(param_1 + 0xfc);
  iVar4 = iVar3;
  local_1c[0] = param_2;
  if (*(int *)(param_1 + 0xfc) == 0) {
LAB_00187920:
    if (*(int *)(param_1 + 0x100) == iVar4) {
      _ZNSt8_Rb_treeIP11CGameObjectS1_St9_IdentityIS1_ESt4lessIS1_ESaIS1_EE10_M_insert_EPKSt18_Rb_tree_node_baseSA_RKS1_
                (param_1 + 0xf4,0,iVar4,local_1c);
      goto LAB_001878f8;
    }
    iVar1 = _ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(iVar4);
    if (local_1c[0] <= *(int **)(iVar1 + 0x10)) goto LAB_001878f8;
  }
  else {
    do {
      iVar4 = iVar1;
      piVar2 = *(int **)(iVar4 + 0x10);
      if (param_2 < piVar2) {
        iVar1 = *(int *)(iVar4 + 8);
      }
      else {
        iVar1 = *(int *)(iVar4 + 0xc);
      }
    } while (iVar1 != 0);
    if (param_2 < piVar2) goto LAB_00187920;
    if (param_2 <= piVar2) goto LAB_001878f8;
  }
  if (iVar3 == iVar4) {
    uVar5 = 1;
  }
  else if (local_1c[0] < *(int **)(iVar4 + 0x10)) {
    uVar5 = 1;
  }
  else {
    uVar5 = 0;
  }
  iVar1 = _Znwj(0x14);
  if (iVar1 != -0x10) {
    *(int **)(iVar1 + 0x10) = local_1c[0];
  }
  _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(uVar5,iVar1,iVar4,iVar3);
  *(int *)(param_1 + 0x108) = *(int *)(param_1 + 0x108) + 1;
LAB_001878f8:
  _ZN11CGameObject13SetAwareStateEi(local_1c[0],1);
  (**(code **)(*local_1c[0] + 0x14))();
  return;
}

