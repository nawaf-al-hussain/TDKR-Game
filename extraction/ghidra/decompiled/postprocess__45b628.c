// _ZN34CPostProcessEffect_CC_DepthOfField5ApplyEv @ 0045b628

void _ZN34CPostProcessEffect_CC_DepthOfField5ApplyEv(int param_1)

{
  undefined4 uVar1;
  int *piVar2;
  int iVar3;
  int *piVar4;
  undefined4 local_18;
  undefined4 local_14;
  
  piVar2 = *(int **)(*(int *)(*(int *)(param_1 + 0x38) + 8) + 0xc);
  piVar4 = (int *)(DAT_0045b728 + 0x45b64c);
  (**(code **)(*piVar2 + 0x2c))(piVar2);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x4a),0,piVar2 + 0x13);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x4c),0,piVar2 + 0x14);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x4e),0,piVar2 + 0x15);
  local_18 = (**(code **)(**(int **)(*piVar4 + 0xe4) + 0x134))();
  piVar2 = *(int **)(*piVar4 + 0xe4);
  local_14 = (**(code **)(*piVar2 + 0x138))(piVar2);
  iVar3 = *(int *)(param_1 + 0x34);
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(iVar3 + 4),DAT_0045b72c + 0x45b6d8,0);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (iVar3,uVar1,0,&local_18);
  iVar3 = *(int *)(param_1 + 0x34);
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(iVar3 + 4),DAT_0045b730 + 0x45b70c,0);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (iVar3,uVar1,0,&local_14);
  return;
}


