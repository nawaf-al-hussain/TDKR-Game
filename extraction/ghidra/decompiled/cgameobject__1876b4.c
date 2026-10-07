// _ZN13CAIController15UnregisterEnemyEP11CGameObject @ 001876b4

void _ZN13CAIController15UnregisterEnemyEP11CGameObject(int param_1,int *param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  int *local_1c [2];
  int *local_14;
  
  iVar2 = param_1 + 0xb0;
  iVar1 = *(int *)(param_1 + 0xb4);
  iVar3 = iVar2;
  while (iVar1 != 0) {
    if (*(int **)(iVar1 + 0x10) < param_2) {
      iVar1 = *(int *)(iVar1 + 0xc);
    }
    else {
      iVar1 = *(int *)(iVar1 + 8);
      iVar3 = iVar1;
    }
  }
  iVar1 = iVar2;
  if ((iVar2 != iVar3) && (*(int **)(iVar3 + 0x10) <= param_2)) {
    iVar1 = iVar3;
  }
  local_1c[0] = param_2;
  if (iVar2 == iVar1) {
    (**(code **)(*param_2 + 0x14))();
  }
  else {
    _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE5eraseERKS1_(param_1 + 0xac,local_1c);
    iVar2 = param_1 + 0xf8;
    iVar1 = iVar2;
    iVar3 = *(int *)(param_1 + 0xfc);
    while (iVar3 != 0) {
      if (*(int **)(iVar3 + 0x10) < local_1c[0]) {
        iVar3 = *(int *)(iVar3 + 0xc);
      }
      else {
        iVar1 = iVar3;
        iVar3 = *(int *)(iVar3 + 8);
      }
    }
    if ((iVar2 != iVar1) && (local_1c[0] < *(int **)(iVar1 + 0x10))) {
      iVar1 = iVar2;
    }
    if (iVar2 != iVar1) {
      local_14 = local_1c[0];
      _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE5eraseERKS1_(param_1 + 0xf4);
      if ((local_14[0x2b] != 0) && (*(int *)(local_14[0x2b] + 0x18) == 3)) {
        for (puVar4 = *(undefined4 **)(param_1 + 0x124); puVar4 != (undefined4 *)(param_1 + 0x124);
            puVar4 = (undefined4 *)*puVar4) {
          if (local_14 == (int *)puVar4[5]) {
            _ZNSt8__detail15_List_node_base9_M_unhookEv(puVar4);
            _ZdlPv(puVar4);
            *(int *)(param_1 + 0x110) = *(int *)(param_1 + 0x110) + -1;
            break;
          }
        }
      }
      _ZN11CGameObject13SetAwareStateEi(local_14,0);
      (**(code **)(*local_14 + 0x14))();
    }
    if (*(int **)(param_1 + 0x114) == local_1c[0]) {
      *(undefined4 *)(param_1 + 0x114) = 0;
    }
    (**(code **)(*local_1c[0] + 0x14))(local_1c[0]);
  }
  return;
}

