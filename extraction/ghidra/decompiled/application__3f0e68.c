// _ZN11Application21SendTrackingEventDeadEv @ 003f0e68

void _ZN11Application21SendTrackingEventDeadEv(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  uVar2 = 0x8be4;
  if ((*(uint *)(DAT_003f0ecc + 0x3f0e7c) & 0x70) != 0) {
    uVar2 = 0x8be5;
  }
  if ((*(uint *)(DAT_003f0ecc + 0x3f0e7c) & 0x80) != 0) {
    uVar2 = 0x8be6;
  }
  uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
  _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
            (uVar1,0x9329,0,uVar2,0,0,0,0,0,0);
  return;
}


