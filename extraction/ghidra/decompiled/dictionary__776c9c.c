// _ZN6glitch7collada23IParametricController2dC1ENS0_28E_PARAMETRIC_CONTROLLER_TYPEERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 00776c9c

/* WARNING: Restarted to delay deadcode elimination for space: stack */

int * _ZN6glitch7collada23IParametricController2dC1ENS0_28E_PARAMETRIC_CONTROLLER_TYPEERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
                (int *param_1,int param_2,undefined4 *param_3)

{
  undefined4 *puVar1;
  int iVar2;
  int iVar3;
  int *piVar4;
  undefined4 *puVar5;
  undefined4 local_40;
  undefined4 uStack_3c;
  undefined4 uStack_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  
  iVar3 = DAT_00776f3c;
  piVar4 = (int *)*param_3;
  iVar2 = *(int *)(DAT_00776f38 + 0x776cc4);
  param_1[1] = 0;
  param_1[2] = iVar2 + 0xc;
  *param_1 = iVar3 + 0x776cd4;
  param_1[3] = param_2;
  param_1[4] = (int)piVar4;
  if (piVar4 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)piVar4 + *(int *)(*piVar4 + -0xc) + 4);
  }
  iVar3 = DAT_00776f40;
  param_1[5] = 0;
  param_1[6] = 0;
  param_1[7] = 0;
  *param_1 = iVar3 + 0x776d18;
  param_1[8] = 0;
  param_1[9] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xc] = 0;
  param_1[0xd] = 0;
  param_1[0xe] = 0;
  piVar4 = (int *)_Znwj(0x58);
  iVar3 = DAT_00776f44 + 0x776d54;
  piVar4[1] = 0;
  piVar4[4] = 0;
  piVar4[2] = 0;
  piVar4[3] = 0;
  *piVar4 = iVar3;
  piVar4[5] = 0;
  piVar4[6] = 0;
  piVar4[7] = 0;
  piVar4[8] = 0;
  piVar4[9] = 0;
  piVar4[10] = 0;
  piVar4[0xb] = 0;
  piVar4[0xc] = 0;
  piVar4[0xd] = 0;
  piVar4[0xe] = 0;
  piVar4[0xf] = 0;
  piVar4[0x10] = 0;
  piVar4[0x11] = 0;
  piVar4[0x12] = 0;
  piVar4[0x13] = 0;
  piVar4[0x14] = 0;
  piVar4[0x15] = 0;
  _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(piVar4 + 1);
  iVar3 = param_1[0xe];
  param_1[0xe] = (int)piVar4;
  if (iVar3 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  puVar5 = (undefined4 *)param_1[9];
  puVar1 = (undefined4 *)param_1[10];
  piVar4 = param_1 + 8;
  local_30 = 0;
  local_2c = 0;
  local_34 = 0x3f800000;
  if (puVar5 == puVar1) {
    _ZNSt6vectorIN6glitch4core8vector3dIfEENS1_10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE9push_backERKS3__part_1184
              (piVar4,&local_34);
    puVar5 = (undefined4 *)param_1[9];
    puVar1 = (undefined4 *)param_1[10];
    if (puVar5 != puVar1) goto LAB_00776e20;
LAB_00776ee4:
    local_20 = 0;
    local_24 = 0x3f800000;
    local_28 = 0;
    _ZNSt6vectorIN6glitch4core8vector3dIfEENS1_10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE9push_backERKS3__part_1184
              (piVar4,&local_28);
    puVar5 = (undefined4 *)param_1[9];
    if (puVar5 == (undefined4 *)param_1[10]) {
LAB_00776f14:
      local_14 = 0x3f800000;
      local_18 = 0;
      local_1c = 0;
      _ZNSt6vectorIN6glitch4core8vector3dIfEENS1_10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE9push_backERKS3__part_1184
                (piVar4,&local_1c);
      goto LAB_00776e6c;
    }
  }
  else {
    if (puVar5 != (undefined4 *)0x0) {
      *puVar5 = 0x3f800000;
      puVar5[1] = 0;
      puVar5[2] = 0;
    }
    puVar5 = puVar5 + 3;
    param_1[9] = (int)puVar5;
    if (puVar5 == puVar1) goto LAB_00776ee4;
LAB_00776e20:
    local_20 = 0;
    local_24 = 0x3f800000;
    local_28 = 0;
    if (puVar5 != (undefined4 *)0x0) {
      *puVar5 = 0;
      puVar5[1] = 0x3f800000;
      puVar5[2] = 0;
    }
    puVar5 = puVar5 + 3;
    param_1[9] = (int)puVar5;
    if (puVar5 == puVar1) goto LAB_00776f14;
  }
  local_14 = 0x3f800000;
  local_18 = 0;
  local_1c = 0;
  if (puVar5 != (undefined4 *)0x0) {
    *puVar5 = 0;
    puVar5[1] = 0;
    puVar5[2] = 0x3f800000;
  }
  param_1[9] = (int)(puVar5 + 3);
LAB_00776e6c:
  puVar1 = (undefined4 *)param_1[0xc];
  local_40 = 0;
  uStack_3c = 1;
  uStack_38 = 2;
  if (puVar1 == (undefined4 *)param_1[0xd]) {
    _ZNSt6vectorIN6glitch7collada23IParametricController2d15SSurfaceWeightsENS0_4core10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS3_S9_EERKS3_
              (param_1 + 0xb,puVar1,&local_40);
  }
  else {
    if (puVar1 != (undefined4 *)0x0) {
      *puVar1 = 0;
      puVar1[1] = 1;
      puVar1[2] = 2;
    }
    param_1[0xc] = (int)(puVar1 + 3);
  }
  return param_1;
}


