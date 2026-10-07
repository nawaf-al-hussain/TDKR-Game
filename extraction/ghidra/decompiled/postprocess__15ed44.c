// _Z26PostProcessingEffectRemoveP9lua_State @ 0015ed44

undefined4 _Z26PostProcessingEffectRemoveP9lua_State(undefined4 param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined1 auStack_10 [4];
  undefined1 auStack_c [4];
  
  iVar1 = _ZN6CLevel8GetLevelEv();
  if (iVar1 != 0) {
    uVar2 = lua_tolstring(param_1,1,0);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2100
              (auStack_10,uVar2);
    iVar1 = *(int *)(**(int **)(DAT_0015edc4 + 0x15ed84) + 0x178);
    if (iVar1 != 0) {
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (auStack_c,auStack_10);
      _ZN19CPostProcessManager13DisableEffectESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (iVar1,auStack_c);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (auStack_c);
    }
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (auStack_10);
  }
  return 0;
}


