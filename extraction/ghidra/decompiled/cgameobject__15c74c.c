// _Z25FindClosestWaypointOnPathP15CGameObjectBaseP15CWayPointObject @ 0015c74c

int * _Z25FindClosestWaypointOnPathP15CGameObjectBaseP15CWayPointObject(int *param_1,int *param_2)

{
  undefined8 uVar1;
  float *pfVar2;
  float *pfVar3;
  int iVar4;
  int *piVar5;
  undefined8 *puVar6;
  int *piVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  float local_3c;
  float local_38;
  float local_34;
  
  pfVar2 = (float *)(**(code **)(*param_2 + 0xc))(param_2);
  pfVar3 = (float *)(**(code **)(*param_1 + 0xc))(param_1);
  fVar8 = *pfVar2;
  fVar10 = pfVar2[1];
  fVar12 = pfVar2[2];
  fVar9 = *pfVar3;
  fVar11 = pfVar3[1];
  fVar13 = pfVar3[2];
  iVar4 = _ZN15CWayPointObject11GetNumLinksEv(param_2);
  piVar7 = param_2;
  if (iVar4 < 2) {
    piVar5 = (int *)_ZN15CWayPointObject7GetNextEv(param_2);
    fVar8 = (fVar8 - fVar9) * (fVar8 - fVar9) + (fVar10 - fVar11) * (fVar10 - fVar11) +
            (fVar12 - fVar13) * (fVar12 - fVar13);
    do {
      if (piVar5 == param_2 || piVar5 == (int *)0x0) break;
      pfVar2 = (float *)(**(code **)(*piVar5 + 0xc))(piVar5);
      pfVar3 = (float *)(**(code **)(*param_1 + 0xc))(param_1);
      fVar9 = (*pfVar2 - *pfVar3) * (*pfVar2 - *pfVar3) +
              (pfVar2[1] - pfVar3[1]) * (pfVar2[1] - pfVar3[1]) +
              (pfVar2[2] - pfVar3[2]) * (pfVar2[2] - pfVar3[2]);
      if (((fVar9 < fVar8) && (iVar4 = (**(code **)(*piVar5 + 8))(piVar5), iVar4 != 0)) &&
         (piVar5[0x1d] == 0)) {
        piVar7 = piVar5;
        fVar8 = fVar9;
      }
      piVar5 = (int *)_ZN15CWayPointObject7GetNextEv(piVar5);
    } while ((piVar5 == (int *)0x0) || (iVar4 = _ZN15CWayPointObject11GetNumLinksEv(), iVar4 < 2));
  }
  piVar5 = (int *)_ZN15CWayPointObject7GetNextEv(piVar7);
  if (piVar5 != (int *)0x0) {
    puVar6 = (undefined8 *)(**(code **)(*piVar5 + 0xc))();
    pfVar2 = (float *)(**(code **)(*param_1 + 0xc))(param_1);
    uVar1 = *puVar6;
    fVar12 = *(float *)(puVar6 + 1);
    fVar9 = *pfVar2;
    fVar8 = pfVar2[1];
    fVar10 = pfVar2[2];
    pfVar2 = (float *)(**(code **)(*piVar5 + 0xc))(piVar5);
    pfVar3 = (float *)(**(code **)(*piVar7 + 0xc))(piVar7);
    local_3c = *pfVar2 - *pfVar3;
    fVar11 = ((float)uVar1 - fVar9) * local_3c;
    local_38 = pfVar2[1] - pfVar3[1];
    fVar8 = ((float)((ulonglong)uVar1 >> 0x20) - fVar8) * local_38;
    local_34 = pfVar2[2] - pfVar3[2];
    fVar9 = (fVar12 - fVar10) * local_34;
    fVar10 = (float)_ZNK6glitch4core8vector3dIfE9getLengthEv(&local_3c);
    if ((fVar11 + fVar8 + fVar9) / fVar10 < fVar10) {
      piVar7 = piVar5;
    }
  }
  return piVar7;
}

