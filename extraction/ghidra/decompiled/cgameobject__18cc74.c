// _ZN13CAIController21GetNoEnemiesAttackingEP11CGameObject @ 0018cc74

int _ZN13CAIController21GetNoEnemiesAttackingEP11CGameObject(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar3 = 0;
  for (iVar2 = *(int *)(param_1 + 0xb8); param_1 + 0xb0 != iVar2;
      iVar2 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar2)) {
    if ((*(int *)(iVar2 + 0x10) != 0) &&
       (iVar1 = _ZN11CGameObject11IsAttackingEPS_b(*(int *)(iVar2 + 0x10),param_2,0), iVar1 != 0)) {
      iVar3 = iVar3 + 1;
    }
  }
  return iVar3;
}

