// _Z17CGetCurrentWeaponP11CGameObject @ 0017991c

undefined4 _Z17CGetCurrentWeaponP11CGameObject(int param_1)

{
  undefined4 uVar1;
  
  if (*(int *)(param_1 + 0xb8) != 0) {
    uVar1 = _ZN19CActorBaseComponent20GetCurrentWeaponTypeEv();
    return uVar1;
  }
  return 0xffffffff;
}

