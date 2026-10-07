// _ZN11Application11SelfDestroyEv @ 003ea718

void _ZN11Application11SelfDestroyEv(void)

{
  int *piVar1;
  
  piVar1 = (int *)_ZN11Application11GetInstanceEv();
  _ZN11Application4QuitEv();
  if (piVar1 == (int *)0x0) {
    return;
  }
  (**(code **)(*piVar1 + 4))(piVar1);
  return;
}


