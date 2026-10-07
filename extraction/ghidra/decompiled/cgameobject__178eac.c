// _Z21CSetMeleeAttackParamsP11CGameObjectRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESB_SB_SB_ @ 00178eac

void _Z21CSetMeleeAttackParamsP11CGameObjectRKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEESB_SB_SB_
               (int param_1,int *param_2,int *param_3,int *param_4,int *param_5)

{
  if (*(int *)(*param_2 + -0xc) != 0) {
    _ZN19CActorBaseComponent12SetHurtStateERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
              (*(undefined4 *)(param_1 + 0xb8));
  }
  if (*(int *)(*param_3 + -0xc) != 0) {
    _ZN19CActorBaseComponent11SetDieStateERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
              (*(undefined4 *)(param_1 + 0xb8),param_3);
  }
  if (*(int *)(*param_4 + -0xc) == 0) {
    if (*(int *)(*param_5 + -0xc) == 0) {
      return;
    }
  }
  else {
    _ZN19CActorBaseComponent12SetHitEffectERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
              (*(undefined4 *)(param_1 + 0xb8),param_4);
    if (*(int *)(*param_5 + -0xc) == 0) {
      return;
    }
  }
  _ZN19CActorBaseComponent10SetHitBoneERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (*(undefined4 *)(param_1 + 0xb8),param_5);
  return;
}

