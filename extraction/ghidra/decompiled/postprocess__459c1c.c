// _ZN27CPostProcessEffect_HeatHazeC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 00459c1c

int * _ZN27CPostProcessEffect_HeatHazeC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
                (int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 uVar3;
  undefined1 auStack_18 [4];
  undefined4 local_14;
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_18);
  _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
            (param_1,auStack_18,param_3,param_4);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_18);
  iVar2 = DAT_00459e50;
  param_1[0x13] = 0;
  param_1[0x14] = 0;
  param_1[0x15] = 0;
  *param_1 = iVar2 + 0x459c74;
  param_1[0x16] = 0;
  param_1[0x17] = 0;
  param_1[0x18] = 0;
  param_1[0x19] = 0;
  param_1[0x1a] = 0;
  iVar2 = _ZN11Application11GetInstanceEv();
  _ZN6glitch5video15CTextureManager10getTextureEPKcS3_
            (&local_14,
             *(undefined4 *)
              (*(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8) + 0x14c),
             DAT_00459e54 + 0x459cac,0);
  _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE(local_14,1);
  _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE(local_14,1);
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_14,0,0);
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_14,1,0);
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_14,2,0);
  iVar2 = param_1[0xd];
  uVar3 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(iVar2 + 4),DAT_00459e58 + 0x459d20,0);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (iVar2,uVar3,0,&local_14);
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),DAT_00459e5c + 0x459d48,0);
  iVar2 = DAT_00459e60 + 0x459d68;
  param_1[0x13] = -0x42333333;
  param_1[0x14] = 0x3d4ccccd;
  *(undefined2 *)(param_1 + 0x1d) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar2,0);
  iVar2 = DAT_00459e64;
  param_1[0x15] = 0x3fb33333;
  param_1[0x16] = 0x3f99999a;
  *(undefined2 *)((int)param_1 + 0x76) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar2 + 0x459d9c,0);
  iVar2 = DAT_00459e68 + 0x459dc8;
  param_1[0x17] = 0x3dcccccd;
  param_1[0x18] = 0x3d99999a;
  *(undefined2 *)(param_1 + 0x1e) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar2,0);
  iVar2 = DAT_00459e6c;
  param_1[0x19] = 0x3fb33333;
  param_1[0x1a] = 0x3f4ccccd;
  *(undefined2 *)((int)param_1 + 0x7a) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar2 + 0x459dfc,0);
  iVar2 = DAT_00459e70;
  param_1[0x1b] = 0x3fc00000;
  *(undefined2 *)(param_1 + 0x1f) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar2 + 0x459e28,0);
  param_1[0x1c] = 0x3f800000;
  *(undefined2 *)((int)param_1 + 0x7e) = uVar1;
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_14);
  return param_1;
}


