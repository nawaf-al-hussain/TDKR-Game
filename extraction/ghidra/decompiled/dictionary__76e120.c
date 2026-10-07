// _ZNK6glitch7collada17CAnimationPackage26getBaseAnimationDictionaryEv @ 0076e120

undefined4 *
_ZNK6glitch7collada17CAnimationPackage26getBaseAnimationDictionaryEv
          (undefined4 *param_1,int param_2)

{
  int *piVar1;
  
  piVar1 = (int *)**(undefined4 **)(param_2 + 0x28);
  *param_1 = piVar1;
  if (piVar1 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)piVar1 + *(int *)(*piVar1 + -0xc) + 4);
  }
  return param_1;
}


