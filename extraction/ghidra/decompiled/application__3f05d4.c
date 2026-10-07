// _ZN11Application30SendTrackingEventItemPurchasedEiii @ 003f05d4

void _ZN11Application30SendTrackingEventItemPurchasedEiii
               (undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int *piVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  int local_1c [2];
  
  local_1c[0] = 0;
  piVar1 = (int *)_ZN12gxStateStack12CurrentStateEv(**(int **)(DAT_003f0690 + 0x3f05e4) + 4);
  iVar2 = (**(code **)(*piVar1 + 8))(piVar1,2);
  if (iVar2 == 0) {
    uVar4 = 0x8c27;
  }
  else if (**(int **)(DAT_003f0694 + 0x3f062c) == 0) {
    uVar4 = 0x8c26;
  }
  else {
    uVar4 = 0x8c26;
    iVar2 = _ZNK13CQuestManager20GetCrtMainStoryQuestEPi
                      (**(int **)(DAT_003f0694 + 0x3f062c),local_1c);
    if (iVar2 != -1) {
      local_1c[0] = local_1c[0] + 0x8a8e;
    }
  }
  uVar3 = _ZN4glot15TrackingManager11GetInstanceEv();
  _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
            (uVar3,0x8009,0,param_2,param_3,uVar4,local_1c[0],param_4,0,0);
  return;
}


