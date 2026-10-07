// _ZN13CQuestManager13AddLevelQuestEP11CGameObject @ 00191ba8

void _ZN13CQuestManager13AddLevelQuestEP11CGameObject(int param_1,undefined4 param_2)

{
  undefined4 *puVar1;
  int iVar2;
  undefined4 local_c [2];
  
  puVar1 = *(undefined4 **)(param_1 + 0xe4);
  if (puVar1 == *(undefined4 **)(param_1 + 0xe8)) {
    local_c[0] = param_2;
    _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
              (param_1 + 0xe0,puVar1,local_c);
  }
  else {
    iVar2 = 0;
    if (puVar1 != (undefined4 *)0x0) {
      *puVar1 = param_2;
      iVar2 = *(int *)(param_1 + 0xe4);
    }
    *(int *)(param_1 + 0xe4) = iVar2 + 4;
  }
  return;
}

