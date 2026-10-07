// _ZN6glitch7collada23CParametricController3dC1ERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 007791d8

/* WARNING: Restarted to delay deadcode elimination for space: stack */

int * _ZN6glitch7collada23CParametricController3dC1ERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
                (int *param_1,undefined4 *param_2)

{
  int iVar1;
  int *piVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_60;
  undefined4 uStack_5c;
  undefined4 uStack_58;
  undefined4 uStack_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  
  piVar2 = (int *)*param_2;
  iVar1 = DAT_0077952c + 0x7791fc;
  param_1[2] = *(int *)(DAT_00779528 + 0x7791fc) + 0xc;
  param_1[1] = 0;
  *param_1 = iVar1;
  param_1[3] = 3;
  param_1[4] = (int)piVar2;
  if (piVar2 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)piVar2 + *(int *)(*piVar2 + -0xc) + 4);
  }
  iVar1 = DAT_00779530;
  param_1[5] = 0;
  param_1[6] = 0;
  param_1[7] = 0;
  *param_1 = iVar1 + 0x779258;
  param_1[8] = 0;
  param_1[9] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xc] = 0;
  param_1[0xd] = 0;
  param_1[0xe] = 0;
  piVar2 = (int *)_Znwj(0x6c);
  iVar1 = DAT_00779534;
  piVar2[1] = 0;
  piVar2[2] = 0;
  piVar2[5] = 0x7f7fffff;
  *piVar2 = iVar1 + 0x7792a8;
  piVar2[3] = 0;
  piVar2[6] = 0x7f7fffff;
  piVar2[4] = 0;
  piVar2[7] = 0x7f7fffff;
  piVar2[8] = -0x800001;
  piVar2[9] = -0x800001;
  piVar2[10] = -0x800001;
  piVar2[0xb] = 0;
  piVar2[0xc] = 0;
  piVar2[0xd] = 0;
  piVar2[0xe] = 0;
  piVar2[0xf] = 0;
  piVar2[0x10] = 0;
  piVar2[0x11] = 0;
  piVar2[0x12] = 0;
  piVar2[0x13] = 0;
  piVar2[0x14] = 0;
  piVar2[0x15] = 0;
  piVar2[0x16] = 0;
  piVar2[0x17] = 0;
  piVar2[0x18] = 0;
  piVar2[0x19] = 0;
  piVar2[0x1a] = 0;
  _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(piVar2 + 1);
  iVar1 = param_1[0xe];
  param_1[0xe] = (int)piVar2;
  if (iVar1 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  puVar4 = (undefined4 *)param_1[9];
  puVar3 = (undefined4 *)param_1[10];
  piVar2 = param_1 + 8;
  local_4c = 0;
  local_48 = 0;
  local_44 = 0;
  local_50 = 0x3f800000;
  if (puVar4 == puVar3) {
    _ZNSt6vectorIN6glitch4core8vector4dIfEENS1_10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS3_S8_EERKS3_
              (piVar2,puVar3,&local_50);
    puVar4 = (undefined4 *)param_1[9];
    puVar3 = (undefined4 *)param_1[10];
    if (puVar3 != puVar4) goto LAB_00779388;
LAB_00779490:
    local_34 = 0;
    local_38 = 0;
    local_3c = 0x3f800000;
    local_40 = 0;
    _ZNSt6vectorIN6glitch4core8vector4dIfEENS1_10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS3_S8_EERKS3_
              (piVar2,puVar3,&local_40);
    puVar4 = (undefined4 *)param_1[9];
    puVar3 = (undefined4 *)param_1[10];
    if (puVar4 != puVar3) goto LAB_007793c0;
LAB_007794c8:
    local_24 = 0;
    local_28 = 0x3f800000;
    local_2c = 0;
    local_30 = 0;
    _ZNSt6vectorIN6glitch4core8vector4dIfEENS1_10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS3_S8_EERKS3_
              (piVar2,puVar3,&local_30);
    puVar4 = (undefined4 *)param_1[9];
    if (puVar4 == (undefined4 *)param_1[10]) goto LAB_00779500;
  }
  else {
    if (puVar4 != (undefined4 *)0x0) {
      *puVar4 = 0x3f800000;
      puVar4[1] = 0;
      puVar4[2] = 0;
      puVar4[3] = 0;
    }
    puVar4 = puVar4 + 4;
    param_1[9] = (int)puVar4;
    if (puVar3 == puVar4) goto LAB_00779490;
LAB_00779388:
    local_34 = 0;
    local_38 = 0;
    local_3c = 0x3f800000;
    local_40 = 0;
    if (puVar4 != (undefined4 *)0x0) {
      *puVar4 = 0;
      puVar4[1] = 0x3f800000;
      puVar4[2] = 0;
      puVar4[3] = 0;
    }
    puVar4 = puVar4 + 4;
    param_1[9] = (int)puVar4;
    if (puVar4 == puVar3) goto LAB_007794c8;
LAB_007793c0:
    local_24 = 0;
    local_28 = 0x3f800000;
    local_2c = 0;
    local_30 = 0;
    if (puVar4 != (undefined4 *)0x0) {
      *puVar4 = 0;
      puVar4[1] = 0;
      puVar4[2] = 0x3f800000;
      puVar4[3] = 0;
    }
    puVar4 = puVar4 + 4;
    param_1[9] = (int)puVar4;
    if (puVar4 == puVar3) {
LAB_00779500:
      local_14 = 0x3f800000;
      local_18 = 0;
      local_1c = 0;
      local_20 = 0;
      _ZNSt6vectorIN6glitch4core8vector4dIfEENS1_10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS3_S8_EERKS3_
                (piVar2,puVar4,&local_20);
      goto LAB_00779410;
    }
  }
  local_14 = 0x3f800000;
  local_18 = 0;
  local_1c = 0;
  local_20 = 0;
  if (puVar4 != (undefined4 *)0x0) {
    *puVar4 = 0;
    puVar4[1] = 0;
    puVar4[2] = 0;
    puVar4[3] = 0x3f800000;
  }
  param_1[9] = (int)(puVar4 + 4);
LAB_00779410:
  puVar3 = (undefined4 *)param_1[0xc];
  local_60 = 0;
  uStack_5c = 1;
  uStack_58 = 2;
  uStack_54 = 3;
  if (puVar3 == (undefined4 *)param_1[0xd]) {
    _ZNSt6vectorIN6glitch7collada23CParametricController3d14SVolumeWeightsENS0_4core10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS3_S9_EERKS3_
              (param_1 + 0xb,puVar3,&local_60);
  }
  else {
    if (puVar3 != (undefined4 *)0x0) {
      *puVar3 = 0;
      puVar3[1] = 1;
      puVar3[2] = 2;
      puVar3[3] = 3;
    }
    param_1[0xc] = (int)(puVar3 + 4);
  }
  return param_1;
}


