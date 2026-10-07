// _ZN15CWeatherManager15SetIlluminationEP25CComponentBaseGlobalIllum @ 0041d448

void _ZN15CWeatherManager15SetIlluminationEP25CComponentBaseGlobalIllum(int *param_1,int param_2)

{
  if (param_2 == 0) {
    if (*param_1 == 0) {
      param_1[0x16] = 0;
      return;
    }
    param_2 = *param_1 + 0xb8;
    param_1[0x16] = param_2;
    if (param_2 == 0) {
      return;
    }
  }
  else {
    param_1[0x16] = param_2;
  }
  param_1[0x17] = *(int *)(param_2 + 0xc);
  param_1[0x18] = *(int *)(param_2 + 0x10);
  param_1[0x19] = *(int *)(param_2 + 0x14);
  param_1[0x1a] = *(int *)(param_2 + 0x18);
  param_1[0x1b] = *(int *)(param_2 + 0x1c);
  param_1[0x1c] = *(int *)(param_2 + 0x20);
  param_1[0x1d] = *(int *)(param_2 + 0x58);
  return;
}

