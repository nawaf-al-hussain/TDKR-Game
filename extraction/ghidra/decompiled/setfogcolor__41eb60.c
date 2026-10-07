// _ZN15CWeatherManager11SetFogColorERKN6glitch4core8vector4dIfEE @ 0041eb60

void _ZN15CWeatherManager11SetFogColorERKN6glitch4core8vector4dIfEE
               (undefined4 param_1,float *param_2)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined1 local_c;
  undefined1 local_b;
  undefined1 local_a;
  undefined1 local_9;
  
  iVar1 = _ZN11Application11GetInstanceEv();
  iVar1 = *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
  uVar2 = VectorFloatToUnsigned(param_2[2] * DAT_0041ebf4,3);
  uVar3 = VectorFloatToUnsigned(param_2[3] * DAT_0041ebf4,3);
  local_9 = (undefined1)uVar2;
  uVar2 = VectorFloatToUnsigned(*param_2 * DAT_0041ebf4,3);
  local_c = (undefined1)uVar3;
  uVar3 = VectorFloatToUnsigned(param_2[1] * DAT_0041ebf4,3);
  local_b = (undefined1)uVar2;
  local_a = (undefined1)uVar3;
  _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterINS0_6SColorEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSC_
            (*(undefined4 *)(iVar1 + 0x154),*(undefined2 *)(iVar1 + 0x172),0,&local_c);
  return;
}


