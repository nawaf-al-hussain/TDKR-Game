// _ZNK26CComponentIrradianceVolume5CloneEv @ 002f6af8

void _ZNK26CComponentIrradianceVolume5CloneEv(int param_1)

{
  undefined1 uVar1;
  undefined1 uVar2;
  int *piVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  
  piVar3 = (int *)_Znwj(0x18);
  uVar1 = *(undefined1 *)(param_1 + 4);
  iVar6 = *(int *)(param_1 + 0x10);
  uVar2 = *(undefined1 *)(param_1 + 0xc);
  iVar4 = *(int *)(param_1 + 0x14);
  iVar5 = DAT_002f6b44 + 0x2f6b30;
  piVar3[2] = *(int *)(param_1 + 8);
  *piVar3 = iVar5;
  *(undefined1 *)(piVar3 + 1) = uVar1;
  piVar3[4] = iVar6;
  *(undefined1 *)(piVar3 + 3) = uVar2;
  piVar3[5] = iVar4;
  return;
}


