// _ZN23CPostProcessEffect_Hurt6FadeInEv @ 0045a708

void _ZN23CPostProcessEffect_Hurt6FadeInEv(int param_1)

{
  float fVar1;
  float fVar2;
  
  fVar1 = *(float *)(param_1 + 0x44) / *(float *)(param_1 + 8);
  fVar2 = *(float *)(param_1 + 0x10);
  if (fVar1 <= *(float *)(param_1 + 0x10)) {
    fVar2 = fVar1;
  }
  *(float *)(param_1 + 0x4c) = fVar2;
  return;
}


