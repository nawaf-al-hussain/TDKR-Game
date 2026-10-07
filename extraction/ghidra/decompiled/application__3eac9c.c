// _ZN11Application7DestroyEv @ 003eac9c

void _ZN11Application7DestroyEv(int *param_1)

{
  _ZN11Application4QuitEv();
  if (param_1 == (int *)0x0) {
    return;
  }
  (**(code **)(*param_1 + 4))();
  return;
}


