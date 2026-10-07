// _ZN15CTemplateSkyBox4LoadEP13CMemoryStream @ 0049d59c

void _ZN15CTemplateSkyBox4LoadEP13CMemoryStream
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 uVar2;
  
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 4,param_3,param_4,param_4);
  iVar1 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(bool *)(param_1 + 8) = iVar1 != 0;
  uVar2 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0xc) = uVar2;
  uVar2 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + 0x10) = uVar2;
  return;
}

