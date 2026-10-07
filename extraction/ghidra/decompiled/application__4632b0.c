// _ZN11Application16FillRedirectLinkERKSs.constprop.2499 @ 004632b0

undefined4 _ZN11Application16FillRedirectLinkERKSs_constprop_2499(undefined4 param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined1 auStack_30 [4];
  undefined1 auStack_2c [4];
  undefined1 auStack_28 [4];
  undefined1 auStack_24 [4];
  int local_20;
  int local_1c;
  int local_18;
  int local_14 [2];
  
  _ZNSsC1ERKSs();
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_00463504 + 0x4632d8,0,8);
  if (iVar1 != -1) {
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,8,DAT_00463508 + 0x4632fc,4);
    _ZNSs6assignERKSs(param_1,uVar2);
  }
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_0046350c + 0x463324,0,7);
  if (iVar1 != -1) {
    _ZNSsC1EPKcRKSaIcE(local_14,DAT_00463510 + 0x463344,auStack_24);
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,7,local_14[0],*(undefined4 *)(local_14[0] + -0xc));
    _ZNSs6assignERKSs(param_1,uVar2);
    _ZNSsD1Ev(local_14);
  }
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_00463514 + 0x46338c,0,4);
  if (iVar1 != -1) {
    _ZNSsC1EPKcRKSaIcE(&local_18,DAT_00463518 + 0x4633ac,auStack_28);
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,4,local_18,*(undefined4 *)(local_18 + -0xc));
    _ZNSs6assignERKSs(param_1,uVar2);
    _ZNSsD1Ev(&local_18);
  }
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_0046351c + 0x4633f4,0,9);
  if (iVar1 != -1) {
    _ZNSsC1EPKcRKSaIcE(&local_1c,DAT_00463520 + 0x463414,auStack_2c);
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,9,local_1c,*(undefined4 *)(local_1c + -0xc));
    _ZNSs6assignERKSs(param_1,uVar2);
    _ZNSsD1Ev(&local_1c);
  }
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_00463524 + 0x46345c,0,8);
  if (iVar1 != -1) {
    _ZNSsC1EPKcRKSaIcE(&local_20,DAT_00463528 + 0x46347c,auStack_30);
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,8,local_20,*(undefined4 *)(local_20 + -0xc));
    _ZNSs6assignERKSs(param_1,uVar2);
    _ZNSsD1Ev(&local_20);
  }
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_0046352c + 0x4634c4,0,4);
  if (iVar1 != -1) {
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,4,DAT_00463530 + 0x4634e8,4);
    _ZNSs6assignERKSs(param_1,uVar2);
  }
  return param_1;
}


