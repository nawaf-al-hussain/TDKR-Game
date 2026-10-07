// _ZN29CPostProcessEffect_RadialBlur7FadeOutEv @ 0045a400

void _ZN29CPostProcessEffect_RadialBlur7FadeOutEv(int param_1)

{
  float fVar1;
  float fVar2;
  
  fVar1 = *(float *)(param_1 + 0x10) - *(float *)(param_1 + 0x44) / *(float *)(param_1 + 0xc);
  fVar2 = DAT_0045a42c;
  if (DAT_0045a42c <= fVar1) {
    fVar2 = fVar1;
  }
  *(float *)(param_1 + 0x54) = fVar2;
  return;
}


