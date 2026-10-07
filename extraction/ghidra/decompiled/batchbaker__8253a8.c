// _ZNK6glitch5video7IShader16removeBatchBakerEv @ 008253a8

void _ZNK6glitch5video7IShader16removeBatchBakerEv(int param_1)

{
  bool bVar1;
  int *piVar2;
  int *piVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  
  iVar4 = *(int *)(*(int *)(param_1 + 0x10) + 0x144);
  uVar6 = (uint)*(ushort *)(param_1 + 0x38);
  if (uVar6 < (uint)(*(int *)(iVar4 + 0x20) - *(int *)(iVar4 + 0x1c) >> 3)) {
    piVar3 = (int *)(*(int *)(iVar4 + 0x1c) + uVar6 * 8);
  }
  else {
    piVar3 = (int *)(DAT_0082541c + 0x8253d8);
  }
  if (*piVar3 == 0) {
    return;
  }
  _ZN3glf8SpinLock4LockEv(iVar4 + 0x2c);
  iVar5 = *(int *)(*(int *)(iVar4 + 0x1c) + uVar6 * 8 + 4);
  _ZN3glf8SpinLock6UnlockEv(iVar4 + 0x2c);
  piVar3 = *(int **)(iVar5 + 0x18);
  *(undefined4 *)(iVar5 + 0x18) = 0;
  if (piVar3 == (int *)0x0) {
    return;
  }
  piVar2 = piVar3 + 1;
  DataMemoryBarrier(0xf);
  do {
    iVar4 = *piVar2;
    bVar1 = (bool)hasExclusiveAccess(piVar2);
  } while (!bVar1);
  *piVar2 = iVar4 + -1;
  DataMemoryBarrier(0xf);
  if (iVar4 + -1 == 0) {
    (**(code **)(*piVar3 + 8))();
    (**(code **)(*piVar3 + 4))(piVar3);
    return;
  }
  return;
}


