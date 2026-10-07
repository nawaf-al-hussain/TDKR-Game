// _Z10CKillActorP11CGameObjectSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEEb @ 00179284

void _Z10CKillActorP11CGameObjectSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS3_6memory13E_MEMORY_HINTE0EEEEb
               (int param_1,int *param_2,undefined4 param_3)

{
  undefined1 auStack_14 [8];
  
  if (*(int *)(*param_2 + -0xc) == 0) {
    param_3 = 1;
  }
  if (param_1 != 0) {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (auStack_14);
    _ZN11CGameObject4KillESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEbPS_
              (param_1,auStack_14,param_3,0);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_14);
  }
  return;
}

