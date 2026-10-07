// _ZNK22CCustomSkyBoxSceneNode5cloneEv @ 0046ad5c

int * _ZNK22CCustomSkyBoxSceneNode5cloneEv(int *param_1,int *param_2)

{
  *param_1 = (int)param_2;
  if (param_2 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)param_2 + *(int *)(*param_2 + -0x10) + 4);
  }
  return param_1;
}

