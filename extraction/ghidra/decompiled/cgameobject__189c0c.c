// _ZN13CAIController23getGadgetZoomCandidatesEiRKN6glitch4core6line3dIfEEfRSt3mapIfP11CGameObjectSt4lessIfESaISt4pairIKfS8_EEERS6_IS8_NS1_8vector3dIfEES9_IS8_ESaISB_IKS8_SI_EEE @ 00189c0c

/* WARNING: Type propagation algorithm not settling */

void _ZN13CAIController23getGadgetZoomCandidatesEiRKN6glitch4core6line3dIfEEfRSt3mapIfP11CGameObjectSt4lessIfESaISt4pairIKfS8_EEERS6_IS8_NS1_8vector3dIfEES9_IS8_ESaISB_IKS8_SI_EEE
               (int param_1,int param_2,float *param_3,float param_4,int param_5,int param_6)

{
  float fVar1;
  float fVar2;
  int iVar3;
  float extraout_r0;
  int iVar4;
  float fVar5;
  float extraout_r0_00;
  float extraout_r0_01;
  int *piVar6;
  float *pfVar7;
  int iVar8;
  int *piVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  float fVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  float fVar19;
  int *local_f4;
  float local_e0 [3];
  undefined4 local_d4;
  float local_d0 [3];
  float local_c4;
  float local_c0;
  float *local_bc;
  float *local_b8;
  float *local_b4;
  float local_b0;
  float local_ac;
  float local_a8;
  float local_a4;
  float local_a0;
  float local_9c;
  float local_98;
  float local_94;
  float local_90;
  float local_8c;
  float local_88;
  float local_84;
  int *local_80;
  undefined4 local_7c;
  undefined4 local_78;
  undefined4 local_74;
  int *local_70;
  undefined4 local_6c;
  undefined4 local_68;
  undefined4 local_64;
  int *local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54;
  
  local_d0[2] = param_3[3] - *param_3;
  local_c4 = param_3[4] - param_3[1];
  local_c0 = param_3[5] - param_3[2];
  _ZN6glitch4core8vector3dIfE9normalizeEv(local_d0 + 2);
  fVar2 = DAT_0018a020;
  fVar1 = DAT_0018a01c;
  local_b0 = 0.0;
  local_ac = 0.0;
  local_a8 = 0.0;
  local_bc = (float *)0x0;
  local_b8 = (float *)0x0;
  local_b4 = (float *)0x0;
  if (param_2 == 3) {
    iVar10 = **(int **)(DAT_0018a024 + 0x189fc4);
    piVar6 = *(int **)(iVar10 + 0x84);
    piVar9 = *(int **)(iVar10 + 0x80);
LAB_00189fd4:
    while (local_f4 = piVar9, local_f4 != piVar6) {
      piVar9 = local_f4 + 1;
      if (0 < *(int *)(*local_f4 + 0x154)) {
        piVar6 = *(int **)(*local_f4 + 0x134);
        iVar8 = *piVar6;
        iVar3 = *(int *)(iVar8 + 0x10);
        if (0 < iVar3) {
          iVar11 = 0;
          iVar13 = param_5 + 4;
LAB_0018a034:
          do {
            piVar6 = *(int **)(*(int *)(iVar8 + 0xc) + iVar11 * 4);
            iVar4 = (**(code **)(*piVar6 + 0x54))(piVar6);
            if ((((((iVar4 != 0) && (iVar4 = (**(code **)(*piVar6 + 0x84))(piVar6), iVar4 != 0)) &&
                  (iVar4 = _ZNK11CGameObject6IsDeadEv(piVar6), iVar4 == 0)) &&
                 ((piVar6[0x32] != 0 && (*(char *)(piVar6[0x32] + 0x14) != '\x02')))) &&
                (iVar4 = _ZNK11CGameObject11IsInFrustumEv(piVar6), iVar4 != 0)) &&
               (((piVar6[0x39] == 0x4c752 || (piVar6[0x39] == 0x2c)) ||
                ((iVar4 = _ZN11CGameObject9IsVehicleEv(piVar6), iVar4 != 0 &&
                 ((iVar4 = piVar6[0x39], iVar4 == 0x4c731 || iVar4 == 0xc0e54 || (iVar4 == 0xc0e55))
                 )))))) {
              local_b8 = local_bc;
              pfVar7 = (float *)(**(code **)(*piVar6 + 0x18))(piVar6);
              if (local_b8 == local_b4) {
                _ZNSt6vectorIN6glitch4core8vector3dIfEESaIS3_EE9push_backERKS3__part_2131
                          (&local_bc,pfVar7);
              }
              else {
                if (local_b8 != (float *)0x0) {
                  *local_b8 = *pfVar7;
                  local_b8[1] = pfVar7[1];
                  local_b8[2] = pfVar7[2];
                }
                local_b8 = local_b8 + 3;
              }
              pfVar7 = (float *)(**(code **)(*piVar6 + 0x18))(piVar6);
              fVar15 = *pfVar7;
              fVar19 = pfVar7[1];
              fVar18 = pfVar7[2];
              fVar5 = (float)_ZNK11CGameObject9GetHeightEv(piVar6);
              iVar4 = ((int)local_b8 - (int)local_bc >> 2) * -0x55555555;
              if (0 < iVar4) {
                iVar12 = 0;
                iVar14 = 0;
LAB_0018a1d8:
                pfVar7 = (float *)((int)local_bc + iVar12);
                local_b0 = *pfVar7 - *param_3;
                iVar14 = iVar14 + 1;
                iVar12 = iVar12 + 0xc;
                local_ac = pfVar7[1] - param_3[1];
                local_a8 = pfVar7[2] - param_3[2];
                fVar17 = local_b0 * local_b0 + local_ac * local_ac + local_a8 * local_a8;
                fVar16 = (float)_ZN6glitch4core8vector3dIfE9normalizeEv(&local_b0);
                acosf(fVar16);
                if ((extraout_r0_00 * fVar1 <= -param_4) || (param_4 <= extraout_r0_00 * fVar1))
                goto LAB_0018a274;
                iVar14 = *(int *)(param_5 + 8);
                iVar4 = iVar13;
                iVar12 = iVar14;
                while( true ) {
                  while (iVar12 != 0) {
                    if (fVar17 <= *(float *)(iVar12 + 0x10)) {
                      iVar4 = iVar12;
                      iVar12 = *(int *)(iVar12 + 8);
                    }
                    else {
                      iVar12 = *(int *)(iVar12 + 0xc);
                    }
                  }
                  iVar12 = iVar13;
                  if ((iVar13 != iVar4) && (iVar12 = iVar4, fVar17 < *(float *)(iVar4 + 0x10))) {
                    iVar12 = iVar13;
                  }
                  iVar4 = iVar13;
                  if (iVar13 == iVar12) break;
                  fVar17 = fVar17 + fVar2;
                  iVar12 = iVar14;
                }
                while (iVar14 != 0) {
                  if (fVar17 <= *(float *)(iVar14 + 0x10)) {
                    iVar4 = iVar14;
                    iVar14 = *(int *)(iVar14 + 8);
                  }
                  else {
                    iVar14 = *(int *)(iVar14 + 0xc);
                  }
                }
                if ((iVar13 == iVar4) || (fVar17 < *(float *)(iVar4 + 0x10))) {
                  local_e0[1] = 0.0;
                  local_e0[0] = fVar17;
                  iVar4 = _ZNSt8_Rb_treeIfSt4pairIKfP11CGameObjectESt10_Select1stIS4_ESt4lessIfESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4__constprop_3307
                                    (param_5,iVar4,local_e0);
                }
                *(int **)(iVar4 + 0x14) = piVar6;
                iVar4 = param_6 + 4;
                iVar12 = *(int *)(param_6 + 8);
                while (iVar12 != 0) {
                  if (*(int **)(iVar12 + 0x10) < piVar6) {
                    iVar12 = *(int *)(iVar12 + 0xc);
                  }
                  else {
                    iVar4 = iVar12;
                    iVar12 = *(int *)(iVar12 + 8);
                  }
                }
                if ((param_6 + 4 == iVar4) || (piVar6 < *(int **)(iVar4 + 0x10))) {
                  local_7c = 0;
                  local_78 = 0;
                  local_74 = 0;
                  local_80 = piVar6;
                  iVar4 = _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_N6glitch4core8vector3dIfEEESt10_Select1stIS8_ESt4lessIS1_ESaIS8_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS8_ERKS8__constprop_3311
                                    (param_6,iVar4,&local_80);
                }
                *(float *)(iVar4 + 0x1c) = (fVar18 - local_a8) + fVar5;
                *(float *)(iVar4 + 0x18) = fVar19 - local_ac;
                *(float *)(iVar4 + 0x14) = fVar15 - local_b0;
              }
            }
            iVar11 = iVar11 + 1;
          } while (iVar11 != iVar3);
          goto LAB_0018a290;
        }
        goto LAB_0018a29c;
      }
    }
    goto LAB_00189f94;
  }
  iVar10 = *(int *)(param_1 + 0xb8);
  iVar8 = param_5 + 4;
  do {
    if (param_1 + 0xb0 == iVar10) {
LAB_00189f94:
      if (local_bc != (float *)0x0) {
        _ZdlPv();
      }
      return;
    }
    piVar9 = *(int **)(iVar10 + 0x10);
    if ((((piVar9 != (int *)0x0) && (iVar3 = (**(code **)(*piVar9 + 0x54))(piVar9), iVar3 != 0)) &&
        (iVar3 = _ZNK11CGameObject6IsDeadEv(piVar9), iVar3 == 0)) &&
       (((iVar3 = _ZNK11CGameObject12IsTargetableEv(piVar9), iVar3 != 0 &&
         (iVar3 = _ZNK11CGameObject11IsInFrustumEv(piVar9), iVar3 != 0)) &&
        ((*(char *)(piVar9[0x32] + 0x14) != '\x02' &&
         ((param_2 != 2 || (iVar3 = _ZN15CNpcAIComponent7IsMeleeEv(piVar9[0x2f]), iVar3 == 0))))))))
    {
      iVar3 = piVar9[0x2e];
      local_b8 = local_bc;
      if (*(char *)(*(int *)(iVar3 + 0x60) + 6) == '\0') {
        pfVar7 = (float *)(**(code **)(*piVar9 + 0x18))(piVar9);
        if (local_b8 == local_b4) {
          _ZNSt6vectorIN6glitch4core8vector3dIfEESaIS3_EE9push_backERKS3__part_2131
                    (&local_bc,pfVar7);
        }
        else {
          if (local_b8 != (float *)0x0) {
            *local_b8 = *pfVar7;
            local_b8[1] = pfVar7[1];
            local_b8[2] = pfVar7[2];
          }
          local_b8 = local_b8 + 3;
        }
        fVar5 = local_bc[1];
        fVar18 = local_bc[2];
        fVar19 = *local_bc;
      }
      else {
        _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv
                  (&local_a4,*(undefined4 *)(iVar3 + 0x150));
        _ZNK6glitch5scene10ISceneNode19getAbsolutePositionEv
                  (&local_98,*(undefined4 *)(iVar3 + 0x148));
        if (local_b8 == local_b4) {
          _ZNSt6vectorIN6glitch4core8vector3dIfEESaIS3_EE9push_backERKS3__part_2131
                    (&local_bc,&local_a4);
          if (local_b8 == local_b4) goto LAB_0018a980;
LAB_00189da4:
          if (local_b8 != (float *)0x0) {
            *local_b8 = local_98;
            local_b8[1] = local_94;
            local_b8[2] = local_90;
          }
          local_b8 = local_b8 + 3;
        }
        else {
          if (local_b8 != (float *)0x0) {
            *local_b8 = local_a4;
            local_b8[1] = local_a0;
            local_b8[2] = local_9c;
          }
          local_b8 = local_b8 + 3;
          if (local_b8 != local_b4) goto LAB_00189da4;
LAB_0018a980:
          _ZNSt6vectorIN6glitch4core8vector3dIfEESaIS3_EE9push_backERKS3__part_2131
                    (&local_bc,&local_98);
        }
        local_8c = (local_a4 + local_98) * 0.5;
        local_88 = (local_a0 + local_94) * 0.5;
        local_84 = (local_9c + local_90) * 0.5;
        if (local_b8 == local_b4) {
          _ZNSt6vectorIN6glitch4core8vector3dIfEESaIS3_EE9push_backERKS3__part_2131
                    (&local_bc,&local_8c);
          fVar5 = local_a0;
          fVar18 = local_9c;
          fVar19 = local_a4;
        }
        else {
          if (local_b8 != (float *)0x0) {
            *local_b8 = local_8c;
            local_b8[1] = local_88;
            local_b8[2] = local_84;
          }
          local_b8 = local_b8 + 3;
          fVar5 = local_a0;
          fVar18 = local_9c;
          fVar19 = local_a4;
        }
      }
      iVar3 = ((int)local_b8 - (int)local_bc >> 2) * -0x55555555;
      if (0 < iVar3) {
        iVar11 = 0;
        iVar13 = 0;
LAB_00189e98:
        pfVar7 = (float *)((int)local_bc + iVar11);
        local_b0 = *pfVar7 - *param_3;
        iVar13 = iVar13 + 1;
        iVar11 = iVar11 + 0xc;
        local_ac = pfVar7[1] - param_3[1];
        local_a8 = pfVar7[2] - param_3[2];
        fVar16 = local_b0 * local_b0 + local_ac * local_ac + local_a8 * local_a8;
        fVar15 = (float)_ZN6glitch4core8vector3dIfE9normalizeEv(&local_b0);
        acosf(fVar15);
        if ((extraout_r0 * fVar1 <= -param_4) || (param_4 <= extraout_r0 * fVar1))
        goto LAB_00189e84;
        iVar13 = *(int *)(param_5 + 8);
        iVar3 = iVar8;
        iVar11 = iVar13;
        while( true ) {
          while (iVar11 != 0) {
            if (fVar16 <= *(float *)(iVar11 + 0x10)) {
              iVar3 = iVar11;
              iVar11 = *(int *)(iVar11 + 8);
            }
            else {
              iVar11 = *(int *)(iVar11 + 0xc);
            }
          }
          iVar11 = iVar8;
          if ((iVar8 != iVar3) && (iVar11 = iVar3, fVar16 < *(float *)(iVar3 + 0x10))) {
            iVar11 = iVar8;
          }
          iVar3 = iVar8;
          if (iVar8 == iVar11) break;
          fVar16 = fVar16 + fVar2;
          iVar11 = iVar13;
        }
        while (iVar13 != 0) {
          if (fVar16 <= *(float *)(iVar13 + 0x10)) {
            iVar13 = *(int *)(iVar13 + 8);
            iVar3 = iVar13;
          }
          else {
            iVar13 = *(int *)(iVar13 + 0xc);
          }
        }
        if ((iVar8 == iVar3) || (fVar16 < *(float *)(iVar3 + 0x10))) {
          local_d0[1] = 0.0;
          local_d0[0] = fVar16;
          iVar3 = _ZNSt8_Rb_treeIfSt4pairIKfP11CGameObjectESt10_Select1stIS4_ESt4lessIfESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4__constprop_3307
                            (param_5,iVar3,local_d0);
        }
        *(int **)(iVar3 + 0x14) = piVar9;
        iVar3 = param_6 + 4;
        iVar11 = *(int *)(param_6 + 8);
        while (iVar11 != 0) {
          if (*(int **)(iVar11 + 0x10) < piVar9) {
            iVar11 = *(int *)(iVar11 + 0xc);
          }
          else {
            iVar3 = iVar11;
            iVar11 = *(int *)(iVar11 + 8);
          }
        }
        if ((param_6 + 4 == iVar3) || (piVar9 < *(int **)(iVar3 + 0x10))) {
          local_5c = 0;
          local_58 = 0;
          local_54 = 0;
          local_60 = piVar9;
          iVar3 = _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_N6glitch4core8vector3dIfEEESt10_Select1stIS8_ESt4lessIS1_ESaIS8_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS8_ERKS8__constprop_3311
                            (param_6,iVar3,&local_60);
        }
        *(float *)(iVar3 + 0x18) = fVar5 - local_ac;
        *(float *)(iVar3 + 0x1c) = fVar18 - local_a8;
        *(float *)(iVar3 + 0x14) = fVar19 - local_b0;
      }
    }
LAB_00189cac:
    iVar10 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar10);
  } while( true );
