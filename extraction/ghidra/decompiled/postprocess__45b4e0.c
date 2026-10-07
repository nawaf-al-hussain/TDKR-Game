// _ZN30CPostProcessEffect_CC_HeatHaze5ApplyEv @ 0045b4e0

undefined4 _ZN30CPostProcessEffect_CC_HeatHaze5ApplyEv(int param_1)

{
  int iVar1;
  int iVar2;
  float *pfVar3;
  int iVar4;
  float fVar5;
  
  iVar4 = *(int *)(*(int *)(*(int *)(param_1 + 0x38) + 8) + 0x1c);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterINS_4core8vector2dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x4a),0,iVar4 + 0x4c);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterINS_4core8vector2dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x4c),0,iVar4 + 0x54);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterINS_4core8vector2dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x4e),0,iVar4 + 0x5c);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterINS_4core8vector2dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x50),0,iVar4 + 100);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x52),0,iVar4 + 0x6c);
  iVar1 = *(int *)(param_1 + 0x34);
  if ((uint)*(ushort *)(param_1 + 0x54) < (uint)*(ushort *)(*(int *)(iVar1 + 4) + 0xe)) {
    iVar2 = *(int *)(*(int *)(iVar1 + 4) + 0x20) + (uint)*(ushort *)(param_1 + 0x54) * 0x10;
    if (iVar2 == 0) {
      return 0;
    }
    if ((*(char *)(iVar2 + 9) == '\x05') && (*(short *)(iVar2 + 0xc) != 0)) {
      fVar5 = *(float *)(iVar4 + 0x70);
      pfVar3 = (float *)(iVar1 + 0x30 + *(int *)(iVar2 + 4));
      if (*pfVar3 != fVar5) {
        *(undefined4 *)(iVar1 + 0x14) = 0xffffffff;
        *(undefined4 *)(iVar1 + 0x18) = 0xffffffff;
        *(undefined4 *)(iVar1 + 0xc) = 0xffffffff;
        *(undefined4 *)(iVar1 + 0x10) = 0xffffffff;
      }
      *pfVar3 = fVar5;
      return 1;
    }
  }
  return 0;
}


