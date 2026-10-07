// _ZN30CPostProcessEffect_CC_HeatHazeC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager @ 0045b360

int * _ZN30CPostProcessEffect_CC_HeatHazeC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager
                (int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 uVar3;
  undefined1 auStack_18 [4];
  undefined1 auStack_14 [4];
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_18);
  _ZN18CPostProcessEffectC2ESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEERNS2_7collada16CColladaDatabaseEP19CPostProcessManager_constprop_2436
            (param_1,auStack_18,param_3,param_4);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_18);
  *param_1 = DAT_0045b4bc + 0x45b3ac;
  iVar2 = _ZN11Application11GetInstanceEv();
  _ZN6glitch5video15CTextureManager10getTextureEPKcS3_
            (auStack_14,
             *(undefined4 *)
              (*(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8) + 0x14c),
             DAT_0045b4c0 + 0x45b3c4,0);
  iVar2 = param_1[0xd];
  uVar3 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(iVar2 + 4),DAT_0045b4c4 + 0x45b3ec,0);
  _ZN6glitch5video6detail19IMaterialParametersINS0_9CMaterialENS_24ISharedMemoryBlockHeaderIS3_EEE12setParameterIN5boost13intrusive_ptrINS0_8ITextureEEEEENS8_9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (iVar2,uVar3,0,auStack_14);
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),DAT_0045b4c8 + 0x45b414,0);
  iVar2 = DAT_0045b4cc + 0x45b42c;
  *(undefined2 *)((int)param_1 + 0x4a) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar2,0);
  iVar2 = DAT_0045b4d0 + 0x45b448;
  *(undefined2 *)(param_1 + 0x13) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar2,0);
  iVar2 = DAT_0045b4d4 + 0x45b464;
  *(undefined2 *)((int)param_1 + 0x4e) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar2,0);
  iVar2 = DAT_0045b4d8 + 0x45b480;
  *(undefined2 *)(param_1 + 0x14) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar2,0);
  iVar2 = DAT_0045b4dc + 0x45b49c;
  *(undefined2 *)((int)param_1 + 0x52) = uVar1;
  uVar1 = _ZNK6glitch5video17CMaterialRenderer14getParameterIDEPKct
                    (*(undefined4 *)(param_1[0xd] + 4),iVar2,0);
  *(undefined2 *)(param_1 + 0x15) = uVar1;
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(auStack_14);
  return param_1;
}


