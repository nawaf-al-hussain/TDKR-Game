// _ZNK6glitch7collada20CAnimationDictionary7getClipEPKc @ 0076d5ec

undefined4 * _ZNK6glitch7collada20CAnimationDictionary7getClipEPKc(int param_1,char *param_2)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  int iVar4;
  undefined4 *puVar5;
  
  iVar4 = *(int *)(*(int *)(param_1 + 0x1c) + 8);
  puVar3 = *(undefined4 **)(*(int *)(param_1 + 0x1c) + 0xc);
  puVar5 = puVar3 + iVar4 * 3;
  iVar4 = (iVar4 * 0xc >> 2) * -0x55555555;
  if (0 < iVar4) {
    do {
      while( true ) {
        iVar1 = iVar4 >> 1;
        iVar2 = strcmp((char *)puVar3[iVar1 * 3],param_2);
        if (-1 < iVar2) break;
        puVar3 = puVar3 + iVar1 * 3 + 3;
        iVar4 = (iVar4 - iVar1) + -1;
        if (iVar4 < 1) goto LAB_0076d66c;
      }
      iVar4 = iVar1;
    } while (iVar1 != 0);
  }
LAB_0076d66c:
  if (puVar5 == puVar3) {
    puVar3 = (undefined4 *)0x0;
  }
  else {
    iVar4 = strcmp((char *)*puVar3,param_2);
    if (iVar4 != 0) {
      puVar3 = (undefined4 *)0x0;
    }
  }
  return puVar3;
}


