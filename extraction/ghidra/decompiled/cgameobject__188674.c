// _ZN13CAIController24Alliance_UnregisterEnemyEP11CGameObject @ 00188674

void _ZN13CAIController24Alliance_UnregisterEnemyEP11CGameObject(int param_1,int *param_2)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  int *local_24 [2];
  int *local_1c;
  
  puVar1 = (undefined4 *)(param_1 + 0x124);
  for (puVar2 = (undefined4 *)*puVar1; local_24[0] = param_2, puVar2 != puVar1;
      puVar2 = (undefined4 *)*puVar2) {
    if (param_2 == (int *)puVar2[5]) {
      _ZNSt8__detail15_List_node_base9_M_unhookEv(puVar2);
      _ZdlPv(puVar2);
      *(int *)(param_1 + 0x110) = *(int *)(param_1 + 0x110) + -1;
      break;
    }
  }
  if ((param_2[0x2b] != 0) && (*(int *)(param_2[0x2b] + 0x18) == 3)) {
    _ZN11CGameObject13SetAwareStateEi(param_2,2);
  }
  local_1c = local_24[0];
  if (local_24[0] == *(int **)(param_1 + 0x114)) {
    *(undefined4 *)(param_1 + 0x114) = 0;
  }
  _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE5eraseERKS1_(param_1 + 0xf4);
  if ((local_1c[0x2b] != 0) && (*(int *)(local_1c[0x2b] + 0x18) == 3)) {
    for (puVar2 = *(undefined4 **)(param_1 + 0x124); puVar1 != puVar2;
        puVar2 = (undefined4 *)*puVar2) {
      if (local_1c == (int *)puVar2[5]) {
        _ZNSt8__detail15_List_node_base9_M_unhookEv(puVar2);
        _ZdlPv(puVar2);
        *(int *)(param_1 + 0x110) = *(int *)(param_1 + 0x110) + -1;
        break;
      }
    }
  }
  _ZN11CGameObject13SetAwareStateEi(local_1c,0);
  (**(code **)(*local_1c + 0x14))();
  if (local_24[0][0x2b] != 0) {
    _ZN19CAwarenessComponent11ClearStatesEv();
  }
  _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE5eraseERKS1_(param_1 + 0xac,local_24);
  _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE5eraseERKS1_(param_1 + 0xc4,local_24);
  _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE5eraseERKS1_(param_1 + 0xf4,local_24);
  _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE5eraseERKS1_(param_1 + 0x94,local_24);
  return;
}

