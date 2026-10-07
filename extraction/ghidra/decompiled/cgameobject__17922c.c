// _Z19CVehicleDropEnemiesP11CGameObjectP15CGameObjectBasef @ 0017922c

void _Z19CVehicleDropEnemiesP11CGameObjectP15CGameObjectBasef
               (int param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  
  if (param_1 == 0) {
    return;
  }
  iVar1 = _ZNK11CGameObject6IsDeadEv();
  if (iVar1 != 0) {
    return;
  }
  if (*(int *)(param_1 + 0xbc) == 0) {
    return;
  }
  if (*(char *)(*(int *)(param_1 + 0xbc) + 0xd) == '\0') {
    return;
  }
  *(undefined4 *)(*(int *)(param_1 + 0xc0) + 0x34) = 1;
  _Z20VehicleGoToWaypointEP11CGameObjectP15CGameObjectBasef(param_1,param_2,param_3);
  return;
}

