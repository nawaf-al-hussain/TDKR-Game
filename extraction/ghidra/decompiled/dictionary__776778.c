// _ZN6glitch7collada32CSphericalParametricController2dC1ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 00776778

int * _ZN6glitch7collada32CSphericalParametricController2dC1ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
                (int *param_1,int param_2)

{
  int iVar1;
  int *piVar2;
  
  _ZN6glitch7collada23IParametricController2dC1ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
            ();
  iVar1 = DAT_00776858;
  param_1[0xf] = 0;
  param_1[0x10] = 0;
  param_1[0x15] = 0;
  param_1[0x17] = 0;
  param_1[0x11] = 0x3f800000;
  param_1[0x16] = 0x3f800000;
  param_1[0x12] = 0;
  param_1[0x13] = 0;
  param_1[0x14] = 0;
  *param_1 = iVar1 + 0x7767a8;
  piVar2 = (int *)**(undefined4 **)(param_2 + 0x18);
  param_1[0xf] = *piVar2;
  param_1[0x10] = piVar2[1];
  param_1[0x11] = piVar2[2];
  param_1[0x15] = piVar2[3];
  param_1[0x16] = piVar2[4];
  param_1[0x17] = piVar2[5];
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


