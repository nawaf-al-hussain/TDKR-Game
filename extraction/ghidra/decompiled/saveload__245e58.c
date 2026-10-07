// _ZN16CHealthComponent8SaveLoadEP13CMemoryStream @ 00245e58

void _ZN16CHealthComponent8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 local_18;
  undefined1 auStack_14 [8];
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd);
  if (*(char *)(*(int *)(param_1 + 4) + 0xed) == '\0') {
    _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xa8);
    _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xac);
    _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x18);
  }
  else {
    _ZN13CMemoryStream4ReadERi(param_2,auStack_14);
    _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0xac);
    _ZN13CMemoryStream4ReadERi(param_2,auStack_14);
  }
  _ZN13CMemoryStream4ReadERi(param_2,&local_18);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x1c);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x20);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x24);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x4c);
  if ((*(char *)(*(int *)(param_1 + 4) + 0xed) != '\0') ||
     (iVar1 = *(int *)(*(int *)(param_1 + 4) + 0xe4), iVar1 == 0xc38e || iVar1 == 0x9c44)) {
    *(undefined4 *)(param_1 + 0x18) = *(undefined4 *)(param_1 + 0xa8);
  }
  *(undefined4 *)(param_1 + 0x28) = local_18;
  return;
}


