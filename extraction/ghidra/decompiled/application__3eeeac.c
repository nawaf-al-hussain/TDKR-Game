// _ZN11Application12LoadUserInfoEv @ 003eeeac

undefined4 _ZN11Application12LoadUserInfoEv(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  float fVar3;
  float extraout_r0;
  undefined4 uVar4;
  uint in_fpscr;
  float __x;
  undefined1 auStack_50 [60];
  
  uVar4 = 0;
  if (*(int *)(DAT_003eef8c + 0x3eeec8) != 0) {
    _ZN13CMemoryStreamC1Ei(auStack_50,0x400);
    iVar1 = _ZN11Application14DecryptAndLoadEPKciP13CMemoryStream
                      (param_1,DAT_003eef90 + 0x3eeeec,3,auStack_50);
    uVar4 = 0;
    if (iVar1 != 0) {
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e0].st_size + param_1) = 0;
      uVar4 = 1;
      uVar2 = _ZN13CMemoryStream7ReadIntEv(auStack_50);
      *(undefined4 *)(&__DT_SYMTAB[0x1e0].st_info + param_1) = uVar2;
      fVar3 = (float)_ZN13CMemoryStream9ReadFloatEv(auStack_50);
      uVar2 = _ZN3glf22AndroidGetMillisecondsEv();
      VectorSignedToFloat(uVar2,(byte)(in_fpscr >> 0x16) & 3);
      ceilf(__x);
      iVar1 = (int)(extraout_r0 - fVar3);
      if (iVar1 < 1) {
        iVar1 = 1;
      }
      *(int *)((int)&__DT_SYMTAB[0x1e1].st_name + param_1) = iVar1;
    }
    _ZN13CMemoryStreamD2Ev(auStack_50);
  }
  return uVar4;
}


