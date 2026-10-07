// _ZNK6glitch5video7IShader16removeBatchBakerEv @ 008253a8

void _ZNK6glitch5video7IShader16removeBatchBakerEv(int param_1)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  
  iVar2 = *(int *)(*(int *)(param_1 + 0x10) + 0x144);
  uVar4 = (uint)*(ushort *)(param_1 + 0x38);
  if (uVar4 < (uint)(*(int *)(iVar2 + 0x20) - *(int *)(iVar2 + 0x1c) >> 3)) {
    piVar1 = (int *)(*(int *)(iVar2 + 0x1c) + uVar4 * 8);
  }
  else {
    piVar1 = (int *)(DAT_0082541c + 0x8253d8);
  }
  if (*piVar1 != 0) {
    _ZN3glf8SpinLock4LockEv(iVar2 + 0x2c);
    iVar3 = *(int *)(*(int *)(iVar2 + 0x1c) + uVar4 * 8 + 4);
    _ZN3glf8SpinLock6UnlockEv(iVar2 + 0x2c);
    iVar2 = *(int *)(iVar3 + 0x18);
    *(undefined4 *)(iVar3 + 0x18) = 0;
    if (iVar2 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      return;
    }
    return;
  }
  return;
}

