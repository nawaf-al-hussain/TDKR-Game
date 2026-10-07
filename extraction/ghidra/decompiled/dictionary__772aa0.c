// _ZN6glitch7collada21IParametricControllerC1ENS0_28E_PARAMETRIC_CONTROLLER_TYPEERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 00772aa0

int * _ZN6glitch7collada21IParametricControllerC1ENS0_28E_PARAMETRIC_CONTROLLER_TYPEERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
                (int *param_1,int param_2,undefined4 *param_3)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  
  iVar1 = DAT_00772b04;
  piVar3 = (int *)*param_3;
  iVar2 = *(int *)(DAT_00772b00 + 0x772ac4);
  param_1[1] = 0;
  param_1[2] = iVar2 + 0xc;
  *param_1 = iVar1 + 0x772ad4;
  param_1[3] = param_2;
  param_1[4] = (int)piVar3;
  if (piVar3 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)piVar3 + *(int *)(*piVar3 + -0xc) + 4);
  }
  return param_1;
}


