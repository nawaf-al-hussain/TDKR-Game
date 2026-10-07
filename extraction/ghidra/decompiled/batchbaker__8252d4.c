// _ZNK6glitch5video7IShader13getBatchBakerEv @ 008252d4

int * _ZNK6glitch5video7IShader13getBatchBakerEv(int *param_1,int param_2)

{
  int iVar1;
  int *piVar2;
  uint uVar3;
  int iVar4;
  int iVar5;
  int *piVar6;
  int local_1c;
  
  piVar6 = *(int **)(*(int *)(param_2 + 0x10) + 0x144);
  uVar3 = (uint)*(ushort *)(param_2 + 0x38);
  if (uVar3 < (uint)(piVar6[8] - piVar6[7] >> 3)) {
    piVar2 = (int *)(piVar6[7] + uVar3 * 8);
  }
  else {
    piVar2 = (int *)(DAT_008253a4 + 0x82530c);
  }
  iVar5 = *piVar2;
  if (iVar5 == 0) {
    *param_1 = 0;
  }
  else {
    _ZN3glf8SpinLock4LockEv(piVar6 + 0xb);
    iVar4 = *(int *)(piVar6[7] + uVar3 * 8 + 4);
    _ZN3glf8SpinLock6UnlockEv(piVar6 + 0xb);
    iVar1 = *(int *)(iVar4 + 0x18);
    if (iVar1 == 0) {
      (**(code **)(*piVar6 + 0x20))(&local_1c,piVar6,iVar5);
      _ZNK6glitch5video6detail13shadermanager17SShaderProperties13setBatchBakerERKN5boost13intrusive_ptrINS0_11IBatchBakerEEE_constprop_807
                (iVar4 + 0x18,&local_1c);
      if (local_1c != 0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      iVar1 = *(int *)(iVar4 + 0x18);
      *param_1 = iVar1;
      if (iVar1 == 0) {
        return param_1;
      }
    }
    else {
      *param_1 = iVar1;
    }
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar1 + 4);
  }
  return param_1;
}


