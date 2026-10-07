// _ZN6CLevel14LoadGlobalDataEP13CMemoryStream @ 00403a94

undefined4 _ZN6CLevel14LoadGlobalDataEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int iVar2;
  int iVar3;
  int local_14;
  
  _ZN13CMemoryStream4ReadERi(param_2,&local_14);
  iVar3 = DAT_00403b64 + 0x403ac4;
  if ((0 < local_14) && (**(char **)(iVar3 + DAT_00403b68) == '\0')) {
    iVar2 = _ZN6CLevel8GetLevelEv();
    *(int *)(iVar2 + 0x10c) = local_14;
  }
  if (*(char *)(param_1 + 0x47) == '\0') {
    _ZN6CLevel17LoadGlobalObjectsEP13CMemoryStream(param_1,param_2);
    uVar1 = _ZNK6CLevel18GetPlayerComponentEv(param_1);
    _ZN15PlayerComponent13LoadMaxHealthEP13CMemoryStream(uVar1,param_2);
    _ZN14CScriptGlobals14SaveLoadGlobalEP13CMemoryStream
              (**(undefined4 **)(iVar3 + DAT_00403b6c),param_2);
    _ZN13CQuestManager14SaveLoadGlobalEP13CMemoryStream
              (**(undefined4 **)(iVar3 + DAT_00403b70),param_2);
    uVar1 = _ZN10cSingletonI19cAchievementManagerE12getSingletonEv();
    _ZN19cAchievementManager10LoadGlobalEP13CMemoryStream(uVar1,param_2);
    _ZN8CLottery10LoadGlobalEv(*(undefined4 *)(**(int **)(iVar3 + DAT_00403b74) + 0x68));
  }
  return 1;
}

