// _ZN23CPostProcessEffect_GrayC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 0045a430

int * _ZN23CPostProcessEffect_GrayC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
                (int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  undefined2 uVar3;
  undefined1 auStack_20 [4];
  int local_1c [2];
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_20);
  _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
            (param_1,auStack_20,param_3,param_4);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_20);
  iVar2 = DAT_0045a504;
  iVar1 = DAT_0045a500;
  param_1[0x14] = 0;
  param_1[0x15] = 0;
  *param_1 = iVar1 + 0x45a490;
  param_1[0x16] = 0;
  param_1[0x17] = 0;
  uVar3 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar2 + 0x45a498,0);
  iVar1 = DAT_0045a508;
  param_1[0x13] = 0x3f800000;
  *(undefined2 *)(param_1 + 0x18) = uVar3;
  uVar3 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar1 + 0x45a4c4,0);
  local_1c[0] = param_1[0x17];
  param_1[0x14] = 0;
  param_1[0x15] = 0;
  param_1[0x16] = 0;
  param_1[0x17] = 0;
  *(undefined2 *)((int)param_1 + 0x62) = uVar3;
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(local_1c);
  return param_1;
}


