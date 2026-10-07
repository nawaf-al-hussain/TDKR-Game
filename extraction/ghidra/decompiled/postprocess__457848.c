// _ZN19CPostProcessManager20EndRenderReflectionsEv @ 00457848

void _ZN19CPostProcessManager20EndRenderReflectionsEv(undefined1 *param_1)

{
  int iVar1;
  int iVar2;
  int local_14;
  
  iVar2 = *(int *)(*(int *)(param_1 + 0x14) + 8);
  _ZN11Application11GetInstanceEv();
  iVar1 = _ZN11Application11GetInstanceEv();
  (**(code **)(**(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8) + 0x74))
            (&local_14);
  iVar1 = local_14;
  if (local_14 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_14 + 4);
    if (local_14 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (iVar1 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar1);
    }
  }
  *(undefined1 *)(iVar2 + 0x20) = 0;
  _ZN6CLevel8GetLevelEv();
  *param_1 = 1;
  return;
}


