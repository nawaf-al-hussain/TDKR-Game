// _ZN24CTemplateLevelProperties4LoadEP13CMemoryStream @ 002123bc

void _ZN24CTemplateLevelProperties4LoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  
  _ZN19CComponentLevelInit4LoadEP13CMemoryStream();
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0xa8) = uVar1;
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 0xac);
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0xb0) = uVar1;
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0xb4) = uVar1;
  _ZN25CComponentBaseGlobalIllum4LoadEP13CMemoryStream(param_1 + 0xb8,param_2);
  uVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + 0x128) = uVar1;
  return;
}


