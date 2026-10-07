// _ZN11Application24SendTrackingEventCollectEii @ 003f02d0

void _ZN11Application24SendTrackingEventCollectEii(undefined4 param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  
  if (param_2 == 0x268a) {
    iVar3 = 0x8aaf;
  }
  else {
    if (param_2 < 0x268b) {
      if (param_2 == 0x2689) {
        iVar3 = 0;
        iVar5 = 0;
        iVar1 = 0;
        iVar4 = param_3;
        param_3 = 0;
        goto LAB_003f0420;
      }
LAB_003f03f4:
      switch(param_2) {
      case 0x4c764:
        iVar3 = 0x8b15;
        iVar4 = 0;
        iVar5 = 0x8b15;
        iVar1 = 0;
        break;
      case 0x4c765:
        iVar3 = 0x8b18;
        iVar4 = 0;
        iVar5 = 0x8b18;
        iVar1 = 0;
        break;
      case 0x4c766:
        iVar3 = 0x8b17;
        iVar4 = 0;
        iVar5 = 0x8b17;
        iVar1 = 0;
        break;
      case 0x4c767:
        iVar3 = 0x8b19;
        iVar4 = 0;
        iVar5 = 0x8b19;
        iVar1 = 0;
        break;
      default:
        iVar3 = 0;
        iVar1 = 0;
        iVar5 = 0;
        iVar4 = iVar3;
      }
      goto LAB_003f0420;
    }
    if (param_2 == 0x61a83) {
      iVar3 = 0x8aad;
    }
    else {
      if (param_2 != 0x61a85) goto LAB_003f03f4;
      iVar3 = 0x8aae;
    }
  }
  iVar1 = _ZN6CLevel8GetLevelEv();
  if ((iVar1 != 0) && (iVar1 = _ZN6CLevel8GetLevelEv(), *(int *)(iVar1 + 0xec) != 0)) {
    _ZN6CLevel8GetLevelEv();
    iVar1 = _ZNK6CLevel18GetPlayerComponentEv();
    if (iVar1 != 0) {
      _ZN6CLevel8GetLevelEv();
      iVar1 = _ZNK6CLevel18GetPlayerInventoryEv();
      if (iVar1 != 0) {
        _ZN6CLevel8GetLevelEv();
        uVar2 = _ZNK6CLevel18GetPlayerInventoryEv();
        iVar1 = _ZN10CInventory12GetItemCountEi(uVar2,param_2);
        uVar2 = _ZN4glot15TrackingManager11GetInstanceEv();
        _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                  (uVar2,0x8a6f,0,iVar3,iVar1,0,0,0,0,0);
        if (iVar3 == 0 || iVar1 != 0x1e) {
          return;
        }
        uVar2 = _ZN4glot15TrackingManager11GetInstanceEv();
        _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                  (uVar2,0x903a,0,iVar3,1000,0,0,0,0,0);
        return;
      }
    }
  }
  iVar5 = 0;
  iVar1 = iVar3;
  iVar4 = iVar5;
LAB_003f0420:
  if (iVar3 == 0) {
    uVar2 = _ZN4glot15TrackingManager11GetInstanceEv();
    _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
              (uVar2,0x8a6f,0,0,0,0,0,iVar4,0,0);
  }
  else {
    uVar2 = _ZN4glot15TrackingManager11GetInstanceEv();
    _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
              (uVar2,0x8a6f,0,iVar1,0,iVar5,param_3,0,0,0);
  }
  return;
}


