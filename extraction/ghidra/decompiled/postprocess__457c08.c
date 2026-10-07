// _ZN19CPostProcessManager15IsEffectEnabledEi @ 00457c08

undefined1 _ZN19CPostProcessManager15IsEffectEnabledEi(int param_1,int param_2)

{
  undefined1 uVar1;
  int iVar2;
  
  iVar2 = *(int *)(*(int *)(param_1 + 8) + param_2 * 4);
  uVar1 = 0;
  if (iVar2 != 0) {
    uVar1 = *(undefined1 *)(iVar2 + 0x30);
  }
  return uVar1;
}


