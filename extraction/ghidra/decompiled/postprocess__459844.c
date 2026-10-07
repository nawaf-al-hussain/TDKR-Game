// _ZN24CPostProcessEffect_BlendC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 00459844

int * _ZN24CPostProcessEffect_BlendC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
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
  iVar3 = DAT_00459918;
  uVar2 = *(undefined4 *)(param_1[0xd] + 4);
  *param_1 = DAT_00459914 + 0x45989c;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar2,iVar3 + 0x4598a4,0);
  iVar3 = DAT_0045991c + 0x4598b8;
  *(undefined2 *)((int)param_1 + 0x4a) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar3,0);
  iVar3 = DAT_00459920 + 0x4598d4;
  *(undefined2 *)(param_1 + 0x13) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar3,0);
  iVar3 = DAT_00459924 + 0x4598f0;
  *(undefined2 *)((int)param_1 + 0x4e) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar3,0);
  param_1[0x15] = -0x40800000;
  *(undefined2 *)(param_1 + 0x14) = uVar1;
  return param_1;
}


