// _ZN13CZonesManager22HandleZoneLoadRequestsEb @ 002d0ee0

/* WARNING: Restarted to delay deadcode elimination for space: stack */

void _ZN13CZonesManager22HandleZoneLoadRequestsEb(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  uint extraout_r3;
  uint extraout_r3_00;
  uint uVar9;
  int iVar10;
  int iVar11;
  int *piVar12;
  int iVar13;
  int iVar14;
  undefined4 *extraout_r12;
  undefined4 *extraout_r12_00;
  int *piVar15;
  bool bVar16;
  uint *puVar17;
  undefined4 *puVar18;
  undefined4 *puVar19;
  undefined4 local_44;
  int *local_40;
  int local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  
  local_2c = CONCAT22(local_2c._2_2_,CONCAT11(local_2c._1_1_,(undefined1)local_2c));
  bVar16 = false;
  iVar7 = DAT_002d14a8 + 0x2d0f00;
  iVar14 = param_1 + 0x20;
  piVar15 = *(int **)(param_1 + 0x34);
  if (*(int **)(param_1 + 0x38) != *(int **)(param_1 + 0x34)) {
    do {
      iVar10 = *(int *)(param_1 + 0x24);
      piVar12 = piVar15 + 1;
      iVar13 = *piVar15;
      iVar5 = iVar14;
      iVar2 = iVar10;
      while (iVar2 != 0) {
        if (*(int *)(iVar2 + 0x10) < iVar13) {
          iVar2 = *(int *)(iVar2 + 0xc);
        }
        else {
          iVar5 = iVar2;
          iVar2 = *(int *)(iVar2 + 8);
        }
      }
      if ((iVar14 != iVar5) && (*(int *)(iVar5 + 0x10) <= iVar13)) goto LAB_002d1010;
      local_38 = 0xffffffff;
      local_34 = 0xffffffff;
      local_30 = 0xffffffff;
      local_2c = local_2c & 0xffff0000;
      iVar2 = iVar14;
      local_3c = iVar13;
      if (iVar14 == iVar5) {
        iVar1 = 0;
        if (*(int *)(param_1 + 0x30) != 0) {
          iVar11 = *(int *)(param_1 + 0x2c);
          iVar1 = *(int *)(iVar11 + 0x10);
          if (iVar1 < iVar13) {
            bVar16 = iVar14 == iVar11;
LAB_002d11f4:
            iVar5 = _Znwj(0x24);
            if ((int *)(iVar5 + 0x10) != (int *)0x0) {
              *(int *)(iVar5 + 0x10) = local_3c;
              *(undefined4 *)(iVar5 + 0x14) = local_38;
              *(undefined4 *)(iVar5 + 0x18) = local_34;
              *(undefined4 *)(iVar5 + 0x1c) = local_30;
              *(uint *)(iVar5 + 0x20) = local_2c;
            }
            goto LAB_002d11b8;
          }
        }
        if (iVar10 == 0) {
LAB_002d131c:
          if (*(int *)(param_1 + 0x28) == iVar2) {
            iVar5 = _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_2910
                              (param_1 + 0x1c,0,iVar2,&local_3c);
            goto LAB_002d1010;
          }
LAB_002d1328:
          iVar5 = _ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(iVar2);
          iVar6 = *(int *)(iVar5 + 0x10);
        }
        else {
          do {
            iVar5 = iVar10;
            iVar6 = *(int *)(iVar5 + 0x10);
            if (iVar13 < iVar6) {
              iVar1 = *(int *)(iVar5 + 8);
            }
            if (iVar13 >= iVar6) {
              iVar1 = *(int *)(iVar5 + 0xc);
            }
            iVar10 = iVar1;
          } while (iVar1 != 0);
          iVar2 = iVar5;
          if (iVar13 < iVar6) goto LAB_002d131c;
        }
LAB_002d128c:
        iVar11 = iVar2;
        if (iVar6 < iVar13) {
          if (iVar14 == iVar11) {
            bVar16 = true;
          }
          else if (iVar13 < *(int *)(iVar11 + 0x10)) {
            bVar16 = true;
          }
          else {
            bVar16 = false;
          }
          iVar5 = _Znwj(0x24);
          if ((int *)(iVar5 + 0x10) != (int *)0x0) {
            *(int *)(iVar5 + 0x10) = local_3c;
            *(undefined4 *)(iVar5 + 0x14) = local_38;
            *(undefined4 *)(iVar5 + 0x18) = local_34;
            *(undefined4 *)(iVar5 + 0x1c) = local_30;
            *(uint *)(iVar5 + 0x20) = local_2c;
          }
LAB_002d11b8:
          _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
                    (bVar16,iVar5,iVar11,iVar14);
          *(int *)(param_1 + 0x30) = *(int *)(param_1 + 0x30) + 1;
        }
      }
      else {
        if (*(int *)(iVar5 + 0x10) <= iVar13) {
          if (*(int *)(iVar5 + 0x10) < iVar13) {
            iVar11 = *(int *)(param_1 + 0x2c);
            if (iVar11 == iVar5) {
              bVar16 = iVar14 == iVar5;
              goto LAB_002d11f4;
            }
            iVar11 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar5);
            iVar1 = *(int *)(iVar11 + 0x10);
            if (iVar13 < iVar1) {
              if (*(int *)(iVar5 + 0xc) == 0) {
                iVar2 = _Znwj(0x24);
                piVar15 = (int *)(iVar2 + 0x10);
                puVar17 = (uint *)0x0;
                uVar9 = extraout_r3_00;
                if (piVar15 != (int *)0x0) {
                  *piVar15 = local_3c;
                  *(undefined4 *)(iVar2 + 0x14) = local_38;
                  *(undefined4 *)(iVar2 + 0x18) = local_34;
                  *(undefined4 *)(iVar2 + 0x1c) = local_30;
                  puVar17 = (uint *)(iVar2 + 0x20);
                  uVar9 = local_2c;
                }
                uVar3 = 0;
                if (piVar15 != (int *)0x0) {
                  *puVar17 = uVar9;
                }
                goto LAB_002d0ff4;
              }
              iVar5 = _Znwj(0x24);
              piVar15 = (int *)(iVar5 + 0x10);
              puVar19 = (undefined4 *)0x0;
              puVar18 = extraout_r12;
              if (piVar15 != (int *)0x0) {
                puVar18 = &local_2c;
                *piVar15 = local_3c;
                *(undefined4 *)(iVar5 + 0x14) = local_38;
                *(undefined4 *)(iVar5 + 0x18) = local_34;
                *(undefined4 *)(iVar5 + 0x1c) = local_30;
                puVar19 = (undefined4 *)(iVar5 + 0x20);
              }
              bVar16 = true;
              if (piVar15 != (int *)0x0) {
                *puVar19 = *puVar18;
              }
              goto LAB_002d11b8;
            }
            if (iVar10 != 0) {
              do {
                iVar5 = iVar10;
                iVar6 = *(int *)(iVar5 + 0x10);
                if (iVar13 < iVar6) {
                  iVar1 = *(int *)(iVar5 + 8);
                }
                if (iVar6 <= iVar13) {
                  iVar1 = *(int *)(iVar5 + 0xc);
                }
                iVar10 = iVar1;
              } while (iVar1 != 0);
              iVar2 = iVar5;
              if (iVar6 <= iVar13) goto LAB_002d128c;
            }
            goto LAB_002d131c;
          }
          goto LAB_002d1010;
        }
        iVar11 = *(int *)(param_1 + 0x28);
        if (iVar11 == iVar5) {
          iVar5 = _Znwj(0x24);
          piVar15 = (int *)(iVar5 + 0x10);
          puVar19 = (undefined4 *)0x0;
          puVar18 = extraout_r12_00;
          if (piVar15 != (int *)0x0) {
            puVar18 = &local_2c;
            *piVar15 = local_3c;
            *(undefined4 *)(iVar5 + 0x14) = local_38;
            *(undefined4 *)(iVar5 + 0x18) = local_34;
            *(undefined4 *)(iVar5 + 0x1c) = local_30;
            puVar19 = (undefined4 *)(iVar5 + 0x20);
          }
          bVar16 = true;
          if (piVar15 != (int *)0x0) {
            *puVar19 = *puVar18;
          }
          goto LAB_002d11b8;
        }
        iVar1 = _ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(iVar5);
        iVar8 = *(int *)(iVar1 + 0x10);
        if (iVar13 <= iVar8) {
          if (iVar10 != 0) {
            do {
              iVar5 = iVar10;
              iVar6 = *(int *)(iVar5 + 0x10);
              if (iVar13 < iVar6) {
                iVar8 = *(int *)(iVar5 + 8);
              }
              if (iVar6 <= iVar13) {
                iVar8 = *(int *)(iVar5 + 0xc);
              }
              iVar10 = iVar8;
            } while (iVar8 != 0);
            iVar2 = iVar5;
            if (iVar6 <= iVar13) goto LAB_002d128c;
          }
          if (iVar11 == iVar2) {
            iVar5 = _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE10_M_insert_EPKSt18_Rb_tree_node_baseSD_RKS4__constprop_2910
                              (param_1 + 0x1c,0,iVar11,&local_3c);
            goto LAB_002d1010;
          }
          goto LAB_002d1328;
        }
        if (*(int *)(iVar1 + 0xc) == 0) {
          bVar16 = iVar14 == iVar1;
          iVar11 = iVar1;
          goto LAB_002d11f4;
        }
        iVar2 = _Znwj(0x24);
        piVar15 = (int *)(iVar2 + 0x10);
        puVar17 = (uint *)0x0;
        uVar9 = extraout_r3;
        if (piVar15 != (int *)0x0) {
          *piVar15 = local_3c;
          *(undefined4 *)(iVar2 + 0x14) = local_38;
          *(undefined4 *)(iVar2 + 0x18) = local_34;
          *(undefined4 *)(iVar2 + 0x1c) = local_30;
          puVar17 = (uint *)(iVar2 + 0x20);
          uVar9 = local_2c;
        }
        uVar3 = 1;
        if (piVar15 != (int *)0x0) {
          *puVar17 = uVar9;
        }
LAB_002d0ff4:
        _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(uVar3,iVar2,iVar5,iVar14);
        *(int *)(param_1 + 0x30) = *(int *)(param_1 + 0x30) + 1;
        iVar5 = iVar2;
      }
LAB_002d1010:
      uVar3 = _ZN6CLevel8GetLevelEv();
      iVar2 = DAT_002d14b0;
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (&local_44,*(undefined4 *)(DAT_002d14ac + 0x2d1024));
      piVar15 = (int *)_Z9GetDevicev();
      (**(code **)(**(int **)(*piVar15 + 0x28) + 0xc))
                (&local_40,*(int **)(*piVar15 + 0x28),local_44);
      (**(code **)(*local_40 + 0x18))(local_40,*(undefined4 *)(iVar5 + 0x18),0);
      uVar4 = _ZnajPKci(*(undefined4 *)(iVar5 + 0x1c),iVar7,0x642);
      (**(code **)(*local_40 + 0xc))(local_40,uVar4,*(undefined4 *)(iVar5 + 0x1c));
      iVar10 = _ZnwjPKci(0x38,iVar7,0x644);
      _ZN13CMemoryStreamC1EPKvjb(iVar10,uVar4,*(undefined4 *)(iVar5 + 0x1c),1);
      piVar15 = *(int **)(iVar2 + 0x2d10bc);
      *piVar15 = iVar10;
      _ZN13CMemoryStream13SetDictionaryERSt6vectorISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESaIS9_EERS0_ISbIwS1_IwENS5_IwLS7_0EEEESaISF_EEb
                (iVar10,param_1,param_1 + 0xc,*(undefined1 *)(param_1 + 0x18));
      if (local_40 != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (&local_44);
      *(undefined1 *)(iVar5 + 0x21) = 1;
      do {
        iVar5 = _ZN6CLevel24LoadZoneFromMemoryStreamEv(uVar3);
      } while (iVar5 == 0);
      _ZN13CMemoryStream7EndReadEv(*piVar15);
      iVar5 = *piVar15;
      if (iVar5 != 0) {
        _ZN13CMemoryStreamD2Ev(iVar5);
        _ZdlPv(iVar5);
        *piVar15 = 0;
      }
      bVar16 = true;
      piVar15 = piVar12;
    } while (*(int **)(param_1 + 0x38) != piVar12);
  }
  if (bVar16) {
    iVar7 = *(int *)(*(int *)(param_1 + 0x80) +
                    ((*(int *)(param_1 + 0x84) - *(int *)(param_1 + 0x80) >> 2) + -1) * 4);
    _ZN5CZone5Init1Ev(iVar7);
    _ZN5CZone5Init2Ev(iVar7);
    *(int *)(iVar7 + 0x154) = *(int *)(iVar7 + 0x154) + 1;
    if ((param_2 != 0) && (*(char *)(iVar7 + 0x17c) != '\0')) {
      if (0 < *(int *)(iVar7 + 0x178)) {
        _ZN17CLuaScriptManager13StartFunctionEiiP11ScriptParamP15CGameObjectBaseiii
                  (**(undefined4 **)(DAT_002d14b4 + 0x2d13ac),*(int *)(iVar7 + 0x178),0,0,0,
                   0xffffffff,0xffffffff,2);
      }
      *(undefined1 *)(iVar7 + 0x17c) = 0;
    }
  }
  *(undefined4 *)(param_1 + 0x38) = *(undefined4 *)(param_1 + 0x34);
  return;
}


