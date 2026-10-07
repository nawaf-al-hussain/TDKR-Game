// _Z22CActorGetMoveStateTypeP11CGameObject @ 001789dc

undefined4 _Z22CActorGetMoveStateTypeP11CGameObject(int param_1)

{
  undefined4 uVar1;
  
  if (*(int *)(param_1 + 0xb4) != 0) {
    uVar1 = _ZN18CStateSetComponent16GetMoveStateTypeEv();
    return uVar1;
  }
  return 0xffffffff;
}

