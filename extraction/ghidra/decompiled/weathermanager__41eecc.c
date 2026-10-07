// _ZN15CWeatherManager18SetLevelPropertiesEP24CTemplateLevelProperties @ 0041eecc

void _ZN15CWeatherManager18SetLevelPropertiesEP24CTemplateLevelProperties(int *param_1,int param_2)

{
  int iVar1;
  
  *param_1 = param_2;
  if (param_1[0x16] != 0) {
    return;
  }
  if (param_2 != 0) {
    iVar1 = *(int *)(param_2 + 0xc4);
    param_1[0x16] = param_2 + 0xb8;
    param_1[0x17] = iVar1;
    param_1[0x18] = *(int *)(param_2 + 200);
    param_1[0x19] = *(int *)(param_2 + 0xcc);
    param_1[0x1a] = *(int *)(param_2 + 0xd0);
    param_1[0x1b] = *(int *)(param_2 + 0xd4);
    param_1[0x1c] = *(int *)(param_2 + 0xd8);
    param_1[0x1d] = *(int *)(param_2 + 0x110);
    return;
  }
  param_1[0x16] = 0;
  return;
}

