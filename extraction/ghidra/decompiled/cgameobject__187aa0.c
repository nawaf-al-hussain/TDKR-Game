// _ZN13CAIController16UnsetEnemyActiveEP11CGameObject @ 00187aa0

void _ZN13CAIController16UnsetEnemyActiveEP11CGameObject(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  
  puVar2 = *(undefined4 **)(param_1 + 0x124);
  do {
    if ((undefined4 *)(param_1 + 0x124) == puVar2) {
      iVar1 = *(int *)(param_2 + 0xac);
      if (iVar1 == 0) {
        return;
      }
LAB_00187adc:
      if (*(int *)(iVar1 + 0x18) != 3) {
        return;
      }
      _ZN11CGameObject13SetAwareStateEi(param_2,2);
      return;
    }
    if (puVar2[5] == param_2) {
      _ZNSt8__detail15_List_node_base9_M_unhookEv(puVar2);
      _ZdlPv(puVar2);
      *(int *)(param_1 + 0x110) = *(int *)(param_1 + 0x110) + -1;
      iVar1 = *(int *)(param_2 + 0xac);
      if (iVar1 == 0) {
        return;
      }
      goto LAB_00187adc;
    }
    puVar2 = (undefined4 *)*puVar2;
  } while( true );
}

