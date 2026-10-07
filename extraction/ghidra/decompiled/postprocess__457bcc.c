// _ZN19CPostProcessManager11FlipTargetsEv @ 00457bcc

void _ZN19CPostProcessManager11FlipTargetsEv(int param_1)

{
  int iVar1;
  
  if (*(char *)(param_1 + 0x66) == '\0') {
    return;
  }
  iVar1 = *(int *)(param_1 + 0x3c) + 1;
  if (1 < iVar1) {
    iVar1 = 0;
  }
  *(int *)(param_1 + 0x3c) = iVar1;
  return;
}


