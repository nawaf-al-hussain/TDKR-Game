// _ZN13CZonesManager5ResetEv @ 002ccbb4

void _ZN13CZonesManager5ResetEv(int param_1)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int *piVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int *piVar10;
  int iVar11;
  int iVar12;
  undefined4 *puVar13;
  int iVar14;
  int iStack_40;
  undefined1 auStack_30 [4];
  int *apiStack_2c [2];
  
  iVar8 = DAT_002ccbd8;
  *(undefined4 *)(param_1 + 0x6c) = 0;
  iVar8 = *(int *)(iVar8 + 0x2ccbc8);
  *(undefined1 *)(param_1 + 0x7c) = 0;
  *(undefined1 *)(param_1 + 0x98) = 0;
  *(undefined1 *)(param_1 + 0x7d) = 0;
  iVar3 = *(int *)(iVar8 + 0x68);
  _ZN13CZonesManager20UpdateAddRemoveListsEv(**(undefined4 **)(DAT_001fbe68 + 0x1fbb0c));
  iVar9 = *(int *)(iVar3 + 4);
  iVar8 = *(int *)(iVar3 + 8) - iVar9 >> 2;
  iVar11 = iVar8 + -1;
  if (iVar11 < 0) {
    return;
  }
  iVar8 = (iVar8 + 0x3fffffff) * 4;
  piVar5 = (int *)(DAT_001fbe6c + 0x1fbb48);
  iVar6 = DAT_001fbe70 + 0x1fbb54;
  do {
    piVar10 = *(int **)(iVar9 + iVar8);
    (**(code **)(*piVar10 + 0x50))(piVar10,0);
    (**(code **)(*piVar10 + 0x80))(piVar10,0);
    _ZN11CGameObject9SetHealthEf(piVar10,0);
    iVar14 = *piVar5;
    iVar12 = iVar14 + 0xb0;
    iVar4 = *(int *)(iVar14 + 0xb4);
    iVar9 = iVar12;
    iVar7 = iVar4;
    while (iVar7 != 0) {
      if (*(int **)(iVar7 + 0x10) < piVar10) {
        iVar7 = *(int *)(iVar7 + 0xc);
      }
      else {
        iVar9 = iVar7;
        iVar7 = *(int *)(iVar7 + 8);
      }
    }
    iVar7 = iVar12;
    if ((iVar12 != iVar9) && (iVar7 = iVar9, piVar10 < *(int **)(iVar9 + 0x10))) {
      iVar7 = iVar12;
    }
    if (iVar12 != iVar7) {
      iVar9 = iVar12;
      iStack_40 = iVar12;
      if (iVar4 != 0) {
LAB_001fbc04:
        piVar1 = *(int **)(iVar4 + 0x10);
        iVar7 = iVar4;
        if (piVar10 >= piVar1 && piVar10 != piVar1) {
          iVar7 = *(int *)(iVar4 + 0xc);
        }
        iVar4 = iVar7;
        if (piVar1 < piVar10) break;
        if (piVar10 < piVar1) {
          iVar4 = *(int *)(iVar7 + 8);
          iVar9 = iVar7;
          break;
        }
        iStack_40 = iVar7;
        iVar4 = *(int *)(iVar7 + 8);
        while (iVar2 = *(int *)(iVar7 + 0xc), iVar4 != 0) {
          if (*(int **)(iVar4 + 0x10) < piVar10) {
            iVar4 = *(int *)(iVar4 + 0xc);
          }
          else {
            iStack_40 = iVar4;
            iVar4 = *(int *)(iVar4 + 8);
          }
        }
        while (iVar2 != 0) {
          if (piVar10 < *(int **)(iVar2 + 0x10)) {
            iVar2 = *(int *)(iVar2 + 8);
            iVar9 = iVar2;
          }
          else {
            iVar2 = *(int *)(iVar2 + 0xc);
          }
        }
        if (iStack_40 == *(int *)(iVar14 + 0xb8)) goto LAB_001fbdac;
        goto LAB_001fbc38;
      }
LAB_001fbc2c:
      iVar9 = iStack_40;
      if (iStack_40 == *(int *)(iVar14 + 0xb8)) {
LAB_001fbdac:
        if (iVar12 != iVar9) goto LAB_001fbc38;
        _ZNSt8_Rb_treeIP11CGameObjectS1_St9_IdentityIS1_ESt4lessIS1_ESaIS1_EE8_M_eraseEPSt13_Rb_tree_nodeIS1_E
                  (iVar14 + 0xac);
        *(int *)(iVar14 + 0xb8) = iVar12;
        *(undefined4 *)(iVar14 + 0xb4) = 0;
        *(int *)(iVar14 + 0xbc) = iVar12;
        *(undefined4 *)(iVar14 + 0xc0) = 0;
      }
      else {
LAB_001fbc38:
        if (iStack_40 != iVar9) {
          do {
            iVar7 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iStack_40);
            _ZSt28_Rb_tree_rebalance_for_erasePSt18_Rb_tree_node_baseRS_(iStack_40,iVar14 + 0xb0);
            _ZdlPv();
            *(int *)(iVar14 + 0xc0) = *(int *)(iVar14 + 0xc0) + -1;
            iStack_40 = iVar7;
          } while (iVar9 != iVar7);
        }
      }
      iVar4 = iVar14 + 0xf8;
      iVar9 = iVar4;
      iVar7 = *(int *)(iVar14 + 0xfc);
      while (iVar7 != 0) {
        if (*(int **)(iVar7 + 0x10) < piVar10) {
          iVar7 = *(int *)(iVar7 + 0xc);
        }
        else {
          iVar9 = iVar7;
          iVar7 = *(int *)(iVar7 + 8);
        }
      }
      if ((iVar4 != iVar9) && (piVar10 < *(int **)(iVar9 + 0x10))) {
        iVar9 = iVar4;
      }
      if (iVar4 != iVar9) {
        apiStack_2c[0] = piVar10;
        _ZNSt3setIP11CGameObjectSt4lessIS1_ESaIS1_EE5eraseERKS1_(iVar14 + 0xf4,apiStack_2c);
        if ((apiStack_2c[0][0x2b] != 0) && (*(int *)(apiStack_2c[0][0x2b] + 0x18) == 3)) {
          for (puVar13 = *(undefined4 **)(iVar14 + 0x124); puVar13 != (undefined4 *)(iVar14 + 0x124)
              ; puVar13 = (undefined4 *)*puVar13) {
            if (apiStack_2c[0] == (int *)puVar13[5]) {
              _ZNSt8__detail15_List_node_base9_M_unhookEv(puVar13);
              _ZdlPv(puVar13);
              *(int *)(iVar14 + 0x110) = *(int *)(iVar14 + 0x110) + -1;
              break;
            }
          }
        }
        _ZN11CGameObject13SetAwareStateEi(apiStack_2c[0],0);
        (**(code **)(*apiStack_2c[0] + 0x14))();
      }
      if (piVar10 == *(int **)(iVar14 + 0x114)) {
        *(undefined4 *)(iVar14 + 0x114) = 0;
      }
    }
    (**(code **)(*piVar10 + 0x14))(piVar10);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2100
              (auStack_30,iVar6);
    _ZN11CGameObject4KillESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEbPS_
              (piVar10,auStack_30,1,0);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_30);
    iVar9 = (**(code **)(*piVar10 + 0xa0))(piVar10);
    if (iVar9 != 0) {
      _ZN11CGameObject7SetZoneEP5CZoneb(piVar10,0,1);
    }
    iVar11 = iVar11 + -1;
    iVar8 = iVar8 + -4;
    if (iVar11 < 0) {
      return;
    }
    iVar9 = *(int *)(iVar3 + 4);
  } while( true );
  iStack_40 = iVar9;
  if (iVar4 == 0) goto LAB_001fbc2c;
  goto LAB_001fbc04;
}


