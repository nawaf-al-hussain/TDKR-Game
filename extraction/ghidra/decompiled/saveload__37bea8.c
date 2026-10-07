// _ZN11CSlowMotion8SaveLoadEP13CMemoryStream @ 0037bea8

void _ZN11CSlowMotion8SaveLoadEP13CMemoryStream(int param_1,int *param_2)

{
  int iVar1;
  int iVar2;
  
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 8);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x10);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x14);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x18);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x1c);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xc);
  iVar2 = param_2[3];
  iVar1 = *param_2;
  *(int *)(param_1 + 0x20) = (int)*(char *)(iVar1 + iVar2) << 0x18;
  param_2[3] = iVar2 + 1;
  *(uint *)(param_1 + 0x20) = *(uint *)(param_1 + 0x20) | (uint)*(byte *)(iVar1 + iVar2 + 1) << 0x10
  ;
  param_2[3] = iVar2 + 2;
  *(uint *)(param_1 + 0x20) = *(uint *)(param_1 + 0x20) | (uint)*(byte *)(iVar1 + iVar2 + 2) << 8;
  param_2[3] = iVar2 + 3;
  *(uint *)(param_1 + 0x20) = *(uint *)(param_1 + 0x20) | (uint)*(byte *)(iVar1 + iVar2 + 3);
  param_2[3] = iVar2 + 4;
  *(int *)(param_1 + 0x24) = (int)*(char *)(iVar1 + iVar2 + 4) << 0x18;
  param_2[3] = iVar2 + 5;
  *(uint *)(param_1 + 0x24) = *(uint *)(param_1 + 0x24) | (uint)*(byte *)(iVar1 + iVar2 + 5) << 0x10
  ;
  param_2[3] = iVar2 + 6;
  *(uint *)(param_1 + 0x24) = *(uint *)(param_1 + 0x24) | (uint)*(byte *)(iVar1 + iVar2 + 6) << 8;
  param_2[3] = iVar2 + 7;
  *(uint *)(param_1 + 0x24) = *(uint *)(param_1 + 0x24) | (uint)*(byte *)(iVar1 + iVar2 + 7);
  param_2[3] = iVar2 + 8;
  return;
}


