// _ZNK6glitch5scene16CSkyBoxSceneNode11getMaterialEj @ 0096a598

int * _ZNK6glitch5scene16CSkyBoxSceneNode11getMaterialEj(int *param_1,int param_2,int param_3)

{
  int iVar1;
  
  iVar1 = *(int *)(param_2 + param_3 * 4 + 0x124);
  *param_1 = iVar1;
  if (iVar1 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  return param_1;
}

