// _ZN11Application20SaveGlobalDataInFileEPKc @ 003f29b8

/* WARNING: Removing unreachable block (ram,0x003eede8) */

undefined4 _ZN11Application20SaveGlobalDataInFileEPKc(int param_1,undefined4 param_2)

{
  char cVar1;
  int iVar2;
  undefined4 uVar3;
  int *piVar4;
  int iVar5;
  undefined4 *puVar6;
  int *unaff_r4;
  undefined4 uVar7;
  undefined4 uStack_1c;
  
  iVar5 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)(iVar5 + 0xc) = 0;
  *(undefined4 *)(iVar5 + 8) = 0;
  iVar5 = _ZN6CLevel8GetLevelEv();
  uVar3 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  if (iVar5 == 0) {
    _ZN13CMemoryStream9WriteByteEh(uVar3,0);
  }
  else {
    _ZN13CMemoryStream9WriteByteEh(uVar3,1);
    uVar7 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    _ZN13CMemoryStream5WriteEi(uVar7,*(undefined4 *)(iVar5 + 0x10c));
    _ZN6CLevel17SaveGlobalObjectsEP13CMemoryStream(iVar5,uVar7);
    uVar3 = _ZNK6CLevel18GetPlayerComponentEv(iVar5);
    _ZN15PlayerComponent13SaveMaxHealthEP13CMemoryStream(uVar3,uVar7);
    _ZN14CScriptGlobals14SaveSaveGlobalEP13CMemoryStream
              (**(undefined4 **)(DAT_003f2a80 + 0x3f2a30),uVar7);
    _ZN13CQuestManager14SaveSaveGlobalEP13CMemoryStream
              (**(undefined4 **)(DAT_003f2a84 + 0x3f2a44),uVar7);
    uVar3 = _ZN10cSingletonI19cAchievementManagerE12getSingletonEv();
    _ZN19cAchievementManager10SaveGlobalEP13CMemoryStream(uVar3,uVar7);
  }
  puVar6 = *(undefined4 **)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  cVar1 = *(char *)(DAT_003eedfc + 0x3eec90);
  uStack_1c = 0x16;
  *(char *)(DAT_003eee00 + 0x3eeca4) = cVar1;
  if (cVar1 == '\0') {
    iVar5 = _ZN11Application11GetInstanceEv();
    iVar5 = *(int *)((int)&__DT_SYMTAB[0x1df].st_name + iVar5);
    iVar5 = *(int *)(iVar5 + 8) + *(int *)(*(int *)(iVar5 + 0xc) + 0x1330) * 2;
    if (iVar5 == 0) {
      uVar3 = 0;
    }
    else {
      iVar2 = _Znaj(0x100);
      _Z21_ConvertUnicodeToUTF8PcPKt(iVar2,iVar5);
      iVar5 = _ZN11Application11GetInstanceEv();
      (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar5) + 0x5c))
                (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar5),iVar2);
      uVar3 = 0;
      if (iVar2 != 0) {
        _ZdaPv();
        uVar3 = 0;
      }
    }
  }
  else {
    iVar5 = _ZN11Application11GetInstanceEv();
    piVar4 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar5) + 0x28);
    (**(code **)(*piVar4 + 0x14))(&stack0xffffffe8,piVar4,param_2,0,0);
    uVar3 = 0;
    if (unaff_r4 != (int *)0x0) {
      (**(code **)(*unaff_r4 + 0xc))(unaff_r4,&uStack_1c,4);
      _ZN11CEncryption15PrepareForWriteEP13CMemoryStream
                (*(undefined4 *)(DAT_003eee04 + 0x3eed90),puVar6);
      uVar3 = puVar6[2];
      (**(code **)(*unaff_r4 + 0xc))(unaff_r4,&stack0xffffffec,4);
      (**(code **)(*unaff_r4 + 0xc))(unaff_r4,*puVar6,uVar3);
      if (unaff_r4 != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      uVar3 = 1;
    }
  }
  return uVar3;
}


