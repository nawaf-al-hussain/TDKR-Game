// _ZNK11Application23GetCashGainedInTutorialEv @ 003f0f3c

uint _ZNK11Application23GetCashGainedInTutorialEv(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  uint uVar3;
  
  iVar1 = _ZN6CLevel8GetLevelEv();
  if (iVar1 == 0) {
    return 0;
  }
  iVar1 = _ZN6CLevel8GetLevelEv();
  if (*(int *)(iVar1 + 0xec) == 0) {
    return 0;
  }
  _ZN6CLevel8GetLevelEv();
  iVar1 = _ZNK6CLevel18GetPlayerComponentEv();
  if (iVar1 == 0) {
    return 0;
  }
  _ZN6CLevel8GetLevelEv();
  iVar1 = _ZNK6CLevel18GetPlayerInventoryEv();
  if (iVar1 == 0) {
    return 0;
  }
  _ZN6CLevel8GetLevelEv();
  uVar2 = _ZNK6CLevel18GetPlayerInventoryEv();
  iVar1 = _ZN10CInventory17GetCurrencyPointsEi(uVar2,2);
  uVar3 = iVar1 - *(int *)((int)&__DT_SYMTAB[0x1e2].st_name + param_1);
  return uVar3 & ~((int)uVar3 >> 0x1f);
}


