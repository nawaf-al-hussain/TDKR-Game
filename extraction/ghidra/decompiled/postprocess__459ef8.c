// _ZN31CPostProcessEffect_DepthOfFieldC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 00459ef8

int * _ZN31CPostProcessEffect_DepthOfFieldC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
                (int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined2 uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined1 auStack_1c [8];
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_1c);
  _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
            (param_1,auStack_1c,param_3,param_4);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_1c);
  iVar3 = DAT_00459fc8;
  uVar2 = *(undefined4 *)(param_1[0xd] + 4);
  *param_1 = DAT_00459fc4 + 0x459f58;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar2,iVar3 + 0x459f60,0);
  iVar3 = DAT_00459fcc + 0x459f7c;
  param_1[0x13] = 0x40c00000;
  *(undefined2 *)(param_1 + 0x17) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar3,0);
  iVar3 = DAT_00459fd0;
  param_1[0x16] = 0x40800000;
  param_1[0x15] = 0x3f800000;
  *(undefined2 *)(param_1 + 0x18) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar3 + 0x459fa4,0);
  param_1[0x14] = 0x40800000;
  *(undefined2 *)((int)param_1 + 0x5e) = uVar1;
  return param_1;
}


