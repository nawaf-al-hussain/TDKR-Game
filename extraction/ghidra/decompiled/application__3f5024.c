// _ZN11Application7OnEventERKN3glf9CoreEventE @ 003f5024

void _ZN11Application7OnEventERKN3glf9CoreEventE(int param_1,short *param_2)

{
  char cVar1;
  short sVar2;
  undefined4 uVar3;
  int *piVar4;
  time_t tVar5;
  undefined4 extraout_r0;
  char *__s1;
  time_t __time0;
  undefined4 extraout_r1;
  int iVar6;
  int iVar7;
  int iVar8;
  int *piVar9;
  undefined4 uVar10;
  uint *puVar11;
  int *piVar12;
  char *pcVar13;
  uint uVar14;
  undefined4 *puVar15;
  undefined1 auStack_7b4 [12];
  undefined1 auStack_7a8 [12];
  char local_79c;
  char local_79b;
  char local_790;
  char local_78f;
  undefined1 auStack_784 [12];
  undefined1 auStack_778 [12];
  undefined1 auStack_76c [12];
  undefined1 auStack_760 [12];
  undefined1 auStack_754 [12];
  undefined1 auStack_748 [12];
  undefined1 auStack_73c [12];
  undefined1 local_730;
  undefined1 local_72f;
  undefined1 local_724;
  undefined1 local_723;
  undefined1 auStack_718 [40];
  char local_6f0;
  char local_6ef;
  undefined4 local_6e8;
  undefined4 local_6e4;
  undefined3 local_6b0;
  byte bStack_6ad;
  char local_6ac [8];
  undefined4 local_6a4;
  undefined4 local_6a0;
  undefined3 local_66c;
  byte bStack_669;
  undefined1 auStack_668 [84];
  undefined1 auStack_614 [84];
  undefined1 auStack_5c0 [84];
  undefined1 auStack_56c [84];
  undefined1 auStack_518 [84];
  undefined1 auStack_4c4 [84];
  undefined1 auStack_470 [84];
  undefined1 auStack_41c [84];
  undefined1 auStack_3c8 [84];
  undefined1 auStack_374 [84];
  undefined1 auStack_320 [84];
  undefined1 auStack_2cc [84];
  undefined1 auStack_278 [84];
  undefined1 auStack_224 [84];
  undefined1 auStack_1d0 [84];
  undefined1 auStack_17c [84];
  undefined1 auStack_128 [84];
  undefined1 auStack_d4 [84];
  undefined1 auStack_80 [84];
  int local_2c;
  
  iVar8 = DAT_003f5fc8 + 0x3f5044;
  piVar9 = *(int **)(iVar8 + DAT_003f5fcc);
  local_2c = *piVar9;
  _ZN3glf3App11GetInstanceEv();
  if ((**(char **)(iVar8 + DAT_003f5fd0) == '\0') ||
     (_ZN3glf3App11GetInstanceEv(), **(char **)(iVar8 + DAT_003f5fd4) == '\0')) {
    sVar2 = *param_2;
LAB_003f506c:
    if (sVar2 != 0xcd) goto LAB_003f5074;
    if (*(int *)(param_2 + 10) == 4) {
      piVar12 = *(int **)(iVar8 + DAT_003f5fdc);
      piVar4 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar12 + 4);
      iVar7 = (**(code **)(*piVar4 + 8))(piVar4,1);
      if (iVar7 == 0) {
        piVar4 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar12 + 4);
        iVar7 = (**(code **)(*piVar4 + 8))(piVar4,0x2a);
        if (iVar7 != 0) goto LAB_003f53b8;
        piVar4 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar12 + 4);
        iVar7 = (**(code **)(*piVar4 + 8))(piVar4,100);
        if (iVar7 != 0) goto LAB_003f53b8;
        piVar4 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar12 + 4);
        iVar7 = (**(code **)(*piVar4 + 8))(piVar4,0x25);
        if (iVar7 != 0) goto LAB_003f53b8;
      }
      else {
LAB_003f53b8:
        _ZN3glf23AndroidSendToBackgroundEv();
      }
      puVar11 = (uint *)(DAT_003f5ffc + 0x3f53c8);
      if (((*puVar11 & 1) == 0) && (iVar7 = __cxa_guard_acquire(puVar11), iVar7 != 0)) {
        tVar5 = time((time_t *)0x0);
        *(time_t *)(DAT_003f6028 + 0x3f5738) = tVar5;
        __cxa_guard_release(puVar11);
      }
      puVar11 = (uint *)(DAT_003f6000 + 0x3f53dc);
      if (((*puVar11 & 1) == 0) && (iVar7 = __cxa_guard_acquire(puVar11), iVar7 != 0)) {
        tVar5 = time((time_t *)0x0);
        *(time_t *)(DAT_003f6024 + 0x3f5708) = tVar5;
        __cxa_guard_release(puVar11);
      }
      iVar7 = _ZN6CLevel8GetLevelEv();
      if ((iVar7 == 0) || (iVar7 = _ZN6CLevel8GetLevelEv(), *(int *)(iVar7 + 0xec) == 0)) {
LAB_003f5414:
        piVar4 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar12 + 4);
        iVar7 = (**(code **)(*piVar4 + 8))(piVar4,8);
        if (iVar7 != 0) goto LAB_003f5438;
        piVar4 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar12 + 4);
        iVar7 = (**(code **)(*piVar4 + 8))(piVar4,0x2c);
        if (iVar7 != 0) goto LAB_003f5438;
      }
      else {
        _ZN6CLevel8GetLevelEv();
        iVar7 = _ZNK6CLevel18GetPlayerComponentEv();
        if (*(int *)(iVar7 + 0x270) != 1) goto LAB_003f5414;
LAB_003f5438:
        tVar5 = time((time_t *)0x0);
        __time0 = *(time_t *)(DAT_003f6008 + 0x3f5454);
        *(time_t *)(DAT_003f6004 + 0x3f5450) = tVar5;
        difftime(tVar5,__time0);
        if (2.0 <= (double)CONCAT44(extraout_r1,extraout_r0)) {
          iVar7 = _ZN11Application11GetInstanceEv();
          iVar7 = *(int *)((int)&__DT_SYMTAB[0x1df].st_name + iVar7);
          iVar7 = *(int *)(iVar7 + 8) + *(int *)(*(int *)(iVar7 + 0xc) + 0x11a4) * 2;
          if (iVar7 != 0) {
            iVar6 = _Znaj(0x100);
            _Z21_ConvertUnicodeToUTF8PcPKt(iVar6,iVar7);
            iVar7 = _ZN11Application11GetInstanceEv();
            (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar7) + 0x5c))
                      (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar7),iVar6);
            if (iVar6 != 0) {
              _ZdaPv(iVar6);
            }
            tVar5 = time((time_t *)0x0);
            *(time_t *)(DAT_003f6080 + 0x3f5be0) = tVar5;
          }
        }
      }
      iVar7 = *(int *)(DAT_003f600c + 0x3f5478);
      uVar3 = 0;
      if (iVar7 == 0) goto LAB_003f50c4;
      if (*(char *)(iVar7 + 0x49e) != '\0') {
        *(undefined1 *)(iVar7 + 0x49e) = 0;
      }
      if (*(char *)(iVar7 + 0x498) != '\0') {
        uVar3 = *(undefined4 *)(DAT_003f602c + 0x3f5758);
        _ZN7gameswf15CharacterHandleC1EPNS_9CharacterE(auStack_5c0,0);
        _ZN12CMenuManager12GetCharacterEPKcN7gameswf15CharacterHandleE
                  (auStack_614,uVar3,DAT_003f6030 + 0x3f5770,auStack_5c0);
        _ZN7gameswf15CharacterHandleD1Ev(auStack_5c0);
        iVar8 = _ZNK7gameswf15CharacterHandle7isValidEv(auStack_614);
        if (iVar8 != 0) {
          _ZN7gameswf15CharacterHandle12invokeMethodEPKcPKNS_7ASValueEi
                    (auStack_7a8,auStack_614,DAT_003f6034 + 0x3f57a0,0,0);
          _ZN7gameswf7ASValue8dropRefsEv(auStack_7a8);
        }
        _ZN7gameswf15CharacterHandleD1Ev(auStack_614);
        uVar3 = 0;
        goto LAB_003f50c4;
      }
      cVar1 = *(char *)(iVar7 + 0x499);
      if (cVar1 != '\0') {
        iVar6 = *piVar12;
        *(undefined1 *)(iVar7 + 0x499) = 0;
        piVar4 = (int *)_ZN12gxStateStack12CurrentStateEv(iVar6 + 4);
        iVar7 = (**(code **)(*piVar4 + 8))(piVar4,2);
        if (iVar7 != 0) {
          _ZN11CHUDDisplay11SetHudStateEPc
                    (*(undefined4 *)(DAT_003f6038 + 0x3f5820),DAT_003f603c + 0x3f5824);
        }
        uVar3 = 0;
        _ZN15VoxSoundManager4PlayEPKcNS_6E_LOOPEi
                  (auStack_718,**(undefined4 **)(iVar8 + DAT_003f6040),DAT_003f6044 + 0x3f5848,
                   0xffffffff,0);
        _ZN3vox13EmitterHandleD1Ev(auStack_718);
        goto LAB_003f50c4;
      }
      if ((*(uint *)(iVar7 + 0x4c8) & 0x8000) != 0) {
        puVar15 = (undefined4 *)(DAT_003f6048 + 0x3f5870);
        uVar3 = *puVar15;
        _ZN7gameswf15CharacterHandleC1EPNS_9CharacterE(auStack_518,0);
        _ZN12CMenuManager12GetCharacterEPKcN7gameswf15CharacterHandleE
                  (auStack_56c,uVar3,DAT_003f604c + 0x3f588c,auStack_518);
        _ZN7gameswf15CharacterHandleD1Ev(auStack_518);
        iVar7 = _ZNK7gameswf15CharacterHandle7isValidEv(auStack_56c);
        if (iVar7 != 0) {
          local_79c = cVar1;
          local_79b = cVar1;
          local_790 = cVar1;
          local_78f = cVar1;
          iVar8 = _ZN11Application11GetInstanceEv();
          _ZN8CStrings19GetStringNameFromIdEiPc
                    (*(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + iVar8),0x442,auStack_614);
          iVar8 = _ZN11Application11GetInstanceEv();
          uVar3 = _ZN8CStrings17GetStringFromNameEPKc
                            (*(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + iVar8),auStack_614);
          local_6f0 = '\x01';
          local_6ef = cVar1;
          _ZN7gameswf6String19encodeUTF8FromWcharEPS0_PKt(&local_6f0,uVar3);
          _local_6b0 = CONCAT13(bStack_6ad & 0xfe,0xffffff);
          _ZN7gameswf7ASValue9setStringERKNS_6StringE(&local_790,&local_6f0);
          if (local_6f0 == -1) {
            _ZN7gameswf13free_internalEPvj(local_6e4,local_6e8);
          }
          iVar8 = DAT_003f6050;
          pcVar13 = (char *)_ZNK7gameswf7ASValue6toCStrEv(&local_790);
          puVar15 = (undefined4 *)(iVar8 + 0x3f5944);
          uVar3 = *puVar15;
          _ZN7gameswf15CharacterHandleC1EPNS_9CharacterE(auStack_470,0);
          _ZN12CMenuManager12GetCharacterEPKcN7gameswf15CharacterHandleE
                    (auStack_4c4,uVar3,DAT_003f6054 + 0x3f5968,auStack_470);
          _ZN7gameswf15CharacterHandleD1Ev(auStack_470);
          _ZN7gameswf15CharacterHandle12invokeMethodEPKcPKNS_7ASValueEi
                    (auStack_784,auStack_4c4,DAT_003f6058 + 0x3f5988,0,0);
          _ZN7gameswf7ASValueaSERKS0_(&local_79c,auStack_784);
          _ZN7gameswf7ASValue8dropRefsEv(auStack_784);
          __s1 = (char *)_ZNK7gameswf7ASValue6toCStrEv(&local_79c);
          iVar7 = DAT_003f605c + 0x3f59bc;
          __android_log_print(4,iVar7,DAT_003f6060 + 0x3f59c0,__s1);
          __android_log_print(4,iVar7,DAT_003f6064 + 0x3f59e4,pcVar13);
          iVar8 = strcmp(__s1,pcVar13);
          if (iVar8 == 0) {
            uVar3 = *puVar15;
            _ZN7gameswf15CharacterHandleC1EPNS_9CharacterE(auStack_3c8,0);
            _ZN12CMenuManager12GetCharacterEPKcN7gameswf15CharacterHandleE
                      (auStack_41c,uVar3,DAT_003f6068 + 0x3f5a20,auStack_3c8);
            _ZN7gameswf15CharacterHandleD1Ev(auStack_3c8);
            iVar8 = _ZNK7gameswf15CharacterHandle7isValidEv(auStack_41c);
            if (iVar8 != 0) {
              _ZN7gameswf15CharacterHandle12invokeMethodEPKcPKNS_7ASValueEi
                        (auStack_778,auStack_41c,DAT_003f60a0 + 0x3f5e78,0,0);
              _ZN7gameswf7ASValue8dropRefsEv(auStack_778);
            }
            _ZN7gameswf15CharacterHandleD1Ev(auStack_41c);
          }
          else {
            __android_log_print(4,iVar7,DAT_003f608c + 0x3f5cf8);
            uVar3 = *puVar15;
            _ZN7gameswf15CharacterHandleC1EPNS_9CharacterE(auStack_320,0);
            _ZN12CMenuManager12GetCharacterEPKcN7gameswf15CharacterHandleE
                      (auStack_374,uVar3,DAT_003f6090 + 0x3f5d20,auStack_320);
            _ZN7gameswf15CharacterHandleD1Ev(auStack_320);
            iVar8 = _ZNK7gameswf15CharacterHandle7isValidEv(auStack_374);
            if (iVar8 == 0) {
              _ZN7gameswf15CharacterHandleD1Ev(auStack_374);
            }
            else {
              _ZN7gameswf15CharacterHandle12invokeMethodEPKcPKNS_7ASValueEi
                        (auStack_76c,auStack_374,DAT_003f6094 + 0x3f5d58,0,0);
              _ZN7gameswf7ASValue8dropRefsEv(auStack_76c);
              _ZN7gameswf15CharacterHandleD1Ev(auStack_374);
            }
          }
          _ZN7gameswf15CharacterHandleD1Ev(auStack_4c4);
          _ZN7gameswf7ASValue8dropRefsEv(&local_790);
          _ZN7gameswf7ASValue8dropRefsEv(&local_79c);
          _ZN7gameswf15CharacterHandleD1Ev(auStack_56c);
          uVar3 = 0;
          goto LAB_003f50c4;
        }
        iVar7 = _ZN6CLevel8GetLevelEv();
        iVar7 = _ZNK11CGameObject6IsDeadEv(*(undefined4 *)(iVar7 + 0xec));
        if (iVar7 != 0) {
          uVar3 = *puVar15;
          uVar10 = *(undefined4 *)(*(int *)(DAT_003f60a4 + 0x3f5ea0) + 0x3b4);
          _ZN7gameswf15CharacterHandleC1EPNS_9CharacterE(auStack_278,0);
          _ZN12CMenuManager12GetCharacterEPKcN7gameswf15CharacterHandleE
                    (auStack_2cc,uVar3,uVar10,auStack_278);
          _ZN7gameswf15CharacterHandleD1Ev(auStack_278);
          _ZN8CStrings19GetStringNameFromIdEiPc
                    (*(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + param_1),0x442,auStack_374);
          uVar3 = _ZN8CStrings17GetStringFromNameEPKc
                            (*(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + param_1),auStack_374);
          local_730 = 0;
          local_6ac[0] = '\x01';
          local_72f = 0;
          local_724 = 0;
          local_723 = 0;
          local_6ac[1] = 0;
          _ZN7gameswf6String19encodeUTF8FromWcharEPS0_PKt(local_6ac,uVar3);
          _local_66c = CONCAT13(bStack_669 & 0xfe,0xffffff);
          _ZN7gameswf7ASValue9setStringERKNS_6StringE(&local_730,local_6ac);
          if (local_6ac[0] == -1) {
            _ZN7gameswf13free_internalEPvj(local_6a0,local_6a4);
          }
          _ZN7gameswf7ASValue9setStringEPKc(&local_724,DAT_003f60a8 + 0x3f5f7c);
          _ZN7gameswf15CharacterHandle12invokeMethodEPKcPKNS_7ASValueEi
                    (auStack_760,auStack_2cc,DAT_003f60ac + 0x3f5f94,&local_730,2);
          _ZN7gameswf7ASValue8dropRefsEv(auStack_760);
          _ZN7gameswf7ASValue8dropRefsEv(&local_724);
          _ZN7gameswf7ASValue8dropRefsEv(&local_730);
          _ZN7gameswf15CharacterHandleD1Ev(auStack_2cc);
        }
        _ZN7gameswf15CharacterHandleD1Ev(auStack_56c);
      }
      pcVar13 = *(char **)(&__DT_SYMTAB[0x1e9].st_info + param_1);
      if (*(int *)(pcVar13 + -0xc) == 0) {
        puVar15 = (undefined4 *)(DAT_003f6074 + 0x3f5ae8);
        uVar3 = *puVar15;
        _ZN7gameswf15CharacterHandleC1EPNS_9CharacterE(auStack_1d0,0);
        _ZN12CMenuManager12GetCharacterEPKcN7gameswf15CharacterHandleE
                  (auStack_224,uVar3,DAT_003f6078 + 0x3f5b08,auStack_1d0);
        _ZN7gameswf15CharacterHandleD1Ev(auStack_1d0);
        iVar7 = _ZNK7gameswf15CharacterHandle7isValidEv(auStack_224);
        if (iVar7 != 0) {
          _ZN7gameswf15CharacterHandle12invokeMethodEPKcPKNS_7ASValueEi
                    (auStack_754,auStack_224,DAT_003f607c + 0x3f5b3c,0,0);
          _ZN7gameswf7ASValue8dropRefsEv(auStack_754);
LAB_003f5b4c:
          _ZN7gameswf15CharacterHandleD1Ev(auStack_224);
          uVar3 = 0;
          goto LAB_003f50c4;
        }
        uVar3 = *puVar15;
        _ZN7gameswf15CharacterHandleC1EPNS_9CharacterE(auStack_128,0);
        _ZN12CMenuManager12GetCharacterEPKcN7gameswf15CharacterHandleE
                  (auStack_17c,uVar3,DAT_003f6084 + 0x3f5c58,auStack_128);
        _ZN7gameswf15CharacterHandleD1Ev(auStack_128);
        iVar7 = _ZNK7gameswf15CharacterHandle7isValidEv(auStack_17c);
        if (iVar7 == 0) {
          uVar3 = *puVar15;
          uVar10 = *(undefined4 *)(*(int *)(DAT_003f6098 + 0x3f5db4) + 0x3b4);
          _ZN7gameswf15CharacterHandleC1EPNS_9CharacterE(auStack_80,0);
          _ZN12CMenuManager12GetCharacterEPKcN7gameswf15CharacterHandleE
                    (auStack_d4,uVar3,uVar10,auStack_80);
          _ZN7gameswf15CharacterHandleD1Ev(auStack_80);
          iVar7 = _ZNK7gameswf15CharacterHandle7isValidEv(auStack_d4);
          if (iVar7 != 0) {
            _ZN7gameswf15CharacterHandle12invokeMethodEPKcPKNS_7ASValueEi
                      (auStack_73c,auStack_d4,DAT_003f609c + 0x3f5e04,0,0);
            _ZN7gameswf7ASValue8dropRefsEv(auStack_73c);
            _ZN7gameswf15CharacterHandleD1Ev(auStack_d4);
            _ZN7gameswf15CharacterHandleD1Ev(auStack_17c);
            goto LAB_003f5b4c;
          }
          _ZN7gameswf15CharacterHandleD1Ev(auStack_d4);
        }
        else {
          _ZN7gameswf15CharacterHandle12invokeMethodEPKcPKNS_7ASValueEi
                    (auStack_748,auStack_17c,DAT_003f6088 + 0x3f5c98,0,0);
          _ZN7gameswf7ASValue8dropRefsEv(auStack_748);
        }
        _ZN7gameswf15CharacterHandleD1Ev(auStack_17c);
        _ZN7gameswf15CharacterHandleD1Ev(auStack_224);
      }
      else {
        iVar7 = strcmp(pcVar13,(char *)(DAT_003f6010 + 0x3f54d8));
        if (iVar7 == 0) {
          iVar7 = _ZN4glot15TrackingManager11GetInstanceEv();
          if (iVar7 != 0) {
            _ZN4glot15TrackingManager11GetInstanceEv();
            _ZN4glot15TrackingManager14updateSaveFileEv();
          }
          iVar7 = _ZN11Application11GetInstanceEv();
          uVar3 = *(undefined4 *)(*(int *)(&__DT_SYMTAB[0x1e9].st_info + param_1) + -0xc);
          *(undefined1 *)(iVar7 + 5) = 0;
          _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE9_M_mutateEjjj
                    (param_1 + 0x11fb0,0,uVar3);
        }
        else {
          iVar7 = strcmp(pcVar13,(char *)(DAT_003f6014 + 0x3f54f0));
          if (iVar7 == 0) {
            _ZN11GS_BaseMenu16ReturnToMainMenuEb();
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE9_M_mutateEjjj
                      (param_1 + 0x11fb0,0,
                       *(undefined4 *)(*(int *)(&__DT_SYMTAB[0x1e9].st_info + param_1) + -0xc),0);
          }
        }
      }
      if ((*(int *)(DAT_003f6018 + 0x3f5504) == 0) ||
         (uVar14 = *(uint *)(*(int *)(DAT_003f6018 + 0x3f5504) + 0x4c8),
         *(undefined1 *)((int)&__DT_SYMTAB[0x1ea].st_name + param_1) = 0, (uVar14 & 0x8000) != 0))
      goto LAB_003f5228;
      uVar3 = _ZN6CLevel8GetLevelEv();
      _ZN6CLevel14OpenIngameMenuEb(uVar3,0);
      sVar2 = *param_2;
      *(undefined1 *)((int)&__DT_SYMTAB[0x1ea].st_name + param_1) = 1;
      goto LAB_003f5074;
    }
    if (*(int *)(param_2 + 10) == 0x52) {
      uVar3 = 0;
      iVar7 = *(int *)(DAT_003f5fe0 + 0x3f51ac);
      *(undefined1 *)((int)&__DT_SYMTAB[0x1ea].st_name + param_1) = 0;
      if (iVar7 == 0) {
        uVar3 = 0;
        goto LAB_003f50c4;
      }
      if (*(char *)(iVar7 + 0x498) != '\0') goto LAB_003f50c4;
      if ((*(uint *)(iVar7 + 0x4c8) & 0x800000) != 0) {
        uVar3 = 0;
        goto LAB_003f50c4;
      }
      if ((*(uint *)(iVar7 + 0x4c8) & 0x8000) == 0) {
        uVar3 = _ZN6CLevel8GetLevelEv(0);
        _ZN6CLevel14OpenIngameMenuEb(uVar3,0);
        sVar2 = *param_2;
        *(undefined1 *)((int)&__DT_SYMTAB[0x1ea].st_name + param_1) = 1;
        goto LAB_003f5074;
      }
      _ZN11CHUDDisplay8EnterIGMEbbb(iVar7,0,0,0);
      iVar7 = *(int *)(&__DT_SYMTAB[0x1e9].st_info + param_1);
      *(undefined1 *)((int)&__DT_SYMTAB[0x1ea].st_name + param_1) = 0;
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE9_M_mutateEjjj
                (param_1 + 0x11fb0,0,*(undefined4 *)(iVar7 + -0xc),0);
      _ZN7gameswf15CharacterHandleaSEPNS_9CharacterE(*(undefined4 *)(iVar8 + DAT_003f5fe4),0);
LAB_003f5228:
      sVar2 = *param_2;
      goto LAB_003f5074;
    }
    goto switchD_003f5304_default;
  }
  uVar3 = 0;
  if (*(char *)(DAT_003f5fd8 + 0x3f5104) == '\0') goto LAB_003f50c4;
  sVar2 = *param_2;
  if ((ushort)(sVar2 - 0xccU) < 2) {
    if (*(int *)(param_2 + 10) == 0x12) {
      if (sVar2 != 0xcc) {
        uVar3 = *(undefined4 *)(iVar8 + DAT_003f5fe4);
        _ZN7gameswf15CharacterHandleC1ERKS0_(auStack_668,uVar3);
        _ZN7gameswf15CharacterHandle12invokeMethodEPKcPKNS_7ASValueEi
                  (auStack_7b4,auStack_668,DAT_003f601c + 0x3f5634,0,0);
        pcVar13 = (char *)_ZNK7gameswf7ASValue6toCStrEv(auStack_7b4);
        _ZN7gameswf7ASValue8dropRefsEv(auStack_7b4);
        piVar4 = (int *)_ZN12gxStateStack12CurrentStateEv(**(int **)(iVar8 + DAT_003f5fdc) + 4);
        iVar8 = (**(code **)(*piVar4 + 8))(piVar4,2);
        if (((iVar8 == 0) || (iVar8 = (**(code **)(*piVar4 + 8))(piVar4,8), iVar8 != 0)) ||
           (*pcVar13 != '\0')) {
          iVar8 = strcmp(pcVar13,(char *)(DAT_003f6020 + 0x3f5690));
          if (iVar8 == 0) {
            _ZN11CHUDDisplay8EnterIGMEbbb(*(undefined4 *)(DAT_003f6070 + 0x3f5ac4),0,0,0);
            _ZN7gameswf15CharacterHandleaSEPNS_9CharacterE(uVar3,0);
          }
        }
        else {
          _ZN11CHUDDisplay8EnterIGMEbbb(*(undefined4 *)(DAT_003f606c + 0x3f5aa8),1,0,0);
        }
        _ZN7gameswf15CharacterHandleD1Ev(auStack_668);
        uVar3 = 1;
        goto LAB_003f50c4;
      }
    }
    else if (*(int *)(param_2 + 10) == 4) goto LAB_003f506c;
    piVar12 = *(int **)(iVar8 + DAT_003f5fdc);
    piVar4 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar12 + 4);
    iVar8 = (**(code **)(*piVar4 + 8))(piVar4,0x25);
    if (iVar8 == 0) {
      _ZN9CControls10OnKeyEventEibi(*(undefined4 *)(param_2 + 10),*param_2 == 0xcc);
      uVar3 = 1;
    }
    else {
      piVar4 = (int *)_ZN12gxStateStack12CurrentStateEv(*piVar12 + 4);
      (**(code **)(*piVar4 + 0x30))();
      uVar3 = 1;
    }
    goto LAB_003f50c4;
  }
