// _ZN15CWeatherManager11SetFogColorERKN6glitch5video6SColorE @ 0041eb28

void _ZN15CWeatherManager11SetFogColorERKN6glitch5video6SColorE
               (undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  
  iVar1 = _ZN11Application11GetInstanceEv();
  iVar1 = *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
  _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
            (*(undefined4 *)(iVar1 + 0x154),*(undefined2 *)(iVar1 + 0x172),0,param_2);
  return;
}

