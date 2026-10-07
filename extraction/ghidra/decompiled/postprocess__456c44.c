// _ZN19CPostProcessManager21CreateScreenRectangleEv @ 00456c44

/* WARNING: Type propagation algorithm not settling */

void _ZN19CPostProcessManager21CreateScreenRectangleEv(int param_1)

{
  bool bVar1;
  int *piVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  int *piVar8;
  int *__ptr;
  int *local_34;
  int local_30 [5];
  undefined1 local_1c;
  undefined1 local_1b;
  
  iVar3 = _ZN11Application11GetInstanceEv();
  piVar8 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar3) + 8);
  _ZN6glitch5video14CVertexStreams8allocateEhj(&local_34,2,0);
  piVar2 = local_34;
  if (local_34 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_34);
  }
  __ptr = *(int **)(param_1 + 0x54);
  *(int **)(param_1 + 0x54) = piVar2;
  if (__ptr != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar3 = *__ptr;
      bVar1 = (bool)hasExclusiveAccess(__ptr);
    } while (!bVar1);
    *__ptr = iVar3 + -1;
    DataMemoryBarrier(0xf);
    if (iVar3 + -1 == 0) {
      _ZN6glitch5video14CVertexStreamsD1Ev(__ptr);
      free(__ptr);
    }
  }
  if (local_34 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar3 = *local_34;
      bVar1 = (bool)hasExclusiveAccess(local_34);
    } while (!bVar1);
    *local_34 = iVar3 + -1;
    DataMemoryBarrier(0xf);
    if (iVar3 + -1 == 0) {
      _ZN6glitch5video14CVertexStreamsD1Ev(local_34);
      free(local_34);
    }
  }
  local_30[1] = 0;
  local_30[2] = 1;
  local_30[3] = 0;
  local_30[4] = 0;
  local_1c = 1;
  local_1b = 1;
  (**(code **)(*piVar8 + 0x58))(local_30,piVar8,local_30 + 1);
  iVar3 = local_30[0];
  if (local_30[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_30[0] + 4);
  }
  iVar4 = *(int *)(param_1 + 0x58);
  *(int *)(param_1 + 0x58) = iVar3;
  if (iVar4 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  if (local_30[0] != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  iVar3 = *(int *)(param_1 + 0x58);
  iVar4 = *(int *)(param_1 + 0x54);
  if (iVar3 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar3 + 4);
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar3 + 4);
  }
  iVar5 = *(int *)(iVar4 + 0x14);
  *(int *)(iVar4 + 0x14) = iVar3;
  if (iVar5 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  *(undefined4 *)(iVar4 + 0x18) = 0;
  *(undefined2 *)(iVar4 + 0x1e) = 6;
  *(undefined2 *)(iVar4 + 0x20) = 3;
  *(undefined2 *)(iVar4 + 0x22) = 0x1c;
  _ZN6glitch5video14CVertexStreams25updateHomogeneityInternalEb(iVar4);
  if (iVar3 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar3);
  }
  iVar3 = *(int *)(param_1 + 0x58);
  iVar4 = *(int *)(param_1 + 0x54);
  if (iVar3 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar3 + 4);
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar3 + 4);
  }
  iVar5 = *(int *)(iVar4 + 0x24);
  *(int *)(iVar4 + 0x24) = iVar3;
  if (iVar5 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  *(undefined4 *)(iVar4 + 0x28) = 0xc;
  *(undefined2 *)(iVar4 + 0x2e) = 6;
  *(undefined2 *)(iVar4 + 0x30) = 2;
  *(undefined2 *)(iVar4 + 0x32) = 0x1c;
  _ZN6glitch5video14CVertexStreams25updateHomogeneityInternalEb(iVar4,0);
  if (iVar3 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar3);
  }
  iVar3 = *(int *)(param_1 + 0x58);
  iVar4 = *(int *)(param_1 + 0x54);
  if (iVar3 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar3 + 4);
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar3 + 4);
  }
  iVar5 = *(int *)(iVar4 + 0x34);
  *(int *)(iVar4 + 0x34) = iVar3;
  if (iVar5 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  *(undefined4 *)(iVar4 + 0x38) = 0x14;
  *(undefined2 *)(iVar4 + 0x3e) = 6;
  *(undefined2 *)(iVar4 + 0x40) = 2;
  *(undefined2 *)(iVar4 + 0x42) = 0x1c;
  _ZN6glitch5video14CVertexStreams25updateHomogeneityInternalEb(iVar4,0);
  if (iVar3 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar3);
  }
  iVar3 = DAT_00456f24;
  uVar7 = *(undefined4 *)(param_1 + 0x58);
  *(undefined4 *)(*(int *)(param_1 + 0x54) + 8) = 4;
  uVar6 = _Z11CustomAllocjPKci(0x70,iVar3 + 0x456ee0,0xc6);
  _ZN6glitch5video7IBuffer5resetEjPvb(uVar7,0x70,uVar6,1);
  return;
}


