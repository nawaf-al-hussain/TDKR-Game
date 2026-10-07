// _Z16CNPCAttackTargetP11CGameObjectS0_ @ 00177e9c

void _Z16CNPCAttackTargetP11CGameObjectS0_(int param_1,int param_2)

{
  int iVar1;
  
  if (param_1 == 0) {
    return;
  }
  iVar1 = _ZNK11CGameObject6IsDeadEv();
  if (iVar1 != 0) {
    return;
  }
  if (*(int *)(param_1 + 0xbc) == 0) {
    return;
  }
  iVar1 = _ZNK11CGameObject8IsCowardEv(param_1);
  if (iVar1 != 0) {
    return;
  }
  if (param_2 == 0) {
    return;
  }
  iVar1 = _ZNK11CGameObject13IsInStateTypeEib(param_1,0x11800);
  if (iVar1 != 0) {
    return;
  }
  iVar1 = _ZN11CGameObject11IsAttackingEPS_b(param_1,param_2);
  if (iVar1 != 0) {
    return;
  }
  _ZN19CAwarenessComponent16SetCurrentTargetEP11CGameObject(*(undefined4 *)(param_1 + 0xac),param_2)
  ;
  if (*(char *)(param_2 + 0xed) != '\0') {
    _ZN15CNpcAIComponent8SetEnemyEb(*(undefined4 *)(param_1 + 0xbc),1);
    _ZN15CNpcAIComponent9SetStanceEi(*(undefined4 *)(param_1 + 0xbc),2);
  }
  iVar1 = _ZNK11CGameObject13IsInStateTypeEib(param_1,0x80,0);
  if (iVar1 != 0) {
    return;
  }
  _ZN15CNpcAIComponent15StartCatchEnemyEv(*(undefined4 *)(param_1 + 0xbc));
  return;
}

