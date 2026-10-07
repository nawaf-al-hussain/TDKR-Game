// _ZN13CWantedPatrol8SaveLoadEP13CMemoryStream @ 001de7f8

void _ZN13CWantedPatrol8SaveLoadEP13CMemoryStream
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x10,param_3,param_4,param_4);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x14);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x18);
  _ZN13CMemoryStream4ReadERf(param_2,param_1 + 0x1c);
  *(float *)(param_1 + 0x20) = *(float *)(param_1 + 0x18) * *(float *)(param_1 + 0x18);
  *(float *)(param_1 + 0x24) = *(float *)(param_1 + 0x1c) * *(float *)(param_1 + 0x1c);
  return;
}


