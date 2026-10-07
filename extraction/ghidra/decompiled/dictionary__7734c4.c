// _ZN6glitch7collada21IParametricController22setAnimationDictionaryERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 007734c4

void _ZN6glitch7collada21IParametricController22setAnimationDictionaryERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
               (int param_1,undefined4 *param_2)

{
  bool bVar1;
  int iVar2;
  int *piVar3;
  int *piVar4;
  
  piVar4 = (int *)*param_2;
  if (piVar4 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)piVar4 + *(int *)(*piVar4 + -0xc) + 4);
  }
  piVar3 = *(int **)(param_1 + 0x10);
  *(int **)(param_1 + 0x10) = piVar4;
  if (piVar3 == (int *)0x0) {
    return;
  }
  piVar3 = (int *)((int)piVar3 + *(int *)(*piVar3 + -0xc));
  piVar4 = piVar3 + 1;
  DataMemoryBarrier(0xf);
  do {
    iVar2 = *piVar4;
    bVar1 = (bool)hasExclusiveAccess(piVar4);
  } while (!bVar1);
  *piVar4 = iVar2 + -1;
  DataMemoryBarrier(0xf);
  if (iVar2 + -1 == 0) {
    (**(code **)(*piVar3 + 8))();
    (**(code **)(*piVar3 + 4))(piVar3);
    return;
  }
  return;
}


