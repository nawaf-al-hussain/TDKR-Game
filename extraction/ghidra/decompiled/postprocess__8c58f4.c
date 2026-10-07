// _ZN6glitch5scene14CSegmentMerger11postProcessEPNS0_13CSceneManagerERSt6vectorINS0_9SDrawInfoENS_4core10SAllocatorIS5_LNS_6memory13E_MEMORY_HINTE0EEEEPNS0_11SRenderTreeE @ 008c58f4

void _ZN6glitch5scene14CSegmentMerger11postProcessEPNS0_13CSceneManagerERSt6vectorINS0_9SDrawInfoENS_4core10SAllocatorIS5_LNS_6memory13E_MEMORY_HINTE0EEEEPNS0_11SRenderTreeE
               (int param_1,undefined4 param_2,int *param_3)

{
  int *piVar1;
  uint uVar2;
  int *piVar3;
  int iVar4;
  undefined4 uVar5;
  int *piVar6;
  
  piVar6 = *(int **)(param_1 + 4);
  piVar3 = *(int **)(param_1 + 8);
  if (piVar6 != piVar3) {
    do {
      piVar1 = (int *)*piVar6;
      if (7 < (uint)(piVar6[1] - (int)piVar1)) {
        iVar4 = *param_3;
        uVar2 = 1;
        uVar5 = **(undefined4 **)(*piVar1 * 0x98 + iVar4 + 0x2c);
        while( true ) {
          piVar1 = piVar1 + uVar2;
          uVar2 = uVar2 + 1;
          **(undefined4 **)(*piVar1 * 0x98 + iVar4 + 0x2c) = uVar5;
          piVar1 = (int *)*piVar6;
          if ((uint)(piVar6[1] - (int)piVar1 >> 2) <= uVar2) break;
          iVar4 = *param_3;
        }
        piVar3 = *(int **)(param_1 + 8);
      }
      piVar6 = piVar6 + 6;
    } while (piVar6 != piVar3);
  }
  return;
}


