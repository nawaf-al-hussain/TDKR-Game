// _ZN15CWeatherManager4LoadEP13CMemoryStream @ 0041e8dc

undefined4
_ZN15CWeatherManager4LoadEP13CMemoryStream
          (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 4,param_3,param_4,param_4);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x28);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 8);
  if (*(char *)(param_1 + 4) != '\0') {
    *(undefined4 *)(param_1 + 0x58) =
         *(undefined4 *)(*(int *)(param_1 + 0xc) + *(int *)(param_1 + 8) * 4);
  }
  return 1;
}


