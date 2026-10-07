// _ZN11Application19SafePopRenderTargetEv @ 003f6114

int * _ZN11Application19SafePopRenderTargetEv(int *param_1)

{
  int iVar1;
  int iVar2;
  int local_14 [2];
  
  *param_1 = 0;
  iVar1 = _ZN11Application11GetInstanceEv();
  (**(code **)(**(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8) + 0x74))(local_14)
  ;
  iVar1 = local_14[0];
  if (local_14[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_14[0] + 4);
  }
  iVar2 = *param_1;
  *param_1 = iVar1;
  if (iVar2 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  if (local_14[0] != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  return param_1;
}


