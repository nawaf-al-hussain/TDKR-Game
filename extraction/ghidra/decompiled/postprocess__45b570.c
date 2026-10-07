// _ZN34CPostProcessEffect_CC_DepthOfFieldC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 0045b570

int * _ZN34CPostProcessEffect_CC_DepthOfFieldC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
                (int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined2 uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined1 auStack_14 [4];
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_14);
  _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
            (param_1,auStack_14,param_3,param_4);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_14);
  iVar3 = DAT_0045b61c;
  uVar2 = *(undefined4 *)(param_1[0xd] + 4);
  *param_1 = DAT_0045b618 + 0x45b5c8;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar2,iVar3 + 0x45b5d0,0);
  iVar3 = DAT_0045b620 + 0x45b5e4;
  *(undefined2 *)((int)param_1 + 0x4a) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar3,0);
  iVar3 = DAT_0045b624 + 0x45b600;
  *(undefined2 *)(param_1 + 0x13) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar3,0);
  *(undefined2 *)((int)param_1 + 0x4e) = uVar1;
  return param_1;
}


