// _Z14CIsStaticActorP11CGameObject @ 00179954

bool _Z14CIsStaticActorP11CGameObject(int param_1)

{
  if (*(int *)(param_1 + 0xbc) != 0) {
    return false;
  }
  if (*(int *)(param_1 + 0xb0) == 0) {
    return *(int *)(param_1 + 0xe4) != 0xc38e && *(int *)(param_1 + 0xe4) != 0x9c44;
  }
  return false;
}

