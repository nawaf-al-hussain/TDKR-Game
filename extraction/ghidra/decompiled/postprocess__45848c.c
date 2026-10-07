// _ZN19CPostProcessManager17DisableAllEffectsEv @ 0045848c

void _ZN19CPostProcessManager17DisableAllEffectsEv(int param_1)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  int iVar4;
  
  iVar2 = *(int *)(param_1 + 8);
  iVar1 = *(int *)(param_1 + 0xc) - iVar2 >> 2;
  if (iVar1 < 1) {
    return;
  }
  iVar4 = 0;
  while( true ) {
    puVar3 = *(undefined4 **)(iVar2 + iVar4 * 4);
    iVar4 = iVar4 + 1;
    if (puVar3 != (undefined4 *)0x0) {
      (**(code **)*puVar3)(puVar3);
    }
    if (iVar4 == iVar1) break;
    iVar2 = *(int *)(param_1 + 8);
  }
  return;
}


