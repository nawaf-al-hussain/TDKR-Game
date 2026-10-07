// _ZN6glitch7collada31CCircularParametricController1dC1ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 0077436c

int * _ZN6glitch7collada31CCircularParametricController1dC1ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
                (int *param_1,int param_2)

{
  int iVar1;
  int *piVar2;
  
  _ZN6glitch7collada23IParametricController1dC1ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
            ();
  iVar1 = DAT_00774440;
  param_1[0x1a] = 0;
  param_1[0x1b] = 0;
  param_1[0x1c] = 0;
  param_1[0x1d] = 0;
  param_1[0x1e] = 0;
  param_1[0x1f] = 0;
  param_1[0x20] = 0;
  param_1[0x21] = 0;
  param_1[0x22] = 0;
  *param_1 = iVar1 + 0x77439c;
  piVar2 = (int *)**(undefined4 **)(param_2 + 0x18);
  param_1[0x1a] = *piVar2;
  param_1[0x1b] = piVar2[1];
  param_1[0x1c] = piVar2[2];
  param_1[0x1d] = piVar2[3];
  param_1[0x1e] = piVar2[4];
  param_1[0x1f] = piVar2[5];
  _ZN6glitch4core8vector3dIfE9normalizeEv(param_1 + 0x1a);
  _ZN6glitch4core8vector3dIfE9normalizeEv(param_1 + 0x1d);
  param_1[0x20] =
       (int)((float)param_1[0x1c] * (float)param_1[0x1e] -
            (float)param_1[0x1b] * (float)param_1[0x1f]);
  param_1[0x21] =
       (int)((float)param_1[0x1a] * (float)param_1[0x1f] -
            (float)param_1[0x1d] * (float)param_1[0x1c]);
  param_1[0x22] =
       (int)((float)param_1[0x1d] * (float)param_1[0x1b] -
            (float)param_1[0x1a] * (float)param_1[0x1e]);
  return param_1;
}


