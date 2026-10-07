// _ZN13CAIController19Alliance_UnregisterEP11CGameObject11AI_ALLIANCE @ 00188540

void _ZN13CAIController19Alliance_UnregisterEP11CGameObject11AI_ALLIANCE
               (int param_1,undefined4 param_2,uint param_3)

{
  if ((param_3 & 1) == 0) {
    if ((param_3 & 2) != 0) {
      _ZN13CAIController24Alliance_UnregisterEnemyEP11CGameObject();
    }
  }
  else {
    _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE5eraseERKS1_(param_1 + 0xdc);
  }
  return;
}

