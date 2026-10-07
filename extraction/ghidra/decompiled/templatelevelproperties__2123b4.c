// _ZThn164_N24CTemplateLevelProperties4LoadEP13CMemoryStream @ 002123b4

void _ZThn164_N24CTemplateLevelProperties4LoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  
  _ZN19CComponentLevelInit4LoadEP13CMemoryStream();
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 4) = uVar1;
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 8);
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0xc) = uVar1;
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x10) = uVar1;
  _ZN25CComponentBaseGlobalIllum4LoadEP13CMemoryStream(param_1 + 0x14,param_2);
  uVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + 0x84) = uVar1;
  return;
}


