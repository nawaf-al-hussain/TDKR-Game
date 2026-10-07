// _ZN11Application15TutorialStartedEv @ 003f0ed0

void _ZN11Application15TutorialStartedEv(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  
  *(undefined4 *)((int)&__DT_SYMTAB[0x1e2].st_name + param_1) = 0;
  iVar1 = _ZN6CLevel8GetLevelEv();
  if (iVar1 == 0) {
    return;
  }
  iVar1 = _ZN6CLevel8GetLevelEv();
  if (*(int *)(iVar1 + 0xec) == 0) {
    return;
  }
  _ZN6CLevel8GetLevelEv();
  iVar1 = _ZNK6CLevel18GetPlayerComponentEv();
  if (iVar1 == 0) {
    return;
  }
  _ZN6CLevel8GetLevelEv();
  iVar1 = _ZNK6CLevel18GetPlayerInventoryEv();
  if (iVar1 == 0) {
    return;
  }
  _ZN6CLevel8GetLevelEv();
  uVar2 = _ZNK6CLevel18GetPlayerInventoryEv();
  uVar2 = _ZN10CInventory17GetCurrencyPointsEi(uVar2,2);
  *(undefined4 *)((int)&__DT_SYMTAB[0x1e2].st_name + param_1) = uVar2;
  return;
}


