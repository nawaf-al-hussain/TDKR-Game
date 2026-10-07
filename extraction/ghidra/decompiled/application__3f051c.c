// _ZN11Application33SendTrackingEventLotteryCompletedEiiiii @ 003f051c

void _ZN11Application33SendTrackingEventLotteryCompletedEiiiii
               (undefined4 param_1,undefined4 param_2,int param_3,undefined4 param_4,
               undefined4 param_5,undefined4 param_6)

{
  undefined4 uVar1;
  
  uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
  _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
            (uVar1,0x8a65,0,param_2,param_3,param_4,param_5,param_3 == 0x8be3,param_6,0);
  return;
}


