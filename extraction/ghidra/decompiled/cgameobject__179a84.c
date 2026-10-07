// _Z17CNPCGetAIBehaviorP11CGameObject @ 00179a84

undefined4 _Z17CNPCGetAIBehaviorP11CGameObject(int *param_1)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  
  if ((param_1 == (int *)0x0) || (param_1[0x2f] == 0)) {
    uVar1 = _ZN6CLevel8GetLevelEv();
    uVar2 = (**(code **)(*param_1 + 0x14))(param_1);
    iVar3 = _ZN6CLevel19FindWayPointInRoomsEi(uVar1,uVar2);
    if (iVar3 != 0) {
      param_1 = *(int **)(iVar3 + 0x74);
    }
    if ((param_1 == (int *)0x0) || (param_1[0x2f] == 0)) {
      return 0xffffffff;
    }
  }
  uVar1 = _ZN15CNpcAIComponent14NPCBehaviorGetEv();
  return uVar1;
}

