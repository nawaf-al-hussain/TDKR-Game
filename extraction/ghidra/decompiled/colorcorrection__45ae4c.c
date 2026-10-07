// _ZN34CPostProcessEffect_ColorCorrection6EnableEb @ 0045ae4c

void _ZN34CPostProcessEffect_ColorCorrection6EnableEb(int param_1,int param_2)

{
  int iVar1;
  
  if (param_2 == 0) {
    *(undefined1 *)(param_1 + 0x58) = 0;
    *(undefined4 *)(param_1 + 0x44) = 0;
    *(undefined4 *)(param_1 + 0x40) = 1;
  }
  else {
    if (((DAT_0045af04 <= *(float *)(param_1 + 4)) && (*(float *)(param_1 + 4) <= DAT_0045af08)) &&
       (*(int *)(param_1 + 0x40) != 3)) {
      iVar1 = *(int *)(param_1 + 0x54);
      if (iVar1 != 0) {
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar1 + 4);
      }
      *(int *)(param_1 + 0x50) = iVar1;
      _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
    }
    *(undefined1 *)(param_1 + 0x30) = 1;
    *(undefined1 *)(param_1 + 0x58) = 1;
    *(undefined4 *)(param_1 + 0x44) = 0;
    *(undefined4 *)(param_1 + 0x40) = 0;
  }
  return;
}


