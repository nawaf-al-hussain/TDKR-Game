// _ZN6glitch5scene16CSkyBoxSceneNodeC1EPNS_5video12IVideoDriverERKN5boost13intrusive_ptrINS2_8ITextureEEESA_SA_SA_SA_SA_i.constprop.1157 @ 0098f248

/* WARNING: Type propagation algorithm not settling */

int * _ZN6glitch5scene16CSkyBoxSceneNodeC1EPNS_5video12IVideoDriverERKN5boost13intrusive_ptrINS2_8ITextureEEESA_SA_SA_SA_SA_i_constprop_1157
                (int *param_1,int *param_2,int *param_3,int *param_4,int *param_5,int *param_6,
                int *param_7,int *param_8,undefined4 param_9)

{
  bool bVar1;
  undefined2 uVar2;
  uint uVar3;
  int iVar4;
  undefined4 uVar5;
  undefined4 *puVar6;
  int iVar7;
  int *piVar8;
  int *piVar9;
  int iVar10;
  int *local_94;
  int local_90;
  int *local_8c;
  int *local_88;
  int *local_84;
  undefined4 local_80;
  int local_7c;
  int local_78 [15];
  undefined1 local_3c;
  undefined1 local_3b;
  int *local_38;
  int *local_34;
  int *local_30;
  int *local_2c;
  int *local_28;
  int *local_24;
  
  iVar10 = DAT_00990168;
  iVar4 = DAT_00990164;
  param_1[0x53] = 0;
  param_1[0x51] = iVar4 + 0x98f274;
  param_1[0x52] = iVar4 + 0x98f294;
  local_78[4] = 0;
  local_78[10] = 0x3f800000;
  local_78[1] = 0x3f800000;
  local_78[2] = 0x3f800000;
  local_78[3] = 0x3f800000;
  local_78[5] = 0;
  local_78[6] = 0;
  local_78[7] = 0;
  local_78[8] = 0;
  local_78[9] = 0;
  _ZN6glitch5scene10ISceneNodeC2EiRKNS_4core8vector3dIfEERKNS2_10quaternionES6_
            (param_1,iVar10 + 0x98f274,param_9,local_78 + 4,local_78 + 7,local_78 + 1);
  iVar4 = DAT_0099016c;
  iVar10 = param_2[0x52];
  param_1[0x48] = 0;
  param_1[0x52] = iVar4 + 0x98f448;
  param_1[0x51] = iVar4 + 0x98f428;
  param_1[0x45] = 0;
  param_1[0x49] = 0;
  *param_1 = iVar4 + 0x98f2fc;
  param_1[0x46] = 0;
  param_1[0x47] = 0;
  param_1[0x4a] = 0;
  param_1[0x42] = 0;
  param_1[0x4b] = 0;
  param_1[0x43] = 0;
  param_1[0x4c] = 0;
  param_1[0x44] = 0;
  param_1[0x4d] = 0;
  param_1[0x4e] = 0;
  param_1[0x4f] = 0;
  *(undefined2 *)(param_1 + 0x50) = 0xffff;
  uVar3 = _ZN6glitch5video24CMaterialRendererManager22createMaterialRendererEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
                    (iVar10,param_2,0xc,0);
  if (uVar3 < (uint)(*(int *)(iVar10 + 0x1c) - *(int *)(iVar10 + 0x18) >> 3)) {
    local_94 = (int *)(*(int *)(iVar10 + 0x18) + uVar3 * 8);
  }
  else {
    local_94 = *(int **)(DAT_00990170 + 0x98f374);
  }
  local_94 = (int *)*local_94;
  if (local_94 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDENS0_23E_SHADER_PARAMETER_TYPEEtb
                    (local_94,2,0,0);
  *(undefined2 *)(param_1 + 0x50) = uVar2;
  iVar4 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDENS0_23E_SHADER_PARAMETER_TYPEEtb
                    (local_94,6,0,0);
  local_38 = (int *)*param_7;
  if (local_38 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_38 + 1);
  }
  local_34 = (int *)*param_5;
  if (local_34 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_34 + 1);
  }
  local_30 = (int *)*param_8;
  if (local_30 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_30 + 1);
  }
  local_2c = (int *)*param_6;
  if (local_2c != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_2c + 1);
  }
  local_28 = (int *)*param_3;
  if (local_28 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_28 + 1);
  }
  local_24 = (int *)*param_4;
  if (local_24 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_24 + 1);
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (&local_7c,iVar10,param_2,0xc,0);
  local_78[0] = local_7c;
  iVar7 = local_7c;
  if (local_7c != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
    iVar7 = local_78[0];
  }
  local_78[0] = param_1[0x49];
  param_1[0x49] = iVar7;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_78);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(&local_7c);
  piVar8 = local_38;
  if (local_38 != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_38,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x49],(short)param_1[0x50],0,&local_38);
    if (iVar4 != 0xffff) {
      local_80 = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x49],iVar4,0,&local_80);
    }
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (&local_7c,iVar10,param_2,0xc,0);
  local_78[0] = local_7c;
  if (local_7c != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar7 = param_1[0x4a];
  param_1[0x4a] = local_78[0];
  local_78[0] = iVar7;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_78);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(&local_7c);
  piVar8 = local_34;
  if (local_34 != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_34,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x4a],(short)param_1[0x50],0,&local_34);
    if (iVar4 != 0xffff) {
      local_80 = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x4a],iVar4,0,&local_80);
    }
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (&local_7c,iVar10,param_2,0xc,0);
  local_78[0] = local_7c;
  if (local_7c != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar7 = param_1[0x4b];
  param_1[0x4b] = local_78[0];
  local_78[0] = iVar7;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_78);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(&local_7c);
  piVar8 = local_30;
  if (local_30 != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_30,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x4b],(short)param_1[0x50],0,&local_30);
    if (iVar4 != 0xffff) {
      local_80 = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x4b],iVar4,0,&local_80);
    }
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (&local_7c,iVar10,param_2,0xc,0);
  local_78[0] = local_7c;
  if (local_7c != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar7 = param_1[0x4c];
  param_1[0x4c] = local_78[0];
  local_78[0] = iVar7;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_78);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(&local_7c);
  piVar8 = local_2c;
  if (local_2c != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_2c,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x4c],(short)param_1[0x50],0,&local_2c);
    if (iVar4 != 0xffff) {
      local_80 = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x4c],iVar4,0,&local_80);
    }
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (&local_7c,iVar10,param_2,0xc,0);
  local_78[0] = local_7c;
  if (local_7c != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar7 = param_1[0x4d];
  param_1[0x4d] = local_78[0];
  local_78[0] = iVar7;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_78);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(&local_7c);
  piVar8 = local_28;
  if (local_28 != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_28,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x4d],(short)param_1[0x50],0,&local_28);
    if (iVar4 != 0xffff) {
      local_80 = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x4d],iVar4,0,&local_80);
    }
  }
  _ZN6glitch5video24CMaterialRendererManager22createMaterialInstanceEPNS0_12IVideoDriverENS0_15E_MATERIAL_TYPEEPNS_7collada15CColladaFactoryE
            (&local_7c,iVar10,param_2,0xc,0);
  local_78[0] = local_7c;
  if (local_7c != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  iVar10 = param_1[0x4e];
  param_1[0x4e] = local_78[0];
  local_78[0] = iVar10;
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(local_78);
  _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(&local_7c);
  piVar8 = local_24;
  if (local_24 != (int *)0x0) {
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_24,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(piVar8,2,2);
    _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (param_1[0x4e],(short)param_1[0x50],0,&local_24);
    if (iVar4 != 0xffff) {
      local_80 = 0xffffffff;
      _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE15setParameterCvtINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
                (param_1[0x4e],iVar4,0);
    }
  }
  if (local_24 != (int *)0x0) {
    piVar8 = local_24 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar4 = *piVar8 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar8);
    } while (!bVar1);
    *piVar8 = iVar4;
    DataMemoryBarrier(0xf);
    if (iVar4 == 0) {
      (**(code **)(*local_24 + 4))();
    }
    else if (iVar4 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_28 != (int *)0x0) {
    piVar8 = local_28 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar4 = *piVar8 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar8);
    } while (!bVar1);
    *piVar8 = iVar4;
    DataMemoryBarrier(0xf);
    if (iVar4 == 0) {
      (**(code **)(*local_28 + 4))();
    }
    else if (iVar4 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_2c != (int *)0x0) {
    piVar8 = local_2c + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar4 = *piVar8 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar8);
    } while (!bVar1);
    *piVar8 = iVar4;
    DataMemoryBarrier(0xf);
    if (iVar4 == 0) {
      (**(code **)(*local_2c + 4))();
    }
    else if (iVar4 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_30 != (int *)0x0) {
    piVar8 = local_30 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar4 = *piVar8 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar8);
    } while (!bVar1);
    *piVar8 = iVar4;
    DataMemoryBarrier(0xf);
    if (iVar4 == 0) {
      (**(code **)(*local_30 + 4))();
    }
    else if (iVar4 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_34 != (int *)0x0) {
    piVar8 = local_34 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar4 = *piVar8 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar8);
    } while (!bVar1);
    *piVar8 = iVar4;
    DataMemoryBarrier(0xf);
    if (iVar4 == 0) {
      (**(code **)(*local_34 + 4))();
    }
    else if (iVar4 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  if (local_38 != (int *)0x0) {
    piVar8 = local_38 + 1;
    DataMemoryBarrier(0xf);
    do {
      iVar4 = *piVar8 + -1;
      bVar1 = (bool)hasExclusiveAccess(piVar8);
    } while (!bVar1);
    *piVar8 = iVar4;
    DataMemoryBarrier(0xf);
    if (iVar4 == 0) {
      (**(code **)(*local_38 + 4))();
    }
    else if (iVar4 == 1) {
      _ZNK6glitch5video8ITexture24removeFromTextureManagerEv();
    }
  }
  _ZN6glitch5video14CVertexStreams8allocateEhj(&local_84,1,0);
  piVar8 = local_84;
  if (local_84 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_84);
  }
  piVar9 = (int *)param_1[0x48];
  param_1[0x48] = (int)piVar8;
  if (piVar9 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar4 = *piVar9;
      bVar1 = (bool)hasExclusiveAccess(piVar9);
    } while (!bVar1);
    *piVar9 = iVar4 + -1;
    DataMemoryBarrier(0xf);
    if (iVar4 + -1 == 0) {
      _ZN6glitch5video14CVertexStreamsD1Ev(piVar9);
      _Z10GlitchFreePv(piVar9);
    }
  }
  if (local_84 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar4 = *local_84;
      bVar1 = (bool)hasExclusiveAccess(local_84);
    } while (!bVar1);
    *local_84 = iVar4 + -1;
    DataMemoryBarrier(0xf);
    if (iVar4 + -1 == 0) {
      _ZN6glitch5video14CVertexStreamsD1Ev(local_84);
      _Z10GlitchFreePv(local_84);
    }
  }
  local_78[0xb] = 0;
  local_78[0xc] = 0;
  local_78[0xd] = 0;
  local_78[0xe] = 0;
  local_3c = 1;
  local_3b = 1;
  (**(code **)(*param_2 + 0x58))(&local_90,param_2,local_78 + 0xb);
  iVar4 = local_90;
  iVar10 = param_1[0x48];
  if (local_90 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_90 + 4);
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar4 + 4);
  }
  iVar7 = *(int *)(iVar10 + 0x14);
  *(int *)(iVar10 + 0x14) = iVar4;
  if (iVar7 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  *(undefined4 *)(iVar10 + 0x18) = 8;
  *(undefined2 *)(iVar10 + 0x1e) = 6;
  *(undefined2 *)(iVar10 + 0x20) = 3;
  *(undefined2 *)(iVar10 + 0x22) = 0x14;
  _ZN6glitch5video14CVertexStreams25updateHomogeneityInternalEb(iVar10,0);
  if (iVar4 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar4);
  }
  iVar4 = local_90;
  iVar10 = param_1[0x48];
  if (local_90 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_90 + 4);
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar4 + 4);
  }
  iVar7 = *(int *)(iVar10 + 0x24);
  *(int *)(iVar10 + 0x24) = iVar4;
  if (iVar7 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  *(undefined4 *)(iVar10 + 0x28) = 0;
  *(undefined2 *)(iVar10 + 0x2e) = 6;
  *(undefined2 *)(iVar10 + 0x30) = 2;
  *(undefined2 *)(iVar10 + 0x32) = 0x14;
  _ZN6glitch5video14CVertexStreams25updateHomogeneityInternalEb(iVar10);
  if (iVar4 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar4);
  }
  iVar4 = local_90;
  *(undefined4 *)(param_1[0x48] + 8) = 0x18;
  uVar5 = _Znaj(0x1e0);
  _ZN6glitch5video7IBuffer5resetEjPvb(iVar4,0x1e0,uVar5,1);
  iVar4 = local_90;
  if (local_90 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_90 + 4);
  }
  puVar6 = (undefined4 *)
           _ZNK6glitch5video7IBuffer11mapInternalEjjjj
                     (local_90,1,0,*(undefined4 *)(local_90 + 0x14),0);
  local_8c = (int *)param_1[0x48];
  if (local_8c != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE();
  }
  _ZN6glitch5video27CMaterialVertexAttributeMap8allocateERKN5boost13intrusive_ptrINS0_17CMaterialRendererEEERKNS3_IKNS0_14CVertexStreamsEEE
            (&local_88,&local_94,&local_8c);
  piVar8 = local_88;
  if (local_88 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_88);
  }
  piVar9 = (int *)param_1[0x4f];
  param_1[0x4f] = (int)piVar8;
  if (piVar9 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar10 = *piVar9;
      bVar1 = (bool)hasExclusiveAccess(piVar9);
    } while (!bVar1);
    *piVar9 = iVar10 + -1;
    DataMemoryBarrier(0xf);
    if (iVar10 + -1 == 0) {
      _ZN6glitch5video27CMaterialVertexAttributeMapD2Ev(piVar9);
      _Z10GlitchFreePv(piVar9);
    }
  }
  if (local_88 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar10 = *local_88;
      bVar1 = (bool)hasExclusiveAccess(local_88);
    } while (!bVar1);
    *local_88 = iVar10 + -1;
    DataMemoryBarrier(0xf);
    if (iVar10 + -1 == 0) {
      _ZN6glitch5video27CMaterialVertexAttributeMapD2Ev(local_88);
      _Z10GlitchFreePv(local_88);
    }
  }
  piVar8 = local_8c;
  if (local_8c != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar10 = *local_8c;
      bVar1 = (bool)hasExclusiveAccess(local_8c);
    } while (!bVar1);
    *local_8c = iVar10 + -1;
    DataMemoryBarrier(0xf);
    if (iVar10 + -1 == 0) {
      _ZN6glitch5video14CVertexStreamsD1Ev(local_8c);
      _Z10GlitchFreePv(piVar8);
    }
  }
  puVar6[5] = 0;
  puVar6[10] = 0;
  puVar6[0xb] = 0;
  puVar6[0x10] = 0;
  puVar6[0x19] = 0;
  puVar6[0x1e] = 0;
  puVar6[0x1f] = 0;
  puVar6[2] = 0xc1200000;
  puVar6[3] = 0xc1200000;
  puVar6[4] = 0xc1200000;
  puVar6[8] = 0xc1200000;
  puVar6[9] = 0xc1200000;
  puVar6[0xe] = 0xc1200000;
  puVar6[0x11] = 0xc1200000;
  puVar6[0x13] = 0xc1200000;
  puVar6[0x17] = 0xc1200000;
  puVar6[0x18] = 0xc1200000;
  puVar6[0x1c] = 0xc1200000;
  puVar6[7] = 0x41200000;
  puVar6[0xc] = 0x41200000;
  puVar6[0xd] = 0x41200000;
  puVar6[0x12] = 0x41200000;
  puVar6[0x16] = 0x41200000;
  puVar6[0x1b] = 0x41200000;
  puVar6[0x1d] = 0x41200000;
  puVar6[0x20] = 0x41200000;
  *puVar6 = 0x3f800000;
  puVar6[1] = 0x3f800000;
  puVar6[6] = 0x3f800000;
  puVar6[0xf] = 0x3f800000;
  puVar6[0x14] = 0x3f800000;
  puVar6[0x15] = 0x3f800000;
  puVar6[0x1a] = 0x3f800000;
  puVar6[0x21] = 0x41200000;
  puVar6[0x22] = 0x41200000;
  puVar6[0x23] = 0x3f800000;
  puVar6[0x24] = 0;
  puVar6[0x25] = 0x41200000;
  puVar6[0x26] = 0x41200000;
  puVar6[0x27] = 0xc1200000;
  puVar6[0x28] = 0x3f800000;
  puVar6[0x29] = 0x3f800000;
  puVar6[0x2a] = 0x41200000;
  puVar6[0x2b] = 0xc1200000;
  puVar6[0x2c] = 0x41200000;
  puVar6[0x2d] = 0;
  puVar6[0x2e] = 0x3f800000;
  puVar6[0x2f] = 0xc1200000;
  puVar6[0x30] = 0xc1200000;
  puVar6[0x31] = 0x41200000;
  puVar6[0x32] = 0;
  puVar6[0x33] = 0;
  puVar6[0x34] = 0xc1200000;
  puVar6[0x35] = 0x41200000;
  puVar6[0x36] = 0x41200000;
  puVar6[0x37] = 0x3f800000;
  puVar6[0x38] = 0;
  puVar6[0x39] = 0x41200000;
  puVar6[0x3a] = 0x41200000;
  puVar6[0x3b] = 0x41200000;
  puVar6[0x3c] = 0x3f800000;
  puVar6[0x3d] = 0x3f800000;
  puVar6[0x3e] = 0xc1200000;
  puVar6[0x3f] = 0xc1200000;
  puVar6[0x40] = 0x41200000;
  puVar6[0x41] = 0;
  puVar6[0x42] = 0x3f800000;
  puVar6[0x43] = 0xc1200000;
  puVar6[0x44] = 0xc1200000;
  puVar6[0x45] = 0xc1200000;
  puVar6[0x46] = 0;
  puVar6[0x47] = 0;
  puVar6[0x48] = 0xc1200000;
  puVar6[0x49] = 0x41200000;
  puVar6[0x4a] = 0xc1200000;
  puVar6[0x4b] = 0x3f800000;
  puVar6[0x4c] = 0;
  puVar6[0x4d] = 0xc1200000;
  puVar6[0x4e] = 0x41200000;
  puVar6[0x4f] = 0x41200000;
  puVar6[0x50] = 0x3f800000;
  puVar6[0x51] = 0x3f800000;
  puVar6[0x52] = 0x41200000;
  puVar6[0x53] = 0x41200000;
  puVar6[0x54] = 0xc1200000;
  puVar6[0x55] = 0;
  puVar6[0x56] = 0x3f800000;
  puVar6[0x57] = 0x41200000;
  puVar6[0x58] = 0x41200000;
  puVar6[0x59] = 0x41200000;
  puVar6[0x5a] = 0;
  puVar6[0x5b] = 0;
  puVar6[0x5c] = 0xc1200000;
  puVar6[0x5d] = 0x41200000;
  puVar6[0x5e] = 0x41200000;
  puVar6[0x5f] = 0x3f800000;
  puVar6[0x60] = 0;
  puVar6[0x61] = 0xc1200000;
  puVar6[0x62] = 0x41200000;
  puVar6[99] = 0xc1200000;
  puVar6[100] = 0;
  puVar6[0x65] = 0;
  puVar6[0x66] = 0x41200000;
  puVar6[0x67] = 0xc1200000;
  puVar6[0x68] = 0x41200000;
  puVar6[0x69] = 0x3f800000;
  puVar6[0x6a] = 0;
  puVar6[0x6b] = 0x41200000;
  puVar6[0x6c] = 0xc1200000;
  puVar6[0x6d] = 0xc1200000;
  puVar6[0x6e] = 0x3f800000;
  puVar6[0x6f] = 0x3f800000;
  puVar6[0x70] = 0xc1200000;
  puVar6[0x71] = 0xc1200000;
  puVar6[0x72] = 0xc1200000;
  puVar6[0x73] = 0;
  puVar6[0x74] = 0x3f800000;
  puVar6[0x75] = 0xc1200000;
  puVar6[0x76] = 0xc1200000;
  puVar6[0x77] = 0x41200000;
  if (iVar4 != 0) {
    puVar6 = (undefined4 *)0x0;
    _ZNK6glitch5video7IBuffer5unmapEv(iVar4);
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar4);
  }
  _ZN6glitch5video7IBuffer4bindEjj(local_90,1,0);
  _ZN6glitch5video14CVertexStreams12updateStatesEb(param_1[0x48],0);
  if (puVar6 != (undefined4 *)0x0) {
    _ZNK6glitch5video7IBuffer5unmapEv(0);
  }
  if (local_90 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  piVar8 = local_94;
  if (local_94 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar4 = *local_94;
      bVar1 = (bool)hasExclusiveAccess(local_94);
    } while (!bVar1);
    *local_94 = iVar4 + -1;
    DataMemoryBarrier(0xf);
    if (iVar4 + -1 == 0) {
      _ZN6glitch5video17CMaterialRendererD2Ev(local_94);
      _Z10GlitchFreePv(piVar8);
    }
  }
  return param_1;
}

