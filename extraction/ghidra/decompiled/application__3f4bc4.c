// _ZN11Application7SuspendEv @ 003f4bc4

void _ZN11Application7SuspendEv(int param_1)

{
  undefined4 uVar1;
  undefined4 extraout_r0;
  int iVar2;
  uint *puVar3;
  int iVar4;
  uint in_fpscr;
  float __x;
  undefined1 auStack_48 [60];
  
  iVar4 = DAT_003f4d00;
  *(undefined1 *)((int)&__DT_SYMTAB[0x1e0].st_name + param_1) = 1;
  iVar4 = iVar4 + 0x3f4bf0;
  if (**(int **)(iVar4 + DAT_003f4d04) != 0) {
    _ZN15VoxSoundManager14PauseAllSoundsEi(**(undefined4 **)(iVar4 + DAT_003f4d08),0xffffffff);
  }
  if (*(int *)(DAT_003f4d0c + 0x3f4c1c) != 0) {
    _ZN13CMemoryStreamC1Ei(auStack_48,0x400);
    _ZN13CMemoryStream8WriteIntEi
              (auStack_48,*(undefined4 *)((int)&__DT_SYMTAB[0x1e0].st_size + param_1));
    uVar1 = _ZN3glf22AndroidGetMillisecondsEv();
    VectorSignedToFloat(uVar1,(byte)(in_fpscr >> 0x16) & 3);
    floorf(__x);
    _ZN13CMemoryStream10WriteFloatEf(auStack_48,extraout_r0);
    _ZN11Application14EncryptAndSaveEPKciP13CMemoryStream
              (param_1,DAT_003f4d10 + 0x3f4c7c,3,auStack_48);
    _ZN13CMemoryStreamD2Ev(auStack_48);
  }
  iVar2 = _ZN4glot15TrackingManager11GetInstanceEv();
  if (iVar2 != 0) {
    if (**(int **)(iVar4 + DAT_003f4d14) != 0) {
      _ZN13CQuestManager20SaveStoryMissionTimeEv();
    }
    _ZN11Application26SendTrackingEventInterruptEii_constprop_2567(param_1,0x8be7);
    _ZN4glot15TrackingManager11GetInstanceEv();
    _ZN4glot15TrackingManager14updateSaveFileEv();
  }
  puVar3 = (uint *)(DAT_003f4d18 + 0x3f4cd8);
  *(undefined1 *)((int)&__DT_SYMTAB[0x1f1].st_name + param_1 + 2) = 1;
  *puVar3 = *puVar3 & 0xfffff7f7;
  **(undefined4 **)(iVar4 + DAT_003f4d1c) = 1;
  return;
}


