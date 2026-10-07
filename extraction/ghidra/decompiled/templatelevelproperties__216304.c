// _ZN24CTemplateLevelPropertiesD0Ev @ 00216304

int * _ZN24CTemplateLevelPropertiesD0Ev(int *param_1)

{
  int iVar1;
  int iVar2;
  
  iVar1 = DAT_002163ac + 0x21632c;
  iVar2 = DAT_002163a8 + 0x216344;
  *param_1 = DAT_002163a8 + 0x216328;
  param_1[0x29] = iVar2;
  param_1[0x2e] = iVar1;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x42);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x3d);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x3c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x3b);
  if (param_1[0x37] != 0) {
    _ZdlPv();
  }
  iVar2 = DAT_002163b0 + 0x216380;
  iVar1 = DAT_002163b4 + 0x216384;
  param_1[0x2e] = iVar2;
  param_1[0x29] = iVar1;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x2b);
  param_1[0x29] = iVar2;
  _ZN19CComponentLevelInitD1Ev(param_1);
  _ZdlPv(param_1);
  return param_1;
}


