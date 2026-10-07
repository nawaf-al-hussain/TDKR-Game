// _ZN15CQuestComponent8SaveLoadEP13CMemoryStream @ 0019158c

void _ZN15CQuestComponent8SaveLoadEP13CMemoryStream
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  short *psVar3;
  int iVar4;
  code *pcVar5;
  int iVar6;
  
  iVar1 = (**(code **)(**(int **)(param_1 + 4) + 0x54))();
  if (iVar1 == 0) {
    return;
  }
  puVar2 = *(undefined4 **)(*(int *)(DAT_0019162c + 0x1915bc) + 8);
  iVar6 = *(int *)(*(int *)(param_1 + 0x10) + 4);
  iVar1 = *(int *)(*(int *)(DAT_0019162c + 0x1915bc) + 0xc) - (int)puVar2 >> 2;
  if (iVar1 == 0) {
    return;
  }
  psVar3 = (short *)*puVar2;
  if (iVar6 != *psVar3) {
    iVar4 = 0;
    do {
      iVar4 = iVar4 + 1;
      if (iVar1 == iVar4) {
        return;
      }
      psVar3 = (short *)puVar2[iVar4];
    } while (iVar6 != *psVar3);
  }
  if ((char)psVar3[4] != '\a') {
    return;
  }
  pcVar5 = *(code **)(**(int **)(param_1 + 4) + 0x50);
  (*pcVar5)(*(int **)(param_1 + 4),0,psVar3,pcVar5,param_4);
  return;
}


