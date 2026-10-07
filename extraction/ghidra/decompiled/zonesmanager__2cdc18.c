// _ZN13CZonesManager11SpawnObjectEiRKN6glitch4core8vector3dIfEERKSbIcSt11char_traitsIcENS1_10SAllocatorIcLNS0_6memory13E_MEMORY_HINTE0EEEEP5CZoneb @ 002cdc18

int * _ZN13CZonesManager11SpawnObjectEiRKN6glitch4core8vector3dIfEERKSbIcSt11char_traitsIcENS1_10SAllocatorIcLNS0_6memory13E_MEMORY_HINTE0EEEEP5CZoneb
                (int param_1,undefined4 param_2,int *param_3,undefined4 param_4,int param_5,
                undefined1 param_6)

{
  int iVar1;
  undefined4 uVar2;
  size_t sVar3;
  int *piVar4;
  int *piVar5;
  float fVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  char cVar11;
  int iVar12;
  code *pcVar13;
  char *pcVar14;
  int iVar15;
  char *pcVar16;
  undefined4 uVar17;
  undefined4 uVar18;
  char *local_50;
  int local_4c;
  int local_48;
  float local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  int local_34;
  int local_30;
  float local_2c;
  
  _Z14StrGetFileNameRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE
            (&local_50,param_4);
  pcVar14 = local_50;
  if (*(int *)(local_50 + -0xc) == 0) {
    iVar1 = _ZN6CLevel8GetLevelEv();
    uVar2 = _ZN18CGameObjectManager17GetMeshNameFromIdEi(*(undefined4 *)(iVar1 + 0xa94),param_2);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (&local_50,uVar2);
    pcVar14 = local_50;
  }
  sVar3 = strlen(pcVar14);
  pcVar16 = pcVar14;
  while (pcVar14 + sVar3 != pcVar16) {
    cVar11 = *pcVar16;
    if ((uint)(int)cVar11 < 0x100) {
      cVar11 = (char)*(undefined2 *)(**(int **)(DAT_002ce27c + 0x2cdc98) + cVar11 * 2 + 2);
    }
    *pcVar16 = cVar11;
    pcVar16 = pcVar16 + 1;
  }
  pcVar14[sVar3] = '\0';
  piVar4 = (int *)_ZN22GameObjectCacheManager3PopEiRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                            (*(undefined4 *)(param_1 + 0x68),param_2,&local_50);
  if (piVar4 == (int *)0x0) {
    iVar1 = _ZN6CLevel8GetLevelEv();
    piVar4 = (int *)_ZN18CGameObjectManager23CreateObjectFromLibraryEiP5CZoneRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS4_6memory13E_MEMORY_HINTE0EEEE
                              (*(undefined4 *)(iVar1 + 0xa94),param_2,0,&local_50);
    pcVar13 = *(code **)(*piVar4 + 0x24);
    **(int **)(param_1 + 0x68) = **(int **)(param_1 + 0x68) + 1;
    (*pcVar13)();
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
              (piVar4 + 0x3f,&local_50);
    pcVar16 = (char *)piVar4[0x3f];
    sVar3 = strlen(pcVar16);
    pcVar14 = pcVar16;
    while (pcVar14 != pcVar16 + sVar3) {
      cVar11 = *pcVar14;
      if ((uint)(int)cVar11 < 0x100) {
        cVar11 = (char)*(undefined2 *)(**(int **)(DAT_002ce280 + 0x2ce0a0) + cVar11 * 2 + 2);
      }
      *pcVar14 = cVar11;
      pcVar14 = pcVar14 + 1;
    }
    pcVar16[sVar3] = '\0';
    (**(code **)(*piVar4 + 0x50))(piVar4,1);
    (**(code **)(*piVar4 + 0x80))(piVar4,1);
    iVar1 = piVar4[0x36];
    if (iVar1 == 0) {
      uVar17 = 0;
      uVar2 = uVar17;
      uVar18 = uVar17;
    }
    else {
      uVar2 = *(undefined4 *)(iVar1 + 0xc);
      uVar18 = *(undefined4 *)(iVar1 + 0x10);
      *(int *)(iVar1 + 0xc) = *param_3;
      uVar17 = *(undefined4 *)(iVar1 + 0x14);
      *(int *)(iVar1 + 0x10) = param_3[1];
      *(int *)(iVar1 + 0x14) = param_3[2];
    }
    _ZN22GameObjectCacheManager4PushEP11CGameObject(*(undefined4 *)(param_1 + 0x68),piVar4);
    (**(code **)(*piVar4 + 0x74))(piVar4);
    (**(code **)(*piVar4 + 0x28))(piVar4,param_3,1);
    local_40 = 0;
    local_3c = 0;
    local_38 = 0;
    (**(code **)(*piVar4 + 0x2c))(piVar4,&local_40);
    _ZN11CGameObject11SetDontSaveEb(piVar4,*(undefined1 *)(param_1 + 0x98));
    iVar1 = piVar4[0x36];
    if (iVar1 != 0) {
      *(undefined4 *)(iVar1 + 0xc) = uVar2;
      *(undefined4 *)(iVar1 + 0x10) = uVar18;
      *(undefined4 *)(iVar1 + 0x14) = uVar17;
    }
    _ZN11CGameObject6FadeInEb(piVar4,1);
    fVar6 = (float)_ZN11CGameObject10GetOpacityEv(piVar4);
    if (fVar6 == 0.0) {
      _ZN11CGameObject19ForceNodeVisibilityEb(piVar4,0);
    }
    if (param_5 != 0) {
      local_34 = *param_3;
      local_30 = param_3[1];
      local_2c = (float)param_3[2] + 0.5;
      iVar1 = _ZN13CZonesManager17GetZoneByWorldBoxEN6glitch4core8vector3dIfEEP5CZone
                        (param_1,&local_34,param_5);
      if (iVar1 != 0) {
        param_5 = iVar1;
      }
    }
    _ZN11CGameObject7SetZoneEP5CZoneb(piVar4,param_5,param_6);
  }
  else {
    _ZN6CLevel8GetLevelEv();
    iVar1 = _ZNK6CLevel25GetWantedManagerComponentEv();
    if (iVar1 != 0) {
      iVar8 = *(int *)(iVar1 + 0x7c);
      iVar15 = iVar1 + 0x78;
      iVar10 = iVar15;
      iVar12 = iVar15;
      if (iVar8 != 0) {
LAB_002cdd00:
        piVar5 = *(int **)(iVar8 + 0x10);
        iVar9 = iVar8;
        if (piVar4 >= piVar5 && piVar4 != piVar5) {
          iVar9 = *(int *)(iVar8 + 0xc);
        }
        iVar8 = iVar9;
        if (piVar5 < piVar4) goto LAB_002cdd1c;
        if (piVar4 < piVar5) {
          iVar8 = *(int *)(iVar9 + 8);
          iVar12 = iVar9;
          goto LAB_002cdd1c;
        }
        iVar10 = iVar9;
        iVar8 = *(int *)(iVar9 + 8);
        while (iVar7 = *(int *)(iVar9 + 0xc), iVar8 != 0) {
          if (*(int **)(iVar8 + 0x10) < piVar4) {
            iVar8 = *(int *)(iVar8 + 0xc);
          }
          else {
            iVar10 = iVar8;
            iVar8 = *(int *)(iVar8 + 8);
          }
        }
        while (iVar7 != 0) {
          if (piVar4 < *(int **)(iVar7 + 0x10)) {
            iVar7 = *(int *)(iVar7 + 8);
            iVar12 = iVar7;
          }
          else {
            iVar7 = *(int *)(iVar7 + 0xc);
          }
        }
      }
LAB_002cdd28:
      if ((*(int *)(iVar1 + 0x80) == iVar10) && (iVar15 == iVar12)) {
        _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_bESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE8_M_eraseEPSt13_Rb_tree_nodeIS4_E
                  (iVar1 + 0x74);
        *(int *)(iVar1 + 0x80) = iVar15;
        *(undefined4 *)(iVar1 + 0x7c) = 0;
        *(int *)(iVar1 + 0x84) = iVar15;
        *(undefined4 *)(iVar1 + 0x88) = 0;
      }
      else if (iVar10 != iVar12) {
        do {
          iVar8 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar10);
          _ZSt28_Rb_tree_rebalance_for_erasePSt18_Rb_tree_node_baseRS_(iVar10,iVar1 + 0x78);
          _ZdlPv();
          *(int *)(iVar1 + 0x88) = *(int *)(iVar1 + 0x88) + -1;
          iVar10 = iVar8;
        } while (iVar12 != iVar8);
      }
      iVar8 = *(int *)(iVar1 + 0x94);
      iVar15 = iVar1 + 0x90;
      iVar12 = iVar15;
      iVar10 = iVar15;
      if (iVar8 != 0) {
LAB_002cdda4:
        piVar5 = *(int **)(iVar8 + 0x10);
        iVar9 = iVar8;
        if (piVar4 >= piVar5 && piVar4 != piVar5) {
          iVar9 = *(int *)(iVar8 + 0xc);
        }
        iVar8 = iVar9;
        if (piVar5 < piVar4) goto LAB_002cddc0;
        if (piVar4 < piVar5) {
          iVar8 = *(int *)(iVar9 + 8);
          iVar12 = iVar9;
          goto LAB_002cddc0;
        }
        iVar8 = *(int *)(iVar9 + 8);
        iVar10 = iVar9;
        while (iVar7 = *(int *)(iVar9 + 0xc), iVar8 != 0) {
          if (*(int **)(iVar8 + 0x10) < piVar4) {
            iVar8 = *(int *)(iVar8 + 0xc);
          }
          else {
            iVar8 = *(int *)(iVar8 + 8);
            iVar10 = iVar8;
          }
        }
        while (iVar7 != 0) {
          if (piVar4 < *(int **)(iVar7 + 0x10)) {
            iVar7 = *(int *)(iVar7 + 8);
            iVar12 = iVar7;
          }
          else {
            iVar7 = *(int *)(iVar7 + 0xc);
          }
        }
      }
LAB_002cddcc:
      if ((*(int *)(iVar1 + 0x98) == iVar10) && (iVar15 == iVar12)) {
        _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_bESt10_Select1stIS4_ESt4lessIS1_ESaIS4_EE8_M_eraseEPSt13_Rb_tree_nodeIS4_E
                  (iVar1 + 0x8c);
        *(int *)(iVar1 + 0x98) = iVar15;
        *(undefined4 *)(iVar1 + 0x94) = 0;
        *(int *)(iVar1 + 0x9c) = iVar15;
        *(undefined4 *)(iVar1 + 0xa0) = 0;
      }
      else if (iVar10 != iVar12) {
        do {
          iVar8 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar10);
          _ZSt28_Rb_tree_rebalance_for_erasePSt18_Rb_tree_node_baseRS_(iVar10,iVar1 + 0x90);
          _ZdlPv();
          *(int *)(iVar1 + 0xa0) = *(int *)(iVar1 + 0xa0) + -1;
          iVar10 = iVar8;
        } while (iVar12 != iVar8);
      }
    }
    pcVar13 = *(code **)(*piVar4 + 0x24);
    **(int **)(param_1 + 0x68) = **(int **)(param_1 + 0x68) + 1;
    (*pcVar13)(piVar4);
    (**(code **)(*piVar4 + 0x50))(piVar4,1);
    (**(code **)(*piVar4 + 0x80))(piVar4,1);
    piVar4[3] = *param_3;
    pcVar13 = *(code **)(*piVar4 + 0x28);
    piVar4[4] = param_3[1];
    piVar4[5] = param_3[2];
    (*pcVar13)(piVar4,param_3,1);
    local_40 = 0;
    local_3c = 0;
    local_38 = 0;
    (**(code **)(*piVar4 + 0x2c))(piVar4,&local_40);
    if (param_5 != 0) {
      local_4c = *param_3;
      local_48 = param_3[1];
      local_44 = (float)param_3[2] + 0.5;
      iVar1 = _ZN13CZonesManager17GetZoneByWorldBoxEN6glitch4core8vector3dIfEEP5CZone
                        (param_1,&local_4c,param_5);
      if (iVar1 != 0) {
        param_5 = iVar1;
      }
    }
    _ZN11CGameObject7SetZoneEP5CZoneb(piVar4,param_5,param_6);
    _ZN11CGameObject6ReInitEb(piVar4,1);
    (**(code **)(*piVar4 + 0x78))(piVar4);
    _ZN11CGameObject11SetDontSaveEb(piVar4,*(undefined1 *)(param_1 + 0x98));
    _ZN11CGameObject6FadeInEb(piVar4,1);
    fVar6 = (float)_ZN11CGameObject10GetOpacityEv(piVar4);
    if (fVar6 == 0.0) {
      _ZN11CGameObject19ForceNodeVisibilityEb(piVar4,0);
    }
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_50);
  return piVar4;
LAB_002cdd1c:
  iVar10 = iVar12;
  if (iVar8 == 0) goto LAB_002cdd28;
  goto LAB_002cdd00;
LAB_002cddc0:
  iVar10 = iVar12;
  if (iVar8 == 0) goto LAB_002cddcc;
  goto LAB_002cdda4;
}


