// _ZN6glitch7collada37CSceneNodeAnimatorSynchronizedBlender22setAnimationDictionaryERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 007844b0

void _ZN6glitch7collada37CSceneNodeAnimatorSynchronizedBlender22setAnimationDictionaryERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  int *piVar2;
  undefined4 extraout_r2;
  int iVar3;
  code *pcVar4;
  int iVar5;
  
  iVar3 = *(int *)(param_1 + 0x40);
  iVar1 = *(int *)(param_1 + 0x44) - iVar3 >> 2;
  if (iVar1 < 1) {
    return;
  }
  iVar5 = 0;
  while( true ) {
    piVar2 = *(int **)(iVar3 + iVar5 * 4);
    iVar5 = iVar5 + 1;
    pcVar4 = *(code **)(*piVar2 + 100);
    (*pcVar4)(piVar2,param_2,param_3,pcVar4,param_4);
    if (iVar5 == iVar1) break;
    iVar3 = *(int *)(param_1 + 0x40);
    param_3 = extraout_r2;
  }
  return;
}


