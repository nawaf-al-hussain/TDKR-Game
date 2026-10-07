// _ZN11Application4InitEi @ 003eb3b0

undefined4 _ZN11Application4InitEi(int param_1,undefined4 param_2)

{
  char *pcVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  size_t sVar5;
  int iVar6;
  int *piVar7;
  void *__s;
  undefined4 uVar8;
  char *pcVar9;
  undefined4 *puVar10;
  undefined4 uVar11;
  undefined4 uVar12;
  uint uVar13;
  int *piVar14;
  int iVar15;
  int *piVar16;
  int iVar17;
  undefined4 *puVar18;
  int *local_3c;
  int *local_38;
  int *local_34;
  int local_30;
  int local_2c;
  undefined4 local_28;
  undefined4 local_24 [2];
  
  iVar15 = DAT_003ebf74 + 0x3eb3c8;
  switch(param_2) {
  case 0:
    *(undefined1 *)(**(int **)(iVar15 + DAT_003ec04c) + 0x27) = 1;
    iVar15 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar15) + 0x28);
    (**(code **)(*piVar16 + 0x78))(piVar16,DAT_003ec050 + 0x3ebde0,1,1);
    _ZN11Application17InitShaderOptionsEv(param_1);
    uVar8 = 0;
    break;
  case 1:
    __s = (void *)_Z11CustomAllocjPKci(0x14,DAT_003ec044 + 0x3ebd74,0x5b4);
    *(void **)(DAT_003ec048 + 0x3ebd88) = __s;
    memset(__s,0,0x10);
    *(undefined4 *)((int)__s + 0x10) = 0x9e3779b9;
    _ZN11CEncryption4InitEv(__s);
    uVar8 = 0;
    break;
  case 2:
    iVar15 = DAT_003ec040 + 0x3ebd10;
    uVar8 = _Z11CustomAllocjPKci(0x20,iVar15,0x5ba);
    _ZN8CStringsC1Ev();
    *(undefined4 *)((int)&__DT_SYMTAB[0x1df].st_name + param_1) = uVar8;
    uVar12 = _Z11CustomAllocjPKci(0x20,iVar15,0x5bb);
    _ZN8CStringsC1Ev();
    uVar11 = *(undefined4 *)((int)&__DT_SYMTAB[0x1df].st_name + param_1);
    uVar8 = 0;
    *(undefined4 *)((int)&__DT_SYMTAB[0x1df].st_value + param_1) = uVar12;
    *(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + param_1) = uVar11;
    break;
  case 3:
    piVar16 = *(int **)(iVar15 + DAT_003ec02c);
    iVar17 = *piVar16;
    if (iVar17 != 0) {
      iVar6 = _Znwj(0xc);
      if (iVar6 != -8) {
        *(int *)(iVar6 + 8) = iVar17;
      }
      _ZNSt8__detail15_List_node_base7_M_hookEPS0_(iVar6,param_1 + 0x11ef8);
    }
    iVar6 = DAT_003ec030 + 0x3ebc5c;
    piVar7 = (int *)_Z11CustomAllocjPKci(0x28,iVar6,0x5ce);
    _ZN15TouchScreenBaseC1E15E_TouchPriority(piVar7,1);
    piVar14 = (int *)(DAT_003ec034 + 0x3ebc80);
    iVar17 = *piVar16;
    *piVar7 = DAT_003ec038 + 0x3ebc90;
    *piVar14 = (int)piVar7;
    _ZN15TouchScreenBase23RegisterForGlobalEventsEPS_(iVar17,piVar7);
    piVar7[1] = 1;
    piVar7[9] = -1;
    _Z11CustomAllocjPKci(0x38,iVar6,0x5d4);
    _ZN12EventManagerC1Ev();
    iVar15 = **(int **)(iVar15 + DAT_003ec03c);
    if (iVar15 == 0) {
      uVar8 = 0;
    }
    else {
      iVar17 = _Znwj(0xc);
      if (iVar17 != -8) {
        *(int *)(iVar17 + 8) = iVar15;
      }
      _ZNSt8__detail15_List_node_base7_M_hookEPS0_(iVar17,param_1 + 0x11ef8);
      uVar8 = 0;
    }
    break;
  case 4:
    iVar15 = DAT_003ec028 + 0x3ebbdc;
    _Z11CustomAllocjPKci(0x40,iVar15,0x5db);
    _ZN14CGadgetManagerC1Ev();
    _Z11CustomAllocjPKci(0x2c,iVar15,0x5dc);
    _ZN15UpgradesManagerC1Ev();
    _Z11CustomAllocjPKci(200,iVar15,0x5dd);
    _ZN11ShopManagerC1Ev();
    uVar8 = 0;
    break;
  case 5:
    _Z11CustomAllocjPKci(0x28,DAT_003ec020 + 0x3ebb20,0x5e4);
    _ZN17FederationManagerC1Ev();
    iVar15 = **(int **)(iVar15 + DAT_003ebfc4);
    if (iVar15 != 0) {
      iVar17 = _Znwj(0xc);
      if (iVar17 != -8) {
        *(int *)(iVar17 + 8) = iVar15;
      }
      _ZNSt8__detail15_List_node_base7_M_hookEPS0_(iVar17,param_1 + 0x11ef8);
    }
    piVar16 = (int *)(DAT_003ec024 + 0x3ebb64);
    iVar15 = *piVar16;
    if (iVar15 == 0) {
      iVar15 = _Znwj(0x80);
      _ZN15CEffectsManagerC2Ev();
      *piVar16 = iVar15;
    }
    iVar17 = _ZN11Application11GetInstanceEv();
    iVar17 = *(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17);
    if (iVar17 != 0) {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar17 + 4);
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar17 + 4);
    }
    iVar6 = *(int *)(iVar15 + 0x34);
    *(int *)(iVar15 + 0x34) = iVar17;
    if (iVar6 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (iVar17 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar17);
    }
    _ZN15VoxSoundManager14CreateInstanceEv();
    uVar8 = 0;
    break;
  case 6:
    iVar15 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar15) + 0x28);
    (**(code **)(*piVar16 + 0x78))(piVar16,DAT_003ec01c + 0x3ebaf0,1,1);
    uVar8 = 0;
    break;
  case 7:
    _ZN13CGameSettings4LoadEv(**(undefined4 **)(iVar15 + DAT_003ebf78));
    if (*(uint *)(&__DT_SYMTAB[0x1ef].st_info + param_1) < 10) {
LAB_003eba7c:
      _ZN11Application11LoadStringsEPKc_part_1369_constprop_2592(param_1);
      iVar15 = *(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1);
    }
    else {
      _ZN11Application21GetLanguageFromDeviceEv(param_1);
      iVar15 = *(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1);
      if (-1 < iVar15) goto LAB_003eba7c;
    }
    uVar13 = iVar15 - 6;
    if (uVar13 < 4) {
      uVar12 = *(undefined4 *)(DAT_003ec018 + 0x3ebab8 + uVar13 * 4);
      uVar8 = *(undefined4 *)(DAT_003ec014 + 0x3ebab4 + uVar13 * 4);
    }
    else {
      uVar12 = 1000;
      uVar8 = 0;
    }
    _ZN7gameswf21setFontBaselineAdjustEf(uVar8);
    _ZN7gameswf19setFontRatioPercentEi(uVar12);
    uVar8 = 0;
    break;
  case 8:
    _ZN11Application11GetInstanceEv();
    _ZN11Application25CheckSpaceAvailableToSaveEb(1);
    uVar8 = 0;
    break;
  case 9:
    _ZN12CMenuManager4InitEv(*(undefined4 *)(DAT_003ec010 + 0x3eba3c));
    uVar8 = 0;
    break;
  case 10:
    iVar17 = _ZN11Application11GetInstanceEv();
    uVar12 = *(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17) + 8);
    iVar17 = _ZN11Application11GetInstanceEv();
    uVar8 = *(undefined4 *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17);
    piVar16 = (int *)_Z11CustomAllocjPKci(0xd8,DAT_003ec004 + 0x3eb98c,0x61e);
    _ZN6glitch10irradiance18CIrradianceManagerC1EPNS_7IDeviceE(piVar16,uVar8);
    iVar17 = DAT_003ec008 + 0x3eb9bc;
    *(byte *)(piVar16 + 5) = *(byte *)(piVar16 + 5) | 8;
    *piVar16 = iVar17;
    piVar16[0x35] = 0x40a00000;
    _ZN23CustomIrradianceManager16InitDefaultLightEv(piVar16);
    *(int **)((int)&__DT_SYMTAB[0x1e6].st_value + param_1) = piVar16;
    local_3c = piVar16;
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(piVar16 + 1);
    _ZN6glitch5video12IVideoDriver20setIrradianceManagerERKN5boost13intrusive_ptrINS_10irradiance18IIrradianceManagerEEE
              (uVar12,&local_3c);
    if (local_3c != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    uVar8 = 0;
    *(byte *)(*(int *)((int)&__DT_SYMTAB[0x1e6].st_value + param_1) + 0x28) =
         *(byte *)(**(int **)(iVar15 + DAT_003ec00c) + 0x31) ^ 1;
    break;
  case 0xb:
    iVar15 = _ZN11Application11GetInstanceEv();
    (**(code **)(**(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar15) + 0x10) + 0x30))
              (&local_38);
    iVar15 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar15) + 0x28);
    (**(code **)(*piVar16 + 0xc))(&local_34,piVar16,DAT_003ebffc + 0x3eb868);
    uVar8 = (**(code **)(*local_34 + 0x20))();
    uVar12 = _Z11CustomAllocjPKci(uVar8,0,0);
    *(undefined4 *)((int)&__DT_SYMTAB[0x1e9].st_value + param_1) = uVar12;
    (**(code **)(*local_34 + 0xc))(local_34,uVar12,uVar8);
    _ZN6glitch2io20createMemoryReadFileEPvlPKcb
              (&local_30,*(undefined4 *)((int)&__DT_SYMTAB[0x1e9].st_value + param_1),uVar8,
               DAT_003ec000 + 0x3eb8d0,0);
    iVar15 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar15) + 0x10);
    (**(code **)(*piVar16 + 0x50))(&local_2c,piVar16,&local_30,0x10);
    *(int *)((int)&__DT_SYMTAB[0x1e9].st_name + param_1) = local_2c;
    if (local_2c != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (local_30 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (local_34 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    uVar8 = 0;
    if (local_38 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)local_38 + *(int *)(*local_38 + -0xc));
      uVar8 = 0;
    }
    break;
  case 0xc:
    piVar16 = *(int **)(iVar15 + DAT_003ebff8);
    _ZN11ShopManager4InitEv(*piVar16);
    _ZN8CLottery16InitLotteryItemsEv(*(undefined4 *)(*piVar16 + 0x68));
    uVar8 = 0;
    break;
  case 0xd:
    iVar17 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17) + 0x28);
    (**(code **)(*piVar16 + 0x78))(piVar16,DAT_003ebfcc + 0x3eb698,1,1);
    iVar17 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17) + 0x28);
    (**(code **)(*piVar16 + 0x78))(piVar16,DAT_003ebfd0 + 0x3eb6c0,1,1);
    iVar17 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17) + 0x28);
    (**(code **)(*piVar16 + 0x78))(piVar16,DAT_003ebfd4 + 0x3eb6e8,1,1);
    iVar17 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17) + 0x28);
    (**(code **)(*piVar16 + 0x78))(piVar16,DAT_003ebfd8 + 0x3eb710,1,1);
    iVar17 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17) + 0x28);
    (**(code **)(*piVar16 + 0x78))(piVar16,DAT_003ebfdc + 0x3eb738,1,1);
    iVar17 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17) + 0x28);
    (**(code **)(*piVar16 + 0x78))(piVar16,DAT_003ebfe0 + 0x3eb760,1,1);
    iVar17 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17) + 0x28);
    (**(code **)(*piVar16 + 0x78))(piVar16,DAT_003ebfe4 + 0x3eb788,1,1);
    iVar17 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17) + 0x28);
    (**(code **)(*piVar16 + 0x78))(piVar16,DAT_003ebfe8 + 0x3eb7b0,1,1);
    iVar17 = _ZN11Application11GetInstanceEv();
    piVar16 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar17) + 0x28);
    (**(code **)(*piVar16 + 0x78))(piVar16,DAT_003ebfec + 0x3eb7d8,1,1);
    _ZN15CEffectsManager11DeserializeEPKc
              (**(undefined4 **)(iVar15 + DAT_003ebff0),DAT_003ebff4 + 0x3eb7fc);
    uVar8 = 0;
    break;
  case 0xe:
    _ZNK3glf3App13GetScreenSizeERiS1_i(param_1,&local_28,local_24,0);
    _ZN17CNovaSceneManager10InitializeEii
              (*(undefined4 *)(DAT_003ebfc8 + 0x3eb66c),local_28,local_24[0]);
    uVar8 = 0;
    break;
  case 0xf:
    pcVar1 = (char *)(**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + param_1) + 0x38))();
    iVar2 = strcmp(pcVar1,(char *)(DAT_003ebf88 + 0x3eb4a8));
    iVar3 = DAT_003ec060;
    iVar6 = DAT_003ec05c;
    iVar17 = DAT_003ec058;
    if (iVar2 == 0) {
      pcVar1 = (char *)(**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + param_1) + 0x34))();
      pcVar9 = (char *)(DAT_003ebf8c + 0x3eb4d8);
      *(undefined1 *)((int)&__DT_SYMTAB[0x1e7].st_name + param_1) = 0;
      iVar3 = strncmp(pcVar1,pcVar9,6);
      iVar6 = DAT_003ec074;
      iVar17 = DAT_003ec070;
      if (iVar3 == 0) {
        uVar12 = 0xca02;
        puVar10 = (undefined4 *)(DAT_003ec06c + 0x3ebeb8);
        puVar18 = (undefined4 *)(DAT_003ec070 + 0x3ebec0);
        *(undefined4 *)(DAT_003ec068 + 0x3ebeb4) = 0xca02;
        *puVar10 = 1;
        uVar8 = *(undefined4 *)(iVar17 + 0x3ebec4);
        *(undefined4 *)(iVar6 + 0x3ebed4) = *puVar18;
        *(char *)(iVar6 + 0x3ebed8) = (char)uVar8;
      }
      else {
        iVar3 = strncmp(pcVar1,(char *)(DAT_003ebf90 + 0x3eb4fc),4);
        iVar6 = DAT_003ec094;
        iVar17 = DAT_003ec090;
        if (iVar3 == 0) {
          uVar12 = 0xca01;
          puVar10 = (undefined4 *)(DAT_003ec08c + 0x3ebf38);
          puVar18 = (undefined4 *)(DAT_003ec090 + 0x3ebf40);
          *(undefined4 *)(DAT_003ec088 + 0x3ebf34) = 0xca01;
          *puVar10 = 2;
          uVar8 = *(undefined4 *)(iVar17 + 0x3ebf44);
          *(undefined4 *)(iVar6 + 0x3ebf54) = *puVar18;
          *(char *)(iVar6 + 0x3ebf58) = (char)uVar8;
        }
        else {
          iVar4 = strncmp(pcVar1,(char *)(DAT_003ebf94 + 0x3eb518),4);
          iVar2 = DAT_003ec084;
          iVar3 = DAT_003ec080;
          iVar6 = DAT_003ebfa4;
          iVar17 = DAT_003ebfa0;
          if (iVar4 == 0) {
            uVar12 = 0xca03;
            puVar18 = (undefined4 *)(DAT_003ebf9c + 0x3eb540);
            puVar10 = (undefined4 *)(DAT_003ebfa0 + 0x3eb548);
            *(undefined4 *)(DAT_003ebf98 + 0x3eb53c) = 0xca03;
            *puVar18 = 0;
            uVar8 = *(undefined4 *)(iVar17 + 0x3eb54c);
            *(undefined4 *)(iVar6 + 0x3eb554) = *puVar10;
            *(char *)(iVar6 + 0x3eb558) = (char)uVar8;
          }
          else {
            uVar12 = 0xca03;
            puVar10 = (undefined4 *)(DAT_003ec07c + 0x3ebefc);
            puVar18 = (undefined4 *)(DAT_003ec080 + 0x3ebf04);
            *(undefined4 *)(DAT_003ec078 + 0x3ebef8) = 0xca03;
            *puVar10 = 0;
            uVar8 = *(undefined4 *)(iVar3 + 0x3ebf08);
            *(undefined4 *)(iVar2 + 0x3ebf10) = *puVar18;
            *(char *)(iVar2 + 0x3ebf14) = (char)uVar8;
          }
        }
      }
      sprintf((char *)(DAT_003ebfa8 + 0x3eb56c),(char *)(DAT_003ebfac + 0x3eb570),uVar12);
    }
    else {
      uVar8 = *(undefined4 *)(DAT_003ec054 + 0x3ebe24);
      puVar10 = (undefined4 *)(DAT_003ec05c + 0x3ebe34);
      piVar16 = *(int **)(&__DT_SYMTAB[0x1dd].st_info + param_1);
      puVar18 = (undefined4 *)(DAT_003ec060 + 0x3ebe3c);
      *(undefined4 *)(DAT_003ec058 + 0x3ebe28) = *(undefined4 *)(DAT_003ec054 + 0x3ebe20);
      *(short *)(iVar17 + 0x3ebe2c) = (short)uVar8;
      uVar8 = *(undefined4 *)(iVar6 + 0x3ebe38);
      *puVar18 = *puVar10;
      *(char *)(iVar3 + 0x3ebe40) = (char)uVar8;
      pcVar1 = (char *)(**(code **)(*piVar16 + 0x34))(piVar16);
      iVar17 = DAT_003ec064;
      *(undefined1 *)((int)&__DT_SYMTAB[0x1e7].st_name + param_1) = 0;
      iVar17 = strncmp(pcVar1,(char *)(iVar17 + 0x3ebe74),6);
      if (iVar17 == 0) {
        *(undefined1 *)((int)&__DT_SYMTAB[0x1e7].st_name + param_1) = 1;
      }
    }
    pcVar9 = (char *)(DAT_003ebfb0 + 0x3eb58c);
    pcVar1 = (char *)(**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + param_1) + 100))
                               (*(int **)(&__DT_SYMTAB[0x1dd].st_info + param_1),0);
    strcpy(pcVar9,pcVar1);
    sVar5 = strlen(pcVar9);
    _ZN4glwt5Codec11GenerateMD5EPKvjPc(pcVar9,sVar5,DAT_003ebfb4 + 0x3eb5b4);
    puVar10 = (undefined4 *)(DAT_003ebfbc + 0x3eb5d4);
    uVar8 = *(undefined4 *)(DAT_003ebfb8 + 0x3eb5d0);
    *(short *)(DAT_003ebfbc + 0x3eb5d8) = (short)*(undefined4 *)(DAT_003ebfb8 + 0x3eb5d4);
    iVar17 = DAT_003ebfc0;
    *puVar10 = uVar8;
    _Z11CustomAllocjPKci(0x68,iVar17 + 0x3eb5ec,0x6ba);
    _ZN10IAPManagerC1Ev();
    piVar16 = *(int **)(iVar15 + DAT_003ebf84);
    _ZN10IAPManager4InitEv(*piVar16);
    iVar17 = *piVar16;
    if (iVar17 != 0) {
      iVar6 = _Znwj(0xc);
      if (iVar6 != -8) {
        *(int *)(iVar6 + 8) = iVar17;
      }
      _ZNSt8__detail15_List_node_base7_M_hookEPS0_(iVar6,param_1 + 0x11ef8);
    }
    _ZN17FederationManager4InitEv(**(undefined4 **)(iVar15 + DAT_003ebfc4));
    _ZN11Application19InitTrackingManagerEv(param_1);
    uVar8 = 0;
    break;
  case 0x10:
    _ZN9CControls17LoadControlSchemeEPKci
              (DAT_003ebf80 + 0x3eb468,**(undefined4 **)(iVar15 + DAT_003ebf7c));
    _ZN10IAPManager17RequestStoreItemsEv(**(undefined4 **)(iVar15 + DAT_003ebf84));
    uVar8 = 0;
    break;
  case 0x11:
    _ZN11Application12InitFromLogoEv();
    uVar8 = 0;
    break;
  case 0x12:
    _ZN11Application14LoadGameConfigEv();
    uVar8 = 0;
    break;
  case 0x13:
    _ZN13CGameSettings4SaveEv(**(undefined4 **)(iVar15 + DAT_003ebf78));
    uVar8 = 1;
    break;
  default:
    uVar8 = 0;
  }
  return uVar8;
}


