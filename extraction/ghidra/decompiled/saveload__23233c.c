// _ZN28CCollectibleGeneralComponent8SaveLoadEP13CMemoryStream @ 0023233c

void _ZN28CCollectibleGeneralComponent8SaveLoadEP13CMemoryStream
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 uVar1;
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd,param_3,param_4,param_4);
  uVar1 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x14) = uVar1;
  return;
}


