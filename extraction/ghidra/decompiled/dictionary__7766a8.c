// _ZN6glitch7collada32CSphericalParametricController2dC1ERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEERKNS_4core8vector3dIfEESC_ @ 007766a8

int * _ZN6glitch7collada32CSphericalParametricController2dC1ERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEERKNS_4core8vector3dIfEESC_
                (int *param_1,undefined4 param_2,int *param_3,int *param_4)

{
  int iVar1;
  int iVar2;
  
  _ZN6glitch7collada23IParametricController2dC1ENS0_28E_PARAMETRIC_CONTROLLER_TYPEERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
            (param_1,2,param_2);
  iVar2 = DAT_00776774;
  param_1[0xf] = *param_3;
  iVar1 = param_3[1];
  *param_1 = iVar2 + 0x7766ec;
  param_1[0x10] = iVar1;
  iVar2 = param_3[2];
  param_1[0x12] = 0;
  param_1[0x13] = 0;
  param_1[0x11] = iVar2;
  param_1[0x14] = 0;
  param_1[0x15] = *param_4;
  param_1[0x16] = param_4[1];
  param_1[0x17] = param_4[2];
  _ZN6glitch4core8vector3dIfE9normalizeEv(param_1 + 0xf);
  _ZN6glitch4core8vector3dIfE9normalizeEv(param_1 + 0x15);
  param_1[0x12] =
       (int)((float)param_1[0x11] * (float)param_1[0x16] -
            (float)param_1[0x10] * (float)param_1[0x17]);
  param_1[0x13] =
       (int)((float)param_1[0xf] * (float)param_1[0x17] -
            (float)param_1[0x15] * (float)param_1[0x11]);
  param_1[0x14] =
       (int)((float)param_1[0x15] * (float)param_1[0x10] -
            (float)param_1[0xf] * (float)param_1[0x16]);
  _ZN6glitch4core8vector3dIfE9normalizeEv(param_1 + 0x12);
  return param_1;
}


