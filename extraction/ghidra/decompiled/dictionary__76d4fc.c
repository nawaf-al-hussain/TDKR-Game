// _ZN6glitch7collada20CAnimationDictionaryD1Ev @ 0076d4fc

int * _ZN6glitch7collada20CAnimationDictionaryD1Ev(int *param_1)

{
  int iVar1;
  
  iVar1 = DAT_0076d55c + 0x76d548;
  *param_1 = DAT_0076d55c + 0x76d524;
  param_1[0xc] = iVar1;
  if (param_1[9] != 0) {
    _Z10GlitchFreePv();
  }
  _ZN6glitch7collada16CColladaDatabaseD1Ev(param_1 + 2);
  iVar1 = DAT_0076d564 + 0x76d554;
  *param_1 = DAT_0076d560 + 0x76d554;
  param_1[0xc] = iVar1;
  return param_1;
}


