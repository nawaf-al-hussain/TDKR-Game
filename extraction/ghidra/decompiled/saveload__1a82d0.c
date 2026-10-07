// _ZN12CCallVehicle8SaveLoadEP13CMemoryStream @ 001a82d0

void _ZN12CCallVehicle8SaveLoadEP13CMemoryStream
               (int param_1,int *param_2,undefined4 param_3,undefined4 param_4)

{
  uint *puVar1;
  int iVar2;
  int iVar3;
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x2c,param_3,param_4,param_4);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x30);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x34);
  puVar1 = (uint *)(param_1 + 0x40);
  *(float *)(param_1 + 0x38) = *(float *)(param_1 + 0x30) * *(float *)(param_1 + 0x30);
  *(float *)(param_1 + 0x3c) = *(float *)(param_1 + 0x34) * *(float *)(param_1 + 0x34);
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


