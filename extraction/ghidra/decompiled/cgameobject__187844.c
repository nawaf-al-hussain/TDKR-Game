// _ZN13CAIController12IsEnemyAwareEP11CGameObject @ 00187844

bool _ZN13CAIController12IsEnemyAwareEP11CGameObject(int param_1,uint param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar2 = param_1 + 0xf8;
  iVar1 = *(int *)(param_1 + 0xfc);
  iVar3 = iVar2;
  while (iVar1 != 0) {
    if (*(uint *)(iVar1 + 0x10) < param_2) {
      iVar1 = *(int *)(iVar1 + 0xc);
    }
    else {
      iVar1 = *(int *)(iVar1 + 8);
      iVar3 = iVar1;
    }
  }
  iVar1 = iVar2;
  if ((iVar2 != iVar3) && (*(uint *)(iVar3 + 0x10) <= param_2)) {
    iVar1 = iVar3;
  }
  return iVar2 != iVar1;
}

