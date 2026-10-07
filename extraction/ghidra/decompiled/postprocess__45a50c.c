// _ZN23CPostProcessEffect_Gray5ApplyEv @ 0045a50c

undefined4 _ZN23CPostProcessEffect_Gray5ApplyEv(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  float *pfVar3;
  int iVar4;
  float fVar5;
  
  if (*(int *)(param_1 + 0x5c) != 0) {
    iVar4 = *(int *)(param_1 + 0x34);
    uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                      (*(undefined4 *)(iVar4 + 4),DAT_0045a578 + 0x45a538,0);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (iVar4,uVar1,0,param_1 + 0x5c);
  }
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (*(undefined4 *)(param_1 + 0x34),*(undefined2 *)(param_1 + 0x60),0,param_1 + 0x4c);
  iVar4 = *(int *)(param_1 + 0x34);
  if ((uint)*(ushort *)(param_1 + 0x62) < (uint)*(ushort *)(*(int *)(iVar4 + 4) + 0xe)) {
    iVar2 = *(int *)(*(int *)(iVar4 + 4) + 0x20) + (uint)*(ushort *)(param_1 + 0x62) * 0x10;
    if (iVar2 == 0) {
      return 0;
    }
    if ((*(char *)(iVar2 + 9) == '\a') && (*(short *)(iVar2 + 0xc) != 0)) {
      fVar5 = *(float *)(param_1 + 0x50);
      pfVar3 = (float *)(iVar4 + 0x30 + *(int *)(iVar2 + 4));
      if ((*pfVar3 != fVar5) ||
         ((pfVar3[1] != *(float *)(param_1 + 0x54) || (pfVar3[2] != *(float *)(param_1 + 0x58))))) {
        *(undefined4 *)(iVar4 + 0x14) = 0xffffffff;
        *(undefined4 *)(iVar4 + 0x18) = 0xffffffff;
        *(undefined4 *)(iVar4 + 0xc) = 0xffffffff;
        *(undefined4 *)(iVar4 + 0x10) = 0xffffffff;
      }
      *pfVar3 = fVar5;
      pfVar3[1] = *(float *)(param_1 + 0x54);
      pfVar3[2] = *(float *)(param_1 + 0x58);
      return 1;
    }
  }
  return 0;
}


