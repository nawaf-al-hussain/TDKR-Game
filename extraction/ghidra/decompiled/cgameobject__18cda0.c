// _ZN13CAIController15HasEnemiesAwareEP11CGameObject @ 0018cda0

bool _ZN13CAIController15HasEnemiesAwareEP11CGameObject(int param_1,int param_2)

{
  if (param_2 == 0) {
    return false;
  }
  if (*(char *)(param_2 + 0xed) == '\0') {
    return false;
  }
  return *(int *)(param_1 + 0x108) != 0;
}

