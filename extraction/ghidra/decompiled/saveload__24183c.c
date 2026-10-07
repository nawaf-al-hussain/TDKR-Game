// _ZN20CExhaustFanComponent8SaveLoadEP13CMemoryStream @ 0024183c

void _ZN20CExhaustFanComponent8SaveLoadEP13CMemoryStream(int param_1,int *param_2)

{
  int iVar1;
  uint *puVar2;
  int iVar3;
  
  puVar2 = (uint *)(param_1 + 0xb8);
  iVar3 = param_2[3];
  iVar1 = *param_2;
  *puVar2 = (int)*(char *)(iVar1 + iVar3) << 0x18;
  param_2[3] = iVar3 + 1;
  *puVar2 = *puVar2 | (uint)*(byte *)(iVar1 + iVar3 + 1) << 0x10;
  param_2[3] = iVar3 + 2;
  *puVar2 = *puVar2 | (uint)*(byte *)(iVar1 + iVar3 + 2) << 8;
  param_2[3] = iVar3 + 3;
  *puVar2 = *puVar2 | (uint)*(byte *)(iVar1 + iVar3 + 3);
  param_2[3] = iVar3 + 4;
  return;
}


