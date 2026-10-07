// _ZN19CCinematicComponent8SaveLoadEP13CMemoryStream @ 002a5d28

void _ZN19CCinematicComponent8SaveLoadEP13CMemoryStream
               (int param_1,int *param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd,param_3,param_4,param_4);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x3c);
  iVar1 = param_2[3];
  *(bool *)(param_1 + 0x40) = *(char *)(*param_2 + iVar1) != '\0';
  param_2[3] = iVar1 + 1;
  return;
}


