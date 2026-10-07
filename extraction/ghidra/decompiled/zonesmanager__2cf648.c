// _ZN13CZonesManager15GetClosestActorEiRfi @ 002cf648

undefined4
_ZN13CZonesManager15GetClosestActorEiRfi(int param_1,undefined4 param_2,float *param_3,int param_4)

{
  int iVar1;
  int *piVar2;
  float *pfVar3;
  int iVar4;
  int iVar5;
  undefined4 uVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  float fVar13;
  
  piVar2 = (int *)_ZN13CZonesManager10FindObjectEit(param_1,param_2,0xffff);
  if (piVar2 == (int *)0x0) {
    uVar6 = 0xffffffff;
  }
  else {
    pfVar3 = (float *)(**(code **)(*piVar2 + 0x18))();
    iVar4 = *(int *)(param_1 + 0x54);
    iVar1 = *(int *)(param_1 + 0x58) - iVar4 >> 2;
    fVar13 = *pfVar3;
    fVar12 = pfVar3[1];
    fVar11 = pfVar3[2];
    if (iVar1 < 1) {
      uVar6 = 0xffffffff;
      *param_3 = DAT_002cf850;
    }
    else {
      fVar10 = DAT_002cf84c;
      if (param_4 < 0) {
        iVar5 = 0;
        uVar6 = 0xffffffff;
        while( true ) {
          piVar2 = *(int **)(iVar4 + iVar5 * 4);
          if (((piVar2[0x2f] != 0) || (piVar2[0x2c] != 0)) ||
             (piVar2[0x39] == 0xc38e || piVar2[0x39] == 0x9c44)) {
            pfVar3 = (float *)(**(code **)(*piVar2 + 0x18))(piVar2);
            fVar9 = fVar13 - *pfVar3;
            fVar7 = fVar12 - pfVar3[1];
            fVar8 = fVar11 - pfVar3[2];
            fVar7 = fVar9 * fVar9 + fVar7 * fVar7 + fVar8 * fVar8;
            if (fVar7 < fVar10) {
              uVar6 = (**(code **)(*piVar2 + 0x14))(piVar2);
              fVar10 = fVar7;
            }
          }
          iVar5 = iVar5 + 1;
          if (iVar5 == iVar1) break;
          iVar4 = *(int *)(param_1 + 0x54);
        }
      }
      else {
        iVar5 = 0;
        uVar6 = 0xffffffff;
        while( true ) {
          piVar2 = *(int **)(iVar4 + iVar5 * 4);
          if ((((piVar2[0x2f] != 0) || (piVar2[0x2c] != 0)) ||
              (piVar2[0x39] == 0xc38e || piVar2[0x39] == 0x9c44)) &&
             (iVar4 = _ZN11CGameObject13GetAIBehaviorEv(piVar2), iVar4 == param_4)) {
            pfVar3 = (float *)(**(code **)(*piVar2 + 0x18))(piVar2);
            fVar9 = fVar13 - *pfVar3;
            fVar7 = fVar12 - pfVar3[1];
            fVar8 = fVar11 - pfVar3[2];
            fVar7 = fVar9 * fVar9 + fVar7 * fVar7 + fVar8 * fVar8;
            if (fVar7 < fVar10) {
              uVar6 = (**(code **)(*piVar2 + 0x14))(piVar2);
              fVar10 = fVar7;
            }
          }
          if (iVar5 + 1 == iVar1) break;
          iVar5 = iVar5 + 1;
          iVar4 = *(int *)(param_1 + 0x54);
        }
      }
      *param_3 = SQRT(fVar10);
    }
  }
  return uVar6;
}


