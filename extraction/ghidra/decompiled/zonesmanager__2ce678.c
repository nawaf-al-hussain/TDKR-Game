// _ZN13CZonesManager20SpawnObjectNearActorEP11CGameObjectRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS4_6memory13E_MEMORY_HINTE0EEEESC_fffb @ 002ce678

int * _ZN13CZonesManager20SpawnObjectNearActorEP11CGameObjectRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS4_6memory13E_MEMORY_HINTE0EEEESC_fffb
                (undefined4 param_1,int *param_2,undefined4 param_3,undefined4 param_4,float param_5
                ,float param_6,float param_7,undefined1 param_8)

{
  float fVar1;
  float fVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  float fVar6;
  int *piVar7;
  float fVar8;
  float fVar9;
  float *pfVar10;
  undefined4 extraout_r0;
  undefined4 extraout_r0_00;
  int iVar11;
  undefined4 uVar12;
  undefined4 uVar13;
  uint uVar14;
  undefined4 uVar15;
  undefined4 extraout_r1;
  undefined4 extraout_r1_00;
  int iVar16;
  int *unaff_r6;
  undefined4 extraout_s0;
  undefined4 extraout_s1;
  double __x;
  int iVar17;
  float fVar18;
  float fVar19;
  undefined8 uVar20;
  longlong lVar21;
  undefined1 local_151;
  float local_150;
  float local_14c;
  float local_148;
  undefined4 local_144;
  undefined4 local_140;
  float local_13c;
  float local_138;
  float local_134;
  float local_130;
  undefined4 local_12c;
  undefined4 local_128;
  undefined4 local_124;
  undefined4 local_120;
  undefined4 local_11c;
  undefined4 local_118;
  undefined4 local_114;
  undefined2 local_110;
  undefined4 local_10c;
  undefined1 local_108;
  int local_104;
  undefined4 local_100;
  undefined4 local_fc;
  undefined4 local_f8;
  undefined4 local_f4;
  float local_f0;
  undefined4 local_ec;
  undefined4 local_e8;
  undefined4 local_e4;
  undefined4 local_e0;
  undefined4 local_dc;
  undefined4 local_d8;
  undefined1 local_d4;
  undefined1 local_d0 [4];
  int *local_cc;
  undefined4 local_c8;
  undefined4 local_c4;
  undefined4 local_c0;
  undefined4 local_bc;
  undefined4 local_b8;
  float local_b4;
  undefined1 local_b0;
  undefined1 local_af;
  undefined1 local_ae;
  undefined4 local_ac;
  undefined4 local_a8;
  undefined4 local_a4;
  undefined4 local_a0;
  undefined4 local_9c;
  undefined4 local_98;
  undefined4 local_94;
  undefined4 local_90;
  undefined4 local_8c;
  int local_88;
  undefined1 local_84;
  undefined4 *local_80;
  undefined4 *local_7c;
  undefined4 *local_78;
  int *local_74;
  undefined2 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  
  if (*(char *)(param_2[0x2e] + 0x19c) == '\0') {
    _ZN6CLevel8GetLevelEv();
    uVar5 = _ZN6CLevel10GetNavMeshEv();
    local_148 = 0.0;
    local_144 = 0;
    local_140 = 0;
    local_13c = 0.0;
    if (param_6 == 0.0) {
      if (param_7 == 0.0) {
        local_150 = (float)param_2[0x13];
        iVar17 = 0x10;
        local_14c = (float)param_2[0x14];
        fVar19 = DAT_002ceaf8;
        fVar18 = DAT_002ceafc;
      }
      else {
        fVar19 = param_7 * 0.5 * DAT_002ceaf4;
        iVar17 = (int)(param_7 / fVar19);
        local_150 = -(float)param_2[0x13];
        local_14c = -(float)param_2[0x14];
        fVar18 = param_7 * 0.5;
      }
    }
    else {
      local_150 = (float)param_2[0x13];
      local_14c = (float)param_2[0x14];
      fVar19 = param_6 * 0.5 * DAT_002ceaf4;
      iVar17 = (int)(param_6 / fVar19);
      fVar18 = param_6 * 0.5;
    }
    iVar16 = 0;
    _ZN6glitch4core8vector3dIfE9normalizeEv(&local_150);
    local_150 = local_150 * param_5;
    local_14c = local_14c * param_5;
    local_148 = local_148 * param_5;
    fVar6 = (float)_Z9getRandomv();
    fVar1 = DAT_002ceae8;
    local_10c = 0xffff;
    local_110 = 0xffff;
    local_e0 = 0xbf800000;
    uVar15 = 1;
    local_f8 = 0;
    local_f4 = 0;
    local_f0 = 0.0;
    local_e8 = 0;
    local_e4 = 0;
    local_bc = 0;
    local_b8 = 0;
    local_b4 = 0.0;
    local_ac = 0;
    local_a8 = 0;
    local_a4 = 0;
    local_a0 = 0;
    local_9c = 0;
    local_98 = 0;
    local_94 = 0;
    local_104 = 0;
    local_100 = 0;
    local_fc = 0;
    local_11c = 0;
    local_118 = 0;
    local_108 = 1;
    local_ec = 0x447a0000;
    local_d8 = 0;
    local_d4 = SUB41(&local_11c,0);
    local_cc = (int *)0x0;
    local_c8 = 0;
    local_c4 = 0;
    local_b0 = 0;
    local_88 = DAT_002ceaec + 0x2ce804;
    local_af = 0;
    local_ae = 0;
    local_90 = 0;
    local_70 = 0x13f;
    local_80 = &local_ac;
    local_7c = &local_a0;
    local_78 = &local_94;
    local_74 = (int *)&local_b0;
    piVar7 = local_74;
    if (iVar17 < 1) {
      piVar7 = (int *)0x0;
    }
    local_8c = 0;
    if (iVar17 < 1) {
      unaff_r6 = piVar7;
    }
    local_12c = 0;
    local_128 = 0;
    local_124 = 0;
    local_84 = 0;
    local_6c = 0;
    local_68 = 0;
    local_d0[0] = 0;
    local_c0 = 0;
    local_114 = 1;
    local_dc = 0x447a0000;
    local_151 = 0;
    local_120 = 0x3f800000;
    if (0 < iVar17) {
      unaff_r6 = (int *)0x0;
      fVar6 = fVar18 * fVar6 + fVar18 * fVar6;
      do {
        if (fVar18 < fVar6) {
          fVar6 = fVar6 - (fVar18 + fVar18);
        }
        if (unaff_r6 != (int *)0x0) {
          fVar8 = (float)_ZNK6glitch4core8vector3dIfE9getLengthEv(&local_150,uVar15);
          fVar9 = (float)_ZNK11CGameObject9GetRadiusEv(unaff_r6);
          fVar8 = fVar8 + fVar9 * 0.5;
          _ZN6glitch4core8vector3dIfE9normalizeEv(&local_150);
          local_150 = local_150 * fVar8;
          local_14c = local_14c * fVar8;
          local_148 = local_148 * fVar8;
        }
        pfVar10 = (float *)(**(code **)(*param_2 + 0x18))(param_2);
        fVar2 = local_148;
        fVar9 = local_14c;
        fVar8 = local_150;
        __x = cos((double)CONCAT44(extraout_s1,extraout_s0));
        sin(__x);
        local_138 = (*pfVar10 + (float)(double)CONCAT44(extraout_r1,extraout_r0) * fVar8) -
                    (float)(double)CONCAT44(extraout_r1_00,extraout_r0_00) * fVar9;
        local_134 = (float)(double)CONCAT44(extraout_r1,extraout_r0) * fVar9 +
                    (float)(double)CONCAT44(extraout_r1_00,extraout_r0_00) * fVar8 + pfVar10[1];
        local_130 = pfVar10[2] + fVar2;
        uVar20 = _ZN12CNavMeshNova15FindClosestCellEN6glitch4core8vector3dIfEERS3_Rbf
                           (uVar5,&local_138,&local_144,&local_151,0x3f800000);
        lVar21 = CONCAT44((int)((ulonglong)uVar20 >> 0x20),unaff_r6);
        if (unaff_r6 == (int *)0x0) {
          uVar15 = (**(code **)(*param_2 + 0xa0))(param_2);
          iVar11 = _ZN6CLevel8GetLevelEv();
          uVar14 = _ZN18CGameObjectManager21GetTemplateIdFromNameERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                             (*(undefined4 *)(iVar11 + 0xa94),param_3);
          lVar21 = (ulonglong)uVar14 << 0x20;
          if (uVar14 != 0xffffffff) {
            lVar21 = _ZN13CZonesManager11SpawnObjectEiRKN6glitch4core8vector3dIfEERKSbIcSt11char_traitsIcENS1_10SAllocatorIcLNS0_6memory13E_MEMORY_HINTE0EEEEP5CZoneb
                               (param_1,uVar14,&local_144,param_4,uVar15,param_8);
            if ((int)lVar21 != 0) {
              *(undefined1 *)((int)lVar21 + 0x100) = 1;
            }
          }
        }
        uVar15 = (undefined4)((ulonglong)lVar21 >> 0x20);
        unaff_r6 = (int *)lVar21;
        if ((int)uVar20 != -1) {
          local_ec = 0x447a0000;
          local_f8 = local_144;
          local_f4 = local_140;
          local_f0 = local_13c + 2.0;
          iVar11 = _ZN6CLevel8GetLevelEv();
          uVar20 = _ZN12CollisionMgr20GetIntersectionPointEP16CollisionRequestP17CollisionResponseb
                             (*(undefined4 *)(iVar11 + 0x128),&local_11c,local_d0,0);
          fVar8 = local_b4;
          uVar4 = local_b8;
          uVar3 = local_bc;
          uVar15 = (undefined4)((ulonglong)uVar20 >> 0x20);
          if (((int)uVar20 != 0) && (local_b4 - local_13c < fVar1)) {
            iVar11 = param_2[0x27];
            local_13c = local_b4;
            local_140 = local_b8;
            local_144 = local_bc;
            uVar12 = (**(code **)(*param_2 + 0x18))(param_2);
            _ZN6CLevel8GetLevelEv();
            uVar13 = _ZN6CLevel10GetNavMeshEv();
            _ZN6CLevel8GetLevelEv();
            uVar20 = _ZN6CLevel10GetNavMeshEv();
            uVar15 = (undefined4)((ulonglong)uVar20 >> 0x20);
            if ((int)uVar20 != 0) {
              uVar20 = _ZN13CNavMeshQuery7HasPathEP12CNavMeshNovaRKN6glitch4core8vector3dIfEES1_S7_f
                                 (*(undefined4 *)(iVar11 + 0x144),uVar13,uVar12,uVar13,&local_144,
                                  param_5);
              uVar15 = (undefined4)((ulonglong)uVar20 >> 0x20);
              if ((int)uVar20 != 0) {
                if (unaff_r6 != (int *)0x0) {
                  (**(code **)(*unaff_r6 + 0x28))(unaff_r6,&local_144,1);
                  iVar11 = unaff_r6[0x2e];
                  *(undefined4 *)(iVar11 + 0x34) = *(undefined4 *)(iVar11 + 0x30);
                  uVar20 = _ZN19CActorBaseComponent18CheckForCollisionsEPN6glitch4core8vector3dIfEEPNS1_10quaternionEibbbb
                                     (iVar11,&local_144,&local_12c,0x11,1,0,0,0);
                  uVar15 = (undefined4)((ulonglong)uVar20 >> 0x20);
                  if ((int)uVar20 != 0) goto LAB_002ceb00;
                }
                local_144 = uVar3;
                local_13c = fVar8;
                local_140 = uVar4;
                (**(code **)(*unaff_r6 + 0x80))(unaff_r6,1);
                _ZN11CGameObject6FadeInEb(unaff_r6,1);
                fVar19 = (float)_ZN11CGameObject10GetOpacityEv(unaff_r6);
                piVar7 = local_cc;
                if (fVar19 == 0.0) {
                  _ZN11CGameObject19ForceNodeVisibilityEb(unaff_r6,0);
                  piVar7 = local_cc;
                }
                goto LAB_002ceb48;
              }
            }
          }
        }
LAB_002ceb00:
        iVar16 = iVar16 + 1;
        fVar6 = fVar6 + fVar19;
      } while (iVar16 != iVar17);
      piVar7 = local_cc;
      if (unaff_r6 != (int *)0x0) {
        (**(code **)(*unaff_r6 + 0x50))(unaff_r6,0);
        (**(code **)(*unaff_r6 + 0x80))(unaff_r6);
        piVar7 = local_cc;
        unaff_r6 = (int *)0x0;
      }
    }
LAB_002ceb48:
    local_88 = DAT_002ceaf0 + 0x2ceb60;
    if (piVar7 != (int *)0x0) {
      _ZdlPv();
    }
    if (local_104 != 0) {
      _ZdlPv();
    }
  }
  else {
    unaff_r6 = (int *)0x0;
  }
  return unaff_r6;
}


