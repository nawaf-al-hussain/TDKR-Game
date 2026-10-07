// _ZNK6glitch5video14IShaderManager16createBatchBakerEPKNS0_7IShaderE @ 00825ee8

int * _ZNK6glitch5video14IShaderManager16createBatchBakerEPKNS0_7IShaderE
                (int *param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  
  iVar1 = _Znwj(0x18);
  _ZN6glitch5video13CGenericBakerC1EPKNS0_7IShaderE(iVar1,param_3);
  *param_1 = iVar1;
  if (iVar1 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar1 + 4);
  }
  return param_1;
}