LAB_003f5074:
  if ((ushort)(sVar2 - 0xd6U) < 3) {
    if (sVar2 == 0xd6) {
      uVar3 = 0;
    }
    else if (sVar2 == 0xd8) {
      uVar3 = 2;
    }
    else {
      uVar3 = 1;
    }
    _ZN15TouchScreenBase13AddTouchEventEiiil
              (uVar3,(int)param_2[0xc],(int)param_2[0xd],*(undefined4 *)(param_2 + 10));
    sVar2 = *param_2;
  }
  if (sVar2 != 0x65) goto LAB_003f50b8;
  switch(*(undefined4 *)(param_2 + 2)) {
  case 0:
    goto LAB_003f531c;
  case 1:
    _ZN3glf7Console5PrintEPKcz(DAT_003f5ff0 + 0x3f5340);
    GameResume();
    sVar2 = *param_2;
    break;
  case 2:
LAB_003f531c:
    _ZN3glf7Console5PrintEPKcz(DAT_003f5fec + 0x3f5328);
    GamePause();
    sVar2 = *param_2;
    break;
  case 3:
    goto switchD_003f5304_default;
  case 4:
    _ZN3glf7Console5PrintEPKcz(DAT_003f5ff4 + 0x3f5358);
    GamePause();
    sVar2 = *param_2;
    break;
  case 5:
    _ZN3glf7Console5PrintEPKcz(DAT_003f5ff8 + 0x3f5370);
    *(undefined1 *)((int)&__DT_SYMTAB[0x1f1].st_size + param_1) = 1;
    GameResume();
    sVar2 = *param_2;
    break;
  default:
    goto switchD_003f5304_default;
  }
