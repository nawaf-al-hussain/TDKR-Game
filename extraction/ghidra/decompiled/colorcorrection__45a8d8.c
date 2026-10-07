// _ZN34CPostProcessEffect_ColorCorrectionC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 0045a8d8

int * _ZN34CPostProcessEffect_ColorCorrectionC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
                (int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  undefined1 auStack_24 [4];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_24);
  _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
            (param_1,auStack_24,param_3,param_4);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_24);
  iVar1 = DAT_0045aa20;
  iVar2 = DAT_0045aa1c;
  param_1[0x14] = 0;
  param_1[0x15] = 0;
  *param_1 = iVar2 + 0x45a92c;
  _Z10getHackTexPKc(&local_20,iVar1 + 0x45a93c);
  local_18 = local_20;
  if (local_20 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_20 + 4);
  }
  iVar2 = param_1[0x14];
  param_1[0x14] = local_18;
  local_18 = iVar2;
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_20);
  _Z10getHackTexPKc(&local_1c,DAT_0045aa24 + 0x45a988);
  local_14 = local_1c;
  if (local_1c != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_1c + 4);
  }
  iVar2 = param_1[0x15];
  param_1[0x15] = local_14;
  local_14 = iVar2;
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_1c);
  _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE(param_1[0x14],0);
  _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE(param_1[0x14],0);
  iVar2 = param_1[0x14];
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(iVar2,0,2);
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(iVar2,1,2);
  _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(iVar2,2,2);
  return param_1;
}


