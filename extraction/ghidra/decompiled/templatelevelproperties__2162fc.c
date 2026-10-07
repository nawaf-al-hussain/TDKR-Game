// _ZThn164_N24CTemplateLevelPropertiesD0Ev @ 002162fc

int * _ZThn164_N24CTemplateLevelPropertiesD0Ev(int *param_1)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  
  piVar1 = param_1 + -0x29;
  iVar2 = DAT_002163ac + 0x21632c;
  iVar3 = DAT_002163a8 + 0x216344;
  *piVar1 = DAT_002163a8 + 0x216328;
  *param_1 = iVar3;
  param_1[5] = iVar2;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x19);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x14);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x13);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x12);
  if (param_1[0xe] != 0) {
    _ZdlPv();
  }
  iVar3 = DAT_002163b0 + 0x216380;
  iVar2 = DAT_002163b4 + 0x216384;
  param_1[5] = iVar3;
  *param_1 = iVar2;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 2);
  *param_1 = iVar3;
  _ZN19CComponentLevelInitD1Ev(piVar1);
  _ZdlPv(piVar1);
  return piVar1;
}


