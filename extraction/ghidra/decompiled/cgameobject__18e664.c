// _ZN13CAIController24GetCombatBatarangTargetsERSt6vectorIP11CGameObjectSaIS2_EERKN6glitch4core8vector3dIfEEff @ 0018e664

void _ZN13CAIController24GetCombatBatarangTargetsERSt6vectorIP11CGameObjectSaIS2_EERKN6glitch4core8vector3dIfEEff
               (int param_1,int param_2,undefined4 param_3,float param_4,float param_5)

{
  float fVar1;
  float fVar2;
  int iVar3;
  float extraout_r0;
  int iVar4;
  undefined4 *puVar5;
  int iVar6;
  int iVar7;
  int *piVar8;
  undefined8 uVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  
  fVar2 = DAT_0018e848;
  fVar1 = DAT_0018e844;
  iVar4 = *(int *)(param_1 + 0x16c);
  iVar3 = *(int *)(param_1 + 0x168);
  if ((uint)(iVar4 - iVar3) >> 2 == 0) {
    return;
  }
  iVar6 = 0;
  iVar7 = -1;
  fVar12 = DAT_0018e840;
  do {
    piVar8 = *(int **)(iVar3 + iVar6 * 4);
    if (piVar8 == (int *)0x0) {
LAB_0018e7b4:
      if ((uint)(iVar4 - iVar3 >> 2) <= iVar6 + 1U) goto LAB_0018e7f8;
    }
    else {
      (**(code **)(*piVar8 + 0x18))(piVar8);
      uVar9 = (**(code **)(*piVar8 + 0x18))(piVar8);
      atan2f((float)uVar9,(float)((ulonglong)uVar9 >> 0x20));
      for (fVar11 = (extraout_r0 + fVar1) * DAT_0018e84c; fVar2 <= fVar11; fVar11 = fVar11 - fVar2)
      {
      }
      for (; fVar10 = param_4, fVar11 < 0.0; fVar11 = fVar11 + fVar2) {
      }
      for (; fVar2 <= fVar10; fVar10 = fVar10 - fVar2) {
      }
      for (; fVar10 < 0.0; fVar10 = fVar10 + fVar2) {
      }
      fVar11 = ABS(fVar11 - fVar10);
      if (DAT_0018e850 < fVar11) {
        fVar11 = fVar2 - fVar11;
      }
      if (param_5 * 0.5 <= fVar11) {
        iVar4 = *(int *)(param_1 + 0x16c);
        iVar3 = *(int *)(param_1 + 0x168);
        goto LAB_0018e7b4;
      }
      iVar4 = *(int *)(param_1 + 0x16c);
      if (fVar12 <= fVar11) {
        iVar3 = *(int *)(param_1 + 0x168);
        fVar11 = fVar12;
      }
      else {
        iVar3 = *(int *)(param_1 + 0x168);
        iVar7 = iVar6;
      }
      fVar12 = fVar11;
      if ((uint)(iVar4 - iVar3 >> 2) <= iVar6 + 1U) {
LAB_0018e7f8:
        if (iVar7 == -1) {
          return;
        }
        puVar5 = *(undefined4 **)(param_2 + 4);
        if (puVar5 != *(undefined4 **)(param_2 + 8)) {
          iVar4 = 0;
          if (puVar5 != (undefined4 *)0x0) {
            *puVar5 = *(undefined4 *)(iVar3 + iVar7 * 4);
            iVar4 = *(int *)(param_2 + 4);
          }
          *(int *)(param_2 + 4) = iVar4 + 4;
          return;
        }
        _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                  (param_2);
        return;
      }
    }
    iVar6 = iVar6 + 1;
  } while( true );
}

