// _ZNK6glitch10irradiance17CIrradianceVolume8getPointEiiii @ 007ca51c

int _ZNK6glitch10irradiance17CIrradianceVolume8getPointEiiii
              (int *param_1,uint param_2,uint param_3,uint param_4,int param_5)

{
  int iVar1;
  int iVar2;
  
  iVar2 = param_1[0xe];
  param_2 = param_2 & ~((int)param_2 >> 0x1f);
  iVar1 = param_1[0xf];
  param_3 = param_3 & ~((int)param_3 >> 0x1f);
  param_4 = param_4 & ~((int)param_4 >> 0x1f);
  if (iVar2 <= (int)param_2) {
    param_2 = iVar2 - 1;
  }
  if (iVar1 <= (int)param_3) {
    param_3 = iVar1 - 1;
  }
  if (param_1[0x10] <= (int)param_4) {
    param_4 = param_1[0x10] - 1;
  }
  return *(int *)(*param_1 + param_5 * 4) + ((iVar1 * param_4 + param_3) * iVar2 + param_2) * 0x84;
}


