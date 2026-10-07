// _ZN19CPostProcessManagerC1EP17CNovaSceneManagerii @ 00455824

undefined1 *
_ZN19CPostProcessManagerC1EP17CNovaSceneManagerii
          (undefined1 *param_1,undefined4 param_2,int param_3,int param_4)

{
  char cVar1;
  undefined1 uVar2;
  undefined4 uVar3;
  int iVar4;
  int *piVar5;
  int *piVar6;
  uint uVar7;
  int iVar8;
  int local_7c;
  uint local_78;
  int local_74;
  uint local_70;
  int local_6c;
  uint local_68;
  int local_64;
  uint local_60;
  int local_5c;
  uint local_58;
  int local_54;
  int local_50;
  int local_4c;
  int local_48 [2];
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined1 local_24;
  undefined1 local_23;
  undefined1 local_22;
  
  piVar6 = *(int **)(DAT_00455d14 + 0x455844);
  *(undefined4 *)(param_1 + 4) = 0;
  iVar8 = *piVar6;
  *(undefined4 *)(param_1 + 8) = 0;
  *(undefined4 *)(param_1 + 0xc) = 0;
  iVar4 = *(int *)(iVar8 + 0x88);
  cVar1 = *(char *)(iVar8 + 9);
  *(undefined1 **)(param_1 + 0x2c) = param_1 + 0x24;
  *(undefined1 **)(param_1 + 0x30) = param_1 + 0x24;
  *(undefined4 *)(param_1 + 0x10) = 0;
  *(undefined4 *)(param_1 + 0x14) = 0;
  *(undefined4 *)(param_1 + 0x18) = 0;
  if (cVar1 == '\0') {
    uVar2 = *(undefined1 *)(iVar8 + 0x8d);
  }
  else {
    uVar2 = 1;
  }
  *(int *)(param_1 + 0x44) = (iVar4 * param_3) / 100;
  *(undefined4 *)(param_1 + 0x1c) = 0;
  param_1[0x66] = uVar2;
  *(int *)(param_1 + 0x48) = (iVar4 * param_4) / 100;
  *(undefined4 *)(param_1 + 0x24) = 0;
  *(undefined4 *)(param_1 + 0x28) = 0;
  *(undefined4 *)(param_1 + 0x34) = 0;
  *(undefined4 *)(param_1 + 0x4c) = 0;
  *(undefined4 *)(param_1 + 0x50) = 0;
  *(undefined4 *)(param_1 + 0x54) = 0;
  *(undefined4 *)(param_1 + 0x58) = 0;
  iVar4 = _ZN11Application11GetInstanceEv();
  piVar5 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar4) + 8);
  uVar7 = piVar5[0x38];
  (**(code **)(*piVar5 + 0x90))(piVar5,1,0);
  if ((*(uint *)(*piVar6 + 0x80) & 8) == 0) {
    (**(code **)(*piVar5 + 100))(&local_7c,piVar5,param_1 + 0x44,*(undefined4 *)(*piVar6 + 0x94));
    iVar4 = local_7c;
    if (local_7c != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_7c + 4);
    }
    iVar8 = *(int *)(param_1 + 0x4c);
    *(int *)(param_1 + 0x4c) = iVar4;
    if (iVar8 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (local_7c != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
  }
  else {
    local_30 = *(undefined4 *)(param_1 + 0x44);
    local_2c = *(undefined4 *)(param_1 + 0x48);
    local_38 = 0;
    local_34 = 0;
    local_24 = 0;
    local_22 = 0;
    local_40 = 1;
    local_28 = 1;
    local_3c = 0x2e;
    local_23 = 1;
    _ZN6glitch5video15CTextureManager10addTextureEPKcRKNS0_12STextureDescEb
              (local_48,piVar5[0x53],DAT_00455d18 + 0x455938,&local_40,1);
    local_50 = local_48[0];
    if (local_48[0] != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_48[0] + 4);
    }
    uVar3 = *(undefined4 *)(param_1 + 0x50);
    *(int *)(param_1 + 0x50) = local_50;
    local_50 = uVar3;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(local_48);
    _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (*(undefined4 *)(param_1 + 0x50),0);
    _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (*(undefined4 *)(param_1 + 0x50),0);
  }
  _ZN19CPostProcessManager21CreateRenderToTextureEv(param_1);
  (**(code **)(*piVar5 + 0x90))(piVar5,1,uVar7 & 1);
  _ZN19CPostProcessManager21CreateScreenRectangleEv(param_1);
  uVar3 = *(undefined4 *)(*(int *)(*(int *)(DAT_00455d1c + 0x4559f4) + 0x10) + 0x154);
  if (*(char *)(*piVar6 + 0x84) != '\0') {
    local_78 = _ZN6glitch5video31CGlobalMaterialParameterManager12addParameterEPKcNS0_23E_SHADER_PARAMETER_TYPEENS0_29E_SHADER_PARAMETER_VALUE_TYPEEjh
                         (uVar3,DAT_00455d34 + 0x455cb0,2,0xd,1,0xff);
    local_74 = *(int *)(*(int *)(*(int *)(param_1 + 0x14) + 8) + 4);
    uVar7 = local_78 & 0xffff;
    if (local_74 != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_74 + 4);
    }
    _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (uVar3,uVar7,0,&local_74);
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_74);
  }
  local_70 = _ZN6glitch5video31CGlobalMaterialParameterManager12addParameterEPKcNS0_23E_SHADER_PARAMETER_TYPEENS0_29E_SHADER_PARAMETER_VALUE_TYPEEjh
                       (uVar3,DAT_00455d20 + 0x455a1c,2,0xd,1,0xff);
  local_6c = *(int *)(**(int **)(param_1 + 0x14) + 4);
  uVar7 = local_70 & 0xffff;
  if (local_6c != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_6c + 4);
  }
  _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (uVar3,uVar7,0,&local_6c);
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_6c);
  local_68 = _ZN6glitch5video31CGlobalMaterialParameterManager12addParameterEPKcNS0_23E_SHADER_PARAMETER_TYPEENS0_29E_SHADER_PARAMETER_VALUE_TYPEEjh
                       (uVar3,DAT_00455d24 + 0x455a94,2,0xd,1,0xff);
  local_64 = *(int *)(*(int *)(*(int *)(param_1 + 0x14) + 0xc) + 4);
  uVar7 = local_68 & 0xffff;
  *(short *)(param_1 + 100) = (short)local_68;
  if (local_64 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_64 + 4);
  }
  _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (uVar3,uVar7,0,&local_64);
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_64);
  local_60 = _ZN6glitch5video31CGlobalMaterialParameterManager12addParameterEPKcNS0_23E_SHADER_PARAMETER_TYPEENS0_29E_SHADER_PARAMETER_VALUE_TYPEEjh
                       (uVar3,DAT_00455d28 + 0x455b10,2,0xd,1,0xff);
  local_5c = *(int *)(*(int *)(*(int *)(param_1 + 0x14) + 0x18) + 4);
  uVar7 = local_60 & 0xffff;
  if (local_5c != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_5c + 4);
  }
  _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (uVar3,uVar7,0,&local_5c);
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_5c);
  if ((*(uint *)(*piVar6 + 0x80) & 8) != 0) {
    local_58 = _ZN6glitch5video31CGlobalMaterialParameterManager12addParameterEPKcNS0_23E_SHADER_PARAMETER_TYPEENS0_29E_SHADER_PARAMETER_VALUE_TYPEEjh
                         (uVar3,DAT_00455d30 + 0x455c60,2,0xd,1,0xff);
    _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (uVar3,local_58 & 0xffff,0,param_1 + 0x50);
  }
  _ZN19CPostProcessManager11LoadEffectsEv(param_1);
  _ZN6glitch5video15CTextureManager10getTextureEPKcS3_
            (&local_54,piVar5[0x53],DAT_00455d2c + 0x455b9c,0);
  local_4c = local_54;
  if (local_54 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_54 + 4);
  }
  uVar3 = *(undefined4 *)(param_1 + 4);
  *(int *)(param_1 + 4) = local_4c;
  local_4c = uVar3;
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_54);
  *param_1 = 0;
  return param_1;
}


