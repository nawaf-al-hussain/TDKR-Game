// _ZN6glitch7collada23IParametricController1dC1ENS0_28E_PARAMETRIC_CONTROLLER_TYPEERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 0077479c

int * _ZN6glitch7collada23IParametricController1dC1ENS0_28E_PARAMETRIC_CONTROLLER_TYPEERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
                (int *param_1,int param_2,undefined4 *param_3)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  
  iVar1 = DAT_00774864;
  piVar3 = (int *)*param_3;
  iVar2 = *(int *)(DAT_00774860 + 0x7747c0);
  param_1[1] = 0;
  param_1[2] = iVar2 + 0xc;
  *param_1 = iVar1 + 0x7747d0;
  param_1[3] = param_2;
  param_1[4] = (int)piVar3;
  if (piVar3 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)piVar3 + *(int *)(*piVar3 + -0xc) + 4);
  }
  iVar1 = DAT_00774868;
  *(undefined1 *)(param_1 + 5) = 0;
  param_1[6] = 0;
  *param_1 = iVar1 + 0x774814;
  param_1[7] = 0;
  param_1[8] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xe] = 0;
  param_1[0xc] = (int)(param_1 + 10);
  param_1[0xd] = (int)(param_1 + 10);
  param_1[0xf] = 0;
  param_1[0x10] = 0;
  param_1[0x11] = 0;
  param_1[0x13] = 0;
  param_1[0x14] = 0;
  param_1[0x17] = 0;
  param_1[0x15] = (int)(param_1 + 0x13);
  param_1[0x16] = (int)(param_1 + 0x13);
  param_1[0x18] = 0;
  return param_1;
}


