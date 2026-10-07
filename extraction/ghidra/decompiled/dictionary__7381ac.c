// _ZN7gameswf12ASDictionary4initERKNS_12FunctionCallE @ 007381ac

void _ZN7gameswf12ASDictionary4initERKNS_12FunctionCallE
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int *piVar1;
  
  piVar1 = *(int **)(param_1 + 4);
  if (piVar1 == (int *)0x0) {
    return;
  }
  (**(code **)(*piVar1 + 8))(piVar1,0,param_3,*(code **)(*piVar1 + 8),param_4);
  return;
}


