// _ZN13CAIController17GetNoEnemiesAwareEP11CGameObject @ 0018ccc8

int _ZN13CAIController17GetNoEnemiesAwareEP11CGameObject(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  
  if ((param_2 == 0) || (*(char *)(param_2 + 0xed) == '\0')) {
    iVar4 = 0;
    for (iVar2 = *(int *)(param_1 + 0xb8); iVar2 != param_1 + 0xb0;
        iVar2 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar2)) {
      if ((0 < *(int *)(*(int *)(*(int *)(iVar2 + 0x10) + 0xac) + 0x18)) &&
         (iVar1 = _ZNK11CGameObject12IsAggressiveEv(*(int *)(iVar2 + 0x10)), iVar1 != 0)) {
        iVar4 = iVar4 + 1;
      }
    }
  }
  else {
    iVar2 = *(int *)(param_1 + 0x100);
    iVar4 = 0;
    if (iVar2 != param_1 + 0xf8) {
      iVar3 = *(int *)(iVar2 + 0x10);
      iVar1 = _ZNK11CGameObject12IsAggressiveEv(iVar3);
      if (iVar1 == 0) goto LAB_0018cd8c;
      do {
        iVar4 = iVar4 + 1;
        do {
          iVar2 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar2);
          if (param_1 + 0xf8 == iVar2) {
            return iVar4;
          }
          iVar3 = *(int *)(iVar2 + 0x10);
          iVar1 = _ZNK11CGameObject12IsAggressiveEv(iVar3);
          if (iVar1 != 0) break;
LAB_0018cd8c:
        } while (*(int *)(*(int *)(iVar3 + 0xac) + 0x18) < 1);
      } while( true );
    }
  }
  return iVar4;
}

