// _ZN11Application14SaveGlobalDataEv @ 003f36c0

/* WARNING: Removing unreachable block (ram,0x003eede8) */

undefined4 _ZN11Application14SaveGlobalDataEv(int param_1)

{
  char cVar1;
  int iVar2;
  int *piVar3;
  int iVar4;
  undefined4 *puVar5;
  int *unaff_r4;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 uStack_1c;
  
  __android_log_print(4,DAT_003f387c + 0x3f36e0,DAT_003f3880 + 0x3f36e4);
  iVar4 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)(iVar4 + 0xc) = 0;
  *(undefined4 *)(iVar4 + 8) = 0;
  iVar4 = _ZN6CLevel8GetLevelEv();
  if (iVar4 != 0) {
    _ZN11Application19SaveCurrentProgressEP13CMemoryStream
              (param_1,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
    uVar6 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    iVar2 = _ZNK6CLevel18GetPlayerComponentEv(iVar4);
    iVar4 = DAT_003f3884;
    _ZN10CInventory14SaveSaveGlobalEP13CMemoryStream(*(undefined4 *)(iVar2 + 0x5bc),uVar6);
    iVar4 = *(int *)(iVar4 + 0x3f3734);
    if (iVar4 != 0) {
      uVar6 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
      _ZN13CMemoryStream5WriteEb(uVar6,*(undefined1 *)(iVar4 + 0x25c));
      _ZN13CMemoryStream5WriteEb(uVar6,*(undefined1 *)(iVar4 + 0x270));
      _ZN13CMemoryStream5WriteEb(uVar6,*(undefined1 *)(iVar4 + 0x284));
      _ZN13CMemoryStream5WriteEb(uVar6,*(undefined1 *)(iVar4 + 0x298));
      _ZN13CMemoryStream5WriteEb(uVar6,*(undefined1 *)(iVar4 + 0x2ac));
      _ZN13CMemoryStream5WriteEb(uVar6,*(undefined1 *)(iVar4 + 0x2c0));
      _ZN13CMemoryStream5WriteEb(uVar6,*(undefined1 *)(iVar4 + 0x2d4));
    }
  }
  uVar7 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1);
  iVar4 = DAT_003f3888 + 0x3f37b8;
  uVar6 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = 0;
  _ZN11Application14EncryptAndSaveEPKciP13CMemoryStream(param_1,iVar4,0x1d,uVar6);
  iVar4 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = uVar7;
  *(undefined4 *)(iVar4 + 0xc) = 0;
  *(undefined4 *)(iVar4 + 8) = 0;
  iVar4 = _ZN6CLevel8GetLevelEv();
  uVar6 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  if (iVar4 == 0) {
    _ZN13CMemoryStream9WriteByteEh(uVar6,0);
  }
  else {
    _ZN13CMemoryStream9WriteByteEh(uVar6,1);
    uVar7 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    _ZN13CMemoryStream5WriteEi(uVar7,*(undefined4 *)(iVar4 + 0x10c));
    _ZN6CLevel17SaveGlobalObjectsEP13CMemoryStream(iVar4,uVar7);
    uVar6 = _ZNK6CLevel18GetPlayerComponentEv(iVar4);
    _ZN15PlayerComponent13SaveMaxHealthEP13CMemoryStream(uVar6,uVar7);
    _ZN14CScriptGlobals14SaveSaveGlobalEP13CMemoryStream
              (**(undefined4 **)(DAT_003f388c + 0x3f3828),uVar7);
    _ZN13CQuestManager14SaveSaveGlobalEP13CMemoryStream
              (**(undefined4 **)(DAT_003f3890 + 0x3f383c),uVar7);
    uVar6 = _ZN10cSingletonI19cAchievementManagerE12getSingletonEv();
    _ZN19cAchievementManager10SaveGlobalEP13CMemoryStream(uVar6,uVar7);
  }
  iVar4 = DAT_003f3894 + 0x3f3864;
  puVar5 = *(undefined4 **)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  cVar1 = *(char *)(DAT_003eedfc + 0x3eec90);
  uStack_1c = 0x16;
  *(char *)(DAT_003eee00 + 0x3eeca4) = cVar1;
  if (cVar1 == '\0') {
    iVar4 = _ZN11Application11GetInstanceEv();
    iVar4 = *(int *)((int)&__DT_SYMTAB[0x1df].st_name + iVar4);
    iVar4 = *(int *)(iVar4 + 8) + *(int *)(*(int *)(iVar4 + 0xc) + 0x1330) * 2;
    if (iVar4 == 0) {
      uVar6 = 0;
    }
    else {
      iVar2 = _Znaj(0x100);
      _Z21_ConvertUnicodeToUTF8PcPKt(iVar2,iVar4);
      iVar4 = _ZN11Application11GetInstanceEv();
      (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar4) + 0x5c))
                (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar4),iVar2);
      uVar6 = 0;
      if (iVar2 != 0) {
        _ZdaPv();
        uVar6 = 0;
      }
    }
  }
  else {
    iVar2 = _ZN11Application11GetInstanceEv();
    piVar3 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 0x28);
    (**(code **)(*piVar3 + 0x14))(&stack0xffffffe8,piVar3,iVar4,0,0);
    uVar6 = 0;
    if (unaff_r4 != (int *)0x0) {
      (**(code **)(*unaff_r4 + 0xc))(unaff_r4,&uStack_1c,4);
      _ZN11CEncryption15PrepareForWriteEP13CMemoryStream
                (*(undefined4 *)(DAT_003eee04 + 0x3eed90),puVar5);
      uVar6 = puVar5[2];
      (**(code **)(*unaff_r4 + 0xc))(unaff_r4,&stack0xffffffec,4);
      (**(code **)(*unaff_r4 + 0xc))(unaff_r4,*puVar5,uVar6);
      if (unaff_r4 != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      uVar6 = 1;
    }
  }
  return uVar6;
}


