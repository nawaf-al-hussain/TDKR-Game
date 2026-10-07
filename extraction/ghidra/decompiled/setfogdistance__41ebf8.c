// _ZN15CWeatherManager14SetFogDistanceEff @ 0041ebf8

void _ZN15CWeatherManager14SetFogDistanceEff(undefined4 param_1,float param_2,float param_3)

{
  int iVar1;
  int iVar2;
  uint in_fpscr;
  float fVar3;
  float fVar4;
  float local_1c;
  float local_18;
  float local_14;
  
  iVar1 = _ZN11Application11GetInstanceEv();
  fVar4 = *(float *)(**(int **)(DAT_0041ecc8 + 0x41ec24) + 0x1c);
  local_1c = param_2 * fVar4;
  fVar4 = param_3 * fVar4 - local_1c;
  iVar2 = *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
  iVar1 = (int)fVar4;
  if (iVar1 < 0) {
    iVar1 = -iVar1;
  }
  fVar3 = (float)VectorSignedToFloat(iVar1,(byte)(in_fpscr >> 0x16) & 3);
  if (DAT_0041ecbc <= fVar3) {
    local_18 = 1.0 / fVar4;
  }
  else {
    local_18 = DAT_0041ecc4;
    if (fVar4 < 0.0) {
      local_18 = DAT_0041ecc0;
    }
  }
  local_14 = local_18;
  _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterINS_4core8vector3dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
            (*(undefined4 *)(iVar2 + 0x154),*(short *)(iVar2 + 0x172) + 2,0,&local_1c);
  return;
}

