// _ZN19CPostProcessManager17GetEnabledEffectsERSt6vectorISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESaIS9_EE @ 004584e4

void _ZN19CPostProcessManager17GetEnabledEffectsERSt6vectorISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESaIS9_EE
               (int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  undefined1 auStack_1c [8];
  
  iVar3 = *(int *)(param_1 + 8);
  iVar1 = *(int *)(param_1 + 0xc) - iVar3 >> 2;
  if (iVar1 != 0) {
    iVar4 = 0;
    while( true ) {
      iVar3 = *(int *)(iVar3 + iVar4 * 4);
      if ((iVar3 != 0) && (*(char *)(iVar3 + 0x30) != '\0')) {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                  (auStack_1c,iVar3 + 0x3c);
        iVar3 = *(int *)(param_2 + 4);
        if (iVar3 == *(int *)(param_2 + 8)) {
          _ZNSt6vectorISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESaIS8_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS8_SA_EERKS8__constprop_2561
                    (param_2,iVar3,auStack_1c);
        }
        else {
          iVar2 = 0;
          if (iVar3 != 0) {
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                      (iVar3,auStack_1c);
            iVar2 = *(int *)(param_2 + 4);
          }
          *(int *)(param_2 + 4) = iVar2 + 4;
        }
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (auStack_1c);
      }
      if (iVar4 + 1 == iVar1) break;
      iVar4 = iVar4 + 1;
      iVar3 = *(int *)(param_1 + 8);
    }
  }
  return;
}


