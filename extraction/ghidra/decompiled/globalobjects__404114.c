// _ZN6CLevel17LoadGlobalObjectsEP13CMemoryStream @ 00404114

void _ZN6CLevel17LoadGlobalObjectsEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  bool bVar14;
  int local_4c;
  int local_48;
  int local_44;
  int local_40;
  char local_2d;
  int local_2c [2];
  
  iVar13 = *(int *)(param_1 + 0xb84);
  iVar1 = (*(int *)(param_1 + 0xb88) - iVar13 >> 3) * -0x55555555;
  if (0 < iVar1) {
    local_44 = 0;
    local_40 = 0;
    while( true ) {
      iVar13 = iVar13 + local_44;
      iVar3 = *(int *)(iVar13 + 8);
      while (iVar3 != 0) {
        iVar12 = *(int *)(iVar3 + 0xc);
        while (iVar12 != 0) {
          iVar11 = *(int *)(iVar12 + 0xc);
          while (iVar11 != 0) {
            iVar10 = *(int *)(iVar11 + 0xc);
            while (iVar10 != 0) {
              iVar9 = *(int *)(iVar10 + 0xc);
              while (iVar9 != 0) {
                iVar8 = *(int *)(iVar9 + 0xc);
                while (iVar8 != 0) {
                  iVar7 = *(int *)(iVar8 + 0xc);
                  while (iVar7 != 0) {
                    iVar6 = *(int *)(iVar7 + 0xc);
                    while (iVar6 != 0) {
                      iVar5 = *(int *)(iVar6 + 0xc);
                      while (iVar5 != 0) {
                        _ZNSt8_Rb_treeIiSt4pairIKibESt10_Select1stIS2_ESt4lessIiESaIS2_EE8_M_eraseEPSt13_Rb_tree_nodeIS2_E
                                  (iVar13,*(undefined4 *)(iVar5 + 0xc));
                        iVar4 = *(int *)(iVar5 + 8);
                        _ZdlPv(iVar5);
                        iVar5 = iVar4;
                      }
                      iVar5 = *(int *)(iVar6 + 8);
                      _ZdlPv(iVar6);
                      iVar6 = iVar5;
                    }
                    iVar6 = *(int *)(iVar7 + 8);
                    _ZdlPv(iVar7);
                    iVar7 = iVar6;
                  }
                  iVar7 = *(int *)(iVar8 + 8);
                  _ZdlPv(iVar8);
                  iVar8 = iVar7;
                }
                iVar8 = *(int *)(iVar9 + 8);
                _ZdlPv(iVar9);
                iVar9 = iVar8;
              }
              iVar9 = *(int *)(iVar10 + 8);
              _ZdlPv(iVar10);
              iVar10 = iVar9;
            }
            iVar10 = *(int *)(iVar11 + 8);
            _ZdlPv(iVar11);
            iVar11 = iVar10;
          }
          iVar11 = *(int *)(iVar12 + 8);
          _ZdlPv(iVar12);
          iVar12 = iVar11;
        }
        iVar12 = *(int *)(iVar3 + 8);
        _ZdlPv(iVar3);
        iVar3 = iVar12;
      }
      local_40 = local_40 + 1;
      *(int *)(iVar13 + 0xc) = iVar13 + 4;
      *(undefined4 *)(iVar13 + 8) = 0;
      *(int *)(iVar13 + 0x10) = iVar13 + 4;
      local_44 = local_44 + 0x18;
      *(undefined4 *)(iVar13 + 0x14) = 0;
      if (local_40 == iVar1) break;
      iVar13 = *(int *)(param_1 + 0xb84);
    }
  }
  iVar1 = _ZN13CMemoryStream7ReadIntEv(param_2);
  if (0 < iVar1) {
    local_4c = 0;
    local_44 = 0;
    do {
      iVar13 = _ZN13CMemoryStream7ReadIntEv(param_2);
      if (0 < iVar13) {
        local_48 = 0;
        do {
          _ZN13CMemoryStream4ReadERi(param_2,local_2c);
          _ZN13CMemoryStream4ReadERb(param_2,&local_2d);
          iVar11 = local_2c[0];
          iVar9 = *(int *)(param_1 + 0xb84) + local_4c;
          iVar8 = iVar9 + 4;
          iVar10 = *(int *)(iVar9 + 8);
          iVar3 = iVar8;
          iVar12 = iVar10;
          while (iVar12 != 0) {
            if (*(int *)(iVar12 + 0x10) < local_2c[0]) {
              iVar12 = *(int *)(iVar12 + 0xc);
            }
            else {
              iVar3 = iVar12;
              iVar12 = *(int *)(iVar12 + 8);
            }
          }
          if (iVar8 == iVar3) {
            if ((*(int *)(iVar9 + 0x14) == 0) ||
               (iVar12 = *(int *)(iVar9 + 0x10), local_2c[0] <= *(int *)(iVar12 + 0x10))) {
              iVar12 = iVar8;
              if (iVar10 == 0) {
LAB_00404560:
                iVar6 = *(int *)(iVar9 + 0xc);
                if (iVar6 == iVar12) {
                  if (iVar8 == iVar12) goto LAB_00404688;
                  if (local_2c[0] < *(int *)(iVar12 + 0x10)) {
                    bVar14 = true;
                    iVar12 = iVar6;
                  }
                  else {
                    bVar14 = false;
                    iVar12 = iVar6;
                  }
                  goto LAB_00404518;
                }
LAB_0040456c:
                iVar7 = _ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(iVar12);
                iVar3 = *(int *)(iVar7 + 0x10);
              }
              else {
                do {
                  iVar7 = iVar10;
                  iVar3 = *(int *)(iVar7 + 0x10);
                  if (local_2c[0] < iVar3) {
                    iVar10 = *(int *)(iVar7 + 8);
                  }
                  else {
                    iVar10 = *(int *)(iVar7 + 0xc);
                  }
                } while (iVar10 != 0);
                iVar12 = iVar7;
                if (local_2c[0] < iVar3) goto LAB_00404560;
              }
LAB_00404584:
              if (iVar11 <= iVar3) goto LAB_0040445c;
              if (iVar8 == iVar12) {
                bVar14 = true;
              }
              else if (iVar11 < *(int *)(iVar12 + 0x10)) {
                bVar14 = true;
              }
              else {
                bVar14 = false;
              }
              iVar7 = _Znwj(0x18);
              if (iVar7 != -0x10) {
                *(int *)(iVar7 + 0x10) = iVar11;
                *(undefined1 *)(iVar7 + 0x14) = 0;
              }
            }
            else {
              bVar14 = iVar8 == iVar12;
LAB_00404518:
              iVar7 = _Znwj(0x18);
              if (iVar7 != -0x10) {
                *(int *)(iVar7 + 0x10) = iVar11;
                *(undefined1 *)(iVar7 + 0x14) = 0;
              }
            }
LAB_00404540:
            _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
                      (bVar14,iVar7,iVar12,iVar8);
            *(int *)(iVar9 + 0x14) = *(int *)(iVar9 + 0x14) + 1;
          }
          else {
            iVar7 = iVar3;
            if (local_2c[0] < *(int *)(iVar3 + 0x10)) {
              iVar6 = *(int *)(iVar9 + 0xc);
              if (iVar6 == iVar3) {
                iVar7 = _Znwj(0x18);
                if (iVar7 != -0x10) {
                  *(int *)(iVar7 + 0x10) = iVar11;
                  *(undefined1 *)(iVar7 + 0x14) = 0;
                }
                bVar14 = true;
                iVar12 = iVar6;
              }
              else {
                iVar12 = _ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(iVar3);
                if (iVar11 <= *(int *)(iVar12 + 0x10)) {
                  iVar12 = iVar8;
                  if (iVar10 != 0) {
                    do {
                      iVar7 = iVar10;
                      iVar3 = *(int *)(iVar7 + 0x10);
                      if (iVar11 < iVar3) {
                        iVar10 = *(int *)(iVar7 + 8);
                      }
                      else {
                        iVar10 = *(int *)(iVar7 + 0xc);
                      }
                    } while (iVar10 != 0);
                    iVar12 = iVar7;
                    if (iVar3 <= iVar11) goto LAB_00404584;
                  }
                  if (iVar6 != iVar12) goto LAB_0040456c;
                  if (iVar8 != iVar6) {
                    bVar14 = iVar11 < *(int *)(iVar6 + 0x10);
                    iVar12 = iVar6;
                    goto LAB_00404518;
                  }
LAB_00404688:
                  bVar14 = true;
                  iVar12 = iVar6;
                  goto LAB_00404518;
                }
                if (*(int *)(iVar12 + 0xc) != 0) {
                  iVar7 = _Znwj(0x18);
                  if (iVar7 != -0x10) {
                    *(int *)(iVar7 + 0x10) = iVar11;
                    *(undefined1 *)(iVar7 + 0x14) = 0;
                  }
                  _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
                            (1,iVar7,iVar3,iVar8);
                  *(int *)(iVar9 + 0x14) = *(int *)(iVar9 + 0x14) + 1;
                  goto LAB_0040445c;
                }
                bVar14 = iVar8 == iVar12;
                iVar7 = _Znwj(0x18);
                if (iVar7 != -0x10) {
                  *(int *)(iVar7 + 0x10) = iVar11;
                  *(undefined1 *)(iVar7 + 0x14) = 0;
                }
              }
              goto LAB_00404540;
            }
          }
LAB_0040445c:
          iVar3 = *(int *)(param_1 + 0xc0);
          *(char *)(iVar7 + 0x14) = local_2d;
          if (((iVar3 == local_44) &&
              (piVar2 = (int *)_ZN13CZonesManager10FindObjectEit
                                         (**(undefined4 **)(DAT_00404720 + 0x40464c),local_2c[0],
                                          0x11), piVar2 != (int *)0x0)) &&
             ((**(code **)(*piVar2 + 0x50))(piVar2,local_2d), local_2d == '\0')) {
            (**(code **)(*piVar2 + 0x80))(piVar2);
          }
          local_48 = local_48 + 1;
        } while (local_48 != iVar13);
      }
      local_44 = local_44 + 1;
      local_4c = local_4c + 0x18;
    } while (local_44 != iVar1);
  }
  return;
}


