// _ZN13CAIController15UnsetEnemyAwareEP11CGameObject @ 001879b8

void _ZN13CAIController15UnsetEnemyAwareEP11CGameObject(int param_1,int *param_2)

{
  undefined4 *puVar1;
  int *local_14 [2];
  
  local_14[0] = param_2;
  _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE5eraseERKS1_(param_1 + 0xf4,local_14);
  if ((local_14[0][0x2b] != 0) && (*(int *)(local_14[0][0x2b] + 0x18) == 3)) {
    for (puVar1 = *(undefined4 **)(param_1 + 0x124); (undefined4 *)(param_1 + 0x124) != puVar1;
        puVar1 = (undefined4 *)*puVar1) {
      if (local_14[0] == (int *)puVar1[5]) {
        _ZNSt8__detail15_List_node_base9_M_unhookEv(puVar1);
        _ZdlPv(puVar1);
        *(int *)(param_1 + 0x110) = *(int *)(param_1 + 0x110) + -1;
        break;
      }
    }
  }
  _ZN11CGameObject13SetAwareStateEi(local_14[0],0);
  (**(code **)(*local_14[0] + 0x14))();
  return;
}

