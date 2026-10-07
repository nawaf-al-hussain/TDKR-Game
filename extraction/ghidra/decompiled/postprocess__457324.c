// _ZN19CPostProcessManager6UpdateEf @ 00457324

void _ZN19CPostProcessManager6UpdateEf
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int *piVar1;
  uint uVar2;
  uint uVar3;
  int *piVar4;
  int iVar5;
  int iVar6;
  uint uVar7;
  
  piVar4 = *(int **)(param_1 + 8);
  iVar5 = *(int *)(param_1 + 0xc) - (int)piVar4 >> 2;
  if (iVar5 != 0) {
    iVar6 = 0;
    do {
      while( true ) {
        piVar1 = (int *)piVar4[iVar6];
        iVar6 = iVar6 + 1;
        if ((piVar1 == (int *)0x0) || ((char)piVar1[0xc] == '\0')) break;
        (**(code **)(*piVar1 + 0xc))(piVar1,param_2,piVar4,*(code **)(*piVar1 + 0xc),param_4);
        piVar4 = *(int **)(param_1 + 8);
        if (iVar6 == iVar5) goto LAB_0045738c;
      }
    } while (iVar6 != iVar5);
  }
LAB_0045738c:
  piVar4 = (int *)*piVar4;
  *(undefined4 *)(param_1 + 0x38) = 0;
  *(undefined4 *)(param_1 + 0x40) = 0;
  if (piVar4 == (int *)0x0) {
    uVar7 = 0;
    uVar2 = 0;
  }
  else if ((char)piVar4[0xc] == '\0') {
    uVar7 = 0;
    uVar2 = 0;
  }
  else {
    uVar2 = 1;
    uVar7 = (**(code **)(*piVar4 + 0x38))();
    *(undefined4 *)(param_1 + 0x38) = 0;
    *(uint *)(param_1 + 0x40) = uVar7;
  }
  iVar5 = *(int *)(param_1 + 8);
  piVar4 = *(int **)(iVar5 + 4);
  if ((piVar4 != (int *)0x0) && ((char)piVar4[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar4 + 0x38))();
    iVar5 = *(int *)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 1;
    uVar7 = uVar7 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar7;
  }
  piVar4 = *(int **)(iVar5 + 8);
  if ((piVar4 != (int *)0x0) && ((char)piVar4[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar4 + 0x38))();
    iVar5 = *(int *)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 2;
    uVar7 = uVar7 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar7;
  }
  piVar4 = *(int **)(iVar5 + 0xc);
  if ((piVar4 != (int *)0x0) && ((char)piVar4[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar4 + 0x38))();
    iVar5 = *(int *)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 3;
    uVar7 = uVar7 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar7;
  }
  piVar4 = *(int **)(iVar5 + 0x10);
  if ((piVar4 != (int *)0x0) && ((char)piVar4[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar4 + 0x38))();
    iVar5 = *(int *)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 4;
    uVar7 = uVar7 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar7;
  }
  piVar4 = *(int **)(iVar5 + 0x14);
  if ((piVar4 != (int *)0x0) && ((char)piVar4[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar4 + 0x38))();
    iVar5 = *(int *)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 5;
    uVar7 = uVar7 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar7;
  }
  piVar4 = *(int **)(iVar5 + 0x18);
  if ((piVar4 != (int *)0x0) && ((char)piVar4[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar4 + 0x38))();
    iVar5 = *(int *)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 6;
    uVar7 = uVar7 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar7;
  }
  piVar4 = *(int **)(iVar5 + 0x1c);
  if ((piVar4 != (int *)0x0) && ((char)piVar4[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar4 + 0x38))();
    iVar5 = *(int *)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 7;
    uVar7 = uVar7 | uVar3;
    *(uint *)(param_1 + 0x40) = uVar7;
  }
  piVar4 = *(int **)(iVar5 + 0x20);
  if ((piVar4 != (int *)0x0) && ((char)piVar4[0xc] != '\0')) {
    uVar2 = uVar2 + 1;
    uVar3 = (**(code **)(*piVar4 + 0x38))();
    *(undefined4 *)(param_1 + 0x38) = 8;
    uVar7 = uVar7 | uVar3;
  }
  uVar7 = uVar7 & *(uint *)(**(int **)(DAT_00457644 + 0x45748c) + 0x80);
  *(uint *)(param_1 + 0x40) = uVar7;
  if (uVar7 != 0) {
    if (uVar2 < 2) {
      return;
    }
    iVar5 = 0;
    *(undefined4 *)(param_1 + 0x38) = 0;
    while( true ) {
      uVar2 = (**(code **)(**(int **)(*(int *)(param_1 + 8) + iVar5 * 4) + 0x38))();
      if (uVar2 == uVar7) {
        *(int *)(param_1 + 0x38) = iVar5;
        return;
      }
      iVar5 = iVar5 + 1;
      if (iVar5 == 0xc) break;
      uVar7 = *(uint *)(param_1 + 0x40);
    }
    return;
  }
  *(undefined4 *)(param_1 + 0x38) = 0;
  return;
}


