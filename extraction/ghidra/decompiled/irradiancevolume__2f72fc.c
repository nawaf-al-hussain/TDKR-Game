// _ZN25CTemplateIrradianceVolumeD1Ev @ 002f72fc

int * _ZN25CTemplateIrradianceVolumeD1Ev(int *param_1)

{
  int iVar1;
  int iVar2;
  
  iVar2 = DAT_002f7350 + 0x2f7328;
  iVar1 = DAT_002f7354 + 0x2f7330;
  *param_1 = DAT_002f734c + 0x2f7324;
  param_1[0x10] = iVar2;
  param_1[0xd] = iVar1;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0xe);
  param_1[0xd] = iVar2;
  *param_1 = iVar2;
  return param_1;
}


