// _Z27CActorWeaponEnableTargetingP11CGameObjectS0_ @ 00177a80

void _Z27CActorWeaponEnableTargetingP11CGameObjectS0_(int param_1,int *param_2)

{
  bool bVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  int iVar5;
  int *local_1c;
  int *local_18;
  undefined1 auStack_14 [4];
  
  if ((*(int *)(param_1 + 0xb8) != 0) &&
     (iVar5 = *(int *)(*(int *)(param_1 + 0xb8) + 0x2e0), iVar5 != 0)) {
    if ((param_2 == (int *)0x0) || (iVar2 = _ZN11CGameObject7IsHumanEv(param_2), iVar2 == 0)) {
      uVar3 = _ZN6CLevel8GetLevelEv();
      uVar4 = (**(code **)(*param_2 + 0x14))(param_2);
      uVar3 = _ZN6CLevel20FindObjectOrWaypointEi(uVar3,uVar4);
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2EPS3_b_constprop_3054(auStack_14,0);
      _ZN7CWeapon12SetTargetingEbP15CGameObjectBaseN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEEi_constprop_3111
                (iVar5,1,uVar3,auStack_14);
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(auStack_14);
    }
    else {
      uVar3 = _ZNK11CGameObject12GetSceneNodeEv(param_2);
      _ZN6glitch5scene10ISceneNode20getSceneNodeFromNameEPKc
                (&local_1c,uVar3,DAT_00177b98 + 0x177ad0);
      local_18 = local_1c;
      if (local_1c != (int *)0x0) {
        local_1c = (int *)((int)local_1c + *(int *)(*local_1c + -0x10) + 4);
        DataMemoryBarrier(0xf);
        do {
          bVar1 = (bool)hasExclusiveAccess(local_1c);
        } while (!bVar1);
        *local_1c = *local_1c + 1;
        DataMemoryBarrier(0xf);
      }
      _ZN7CWeapon12SetTargetingEbP15CGameObjectBaseN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEEi_constprop_3111
                (iVar5,1,0,&local_18);
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(&local_18);
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(&local_1c);
    }
  }
  return;
}

