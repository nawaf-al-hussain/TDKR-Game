// _ZN19CPostProcessManager4SaveEP13CMemoryStream @ 0045870c

void _ZN19CPostProcessManager4SaveEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int *piVar1;
  int iVar2;
  
  iVar2 = 0;
  do {
    piVar1 = *(int **)(*(int *)(param_1 + 8) + iVar2);
    iVar2 = iVar2 + 4;
    if (piVar1 != (int *)0x0) {
      (**(code **)(*piVar1 + 0x30))(piVar1,param_2);
    }
  } while (iVar2 != 0x30);
  return;
}


