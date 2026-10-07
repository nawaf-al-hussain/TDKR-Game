// _ZN11Application19SaveInventoryInFileEPKc @ 003f3c58

void _ZN11Application19SaveInventoryInFileEPKc
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  
  __android_log_print(4,DAT_003f3d68 + 0x3f3c80,DAT_003f3d64 + 0x3f3c7c,param_4,param_4);
  iVar2 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)(iVar2 + 0xc) = 0;
  *(undefined4 *)(iVar2 + 8) = 0;
  iVar2 = _ZN6CLevel8GetLevelEv();
  if (iVar2 != 0) {
    _ZN11Application19SaveCurrentProgressEP13CMemoryStream
              (param_1,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
    uVar3 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    iVar1 = _ZNK6CLevel18GetPlayerComponentEv(iVar2);
    iVar2 = DAT_003f3d6c;
    _ZN10CInventory14SaveSaveGlobalEP13CMemoryStream(*(undefined4 *)(iVar1 + 0x5bc),uVar3);
    iVar2 = *(int *)(iVar2 + 0x3f3cd0);
    if (iVar2 != 0) {
      uVar3 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
      _ZN13CMemoryStream5WriteEb(uVar3,*(undefined1 *)(iVar2 + 0x25c));
      _ZN13CMemoryStream5WriteEb(uVar3,*(undefined1 *)(iVar2 + 0x270));
      _ZN13CMemoryStream5WriteEb(uVar3,*(undefined1 *)(iVar2 + 0x284));
      _ZN13CMemoryStream5WriteEb(uVar3,*(undefined1 *)(iVar2 + 0x298));
      _ZN13CMemoryStream5WriteEb(uVar3,*(undefined1 *)(iVar2 + 0x2ac));
      _ZN13CMemoryStream5WriteEb(uVar3,*(undefined1 *)(iVar2 + 0x2c0));
      _ZN13CMemoryStream5WriteEb(uVar3,*(undefined1 *)(iVar2 + 0x2d4));
    }
  }
  uVar3 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1);
  *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = 0;
  _ZN11Application14EncryptAndSaveEPKciP13CMemoryStream
            (param_1,param_2,0x1d,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = uVar3;
  return;
}


