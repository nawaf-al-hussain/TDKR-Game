// _ZN19CPostProcessManager16GetCurrentTargetEv @ 00455d38

undefined4 _ZN19CPostProcessManager16GetCurrentTargetEv(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  
  iVar2 = *(int *)(param_1 + 0x3c);
  if (iVar2 < *(int *)(param_1 + 0x18) - *(int *)(param_1 + 0x14) >> 2) {
    if (iVar2 < 0) {
      uVar1 = 0;
    }
    else {
      uVar1 = *(undefined4 *)(*(int *)(param_1 + 0x14) + iVar2 * 4);
    }
    return uVar1;
  }
  return 0;
}


