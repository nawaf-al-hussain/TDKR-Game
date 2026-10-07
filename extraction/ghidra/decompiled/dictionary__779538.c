// _ZN6glitch7collada23CParametricController3dC2ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 00779538

int * _ZN6glitch7collada23CParametricController3dC2ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
                (int *param_1,undefined4 *param_2,undefined4 *param_3)

{
  void *__dest;
  undefined4 uVar1;
  int iVar2;
  int *piVar3;
  int *piVar4;
  int iVar5;
  uint in_fpscr;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  
  iVar2 = DAT_00779800 + 0x779550;
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
  iVar2 = DAT_00779804;
  param_1[5] = 0;
  param_1[6] = 0;
  param_1[7] = 0;
  *param_1 = iVar2 + 0x7795b8;
  param_1[8] = 0;
  param_1[9] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xc] = 0;
  param_1[0xd] = 0;
  param_1[0xe] = 0;
  piVar4 = (int *)param_2[6];
  piVar3 = (int *)_Znwj(0x6c);
  iVar2 = DAT_00779808;
  piVar3[2] = 0;
  piVar3[3] = 0;
  piVar3[4] = 0;
  iVar5 = piVar4[6];
  piVar3[5] = 0x7f7fffff;
  fVar6 = (float)VectorSignedToFloat(iVar5,(byte)(in_fpscr >> 0x16) & 3);
  piVar3[6] = 0x7f7fffff;
  piVar3[2] = iVar5;
  piVar3[7] = 0x7f7fffff;
  iVar5 = piVar4[7];
  piVar3[8] = -0x800001;
  piVar3[9] = -0x800001;
  piVar3[10] = -0x800001;
  fVar7 = (float)VectorSignedToFloat(iVar5,(byte)(in_fpscr >> 0x16) & 3);
  piVar3[3] = iVar5;
  iVar5 = piVar4[8];
  piVar3[0xb] = 0;
  piVar3[0xc] = 0;
  piVar3[0xd] = 0;
  piVar3[0xe] = 0;
  piVar3[0xf] = 0;
  piVar3[0x10] = 0;
  fVar10 = (float)piVar4[9];
  *piVar3 = iVar2 + 0x779610;
  piVar3[4] = iVar5;
  piVar3[1] = 0;
  piVar3[0x11] = 0;
  piVar3[0x12] = 0;
  piVar3[0x13] = 0;
  piVar3[0x14] = 0;
  piVar3[0x15] = 0;
  piVar3[0x16] = 0;
  piVar3[0x17] = 0;
  piVar3[0x18] = 0;
  piVar3[0x19] = 0;
  piVar3[0x1a] = 0;
  piVar3[5] = (int)fVar10;
  fVar11 = (float)piVar4[10];
  piVar3[6] = (int)fVar11;
  fVar12 = (float)piVar4[0xb];
  piVar3[7] = (int)fVar12;
  fVar8 = (float)piVar4[0xc];
  piVar3[8] = (int)fVar8;
  fVar8 = fVar8 - fVar10;
  fVar10 = (float)piVar4[0xd];
  piVar3[9] = (int)fVar10;
  fVar9 = (float)piVar4[0xe];
  iVar2 = piVar4[0xf];
  piVar3[10] = (int)fVar9;
  fVar10 = fVar10 - fVar11;
  piVar3[0xb] = (int)fVar8;
  fVar9 = fVar9 - fVar12;
  piVar3[0xc] = (int)fVar10;
  fVar11 = (float)VectorSignedToFloat(iVar5,(byte)(in_fpscr >> 0x16) & 3);
  piVar3[0xd] = (int)fVar9;
  piVar3[0xe] = (int)(fVar8 / fVar6);
  piVar3[0xf] = (int)(fVar10 / fVar7);
  piVar3[0x10] = (int)(fVar9 / fVar11);
  _ZNSt6vectorIN6glitch7collada18CBarycentricGrid3dINS1_16SAnimationVolumeEE7SVolumeENS0_4core10SAllocatorIS5_LNS0_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIPS5_EEvN9__gnu_cxx17__normal_iteratorISD_SB_EET_SH_St20forward_iterator_tag
            (piVar3 + 0x11,0,piVar4[0x10],piVar4[0x10] + iVar2 * 0x48,0);
  __dest = (void *)_Znaj(piVar4[0x11] << 3);
  iVar2 = piVar3[0x17];
  piVar3[0x17] = (int)__dest;
  if (iVar2 != 0) {
    _ZdaPv(iVar2);
    __dest = (void *)piVar3[0x17];
  }
  memcpy(__dest,(void *)piVar4[0x12],piVar4[0x11] << 3);
  _ZNSt6vectorItN6glitch4core10SAllocatorItLNS0_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIPKtEEvN9__gnu_cxx17__normal_iteratorIPtS6_EET_SE_St20forward_iterator_tag
            (piVar3 + 0x18,piVar3[0x18],piVar4[0x14],piVar4[0x14] + piVar4[0x13] * 2,0);
  _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(piVar3 + 1);
  iVar2 = param_1[0xe];
  param_1[0xe] = (int)piVar3;
  if (iVar2 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  _ZNSt6vectorIN6glitch7collada23CParametricController3d12SVolumeClipsENS0_4core10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIPS3_EEvN9__gnu_cxx17__normal_iteratorISB_S9_EET_SF_St20forward_iterator_tag
            (param_1 + 5,param_1[5],piVar4[1],piVar4[1] + *piVar4 * 0x10,0);
  _ZNSt6vectorIN6glitch4core8vector4dIfEENS1_10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIPKS3_EEvN9__gnu_cxx17__normal_iteratorIPS3_S8_EET_SG_St20forward_iterator_tag
            (param_1 + 8,param_1[8],piVar4[3],piVar4[3] + piVar4[2] * 0x10,0);
  _ZNSt6vectorIN6glitch7collada23CParametricController3d14SVolumeWeightsENS0_4core10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIPS3_EEvN9__gnu_cxx17__normal_iteratorISB_S9_EET_SF_St20forward_iterator_tag
            (param_1 + 0xb,param_1[0xb],piVar4[5],piVar4[5] + piVar4[4] * 0x10,0);
  return param_1;
}


