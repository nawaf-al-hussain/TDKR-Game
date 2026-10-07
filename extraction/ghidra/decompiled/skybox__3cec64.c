// _ZN23CComponentBuiltinSkyBox4LoadEP13CMemoryStream @ 003cec64

void _ZN23CComponentBuiltinSkyBox4LoadEP13CMemoryStream
               (int param_1,int *param_2,undefined4 param_3,undefined4 param_4)

{
  char cVar1;
  undefined4 uVar2;
  
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + 4,param_3,param_4,param_4);
  cVar1 = *(char *)(*param_2 + param_2[3]);
  param_2[3] = param_2[3] + 1;
  *(bool *)(param_1 + 8) = cVar1 != '\0';
  uVar2 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0xc) = uVar2;
  return;
}

