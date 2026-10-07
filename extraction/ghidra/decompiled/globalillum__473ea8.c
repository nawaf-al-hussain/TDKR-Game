// _ZNSt6vectorIP27CTemplateGlobalIlluminationSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_ @ 00473ea8

void _ZNSt6vectorIP27CTemplateGlobalIlluminationSaIS1_EE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPS1_S3_EERKS1_
               (int *param_1,undefined4 *param_2,undefined4 *param_3)

{
  uint uVar1;
  int iVar2;
  uint uVar3;
  void *__dest;
  undefined4 *puVar4;
  int iVar5;
  undefined4 uVar6;
  uint uVar7;
  size_t sVar8;
  void *__dest_00;
  
  puVar4 = (undefined4 *)param_1[1];
  if (puVar4 == (undefined4 *)param_1[2]) {
    uVar3 = (int)puVar4 - *param_1 >> 2;
    if (uVar3 == 0) {
      iVar5 = 4;
      uVar7 = 1;
    }
    else {
      uVar1 = uVar3 * 2;
      uVar7 = 0x3fffffff;
      if (uVar1 < 0x3fffffff) {
        uVar7 = uVar1;
      }
      iVar5 = uVar7 << 2;
      if (uVar1 < uVar3) {
        iVar5 = -4;
        uVar7 = 0x3fffffff;
      }
    }
    iVar2 = (int)param_2 - *param_1 >> 2;
    __dest = (void *)0x0;
    if (uVar7 != 0) {
      __dest = (void *)_Znwj(iVar5);
    }
    if ((void *)((int)__dest + iVar2 * 4) != (void *)0x0) {
      *(undefined4 *)((int)__dest + iVar2 * 4) = *param_3;
    }
    iVar2 = (int)param_2 - *param_1 >> 2;
    sVar8 = 0;
    if (iVar2 != 0) {
      sVar8 = iVar2 << 2;
      memmove(__dest,(void *)*param_1,sVar8);
    }
    __dest_00 = (void *)((int)__dest + sVar8 + 4);
    iVar2 = param_1[1] - (int)param_2 >> 2;
    sVar8 = 0;
    if (iVar2 != 0) {
      sVar8 = iVar2 << 2;
      memmove(__dest_00,param_2,sVar8);
    }
    if (*param_1 != 0) {
      _ZdlPv();
    }
    *param_1 = (int)__dest;
    param_1[1] = (int)__dest_00 + sVar8;
    param_1[2] = (int)__dest + iVar5;
  }
  else {
    iVar5 = 0;
    if (puVar4 != (undefined4 *)0x0) {
      *puVar4 = puVar4[-1];
      iVar5 = param_1[1];
    }
    param_1[1] = iVar5 + 4;
    uVar6 = *param_3;
    iVar2 = (iVar5 + -4) - (int)param_2 >> 2;
    if (iVar2 != 0) {
      memmove((void *)(iVar5 + iVar2 * -4),param_2,iVar2 * 4);
    }
    *param_2 = uVar6;
  }
  return;
}


