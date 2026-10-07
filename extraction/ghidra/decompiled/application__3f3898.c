// _ZN11Application14LoadGlobalDataEv @ 003f3898

undefined4 _ZN11Application14LoadGlobalDataEv(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  int unaff_r5;
  undefined4 uVar5;
  
  uVar5 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1);
  iVar4 = DAT_003f3a20 + 0x3f38c0;
  *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = 0;
  iVar4 = _ZN11Application14DecryptAndLoadEPKciP13CMemoryStream
                    (param_1,iVar4,0x1d,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1)
                    );
  if (iVar4 == 0) {
    *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = uVar5;
    uVar5 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  }
  else {
    iVar4 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = uVar5;
    *(undefined4 *)(iVar4 + 0xc) = 0;
    iVar4 = _ZN6CLevel8GetLevelEv();
    if (iVar4 == 0) {
      uVar5 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    }
    else {
      _ZN11Application19LoadCurrentProgressEP13CMemoryStream
                (param_1,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
      uVar5 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
      if (*(char *)(iVar4 + 0x47) == '\0') {
        iVar4 = _ZNK6CLevel18GetPlayerComponentEv(iVar4);
        _ZN10CInventory14SaveLoadGlobalEP13CMemoryStream(*(undefined4 *)(iVar4 + 0x5bc),uVar5);
        uVar5 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
      }
      iVar4 = *(int *)(DAT_003f3a24 + 0x3f391c);
      if (iVar4 != 0) {
        _ZN13CMemoryStream8ReadBoolERb(uVar5,iVar4 + 0x25c);
        _ZN13CMemoryStream8ReadBoolERb(uVar5,iVar4 + 0x270);
        _ZN13CMemoryStream8ReadBoolERb(uVar5,iVar4 + 0x284);
        _ZN13CMemoryStream8ReadBoolERb(uVar5,iVar4 + 0x298);
        _ZN13CMemoryStream8ReadBoolERb(uVar5,iVar4 + 0x2ac);
        _ZN13CMemoryStream8ReadBoolERb(uVar5,iVar4 + 0x2c0);
        _ZN13CMemoryStream8ReadBoolERb(uVar5,iVar4 + 0x2d4);
        uVar5 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
      }
    }
  }
  iVar4 = _ZN11Application14DecryptAndLoadEPKciP13CMemoryStream
                    (param_1,DAT_003f3a28 + 0x3f3998,0x16,uVar5);
  if (iVar4 == 0) {
    return 0;
  }
  *(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1) + 0xc) = 0;
  iVar4 = _ZN6CLevel8GetLevelEv();
  iVar1 = _ZN13CMemoryStream8ReadByteEv
                    (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  if (iVar4 == 0) {
    return 1;
  }
  if (iVar1 == 1) {
    uVar5 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    _ZN13CMemoryStream4ReadERi(uVar5,&stack0xffffffec);
    iVar1 = DAT_00403b64 + 0x403ac4;
    if ((0 < unaff_r5) && (**(char **)(iVar1 + DAT_00403b68) == '\0')) {
      iVar3 = _ZN6CLevel8GetLevelEv();
      *(int *)(iVar3 + 0x10c) = unaff_r5;
    }
    if (*(char *)(iVar4 + 0x47) == '\0') {
      _ZN6CLevel17LoadGlobalObjectsEP13CMemoryStream(iVar4,uVar5);
      uVar2 = _ZNK6CLevel18GetPlayerComponentEv(iVar4);
      _ZN15PlayerComponent13LoadMaxHealthEP13CMemoryStream(uVar2,uVar5);
      _ZN14CScriptGlobals14SaveLoadGlobalEP13CMemoryStream
                (**(undefined4 **)(iVar1 + DAT_00403b6c),uVar5);
      _ZN13CQuestManager14SaveLoadGlobalEP13CMemoryStream
                (**(undefined4 **)(iVar1 + DAT_00403b70),uVar5);
      uVar2 = _ZN10cSingletonI19cAchievementManagerE12getSingletonEv();
      _ZN19cAchievementManager10LoadGlobalEP13CMemoryStream(uVar2,uVar5);
      _ZN8CLottery10LoadGlobalEv(*(undefined4 *)(**(int **)(iVar1 + DAT_00403b74) + 0x68));
    }
    return 1;
  }
  return 1;
}


