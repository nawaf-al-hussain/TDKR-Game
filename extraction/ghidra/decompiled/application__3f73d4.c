// _ZN11Application16FillRedirectLinkERKSs @ 003f73d4

undefined4
_ZN11Application16FillRedirectLinkERKSs(undefined4 param_1,undefined4 param_2,undefined4 param_3)

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
  
  _ZNSsC1ERKSs(param_1,param_3);
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_003f762c + 0x3f73fc,0,8);
  if (iVar1 != -1) {
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,8,DAT_003f7630 + 0x3f7424,4);
    _ZNSs6assignERKSs(param_1,uVar2);
  }
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_003f7634 + 0x3f744c,0,7);
  if (iVar1 != -1) {
    _ZNSsC1EPKcRKSaIcE(&local_20,DAT_003f7638 + 0x3f746c,auStack_30);
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,7,local_20,*(undefined4 *)(local_20 + -0xc));
    _ZNSs6assignERKSs(param_1,uVar2);
    _ZNSsD1Ev(&local_20);
  }
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_003f763c + 0x3f74b4,0,4);
  if (iVar1 != -1) {
    _ZNSsC1EPKcRKSaIcE(&local_1c,DAT_003f7640 + 0x3f74d4,auStack_2c);
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,4,local_1c,*(undefined4 *)(local_1c + -0xc));
    _ZNSs6assignERKSs(param_1,uVar2);
    _ZNSsD1Ev(&local_1c);
  }
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_003f7644 + 0x3f751c,0,9);
  if (iVar1 != -1) {
    _ZNSsC1EPKcRKSaIcE(&local_18,DAT_003f7648 + 0x3f753c,auStack_28);
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,9,local_18,*(undefined4 *)(local_18 + -0xc));
    _ZNSs6assignERKSs(param_1,uVar2);
    _ZNSsD1Ev(&local_18);
  }
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_003f764c + 0x3f7584,0,8);
  if (iVar1 != -1) {
    _ZNSsC1EPKcRKSaIcE(local_14,DAT_003f7650 + 0x3f75a4,auStack_24);
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,8,local_14[0],*(undefined4 *)(local_14[0] + -0xc));
    _ZNSs6assignERKSs(param_1,uVar2);
    _ZNSsD1Ev(local_14);
  }
  iVar1 = _ZNKSs4findEPKcjj(param_1,DAT_003f7654 + 0x3f75ec,0,4);
  if (iVar1 != -1) {
    uVar2 = _ZNSs7replaceEjjPKcj(param_1,iVar1,4,DAT_003f7658 + 0x3f7610,4);
    _ZNSs6assignERKSs(param_1,uVar2);
  }
  return param_1;
}


