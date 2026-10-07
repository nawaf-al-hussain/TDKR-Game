// _ZN11Application17UnlockAllMissionsEb @ 003ecfe0

void _ZN11Application17UnlockAllMissionsEb(int param_1,int param_2)

{
  uint uVar1;
  int iVar2;
  int *piVar3;
  uint *puVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  int iVar8;
  undefined4 *puVar9;
  int iVar10;
  int *piVar11;
  uint uVar12;
  
  piVar11 = *(int **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
  uVar1 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) - (int)piVar11 >> 2;
  if (uVar1 < 2) {
    return;
  }
  iVar10 = 1;
  do {
    if (uVar1 != 0) {
      piVar3 = (int *)*piVar11;
      iVar8 = *piVar3;
      if (iVar10 != iVar8) {
        uVar5 = 0;
        do {
          uVar5 = uVar5 + 1;
          if (uVar5 == uVar1) goto joined_r0x003ed068;
          piVar3 = (int *)piVar11[uVar5];
          iVar8 = *piVar3;
        } while (iVar10 != iVar8);
      }
      uVar5 = piVar3[4] - piVar3[3] >> 2;
      if (uVar5 != 0) {
        uVar12 = 1;
LAB_003ed08c:
        do {
          if (uVar1 == 0) {
            piVar3 = (int *)0x0;
          }
          else {
            piVar3 = (int *)*piVar11;
            if (*piVar3 != iVar8) {
              uVar6 = 0;
              do {
                uVar6 = uVar6 + 1;
                if (uVar6 == uVar1) {
                  piVar3 = (int *)0x0;
                  break;
                }
                piVar3 = (int *)piVar11[uVar6];
              } while (*piVar3 != iVar8);
            }
          }
          puVar9 = (undefined4 *)piVar3[3];
          iVar2 = piVar3[4] - (int)puVar9 >> 2;
          if (iVar2 == 0) {
LAB_003ed118:
            uVar12 = uVar12 + 1;
            if (uVar5 < uVar12) break;
            goto LAB_003ed08c;
          }
          puVar4 = (uint *)*puVar9;
          if (uVar12 != *puVar4) {
            iVar7 = 0;
            do {
              iVar7 = iVar7 + 1;
              if (iVar7 == iVar2) goto LAB_003ed118;
              puVar4 = (uint *)puVar9[iVar7];
            } while (uVar12 != *puVar4);
          }
          if ((param_2 == 0) && (uVar12 == 1 && iVar10 == 1)) goto LAB_003ed118;
          uVar12 = uVar12 + 1;
          *(char *)(puVar4 + 6) = (char)param_2;
        } while (uVar12 <= uVar5);
      }
    }
joined_r0x003ed068:
    if (uVar1 <= iVar10 + 1U) {
      return;
    }
    iVar10 = iVar10 + 1;
  } while( true );
}


