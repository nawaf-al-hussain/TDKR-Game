// _ZNK6glitch10irradiance17CIrradianceVolume11getDistanceERKNS_4core8vector3dIfEE @ 007ca5cc

float _ZNK6glitch10irradiance17CIrradianceVolume11getDistanceERKNS_4core8vector3dIfEE
                (int param_1,float *param_2)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  
  fVar1 = *(float *)(param_1 + 0x18) - *param_2;
  fVar4 = *param_2 - *(float *)(param_1 + 0x24);
  fVar2 = *(float *)(param_1 + 0x1c) - param_2[1];
  fVar3 = param_2[1] - *(float *)(param_1 + 0x28);
  if (fVar4 <= fVar1) {
    fVar4 = fVar1;
  }
  if (fVar4 < DAT_007ca66c) {
    fVar4 = DAT_007ca66c;
  }
  if (fVar3 <= fVar2) {
    fVar3 = fVar2;
  }
  fVar2 = *(float *)(param_1 + 0x20) - param_2[2];
  fVar1 = param_2[2] - *(float *)(param_1 + 0x2c);
  if (fVar3 < DAT_007ca66c) {
    fVar3 = DAT_007ca66c;
  }
  if (fVar1 <= fVar2) {
    fVar1 = fVar2;
  }
  fVar2 = DAT_007ca66c;
  if (DAT_007ca66c <= fVar1) {
    fVar2 = fVar1;
  }
  return SQRT(fVar4 * fVar4 + fVar3 * fVar3 + fVar2 * fVar2);
}


