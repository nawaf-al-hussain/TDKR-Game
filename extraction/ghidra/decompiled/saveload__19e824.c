// _ZN7CWeapon8SaveLoadEP13CMemoryStream @ 0019e824

void _ZN7CWeapon8SaveLoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  int *piVar6;
  code *pcVar7;
  undefined1 auStack_24 [4];
  undefined1 auStack_20 [4];
  undefined1 auStack_1c [12];
  
  _ZN13CMemoryStream4ReadERb(param_2,param_1 + 0x34);
  if (*(char *)(param_1 + 0x34) != '\0') {
    return;
  }
  if (*(int *)(param_1 + 8) != 0) {
    iVar2 = _ZNK11CGameObject12GetSceneNodeEv();
    if (((*(char *)(param_1 + 0x35) != '\0') &&
        (piVar6 = *(int **)(param_1 + 0x14), piVar6 != (int *)0x0)) && (iVar2 != 0)) {
      pcVar7 = *(code **)(*piVar6 + 0x74);
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2EPS3_b_constprop_3054(auStack_24,iVar2)
      ;
      (*pcVar7)(piVar6,auStack_24);
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(auStack_24);
    }
    *(undefined1 *)(param_1 + 0x35) = 0;
    if (((*(char *)(param_1 + 0x36) != '\0') &&
        (piVar6 = *(int **)(param_1 + 0x18), piVar6 != (int *)0x0)) && (iVar2 != 0)) {
      pcVar7 = *(code **)(*piVar6 + 0x74);
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2EPS3_b_constprop_3054(auStack_20,iVar2)
      ;
      (*pcVar7)(piVar6,auStack_20);
      _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(auStack_20);
    }
    *(undefined1 *)(param_1 + 0x36) = 0;
    if (*(char *)(param_1 + 0x109) != '\0') {
      _ZN15CTrailComponent14ForceStopTrailEj(*(undefined4 *)(param_1 + 0x24));
    }
    iVar4 = *(int *)(param_1 + 0x3c);
    iVar2 = *(int *)(param_1 + 0x38);
    if ((uint)(iVar4 - iVar2) >> 4 != 0) {
      uVar5 = 0;
      do {
        iVar1 = uVar5 * 0x10;
        uVar5 = uVar5 + 1;
        iVar3 = *(int *)(iVar2 + iVar1 + 8);
        if (iVar3 != 0) {
          iVar2 = _ZNK11CGameObject12GetComponentEi(iVar3,0x154bb0);
          if ((iVar2 != 0) && (*(char *)(iVar2 + 0x18) != '\0')) {
            _ZN14CPoolComponent13ReqInvalidateEv();
          }
          iVar2 = *(int *)(param_1 + 0x38);
          iVar4 = *(int *)(param_1 + 0x3c);
          *(undefined4 *)(iVar2 + iVar1 + 8) = 0;
        }
      } while (uVar5 < (uint)(iVar4 - iVar2 >> 4));
    }
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEC2EPS3_b_constprop_3054(auStack_1c,0);
    _ZN7CWeapon12SetTargetingEbP15CGameObjectBaseN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEEEi_constprop_3111
              (param_1,0,0,auStack_1c);
    _ZN5boost13intrusive_ptrIN6glitch5scene10ISceneNodeEED2Ev(auStack_1c);
  }
  return;
}


