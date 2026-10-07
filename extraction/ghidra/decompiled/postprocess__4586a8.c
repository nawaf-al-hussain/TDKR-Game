// _ZN19CPostProcessManager4LoadEP13CMemoryStream @ 004586a8

void _ZN19CPostProcessManager4LoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  
  iVar1 = *(int *)(param_1 + 8);
  iVar3 = 0;
  do {
    piVar2 = *(int **)(iVar1 + iVar3);
    iVar3 = iVar3 + 4;
    if (piVar2 != (int *)0x0) {
      (**(code **)(*piVar2 + 0x34))(piVar2,param_2);
      iVar1 = *(int *)(param_1 + 8);
    }
  } while (iVar3 != 0x30);
  if (*(char *)(*(undefined4 **)(iVar1 + 0x10) + 0x12) != '\0') {
    return;
  }
  (**(code **)**(undefined4 **)(iVar1 + 0x10))();
  return;
}


