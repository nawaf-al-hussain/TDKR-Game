// _ZN6glitch5scene16CSkyBoxSceneNodeC2EPNS_5video12IVideoDriverERKN5boost13intrusive_ptrINS2_8ITextureEEESA_SA_SA_SA_SA_i @ 009682b8

/* WARNING: Type propagation algorithm not settling */

int * _ZN6glitch5scene16CSkyBoxSceneNodeC2EPNS_5video12IVideoDriverERKN5boost13intrusive_ptrINS2_8ITextureEEESA_SA_SA_SA_SA_i
                (int *param_1,int *param_2,int *param_3,int *param_4,int *param_5,int *param_6,
                int *param_7,int *param_8,int *param_9,undefined4 param_10)

{
  bool bVar1;
  undefined2 uVar2;
  uint uVar3;
  undefined4 uVar4;
  undefined4 *puVar5;
  int *piVar6;
  int iVar7;
  int *piVar8;
  int iVar9;
  int iVar10;
  int *local_9c;
  int local_98;
  int local_94 [2];
  int *local_8c;
  int *local_88;
  int *local_84;
  int local_80 [15];
  undefined1 local_44;
  undefined1 local_43;
  int *local_40;
  int *local_3c;
  int *local_38;
  int *local_34;
  int *local_30;
  int *local_2c [2];
  
  local_80[1] = 0;
  local_80[10] = 0x3f800000;
  local_80[4] = 0x3f800000;
  local_80[5] = 0x3f800000;
  local_80[6] = 0x3f800000;
  local_80[2] = 0;
  local_80[3] = 0;
  local_80[7] = 0;
  local_80[8] = 0;
  local_80[9] = 0;
  _ZN6glitch5scene10ISceneNodeC2EiRKNS_4core8vector3dIfEERKNS2_10quaternionES6_
            (param_1,param_2 + 1,param_10,local_80 + 1,local_80 + 7,local_80 + 4);
  iVar10 = *param_2;
  iVar7 = param_3[0x52];
  iVar9 = *(int *)(iVar10 + -0xc);
  *param_1 = iVar10;
  iVar10 = *(int *)(iVar10 + -0x10);
  *(int *)((int)param_1 + iVar9) = param_2[4];
  *(int *)((int)param_1 + iVar10) = param_2[5];
  param_1[0x48] = 0;
  param_1[0x49] = 0;
  param_1[0x4a] = 0;
  param_1[0x4b] = 0;
  param_1[0x4c] = 0;
  param_1[0x4d] = 0;
  param_1[0x4e] = 0;
  param_1[0x4f] = 0;
  param_1[0x45] = 0;
  param_1[0x46] = 0;
  param_1[0x47] = 0;
  param_1[0x42] = 0;
  param_1[0x43] = 0;
  param_1[0x44] = 0;
  *(undefined2 *)(param_1 + 0x50) = 0xffff;
  uVar3 = _ZN6glitch5video24CMaterialRendererManager22createMaterialRendererEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
                    (iVar7,param_3,0xc,0);
  if (uVar3 < (uint)(*(int *)(iVar7 + 0x1c) - *(int *)(iVar7 + 0x18) >> 3)) {
    local_9c = (int *)(*(int *)(iVar7 + 0x18) + uVar3 * 8);
  }
  else {
    local_9c = *(int **)(DAT_009691b4 + 0x9683c0);
  }
  local_9c = (int *)*local_9c;
  if (local_9c != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDENS0_23E_SHADER_PARAMETER_TYPEEtb
                    (local_9c,2,0,0);
  *(undefined2 *)(param_1 + 0x50) = uVar2;
  iVar9 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDENS0_23E_SHADER_PARAMETER_TYPEEtb
                    (local_9c,6,0,0);
  local_40 = (int *)*param_8;
  if (local_40 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_40 + 1);
  }
  local_3c = (int *)*param_6;
  if (local_3c != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_3c + 1);
  }
  local_38 = (int *)*param_9;
  if (local_38 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_38 + 1);
  }
  local_34 = (int *)*param_7;
  if (local_34 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_34 + 1);
  }
  local_30 = (int *)*param_4;
  if (local_30 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_30 + 1);
  }
  local_2c[0] = (int *)*param_5;
  if (local_2c[0] != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_2c[0] + 1);
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (local_94,iVar7,param_3,0xc,0);
  local_80[0] = local_94[0];
  iVar10 = local_94[0];
  if (local_94[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
    iVar10 = local_80[0];
  }
  local_80[0] = param_1[0x49];
  param_1[0x49] = iVar10;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_80);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_94);
  piVar6 = local_40;
  if (local_40 != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_40,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x49],(short)param_1[0x50],0,&local_40);
    if (iVar9 != 0xffff) {
      local_94[1] = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x49],iVar9,0,local_94 + 1);
    }
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (local_94,iVar7,param_3,0xc,0);
  local_80[0] = local_94[0];
  if (local_94[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar10 = param_1[0x4a];
  param_1[0x4a] = local_80[0];
  local_80[0] = iVar10;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_80);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_94);
  piVar6 = local_3c;
  if (local_3c != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_3c,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x4a],(short)param_1[0x50],0,&local_3c);
    if (iVar9 != 0xffff) {
      local_94[1] = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x4a],iVar9,0,local_94 + 1);
    }
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (local_94,iVar7,param_3,0xc,0);
  local_80[0] = local_94[0];
  if (local_94[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar10 = param_1[0x4b];
  param_1[0x4b] = local_80[0];
  local_80[0] = iVar10;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_80);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_94);
  piVar6 = local_38;
  if (local_38 != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_38,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x4b],(short)param_1[0x50],0,&local_38);
    if (iVar9 != 0xffff) {
      local_94[1] = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x4b],iVar9,0,local_94 + 1);
    }
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (local_94,iVar7,param_3,0xc,0);
  local_80[0] = local_94[0];
  if (local_94[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar10 = param_1[0x4c];
  param_1[0x4c] = local_80[0];
  local_80[0] = iVar10;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_80);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_94);
  piVar6 = local_34;
  if (local_34 != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_34,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x4c],(short)param_1[0x50],0,&local_34);
    if (iVar9 != 0xffff) {
      local_94[1] = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x4c],iVar9,0,local_94 + 1);
    }
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (local_94,iVar7,param_3,0xc,0);
  local_80[0] = local_94[0];
  if (local_94[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar10 = param_1[0x4d];
  param_1[0x4d] = local_80[0];
  local_80[0] = iVar10;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_80);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_94);
  piVar6 = local_30;
  if (local_30 != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_30,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x4d],(short)param_1[0x50],0,&local_30);
    if (iVar9 != 0xffff) {
      local_94[1] = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x4d],iVar9,0,local_94 + 1);
    }
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (local_94,iVar7,param_3,0xc,0);
  local_80[0] = local_94[0];
  if (local_94[0] != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar7 = param_1[0x4e];
  param_1[0x4e] = local_80[0];
  local_80[0] = iVar7;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_80);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_94);
  piVar6 = local_2c[0];
  if (local_2c[0] != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_2c[0],0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar6,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x4e],(short)param_1[0x50],0,local_2c);
    if (iVar9 != 0xffff) {
      local_94[1] = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x4e],iVar9,0);
    }
  }
  if (local_2c[0] != (int *)0x0) {
    piVar6 = local_2c[0] + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar7 = *piVar6 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar6);
    } while (!bVar1);
    *piVar6 = iVar7;
    DataMemoryBarrier(0xf);
    if (iVar7 == 0) {
      (**(code **)(*local_2c[0] + 4))();
    }
    else if (iVar7 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_30 != (int *)0x0) {
    piVar6 = local_30 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar7 = *piVar6 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar6);
    } while (!bVar1);
    *piVar6 = iVar7;
    DataMemoryBarrier(0xf);
    if (iVar7 == 0) {
      (**(code **)(*local_30 + 4))();
    }
    else if (iVar7 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_34 != (int *)0x0) {
    piVar6 = local_34 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar7 = *piVar6 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar6);
    } while (!bVar1);
    *piVar6 = iVar7;
    DataMemoryBarrier(0xf);
    if (iVar7 == 0) {
      (**(code **)(*local_34 + 4))();
    }
    else if (iVar7 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_38 != (int *)0x0) {
    piVar6 = local_38 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar7 = *piVar6 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar6);
    } while (!bVar1);
    *piVar6 = iVar7;
    DataMemoryBarrier(0xf);
    if (iVar7 == 0) {
      (**(code **)(*local_38 + 4))();
    }
    else if (iVar7 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_3c != (int *)0x0) {
    piVar6 = local_3c + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar7 = *piVar6 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar6);
    } while (!bVar1);
    *piVar6 = iVar7;
    DataMemoryBarrier(0xf);
    if (iVar7 == 0) {
      (**(code **)(*local_3c + 4))();
    }
    else if (iVar7 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_40 != (int *)0x0) {
    piVar6 = local_40 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar7 = *piVar6 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar6);
    } while (!bVar1);
    *piVar6 = iVar7;
    DataMemoryBarrier(0xf);
    if (iVar7 == 0) {
      (**(code **)(*local_40 + 4))();
    }
    else if (iVar7 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  _ZN6glitch5video14CVertexStreams8allocateEhj(&local_8c,1,0);
  piVar6 = local_8c;
  if (local_8c != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_8c);
  }
  piVar8 = (int *)param_1[0x48];
  param_1[0x48] = (int)piVar6;
  if (piVar8 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar7 = *piVar8;
      bVar1 = (bool)hasExclusiveAccess(piVar8);
    } while (!bVar1);
    *piVar8 = iVar7 + -1;
    DataMemoryBarrier(0xf);
    if (iVar7 + -1 == 0) {
      _ZN6glitch5video14CVertexStreamsD1Ev(piVar8);
      _Z10GlitchFreePv(piVar8);
    }
  }
  if (local_8c != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar7 = *local_8c;
      bVar1 = (bool)hasExclusiveAccess(local_8c);
    } while (!bVar1);
    *local_8c = iVar7 + -1;
    DataMemoryBarrier(0xf);
    if (iVar7 + -1 == 0) {
      _ZN6glitch5video14CVertexStreamsD1Ev(local_8c);
      _Z10GlitchFreePv(local_8c);
    }
  }
  local_80[0xb] = 0;
  local_80[0xc] = 0;
  local_80[0xd] = 0;
  local_80[0xe] = 0;
  local_44 = 1;
  local_43 = 1;
  (**(code **)(*param_3 + 0x58))(&local_98,param_3,local_80 + 0xb);
  iVar7 = local_98;
  iVar9 = param_1[0x48];
  if (local_98 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_98 + 4);
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar7 + 4);
  }
  iVar10 = *(int *)(iVar9 + 0x14);
  *(int *)(iVar9 + 0x14) = iVar7;
  if (iVar10 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  *(undefined4 *)(iVar9 + 0x18) = 8;
  *(undefined2 *)(iVar9 + 0x1e) = 6;
  *(undefined2 *)(iVar9 + 0x20) = 3;
  *(undefined2 *)(iVar9 + 0x22) = 0x14;
  _ZN6glitch5video14CVertexStreams25updateHomogeneityInternalEb(iVar9,0);
  if (iVar7 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar7);
  }
  iVar7 = local_98;
  iVar9 = param_1[0x48];
  if (local_98 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_98 + 4);
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar7 + 4);
  }
  iVar10 = *(int *)(iVar9 + 0x24);
  *(int *)(iVar9 + 0x24) = iVar7;
  if (iVar10 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  *(undefined4 *)(iVar9 + 0x28) = 0;
  *(undefined2 *)(iVar9 + 0x2e) = 6;
  *(undefined2 *)(iVar9 + 0x30) = 2;
  *(undefined2 *)(iVar9 + 0x32) = 0x14;
  _ZN6glitch5video14CVertexStreams25updateHomogeneityInternalEb(iVar9);
  if (iVar7 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar7);
  }
  iVar7 = local_98;
  *(undefined4 *)(param_1[0x48] + 8) = 0x18;
  uVar4 = _Znaj(0x1e0);
  _ZN6glitch5video7IBuffer5resetEjPvb(iVar7,0x1e0,uVar4,1);
  iVar7 = local_98;
  if (local_98 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_98 + 4);
  }
  puVar5 = (undefined4 *)
           _ZNK6glitch5video7IBuffer11mapInternalEjjjj
                     (local_98,1,0,*(undefined4 *)(local_98 + 0x14),0);
  local_84 = (int *)param_1[0x48];
  if (local_84 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  _ZN6glitch5video27CMaterialVertexAttributeMap8allocateERKN5boost13intrusive_ptrINS0_17CMaterialRendererEEERKNS3_IKNS0_14CVertexStreamsEEE
            (&local_88,&local_9c,&local_84);
  piVar6 = local_88;
  if (local_88 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_88);
  }
  piVar8 = (int *)param_1[0x4f];
  param_1[0x4f] = (int)piVar6;
  if (piVar8 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar9 = *piVar8;
      bVar1 = (bool)hasExclusiveAccess(piVar8);
    } while (!bVar1);
    *piVar8 = iVar9 + -1;
    DataMemoryBarrier(0xf);
    if (iVar9 + -1 == 0) {
      _ZN6glitch5video27CMaterialVertexAttributeMapD2Ev(piVar8);
      _Z10GlitchFreePv(piVar8);
    }
  }
  if (local_88 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar9 = *local_88;
      bVar1 = (bool)hasExclusiveAccess(local_88);
    } while (!bVar1);
    *local_88 = iVar9 + -1;
    DataMemoryBarrier(0xf);
    if (iVar9 + -1 == 0) {
      _ZN6glitch5video27CMaterialVertexAttributeMapD2Ev(local_88);
      _Z10GlitchFreePv(local_88);
    }
  }
  piVar6 = local_84;
  if (local_84 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar9 = *local_84;
      bVar1 = (bool)hasExclusiveAccess(local_84);
    } while (!bVar1);
    *local_84 = iVar9 + -1;
    DataMemoryBarrier(0xf);
    if (iVar9 + -1 == 0) {
      _ZN6glitch5video14CVertexStreamsD1Ev(local_84);
      _Z10GlitchFreePv(piVar6);
    }
  }
  puVar5[5] = 0;
  puVar5[10] = 0;
  puVar5[0xb] = 0;
  puVar5[0x10] = 0;
  puVar5[0x19] = 0;
  puVar5[0x1e] = 0;
  puVar5[0x1f] = 0;
  puVar5[2] = 0xc1200000;
  puVar5[3] = 0xc1200000;
  puVar5[4] = 0xc1200000;
  puVar5[8] = 0xc1200000;
  puVar5[9] = 0xc1200000;
  puVar5[0xe] = 0xc1200000;
  puVar5[0x11] = 0xc1200000;
  puVar5[0x13] = 0xc1200000;
  puVar5[0x17] = 0xc1200000;
  puVar5[0x18] = 0xc1200000;
  puVar5[0x1c] = 0xc1200000;
  puVar5[7] = 0x41200000;
  puVar5[0xc] = 0x41200000;
  puVar5[0xd] = 0x41200000;
  puVar5[0x12] = 0x41200000;
  puVar5[0x16] = 0x41200000;
  puVar5[0x1b] = 0x41200000;
  puVar5[0x1d] = 0x41200000;
  puVar5[0x20] = 0x41200000;
  *puVar5 = 0x3f800000;
  puVar5[1] = 0x3f800000;
  puVar5[6] = 0x3f800000;
  puVar5[0xf] = 0x3f800000;
  puVar5[0x14] = 0x3f800000;
  puVar5[0x15] = 0x3f800000;
  puVar5[0x1a] = 0x3f800000;
  puVar5[0x21] = 0x41200000;
  puVar5[0x22] = 0x41200000;
  puVar5[0x23] = 0x3f800000;
  puVar5[0x24] = 0;
  puVar5[0x25] = 0x41200000;
  puVar5[0x26] = 0x41200000;
  puVar5[0x27] = 0xc1200000;
  puVar5[0x28] = 0x3f800000;
  puVar5[0x29] = 0x3f800000;
  puVar5[0x2a] = 0x41200000;
  puVar5[0x2b] = 0xc1200000;
  puVar5[0x2c] = 0x41200000;
  puVar5[0x2d] = 0;
  puVar5[0x2e] = 0x3f800000;
  puVar5[0x2f] = 0xc1200000;
  puVar5[0x30] = 0xc1200000;
  puVar5[0x31] = 0x41200000;
  puVar5[0x32] = 0;
  puVar5[0x33] = 0;
  puVar5[0x34] = 0xc1200000;
  puVar5[0x35] = 0x41200000;
  puVar5[0x36] = 0x41200000;
  puVar5[0x37] = 0x3f800000;
  puVar5[0x38] = 0;
  puVar5[0x39] = 0x41200000;
  puVar5[0x3a] = 0x41200000;
  puVar5[0x3b] = 0x41200000;
  puVar5[0x3c] = 0x3f800000;
  puVar5[0x3d] = 0x3f800000;
  puVar5[0x3e] = 0xc1200000;
  puVar5[0x3f] = 0xc1200000;
  puVar5[0x40] = 0x41200000;
  puVar5[0x41] = 0;
  puVar5[0x42] = 0x3f800000;
  puVar5[0x43] = 0xc1200000;
  puVar5[0x44] = 0xc1200000;
  puVar5[0x45] = 0xc1200000;
  puVar5[0x46] = 0;
  puVar5[0x47] = 0;
  puVar5[0x48] = 0xc1200000;
  puVar5[0x49] = 0x41200000;
  puVar5[0x4a] = 0xc1200000;
  puVar5[0x4b] = 0x3f800000;
  puVar5[0x4c] = 0;
  puVar5[0x4d] = 0xc1200000;
  puVar5[0x4e] = 0x41200000;
  puVar5[0x4f] = 0x41200000;
  puVar5[0x50] = 0x3f800000;
  puVar5[0x51] = 0x3f800000;
  puVar5[0x52] = 0x41200000;
  puVar5[0x53] = 0x41200000;
  puVar5[0x54] = 0xc1200000;
  puVar5[0x55] = 0;
  puVar5[0x56] = 0x3f800000;
  puVar5[0x57] = 0x41200000;
  puVar5[0x58] = 0x41200000;
  puVar5[0x59] = 0x41200000;
  puVar5[0x5a] = 0;
  puVar5[0x5b] = 0;
  puVar5[0x5c] = 0xc1200000;
  puVar5[0x5d] = 0x41200000;
  puVar5[0x5e] = 0x41200000;
  puVar5[0x5f] = 0x3f800000;
  puVar5[0x60] = 0;
  puVar5[0x61] = 0xc1200000;
  puVar5[0x62] = 0x41200000;
  puVar5[99] = 0xc1200000;
  puVar5[100] = 0;
  puVar5[0x65] = 0;
  puVar5[0x66] = 0x41200000;
  puVar5[0x67] = 0xc1200000;
  puVar5[0x68] = 0x41200000;
  puVar5[0x69] = 0x3f800000;
  puVar5[0x6a] = 0;
  puVar5[0x6b] = 0x41200000;
  puVar5[0x6c] = 0xc1200000;
  puVar5[0x6d] = 0xc1200000;
  puVar5[0x6e] = 0x3f800000;
  puVar5[0x6f] = 0x3f800000;
  puVar5[0x70] = 0xc1200000;
  puVar5[0x71] = 0xc1200000;
  puVar5[0x72] = 0xc1200000;
  puVar5[0x73] = 0;
  puVar5[0x74] = 0x3f800000;
  puVar5[0x75] = 0xc1200000;
  puVar5[0x76] = 0xc1200000;
  puVar5[0x77] = 0x41200000;
  if (iVar7 != 0) {
    puVar5 = (undefined4 *)0x0;
    _ZNK6glitch5video7IBuffer5unmapEv(iVar7);
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar7);
  }
  _ZN6glitch5video7IBuffer4bindEjj(local_98,1,0);
  _ZN6glitch5video14CVertexStreams12updateStatesEb(param_1[0x48],0);
  if (puVar5 != (undefined4 *)0x0) {
    _ZNK6glitch5video7IBuffer5unmapEv(0);
  }
  if (local_98 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  piVar6 = local_9c;
  if (local_9c != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar7 = *local_9c;
      bVar1 = (bool)hasExclusiveAccess(local_9c);
    } while (!bVar1);
    *local_9c = iVar7 + -1;
    DataMemoryBarrier(0xf);
    if (iVar7 + -1 == 0) {
      _ZN6glitch5video17CMaterialRendererD2Ev(local_9c);
      _Z10GlitchFreePv(piVar6);
    }
  }
  return param_1;
}

