// _ZN19CPostProcessManager12EnableEffectESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEER20PostEffectScriptData @ 00457c1c

void _ZN19CPostProcessManager12EnableEffectESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEER20PostEffectScriptData
               (int param_1,undefined4 param_2,int *param_3)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  uint uVar4;
  int iVar5;
  int *piVar6;
  code *pcVar7;
  int *piVar8;
  uint uVar9;
  int iVar10;
  int iVar11;
  uint local_2c;
  
  iVar10 = param_1 + 0x24;
  iVar5 = *(int *)(param_1 + 0x28);
  iVar2 = iVar10;
  while (iVar5 != 0) {
    iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                      (iVar5 + 0x10,param_2);
    if (iVar1 < 0) {
      iVar5 = *(int *)(iVar5 + 0xc);
    }
    else {
      iVar5 = *(int *)(iVar5 + 8);
      iVar2 = iVar5;
    }
  }
  iVar5 = iVar10;
  if ((iVar10 != iVar2) &&
     (iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                        (param_2,iVar2 + 0x10), iVar5 = iVar2, iVar1 < 0)) {
    iVar5 = iVar10;
  }
  if (iVar10 == iVar5) {
    return;
  }
  piVar8 = *(int **)(*(int *)(param_1 + 8) + *(int *)(iVar5 + 0x14) * 4);
  (**(code **)*piVar8)(piVar8,1);
  iVar10 = param_3[2];
  iVar1 = param_3[3];
  iVar2 = param_3[1];
  piVar8[1] = *param_3;
  piVar8[3] = iVar10;
  piVar8[4] = iVar1;
  piVar8[2] = iVar2;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
            (piVar8 + 5,param_3 + 4);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
            (piVar8 + 6,param_3 + 5);
  iVar11 = param_3[6];
  iVar10 = param_3[10];
  iVar1 = param_3[7];
  iVar2 = param_3[9];
  piVar8[9] = param_3[8];
  pcVar7 = *(code **)(*piVar8 + 0x1c);
  piVar8[7] = iVar11;
  piVar8[8] = iVar1;
  piVar8[10] = iVar2;
  piVar8[0xb] = iVar10;
  (*pcVar7)(piVar8);
  if (param_3[10] != -1) {
    *(bool *)(piVar8 + 0x12) = 0 < param_3[10];
  }
  piVar6 = *(int **)(param_1 + 8);
  *(undefined4 *)(param_1 + 0x38) = 0;
  *(undefined4 *)(param_1 + 0x40) = 0;
  piVar3 = (int *)*piVar6;
  if (piVar3 == (int *)0x0) {
    local_2c = 0;
    uVar9 = 0;
  }
  else if ((char)piVar3[0xc] == '\0') {
    local_2c = 0;
    uVar9 = 0;
  }
  else {
    local_2c = 1;
    uVar9 = (**(code **)(*piVar3 + 0x38))();
    *(undefined4 *)(param_1 + 0x38) = 0;
    piVar6 = *(int **)(param_1 + 8);
    *(uint *)(param_1 + 0x40) = uVar9;
  }
  piVar3 = (int *)piVar6[1];
  if ((piVar3 != (int *)0x0) && ((char)piVar3[0xc] != '\0')) {
    local_2c = local_2c + 1;
    uVar4 = (**(code **)(*piVar3 + 0x38))();
    piVar6 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 1;
    uVar9 = uVar9 | uVar4;
    *(uint *)(param_1 + 0x40) = uVar9;
  }
  piVar3 = (int *)piVar6[2];
  if ((piVar3 != (int *)0x0) && ((char)piVar3[0xc] != '\0')) {
    local_2c = local_2c + 1;
    uVar4 = (**(code **)(*piVar3 + 0x38))();
    piVar6 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 2;
    uVar9 = uVar9 | uVar4;
    *(uint *)(param_1 + 0x40) = uVar9;
  }
  piVar3 = (int *)piVar6[3];
  if ((piVar3 != (int *)0x0) && ((char)piVar3[0xc] != '\0')) {
    local_2c = local_2c + 1;
    uVar4 = (**(code **)(*piVar3 + 0x38))();
    piVar6 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 3;
    uVar9 = uVar9 | uVar4;
    *(uint *)(param_1 + 0x40) = uVar9;
  }
  piVar3 = (int *)piVar6[4];
  if ((piVar3 != (int *)0x0) && ((char)piVar3[0xc] != '\0')) {
    local_2c = local_2c + 1;
    uVar4 = (**(code **)(*piVar3 + 0x38))();
    piVar6 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 4;
    uVar9 = uVar9 | uVar4;
    *(uint *)(param_1 + 0x40) = uVar9;
  }
  piVar3 = (int *)piVar6[5];
  if ((piVar3 != (int *)0x0) && ((char)piVar3[0xc] != '\0')) {
    local_2c = local_2c + 1;
    uVar4 = (**(code **)(*piVar3 + 0x38))();
    piVar6 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 5;
    uVar9 = uVar9 | uVar4;
    *(uint *)(param_1 + 0x40) = uVar9;
  }
  piVar3 = (int *)piVar6[6];
  if ((piVar3 != (int *)0x0) && ((char)piVar3[0xc] != '\0')) {
    local_2c = local_2c + 1;
    uVar4 = (**(code **)(*piVar3 + 0x38))();
    piVar6 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 6;
    uVar9 = uVar9 | uVar4;
    *(uint *)(param_1 + 0x40) = uVar9;
  }
  piVar3 = (int *)piVar6[7];
  if ((piVar3 != (int *)0x0) && ((char)piVar3[0xc] != '\0')) {
    local_2c = local_2c + 1;
    uVar4 = (**(code **)(*piVar3 + 0x38))();
    piVar6 = *(int **)(param_1 + 8);
    *(undefined4 *)(param_1 + 0x38) = 7;
    uVar9 = uVar9 | uVar4;
    *(uint *)(param_1 + 0x40) = uVar9;
  }
  piVar3 = (int *)piVar6[8];
  if ((piVar3 != (int *)0x0) && ((char)piVar3[0xc] != '\0')) {
    local_2c = local_2c + 1;
    uVar4 = (**(code **)(*piVar3 + 0x38))();
    *(undefined4 *)(param_1 + 0x38) = 8;
    uVar9 = uVar9 | uVar4;
  }
  uVar9 = uVar9 & *(uint *)(**(int **)(DAT_00458108 + 0x457e64) + 0x80);
  *(uint *)(param_1 + 0x40) = uVar9;
  if (uVar9 == 0) {
    *(undefined4 *)(param_1 + 0x38) = 0;
  }
  else if (1 < local_2c) {
    iVar2 = 0;
    *(undefined4 *)(param_1 + 0x38) = 0;
    while (uVar4 = (**(code **)(**(int **)(*(int *)(param_1 + 8) + iVar2 * 4) + 0x38))(),
          uVar4 != uVar9) {
      iVar2 = iVar2 + 1;
      if (iVar2 == 0xc) goto LAB_00457ebc;
      uVar9 = *(uint *)(param_1 + 0x40);
    }
    iVar10 = *piVar8;
    *(int *)(param_1 + 0x38) = iVar2;
    uVar9 = (**(code **)(iVar10 + 0x38))(piVar8);
    uVar9 = uVar9 & *(uint *)(param_1 + 0x40);
    goto joined_r0x00457ed4;
  }
LAB_00457ebc:
  uVar9 = (**(code **)(*piVar8 + 0x38))(piVar8);
  uVar9 = uVar9 & *(uint *)(param_1 + 0x40);
joined_r0x00457ed4:
  if ((uVar9 != 0) && (*(int *)(iVar5 + 0x14) != *(int *)(param_1 + 0x38))) {
    iVar10 = param_3[1];
    piVar8 = *(int **)(*(int *)(param_1 + 8) + *(int *)(param_1 + 0x38) * 4);
    iVar2 = param_3[3];
    iVar5 = param_3[2];
    piVar8[1] = *param_3;
    piVar8[2] = iVar10;
    piVar8[4] = iVar2;
    piVar8[3] = iVar5;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (piVar8 + 5,param_3 + 4);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (piVar8 + 6,param_3 + 5);
    iVar1 = param_3[6];
    iVar2 = param_3[10];
    iVar10 = param_3[7];
    iVar5 = param_3[9];
    piVar8[9] = param_3[8];
    piVar8[7] = iVar1;
    piVar8[8] = iVar10;
    piVar8[10] = iVar5;
    piVar8[0xb] = iVar2;
    (**(code **)(*piVar8 + 0x1c))(piVar8);
  }
  return;
}


