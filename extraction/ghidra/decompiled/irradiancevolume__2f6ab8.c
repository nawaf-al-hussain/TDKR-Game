// _ZNK26CComponentIrradianceVolume3NewEv @ 002f6ab8

void _ZNK26CComponentIrradianceVolume3NewEv(void)

{
  int *piVar1;
  int iVar2;
  
  piVar1 = (int *)_Znwj(0x18);
  iVar2 = DAT_002f6af4 + 0x2f6ae0;
  piVar1[2] = 0;
  *(undefined1 *)(piVar1 + 1) = 0;
  *(undefined1 *)(piVar1 + 3) = 0;
  piVar1[4] = 0;
  piVar1[5] = 0;
  *piVar1 = iVar2;
  return;
}


