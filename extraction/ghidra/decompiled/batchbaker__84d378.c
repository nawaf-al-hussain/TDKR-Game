// _ZNK6glitch5video6detail13shadermanager17SShaderProperties13setBatchBakerERKN5boost13intrusive_ptrINS0_11IBatchBakerEEE.constprop.807 @ 0084d378

void _ZNK6glitch5video6detail13shadermanager17SShaderProperties13setBatchBakerERKN5boost13intrusive_ptrINS0_11IBatchBakerEEE_constprop_807
               (int *param_1,int *param_2)

{
  bool bVar1;
  int *piVar2;
  int *piVar3;
  int iVar4;
  
  iVar4 = *param_2;
  if (iVar4 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar4 + 4);
  }
  piVar2 = (int *)*param_1;
  *param_1 = iVar4;
  if (piVar2 == (int *)0x0) {
    return;
  }
  piVar3 = piVar2 + 1;
  DataMemoryBarrier(0xf);
  do {
    iVar4 = *piVar3;
    bVar1 = (bool)hasExclusiveAccess(piVar3);
  } while (!bVar1);
  *piVar3 = iVar4 + -1;
  DataMemoryBarrier(0xf);
  if (iVar4 + -1 == 0) {
    (**(code **)(*piVar2 + 8))();
    (**(code **)(*piVar2 + 4))(piVar2);
    return;
  }
  return;
}


