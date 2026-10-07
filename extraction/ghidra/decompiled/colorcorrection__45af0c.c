// _ZN34CPostProcessEffect_ColorCorrection4LoadEP13CMemoryStream @ 0045af0c

void _ZN34CPostProcessEffect_ColorCorrection4LoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  char *__s1;
  int iVar1;
  undefined4 uVar2;
  char *__s2;
  char *local_30;
  char *local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  
  iVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(bool *)(param_1 + 0x30) = iVar1 != 0;
  uVar2 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + 0x40) = uVar2;
  uVar2 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  local_30 = (char *)(*(int *)(DAT_0045b1b0 + 0x45af54) + 0xc);
  *(undefined4 *)(param_1 + 0x44) = uVar2;
  local_2c = local_30;
  _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,&local_30);
  _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,&local_2c);
  iVar1 = _ZN11Application11GetInstanceEv();
  _ZN6glitch5video15CTextureManager10getTextureEPKcS3_
            (&local_28,
             *(undefined4 *)
              (*(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8) + 0x14c),local_30,0)
  ;
  local_20 = local_28;
  if (local_28 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_28 + 4);
  }
  uVar2 = *(undefined4 *)(param_1 + 0x50);
  *(int *)(param_1 + 0x50) = local_20;
  local_20 = uVar2;
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_28);
  iVar1 = _ZN11Application11GetInstanceEv();
  _ZN6glitch5video15CTextureManager10getTextureEPKcS3_
            (&local_24,
             *(undefined4 *)
              (*(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8) + 0x14c),local_2c,0)
  ;
  local_1c = local_24;
  if (local_24 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_24 + 4);
  }
  uVar2 = *(undefined4 *)(param_1 + 0x54);
  *(int *)(param_1 + 0x54) = local_1c;
  local_1c = uVar2;
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_24);
  if (*(int *)(param_1 + 0x50) != 0) {
    _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE(*(int *)(param_1 + 0x50),0)
    ;
    _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE
              (*(undefined4 *)(param_1 + 0x50),0);
    uVar2 = *(undefined4 *)(param_1 + 0x50);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(uVar2,0,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(uVar2,1,2);
    _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(uVar2,2,2);
    _ZN6glitch5video8ITexture13setAnisotropyEf(*(undefined4 *)(param_1 + 0x50),0);
  }
  __s1 = local_2c;
  if ((*(int *)(param_1 + 0x54) != 0) && (local_2c != (char *)0x0)) {
    _Z10getHackTexPKc(&local_18,local_2c);
    local_14 = local_18;
    if (local_18 != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_18 + 4);
    }
    uVar2 = *(undefined4 *)(param_1 + 0x54);
    *(int *)(param_1 + 0x54) = local_14;
    local_14 = uVar2;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_18);
    if (*(int *)(param_1 + 0x54) == 0) {
      __s2 = (char *)(DAT_0045b1b4 + 0x45b194);
      iVar1 = strcasecmp(__s1,__s2);
      if (iVar1 != 0) {
        _ZN34CPostProcessEffect_ColorCorrection11InitTextureEPKc(param_1,__s2);
      }
    }
    else {
      _ZN6glitch5video8ITexture12setMinFilterENS0_21E_TEXTURE_FILTER_TYPEE
                (*(int *)(param_1 + 0x54),0);
      _ZN6glitch5video8ITexture12setMagFilterENS0_21E_TEXTURE_FILTER_TYPEE
                (*(undefined4 *)(param_1 + 0x54),0);
      uVar2 = *(undefined4 *)(param_1 + 0x54);
      _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(uVar2,0,2);
      _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(uVar2,1,2);
      _ZN6glitch5video8ITexture7setWrapENS0_15E_TEXTURE_COORDENS0_15E_TEXTURE_CLAMPE(uVar2,2,2);
      _ZN6glitch5video8ITexture13setAnisotropyEf(*(undefined4 *)(param_1 + 0x54),0);
      *(undefined4 *)(param_1 + 0x44) = 0;
      *(undefined4 *)(param_1 + 0x40) = 0;
    }
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_2c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_30);
  return;
}


