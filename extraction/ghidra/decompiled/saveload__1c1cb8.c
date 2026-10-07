// _ZN15CTrafficControl8SaveLoadEP13CMemoryStream @ 001c1cb8

void _ZN15CTrafficControl8SaveLoadEP13CMemoryStream
               (int param_1,int *param_2,undefined4 param_3,undefined4 param_4)

{
  uint *puVar1;
  int iVar2;
  int iVar3;
  
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x130,param_3,param_4,param_4);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x134);
  iVar2 = *(int *)(param_1 + 0x100);
  _ZN13CMemoryStream4ReadERi(param_2,iVar2 + 0x10);
  _ZN13CMemoryStream4ReadERi(param_2,iVar2 + 0x14);
  _ZN13CMemoryStream4ReadERi(param_2,iVar2 + 0x18);
  _ZN13CMemoryStream4ReadERb(param_2,iVar2 + 0x1c);
  _ZN13CMemoryStream4ReadERf(param_2,iVar2 + 0x20);
  _ZN13CMemoryStream4ReadERf(param_2,iVar2 + 0x24);
  *(float *)(iVar2 + 0x28) = *(float *)(iVar2 + 0x20) * *(float *)(iVar2 + 0x20);
  *(float *)(iVar2 + 0x2c) = *(float *)(iVar2 + 0x24) * *(float *)(iVar2 + 0x24);
  _ZN13CMemoryStream4ReadERf(param_2,iVar2 + 0x30);
  _ZN13CMemoryStream4ReadERf(param_2,iVar2 + 0x34);
  iVar2 = *(int *)(param_1 + 0x104);
  _ZN13CMemoryStream4ReadERi(param_2,iVar2 + 0x10);
  _ZN13CMemoryStream4ReadERi(param_2,iVar2 + 0x14);
  _ZN13CMemoryStream4ReadERi(param_2,iVar2 + 0x18);
  _ZN13CMemoryStream4ReadERb(param_2,iVar2 + 0x1c);
  _ZN13CMemoryStream4ReadERf(param_2,iVar2 + 0x20);
  _ZN13CMemoryStream4ReadERf(param_2,iVar2 + 0x24);
  *(float *)(iVar2 + 0x28) = *(float *)(iVar2 + 0x20) * *(float *)(iVar2 + 0x20);
  *(float *)(iVar2 + 0x2c) = *(float *)(iVar2 + 0x24) * *(float *)(iVar2 + 0x24);
  _ZN13CMemoryStream4ReadERf(param_2,iVar2 + 0x30);
  _ZN13CMemoryStream4ReadERf(param_2,iVar2 + 0x34);
  iVar3 = *(int *)(param_1 + 0x10c);
  _ZN13CMemoryStream4ReadERi(param_2,iVar3 + 0x10);
  _ZN13CMemoryStream4ReadERb(param_2,iVar3 + 0x14);
  _ZN13CMemoryStream4ReadERf(param_2,iVar3 + 0x18);
  _ZN13CMemoryStream4ReadERf(param_2,iVar3 + 0x1c);
  iVar2 = *(int *)(param_1 + 0x110);
  *(float *)(iVar3 + 0x20) = *(float *)(iVar3 + 0x18) * *(float *)(iVar3 + 0x18);
  *(float *)(iVar3 + 0x24) = *(float *)(iVar3 + 0x1c) * *(float *)(iVar3 + 0x1c);
  _ZN13CMemoryStream4ReadERb(param_2,iVar2 + 0x2c);
  _ZN13CMemoryStream4ReadERf(param_2,iVar2 + 0x30);
  _ZN13CMemoryStream4ReadERf(param_2,iVar2 + 0x34);
  puVar1 = (uint *)(iVar2 + 0x40);
  *(float *)(iVar2 + 0x38) = *(float *)(iVar2 + 0x30) * *(float *)(iVar2 + 0x30);
  *(float *)(iVar2 + 0x3c) = *(float *)(iVar2 + 0x34) * *(float *)(iVar2 + 0x34);
  iVar3 = param_2[3];
  iVar2 = *param_2;
  *puVar1 = (int)*(char *)(iVar2 + iVar3) << 0x18;
  param_2[3] = iVar3 + 1;
  *puVar1 = *puVar1 | (uint)*(byte *)(iVar2 + iVar3 + 1) << 0x10;
  param_2[3] = iVar3 + 2;
  *puVar1 = *puVar1 | (uint)*(byte *)(iVar2 + iVar3 + 2) << 8;
  param_2[3] = iVar3 + 3;
  *puVar1 = *puVar1 | (uint)*(byte *)(iVar2 + iVar3 + 3);
  param_2[3] = iVar3 + 4;
  return;
}


