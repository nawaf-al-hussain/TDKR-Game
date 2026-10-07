// _ZN19CPostProcessManager13DisableEffectEi @ 0045819c

void _ZN19CPostProcessManager13DisableEffectEi(int param_1,int param_2)

{
  undefined4 *puVar1;
  
  puVar1 = *(undefined4 **)(*(int *)(param_1 + 8) + param_2 * 4);
  if (*(char *)(puVar1 + 0x12) != '\0') {
    return;
  }
  (**(code **)*puVar1)();
  return;
}


