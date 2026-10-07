// _ZN19CComponentLevelInit4LoadEP13CMemoryStream @ 002118f0

void _ZN19CComponentLevelInit4LoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  int local_5c;
  int local_58;
  int local_54;
  int local_50;
  undefined1 local_4c;
  int local_48;
  undefined4 local_44;
  int local_40;
  int local_3c;
  undefined4 local_38;
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  undefined1 local_24;
  
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 4);
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 8);
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 0xc);
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 0x10);
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 0x14);
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 0x18);
  iVar1 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(bool *)(param_1 + 0x1c) = iVar1 != 0;
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 0x20);
  uVar2 = _ZN13CMemoryStream7ReadIntEv(param_2);
  iVar5 = *(int *)(param_1 + 0x28);
  local_4c = 0;
  local_44 = 0;
  local_5c = *(int *)(DAT_00211d4c + 0x211988) + 0xc;
  local_38 = 0;
  local_24 = 0;
  iVar1 = iVar5 - *(int *)(param_1 + 0x24) >> 2;
  uVar6 = iVar1 * -0x11111111;
  local_58 = local_5c;
  local_54 = local_5c;
  local_50 = local_5c;
  local_48 = local_5c;
  local_40 = local_5c;
  local_3c = local_5c;
  local_34 = local_5c;
  local_30 = local_5c;
  local_2c = local_5c;
  local_28 = local_5c;
  if (uVar6 < uVar2) {
    _ZNSt6vectorI17CContainerMissionSaIS0_EE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPS0_S2_EEjRKS0_
              (param_1 + 0x24,iVar5,uVar2 + iVar1 * 0x11111111,&local_5c);
  }
  else if (uVar2 < uVar6) {
    iVar4 = *(int *)(param_1 + 0x24) + uVar2 * 0x3c;
    for (iVar1 = iVar4; iVar5 != iVar1; iVar1 = iVar1 + 0x3c) {
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar1 + 0x34);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar1 + 0x30);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar1 + 0x2c);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar1 + 0x28);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar1 + 0x20);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar1 + 0x1c);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar1 + 0x14);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar1 + 0xc);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar1 + 8);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar1 + 4);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar1);
    }
    *(int *)(param_1 + 0x28) = iVar4;
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_28);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_2c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_30);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_34);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_3c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_40);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_48);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_50);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_54);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_58);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_5c);
  if (0 < (int)uVar2) {
    iVar1 = 0;
    uVar6 = 0;
    do {
      uVar6 = uVar6 + 1;
      iVar4 = *(int *)(param_1 + 0x24) + iVar1;
      iVar1 = iVar1 + 0x3c;
      _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,iVar4);
      _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,iVar4 + 4);
      _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,iVar4 + 8);
      _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,iVar4 + 0xc);
      iVar5 = _ZN13CMemoryStream8ReadCharEv(param_2);
      *(bool *)(iVar4 + 0x10) = iVar5 != 0;
      _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,iVar4 + 0x14);
      uVar3 = _ZN13CMemoryStream7ReadIntEv(param_2);
      *(undefined4 *)(iVar4 + 0x18) = uVar3;
      _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,iVar4 + 0x1c);
      _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,iVar4 + 0x20);
      uVar3 = _ZN13CMemoryStream7ReadIntEv(param_2);
      *(undefined4 *)(iVar4 + 0x24) = uVar3;
      _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,iVar4 + 0x28);
      _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,iVar4 + 0x2c);
      _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,iVar4 + 0x30);
      _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (param_2,iVar4 + 0x34);
      iVar5 = _ZN13CMemoryStream8ReadCharEv(param_2);
      *(bool *)(iVar4 + 0x38) = iVar5 != 0;
    } while (uVar6 != uVar2);
  }
  iVar1 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(bool *)(param_1 + 0x30) = iVar1 != 0;
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 0x34);
  iVar1 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(bool *)(param_1 + 0x38) = iVar1 != 0;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x3c) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x40) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x44) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x48) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x4c) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x50) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x54) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x58) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x5c) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x60) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 100) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x68) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x6c) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x70) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x74) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x78) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x7c) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x80) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x84) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x88) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x8c) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x90) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x94) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x98) = uVar3;
  uVar3 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x9c) = uVar3;
  iVar1 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(bool *)(param_1 + 0xa0) = iVar1 != 0;
  return;
}


