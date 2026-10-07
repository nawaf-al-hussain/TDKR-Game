// _Z13CNPCGetStanceP11CGameObjectP15CWayPointObject @ 00177e58

undefined4 _Z13CNPCGetStanceP11CGameObjectP15CWayPointObject(int param_1,int param_2)

{
  if ((param_1 == 0) && ((param_2 == 0 || (param_1 = *(int *)(param_2 + 0x74), param_1 == 0)))) {
    return 0xffffffff;
  }
  if (*(int *)(param_1 + 0xbc) == 0) {
    return 0xffffffff;
  }
  return *(undefined4 *)(*(int *)(param_1 + 0xbc) + 0x44);
}

