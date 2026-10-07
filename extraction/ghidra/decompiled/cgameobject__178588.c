// _Z17CNPCSetAIBehaviorP11CGameObjecti @ 00178588

void _Z17CNPCSetAIBehaviorP11CGameObjecti(int *param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  
  if ((param_1 == (int *)0x0) || (iVar1 = param_1[0x2f], iVar1 == 0)) {
    uVar2 = _ZN6CLevel8GetLevelEv();
    uVar3 = (**(code **)(*param_1 + 0x14))(param_1);
    iVar1 = _ZN6CLevel19FindWayPointInRoomsEi(uVar2,uVar3);
    if (iVar1 != 0) {
      param_1 = *(int **)(iVar1 + 0x74);
    }
    if (param_1 == (int *)0x0) {
      return;
    }
    iVar1 = param_1[0x2f];
    if (iVar1 == 0) {
      return;
    }
  }
  _ZN15CNpcAIComponent14NPCBehaviorSetEi(iVar1,param_2);
  return;
}

