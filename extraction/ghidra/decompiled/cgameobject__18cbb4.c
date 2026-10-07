// _ZN13CAIController15IsActorAttackedEP11CGameObjectfb @ 0018cbb4

undefined4
_ZN13CAIController15IsActorAttackedEP11CGameObjectfb
          (undefined4 param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 uVar2;
  
  iVar1 = _ZN6CLevel8GetLevelEv();
  if ((param_2 != *(int *)(iVar1 + 0xec)) &&
     (iVar1 = _ZN11CGameObject11IsAttackingEPS_b(*(int *)(iVar1 + 0xec),param_2,param_4), iVar1 != 0
     )) {
    return 1;
  }
  uVar2 = _ZN13CAIController15IsActorAttackedEP11CGameObjectfb_part_635
                    (param_1,param_2,param_3,param_4);
  return uVar2;
}

