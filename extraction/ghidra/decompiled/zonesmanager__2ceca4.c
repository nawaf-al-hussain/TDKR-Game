// _ZN13CZonesManager22SpawnObjectNearActorExEP11CGameObjectfRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS4_6memory13E_MEMORY_HINTE0EEEESC_iff @ 002ceca4

int * _ZN13CZonesManager22SpawnObjectNearActorExEP11CGameObjectfRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS4_6memory13E_MEMORY_HINTE0EEEESC_iff
                (undefined4 param_1,int *param_2,float param_3,undefined4 param_4,undefined4 param_5
                ,uint param_6,float param_7,float param_8)

{
  float fVar1;
  float fVar2;
  float fVar3;
  int iVar4;
  undefined4 uVar5;
  float fVar6;
  int *piVar7;
  float *pfVar8;
  undefined4 extraout_r0;
  undefined4 extraout_r0_00;
  int iVar9;
  float fVar10;
  undefined4 extraout_r1;
  undefined4 extraout_r1_00;
  int iVar11;
  undefined4 extraout_s0;
  undefined4 extraout_s1;
  double __x;
  float fVar12;
  undefined1 local_139;
  float local_138;
  float local_134;
  float local_130;
  undefined4 local_12c;
  undefined4 local_128;
  float local_124;
  float local_120;
  float local_11c;
  float local_118;
  undefined4 local_114;
  undefined4 local_110;
  undefined4 local_10c;
  undefined2 local_108;
  undefined4 local_104;
  undefined1 local_100;
  int local_fc;
  undefined4 local_f8;
  undefined4 local_f4;
  undefined4 local_f0;
  undefined4 local_ec;
  float local_e8;
  undefined4 local_e4;
  undefined4 local_e0;
  undefined4 local_dc;
  undefined4 local_d8;
  undefined4 local_d4;
  undefined4 local_d0;
  undefined1 local_cc;
  undefined1 local_c8 [4];
  int *local_c4;
  undefined4 local_c0;
  undefined4 local_bc;
  undefined4 local_b8;
  undefined4 local_b4;
  undefined4 local_b0;
  float local_ac;
  undefined1 local_a8;
  undefined1 local_a7;
  undefined1 local_a6;
  undefined4 local_a4;
  undefined4 local_a0;
  undefined4 local_9c;
  undefined4 local_98;
  undefined4 local_94;
  undefined4 local_90;
  undefined4 local_8c;
  undefined4 local_88;
  undefined4 local_84;
  int local_80;
  undefined1 local_7c;
  undefined4 *local_78;
  undefined4 *local_74;
  undefined4 *local_70;
  undefined1 *local_6c;
  undefined2 local_68;
  undefined4 local_64;
  undefined4 local_60;
  
  if ((param_6 & 1) != 0) {
    if (*(char *)(param_2[0x2e] + 0x19c) != '\0') {
      return (int *)0x0;
    }
    iVar4 = _ZN19CActorBaseComponent9IsOnRoofsEv();
    if (iVar4 != 0) {
      return (int *)0x0;
    }
  }
  _ZN6CLevel8GetLevelEv();
  uVar5 = _ZN6CLevel10GetNavMeshEv();
  local_130 = 0.0;
  local_12c = 0;
  local_128 = 0;
  local_124 = 0.0;
  if (param_7 == 0.0) {
    if (param_8 == 0.0) {
      local_138 = (float)param_2[0x13];
      iVar4 = 6;
      local_134 = (float)param_2[0x14];
      param_8 = DAT_002cf12c;
      fVar10 = DAT_002cf128;
      fVar12 = DAT_002cf124;
    }
    else {
      param_8 = param_8 * 0.5;
      iVar4 = (int)((param_8 + param_8) / (param_8 * DAT_002cf120));
      local_138 = -(float)param_2[0x13];
      local_134 = -(float)param_2[0x14];
      fVar10 = param_8 * DAT_002cf120;
      fVar12 = param_8 + param_8;
    }
  }
  else {
    local_138 = (float)param_2[0x13];
    local_134 = (float)param_2[0x14];
    param_8 = param_7 * 0.5;
    fVar10 = param_8 * DAT_002cf120;
    fVar12 = param_8 + param_8;
    iVar4 = (int)(fVar12 / fVar10);
  }
  iVar11 = 0;
  _ZN6glitch4core8vector3dIfE9normalizeEv(&local_138);
  local_138 = local_138 * param_3;
  local_134 = local_134 * param_3;
  local_130 = local_130 * param_3;
  fVar6 = (float)_Z9getRandomv();
  local_f0 = 0;
  local_ec = 0;
  local_80 = DAT_002cf130 + 0x2cedd8;
  local_e8 = 0.0;
  local_e0 = 0;
  local_dc = 0;
  local_b4 = 0;
  local_b0 = 0;
  local_ac = 0.0;
  local_a4 = 0;
  local_a0 = 0;
  local_9c = 0;
  local_98 = 0;
  local_94 = 0;
  local_90 = 0;
  local_8c = 0;
  local_fc = 0;
  local_f8 = 0;
  local_f4 = 0;
  local_114 = 0;
  local_110 = 0;
  local_100 = 1;
  local_e4 = 0x447a0000;
  local_d0 = 0;
  local_cc = SUB41(&local_114,0);
  local_c4 = (int *)0x0;
  local_c0 = 0;
  local_bc = 0;
  local_a8 = 0;
  local_a7 = 0;
  local_104 = 0xffff;
  local_108 = 0xffff;
  piVar7 = (int *)0xbf800000;
  local_d8 = 0xbf800000;
  if (iVar4 < 1) {
    piVar7 = (int *)0x0;
  }
  local_a6 = 0;
  if (iVar4 < 1) {
    param_2 = piVar7;
  }
  local_88 = 0;
  local_84 = 0;
  local_7c = 0;
  local_68 = 0x13f;
  local_78 = &local_a4;
  local_74 = &local_98;
  local_64 = 0;
  local_70 = &local_8c;
  local_60 = 0;
  local_6c = &local_a8;
  local_c8[0] = 0;
  local_b8 = 0;
  local_10c = 1;
  local_d4 = 0x447a0000;
  local_139 = 0;
  if (0 < iVar4) {
    fVar6 = param_8 * fVar6 + param_8 * fVar6;
    do {
      iVar11 = iVar11 + 1;
      if (param_8 < fVar6) {
        fVar6 = fVar6 - fVar12;
      }
      pfVar8 = (float *)(**(code **)(*param_2 + 0x18))(param_2);
      fVar3 = local_130;
      fVar2 = local_134;
      fVar1 = local_138;
      __x = cos((double)CONCAT44(extraout_s1,extraout_s0));
      sin(__x);
      local_120 = (*pfVar8 + (float)(double)CONCAT44(extraout_r1,extraout_r0) * fVar1) -
                  (float)(double)CONCAT44(extraout_r1_00,extraout_r0_00) * fVar2;
      local_11c = (float)(double)CONCAT44(extraout_r1,extraout_r0) * fVar2 +
                  (float)(double)CONCAT44(extraout_r1_00,extraout_r0_00) * fVar1 + pfVar8[1];
      local_118 = pfVar8[2] + fVar3;
      iVar9 = _ZN12CNavMeshNova15FindClosestCellEN6glitch4core8vector3dIfEERS3_Rbf
                        (uVar5,&local_120,&local_12c,&local_139,0x3f800000);
      if (iVar9 != -1) {
        local_e4 = 0x447a0000;
        local_f0 = local_12c;
        local_ec = local_128;
        local_e8 = local_124 + 2.0;
        iVar9 = _ZN6CLevel8GetLevelEv();
        iVar9 = _ZN12CollisionMgr20GetIntersectionPointEP16CollisionRequestP17CollisionResponseb
                          (*(undefined4 *)(iVar9 + 0x128),&local_114,local_c8,0);
        if ((iVar9 != 0) && (local_ac - local_124 < 0.25)) {
          local_124 = local_ac;
          local_12c = local_b4;
          local_128 = local_b0;
          uVar5 = (**(code **)(*param_2 + 0xa0))(param_2);
          iVar4 = _ZN6CLevel8GetLevelEv();
          iVar4 = _ZN18CGameObjectManager21GetTemplateIdFromNameERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                            (*(undefined4 *)(iVar4 + 0xa94),param_4);
          if (iVar4 != -1) {
            param_2 = (int *)_ZN13CZonesManager11SpawnObjectEiRKN6glitch4core8vector3dIfEERKSbIcSt11char_traitsIcENS1_10SAllocatorIcLNS0_6memory13E_MEMORY_HINTE0EEEEP5CZoneb
                                       (param_1,iVar4,&local_12c,param_5,uVar5,1);
            piVar7 = local_c4;
            if (param_2 != (int *)0x0) {
              _ZN11CGameObject6FadeInEb(param_2,1);
              fVar10 = (float)_ZN11CGameObject10GetOpacityEv(param_2);
              piVar7 = local_c4;
              if (fVar10 == 0.0) {
                _ZN11CGameObject19ForceNodeVisibilityEb(param_2,0);
                piVar7 = local_c4;
              }
            }
            goto LAB_002ceffc;
          }
          break;
        }
      }
      fVar6 = fVar6 + fVar10;
    } while (iVar11 != iVar4);
    param_2 = (int *)0x0;
    piVar7 = local_c4;
  }
LAB_002ceffc:
  local_80 = DAT_002cf134 + 0x2cf014;
  if (piVar7 != (int *)0x0) {
    _ZdlPv();
  }
  if (local_fc != 0) {
    _ZdlPv();
  }
  return param_2;
}


