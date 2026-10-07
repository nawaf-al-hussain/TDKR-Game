// _ZN6glitch7collada21CSceneNodeAnimatorSet22setAnimationDictionaryERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 0077d81c

void _ZN6glitch7collada21CSceneNodeAnimatorSet22setAnimationDictionaryERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
               (int *param_1,undefined4 *param_2)

{
  undefined4 *puVar1;
  int *piVar2;
  int *piVar3;
  
  piVar3 = (int *)*param_2;
  if (piVar3 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)piVar3 + *(int *)(*piVar3 + -0xc) + 4);
  }
  piVar2 = (int *)param_1[0x14];
  param_1[0x14] = (int)piVar3;
  if (piVar2 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
              ((int)piVar2 + *(int *)(*piVar2 + -0xc));
    piVar3 = (int *)param_1[0x14];
  }
  if (piVar3 == (int *)0x0) {
    return;
  }
  if (param_1[0x15] == -1) {
    return;
  }
  puVar1 = (undefined4 *)(**(code **)(*piVar3 + 0x10))(piVar3);
  (**(code **)(*param_1 + 0xa4))(param_1,*puVar1);
  (**(code **)(*(int *)param_1[3] + 0x14))((int *)param_1[3],puVar1[1]);
  return;
}


