// _ZN15CWeatherManager5ResetEv @ 0041e92c

void _ZN15CWeatherManager5ResetEv(int param_1)

{
  int iVar1;
  undefined1 auStack_14 [8];
  
  iVar1 = DAT_0041e990;
  if (*(int *)(param_1 + 0x20) != 0) {
    *(undefined4 *)(param_1 + 0x20) = 0;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (auStack_14,iVar1 + 0x41e95c);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (param_1 + 0x18,auStack_14);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_14);
  }
  *(undefined1 *)(param_1 + 4) = 0;
  *(undefined4 *)(param_1 + 8) = 0;
  *(undefined4 *)(param_1 + 0x58) = 0;
  *(undefined1 *)(param_1 + 0x28) = 0;
  return;
}

