// _ZNK33CComponentBuiltinIrradianceVolume5CloneEv @ 003ceacc

void _ZNK33CComponentBuiltinIrradianceVolume5CloneEv(int param_1)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  
  piVar1 = (int *)_Znwj(0x10);
  iVar3 = DAT_003ceb08 + 0x3ceaf4;
  piVar1[1] = *(int *)(param_1 + 4);
  piVar1[2] = *(int *)(param_1 + 8);
  iVar2 = *(int *)(param_1 + 0xc);
  *piVar1 = iVar3;
  piVar1[3] = iVar2;
  return;
}


