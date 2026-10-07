// _Z28CActorWeaponDisableTargetingP11CGameObject @ 00177b9c

void _Z28CActorWeaponDisableTargetingP11CGameObject(int param_1)

{
  undefined4 uVar1;
  undefined1 auStack_c [4];
  
  uVar1 = *(undefined4 *)(*(int *)(param_1 + 0xb8) + 0x2e0);
  _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2EPS3_b_constprop_3054(auStack_c,0);
  _ZN7CWeapon12SetTargetingEbP15CGameObjectBaseN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEEi_constprop_3111
            (uVar1,0,0,auStack_c);
  _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(auStack_c);
  return;
}

