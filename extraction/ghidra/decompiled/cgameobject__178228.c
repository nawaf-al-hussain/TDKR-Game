// _Z19CPlayEffectOnObjectPKcP11CGameObjectfffbS0_fffb @ 00178228

void _Z19CPlayEffectOnObjectPKcP11CGameObjectfffbS0_fffb
               (undefined4 param_1,int *param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5,char param_6,char *param_7,undefined4 param_8,undefined4 param_9,
               undefined4 param_10,undefined1 param_11)

{
  char cVar1;
  bool bVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  int iVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  int *piVar8;
  undefined4 uVar9;
  undefined1 auStack_7c [4];
  int *local_78;
  undefined1 auStack_74 [4];
  int *local_70;
  int *local_6c;
  undefined1 auStack_68 [4];
  undefined1 auStack_64 [4];
  int *local_60;
  undefined4 local_5c;
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
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2100
            (auStack_7c,param_1);
  _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2EPS3_b_constprop_3054(&local_78,0);
  puVar3 = (undefined4 *)(**(code **)(*param_2 + 0x18))(param_2);
  uVar4 = *puVar3;
  uVar7 = puVar3[2];
  uVar9 = puVar3[1];
  if (param_6 != '\0') {
    cVar1 = *param_7;
    if (cVar1 != '\0') {
      _ZNK11CGameObject15GetSceneNodePtrEv(auStack_74,param_2);
      _Z23GU_GetSceneNodeFromNameRKN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEEPKc
                (&local_70,auStack_74,param_7);
    }
    else {
      uVar4 = _ZNK11CGameObject12GetSceneNodeEv(param_2);
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2EPS3_b_constprop_3054(&local_70,uVar4);
    }
    local_60 = local_78;
    if (local_70 != (int *)0x0) {
      piVar8 = (int *)((int)local_70 + *(int *)(*local_70 + -0x10) + 4);
      DataMemoryBarrier(0xf);
      do {
        bVar2 = (bool)hasExclusiveAccess(piVar8);
      } while (!bVar2);
      *piVar8 = *piVar8 + 1;
      DataMemoryBarrier(0xf);
    }
    local_78 = local_70;
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(&local_60);
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(&local_70);
    if (cVar1 != '\0') {
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(auStack_74);
    }
    if (local_78 == (int *)0x0) goto LAB_00178504;
    iVar5 = _ZNK11CGameObject12GetSceneNodeEv(param_2);
    *(uint *)(iVar5 + 0xf4) = *(uint *)(iVar5 + 0xf4) | 0x1000;
    uVar4 = param_3;
    uVar7 = param_5;
    uVar9 = param_4;
  }
  uVar6 = _ZN6CLevel8GetLevelEv();
  local_5c = 0;
  local_58 = 0;
  local_54 = 0;
  local_6c = local_78;
  if (local_78 != (int *)0x0) {
    piVar8 = (int *)((int)local_78 + *(int *)(*local_78 + -0x10) + 4);
    DataMemoryBarrier(0xf);
    do {
      bVar2 = (bool)hasExclusiveAccess(piVar8);
    } while (!bVar2);
    *piVar8 = *piVar8 + 1;
    DataMemoryBarrier(0xf);
  }
  local_44 = param_8;
  local_40 = param_9;
  local_3c = param_10;
  local_50 = uVar4;
  local_4c = uVar9;
  local_48 = uVar7;
  piVar8 = (int *)_ZN6CLevel11StartEffectERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEENS3_8vector3dIfEESC_N5boost13intrusive_ptrINS2_5scene10ISceneNodeEEESC_bP11CGameObject
                            (uVar6,auStack_7c,&local_50,&local_5c,&local_6c,&local_44,param_11,0);
  _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(&local_6c);
  (**(code **)(*param_2 + 0x14))(param_2);
  if (piVar8 != (int *)0x0) {
    if (param_6 == '\0') {
      local_38 = 0;
      local_34 = 0;
      local_30 = 0;
      local_2c = 0x3f800000;
      _ZNK11CGameObject21GetQuaternionRotationERN6glitch4core10quaternionE(param_2,&local_38);
      (**(code **)(*piVar8 + 0x30))(piVar8,&local_38);
    }
    else if ((char)param_2[0x1f] != '\0') {
      uVar4 = _ZNK11CGameObject12GetSceneNodeEv(piVar8);
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2EPS3_b_constprop_3054(auStack_68,uVar4)
      ;
      _Z11SetGameDataN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEEj(auStack_68,1);
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(auStack_68);
      _ZN11CGameObject16SetAlwaysVisibleEb(piVar8,1);
    }
    uVar4 = _ZNK11CGameObject12GetComponentEi(piVar8,0x2ca13c06);
    uVar7 = (**(code **)(*param_2 + 0x14))(param_2);
    _Z14AddEffectEntryiPcS_P16CEffectComponent(uVar7,param_7,param_1,uVar4);
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2EPS3_b_constprop_3054(auStack_64,0);
    _ZN11CGameObject12LinkToObjectEPS_RKN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEE
              (piVar8,param_2,auStack_64);
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(auStack_64);
    _ZN11CGameObject13SetChildFlagsEi(piVar8,10);
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(&local_78);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_7c);
    return;
  }
LAB_00178504:
  _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(&local_78);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_7c);
  return;
}

