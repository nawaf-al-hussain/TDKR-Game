// _ZN29CPostProcessEffect_RadialBlurC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 0045a338

int * _ZN29CPostProcessEffect_RadialBlurC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
                (int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  undefined2 uVar3;
  undefined4 uVar4;
  undefined1 auStack_14 [4];
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_14);
  _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
            (param_1,auStack_14,param_3,param_4);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_14);
  iVar1 = DAT_0045a3bc;
  param_1[0x13] = 0;
  iVar2 = DAT_0045a3c0;
  uVar4 = *(undefined4 *)(param_1[0xd] + 4);
  param_1[0x14] = 0;
  *param_1 = iVar1 + 0x45a394;
  uVar3 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar4,iVar2 + 0x45a3a4,0);
  param_1[0x15] = 0x3f800000;
  *(undefined2 *)(param_1 + 0x16) = uVar3;
  return param_1;
}


