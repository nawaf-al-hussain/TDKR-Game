// _ZN23CPostProcessEffect_Gray7FadeOutEv @ 0045a5a0

void _ZN23CPostProcessEffect_Gray7FadeOutEv(int param_1)

{
  float fVar1;
  float fVar2;
  
  fVar1 = *(float *)(param_1 + 0x10) - *(float *)(param_1 + 0x44) / *(float *)(param_1 + 0xc);
  fVar2 = DAT_0045a5cc;
  if (DAT_0045a5cc <= fVar1) {
    fVar2 = fVar1;
  }
  *(float *)(param_1 + 0x4c) = fVar2;
  return;
}


