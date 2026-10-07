// _ZN29CPostProcessEffect_RadialBlur6FadeInEv @ 0045a3dc

void _ZN29CPostProcessEffect_RadialBlur6FadeInEv(int param_1)

{
  float fVar1;
  float fVar2;
  
  fVar1 = *(float *)(param_1 + 0x44) / *(float *)(param_1 + 8);
  fVar2 = *(float *)(param_1 + 0x10);
  if (fVar1 <= *(float *)(param_1 + 0x10)) {
    fVar2 = fVar1;
  }
  *(float *)(param_1 + 0x54) = fVar2;
  return;
}


