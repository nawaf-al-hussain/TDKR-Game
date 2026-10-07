// _ZN13CZonesManager14GetZoneFromPosERKN6glitch4core8vector3dIfEE @ 002cda5c

int _ZN13CZonesManager14GetZoneFromPosERKN6glitch4core8vector3dIfEE(int param_1,float *param_2)

{
  int iVar1;
  int *piVar2;
  int *piVar3;
  int *piVar4;
  
  piVar4 = *(int **)(param_1 + 0x80);
  piVar2 = piVar4;
  while (piVar3 = piVar2, piVar2 != *(int **)(param_1 + 0x84)) {
    while( true ) {
      piVar2 = piVar3 + 1;
      iVar1 = *piVar3;
      if ((((*param_2 < *(float *)(iVar1 + 0x19c)) || (*(float *)(iVar1 + 0x1a8) < *param_2)) ||
          (param_2[1] < *(float *)(iVar1 + 0x1a0))) ||
         ((*(float *)(iVar1 + 0x1ac) < param_2[1] || (param_2[2] < *(float *)(iVar1 + 0x1a4)))))
      break;
      if (param_2[2] <= *(float *)(iVar1 + 0x1b0)) {
        return iVar1;
      }
      piVar3 = piVar2;
      if (piVar2 == *(int **)(param_1 + 0x84)) goto LAB_002cdae8;
    }
  }
LAB_002cdae8:
  if ((int)piVar2 - (int)piVar4 >> 2 == 0) {
    iVar1 = 0;
  }
  else {
    iVar1 = *piVar4;
  }
  return iVar1;
}


