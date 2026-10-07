// _ZNK6glitch7collada17CAnimationPackage22getAnimationDictionaryEPKc @ 0076e158

undefined4 *
_ZNK6glitch7collada17CAnimationPackage22getAnimationDictionaryEPKc
          (undefined4 *param_1,int param_2,char *param_3)

{
  int iVar1;
  undefined4 *puVar2;
  int *piVar3;
  undefined4 *puVar4;
  
  puVar4 = *(undefined4 **)(param_2 + 0x2c);
  puVar2 = *(undefined4 **)(param_2 + 0x28);
  do {
    if (puVar4 == puVar2) {
      *param_1 = 0;
      return param_1;
    }
    piVar3 = (int *)*puVar2;
    iVar1 = strcmp((char *)piVar3[1],param_3);
    puVar2 = puVar2 + 1;
  } while (iVar1 != 0);
  iVar1 = *piVar3;
  *param_1 = piVar3;
  _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
            ((int)piVar3 + *(int *)(iVar1 + -0xc) + 4);
  return param_1;
}


