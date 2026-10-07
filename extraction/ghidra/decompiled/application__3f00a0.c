// _ZN11Application31SendTrackingEventMissionSkippedEif @ 003f00a0

void _ZN11Application31SendTrackingEventMissionSkippedEif
               (int param_1,undefined4 param_2,float param_3)

{
  int iVar1;
  undefined4 uVar2;
  int *piVar3;
  undefined1 *puVar4;
  
  iVar1 = DAT_003f02a8;
  _ZN6CLevel8GetLevelEv();
  piVar3 = *(int **)(iVar1 + 0x3f00c8);
  iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003f02ac + 0x3f00d4));
  if (iVar1 == 0) {
    puVar4 = &DAT_00008c28;
  }
  else {
    _ZN6CLevel8GetLevelEv();
    iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003f02b0 + 0x3f0198));
    if (iVar1 == 0) {
      puVar4 = &DAT_00008c29;
    }
    else {
      _ZN6CLevel8GetLevelEv();
      iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003f02b4 + 0x3f01bc));
      if (iVar1 == 0) {
        puVar4 = &DAT_00008c2a;
      }
      else {
        _ZN6CLevel8GetLevelEv();
        iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003f02b8 + 0x3f01e0));
        if (iVar1 == 0) {
          puVar4 = &DAT_00008c2b;
        }
        else {
          _ZN6CLevel8GetLevelEv();
          iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003f02bc + 0x3f0204));
          if (iVar1 == 0) {
            puVar4 = &DAT_00008c2c;
          }
          else {
            _ZN6CLevel8GetLevelEv();
            iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003f02c0 + 0x3f0228));
            if (iVar1 == 0) {
              puVar4 = &DAT_00008c2d;
            }
            else {
              _ZN6CLevel8GetLevelEv();
              iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003f02c4 + 0x3f024c));
              if (iVar1 == 0) {
                puVar4 = &DAT_00008c2e;
              }
              else {
                _ZN6CLevel8GetLevelEv();
                iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003f02c8 + 0x3f0270));
                if (iVar1 == 0) {
                  puVar4 = &DAT_00008c2f;
                }
                else {
                  _ZN6CLevel8GetLevelEv();
                  puVar4 = (undefined1 *)0x8c30;
                  iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003f02cc + 0x3f0298));
                  if (iVar1 != 0) {
                    puVar4 = (undefined1 *)0x0;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  uVar2 = _ZN4glot15TrackingManager11GetInstanceEv();
  iVar1 = (int)(param_3 * DAT_003f02a4);
  if (iVar1 < 1) {
    iVar1 = 1;
  }
  _ZN4glot15TrackingManager8AddEventIii21TRACKING_MISSION_TYPEiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18_
            (uVar2,0x8a69,0,param_2,0,0x8a7f,puVar4,iVar1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
  *(undefined1 *)((int)&__DT_SYMTAB[0x1ea].st_name + param_1 + 1) = 1;
  return;
}


