// _ZN19CPostProcessManager7PreDrawEv @ 004578d4

void _ZN19CPostProcessManager7PreDrawEv
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int *piVar1;
  code *pcVar2;
  
  piVar1 = *(int **)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x38) * 4);
  pcVar2 = *(code **)(*piVar1 + 0x20);
  (*pcVar2)(piVar1,*(undefined4 *)(param_1 + 0x3c),0xffffffff,pcVar2,param_4);
  return;
}


