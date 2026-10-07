// _ZN13CAIController12AlertEnemiesEP11CGameObject @ 00187b24

void _ZN13CAIController12AlertEnemiesEP11CGameObject(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  
  for (iVar2 = *(int *)(param_1 + 0xb8); param_1 + 0xb0 != iVar2;
      iVar2 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar2)) {
    iVar1 = *(int *)(iVar2 + 0x10);
    if (((param_2 != iVar1 && iVar1 != 0) && (iVar1 = *(int *)(iVar1 + 0xac), iVar1 != 0)) &&
       (*(int *)(iVar1 + 0x18) < 1)) {
      _ZN19CAwarenessComponent5AlertEbb(iVar1,1,0);
    }
  }
  return;
}

