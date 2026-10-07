// _ZN11Application24GetMissionFromLevelIndexEi @ 003ed224

uint * _ZN11Application24GetMissionFromLevelIndexEi(int param_1,uint param_2)

{
  uint uVar1;
  int iVar2;
  uint *puVar3;
  uint *puVar4;
  uint *puVar5;
  uint uVar6;
  uint uVar7;
  int iVar8;
  int *piVar9;
  undefined4 *puVar10;
  uint uVar11;
  uint uVar12;
  
  puVar10 = *(undefined4 **)((int)&__DT_SYMTAB[0x1e8].st_value + param_1);
  uVar1 = *(int *)((int)&__DT_SYMTAB[0x1e8].st_size + param_1) - (int)puVar10 >> 2;
  if (1 < uVar1) {
    puVar5 = (uint *)*puVar10;
    uVar11 = 1;
    do {
      puVar4 = puVar5;
      if (uVar11 != *puVar5) {
        uVar6 = 0;
        do {
          uVar6 = uVar6 + 1;
          if (uVar6 == uVar1) {
            puVar4 = (uint *)0x0;
            break;
          }
          puVar4 = (uint *)puVar10[uVar6];
        } while (uVar11 != *(uint *)puVar10[uVar6]);
      }
      uVar6 = (int)(puVar4[4] - puVar4[3]) >> 2;
      if (uVar6 != 0) {
        uVar12 = 1;
        do {
          puVar3 = puVar5;
          if (*puVar4 != *puVar5) {
            uVar7 = 0;
            do {
              uVar7 = uVar7 + 1;
              if (uVar1 == uVar7) {
                puVar3 = (uint *)0x0;
                break;
              }
              puVar3 = (uint *)puVar10[uVar7];
            } while (*puVar4 != *(uint *)puVar10[uVar7]);
          }
          piVar9 = (int *)puVar3[3];
          iVar2 = (int)(puVar3[4] - (int)piVar9) >> 2;
          if (iVar2 == 0) {
            puVar3 = (uint *)0x0;
          }
          else {
            puVar3 = (uint *)*piVar9;
            if (uVar12 != *puVar3) {
              iVar8 = 0;
              do {
                iVar8 = iVar8 + 1;
                if (iVar8 == iVar2) {
                  puVar3 = (uint *)0x0;
                  break;
                }
                puVar3 = (uint *)piVar9[iVar8];
              } while (uVar12 != *puVar3);
            }
          }
          if (puVar3[1] == param_2) {
            return puVar3;
          }
          uVar12 = uVar12 + 1;
        } while (uVar12 <= uVar6);
      }
      uVar11 = uVar11 + 1;
    } while (uVar11 != uVar1);
  }
  return (uint *)0x0;
}


