// _ZN10IComponent8SaveLoadEP13CMemoryStream @ 0020db30

void _ZN10IComponent8SaveLoadEP13CMemoryStream(int param_1,int *param_2)

{
  int iVar1;
  
  iVar1 = param_2[3];
  *(bool *)(param_1 + 0xd) = *(char *)(*param_2 + iVar1) != '\0';
  param_2[3] = iVar1 + 1;
  return;
}


