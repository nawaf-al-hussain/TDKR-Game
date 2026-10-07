// _ZN13CAIController21Alliance_EnemyClosestEPP11CGameObjectS1_ @ 00188c84

void _ZN13CAIController21Alliance_EnemyClosestEPP11CGameObjectS1_
               (undefined4 param_1,undefined4 param_2,int param_3)

{
  if (*(int *)(param_3 + 0xbc) == 0) {
    return;
  }
  _ZN13CAIController16Alliance_ClosestEPP11CGameObject11AI_ALLIANCES1_
            (param_1,param_2,*(undefined4 *)(*(int *)(param_3 + 0xbc) + 0x27c),param_3);
  return;
}