LAB_0018a274:
  if (iVar14 == iVar4) goto code_r0x0018a27c;
  goto LAB_0018a1d8;
code_r0x0018a27c:
  iVar11 = iVar11 + 1;
  if (iVar11 == iVar3) goto LAB_0018a290;
  goto LAB_0018a034;
LAB_0018a290:
  piVar6 = *(int **)(*local_f4 + 0x134);
LAB_0018a29c:
  iVar8 = piVar6[2];
  iVar3 = *(int *)(iVar8 + 0x10);
  if (0 < iVar3) {
    iVar11 = 0;
    iVar13 = param_5 + 4;
LAB_0018a2c8:
    do {
      piVar6 = *(int **)(*(int *)(iVar8 + 0xc) + iVar11 * 4);
      iVar4 = (**(code **)(*piVar6 + 0x54))(piVar6);
      if (((((iVar4 != 0) && (iVar4 = (**(code **)(*piVar6 + 0x84))(piVar6), iVar4 != 0)) &&
           (iVar4 = _ZNK11CGameObject6IsDeadEv(piVar6), iVar4 == 0)) &&
          (((piVar6[0x32] != 0 && (*(char *)(piVar6[0x32] + 0x14) != '\x02')) &&
           (iVar4 = _ZNK11CGameObject11IsInFrustumEv(piVar6), iVar4 != 0)))) &&
         (((piVar6[0x39] == 0x4c752 || (piVar6[0x39] == 0x2c)) ||
          ((iVar4 = _ZN11CGameObject9IsVehicleEv(piVar6), iVar4 != 0 &&
           ((iVar4 = piVar6[0x39], iVar4 == 0x4c731 || iVar4 == 0xc0e54 || (iVar4 == 0xc0e55))))))))
      {
        local_b8 = local_bc;
        pfVar7 = (float *)(**(code **)(*piVar6 + 0x18))(piVar6);
        if (local_b8 == local_b4) {
          _ZNSt6vectorIN6glitch4core8vector3dIfEESaIS3_EE9push_backERKS3__part_2131
                    (&local_bc,pfVar7);
        }
        else {
          if (local_b8 != (float *)0x0) {
            *local_b8 = *pfVar7;
            local_b8[1] = pfVar7[1];
            local_b8[2] = pfVar7[2];
          }
          local_b8 = local_b8 + 3;
        }
        pfVar7 = (float *)(**(code **)(*piVar6 + 0x18))(piVar6);
        fVar15 = *pfVar7;
        fVar19 = pfVar7[1];
        fVar18 = pfVar7[2];
        fVar5 = (float)_ZNK11CGameObject9GetHeightEv(piVar6);
        iVar4 = ((int)local_b8 - (int)local_bc >> 2) * -0x55555555;
        if (0 < iVar4) {
          iVar12 = 0;
          iVar14 = 0;
LAB_0018a46c:
          pfVar7 = (float *)((int)local_bc + iVar12);
          local_b0 = *pfVar7 - *param_3;
          iVar14 = iVar14 + 1;
          iVar12 = iVar12 + 0xc;
          local_ac = pfVar7[1] - param_3[1];
          local_a8 = pfVar7[2] - param_3[2];
          fVar17 = local_b0 * local_b0 + local_ac * local_ac + local_a8 * local_a8;
          fVar16 = (float)_ZN6glitch4core8vector3dIfE9normalizeEv(&local_b0);
          acosf(fVar16);
          if ((extraout_r0_01 * fVar1 <= -param_4) || (param_4 <= extraout_r0_01 * fVar1))
          goto LAB_0018a508;
          iVar14 = *(int *)(param_5 + 8);
          iVar4 = iVar13;
          iVar12 = iVar14;
          while( true ) {
            while (iVar12 != 0) {
              if (fVar17 <= *(float *)(iVar12 + 0x10)) {
                iVar4 = iVar12;
                iVar12 = *(int *)(iVar12 + 8);
              }
              else {
                iVar12 = *(int *)(iVar12 + 0xc);
              }
            }
            iVar12 = iVar13;
            if ((iVar13 != iVar4) && (iVar12 = iVar4, fVar17 < *(float *)(iVar4 + 0x10))) {
              iVar12 = iVar13;
            }
            iVar4 = iVar13;
            if (iVar13 == iVar12) break;
            fVar17 = fVar17 + fVar2;
            iVar12 = iVar14;
          }
          while (iVar14 != 0) {
            if (fVar17 <= *(float *)(iVar14 + 0x10)) {
              iVar4 = iVar14;
              iVar14 = *(int *)(iVar14 + 8);
            }
            else {
              iVar14 = *(int *)(iVar14 + 0xc);
            }
          }
          if ((iVar13 == iVar4) || (fVar17 < *(float *)(iVar4 + 0x10))) {
            local_d4 = 0;
            local_e0[2] = fVar17;
            iVar4 = _ZNSt8_Rb_treeIfSt4pairIKfP11CGameObjectESt10_Select1stIS4_ESt4lessIfESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4__constprop_3307
                              (param_5,iVar4,local_e0 + 2);
          }
          *(int **)(iVar4 + 0x14) = piVar6;
          iVar4 = param_6 + 4;
          iVar12 = *(int *)(param_6 + 8);
          while (iVar12 != 0) {
            if (*(int **)(iVar12 + 0x10) < piVar6) {
              iVar12 = *(int *)(iVar12 + 0xc);
            }
            else {
              iVar4 = iVar12;
              iVar12 = *(int *)(iVar12 + 8);
            }
          }
          if ((param_6 + 4 == iVar4) || (piVar6 < *(int **)(iVar4 + 0x10))) {
            local_6c = 0;
            local_68 = 0;
            local_64 = 0;
            local_70 = piVar6;
            iVar4 = _ZNSt8_Rb_treeIP11CGameObjectSt4pairIKS1_N6glitch4core8vector3dIfEEESt10_Select1stIS8_ESt4lessIS1_ESaIS8_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS8_ERKS8__constprop_3311
                              (param_6,iVar4,&local_70);
          }
          *(float *)(iVar4 + 0x1c) = (fVar18 - local_a8) + fVar5;
          *(float *)(iVar4 + 0x18) = fVar19 - local_ac;
          *(float *)(iVar4 + 0x14) = fVar15 - local_b0;
        }
      }
      iVar11 = iVar11 + 1;
    } while (iVar11 != iVar3);
  }
LAB_0018a524:
  piVar6 = *(int **)(iVar10 + 0x84);
  goto LAB_00189fd4;
LAB_0018a508:
  if (iVar14 == iVar4) goto code_r0x0018a510;
  goto LAB_0018a46c;
code_r0x0018a510:
  iVar11 = iVar11 + 1;
  if (iVar11 == iVar3) goto LAB_0018a524;
  goto LAB_0018a2c8;
LAB_00189e84:
  if (iVar13 == iVar3) goto LAB_00189cac;
  goto LAB_00189e98;
}

