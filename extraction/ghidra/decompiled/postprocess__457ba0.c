// _ZN19CPostProcessManager8CloneRTTEi @ 00457ba0

void _ZN19CPostProcessManager8CloneRTTEi
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 extraout_r2;
  code *pcVar1;
  
  _ZN11Application11GetInstanceEv();
  pcVar1 = *(code **)(*(int *)**(undefined4 **)(param_1 + 8) + 0x24);
  (*pcVar1)((int *)**(undefined4 **)(param_1 + 8),param_2,extraout_r2,pcVar1,param_4);
  return;
}