LAB_003f50b8:
  if (sVar2 == 100) {
    uVar10 = *(undefined4 *)(param_2 + 2);
    piVar4 = (int *)_ZN12gxStateStack12CurrentStateEv(**(int **)(iVar8 + DAT_003f5fdc) + 4);
    if (piVar4 != (int *)0x0) {
      iVar8 = (**(code **)(*piVar4 + 8))(piVar4,2);
      if ((iVar8 != 0) &&
         (uVar3 = 0, (*(uint *)(*(int *)(DAT_003f5fe8 + 0x3f529c) + 0x4c8) & 0x8000) == 0))
      goto LAB_003f50c4;
      iVar8 = (**(code **)(*piVar4 + 8))(piVar4,8);
      if (iVar8 != 0) goto switchD_003f5304_default;
      iVar8 = (**(code **)(*piVar4 + 8))(piVar4,1);
      if (iVar8 != 0) {
        uVar3 = 0;
        goto LAB_003f50c4;
      }
      iVar8 = (**(code **)(*piVar4 + 8))(piVar4,0x2c);
      if (iVar8 != 0) {
        uVar3 = 0;
        goto LAB_003f50c4;
      }
    }
    switch(uVar10) {
    case 0:
      uVar3 = _ZN3glf3App11GetInstanceEv(0);
      _ZN3glf3App14SetOrientationENS_11OrientationE(uVar3,1);
      uVar3 = 0;
      break;
    case 1:
      uVar3 = _ZN3glf3App11GetInstanceEv(0);
      _ZN3glf3App14SetOrientationENS_11OrientationE(uVar3,2);
      uVar3 = 0;
      break;
    case 2:
      uVar3 = _ZN3glf3App11GetInstanceEv(0);
      _ZN3glf3App14SetOrientationENS_11OrientationE(uVar3,4);
      uVar3 = 0;
      break;
    case 3:
      uVar3 = _ZN3glf3App11GetInstanceEv(0);
      _ZN3glf3App14SetOrientationENS_11OrientationE(uVar3,8);
      uVar3 = 0;
      break;
    default:
      goto switchD_003f5304_default;
    }
  }
  else {
switchD_003f5304_default:
    uVar3 = 0;
  }
LAB_003f50c4:
  if (local_2c == *piVar9) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(uVar3);
}


