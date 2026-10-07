// _ZN26CComponentIrradianceVolume4LoadEP13CMemoryStream @ 002f6b48

void _ZN26CComponentIrradianceVolume4LoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 uVar2;
  
  iVar1 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(bool *)(param_1 + 4) = iVar1 != 0;
  uVar2 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 8) = uVar2;
  iVar1 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(bool *)(param_1 + 0xc) = iVar1 != 0;
  uVar2 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x10) = uVar2;
  uVar2 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x14) = uVar2;
  return;
}


