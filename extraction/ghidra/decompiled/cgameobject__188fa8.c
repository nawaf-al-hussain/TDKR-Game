// _ZN13CAIController17KillEnemiesInAreaEP11CGameObjectRN6glitch4core8vector3dIfEEfi @ 00188fa8

void _ZN13CAIController17KillEnemiesInAreaEP11CGameObjectRN6glitch4core8vector3dIfEEfi
               (int param_1,undefined4 param_2,float *param_3,float param_4)

{
  float fVar1;
  int iVar2;
  float *pfVar3;
  undefined4 uVar4;
  float fVar5;
  int iVar6;
  int *piVar7;
  int *local_7c;
  undefined1 auStack_78 [4];
  undefined1 auStack_74 [4];
  int local_70;
  undefined4 *local_6c;
  undefined4 *local_68;
  float local_64;
  float local_60;
  float local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  
  local_30 = 0;
  local_2c = 0;
  local_40 = 0x461c3c00;
  local_28 = 0;
  local_3c = 9;
  local_70 = 0;
  local_6c = (undefined4 *)0x0;
  local_68 = (undefined4 *)0x0;
  local_38 = 0xffffffff;
  local_34 = 0;
  local_24 = param_2;
  for (iVar6 = *(int *)(param_1 + 0xb8); param_1 + 0xb0 != iVar6;
      iVar6 = _ZSt18_Rb_tree_incrementPKSt18_Rb_tree_node_base(iVar6)) {
    local_7c = *(int **)(iVar6 + 0x10);
    iVar2 = (**(code **)(*local_7c + 0x54))(local_7c);
    if (((iVar2 != 0) && (iVar2 = _ZNK11CGameObject7IsEnemyEv(local_7c), iVar2 != 0)) &&
       (pfVar3 = (float *)(**(code **)(*local_7c + 0x18))(),
       (*pfVar3 - *param_3) * (*pfVar3 - *param_3) +
       (pfVar3[1] - param_3[1]) * (pfVar3[1] - param_3[1]) +
       (pfVar3[2] - param_3[2]) * (pfVar3[2] - param_3[2]) <= param_4 * param_4)) {
      if (local_6c == local_68) {
        _ZNSt6vectorIP11CGameObjectSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
                  (&local_70,local_6c,&local_7c);
      }
      else {
        if (local_6c != (undefined4 *)0x0) {
          *local_6c = local_7c;
        }
        local_6c = local_6c + 1;
      }
    }
  }
  iVar6 = (int)local_6c - local_70 >> 2;
  if (0 < iVar6) {
    uVar4 = _ZN6CLevel8GetLevelEv();
    fVar1 = DAT_00189228;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2100
              (auStack_78,DAT_0018922c + 0x1890fc);
    local_64 = *param_3;
    local_60 = param_3[1];
    local_5c = param_3[2];
    iVar2 = 0;
    local_58 = 0;
    local_54 = 0;
    local_50 = 0;
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2EPS3_b_constprop_3054(auStack_74,0);
    local_4c = 0x3f800000;
    local_48 = 0x3f800000;
    local_44 = 0x3f800000;
    _ZN6CLevel11StartEffectERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEENS3_8vector3dIfEESC_N5boost13intrusive_ptrINS2_5scene10ISceneNodeEEESC_bP11CGameObject
              (uVar4,auStack_78,&local_64,&local_58,auStack_74,&local_4c,0,0);
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(auStack_74);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_78);
    do {
      piVar7 = *(int **)(local_70 + iVar2 * 4);
      fVar5 = (float)_ZN11CGameObject12GetMaxHealthEv(piVar7);
      uVar4 = 0x47c34f80;
      if (fVar1 <= fVar5) {
        uVar4 = _ZN11CGameObject12GetMaxHealthEv(piVar7);
      }
      iVar2 = iVar2 + 1;
      local_40 = uVar4;
      (**(code **)(*piVar7 + 0xac))(piVar7,&local_40);
      (**(code **)(*piVar7 + 0xa8))(piVar7,&local_40);
    } while (iVar2 != iVar6);
  }
  if (local_70 != 0) {
    _ZdlPv();
  }
  return;
}

