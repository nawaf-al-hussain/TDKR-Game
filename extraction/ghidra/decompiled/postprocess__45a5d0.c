// _ZN23CPostProcessEffect_HurtC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 0045a5d0

int * _ZN23CPostProcessEffect_HurtC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
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
  *param_1 = DAT_0045a6f8 + 0x45a61c;
  iVar2 = _ZN11Application11GetInstanceEv();
  _ZN6glitch5video15CTextureManager10getTextureEPKcS3_
            (&local_14,
             *(undefined4 *)
              (*(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8) + 0x14c),
             DAT_0045a6fc + 0x45a634,0);
  _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE(local_14,1);
  _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE(local_14,1);
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_14,0,2);
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_14,1,2);
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(local_14,2,2);
  iVar2 = param_1[0xd];
  uVar3 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(iVar2 + 4),DAT_0045a700 + 0x45a6a8,0);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (iVar2,uVar3,0,&local_14);
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),DAT_0045a704 + 0x45a6d0,0);
  param_1[0x13] = 0x3dcccccd;
  *(undefined2 *)(param_1 + 0x14) = uVar1;
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_14);
  return param_1;
}


