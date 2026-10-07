// _Z27CSetCrowdInterractionStatesP11CGameObjectS0_RKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESB_SB_SB_ @ 0017999c

void _Z27CSetCrowdInterractionStatesP11CGameObjectS0_RKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESB_SB_SB_
               (int *param_1,int *param_2,undefined4 *param_3,undefined4 *param_4,
               undefined4 *param_5,undefined4 *param_6)

{
  undefined4 uVar1;
  int iVar2;
  code *pcVar3;
  
  pcVar3 = *(code **)(*param_2 + 0x5c);
  uVar1 = (**(code **)(*param_1 + 0x18))();
  (*pcVar3)(param_2,uVar1,0,0,1,1);
  iVar2 = _ZN11CGameObject12GetActorSideEPS_(param_1,param_2);
  if (iVar2 == 0) {
    _ZN18CStateSetComponent22SetStateWithTransitionEPKcsfiiP17CContainerTrigger
              (param_1[0x2d],*param_3,1,0,0xffffffff,0xffffffff,0);
    _ZN18CStateSetComponent22SetStateWithTransitionEPKcsfiiP17CContainerTrigger
              (param_2[0x2d],*param_5,0,0,0xffffffff,0xffffffff,0);
  }
  else {
    _ZN18CStateSetComponent22SetStateWithTransitionEPKcsfiiP17CContainerTrigger
              (param_1[0x2d],*param_4,1,0,0xffffffff,0xffffffff,0);
    _ZN18CStateSetComponent22SetStateWithTransitionEPKcsfiiP17CContainerTrigger
              (param_2[0x2d],*param_6,0,0,0xffffffff,0xffffffff,0);
  }
  return;
}

