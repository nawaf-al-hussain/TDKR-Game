// _ZN19CPostProcessManager15GetNextTargetIDEv @ 00457bf4

int _ZN19CPostProcessManager15GetNextTargetIDEv(int param_1)

{
  int iVar1;
  
  if (*(int *)(param_1 + 0x3c) < 1) {
    iVar1 = *(int *)(param_1 + 0x3c) + 1;
  }
  else {
    iVar1 = 0;
  }
  return iVar1;
}


