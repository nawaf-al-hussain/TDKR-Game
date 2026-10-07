// _ZN17CTriggerComponent8SaveLoadEP13CMemoryStream @ 0025a42c

void _ZN17CTriggerComponent8SaveLoadEP13CMemoryStream
               (int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  _ZN13CMemoryStream4ReadERb(param_2,(int)param_1 + 0xd,param_3,param_4,param_4);
  _ZN13CMemoryStream4ReadERi(param_2,param_1 + 0x26);
  if (*(char *)(param_1[4] + 0x3c) == '\0') {
    return;
  }
  (**(code **)(*(int *)param_1[1] + 0x50))((int *)param_1[1],1);
  (**(code **)(*param_1 + 0x18))(param_1);
  return;
}


