// _ZN18CPostProcessEffect6UpdateEf @ 00455674

void _ZN18CPostProcessEffect6UpdateEf(int *param_1,float param_2)

{
  int iVar1;
  code *pcVar2;
  
  iVar1 = param_1[0x10];
  if (iVar1 == 1) {
    if ((float)param_1[3] != -1.0) {
      pcVar2 = *(code **)(*param_1 + 0x18);
      param_1[0x11] = (int)((float)param_1[0x11] + param_2);
      (*pcVar2)();
      if ((float)param_1[0x11] < (float)param_1[3]) {
        return;
      }
    }
    *(undefined1 *)(param_1 + 0xc) = 0;
    param_1[0x10] = 3;
    param_1[0x11] = 0;
    return;
  }
  if (iVar1 != 2) {
    if (iVar1 != 0) {
      return;
    }
    if ((float)param_1[2] != -1.0) {
      pcVar2 = *(code **)(*param_1 + 0x14);
      param_1[0x11] = (int)((float)param_1[0x11] + param_2);
      (*pcVar2)();
      if ((float)param_1[0x11] < (float)param_1[2]) {
        return;
      }
    }
    param_1[0x10] = 2;
    param_1[0x11] = 0;
    return;
  }
  if ((float)param_1[1] == -1.0) {
    return;
  }
  if ((float)param_1[0x11] < (float)param_1[1]) {
    param_1[0x11] = (int)(param_2 + (float)param_1[0x11]);
  }
  else {
    param_1[0x10] = 1;
    param_1[0x11] = 0;
  }
  return;
}


