// _ZN24CTemplateLevelPropertiesD2Ev @ 00216248

int * _ZN24CTemplateLevelPropertiesD2Ev(int *param_1)

{
  int iVar1;
  int iVar2;
  
  iVar1 = DAT_002162e8 + 0x216270;
  iVar2 = DAT_002162e4 + 0x216288;
  *param_1 = DAT_002162e4 + 0x21626c;
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
  iVar2 = DAT_002162ec + 0x2162c4;
  iVar1 = DAT_002162f0 + 0x2162c8;
  param_1[0x2e] = iVar2;
  param_1[0x29] = iVar1;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x2b);
  param_1[0x29] = iVar2;
  _ZN19CComponentLevelInitD1Ev(param_1);
  return param_1;
}


