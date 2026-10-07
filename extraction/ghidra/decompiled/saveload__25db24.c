// _ZN20CWpMovementComponent8SaveLoadEP13CMemoryStream @ 0025db24

void _ZN20CWpMovementComponent8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 local_14 [2];
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd);
  _ZN13CMemoryStream4ReadERf(param_2,local_14);
  *(undefined4 *)(param_1 + 0x18) = local_14[0];
  _ZN13CMemoryStream4ReadERf(param_2,local_14);
  *(undefined4 *)(param_1 + 0x1c) = local_14[0];
  _ZN13CMemoryStream4ReadERf(param_2,local_14);
  *(undefined4 *)(param_1 + 0x18) = local_14[0];
  _ZN13CMemoryStream4ReadERf(param_2,local_14);
  *(undefined4 *)(param_1 + 0x24) = local_14[0];
  _ZN13CMemoryStream4ReadERf(param_2,local_14);
  *(undefined4 *)(param_1 + 0x28) = local_14[0];
  _ZN13CMemoryStream4ReadERf(param_2,local_14);
  *(undefined4 *)(param_1 + 0x2c) = local_14[0];
  _ZN13CMemoryStream4ReadERf(param_2,local_14);
  *(undefined4 *)(param_1 + 0x30) = local_14[0];
  _ZN13CMemoryStream4ReadERf(param_2,local_14);
  *(undefined4 *)(param_1 + 0x34) = local_14[0];
  _ZN13CMemoryStream4ReadERf(param_2,local_14);
  *(undefined4 *)(param_1 + 0x38) = local_14[0];
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x3c);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x40);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x44);
  return;
}


