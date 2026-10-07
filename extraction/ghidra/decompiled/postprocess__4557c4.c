// _ZN18CPostProcessEffect4LoadEP13CMemoryStream @ 004557c4

void _ZN18CPostProcessEffect4LoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 uVar2;
  
  iVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(bool *)(param_1 + 0x30) = iVar1 != 0;
  uVar2 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + 0x40) = uVar2;
  uVar2 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x44) = uVar2;
  return;
}


