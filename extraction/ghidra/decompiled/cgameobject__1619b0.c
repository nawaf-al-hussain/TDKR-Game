// _Z20VehicleGoToWaypointEP11CGameObjectP15CGameObjectBasef @ 001619b0

void _Z20VehicleGoToWaypointEP11CGameObjectP15CGameObjectBasef
               (int *param_1,int *param_2,undefined4 param_3)

{
  undefined4 *puVar1;
  int iVar2;
  int *piVar3;
  int iVar4;
  int iVar5;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  
  if ((param_2 != (int *)0x0) && (param_1[0x30] != 0)) {
    puVar1 = (undefined4 *)(**(code **)(*param_2 + 0xc))(param_2);
    local_30 = *puVar1;
    local_3c = 0;
    local_38 = 0;
    local_2c = puVar1[1];
    local_34 = 0;
    local_28 = puVar1[2];
    iVar2 = _Z30FindRoadWaypointsFromPositionsP11CGameObjectPN6glitch4core8vector3dIfEEPP11TrafficNodeS8_S8_
                      (param_1,&local_30,&local_3c,&local_38,&local_34);
    if (iVar2 != 0) {
      piVar3 = (int *)(DAT_00161b14 + 0x161a4c);
      iVar2 = _ZN15CTrafficControl19ComputeShortestPathEP11TrafficNodeS1_S1_
                        (*piVar3,local_38,local_3c,local_34);
      if (iVar2 != 0) {
        iVar4 = *piVar3;
        iVar2 = param_1[0x30];
        iVar5 = *(int *)(iVar4 + 0x14c);
        *(int *)(iVar2 + 0x1c) = iVar4;
        *(undefined1 *)(iVar2 + 0xe4) = 1;
        *(undefined1 *)(iVar2 + 0xe5) = 1;
        if (iVar5 == 0) {
          *(undefined4 *)(iVar4 + 0x14c) = 1;
          piVar3 = (int *)_Znwj(0xc);
          *piVar3 = (int)param_1;
          piVar3[1] = 0;
          piVar3[2] = 0;
          *(int **)(iVar4 + 0x148) = piVar3;
          *(int **)(iVar4 + 0x144) = piVar3;
        }
        else {
          *(int *)(iVar4 + 0x14c) = iVar5 + 1;
          piVar3 = (int *)_Znwj(0xc);
          iVar2 = *(int *)(iVar4 + 0x148);
          piVar3[2] = 0;
          *piVar3 = (int)param_1;
          piVar3[1] = iVar2;
          *(int **)(iVar2 + 8) = piVar3;
          *(int **)(iVar4 + 0x148) = piVar3;
        }
        puVar1 = (undefined4 *)(**(code **)(*param_1 + 0x18))(param_1);
        local_24 = *puVar1;
        local_20 = puVar1[1];
        local_1c = puVar1[2];
        _ZN13CVehicleLogic8Nav_InitEP11TrafficNodeS1_RN6glitch4core8vector3dIfEEf
                  (param_1[0x30],local_3c,local_38,&local_24,param_3);
      }
    }
  }
  return;
}

