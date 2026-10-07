// _Z16CActorIsAttackedP11CGameObjectb @ 00178008

undefined4 _Z16CActorIsAttackedP11CGameObjectb(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 uVar2;
  
  uVar2 = *(undefined4 *)(DAT_00178060 + 0x178020);
  iVar1 = _ZN6CLevel8GetLevelEv();
  if ((param_1 != *(int *)(iVar1 + 0xec)) &&
     (iVar1 = _ZN11CGameObject11IsAttackingEPS_b(*(int *)(iVar1 + 0xec),param_1,param_2), iVar1 != 0
     )) {
    return 1;
  }
  uVar2 = _ZN13CAIController15IsActorAttackedEP11CGameObjectfb_part_635(uVar2,param_1,0,param_2);
  return uVar2;
}

