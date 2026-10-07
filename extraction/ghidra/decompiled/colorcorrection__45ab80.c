// _ZN34CPostProcessEffect_ColorCorrection12ApplyTextureEv @ 0045ab80

void _ZN34CPostProcessEffect_ColorCorrection12ApplyTextureEv(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  char *__s1;
  char *__s2;
  int local_18;
  int local_14;
  
  __s1 = *(char **)(param_1 + 0x14);
  if (__s1 != (char *)0x0) {
    _Z10getHackTexPKc(&local_18,__s1);
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
      __s2 = (char *)(DAT_0045ac84 + 0x45ac68);
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
  return;
}


