// _ZN34CPostProcessEffect_ColorCorrection4SaveEP13CMemoryStream @ 0045b1b8

void _ZN34CPostProcessEffect_ColorCorrection4SaveEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int local_20;
  int local_1c;
  undefined1 auStack_18 [4];
  undefined1 auStack_14 [4];
  
  _ZN13CMemoryStream8WriteIntEi(param_2,*(undefined1 *)(param_1 + 0x30));
  _ZN13CMemoryStream8WriteIntEi(param_2,*(undefined4 *)(param_1 + 0x40));
  _ZN13CMemoryStream10WriteFloatEf(param_2,*(undefined4 *)(param_1 + 0x44));
  local_20 = *(int *)(DAT_0045b2b8 + 0x45b204) + 0xc;
  local_1c = local_20;
  if (*(int *)(param_1 + 0x50) == 0) {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_18,DAT_0045b2c0 + 0x45b2b4);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_18,*(int *)(param_1 + 0x50) + 0x10);
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
            (&local_20,auStack_18);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_18);
  if (*(int *)(param_1 + 0x54) == 0) {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_14,DAT_0045b2bc + 0x45b2a0);
  }
  else {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_14,*(int *)(param_1 + 0x54) + 0x10);
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
            (&local_1c,auStack_14);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_14);
  _ZN13CMemoryStream12WriteStringCERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,&local_20);
  _ZN13CMemoryStream12WriteStringCERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,&local_1c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_1c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_20);
  return;
}


