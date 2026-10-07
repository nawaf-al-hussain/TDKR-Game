// _ZN19CPostProcessManager13DisableEffectESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE @ 0045810c

void _ZN19CPostProcessManager13DisableEffectESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
               (int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  
  iVar5 = param_1 + 0x24;
  iVar4 = *(int *)(param_1 + 0x28);
  iVar3 = iVar5;
  while (iVar4 != 0) {
    iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                      (iVar4 + 0x10,param_2);
    if (iVar1 < 0) {
      iVar4 = *(int *)(iVar4 + 0xc);
    }
    else {
      iVar4 = *(int *)(iVar4 + 8);
      iVar3 = iVar4;
    }
  }
  iVar4 = iVar5;
  if ((iVar5 != iVar3) &&
     (iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                        (param_2,iVar3 + 0x10), iVar4 = iVar3, iVar1 < 0)) {
    iVar4 = iVar5;
  }
  if (iVar5 == iVar4) {
    return;
  }
  puVar2 = *(undefined4 **)(*(int *)(param_1 + 8) + *(int *)(iVar4 + 0x14) * 4);
  if (*(char *)(puVar2 + 0x12) != '\0') {
    return;
  }
  (**(code **)*puVar2)();
  return;
}


