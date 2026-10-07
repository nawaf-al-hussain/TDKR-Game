// _ZN24CComponentBeastBakeGroup4LoadEP13CMemoryStream @ 003ce548

void _ZN24CComponentBeastBakeGroup4LoadEP13CMemoryStream
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 uVar1;
  
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 4,param_3,param_4,param_4);
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 8) = uVar1;
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 0xc);
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x10) = uVar1;
  return;
}

