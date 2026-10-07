// _ZN11Application14CheckLoadLevelEv @ 003edfe0

void _ZN11Application14CheckLoadLevelEv(int param_1)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined1 *puVar7;
  int iVar8;
  int *piVar9;
  int iVar10;
  undefined4 uVar11;
  undefined4 *puVar12;
  undefined1 auStack_30 [4];
  undefined1 auStack_2c [8];
  
  iVar8 = DAT_003ee364 + 0x3ee004;
  if (*(int *)((int)&__DT_SYMTAB[0x1e7].st_size + param_1) < 0) {
    return;
  }
  puVar12 = *(undefined4 **)(iVar8 + DAT_003ee368);
  _ZN13CQuestManager16FailActiveQuestsE12E_QUEST_TYPE(*puVar12,2);
  _ZN13CQuestManager22StopSideMissionManagerEv(*puVar12);
  uVar1 = _Z11CustomAllocjPKci(0x94,DAT_003ee36c + 0x3ee038,0x9ed);
  _ZN10GS_LoadingC1Ev();
  puVar6 = (undefined4 *)(DAT_003ee374 + 0x3ee064);
  uVar2 = *(undefined4 *)(&__DT_SYMTAB[0x1e7].st_info + param_1);
  puVar7 = (undefined1 *)(DAT_003ee378 + 0x3ee06c);
  *(undefined4 *)(DAT_003ee370 + 0x3ee05c) =
       *(undefined4 *)((int)&__DT_SYMTAB[0x1e7].st_size + param_1);
  *puVar6 = uVar2;
  *puVar7 = 0;
  iVar3 = _ZN6CLevel8GetLevelEv();
  if (iVar3 != 0) {
    iVar3 = _ZN6CLevel8GetLevelEv();
    *(undefined4 *)(iVar3 + 0x10c) = 0xffffffff;
  }
  __android_log_print(4,DAT_003ee37c + 0x3ee0a8,DAT_003ee380 + 0x3ee0b0);
  iVar3 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)(iVar3 + 0xc) = 0;
  *(undefined4 *)(iVar3 + 8) = 0;
  iVar3 = _ZN6CLevel8GetLevelEv();
  if (iVar3 != 0) {
    _ZN11Application19SaveCurrentProgressEP13CMemoryStream
              (param_1,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
    uVar2 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    iVar4 = _ZNK6CLevel18GetPlayerComponentEv(iVar3);
    iVar3 = DAT_003ee384;
    _ZN10CInventory14SaveSaveGlobalEP13CMemoryStream(*(undefined4 *)(iVar4 + 0x5bc),uVar2);
    iVar3 = *(int *)(iVar3 + 0x3ee0fc);
    if (iVar3 != 0) {
      uVar2 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
      _ZN13CMemoryStream5WriteEb(uVar2,*(undefined1 *)(iVar3 + 0x25c));
      _ZN13CMemoryStream5WriteEb(uVar2,*(undefined1 *)(iVar3 + 0x270));
      _ZN13CMemoryStream5WriteEb(uVar2,*(undefined1 *)(iVar3 + 0x284));
      _ZN13CMemoryStream5WriteEb(uVar2,*(undefined1 *)(iVar3 + 0x298));
      _ZN13CMemoryStream5WriteEb(uVar2,*(undefined1 *)(iVar3 + 0x2ac));
      _ZN13CMemoryStream5WriteEb(uVar2,*(undefined1 *)(iVar3 + 0x2c0));
      _ZN13CMemoryStream5WriteEb(uVar2,*(undefined1 *)(iVar3 + 0x2d4));
    }
  }
  uVar11 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1);
  iVar3 = DAT_003ee388 + 0x3ee180;
  uVar2 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = 0;
  _ZN11Application14EncryptAndSaveEPKciP13CMemoryStream(param_1,iVar3,0x1d,uVar2);
  iVar3 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1) = uVar11;
  *(undefined4 *)(iVar3 + 0xc) = 0;
  *(undefined4 *)(iVar3 + 8) = 0;
  iVar3 = _ZN6CLevel8GetLevelEv();
  uVar2 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  if (iVar3 == 0) {
    _ZN13CMemoryStream9WriteByteEh(uVar2,0);
  }
  else {
    _ZN13CMemoryStream9WriteByteEh(uVar2,1);
    uVar11 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    _ZN13CMemoryStream5WriteEi(uVar11,*(undefined4 *)(iVar3 + 0x10c));
    _ZN6CLevel17SaveGlobalObjectsEP13CMemoryStream(iVar3,uVar11);
    uVar2 = _ZNK6CLevel18GetPlayerComponentEv(iVar3);
    _ZN15PlayerComponent13SaveMaxHealthEP13CMemoryStream(uVar2,uVar11);
    _ZN14CScriptGlobals14SaveSaveGlobalEP13CMemoryStream
              (**(undefined4 **)(iVar8 + DAT_003ee38c),uVar11);
    _ZN13CQuestManager14SaveSaveGlobalEP13CMemoryStream(*puVar12,uVar11);
    uVar2 = _ZN10cSingletonI19cAchievementManagerE12getSingletonEv();
    _ZN19cAchievementManager10SaveGlobalEP13CMemoryStream(uVar2,uVar11);
  }
  _ZN11Application14EncryptAndSaveEPKciP13CMemoryStream
            (param_1,DAT_003ee390 + 0x3ee224,0x16,
             *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  iVar3 = _ZN11Application11GetInstanceEv();
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
            (auStack_30,
             *(int *)((int)&__DT_SYMTAB[0x1e7].st_size + param_1) * 0x114 + DAT_003ee394 + 0x3ee2a0)
  ;
  iVar10 = *(int *)((int)&__DT_SYMTAB[0x1e7].st_size + param_1);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_2c,auStack_30);
  iVar4 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + iVar3);
  *(undefined4 *)(iVar4 + 0xc) = 0;
  *(undefined4 *)(iVar4 + 8) = 0;
  _ZN13CMemoryStream9WriteByteEh(iVar4,0);
  iVar4 = _ZN6CLevel8GetLevelEv();
  if (iVar10 < 0) {
    iVar10 = *(int *)(iVar4 + 0xc0);
  }
  iVar5 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                    (auStack_2c,DAT_003ee398 + 0x3ee2a0);
  if (iVar5 == 0) {
    if (iVar4 == 0) goto LAB_003ee2ec;
    puVar7 = *(undefined1 **)(iVar8 + DAT_003ee39c);
  }
  else {
    puVar7 = auStack_2c;
  }
  _ZN13CMemoryStream12WriteStringCERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + iVar3),puVar7);
  _ZN13CMemoryStream8WriteIntEi(*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + iVar3),iVar10);
LAB_003ee2ec:
  _ZN11Application14EncryptAndSaveEPKciP13CMemoryStream
            (iVar3,DAT_003ee3a0 + 0x3ee304,0xb4,
             *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + iVar3));
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_2c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_30);
  piVar9 = *(int **)(iVar8 + DAT_003ee3a4);
  _ZN12gxStateStack15ClearStateStackEv(*piVar9 + 4);
  _ZN12gxStateStack9PushStateEP11gxGameState(*piVar9 + 4,uVar1);
  *(undefined4 *)((int)&__DT_SYMTAB[0x1e7].st_size + param_1) = 0xffffffff;
  return;
}


