// _ZN23PullableObjectComponent8SaveLoadEP13CMemoryStream @ 0024f1a4

void _ZN23PullableObjectComponent8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  undefined4 local_14 [2];
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0xd);
  _ZN13CMemoryStream4ReadERi(param_2,local_14);
  *(undefined4 *)(param_1 + 0x4c) = local_14[0];
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x50);
  return;
}


