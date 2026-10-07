// _ZN16CEffectComponent8SaveLoadEP13CMemoryStream @ 0023bf1c

void _ZN16CEffectComponent8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  char cVar6;
  char local_11;
  
  _ZN13CMemoryStream4ReadERb(param_2,&local_11);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x4d);
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x4c);
  iVar3 = *(int *)(param_1 + 0x20);
  uVar4 = *(int *)(param_1 + 0x24) - iVar3 >> 2;
  if (*(char *)(param_1 + 0x4c) == '\0') {
LAB_0023bf6c:
    cVar6 = *(char *)(param_1 + 0x4d);
    uVar5 = 0;
    if (uVar4 == 0) goto LAB_0023bfb0;
    uVar4 = 0;
    do {
      piVar2 = *(int **)(iVar3 + uVar4 * 4);
      uVar4 = uVar4 + 1;
      (**(code **)(*piVar2 + 0x4c))(piVar2,cVar6);
      iVar3 = *(int *)(param_1 + 0x20);
      uVar5 = *(int *)(param_1 + 0x24) - iVar3 >> 2;
    } while (uVar4 < uVar5);
  }
  else {
    uVar5 = 0;
    if (uVar4 != 0) {
      uVar5 = 0;
      do {
        iVar1 = uVar5 * 4;
        uVar5 = uVar5 + 1;
        (**(code **)(**(int **)(iVar3 + iVar1) + 0x154))();
        iVar3 = *(int *)(param_1 + 0x20);
        uVar4 = *(int *)(param_1 + 0x24) - iVar3 >> 2;
      } while (uVar5 < uVar4);
      goto LAB_0023bf6c;
    }
  }
  cVar6 = *(char *)(param_1 + 0x4d);
LAB_0023bfb0:
  if ((cVar6 == '\0') || (local_11 == '\0')) {
    if (uVar5 != 0) {
      uVar4 = 0;
      do {
        piVar2 = *(int **)(iVar3 + uVar4 * 4);
        uVar4 = uVar4 + 1;
        (**(code **)(*piVar2 + 0x198))(piVar2,0);
        iVar3 = *(int *)(param_1 + 0x20);
      } while (uVar4 < (uint)(*(int *)(param_1 + 0x24) - iVar3 >> 2));
    }
  }
  else if (uVar5 != 0) {
    uVar4 = 0;
    do {
      iVar1 = uVar4 * 4;
      uVar4 = uVar4 + 1;
      (**(code **)(**(int **)(iVar3 + iVar1) + 400))();
      iVar3 = *(int *)(param_1 + 0x20);
    } while (uVar4 < (uint)(*(int *)(param_1 + 0x24) - iVar3 >> 2));
  }
  return;
}


