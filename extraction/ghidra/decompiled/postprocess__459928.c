// _ZN24CPostProcessEffect_Blend5ApplyEN5boost13intrusive_ptrIN6glitch5video8ITextureEEES5_ff @ 00459928

void _ZN24CPostProcessEffect_Blend5ApplyEN5boost13intrusive_ptrIN6glitch5video8ITextureEEES5_ff
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5)

{
  undefined4 local_14;
  
  local_14 = param_4;
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x4a),0,param_2);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x4c),0,param_3);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x4e),0,&local_14);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x50),0,&param_5);
  *(undefined4 *)(param_1 + 0x54) = param_5;
  return;
}


