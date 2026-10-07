// _ZN27CPostProcessEffect_HeatHaze5ApplyEv @ 00459e74

undefined4 _ZN27CPostProcessEffect_HeatHaze5ApplyEv(int param_1)

{
  int iVar1;
  int iVar2;
  float *pfVar3;
  float fVar4;
  
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterINS_4core8vector2dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x74),0,param_1 + 0x4c);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterINS_4core8vector2dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x76),0,param_1 + 0x54);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterINS_4core8vector2dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x78),0,param_1 + 0x5c);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterINS_4core8vector2dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x7a),0,param_1 + 100);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x7c),0,param_1 + 0x6c);
  iVar1 = *(int *)(param_1 + 0x34);
  if ((uint)*(ushort *)(param_1 + 0x7e) < (uint)*(ushort *)(*(int *)(iVar1 + 4) + 0xe)) {
    iVar2 = *(int *)(*(int *)(iVar1 + 4) + 0x20) + (uint)*(ushort *)(param_1 + 0x7e) * 0x10;
    if (iVar2 == 0) {
      return 0;
    }
    if ((*(char *)(iVar2 + 9) == '\x05') && (*(short *)(iVar2 + 0xc) != 0)) {
      fVar4 = *(float *)(param_1 + 0x70);
      pfVar3 = (float *)(iVar1 + 0x30 + *(int *)(iVar2 + 4));
      if (*pfVar3 != fVar4) {
        *(undefined4 *)(iVar1 + 0x14) = 0xffffffff;
        *(undefined4 *)(iVar1 + 0x18) = 0xffffffff;
        *(undefined4 *)(iVar1 + 0xc) = 0xffffffff;
        *(undefined4 *)(iVar1 + 0x10) = 0xffffffff;
      }
      *pfVar3 = fVar4;
      return 1;
    }
  }
  return 0;
}


