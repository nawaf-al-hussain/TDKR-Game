// _ZN18CPostProcessEffect6EnableEb @ 00455804

void _ZN18CPostProcessEffect6EnableEb(int param_1,int param_2)

{
  if (param_2 != 0) {
    *(undefined1 *)(param_1 + 0x30) = 1;
  }
  *(uint *)(param_1 + 0x40) = (uint)(param_2 == 0);
  *(undefined4 *)(param_1 + 0x44) = 0;
  return;
}


