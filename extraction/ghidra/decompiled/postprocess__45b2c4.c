// _ZN32CPostProcessEffect_CC_RadialBlurC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 0045b2c4

int * _ZN32CPostProcessEffect_CC_RadialBlurC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
                (int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined2 uVar2;
  undefined4 uVar3;
  undefined1 auStack_14 [4];
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_14);
  _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
            (param_1,auStack_14,param_3,param_4);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_14);
  iVar1 = DAT_0045b338;
  uVar3 = *(undefined4 *)(param_1[0xd] + 4);
  *param_1 = DAT_0045b334 + 0x45b31c;
  uVar2 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar3,iVar1 + 0x45b324,0);
  *(undefined2 *)((int)param_1 + 0x4a) = uVar2;
  return param_1;
}


