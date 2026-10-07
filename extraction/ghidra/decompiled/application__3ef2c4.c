// _ZN11Application23SendTrackingEventResumeEi @ 003ef2c4

undefined4 _ZN11Application23SendTrackingEventResumeEi(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 uVar3;
  float extraout_r0;
  undefined4 uVar4;
  undefined4 uVar5;
  int iVar6;
  float extraout_r0_00;
  uint uVar7;
  uint *puVar8;
  undefined4 uVar9;
  uint in_fpscr;
  float __x;
  float __x_00;
  int iVar10;
  
  puVar8 = (uint *)(DAT_003ef500 + 0x3ef2dc);
  if ((*puVar8 & 0x800) == 0) {
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
          iVar2 = _ZNK6CLevel18GetPlayerInventoryEv();
          uVar1 = 0;
          if (iVar2 != 0) {
            uVar1 = 1;
            uVar7 = *puVar8;
            iVar2 = *(int *)((int)&__DT_SYMTAB[0x1e2].st_value + param_1);
            *(undefined1 *)((int)&__DT_SYMTAB[0x1e1].st_value + param_1) = 1;
            *puVar8 = uVar7 & 0xfffffffe | 0x800;
            if (iVar2 == 0) {
              uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
              VectorUnsignedToFloat
                        (*(undefined4 *)(&__DT_SYMTAB[0x1e0].st_info + param_1),
                         (byte)(in_fpscr >> 0x16) & 3);
              ceilf(__x_00);
              iVar2 = *(int *)((int)&__DT_SYMTAB[0x1e1].st_name + param_1);
              if (iVar2 < 1) {
                iVar2 = 1;
              }
              iVar6 = (int)extraout_r0_00;
              _ZN6CLevel8GetLevelEv();
              uVar3 = _ZNK6CLevel18GetPlayerInventoryEv();
              uVar3 = _ZN10CInventory17GetCurrencyPointsEi(uVar3,2);
              _ZN6CLevel8GetLevelEv();
              uVar9 = _ZNK6CLevel18GetPlayerInventoryEv();
              uVar9 = _ZN10CInventory17GetCurrencyPointsEi(uVar9,4);
              _ZN6CLevel8GetLevelEv();
              iVar10 = _ZNK6CLevel18GetPlayerInventoryEv();
              if (iVar6 < 1) {
                iVar6 = 1;
              }
              _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                        (uVar1,0x8001,1,iVar6,iVar2,uVar3,uVar9,*(int *)(iVar10 + 0x60) + 0x8bef,0,0
                        );
              uVar1 = 1;
            }
            else {
              uVar3 = _ZN4glot15TrackingManager11GetInstanceEv();
              VectorUnsignedToFloat
                        (*(undefined4 *)(&__DT_SYMTAB[0x1e0].st_info + param_1),
                         (byte)(in_fpscr >> 0x16) & 3);
              uVar9 = *(undefined4 *)((int)&__DT_SYMTAB[0x1e2].st_value + param_1);
              ceilf(__x);
              iVar2 = *(int *)((int)&__DT_SYMTAB[0x1e1].st_name + param_1);
              if (iVar2 < 1) {
                iVar2 = 1;
              }
              iVar10 = (int)extraout_r0;
              _ZN6CLevel8GetLevelEv();
              uVar4 = _ZNK6CLevel18GetPlayerInventoryEv();
              uVar4 = _ZN10CInventory17GetCurrencyPointsEi(uVar4,2);
              if (iVar10 < 1) {
                iVar10 = 1;
              }
              _ZN6CLevel8GetLevelEv();
              uVar5 = _ZNK6CLevel18GetPlayerInventoryEv();
              uVar5 = _ZN10CInventory17GetCurrencyPointsEi(uVar5,4);
              _ZN6CLevel8GetLevelEv();
              iVar6 = _ZNK6CLevel18GetPlayerInventoryEv();
              _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                        (uVar3,0x8005,1,uVar9,iVar10,iVar2,uVar4,uVar5,
                         *(int *)(iVar6 + 0x60) + 0x8bef,0);
            }
          }
        }
      }
    }
  }
  else {
    *puVar8 = *puVar8 & 0xfffffffe;
    uVar1 = 0;
  }
  return uVar1;
}


