// _ZN11Application26SendTrackingEventInterruptEii.constprop.2567 @ 004678ac

void _ZN11Application26SendTrackingEventInterruptEii_constprop_2567(int param_1,int param_2)

{
  undefined4 uVar1;
  uint uVar2;
  uint *puVar3;
  float *pfVar4;
  int iVar5;
  
  puVar3 = (uint *)(DAT_00467bc4 + 0x4678c8);
  uVar2 = *puVar3;
  if ((uVar2 & 0x80) == 0) {
    if ((((uVar2 & 0x10) != 0) && (*(int *)((int)&__DT_SYMTAB[0x1e3].st_name + param_1) != 0)) &&
       (*(int *)((int)&__DT_SYMTAB[0x1e3].st_value + param_1) != 0)) {
      uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
      pfVar4 = (float *)((int)&__DT_SYMTAB[0x1e3].st_size + param_1);
      iVar5 = (int)(*pfVar4 * DAT_00467bc0);
      if (iVar5 < 1) {
        iVar5 = 1;
      }
      _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                (uVar1,0x8a67,0,*(undefined4 *)((int)&__DT_SYMTAB[0x1e2].st_size + param_1),
                 *(undefined4 *)(&__DT_SYMTAB[0x1e2].st_info + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_name + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_value + param_1),iVar5,param_2,0);
      uVar2 = *puVar3;
      if (param_2 != 0x8be7) {
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e2].st_size + param_1) = 0;
        *(undefined4 *)(&__DT_SYMTAB[0x1e2].st_info + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_name + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_value + param_1) = 0;
        *pfVar4 = 0.0;
      }
    }
    if ((((uVar2 & 0x20) != 0) && (*(int *)((int)&__DT_SYMTAB[0x1e4].st_value + param_1) != 0)) &&
       (*(int *)((int)&__DT_SYMTAB[0x1e4].st_size + param_1) != 0)) {
      uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
      iVar5 = (int)(*(float *)(&__DT_SYMTAB[0x1e4].st_info + param_1) * DAT_00467bc0);
      if (iVar5 < 1) {
        iVar5 = 1;
      }
      _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                (uVar1,0x8a67,0,*(undefined4 *)(&__DT_SYMTAB[0x1e3].st_info + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_name + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_value + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_size + param_1),iVar5,param_2,0);
      if (param_2 == 0x8be7) {
        uVar2 = *(uint *)((int)&DAT_00467bc0 + DAT_00467bcc);
      }
      else {
        *(undefined4 *)(&__DT_SYMTAB[0x1e4].st_info + param_1) = 0;
        iVar5 = DAT_00467bc8;
        *(undefined4 *)(&__DT_SYMTAB[0x1e3].st_info + param_1) = 0;
        uVar2 = *(uint *)(iVar5 + 0x467a98);
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_name + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_value + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_size + param_1) = 0;
      }
    }
    if ((((uVar2 & 0x40) != 0) && (*(int *)((int)&__DT_SYMTAB[0x1e5].st_size + param_1) != 0)) &&
       (*(int *)(&__DT_SYMTAB[0x1e5].st_info + param_1) != 0)) {
      uVar1 = _ZN4glot15TrackingManager11GetInstanceEv();
      iVar5 = (int)(*(float *)((int)&__DT_SYMTAB[0x1e6].st_name + param_1) * DAT_00467bc0);
      if (iVar5 < 1) {
        iVar5 = 1;
      }
      _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                (uVar1,0x8a67,0,*(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_name + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_value + param_1),
                 *(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_size + param_1),
                 *(undefined4 *)(&__DT_SYMTAB[0x1e5].st_info + param_1),iVar5,param_2,0);
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
    iVar5 = (int)(*(float *)((int)&__DT_SYMTAB[0x1e1].st_size + param_1) * DAT_00467bc0);
    if (iVar5 < 1) {
      iVar5 = 1;
    }
    _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
              (uVar1,0x8a6b,0,iVar5,param_2,0,0,0,0,0);
    if (param_2 != 0x8be7) {
      *puVar3 = *puVar3 & 0xffffff7f;
    }
  }
  return;
}


