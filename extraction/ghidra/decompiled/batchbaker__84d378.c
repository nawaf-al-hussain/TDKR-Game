// _ZNK6glitch5video6detail13shadermanager17SShaderProperties13setBatchBakerERKN5boost13intrusive_ptrINS0_11IBatchBakerEEE.constprop.807 @ 0084d378

void _ZNK6glitch5video6detail13shadermanager17SShaderProperties13setBatchBakerERKN5boost13intrusive_ptrINS0_11IBatchBakerEEE_constprop_807
               (int *param_1,int *param_2)

{
  int iVar1;
  int iVar2;
  
  iVar2 = *param_2;
  if (iVar2 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar2 + 4);
  }
  iVar1 = *param_1;
  *param_1 = iVar2;
  if (iVar1 == 0) {
    return;
  }
  _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  return;
}

