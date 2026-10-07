// _ZN6glitch7collada21IParametricControllerC1ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 00772b08

int * _ZN6glitch7collada21IParametricControllerC1ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
                (int *param_1,undefined4 *param_2,undefined4 *param_3)

{
  undefined4 uVar1;
  int iVar2;
  int *piVar3;
  
  iVar2 = DAT_00772b6c + 0x772b20;
  uVar1 = *param_2;
  param_1[1] = 0;
  *param_1 = iVar2;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1119
            (param_1 + 2,uVar1);
  piVar3 = (int *)*param_3;
  iVar2 = param_2[1];
  param_1[4] = (int)piVar3;
  param_1[3] = iVar2;
  if (piVar3 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)piVar3 + *(int *)(*piVar3 + -0xc) + 4);
  }
  return param_1;
}


