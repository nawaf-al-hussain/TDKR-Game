// _ZN11Application22LoadGlobalDataFromFileEPKc @ 003f2a88

undefined4 _ZN11Application22LoadGlobalDataFromFileEPKc(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 uVar5;
  int iStack_14;
  
  iVar1 = _ZN11Application14DecryptAndLoadEPKciP13CMemoryStream
                    (param_1,param_2,0x16,
                     *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  if (iVar1 == 0) {
    return 0;
  }
  *(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1) + 0xc) = 0;
  iVar1 = _ZN6CLevel8GetLevelEv();
  iVar2 = _ZN13CMemoryStream8ReadByteEv
                    (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  if (iVar1 != 0) {
    if (iVar2 == 1) {
      uVar5 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
      _ZN13CMemoryStream4ReadERi(uVar5,&iStack_14);
      iVar2 = DAT_00403b64 + 0x403ac4;
      if ((0 < iStack_14) && (**(char **)(iVar2 + DAT_00403b68) == '\0')) {
        iVar4 = _ZN6CLevel8GetLevelEv();
        *(int *)(iVar4 + 0x10c) = iStack_14;
      }
      if (*(char *)(iVar1 + 0x47) == '\0') {
        _ZN6CLevel17LoadGlobalObjectsEP13CMemoryStream(iVar1,uVar5);
        uVar3 = _ZNK6CLevel18GetPlayerComponentEv(iVar1);
        _ZN15PlayerComponent13LoadMaxHealthEP13CMemoryStream(uVar3,uVar5);
        _ZN14CScriptGlobals14SaveLoadGlobalEP13CMemoryStream
                  (**(undefined4 **)(iVar2 + DAT_00403b6c),uVar5);
        _ZN13CQuestManager14SaveLoadGlobalEP13CMemoryStream
                  (**(undefined4 **)(iVar2 + DAT_00403b70),uVar5);
        uVar3 = _ZN10cSingletonI19cAchievementManagerE12getSingletonEv();
        _ZN19cAchievementManager10LoadGlobalEP13CMemoryStream(uVar3,uVar5);
        _ZN8CLottery10LoadGlobalEv(*(undefined4 *)(**(int **)(iVar2 + DAT_00403b74) + 0x68));
      }
      return 1;
    }
    return 1;
  }
  return 1;
}


