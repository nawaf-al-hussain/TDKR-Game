// _Z14CPutBackWeaponP11CGameObjecti @ 00179934

void _Z14CPutBackWeaponP11CGameObjecti(int param_1,undefined4 param_2)

{
  if (*(int *)(param_1 + 0xb8) == 0) {
    return;
  }
  _ZN19CActorBaseComponent15OnPutBackWeaponEib(*(int *)(param_1 + 0xb8),param_2,0);
  return;
}

