// _ZN19CPostProcessManager9GetTargetEi @ 00457b78

undefined4 _ZN19CPostProcessManager9GetTargetEi(int param_1,int param_2)

{
  undefined4 uVar1;
  
  if (param_2 < *(int *)(param_1 + 0x18) - *(int *)(param_1 + 0x14) >> 2) {
    if (param_2 < 0) {
      uVar1 = 0;
    }
    else {
      uVar1 = *(undefined4 *)(*(int *)(param_1 + 0x14) + param_2 * 4);
    }
    return uVar1;
  }
  return 0;
}


