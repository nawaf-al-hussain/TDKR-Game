// _ZN11Application31SendTrackingEventMissionStartedEiii @ 003ef504

void _ZN11Application31SendTrackingEventMissionStartedEiii(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 uVar2;
  int unaff_r4;
  int unaff_r5;
  int *piVar3;
  undefined1 *puVar4;
  int unaff_r10;
  bool bVar5;
  
  if (param_3 == -1) {
    param_2 = param_2 + 0x8a8e;
    bVar5 = *(int *)((int)&__DT_SYMTAB[0x1e2].st_size + param_1) != param_2;
    if (bVar5) {
      unaff_r10 = 0;
      unaff_r4 = 0x8a7f;
    }
    if (bVar5) {
      unaff_r5 = unaff_r10;
    }
    *(uint *)(DAT_003efa14 + 0x3ef60c) = *(uint *)(DAT_003efa14 + 0x3ef60c) | 0x10;
    if (bVar5) goto LAB_003ef628;
    unaff_r4 = 0x8a7f;
    if (*(int *)((int)&__DT_SYMTAB[0x1e3].st_name + param_1) != 0x8a7f) {
      unaff_r5 = 0;
      unaff_r10 = unaff_r5;
      goto LAB_003ef628;
    }
    unaff_r4 = 0x8a7f;
    unaff_r5 = 0;
    if (*(int *)(&__DT_SYMTAB[0x1e2].st_info + param_1) != 0) {
      unaff_r5 = 0;
      unaff_r10 = unaff_r5;
      goto LAB_003ef628;
    }
LAB_003ef928:
    unaff_r10 = 1;
  }
  else {
    if (param_2 == 0x38b) {
      unaff_r5 = 0x8a89;
      unaff_r4 = 0x8a7e;
    }
    else {
      if (0x38b < param_2) {
        if (param_2 == 0x3a2) {
          unaff_r5 = 0x8a81;
        }
        else if (param_2 < 0x3a3) {
          if (param_2 != 0x38c) {
            if (param_2 != 0x38d) goto LAB_003ef54c;
            unaff_r5 = 0x8a8d;
            unaff_r4 = 0x8a7e;
            goto LAB_003ef554;
          }
          unaff_r5 = 0x8a82;
        }
        else if (param_2 == 0x3a4) {
          unaff_r5 = 0x8a84;
        }
        else if (param_2 < 0x3a4) {
          unaff_r5 = 0x8a83;
        }
        else {
          if (param_2 != 0x3a5) goto LAB_003ef54c;
          unaff_r5 = 0x8a86;
        }
        bVar5 = *(int *)(&__DT_SYMTAB[0x1e3].st_info + param_1) != 0;
        if (bVar5) {
          unaff_r10 = 0;
          unaff_r4 = 0x8a80;
        }
        param_2 = 0;
        if (bVar5) {
          param_2 = unaff_r10;
        }
        *(uint *)(DAT_003efa40 + 0x3ef8ac) = *(uint *)(DAT_003efa40 + 0x3ef8ac) | 0x20;
        if (((bVar5) ||
            (unaff_r4 = 0x8a80, unaff_r10 = param_2,
            *(int *)((int)&__DT_SYMTAB[0x1e4].st_value + param_1) != 0x8a80)) ||
           (unaff_r4 = 0x8a80, *(int *)((int)&__DT_SYMTAB[0x1e4].st_name + param_1) != unaff_r5))
        goto LAB_003ef628;
        goto LAB_003ef928;
      }
      if (param_2 == 0x388) {
        unaff_r5 = 0x8a88;
        unaff_r4 = 0x8a7e;
      }
      else if (param_2 < 0x389) {
        if (param_2 == 0x70) {
          unaff_r5 = 0x8a8c;
          unaff_r4 = 0x8a7e;
        }
        else if (param_2 == 0x71) {
          unaff_r5 = 0x8a87;
          unaff_r4 = 0x8a7e;
        }
        else {
LAB_003ef54c:
          unaff_r5 = 0;
          unaff_r4 = 0;
        }
      }
      else if (param_2 == 0x389) {
        unaff_r5 = 0x8a8a;
        unaff_r4 = 0x8a7e;
      }
      else {
        if (param_2 != 0x38a) goto LAB_003ef54c;
        unaff_r5 = 0x8a8b;
        unaff_r4 = 0x8a7e;
      }
    }
LAB_003ef554:
    bVar5 = *(int *)((int)&__DT_SYMTAB[0x1e5].st_name + param_1) != 0;
    if (bVar5) {
      unaff_r10 = 0;
    }
    param_2 = 0;
    if (bVar5) {
      param_2 = unaff_r10;
    }
    *(uint *)(DAT_003efa10 + 0x3ef56c) = *(uint *)(DAT_003efa10 + 0x3ef56c) | 0x40;
    if (((!bVar5) &&
        (unaff_r10 = param_2, *(int *)((int)&__DT_SYMTAB[0x1e5].st_size + param_1) == unaff_r4)) &&
       (*(int *)((int)&__DT_SYMTAB[0x1e5].st_value + param_1) == unaff_r5)) {
      unaff_r10 = 1;
    }
  }
LAB_003ef628:
  iVar1 = DAT_003efa18;
  _ZN6CLevel8GetLevelEv();
  _ZN6CLevel8GetLevelEv();
  piVar3 = *(int **)(iVar1 + 0x3ef640);
  iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003efa1c + 0x3ef644));
  if (iVar1 == 0) {
    bVar5 = true;
    puVar4 = &DAT_00008c28;
  }
  else {
    _ZN6CLevel8GetLevelEv();
    iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003efa20 + 0x3ef720));
    if (iVar1 == 0) {
      bVar5 = true;
      puVar4 = &DAT_00008c29;
    }
    else {
      _ZN6CLevel8GetLevelEv();
      iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003efa24 + 0x3ef748));
      if (iVar1 == 0) {
        bVar5 = true;
        puVar4 = &DAT_00008c2a;
      }
      else {
        _ZN6CLevel8GetLevelEv();
        iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003efa28 + 0x3ef770));
        if (iVar1 == 0) {
          bVar5 = true;
          puVar4 = &DAT_00008c2b;
        }
        else {
          _ZN6CLevel8GetLevelEv();
          iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003efa2c + 0x3ef798));
          if (iVar1 == 0) {
            bVar5 = true;
            puVar4 = &DAT_00008c2c;
          }
          else {
            _ZN6CLevel8GetLevelEv();
            iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003efa30 + 0x3ef7c0));
            if (iVar1 == 0) {
              bVar5 = true;
              puVar4 = &DAT_00008c2d;
            }
            else {
              _ZN6CLevel8GetLevelEv();
              iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003efa34 + 0x3ef7e8));
              if (iVar1 == 0) {
                bVar5 = true;
                puVar4 = &DAT_00008c2e;
              }
              else {
                _ZN6CLevel8GetLevelEv();
                iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003efa38 + 0x3ef810));
                if (iVar1 == 0) {
                  bVar5 = true;
                  puVar4 = &DAT_00008c2f;
                }
                else {
                  _ZN6CLevel8GetLevelEv();
                  iVar1 = strcasecmp(*(char **)(*piVar3 + 0x10),(char *)(DAT_003efa3c + 0x3ef838));
                  if (iVar1 != 0) {
                    puVar4 = (undefined1 *)0x0;
                  }
                  else {
                    puVar4 = (undefined1 *)0x8c30;
                  }
                  bVar5 = iVar1 == 0;
                }
              }
            }
          }
        }
      }
    }
  }
  if (unaff_r10 == 0) {
    if (unaff_r4 == 0) {
      bVar5 = false;
    }
    if (bVar5) {
      if (unaff_r4 == 0x8a7f) {
        *(int *)(&__DT_SYMTAB[0x1e2].st_info + param_1) = unaff_r5;
        *(int *)((int)&__DT_SYMTAB[0x1e2].st_size + param_1) = param_2;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_size + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e3].st_name + param_1) = 0x8a7f;
        *(undefined1 **)((int)&__DT_SYMTAB[0x1e3].st_value + param_1) = puVar4;
      }
      else if (unaff_r4 == 0x8a80) {
        *(int *)((int)&__DT_SYMTAB[0x1e4].st_name + param_1) = unaff_r5;
        *(int *)(&__DT_SYMTAB[0x1e3].st_info + param_1) = param_2;
        *(undefined4 *)(&__DT_SYMTAB[0x1e4].st_info + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e4].st_value + param_1) = 0x8a80;
        *(undefined1 **)((int)&__DT_SYMTAB[0x1e4].st_size + param_1) = puVar4;
      }
      else if (unaff_r4 == 0x8a7e) {
        *(int *)((int)&__DT_SYMTAB[0x1e5].st_value + param_1) = unaff_r5;
        *(int *)((int)&__DT_SYMTAB[0x1e5].st_name + param_1) = param_2;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e6].st_name + param_1) = 0;
        *(undefined4 *)((int)&__DT_SYMTAB[0x1e5].st_size + param_1) = 0x8a7e;
        *(undefined1 **)(&__DT_SYMTAB[0x1e5].st_info + param_1) = puVar4;
      }
      uVar2 = _ZN4glot15TrackingManager11GetInstanceEv();
      _ZN4glot15TrackingManager8AddEventIiiiiiiiiiiiiiiiiiiiiEEviNS_13eventPriorityET_T0_T1_T2_T3_T4_T5_T6_T7_T8_T9_T10_T11_T12_T13_T14_T15_T16_T17_T18__constprop_2549
                (uVar2,0x8a66,0,param_2,unaff_r5,unaff_r4,puVar4,0,0,0);
    }
  }
  return;
}


