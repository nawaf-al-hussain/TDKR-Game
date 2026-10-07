// _ZN6glitch7collada20CAnimationDictionaryD2Ev @ 0076d498

int * _ZN6glitch7collada20CAnimationDictionaryD2Ev(int *param_1,int *param_2)

{
  int iVar1;
  int iVar2;
  
  iVar2 = *param_2;
  iVar1 = param_1[9];
  *param_1 = iVar2;
  *(int *)((int)param_1 + *(int *)(iVar2 + -0xc)) = param_2[3];
  if (iVar1 != 0) {
    _Z10GlitchFreePv();
  }
  _ZN6glitch7collada16CColladaDatabaseD1Ev(param_1 + 2);
  iVar1 = param_2[1];
  *param_1 = iVar1;
  *(int *)((int)param_1 + *(int *)(iVar1 + -0xc)) = param_2[2];
  return param_1;
}


