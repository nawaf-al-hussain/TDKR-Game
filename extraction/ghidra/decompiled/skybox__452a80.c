// _ZN22CCustomSkyBoxSceneNode9onAnimateEf @ 00452a80

void _ZN22CCustomSkyBoxSceneNode9onAnimateEf(int param_1,undefined4 param_2)

{
  int *piVar1;
  undefined1 auStack_1c [16];
  
  _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv
            (auStack_1c,
             *(undefined4 *)(*(int *)(**(int **)(DAT_00452af0 + 0x452a90) + 0x10) + 0x1b8));
  (**(code **)(**(int **)(param_1 + 0x108) + 0xb8))(*(int **)(param_1 + 0x108),auStack_1c);
  _ZN6glitch5scene10ISceneNode22updateAbsolutePositionEb(*(undefined4 *)(param_1 + 0x108),1);
  piVar1 = *(int **)(param_1 + 0x108);
  if (piVar1 != (int *)0x0) {
    (**(code **)(*piVar1 + 0x18))(piVar1,param_2);
  }
  return;
}

