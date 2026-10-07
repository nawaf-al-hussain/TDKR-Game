// _ZN19CPostProcessManager22BeginRenderReflectionsEv @ 00457648

void _ZN19CPostProcessManager22BeginRenderReflectionsEv(int param_1)

{
  int iVar1;
  int *piVar2;
  byte bVar3;
  int *piVar4;
  int iVar5;
  uint in_fpscr;
  float fVar6;
  float fVar7;
  float local_2c;
  float local_28;
  float local_24;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  
  iVar5 = *(int *)(*(int *)(param_1 + 0x14) + 8);
  piVar4 = *(int **)(*(int *)(DAT_0045783c + 0x457658) + 0x10);
  _ZN11Application11GetInstanceEv();
  iVar1 = _ZN11Application11GetInstanceEv();
  piVar2 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
  (**(code **)(*piVar2 + 0x70))(piVar2,iVar5);
  local_18 = *(undefined4 *)(iVar5 + 0x18);
  local_14 = *(undefined4 *)(iVar5 + 0x1c);
  local_20 = 0;
  local_1c = 0;
  (**(code **)(**(int **)(piVar4[0x48] + -4) + 0xc))(*(int **)(piVar4[0x48] + -4),&local_20);
  iVar1 = _ZN6CLevel8GetLevelEv();
  if (((iVar1 == 0) || (iVar1 = _ZN6CLevel8GetLevelEv(), *(char *)(iVar1 + 0xa50) == '\0')) &&
     (*(char *)(DAT_00457844 + 0x4577d4) == '\0')) {
    iVar1 = piVar4[10];
    bVar3 = *(byte *)((int)piVar4 + 0x292);
    piVar4[10] = 0;
    if (iVar1 != 0) {
      bVar3 = bVar3 | 1;
    }
    *(byte *)((int)piVar4 + 0x292) = bVar3;
  }
  else {
    iVar1 = piVar4[10];
    bVar3 = *(byte *)((int)piVar4 + 0x292);
    piVar4[10] = -1;
    if (iVar1 != -1) {
      bVar3 = bVar3 | 1;
    }
    *(byte *)((int)piVar4 + 0x292) = bVar3;
  }
  (**(code **)(*piVar4 + 0x94))(piVar4,0xffffffff);
  *(undefined1 *)(iVar5 + 0x20) = 1;
  iVar1 = _ZN6CLevel8GetLevelEv();
  if (*(int *)(iVar1 + 0xa98) != 0) {
    iVar1 = _ZN11Application11GetInstanceEv();
    fVar7 = *(float *)(**(int **)(DAT_00457840 + 0x457740) + 0x1c);
    local_2c = fVar7 * DAT_00457828;
    fVar7 = fVar7 * DAT_0045782c - local_2c;
    iVar5 = *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
    iVar1 = (int)fVar7;
    if (iVar1 < 0) {
      iVar1 = -iVar1;
    }
    fVar6 = (float)VectorSignedToFloat(iVar1,(byte)(in_fpscr >> 0x16) & 3);
    if (DAT_00457830 <= fVar6) {
      local_28 = 1.0 / fVar7;
    }
    else {
      local_28 = DAT_00457838;
      if (fVar7 < 0.0) {
        local_28 = DAT_00457834;
      }
    }
    local_24 = local_28;
    _ZN6glitch5video6detail19IMaterialParametersINS0_31CGlobalMaterialParameterManagerENS1_30globalmaterialparametermanager10SEmptyBaseEE12setParameterINS_4core8vector3dIfEEEEN5boost9enable_ifINS1_36SIsValidSetMaterialParamaterOverloadIT_EEbE4typeEtjRKSE_
              (*(undefined4 *)(iVar5 + 0x154),*(short *)(iVar5 + 0x172) + 2,0,&local_2c);
  }
  return;
}


