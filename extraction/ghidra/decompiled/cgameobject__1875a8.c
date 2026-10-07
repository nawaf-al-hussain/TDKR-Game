// _ZN13CAIController13RegisterEnemyEP11CGameObject @ 001875a8

void _ZN13CAIController13RegisterEnemyEP11CGameObject(int param_1,int *param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int *local_14;
  undefined1 auStack_10 [8];
  
  local_14 = param_2;
  iVar2 = _ZN11CGameObject9IsVehicleEv(param_2);
  if (iVar2 == 0) {
    iVar3 = param_1 + 0xb0;
    iVar2 = *(int *)(param_1 + 0xb4);
    iVar1 = iVar3;
    while (iVar2 != 0) {
      if (*(int **)(iVar2 + 0x10) < local_14) {
        iVar2 = *(int *)(iVar2 + 0xc);
      }
      else {
        iVar2 = *(int *)(iVar2 + 8);
        iVar1 = iVar2;
      }
    }
    iVar2 = iVar3;
    if ((iVar3 != iVar1) && (*(int **)(iVar1 + 0x10) <= local_14)) {
      iVar2 = iVar1;
    }
    if (iVar3 == iVar2) {
      _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE6insertERKS1_(auStack_10,param_1 + 0xac,&local_14)
      ;
    }
    (**(code **)(*local_14 + 0x14))();
  }
  return;
}

