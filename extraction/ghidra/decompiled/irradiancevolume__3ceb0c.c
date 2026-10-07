// _ZN33CComponentBuiltinIrradianceVolume4LoadEP13CMemoryStream @ 003ceb0c

void _ZN33CComponentBuiltinIrradianceVolume4LoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 4) = uVar1;
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 8) = uVar1;
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0xc) = uVar1;
  return;
}


