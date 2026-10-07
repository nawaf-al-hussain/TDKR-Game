// _ZN16CMonorailManager8SaveLoadEP13CMemoryStream @ 002b613c

void _ZN16CMonorailManager8SaveLoadEP13CMemoryStream(undefined4 param_1,int *param_2)

{
  int iVar1;
  
  iVar1 = param_2[3];
  *(bool *)param_1 = *(char *)(*param_2 + iVar1) != '\0';
  param_2[3] = iVar1 + 1;
  return;
}


