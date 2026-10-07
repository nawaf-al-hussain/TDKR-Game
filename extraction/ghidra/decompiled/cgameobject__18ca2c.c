// _ZN13CAIController21Aware_IsTargetCloakedEP11CGameObject @ 0018ca2c

bool _ZN13CAIController21Aware_IsTargetCloakedEP11CGameObject(undefined4 param_1,int param_2)

{
  int iVar1;
  
  if (param_2 == 0) {
    return false;
  }
  iVar1 = *(int *)(param_2 + 0xb4);
  if ((iVar1 != 0) &&
     (iVar1 = _ZN18CStateSetComponent8GetStateERK9SStateIdx(iVar1,iVar1 + 0xd8),
     (*(uint *)(iVar1 + 4) & 0x100000) != 0)) {
    return true;
  }
  if (*(int *)(param_2 + 0xb8) != 0) {
    return *(int *)(*(int *)(param_2 + 0xb8) + 0x14) == 6;
  }
  return false;
}

