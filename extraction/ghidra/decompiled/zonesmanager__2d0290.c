// _ZN13CZonesManager17GetZoneByWorldBoxEN6glitch4core8vector3dIfEEP5CZone @ 002d0290

int _ZN13CZonesManager17GetZoneByWorldBoxEN6glitch4core8vector3dIfEEP5CZone
              (int param_1,float *param_2,int param_3)

{
  float *pfVar1;
  int iVar2;
  int iVar3;
  float *pfVar4;
  int *piVar5;
  int *piVar6;
  float *pfVar7;
  int *piVar8;
  int iVar9;
  
  piVar8 = *(int **)(param_1 + 0x80);
  pfVar1 = (float *)0x0;
  iVar2 = 0;
LAB_002d02ac:
  do {
    iVar9 = iVar2;
    pfVar7 = pfVar1;
    piVar5 = piVar8;
    if (*(int **)(param_1 + 0x84) == piVar8) {
      return iVar9;
    }
    while( true ) {
      piVar8 = piVar5 + 1;
      iVar3 = (**(code **)(*(int *)*piVar5 + 0x54))();
      pfVar1 = pfVar7;
      iVar2 = iVar9;
      if (iVar3 == 0) break;
      iVar3 = *piVar5;
      piVar5 = *(int **)(iVar3 + 0x184);
      do {
        if (piVar5 == *(int **)(iVar3 + 0x188)) goto LAB_002d02ac;
        piVar6 = piVar5 + 1;
        pfVar4 = (float *)*piVar5;
        piVar5 = piVar6;
      } while (((((*param_2 < *pfVar4) || (pfVar4[3] < *param_2)) || (param_2[1] < pfVar4[1])) ||
               ((pfVar4[4] < param_2[1] || (param_2[2] < pfVar4[2])))) || (pfVar4[5] < param_2[2]));
      pfVar1 = pfVar4;
      iVar2 = iVar3;
      if (((pfVar7 == (float *)0x0) || ((int)pfVar7[6] < (int)pfVar4[6])) ||
         (pfVar1 = pfVar7, iVar2 = iVar9, pfVar4[6] != pfVar7[6])) break;
      if (iVar3 == param_3) {
        iVar9 = param_3;
        pfVar7 = pfVar4;
      }
      piVar5 = piVar8;
      if (*(int **)(param_1 + 0x84) == piVar8) {
        return iVar9;
      }
    }
  } while( true );
}


