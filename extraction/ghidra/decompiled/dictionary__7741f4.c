// _ZN6glitch7collada31CCircularParametricController1dC1ERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEERKNS_4core8vector3dIfEESC_ @ 007741f4

int * _ZN6glitch7collada31CCircularParametricController1dC1ERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEERKNS_4core8vector3dIfEESC_
                (int *param_1,int *param_2,int *param_3,int *param_4)

{
  int iVar1;
  int iVar2;
  
  param_2 = (int *)*param_2;
  iVar1 = *(int *)(DAT_00774364 + 0x774220);
  *param_1 = DAT_00774360 + 0x774220;
  param_1[1] = 0;
  param_1[2] = iVar1 + 0xc;
  param_1[3] = 0;
  param_1[4] = (int)param_2;
  if (param_2 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)param_2 + *(int *)(*param_2 + -0xc) + 4);
  }
  param_1[0x1a] = 0;
  param_1[0x1b] = 0;
  param_1[0x1c] = 0;
  param_1[0x1d] = 0;
  param_1[0x1e] = 0;
  param_1[0x1f] = 0;
  param_1[0x20] = 0;
  param_1[0x21] = 0;
  param_1[0x22] = 0;
  iVar1 = DAT_00774368;
  iVar2 = *param_3;
  *(undefined1 *)(param_1 + 5) = 0;
  param_1[0x1a] = iVar2;
  iVar2 = param_3[1];
  param_1[0xc] = (int)(param_1 + 10);
  param_1[0xd] = (int)(param_1 + 10);
  param_1[0x1b] = iVar2;
  iVar2 = param_3[2];
  param_1[6] = 0;
  param_1[0x15] = (int)(param_1 + 0x13);
  param_1[0x16] = (int)(param_1 + 0x13);
  *param_1 = iVar1 + 0x7742a0;
  param_1[7] = 0;
  param_1[8] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xe] = 0;
  param_1[0xf] = 0;
  param_1[0x10] = 0;
  param_1[0x11] = 0;
  param_1[0x13] = 0;
  param_1[0x14] = 0;
  param_1[0x17] = 0;
  param_1[0x18] = 0;
  param_1[0x1c] = iVar2;
  param_1[0x1d] = *param_4;
  param_1[0x1e] = param_4[1];
  param_1[0x1f] = param_4[2];
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


