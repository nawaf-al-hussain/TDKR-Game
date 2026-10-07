// _ZN11Application19LoadCurrentProgressEP13CMemoryStream @ 003f3494

void _ZN11Application19LoadCurrentProgressEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint *puVar6;
  uint uVar7;
  undefined4 *puVar8;
  uint *puVar9;
  undefined1 local_29 [5];
  
  puVar8 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
  iVar2 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) - (int)puVar8;
  uVar5 = iVar2 >> 2;
  if (uVar5 < 2) {
    return;
  }
  uVar7 = 1;
LAB_003f34d4:
  uVar4 = 0;
  do {
    puVar6 = (uint *)puVar8[uVar4];
    uVar4 = uVar4 + 1;
    uVar3 = *puVar6;
    if (uVar7 == uVar3) {
      if (puVar6[4] - puVar6[3] >> 2 != 0) {
        uVar5 = 1;
        goto LAB_003f3528;
      }
      break;
    }
  } while (uVar4 < uVar5);
  goto LAB_003f34f4;
LAB_003f3528:
  if (iVar2 >> 2 == 0) {
    puVar9 = (uint *)0x0;
  }
  else {
    puVar9 = (uint *)*puVar8;
    if (*puVar9 != uVar3) {
      iVar1 = 0;
      do {
        iVar1 = iVar1 + 1;
        if (iVar1 == iVar2 >> 2) {
          puVar9 = (uint *)0x0;
          break;
        }
        puVar9 = (uint *)puVar8[iVar1];
      } while (*puVar9 != uVar3);
    }
  }
  puVar8 = (undefined4 *)puVar9[3];
  iVar2 = (int)(puVar9[4] - (int)puVar8) >> 2;
  if (iVar2 == 0) {
    puVar9 = (uint *)0x0;
  }
  else {
    puVar9 = (uint *)*puVar8;
    if (uVar5 != *puVar9) {
      iVar1 = 0;
      do {
        iVar1 = iVar1 + 1;
        if (iVar1 == iVar2) {
          puVar9 = (uint *)0x0;
          break;
        }
        puVar9 = (uint *)puVar8[iVar1];
      } while (uVar5 != *puVar9);
    }
  }
  _ZN13CMemoryStream8ReadBoolERb(param_2,local_29);
  uVar4 = puVar6[4];
  uVar3 = puVar6[3];
  uVar5 = uVar5 + 1;
  iVar2 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1);
  *(undefined1 *)(puVar9 + 6) = local_29[0];
  puVar8 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
  if ((uint)((int)(uVar4 - uVar3) >> 2) < uVar5) goto code_r0x003f35f8;
  uVar3 = *puVar6;
  iVar2 = iVar2 - (int)puVar8;
  goto LAB_003f3528;
code_r0x003f35f8:
  iVar2 = iVar2 - (int)puVar8;
LAB_003f34f4:
  uVar7 = uVar7 + 1;
  uVar5 = iVar2 >> 2;
  if (uVar5 <= uVar7) {
    return;
  }
  goto LAB_003f34d4;
}


