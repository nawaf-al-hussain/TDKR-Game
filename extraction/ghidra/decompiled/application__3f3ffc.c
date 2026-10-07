// _ZN11Application13LoadInventoryEv @ 003f3ffc

undefined4 _ZN11Application13LoadInventoryEv(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  
  uVar2 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1);
  iVar1 = DAT_003f4110 + 0x3f4024;
  *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = 0;
  iVar1 = _ZN11Application14DecryptAndLoadEPKciP13CMemoryStream
                    (param_1,iVar1,0x1d,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1)
                    );
  if (iVar1 == 0) {
    *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = uVar2;
    return 0;
  }
  iVar1 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = uVar2;
  *(undefined4 *)(iVar1 + 0xc) = 0;
  iVar1 = _ZN6CLevel8GetLevelEv();
  if (iVar1 != 0) {
    _ZN11Application19LoadCurrentProgressEP13CMemoryStream
              (param_1,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
    uVar2 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    if (*(char *)(iVar1 + 0x47) == '\0') {
      iVar1 = _ZNK6CLevel18GetPlayerComponentEv(iVar1);
      _ZN10CInventory14SaveLoadGlobalEP13CMemoryStream(*(undefined4 *)(iVar1 + 0x5bc),uVar2);
    }
    iVar1 = *(int *)(DAT_003f4114 + 0x3f4084);
    if (iVar1 == 0) {
      return 1;
    }
    uVar2 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    _ZN13CMemoryStream8ReadBoolERb(uVar2,iVar1 + 0x25c);
    _ZN13CMemoryStream8ReadBoolERb(uVar2,iVar1 + 0x270);
    _ZN13CMemoryStream8ReadBoolERb(uVar2,iVar1 + 0x284);
    _ZN13CMemoryStream8ReadBoolERb(uVar2,iVar1 + 0x298);
    _ZN13CMemoryStream8ReadBoolERb(uVar2,iVar1 + 0x2ac);
    _ZN13CMemoryStream8ReadBoolERb(uVar2,iVar1 + 0x2c0);
    _ZN13CMemoryStream8ReadBoolERb(uVar2,iVar1 + 0x2d4);
    return 1;
  }
  return 1;
}


