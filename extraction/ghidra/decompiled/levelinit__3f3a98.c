// _ZN11Application23SaveLevelInitGlobalDataEv @ 003f3a98

undefined4 _ZN11Application23SaveLevelInitGlobalDataEv(int param_1)

{
  char cVar1;
  int iVar2;
  undefined4 uVar3;
  int *piVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 uVar7;
  undefined4 uStack_1c;
  int *piStack_18;
  undefined4 uStack_14;
  
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
              (**(undefined4 **)(DAT_003f3b60 + 0x3f3b0c),uVar7);
    _ZN13CQuestManager14SaveSaveGlobalEP13CMemoryStream
              (**(undefined4 **)(DAT_003f3b64 + 0x3f3b20),uVar7);
    uVar3 = _ZN10cSingletonI19cAchievementManagerE12getSingletonEv();
    _ZN19cAchievementManager10SaveGlobalEP13CMemoryStream(uVar3,uVar7);
  }
  iVar5 = DAT_003f3b68 + 0x3f3b48;
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
    iVar2 = _ZN11Application11GetInstanceEv();
    piVar4 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 0x28);
    (**(code **)(*piVar4 + 0x14))(&piStack_18,piVar4,iVar5,0,0);
    uVar3 = 0;
    if (piStack_18 != (int *)0x0) {
      (**(code **)(*piStack_18 + 0xc))(piStack_18,&uStack_1c,4);
      _ZN11CEncryption15PrepareForWriteEP13CMemoryStream
                (*(undefined4 *)(DAT_003eee04 + 0x3eed90),puVar6);
      uStack_14 = puVar6[2];
      (**(code **)(*piStack_18 + 0xc))(piStack_18,&uStack_14,4);
      (**(code **)(*piStack_18 + 0xc))(piStack_18,*puVar6,uStack_14);
      piVar4 = piStack_18;
      piStack_18 = (int *)0x0;
      if ((piVar4 == (int *)0x0) ||
         (_ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(), piStack_18 == (int *)0x0))
      {
        uVar3 = 1;
      }
      else {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
        uVar3 = 1;
      }
    }
  }
  return uVar3;
}


