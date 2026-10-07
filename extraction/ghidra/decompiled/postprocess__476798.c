// _ZNSt6vectorIP18CPostProcessEffectSaIS1_EE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPS1_S3_EEjRKS1_ @ 00476798

int * _ZNSt6vectorIP18CPostProcessEffectSaIS1_EE14_M_fill_insertEN9__gnu_cxx17__normal_iteratorIPS1_S3_EEjRKS1_
                (int *param_1,undefined4 *param_2,uint param_3,undefined4 *param_4)

{
  void *__dest;
  undefined4 *puVar1;
  int *piVar2;
  uint uVar3;
  int extraout_r2;
  int iVar4;
  int extraout_r3;
  int iVar5;
  int unaff_r8;
  undefined4 uVar6;
  size_t sVar7;
  uint uVar8;
  undefined4 *puVar9;
  int iVar10;
  bool bVar11;
  undefined8 uVar12;
  undefined1 auStack_28 [4];
  undefined4 *local_24;
  
  if (param_3 == 0) {
    return param_1;
  }
  puVar9 = (undefined4 *)param_1[1];
  if (param_3 <= (uint)(param_1[2] - (int)puVar9 >> 2)) {
    uVar6 = *param_4;
    uVar8 = (int)puVar9 - (int)param_2 >> 2;
    if (uVar8 <= param_3) {
      iVar5 = param_3 - uVar8;
      puVar1 = puVar9;
      iVar4 = iVar5;
      if (iVar5 != 0) {
        do {
          iVar4 = iVar4 + -1;
          *puVar1 = uVar6;
          puVar1 = puVar1 + 1;
        } while (iVar4 != 0);
        puVar1 = (undefined4 *)param_1[1];
      }
      puVar1 = puVar1 + iVar5;
      param_1[1] = (int)puVar1;
      sVar7 = 0;
      if (uVar8 != 0) {
        sVar7 = uVar8 << 2;
        memmove(puVar1,param_2,sVar7);
        puVar1 = (undefined4 *)param_1[1];
      }
      param_1[1] = (int)((int)puVar1 + sVar7);
      for (; puVar9 != param_2; param_2 = param_2 + 1) {
        *param_2 = uVar6;
      }
      return (int *)((int)puVar1 + sVar7);
    }
    iVar4 = (int)(param_3 * 4) >> 2;
    piVar2 = param_1;
    puVar1 = puVar9;
    if (iVar4 != 0) {
      piVar2 = memmove(puVar9,puVar9 + -param_3,iVar4 << 2);
      puVar1 = (undefined4 *)param_1[1];
    }
    param_1[1] = (int)(puVar1 + param_3);
    iVar4 = (int)(puVar9 + -param_3) - (int)param_2 >> 2;
    if (iVar4 != 0) {
      piVar2 = memmove(puVar9 + -iVar4,param_2,iVar4 * 4);
    }
    puVar9 = param_2 + param_3;
    for (; puVar9 != param_2; param_2 = param_2 + 1) {
      *param_2 = uVar6;
    }
    return piVar2;
  }
  iVar4 = *param_1;
  iVar5 = (int)puVar9 - iVar4;
  uVar8 = iVar5 >> 2;
  bVar11 = param_3 == 0x3fffffff - uVar8;
  if (0x3fffffff - uVar8 <= param_3 && !bVar11) {
    uVar12 = _ZSt20__throw_length_errorPKc((int)&DAT_004769e8 + DAT_004769e8);
    iVar4 = (int)uVar12;
    if (bVar11) {
      unaff_r8 = (unaff_r8 >> 0x13) - (int)auStack_28;
    }
    puVar9 = &DAT_004769e8;
    uVar6 = 0x3fffffff;
    iVar10 = extraout_r3;
    if ((int)((ulonglong)uVar12 >> 0x20) == 0) {
      if (extraout_r2 == iVar4 + 4) {
        uVar8 = 1;
      }
      else {
        uVar8 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareERKS7_
                          (extraout_r3,extraout_r2 + 0x10);
        uVar8 = uVar8 >> 0x1f;
      }
    }
    else {
      uVar8 = 1;
    }
    piVar2 = (int *)_Znwj(0x18);
    if (piVar2 + 4 != (int *)0x0) {
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (piVar2 + 4,extraout_r3);
      piVar2[5] = *(int *)(extraout_r3 + 4);
    }
    _ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
              (uVar8,piVar2,extraout_r2,iVar4 + 4,iVar10,param_1,param_2,param_3,uVar6,unaff_r8,
               iVar5,puVar9);
    *(int *)(iVar4 + 0x14) = *(int *)(iVar4 + 0x14) + 1;
    return piVar2;
  }
  if (uVar8 < param_3) {
    uVar3 = uVar8 + param_3;
  }
  else {
    uVar3 = uVar8 * 2;
  }
  if (uVar3 < uVar8) {
    iVar5 = -4;
    iVar4 = (int)param_2 - iVar4 >> 2;
  }
  else {
    uVar8 = 0x3fffffff;
    if (uVar3 < 0x3fffffff) {
      uVar8 = uVar3;
    }
    iVar5 = uVar8 << 2;
    iVar4 = (int)param_2 - iVar4 >> 2;
    __dest = (void *)0x0;
    if (uVar8 == 0) goto LAB_00476880;
  }
  local_24 = param_4;
  __dest = (void *)_Znwj(iVar5);
  param_4 = local_24;
LAB_00476880:
  uVar6 = *param_4;
  uVar8 = param_3;
  puVar9 = (undefined4 *)((int)__dest + iVar4 * 4);
  do {
    uVar8 = uVar8 - 1;
    *puVar9 = uVar6;
    puVar9 = puVar9 + 1;
  } while (uVar8 != 0);
  iVar4 = (int)param_2 - *param_1 >> 2;
  if (iVar4 == 0) {
    iVar4 = param_3 * 4;
    iVar10 = param_1[1] - (int)param_2;
  }
  else {
    sVar7 = iVar4 * 4;
    memmove(__dest,(void *)*param_1,sVar7);
    iVar4 = param_3 * 4 + sVar7;
    iVar10 = param_1[1] - (int)param_2;
  }
  sVar7 = 0;
  if (iVar10 >> 2 != 0) {
    sVar7 = (iVar10 >> 2) << 2;
    memmove((void *)((int)__dest + iVar4),param_2,sVar7);
  }
  piVar2 = (int *)0x0;
  if (*param_1 != 0) {
    piVar2 = (int *)_ZdlPv();
  }
  *param_1 = (int)__dest;
  param_1[1] = (int)__dest + iVar4 + sVar7;
  param_1[2] = (int)__dest + iVar5;
  return piVar2;
}


