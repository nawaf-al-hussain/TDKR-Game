// _ZN18CPostProcessEffect10PostRenderEi @ 004552e8

void _ZN18CPostProcessEffect10PostRenderEi(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int local_14 [2];
  
  iVar2 = *(int *)(*(int *)(param_1 + 0x38) + 0x14);
  if (((param_2 < *(int *)(*(int *)(param_1 + 0x38) + 0x18) - iVar2 >> 2) && (-1 < param_2)) &&
     (iVar2 = *(int *)(iVar2 + param_2 * 4), iVar2 != 0)) {
    _ZN11Application11GetInstanceEv();
    iVar1 = _ZN11Application11GetInstanceEv();
    (**(code **)(**(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8) + 0x74))
              (local_14);
    iVar1 = local_14[0];
    if (local_14[0] != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_14[0] + 4);
      if (local_14[0] != 0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      if (iVar1 != 0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar1);
      }
    }
    *(undefined1 *)(iVar2 + 0x20) = 0;
  }
  return;
}


