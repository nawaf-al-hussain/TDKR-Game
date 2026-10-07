// _ZN6glitch7collada20CAnimationDictionaryD0Ev @ 0076d578

int * _ZN6glitch7collada20CAnimationDictionaryD0Ev(int *param_1)

{
  int iVar1;
  
  iVar1 = DAT_0076d5e0 + 0x76d5c4;
  *param_1 = DAT_0076d5e0 + 0x76d5a0;
  param_1[0xc] = iVar1;
  if (param_1[9] != 0) {
    _Z10GlitchFreePv();
  }
  _ZN6glitch7collada16CColladaDatabaseD1Ev(param_1 + 2);
  iVar1 = DAT_0076d5e8 + 0x76d5d0;
  *param_1 = DAT_0076d5e4 + 0x76d5d0;
  param_1[0xc] = iVar1;
  _ZdlPv(param_1);
  return param_1;
}


