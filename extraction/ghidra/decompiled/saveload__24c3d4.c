// _ZN16CMotionComponent8SaveLoadEP13CMemoryStream @ 0024c3d4

void _ZN16CMotionComponent8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int iVar2;
  int local_18;
  undefined4 local_14;
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd);
  iVar2 = 0;
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x90);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xac);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xb0);
  local_18 = 0;
  _ZN13CMemoryStream4ReadERi(param_2,&local_18);
  if (0 < local_18) {
    do {
      _ZN13CMemoryStream4ReadERf(param_2,&local_14);
      iVar2 = iVar2 + 1;
      _ZN13CMemoryStream4ReadERf(param_2,&local_14);
      _ZN13CMemoryStream4ReadERf(param_2,&local_14);
    } while (iVar2 < local_18);
    *(undefined4 *)(param_1 + 0xd4) = *(undefined4 *)(param_1 + 0xd0);
    _ZN13CMemoryStream4ReadERf(param_2,&local_14);
    *(undefined4 *)(param_1 + 0x98) = local_14;
    _ZN13CMemoryStream4ReadERf(param_2,&local_14);
    *(undefined4 *)(param_1 + 0x9c) = local_14;
    _ZN13CMemoryStream4ReadERf(param_2,&local_14);
    *(undefined4 *)(param_1 + 0xa0) = local_14;
    _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xa4);
    _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xa8);
    _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0xdc);
    uVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
    *(undefined4 *)(param_1 + 0xe0) = uVar1;
    _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xe4);
  }
  return;
}


