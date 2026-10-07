// _ZN34CPostProcessEffect_ColorCorrection7FadeOutEv @ 0045ab50

void _ZN34CPostProcessEffect_ColorCorrection7FadeOutEv(int param_1)

{
  float fVar1;
  float fVar2;
  
  fVar1 = *(float *)(param_1 + 0x10) - *(float *)(param_1 + 0x44) / *(float *)(param_1 + 0xc);
  fVar2 = DAT_0045ab7c;
  if (DAT_0045ab7c <= fVar1) {
    fVar2 = fVar1;
  }
  *(float *)(param_1 + 0x4c) = fVar2;
  return;
}


