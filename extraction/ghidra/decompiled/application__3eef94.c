// _ZN11Application23SendTrackingEventLaunchEi @ 003eef94

undefined4 _ZN11Application23SendTrackingEventLaunchEi(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  int iVar3;
  float fVar4;
  float extraout_r0;
  float extraout_r0_00;
  undefined4 uVar5;
  undefined4 uVar6;
  int iVar7;
  float extraout_r0_01;
  undefined4 uVar8;
  uint in_fpscr;
  float __x;
  float __x_00;
  float __x_01;
  undefined1 auStack_68 [60];
  
  if (*(char *)((int)&__DT_SYMTAB[0x1e1].st_value + param_1) == '\0') {
    iVar2 = _ZN6CLevel8GetLevelEv(param_1);
    uVar1 = 0;
    if (iVar2 != 0) {
      iVar2 = _ZN6CLevel8GetLevelEv();
      uVar1 = 0;
      if (*(int *)(iVar2 + 0xec) != 0) {
        _ZN6CLevel8GetLevelEv();
        iVar2 = _ZNK6CLevel18GetPlayerComponentEv();
        uVar1 = 0;
        if (iVar2 != 0) {
          _ZN6CLevel8GetLevelEv();
          iVar3 = _ZNK6CLevel18GetPlayerInventoryEv();
          iVar2 = DAT_003ef2b8;
          uVar1 = 0;
          if (iVar3 != 0) {
            *(undefined1 *)((int)&__DT_SYMTAB[0x1e1].st_value + param_1) = 1;
            if (*(int *)(iVar2 + 0x3ef018) != 0) {
              _ZN13CMemoryStreamC1Ei(auStack_68,0x400);
              iVar2 = _ZN11Application14DecryptAndLoadEPKciP13CMemoryStream
                                (param_1,DAT_003ef2bc + 0x3ef03c,3,auStack_68);
              if (iVar2 == 0) {
                _ZN13CMemoryStreamD2Ev(auStack_68);
              }
              else {
                *(undefined4 *)((int)&__DT_SYMTAB[0x1e0].st_size + param_1) = 0;
                uVar1 = _ZN13CMemoryStream7ReadIntEv(auStack_68);
                *(undefined4 *)(&__DT_SYMTAB[0x1e0].st_info + param_1) = uVar1;
                fVar4 = (float)_ZN13CMemoryStream9ReadFloatEv(auStack_68);
                uVar1 = _ZN3glf22AndroidGetMillisecondsEv();
                VectorSignedToFloat(uVar1,(byte)(in_fpscr >> 0x16) & 3);
                ceilf(__x);
                iVar2 = (int)(extraout_r0 - fVar4);
                if (iVar2 < 1) {
                  iVar2 = 1;
                }
                *(int *)((int)&__DT_SYMTAB[0x1e1].st_name + param_1) = iVar2;
                _ZN13CMemoryStreamD2Ev(auStack_68);
                if (*(int *)((int)&__DT_SYMTAB[0x1e2].st_value + param_1) == 0) {
                  uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
                  VectorUnsignedToFloat
                            (*(undefined4 *)(&__DT_SYMTAB[0x1e0].st_info + param_1),
                             (byte)(in_fpscr >> 0x16) & 3);
                  ceilf(__x_01);
                  iVar2 = *(int *)((int)&__DT_SYMTAB[0x1e1].st_name + param_1);
                  if (iVar2 < 1) {
                    iVar2 = 1;
                  }
                  iVar7 = (int)extraout_r0_01;
                  _ZN6CLevel8GetLevelEv();
                  uVar8 = _ZNK6CLevel18GetPlayerInventoryEv();
                  uVar8 = _ZN10CInventory17GetCurrencyPointsEi(uVar8,2);
                  _ZN6CLevel8GetLevelEv();
                  uVar5 = _ZNK6CLevel18GetPlayerInventoryEv();
                  uVar5 = _ZN10CInventory17GetCurrencyPointsEi(uVar5,4);
                  _ZN6CLevel8GetLevelEv();
                  iVar3 = _ZNK6CLevel18GetPlayerInventoryEv();
                  if (iVar7 < 1) {
                    iVar7 = 1;
                  }
                  _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                            (uVar1,0x8000,1,iVar7,iVar2,uVar8,uVar5,*(int *)(iVar3 + 0x60) + 0x8bef,
                             0,0);
                }
                else {
                  uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
                  VectorUnsignedToFloat
                            (*(undefined4 *)(&__DT_SYMTAB[0x1e0].st_info + param_1),
                             (byte)(in_fpscr >> 0x16) & 3);
                  uVar8 = *(undefined4 *)((int)&__DT_SYMTAB[0x1e2].st_value + param_1);
                  ceilf(__x_00);
                  iVar2 = *(int *)((int)&__DT_SYMTAB[0x1e1].st_name + param_1);
                  if (iVar2 < 1) {
                    iVar2 = 1;
                  }
                  iVar3 = (int)extraout_r0_00;
                  _ZN6CLevel8GetLevelEv();
                  uVar5 = _ZNK6CLevel18GetPlayerInventoryEv();
                  uVar5 = _ZN10CInventory17GetCurrencyPointsEi(uVar5,2);
                  if (iVar3 < 1) {
                    iVar3 = 1;
                  }
                  _ZN6CLevel8GetLevelEv();
                  uVar6 = _ZNK6CLevel18GetPlayerInventoryEv();
                  uVar6 = _ZN10CInventory17GetCurrencyPointsEi(uVar6,4);
                  _ZN6CLevel8GetLevelEv();
                  iVar7 = _ZNK6CLevel18GetPlayerInventoryEv();
                  _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                            (uVar1,0x8004,1,uVar8,iVar3,iVar2,uVar5,uVar6,
                             *(int *)(iVar7 + 0x60) + 0x8bef,0);
                }
              }
            }
            iVar3 = DAT_003ef2c0 + 0x3ef060;
            iVar2 = _ZN3glf19AndroidGetStoredIntEPKci(iVar3,0xffffffff);
            if (iVar2 == -1) {
              _ZN3glf19AndroidPutStoredIntEPKci(iVar3,1);
              uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
              _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                        (uVar1,0x8002,0,0,0,0,0,0,0,0);
              _ZN11Application12SaveUserInfoEv(param_1);
              uVar1 = 1;
            }
            else {
              uVar1 = 1;
            }
          }
        }
      }
    }
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}


