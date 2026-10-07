// _ZN25CTemplateIrradianceVolumeD0Ev @ 002f7368

int * _ZN25CTemplateIrradianceVolumeD0Ev(int *param_1)

{
  int iVar1;
  int iVar2;
  
  iVar2 = DAT_002f73c4 + 0x2f7394;
  iVar1 = DAT_002f73c8 + 0x2f739c;
  *param_1 = DAT_002f73c0 + 0x2f7390;
  param_1[0xd] = iVar1;
  param_1[0x10] = iVar2;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0xe);
  param_1[0xd] = iVar2;
  *param_1 = iVar2;
  _ZdlPv(param_1);
  return param_1;
}


