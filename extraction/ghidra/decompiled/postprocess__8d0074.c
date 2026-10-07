// _ZThn764_N6glitch5scene13SDrawCompiler11postProcessEv @ 008d0074

void _ZThn764_N6glitch5scene13SDrawCompiler11postProcessEv
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  
  puVar2 = (undefined4 *)(param_1 + 0x3c);
  for (puVar1 = (undefined4 *)*puVar2; puVar2 != puVar1; puVar1 = (undefined4 *)*puVar1) {
    (**(code **)(*(int *)puVar1[2] + 8))
              ((int *)puVar1[2],*(undefined4 *)(param_1 + 0x10),param_1 + 0x14,
               *(undefined4 *)(param_1 + 0xc),param_4);
  }
  for (puVar1 = *(undefined4 **)(param_1 + 0x3c); puVar1 != puVar2; puVar1 = (undefined4 *)*puVar1)
  {
    (**(code **)(*(int *)puVar1[2] + 0xc))
              ((int *)puVar1[2],*(undefined4 *)(param_1 + 0x10),param_1 + 0x14,
               *(undefined4 *)(param_1 + 0xc));
    (**(code **)(*(int *)puVar1[2] + 0x10))();
  }
  return;
}


