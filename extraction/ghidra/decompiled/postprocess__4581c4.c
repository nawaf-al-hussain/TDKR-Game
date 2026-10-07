// _ZN19CPostProcessManager20RecomputeCurrentHashEv @ 004581c4

void _ZN19CPostProcessManager20RecomputeCurrentHashEv(int param_1)

{
  int *piVar1;
  uint uVar2;
  uint uVar3;
  int *piVar4;
  int iVar5;
  uint uVar6;
  
  piVar4 = *(int **)(param_1 + 8);
  *(undefined4 *)(param_1 + 0x38) = 0;
  *(undefined4 *)(param_1 + 0x40) = 0;
  piVar1 = (int *)*piVar4;
  if (piVar1 == (int *)0x0) {
    uVar6 = 0;
    uVar2 = 0;
  }
  else if ((char)piVar1[0xc] == '\0') {
    uVar6 = 0;
    uVar2 = 0;
  }
  else {
    uVar2 = 1;
    uVar6 = (**(code **)(*piVar1 + 0x38))();
    *(undefined4 *)(param_1 + 0x38) = 0;
    piVar4 = *(int **)(param_1 + 8);
    *(uint *)(param_1 + 0x40) = uVar6;
  }
  piVar1 = (int *)piVar4[1];
  if ((piVar1 != (int *)0x0) && ((char)piVar1[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar1 + 0x38))();
    piVar4 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 1;
    uVar6 = uVar6 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar6;
  }
  piVar1 = (int *)piVar4[2];
  if ((piVar1 != (int *)0x0) && ((char)piVar1[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar1 + 0x38))();
    piVar4 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 2;
    uVar6 = uVar6 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar6;
  }
  piVar1 = (int *)piVar4[3];
  if ((piVar1 != (int *)0x0) && ((char)piVar1[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar1 + 0x38))();
    piVar4 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 3;
    uVar6 = uVar6 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar6;
  }
  piVar1 = (int *)piVar4[4];
  if ((piVar1 != (int *)0x0) && ((char)piVar1[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar1 + 0x38))();
    piVar4 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 4;
    uVar6 = uVar6 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar6;
  }
  piVar1 = (int *)piVar4[5];
  if ((piVar1 != (int *)0x0) && ((char)piVar1[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar1 + 0x38))();
    piVar4 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 5;
    uVar6 = uVar6 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar6;
  }
  piVar1 = (int *)piVar4[6];
  if ((piVar1 != (int *)0x0) && ((char)piVar1[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar1 + 0x38))();
    piVar4 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 6;
    uVar6 = uVar6 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar6;
  }
  piVar1 = (int *)piVar4[7];
  if ((piVar1 != (int *)0x0) && ((char)piVar1[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar1 + 0x38))();
    piVar4 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 7;
    uVar6 = uVar6 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar6;
  }
  piVar1 = (int *)piVar4[8];
  if ((piVar1 != (int *)0x0) && ((char)piVar1[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar1 + 0x38))();
    *(undefined4 *)(param_1 + 0x38) = 8;
    uVar6 = uVar6 | uVar3;
  }
  uVar6 = uVar6 & *(uint *)(**(int **)(DAT_00458488 + 0x4582cc) + 0x80);
  *(uint *)(param_1 + 0x40) = uVar6;
  if (uVar6 != 0) {
    if (uVar2 < 2) {
      return;
    }
    iVar5 = 0;
    *(undefined4 *)(param_1 + 0x38) = 0;
    while( true ) {
      uVar2 = (**(code **)(**(int **)(*(int *)(param_1 + 8) + iVar5 * 4) + 0x38))();
      if (uVar2 == uVar6) {
        *(int *)(param_1 + 0x38) = iVar5;
        return;
      }
      iVar5 = iVar5 + 1;
      if (iVar5 == 0xc) break;
      uVar6 = *(uint *)(param_1 + 0x40);
    }
    return;
  }
  *(undefined4 *)(param_1 + 0x38) = 0;
  return;
}


