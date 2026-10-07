// _ZN13CAIController18GetOnScreenEnemiesERSt6vectorIP11CGameObjectSaIS2_EE @ 00189704

void _ZN13CAIController18GetOnScreenEnemiesERSt6vectorIP11CGameObjectSaIS2_EE
               (int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  int iVar3;
  
  for (iVar3 = *(int *)(param_1 + 0xa0); param_1 + 0x98 != iVar3;
      iVar3 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar3)) {
    puVar2 = *(undefined4 **)(param_2 + 4);
    if (puVar2 == *(undefined4 **)(param_2 + 8)) {
      _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                (param_2,puVar2,iVar3 + 0x10);
    }
    else {
      iVar1 = 0;
      if (puVar2 != (undefined4 *)0x0) {
        *puVar2 = *(undefined4 *)(iVar3 + 0x10);
        iVar1 = *(int *)(param_2 + 4);
      }
      *(int *)(param_2 + 4) = iVar1 + 4;
    }
  }
  return;
}

