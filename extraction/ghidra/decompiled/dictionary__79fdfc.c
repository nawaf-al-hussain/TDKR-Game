// _ZN6glitch7collada23IParametricController2dC2ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE.constprop.1462 @ 0079fdfc

int * _ZN6glitch7collada23IParametricController2dC2ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE_constprop_1462
                (int *param_1,undefined4 *param_2,undefined4 *param_3)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  int *piVar4;
  int iVar5;
  
  iVar3 = DAT_0079ff4c + 0x79fe14;
  uVar2 = *param_2;
  param_1[1] = 0;
  *param_1 = iVar3;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1119
            (param_1 + 2,uVar2);
  piVar4 = (int *)*param_3;
  iVar3 = param_2[1];
  param_1[4] = (int)piVar4;
  param_1[3] = iVar3;
  if (piVar4 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)piVar4 + *(int *)(*piVar4 + -0xc) + 4);
  }
  iVar3 = DAT_0079ff50;
  param_1[5] = 0;
  param_1[6] = 0;
  param_1[7] = 0;
  *param_1 = iVar3 + 0x79fe7c;
  param_1[8] = 0;
  param_1[9] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xc] = 0;
  param_1[0xd] = 0;
  param_1[0xe] = 0;
  iVar5 = param_2[6];
  iVar3 = _Znwj(0x58);
  _ZN6glitch7collada18CBarycentricGrid2dINS0_17SAnimationSurfaceEEC2ERKNS0_9anim_pack18SBarycentricGrid2DE
            (iVar3,iVar5 + 0x1c);
  if (iVar3 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar3 + 4);
  }
  iVar1 = param_1[0xe];
  param_1[0xe] = iVar3;
  if (iVar1 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  _ZNSt6vectorIN6glitch7collada23IParametricController2d13SSurfaceClipsENS0_4core10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIPS3_EEvN9__gnu_cxx17__normal_iteratorISB_S9_EET_SF_St20forward_iterator_tag
            (param_1 + 5,param_1[5],*(int *)(iVar5 + 8),
             *(int *)(iVar5 + 8) + *(int *)(iVar5 + 4) * 0xc,0);
  _ZNSt6vectorIN6glitch4core8vector3dIfEENS1_10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIPKS3_EEvN9__gnu_cxx17__normal_iteratorIPS3_S8_EET_SG_St20forward_iterator_tag
            (param_1 + 8,param_1[8],*(int *)(iVar5 + 0x10),
             *(int *)(iVar5 + 0x10) + *(int *)(iVar5 + 0xc) * 0xc,0);
  _ZNSt6vectorIN6glitch7collada23IParametricController2d15SSurfaceWeightsENS0_4core10SAllocatorIS3_LNS0_6memory13E_MEMORY_HINTE0EEEE15_M_range_insertIPS3_EEvN9__gnu_cxx17__normal_iteratorISB_S9_EET_SF_St20forward_iterator_tag
            (param_1 + 0xb,param_1[0xb],*(int *)(iVar5 + 0x18),
             *(int *)(iVar5 + 0x18) + *(int *)(iVar5 + 0x14) * 0xc,0);
  return param_1;
}


