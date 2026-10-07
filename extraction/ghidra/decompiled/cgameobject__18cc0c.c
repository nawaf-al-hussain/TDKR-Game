// _ZN13CAIController15IsActorDetectedEP11CGameObject @ 0018cc0c

undefined4 _ZN13CAIController15IsActorDetectedEP11CGameObject(int param_1,int param_2)

{
  int iVar1;
  
  iVar1 = *(int *)(param_1 + 0xb8);
  while( true ) {
    if (param_1 + 0xb0 == iVar1) {
      return 0;
    }
    if ((((*(int *)(iVar1 + 0x10) != 0) &&
         (iVar1 = *(int *)(*(int *)(iVar1 + 0x10) + 0xac), iVar1 != 0)) &&
        (param_2 == *(int *)(iVar1 + 0x50))) && (0 < *(int *)(iVar1 + 0x18))) break;
    iVar1 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base();
  }
  return 1;
}

