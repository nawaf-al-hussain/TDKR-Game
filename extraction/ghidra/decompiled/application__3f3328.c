// _ZN11Application19SaveCurrentProgressEP13CMemoryStream @ 003f3328

void _ZN11Application19SaveCurrentProgressEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint *puVar4;
  uint uVar5;
  uint uVar6;
  int *piVar7;
  int iVar8;
  undefined4 *puVar9;
  int *piVar10;
  
  puVar9 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
  iVar2 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) - (int)puVar9;
  uVar6 = iVar2 >> 2;
  if (uVar6 < 2) {
    return;
  }
  iVar8 = 1;
LAB_003f3364:
  uVar5 = 0;
  do {
    piVar7 = (int *)puVar9[uVar5];
    uVar5 = uVar5 + 1;
    iVar3 = *piVar7;
    if (iVar8 == iVar3) {
      if ((uint)(piVar7[4] - piVar7[3]) >> 2 != 0) {
        uVar6 = 1;
        goto LAB_003f33b4;
      }
      break;
    }
  } while (uVar5 < uVar6);
  uVar6 = iVar2 >> 2;
  if (uVar6 <= iVar8 + 1U) {
    return;
  }
  goto LAB_003f3394;
LAB_003f33b4:
  if (iVar2 >> 2 == 0) {
    piVar10 = (int *)0x0;
  }
  else {
    piVar10 = (int *)*puVar9;
    if (*piVar10 != iVar3) {
      iVar1 = 0;
      do {
        iVar1 = iVar1 + 1;
        if (iVar1 == iVar2 >> 2) {
          piVar10 = (int *)0x0;
          break;
        }
        piVar10 = (int *)puVar9[iVar1];
      } while (*piVar10 != iVar3);
    }
  }
  puVar9 = (undefined4 *)piVar10[3];
  iVar2 = piVar10[4] - (int)puVar9 >> 2;
  if (iVar2 == 0) {
    puVar4 = (uint *)0x0;
  }
  else {
    puVar4 = (uint *)*puVar9;
    if (uVar6 != *puVar4) {
      iVar3 = 0;
      do {
        iVar3 = iVar3 + 1;
        if (iVar3 == iVar2) {
          puVar4 = (uint *)0x0;
          break;
        }
        puVar4 = (uint *)puVar9[iVar3];
      } while (uVar6 != *puVar4);
    }
  }
  _ZN13CMemoryStream5WriteEb(param_2,(char)puVar4[6]);
  uVar6 = uVar6 + 1;
  iVar2 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1);
  puVar9 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
  if ((uint)(piVar7[4] - piVar7[3] >> 2) < uVar6) goto code_r0x003f347c;
  iVar3 = *piVar7;
  iVar2 = iVar2 - (int)puVar9;
  goto LAB_003f33b4;
code_r0x003f347c:
  iVar2 = iVar2 - (int)puVar9;
  uVar6 = iVar2 >> 2;
  if (uVar6 <= iVar8 + 1U) {
    return;
  }
LAB_003f3394:
  iVar8 = iVar8 + 1;
  goto LAB_003f3364;
}


