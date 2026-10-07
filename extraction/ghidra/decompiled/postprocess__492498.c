// _ZN6CLevel28DisablePostProcessingEffectsEv @ 00492498

void _ZN6CLevel28DisablePostProcessingEffectsEv(void)

{
  int iVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  int iVar5;
  
  iVar2 = *(int *)(**(int **)(DAT_004924b4 + 0x4924a4) + 0x178);
  if (iVar2 == 0) {
    return;
  }
  iVar3 = *(int *)(iVar2 + 8);
  iVar1 = *(int *)(iVar2 + 0xc) - iVar3 >> 2;
  if (iVar1 < 1) {
    return;
  }
  iVar5 = 0;
  while( true ) {
    puVar4 = *(undefined4 **)(iVar3 + iVar5 * 4);
    iVar5 = iVar5 + 1;
    if (puVar4 != (undefined4 *)0x0) {
      (**(code **)*puVar4)(puVar4);
    }
    if (iVar5 == iVar1) break;
    iVar3 = *(int *)(iVar2 + 8);
  }
  return;
}


