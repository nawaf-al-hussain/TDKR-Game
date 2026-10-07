// _Z14CNPCIsInStanceP11CGameObjectP15CWayPointObjecti @ 00177f80

bool _Z14CNPCIsInStanceP11CGameObjectP15CWayPointObjecti(int param_1,int param_2,int param_3)

{
  if ((param_1 != 0) && (*(int *)(param_1 + 0xbc) != 0)) {
    return param_3 == *(int *)(*(int *)(param_1 + 0xbc) + 0x44);
  }
  if (param_2 == 0) {
    return false;
  }
  if ((*(int *)(param_2 + 0x74) != 0) && (*(int *)(*(int *)(param_2 + 0x74) + 0xbc) != 0)) {
    return param_3 == *(int *)(*(int *)(param_1 + 0xbc) + 0x44);
  }
  return false;
}

