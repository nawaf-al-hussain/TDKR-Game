// _ZN6glitch7collada23IParametricController1dC1ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE @ 0077486c

/* WARNING: Restarted to delay deadcode elimination for space: stack */

int * _ZN6glitch7collada23IParametricController1dC1ERKNS0_9anim_pack21SParametricControllerERKN5boost13intrusive_ptrINS0_20IAnimationDictionaryEEE
                (int *param_1,undefined4 *param_2,undefined4 *param_3)

{
  int iVar1;
  uint uVar2;
  int *piVar3;
  undefined4 uVar4;
  int iVar5;
  undefined4 uVar6;
  int *piVar7;
  int iVar8;
  int *piVar9;
  int *piVar10;
  int iVar11;
  uint *puVar12;
  int iVar13;
  int iVar14;
  uint uVar15;
  int iVar16;
  int iVar17;
  uint uVar18;
  int iVar19;
  bool bVar20;
  float fVar21;
  float fVar22;
  float fVar23;
  undefined8 uVar24;
  int *local_84;
  int local_6c;
  int local_68;
  int *local_64 [2];
  int *local_5c [2];
  int *local_54 [2];
  uint local_4c;
  float local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  
  iVar8 = DAT_00775058 + 0x77488c;
  uVar4 = *param_2;
  param_1[1] = 0;
  *param_1 = iVar8;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1119
            (param_1 + 2,uVar4);
  piVar9 = (int *)*param_3;
  iVar8 = param_2[1];
  param_1[4] = (int)piVar9;
  param_1[3] = iVar8;
  if (piVar9 != (int *)0x0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE
              ((int)piVar9 + *(int *)(*piVar9 + -0xc) + 4);
  }
  iVar8 = DAT_0077505c;
  piVar9 = param_1 + 10;
  piVar7 = param_1 + 0x13;
  *(undefined1 *)(param_1 + 5) = 0;
  param_1[6] = 0;
  *param_1 = iVar8 + 0x7748f0;
  param_1[7] = 0;
  param_1[8] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xe] = 0;
  param_1[0xc] = (int)piVar9;
  param_1[0xd] = (int)piVar9;
  param_1[0xf] = 0;
  param_1[0x10] = 0;
  param_1[0x11] = 0;
  param_1[0x13] = 0;
  param_1[0x14] = 0;
  param_1[0x17] = 0;
  param_1[0x15] = (int)piVar7;
  param_1[0x16] = (int)piVar7;
  param_1[0x18] = 0;
  iVar8 = param_2[6];
  uVar18 = *(uint *)(iVar8 + 4);
  bVar20 = uVar18 == 0xccccccc;
  if (0xccccccc < uVar18) {
    uVar24 = _ZSt20__throw_length_errorPKc((int)&DAT_00775058 + DAT_00775060);
    piVar9 = (int *)uVar24;
    if (bVar20) {
      *(undefined8 *)((int)piVar7 - ((int)piVar7 >> 0xb)) = uVar24;
    }
    iVar8 = piVar9[0x18];
    *piVar9 = DAT_00775150 + 0x775088;
    if (iVar8 != 0) {
      for (iVar11 = iVar8 + *(int *)(iVar8 + -4) * 0xc; iVar8 != iVar11; iVar11 = iVar11 + -0xc) {
        if (*(int *)(iVar11 + -0xc) != 0) {
          _ZdlPv();
        }
      }
      _ZdaPv(iVar8 + -8);
    }
    _ZNSt8_Rb_treeIjjSt9_IdentityIjESt4lessIjESaIjEE8_M_eraseEPSt13_Rb_tree_nodeIjE
              (piVar9 + 0x12,piVar9[0x14]);
    if (piVar9[0xf] != 0) {
      _ZdlPv();
    }
    _ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE8_M_eraseEPSt13_Rb_tree_nodeIS2_E
              (piVar9 + 9,piVar9[0xb]);
    if (piVar9[6] != 0) {
      _ZdlPv();
    }
    piVar7 = (int *)piVar9[4];
    *piVar9 = DAT_00775154 + 0x775120;
    if (piVar7 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)piVar7 + *(int *)(*piVar7 + -0xc));
    }
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (piVar9 + 2);
    *piVar9 = (int)&DAT_00775150 + DAT_00775158;
    return piVar9;
  }
  if (uVar18 == 0) {
    iVar11 = 0;
  }
  else {
    iVar1 = _Znwj(uVar18 * 0x14);
    if (param_1[6] != 0) {
      _ZdlPv();
    }
    iVar19 = *(int *)(iVar8 + 4);
    param_1[6] = iVar1;
    param_1[7] = iVar1;
    param_1[8] = iVar1 + uVar18 * 0x14;
    iVar11 = iVar1;
    if (0 < iVar19) {
      iVar16 = 0;
      iVar17 = 0;
      iVar5 = 0;
      do {
        iVar14 = *(int *)(iVar8 + 8) + iVar16;
        iVar13 = *(int *)(*(int *)(iVar8 + 8) + iVar16);
        uVar4 = *(undefined4 *)(iVar14 + 0x10);
        local_40 = 0;
        local_3c = 0;
        *(undefined1 *)(param_1 + 5) = 0;
        local_38 = 0;
        uVar18 = (iVar5 >> 2) * -0x33333333;
        local_44 = 0;
        uVar2 = uVar18 + 1;
        local_34 = 0;
        if (uVar18 < uVar2) {
          _ZNSt6vectorIN6glitch7collada23IParametricController1d7SVertexESaIS3_EE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPS3_S5_EEjRKS3_
                    (param_1 + 6,iVar1,1,&local_44);
          iVar1 = param_1[7];
        }
        else if (uVar18 != uVar2) {
          iVar1 = iVar11 + uVar2 * 0x14;
          param_1[7] = iVar1;
        }
        piVar10 = (int *)param_1[0xb];
        *(undefined4 *)(iVar1 + -0x10) = *(undefined4 *)(iVar14 + 4);
        uVar6 = *(undefined4 *)(iVar14 + 8);
        *(int *)(iVar1 + -0x14) = iVar13;
        *(undefined4 *)(iVar1 + -0xc) = uVar6;
        uVar6 = *(undefined4 *)(iVar14 + 0xc);
        *(undefined4 *)(iVar1 + -4) = uVar4;
        *(undefined4 *)(iVar1 + -8) = uVar6;
        piVar3 = piVar9;
        while (piVar10 != (int *)0x0) {
          if (piVar10[4] < iVar13) {
            piVar10 = (int *)piVar10[3];
          }
          else {
            piVar3 = piVar10;
            piVar10 = (int *)piVar10[2];
          }
        }
        if ((piVar9 == piVar3) || (iVar13 < piVar3[4])) {
          piVar10 = param_1 + 9;
          local_68 = 0;
          local_6c = iVar13;
          if (piVar9 == piVar3) {
            if ((param_1[0xe] == 0) || (local_84 = (int *)param_1[0xd], iVar13 <= local_84[4])) {
              _ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE16_M_insert_uniqueERKS2__constprop_1472
                        (local_64,piVar10,&local_6c);
              iVar1 = param_1[7];
              piVar3 = local_64[0];
            }
            else {
LAB_00774f2c:
              bVar20 = piVar9 == local_84;
              piVar3 = (int *)_Znwj(0x18);
              if (piVar3 + 4 != (int *)0x0) {
                piVar3[4] = local_6c;
                piVar3[5] = local_68;
              }
LAB_00774d38:
              _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
                        (bVar20,piVar3,local_84,piVar9);
              iVar1 = param_1[7];
              param_1[0xe] = param_1[0xe] + 1;
            }
          }
          else if (iVar13 < piVar3[4]) {
            if ((int *)param_1[0xc] == piVar3) {
              piVar3 = (int *)_ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE10_M_insert_EPKSt18_Rb_tree_node_baseSB_RKS2__constprop_1468
                                        (piVar10,piVar3,piVar3,&local_6c);
              iVar1 = param_1[7];
            }
            else {
              local_84 = (int *)_ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base(piVar3);
              if (local_84[4] < iVar13) {
                if (local_84[3] == 0) goto LAB_00774f2c;
                piVar10 = (int *)_Znwj(0x18);
                if (piVar10 + 4 != (int *)0x0) {
                  piVar10[4] = local_6c;
                  piVar10[5] = local_68;
                }
                _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
                          (1,piVar10,piVar3,piVar9);
                iVar1 = param_1[7];
                param_1[0xe] = param_1[0xe] + 1;
                piVar3 = piVar10;
              }
              else {
                _ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE16_M_insert_uniqueERKS2__constprop_1472
                          (local_5c,piVar10,&local_6c);
                iVar1 = param_1[7];
                piVar3 = local_5c[0];
              }
            }
          }
          else if (piVar3[4] < iVar13) {
            if ((int *)param_1[0xd] != piVar3) {
              local_84 = (int *)_ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(piVar3);
              if (local_84[4] <= iVar13) {
                _ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE16_M_insert_uniqueERKS2__constprop_1472
                          (local_54,piVar10,&local_6c);
                iVar1 = param_1[7];
                piVar3 = local_54[0];
                goto LAB_00774b38;
              }
              if (piVar3[3] != 0) {
                piVar3 = (int *)_Znwj(0x18);
                if (piVar3 + 4 != (int *)0x0) {
                  piVar3[4] = local_6c;
                  piVar3[5] = local_68;
                }
                bVar20 = true;
                goto LAB_00774d38;
              }
            }
            piVar3 = (int *)_ZNSt8_Rb_treeIiSt4pairIKiiESt10_Select1stIS2_ESt4lessIiESaIS2_EE10_M_insert_EPKSt18_Rb_tree_node_baseSB_RKS2__constprop_1468
                                      (piVar10,0,piVar3,&local_6c);
            iVar1 = param_1[7];
          }
        }
LAB_00774b38:
        iVar11 = param_1[6];
        iVar17 = iVar17 + 1;
        iVar16 = iVar16 + 0x14;
        iVar5 = iVar1 - iVar11;
        piVar3[5] = (iVar5 >> 2) * -0x33333333 + -1;
      } while (iVar17 != iVar19);
    }
  }
  iVar1 = *(int *)(iVar8 + 0xc);
  if (iVar1 < 1) {
    return param_1;
  }
  iVar19 = 0;
  do {
    uVar2 = (uint)*(ushort *)(*(int *)(iVar8 + 0x10) + iVar19 * 4);
    uVar18 = (uint)*(ushort *)(*(int *)(iVar8 + 0x10) + iVar19 * 4 + 2);
    *(undefined1 *)(param_1 + 5) = 0;
    iVar5 = iVar11 + uVar2 * 0x14;
    fVar23 = *(float *)(iVar5 + 0x10);
    iVar11 = iVar11 + uVar18 * 0x14;
    uVar2 = uVar2 * 0x40001 & 0xffff;
    uVar18 = uVar18 * 0x40001 & 0xffff;
    if (fVar23 < 0.0) {
      fVar23 = (float)(**(code **)(*param_1 + 0x14))(param_1,iVar5 + 4);
      *(float *)(iVar5 + 0x10) = fVar23;
    }
    fVar21 = *(float *)(iVar11 + 0x10);
    if (fVar21 < 0.0) {
      fVar21 = (float)(**(code **)(*param_1 + 0x14))(param_1,iVar11 + 4);
      *(float *)(iVar11 + 0x10) = fVar21;
      fVar23 = *(float *)(iVar5 + 0x10);
    }
    uVar15 = uVar2;
    fVar22 = fVar21;
    if (0.5 < ABS(fVar21 - fVar23) == fVar21 < fVar23) {
      uVar15 = uVar18;
      uVar18 = uVar2;
      fVar22 = fVar23;
      fVar23 = fVar21;
    }
    piVar9 = (int *)param_1[0x14];
    local_4c = uVar18 | uVar15 << 0x10;
    piVar3 = piVar7;
    piVar10 = piVar9;
    while (piVar10 != (int *)0x0) {
      if ((uint)piVar10[4] < local_4c) {
        piVar10 = (int *)piVar10[3];
      }
      else {
        piVar3 = piVar10;
        piVar10 = (int *)piVar10[2];
      }
    }
    piVar10 = piVar7;
    if ((piVar7 != piVar3) && (piVar10 = piVar3, local_4c < (uint)piVar3[4])) {
      piVar10 = piVar7;
    }
    if (piVar7 == piVar10) {
      if (fVar23 < fVar22) {
        fVar23 = fVar23 + 1.0;
      }
      fVar22 = fVar23 - fVar22;
      if (0.0 < fVar22) {
        fVar23 = 1.0;
      }
      else {
        local_48 = 1.0;
      }
      puVar12 = (uint *)param_1[0x10];
      if (0.0 < fVar22) {
        local_48 = fVar23 / fVar22;
      }
      if (puVar12 == (uint *)param_1[0x11]) {
        _ZNSt6vectorIN6glitch7collada23IParametricController1d8SSegmentESaIS3_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS3_S5_EERKS3_
                  (param_1 + 0xf,puVar12,&local_4c);
        piVar9 = (int *)param_1[0x14];
      }
      else {
        if (puVar12 != (uint *)0x0) {
          *puVar12 = local_4c;
          puVar12[1] = (uint)local_48;
        }
        param_1[0x10] = (int)(puVar12 + 2);
      }
      piVar3 = piVar7;
      if (piVar9 == (int *)0x0) {
LAB_00774ec8:
        piVar10 = (int *)param_1[0x15];
        if (piVar10 != piVar3) {
          iVar11 = _ZSt18_Rb_tree_decrementPSt18_Rb_tree_node_base(piVar3);
          uVar18 = *(uint *)(iVar11 + 0x10);
          piVar10 = piVar3;
          goto LAB_00774dec;
        }
        if (piVar7 == piVar3) {
          uVar4 = 1;
        }
        else if (local_4c < (uint)piVar3[4]) {
          uVar4 = 1;
        }
        else {
          uVar4 = 0;
        }
        iVar11 = _Znwj(0x14);
        if (iVar11 != -0x10) {
          *(uint *)(iVar11 + 0x10) = local_4c;
        }
      }
      else {
        do {
          piVar10 = piVar9;
          uVar18 = piVar10[4];
          if (local_4c < uVar18) {
            piVar9 = (int *)piVar10[2];
          }
          else {
            piVar9 = (int *)piVar10[3];
          }
        } while (piVar9 != (int *)0x0);
        piVar3 = piVar10;
        if (local_4c < uVar18) goto LAB_00774ec8;
LAB_00774dec:
        if (local_4c <= uVar18) goto joined_r0x00774e5c;
        if (piVar7 == piVar10) {
          uVar4 = 1;
        }
        else if (local_4c < (uint)piVar10[4]) {
          uVar4 = 1;
        }
        else {
          uVar4 = 0;
        }
        iVar11 = _Znwj(0x14);
        if (iVar11 != -0x10) {
          *(uint *)(iVar11 + 0x10) = local_4c;
        }
      }
      _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_(uVar4,iVar11,piVar10,piVar7)
      ;
      param_1[0x17] = param_1[0x17] + 1;
    }
joined_r0x00774e5c:
    if (iVar19 + 1 == iVar1) {
      return param_1;
    }
    iVar19 = iVar19 + 1;
    iVar11 = param_1[6];
  } while( true );
}


