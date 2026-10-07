// _ZNK6glitch10irradiance17CIrradianceVolume11getPointLowEiiii @ 007ca574

int _ZNK6glitch10irradiance17CIrradianceVolume11getPointLowEiiii
              (int param_1,uint param_2,uint param_3,uint param_4,int param_5)

{
  int iVar1;
  int iVar2;
  
  iVar2 = *(int *)(param_1 + 0x38);
  param_2 = param_2 & ~((int)param_2 >> 0x1f);
  iVar1 = *(int *)(param_1 + 0x3c);
  param_3 = param_3 & ~((int)param_3 >> 0x1f);
  param_4 = param_4 & ~((int)param_4 >> 0x1f);
  if (iVar2 <= (int)param_2) {
    param_2 = iVar2 - 1;
  }
  if (iVar1 <= (int)param_3) {
    param_3 = iVar1 - 1;
  }
  if (*(int *)(param_1 + 0x40) <= (int)param_4) {
    param_4 = *(int *)(param_1 + 0x40) - 1;
  }
  return *(int *)(*(int *)(param_1 + 0xc) + param_5 * 4) +
         ((iVar1 * param_4 + param_3) * iVar2 + param_2) * 0x24;
}


