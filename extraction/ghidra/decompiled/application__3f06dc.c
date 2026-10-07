// _ZN11Application26SendTrackingEventInterruptEii @ 003f06dc

void _ZN11Application26SendTrackingEventInterruptEii(int param_1,int param_2,uint param_3)

{
  undefined4 uVar1;
  uint *puVar2;
  float *pfVar3;
  int iVar4;
  
  if (((param_3 & 1) == 0) || (puVar2 = (uint *)(DAT_003f0a30 + 0x3f0704), (*puVar2 & 0x80) == 0)) {
    if (((param_3 & 2) != 0) &&
       ((((*(uint *)(DAT_003f0a34 + 0x3f0720) & 0x10) != 0 &&
         (*(int *)((int)&__DT_SYMTAB[0x1e3].st_name + param_1) != 0)) &&
        (*(int *)((int)&__DT_SYMTAB[0x1e3].st_value + param_1) != 0)))) {
      uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
      pfVar3 = (float *)((int)&__DT_SYMTAB[0x1e3].st_size + param_1);
      iVar4 = (int)(*pfVar3 * DAT_003f0a2c);
      if (iVar4 < 1) {
        iVar4 = 1;
      }
      _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                (uVar1,0x8a67,0,*(undefined4 *)((int)&__DT_SYMTAB[0x1e2].st_size + param_1),
                 *(undefined4 *)(&__DT_SYMTAB[0x1e2].st_info + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_name + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_value + param_1),iVar4,param_2,0);
      if (param_2 != 0x8be7) {
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e2].st_size + param_1) = 0;
        *(undefined4 *)(&__DT_SYMTAB[0x1e2].st_info + param_1) = 0;
        *pfVar3 = 0.0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_name + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_value + param_1) = 0;
      }
    }
    if ((((param_3 & 4) != 0) && ((*(uint *)(DAT_003f0a38 + 0x3f0760) & 0x20) != 0)) &&
       ((*(int *)((int)&__DT_SYMTAB[0x1e4].st_value + param_1) != 0 &&
        (*(int *)((int)&__DT_SYMTAB[0x1e4].st_size + param_1) != 0)))) {
      uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
      iVar4 = (int)(*(float *)(&__DT_SYMTAB[0x1e4].st_info + param_1) * DAT_003f0a2c);
      if (iVar4 < 1) {
        iVar4 = 1;
      }
      _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                (uVar1,0x8a67,0,*(undefined4 *)(&__DT_SYMTAB[0x1e3].st_info + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_name + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_value + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_size + param_1),iVar4,param_2,0);
      if (param_2 != 0x8be7) {
        *(undefined4 *)(&__DT_SYMTAB[0x1e3].st_info + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_name + param_1) = 0;
        *(undefined4 *)(&__DT_SYMTAB[0x1e4].st_info + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_value + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_size + param_1) = 0;
      }
    }
    if ((((param_3 & 8) != 0) && ((*(uint *)(DAT_003f0a3c + 0x3f078c) & 0x40) != 0)) &&
       ((*(int *)((int)&__DT_SYMTAB[0x1e5].st_size + param_1) != 0 &&
        (*(int *)(&__DT_SYMTAB[0x1e5].st_info + param_1) != 0)))) {
      uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
      iVar4 = (int)(*(float *)((int)&__DT_SYMTAB[0x1e6].st_name + param_1) * DAT_003f0a2c);
      if (iVar4 < 1) {
        iVar4 = 1;
      }
      _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                (uVar1,0x8a67,0,*(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_name + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_value + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_size + param_1),
                 *(undefined4 *)(&__DT_SYMTAB[0x1e5].st_info + param_1),iVar4,param_2,0);
      if (param_2 != 0x8be7) {
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_name + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_value + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e6].st_name + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_size + param_1) = 0;
        *(undefined4 *)(&__DT_SYMTAB[0x1e5].st_info + param_1) = 0;
      }
    }
  }
  else {
    uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
    iVar4 = (int)(*(float *)((int)&__DT_SYMTAB[0x1e1].st_size + param_1) * DAT_003f0a2c);
    if (iVar4 < 1) {
      iVar4 = 1;
    }
    _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
              (uVar1,0x8a6b,0,iVar4,param_2,0,0,0,0,0);
    if (param_2 != 0x8be7) {
      *puVar2 = *puVar2 & 0xffffff7f;
    }
  }
  return;
}


