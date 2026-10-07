// _ZN23CPostProcessEffect_BlurC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 0045a278

int * _ZN23CPostProcessEffect_BlurC1ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
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
  iVar3 = DAT_0045a32c;
  uVar2 = *(undefined4 *)(param_1[0xd] + 4);
  *param_1 = DAT_0045a328 + 0x45a2d0;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct(uVar2,iVar3 + 0x45a2d8,0);
  param_1[0x13] = 0x3cf5c28f;
  iVar3 = DAT_0045a330 + 0x45a2f8;
  *(undefined2 *)(param_1 + 0x16) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar3,0);
  param_1[0x14] = 0x3d4ccccd;
  param_1[0x15] = 0x3f666666;
  *(undefined2 *)((int)param_1 + 0x5a) = uVar1;
  return param_1;
}


