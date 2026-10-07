// _ZN6glitch5video14IShaderManager20removeAllBatchBakersEv @ 00825f24

short _ZN6glitch5video14IShaderManager20removeAllBatchBakersEv(int param_1)

{
  ushort uVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  short sVar7;
  
  iVar3 = *(int *)(param_1 + 0x60);
  iVar2 = *(int *)(iVar3 + 700);
  *(undefined4 *)(iVar3 + 700) = 0;
  if (iVar2 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  iVar2 = *(int *)(iVar3 + 0x2b8);
  *(undefined4 *)(iVar3 + 0x2b8) = 0;
  if (iVar2 != 0) {
    _ZN6glitch5video21intrusive_ptr_releaseEPKNS0_9CMaterialE();
  }
  if (*(int *)(iVar3 + 0x2c0) != 0) {
    _ZN6glitch5video9CMaterial15clearParametersEv();
    iVar2 = *(int *)(iVar3 + 0x2c0);
    *(undefined4 *)(iVar3 + 0x2c0) = 0;
    if (iVar2 != 0) {
      _ZN6glitch5video21intrusive_ptr_releaseEPKNS0_9CMaterialE();
    }
  }
  iVar2 = *(int *)(iVar3 + 0x2c4);
  *(undefined4 *)(iVar3 + 0x2c4) = 0;
  if (iVar2 != 0) {
    _ZN6glitch5video21intrusive_ptr_releaseEPKNS0_9CMaterialE();
  }
  *(undefined1 *)(iVar3 + 0x2c8) = 0xff;
  iVar2 = *(int *)(param_1 + 0x10);
  iVar3 = param_1 + 8;
  sVar7 = 0;
  if (iVar2 != iVar3) {
    iVar4 = param_1 + 0x2c;
    do {
      while( true ) {
        uVar1 = *(ushort *)(iVar2 + 0x1c);
        _ZN3glf8SpinLock4LockEv(iVar4);
        iVar5 = *(int *)(*(int *)(param_1 + 0x1c) + (uint)uVar1 * 8 + 4);
        _ZN3glf8SpinLock6UnlockEv(iVar4);
        iVar5 = *(int *)(iVar5 + 0x18);
        if ((iVar5 == 0) || (*(int *)(iVar5 + 4) != 1)) break;
        uVar1 = *(ushort *)(iVar2 + 0x1c);
        _ZN3glf8SpinLock4LockEv(iVar4);
        sVar7 = sVar7 + 1;
        iVar6 = *(int *)(*(int *)(param_1 + 0x1c) + (uint)uVar1 * 8 + 4);
        _ZN3glf8SpinLock6UnlockEv(iVar4);
        iVar5 = *(int *)(iVar6 + 0x18);
        *(undefined4 *)(iVar6 + 0x18) = 0;
        if (iVar5 == 0) break;
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
        iVar2 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar2);
        if (iVar3 == iVar2) {
          return sVar7;
        }
      }
      iVar2 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar2);
    } while (iVar3 != iVar2);
  }
  return sVar7;
}


