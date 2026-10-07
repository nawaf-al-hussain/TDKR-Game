// _ZN11Application33SendTrackingEventMissionCompletedEiiif @ 003efa44

void _ZN11Application33SendTrackingEventMissionCompletedEiiif
               (int param_1,uint param_2,int param_3,undefined4 param_4,float param_5)

{
  int iVar1;
  undefined4 uVar2;
  dword *pdVar3;
  undefined1 *puVar4;
  undefined4 uVar5;
  int iVar6;
  int *piVar7;
  undefined1 *puVar8;
  int iVar9;
  uint uVar10;
  undefined1 *puVar11;
  undefined4 local_34;
  
  if (param_3 == -1) {
    iVar9 = param_2 + 0x8a8e;
    if (param_2 < 0x1a) {
      uVar5 = *(undefined4 *)(DAT_003efe8c + 0x3efb08 + param_2 * 4);
      local_34 = *(undefined4 *)(DAT_003efe90 + 0x3efb0c + param_2 * 4);
    }
    else {
      uVar5 = 0;
      local_34 = 0;
    }
    iVar6 = *(int *)((int)&__DT_SYMTAB[0x1e2].st_size + param_1);
    *(uint *)(DAT_003efe94 + 0x3efb28) = *(uint *)(DAT_003efe94 + 0x3efb28) & 0xffffffef;
    if ((iVar6 == iVar9) && (*(int *)((int)&__DT_SYMTAB[0x1e3].st_name + param_1) == 0x8a7f)) {
      uVar10 = 1 - *(uint *)(&__DT_SYMTAB[0x1e2].st_info + param_1);
      if (1 < *(uint *)(&__DT_SYMTAB[0x1e2].st_info + param_1)) {
        uVar10 = 0;
      }
    }
    else {
      uVar10 = 0;
    }
    if (DAT_003efe88 <= param_5) {
      puVar11 = (undefined1 *)0x1;
      iVar6 = 0;
      puVar4 = (undefined1 *)0x8a7f;
    }
    else {
      puVar11 = (undefined1 *)0x1;
      iVar6 = 0;
      puVar4 = (undefined1 *)0x8a7f;
      param_5 = *(float *)((int)&__DT_SYMTAB[0x1e3].st_size + param_1);
    }
    goto LAB_003efb70;
  }
  if (param_2 == 0x38b) {
    puVar11 = (undefined1 *)0x1;
    local_34 = 0x19;
    iVar6 = 0x8a89;
    puVar4 = (undefined1 *)0x8a7e;
  }
  else {
    if (0x38b < (int)param_2) {
      if (param_2 == 0x3a2) {
        iVar6 = 0x8a81;
      }
      else if ((int)param_2 < 0x3a3) {
        if (param_2 != 0x38c) {
          if (param_2 != 0x38d) goto LAB_003efa94;
          puVar11 = (undefined1 *)0x1;
          local_34 = 0x19;
          iVar6 = 0x8a8d;
          puVar4 = (undefined1 *)0x8a7e;
          goto LAB_003efe04;
        }
        iVar6 = 0x8a82;
      }
      else if (param_2 == 0x3a4) {
        iVar6 = 0x8a84;
      }
      else if ((int)param_2 < 0x3a4) {
        iVar6 = 0x8a83;
      }
      else {
        if (param_2 != 0x3a5) goto LAB_003efa94;
        iVar6 = 0x8a86;
      }
      iVar9 = *(int *)(&__DT_SYMTAB[0x1e3].st_info + param_1);
      *(uint *)(DAT_003efec0 + 0x3efd8c) = *(uint *)(DAT_003efec0 + 0x3efd8c) & 0xffffffdf;
      if (iVar9 == 0) {
        uVar10 = 0;
        if (*(int *)((int)&__DT_SYMTAB[0x1e4].st_value + param_1) == 0x8a80) {
          uVar10 = (uint)(*(int *)((int)&__DT_SYMTAB[0x1e4].st_name + param_1) == iVar6);
        }
      }
      else {
        uVar10 = 0;
      }
      if (DAT_003efe88 <= param_5) {
        puVar11 = (undefined1 *)0x1;
        local_34 = 100;
        uVar5 = 0x19;
        puVar4 = (undefined1 *)0x8a80;
        iVar9 = 0;
      }
      else {
        puVar11 = (undefined1 *)0x1;
        local_34 = 100;
        param_5 = *(float *)(&__DT_SYMTAB[0x1e4].st_info + param_1);
        uVar5 = 0x19;
        puVar4 = (undefined1 *)0x8a80;
        iVar9 = 0;
      }
      goto LAB_003efb70;
    }
    if (param_2 == 0x388) {
      puVar11 = (undefined1 *)0x1;
      iVar6 = 0x8a88;
      puVar4 = (undefined1 *)0x8a7e;
      local_34 = 0x19;
    }
    else if ((int)param_2 < 0x389) {
      if (param_2 == 0x70) {
        puVar11 = (undefined1 *)0x1;
        local_34 = 0x19;
        iVar6 = 0x8a8c;
        puVar4 = (undefined1 *)0x8a7e;
      }
      else if (param_2 == 0x71) {
        puVar11 = (undefined1 *)0x1;
        local_34 = 0x19;
        iVar6 = 0x8a87;
        puVar4 = (undefined1 *)0x8a7e;
      }
      else {
LAB_003efa94:
        puVar11 = (undefined1 *)0x0;
        local_34 = 0;
        iVar6 = 0;
        puVar4 = (undefined1 *)0x0;
      }
    }
    else if (param_2 == 0x389) {
      puVar11 = (undefined1 *)0x1;
      local_34 = 0x19;
      iVar6 = 0x8a8a;
      puVar4 = (undefined1 *)0x8a7e;
    }
    else {
      if (param_2 != 0x38a) goto LAB_003efa94;
      puVar11 = (undefined1 *)0x1;
      local_34 = 0x19;
      iVar6 = 0x8a8b;
      puVar4 = (undefined1 *)0x8a7e;
    }
  }
LAB_003efe04:
  pdVar3 = (dword *)(DAT_003efec4 + 0x3efe18);
  iVar9 = *(int *)((int)&__DT_SYMTAB[0x1e5].st_name + param_1);
  *pdVar3 = *pdVar3 & 0xffffffbf;
  if (iVar9 == 0) {
    pdVar3 = *(dword **)((int)&__DT_SYMTAB[0x1e5].st_size + param_1);
    uVar10 = 0;
    if (pdVar3 == (dword *)puVar4) {
      pdVar3 = &__DT_SYMTAB[0x1e5].st_value;
      uVar10 = (uint)(iVar6 == *(int *)((int)&__DT_SYMTAB[0x1e5].st_value + param_1));
    }
  }
  else {
    uVar10 = 0;
  }
  if (param_5 < DAT_003efe88) {
    pdVar3 = (dword *)(&__DT_SYMTAB[0x1ae].st_info + param_1);
  }
  uVar5 = 0;
  iVar9 = 0;
  if (param_5 < DAT_003efe88) {
    param_5 = (float)pdVar3[0xdd];
  }
LAB_003efb70:
  iVar1 = DAT_003efe98;
  _ZN6CLevel8GetLevelEv();
  piVar7 = *(int **)(iVar1 + 0x3efb84);
  iVar1 = strcasecmp(*(char **)(*piVar7 + 0x10),(char *)(DAT_003efe9c + 0x3efb88));
  if (iVar1 == 0) {
    puVar8 = &DAT_00008c28;
  }
  else {
    _ZN6CLevel8GetLevelEv();
    iVar1 = strcasecmp(*(char **)(*piVar7 + 0x10),(char *)(DAT_003efea0 + 0x3efc34));
    if (iVar1 == 0) {
      puVar8 = &DAT_00008c29;
    }
    else {
      _ZN6CLevel8GetLevelEv();
      iVar1 = strcasecmp(*(char **)(*piVar7 + 0x10),(char *)(DAT_003efea4 + 0x3efc58));
      if (iVar1 == 0) {
        puVar8 = &DAT_00008c2a;
      }
      else {
        _ZN6CLevel8GetLevelEv();
        iVar1 = strcasecmp(*(char **)(*piVar7 + 0x10),(char *)(DAT_003efea8 + 0x3efc7c));
        if (iVar1 == 0) {
          puVar8 = &DAT_00008c2b;
        }
        else {
          _ZN6CLevel8GetLevelEv();
          iVar1 = strcasecmp(*(char **)(*piVar7 + 0x10),(char *)(DAT_003efeac + 0x3efca0));
          if (iVar1 == 0) {
            puVar8 = &DAT_00008c2c;
          }
          else {
            _ZN6CLevel8GetLevelEv();
            iVar1 = strcasecmp(*(char **)(*piVar7 + 0x10),(char *)(DAT_003efeb0 + 0x3efcc4));
            if (iVar1 == 0) {
              puVar8 = &DAT_00008c2d;
            }
            else {
              _ZN6CLevel8GetLevelEv();
              iVar1 = strcasecmp(*(char **)(*piVar7 + 0x10),(char *)(DAT_003efeb4 + 0x3efce8));
              if (iVar1 == 0) {
                puVar8 = &DAT_00008c2e;
              }
              else {
                _ZN6CLevel8GetLevelEv();
                iVar1 = strcasecmp(*(char **)(*piVar7 + 0x10),(char *)(DAT_003efeb8 + 0x3efd0c));
                if (iVar1 == 0) {
                  puVar8 = &DAT_00008c2f;
                }
                else {
                  _ZN6CLevel8GetLevelEv();
                  iVar1 = strcasecmp(*(char **)(*piVar7 + 0x10),(char *)(DAT_003efebc + 0x3efd30));
                  if (iVar1 == 0) {
                    puVar8 = (undefined1 *)0x8c30;
                  }
                  else {
                    puVar8 = (undefined1 *)0x0;
                    puVar11 = puVar8;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  if (uVar10 != 0) {
    if (puVar11 != (undefined1 *)0x0) {
      uVar2 = _ZN4glot15TrackingManager11GetInstanceEv();
      iVar1 = (int)(param_5 * DAT_003efec8);
      if (iVar1 < 1) {
        iVar1 = 1;
      }
      _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                (uVar2,0x8a68,0,iVar9,iVar6,puVar4,puVar8,iVar1,uVar5,local_34);
    }
    if (puVar4 == (undefined1 *)0x8a7f) {
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e2].st_size + param_1) = 0;
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_size + param_1) = 0;
      *(undefined4 *)(&__DT_SYMTAB[0x1e2].st_info + param_1) = 0;
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_name + param_1) = 0;
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_value + param_1) = 0;
    }
    else if (puVar4 == (undefined1 *)0x8a80) {
      *(undefined4 *)(&__DT_SYMTAB[0x1e3].st_info + param_1) = 0;
      *(undefined4 *)(&__DT_SYMTAB[0x1e4].st_info + param_1) = 0;
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_name + param_1) = 0;
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_value + param_1) = 0;
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_size + param_1) = 0;
    }
    else if (puVar4 == (undefined1 *)0x8a7e) {
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_name + param_1) = 0;
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e6].st_name + param_1) = 0;
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_value + param_1) = 0;
      *(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_size + param_1) = 0;
      *(undefined4 *)(&__DT_SYMTAB[0x1e5].st_info + param_1) = 0;
    }
  }
  return;
}


