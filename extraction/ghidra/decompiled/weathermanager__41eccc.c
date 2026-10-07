// _ZN15CWeatherManager25ApplyIlluminationSettingsEv @ 0041eccc

void _ZN15CWeatherManager25ApplyIlluminationSettingsEv(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  uint in_fpscr;
  float fVar4;
  float fVar5;
  float fVar6;
  int local_4c;
  undefined4 local_48;
  float local_44;
  float local_40;
  float local_3c;
  undefined4 local_38;
  undefined4 uStack_34;
  float local_30;
  float local_2c;
  
  iVar3 = *(int *)(param_1 + 0x58);
  uVar2 = *(undefined4 *)(*(int *)(*(int *)(DAT_0041eec4 + 0x41ece0) + 0x10) + 0x154);
  iVar1 = _ZN11Application11GetInstanceEv();
  _ZN6glitch5video15CTextureManager10getTextureEPKcS3_
            (&local_4c,
             *(undefined4 *)
              (*(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8) + 0x14c),
             *(undefined4 *)(iVar3 + 0x50),0);
  if (local_4c != 0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_4c,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_4c,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_4c,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (uVar2,*(undefined2 *)(param_1 + 0x48),0,&local_4c);
  }
  local_38 = *(undefined4 *)(iVar3 + 0x40);
  uStack_34 = *(undefined4 *)(iVar3 + 0x44);
  local_30 = 1.0 / *(float *)(iVar3 + 0x48);
  local_2c = 1.0 / *(float *)(iVar3 + 0x4c);
  _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterINS_4core8vector4dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (uVar2,*(undefined2 *)(param_1 + 0x4a),0,&local_38);
  local_48 = *(undefined4 *)(param_1 + 0x74);
  _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (uVar2,*(undefined2 *)(param_1 + 0x4c),0);
  _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterIfEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSB_
            (uVar2,*(undefined2 *)(param_1 + 0x4e),0,iVar3 + 0x54);
  iVar1 = _ZN11Application11GetInstanceEv();
  iVar1 = *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
  _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
            (*(undefined4 *)(iVar1 + 0x154),*(undefined2 *)(iVar1 + 0x172),0,param_1 + 100);
  fVar5 = *(float *)(param_1 + 0x5c);
  fVar6 = *(float *)(param_1 + 0x60);
  iVar1 = _ZN11Application11GetInstanceEv();
  fVar4 = *(float *)(**(int **)(DAT_0041eec8 + 0x41ee1c) + 0x1c);
  local_44 = fVar5 * fVar4;
  fVar4 = fVar6 * fVar4 - local_44;
  iVar3 = *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
  iVar1 = (int)fVar4;
  if (iVar1 < 0) {
    iVar1 = -iVar1;
  }
  fVar5 = (float)VectorSignedToFloat(iVar1,(byte)(in_fpscr >> 0x16) & 3);
  if (DAT_0041eeb8 <= fVar5) {
    local_40 = 1.0 / fVar4;
  }
  else {
    local_40 = DAT_0041eec0;
    if (fVar4 < 0.0) {
      local_40 = DAT_0041eebc;
    }
  }
  local_3c = local_40;
  _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterINS_4core8vector3dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(iVar3 + 0x154),*(short *)(iVar3 + 0x172) + 2,0,&local_44);
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_4c);
  return;
}


