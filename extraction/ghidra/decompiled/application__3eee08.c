// _ZN11Application12SaveUserInfoEv @ 003eee08

undefined4 _ZN11Application12SaveUserInfoEv(int param_1)

{
  undefined4 uVar1;
  undefined4 extraout_r0;
  uint in_fpscr;
  float __x;
  undefined1 auStack_40 [56];
  
  if (*(int *)(DAT_003eeea4 + 0x3eee18) == 0) {
    uVar1 = 0;
  }
  else {
    _ZN13CMemoryStreamC1Ei(auStack_40,0x400);
    _ZN13CMemoryStream8WriteIntEi
              (auStack_40,*(undefined4 *)((int)&__DT_SYMTAB[0x1e0].st_size + param_1));
    uVar1 = _ZN3glf22AndroidGetMillisecondsEv();
    VectorSignedToFloat(uVar1,(byte)(in_fpscr >> 0x16) & 3);
    floorf(__x);
    _ZN13CMemoryStream10WriteFloatEf(auStack_40,extraout_r0);
    uVar1 = _ZN11Application14EncryptAndSaveEPKciP13CMemoryStream
                      (param_1,DAT_003eeea8 + 0x3eee84,3,auStack_40);
    _ZN13CMemoryStreamD2Ev(auStack_40);
  }
  return uVar1;
}


