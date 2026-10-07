// _ZThn112_N27CTemplateGlobalIllumination4LoadEP13CMemoryStream @ 0046aea4

void _ZThn112_N27CTemplateGlobalIllumination4LoadEP13CMemoryStream(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined1 uVar2;
  int iVar3;
  undefined4 uVar4;
  uint uVar5;
  undefined4 uVar6;
  void *__dest;
  uint uVar7;
  int extraout_r2;
  uint uVar8;
  undefined4 *puVar9;
  undefined4 extraout_r3;
  undefined4 *__src;
  uint uVar10;
  uint uVar11;
  size_t sVar12;
  void *pvVar13;
  undefined1 *puVar14;
  bool bVar15;
  undefined8 uVar16;
  undefined1 auStack_30 [4];
  void *pvStack_2c;
  
  puVar14 = auStack_30;
  iVar3 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(bool *)(param_1 + -0x6c) = iVar3 != 0;
  uVar4 = _ZN13CMemoryStream7ReadIntEv(param_2);
  *(undefined4 *)(param_1 + -0x68) = uVar4;
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -100) = uVar4;
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -0x60) = uVar4;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x5c) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x5b) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x5a) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x59) = uVar2;
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -0x58) = uVar4;
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -0x54) = uVar4;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x50) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x4f) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x4e) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x4d) = uVar2;
  uVar5 = _ZN13CMemoryStream7ReadIntEv(param_2);
  __src = *(undefined4 **)(param_1 + -0x48);
  __dest = *(void **)(param_1 + -0x4c);
  uVar10 = (int)__src - (int)__dest >> 3;
  if (uVar5 <= uVar10) {
    if (uVar5 < uVar10) {
      *(void **)(param_1 + -0x48) = (void *)((int)__dest + uVar5 * 8);
    }
    goto LAB_002121d8;
  }
  uVar11 = uVar5 - uVar10;
  if (uVar11 == 0) goto LAB_002121d8;
  uVar8 = uVar11;
  puVar9 = __src;
  if (uVar11 <= (uint)(*(int *)(param_1 + -0x44) - (int)__src >> 3)) {
    do {
      uVar8 = uVar8 - 1;
      *puVar9 = 0;
      puVar9[1] = 0;
      puVar9 = puVar9 + 2;
    } while (uVar8 != 0);
    *(undefined4 **)(param_1 + -0x48) = __src + uVar11 * 2;
    goto LAB_002121d8;
  }
  bVar15 = uVar11 == 0x1fffffff - uVar10;
  if (0x1fffffff - uVar10 <= uVar11 && !bVar15) {
    uVar16 = _ZSt20__throw_length_errorPKc((int)&DAT_002123a8 + DAT_002123a8);
    uVar4 = (undefined4)((ulonglong)uVar16 >> 0x20);
    iVar3 = (int)uVar16;
    if (bVar15) {
      puVar14 = (undefined1 *)(extraout_r2 + (uVar11 >> 0x1a));
    }
    *(int **)(puVar14 + -4) = &DAT_002123a8;
    *(int *)(puVar14 + -8) = param_1 + -0x70;
    *(undefined4 *)(puVar14 + -0xc) = param_2;
    *(undefined4 *)(puVar14 + -0x10) = extraout_r3;
    _ZN19CComponentLevelInit4LoadEP13CMemoryStream();
    uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar4);
    *(undefined4 *)(iVar3 + -0x10) = uVar6;
    _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
              (uVar4,iVar3 + -0xc);
    uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar4);
    *(undefined4 *)(iVar3 + -8) = uVar6;
    uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar4);
    *(undefined4 *)(iVar3 + -4) = uVar6;
    _ZN25CComponentBaseGlobalIllum4LoadEP13CMemoryStream(iVar3,uVar4);
    uVar4 = _ZN13CMemoryStream7ReadIntEv(uVar4);
    *(undefined4 *)(iVar3 + 0x70) = uVar4;
    return;
  }
  if (uVar11 < uVar10) {
    uVar8 = uVar10 * 2;
  }
  else {
    uVar8 = uVar10 + uVar11;
  }
  if (uVar8 < uVar10) {
    iVar3 = -8;
LAB_00212380:
    __dest = (void *)_Znwj(iVar3);
    pvVar13 = *(void **)(param_1 + -0x4c);
    uVar8 = (int)__src - (int)pvVar13 >> 3;
  }
  else {
    uVar7 = 0x1fffffff;
    if (uVar8 < 0x1fffffff) {
      uVar7 = uVar8;
    }
    iVar3 = uVar7 << 3;
    pvVar13 = __dest;
    __dest = (void *)0x0;
    uVar8 = uVar10;
    if (uVar7 != 0) goto LAB_00212380;
  }
  uVar7 = uVar11;
  puVar9 = (undefined4 *)((int)__dest + uVar10 * 8);
  do {
    uVar7 = uVar7 - 1;
    *puVar9 = 0;
    puVar9[1] = 0;
    puVar9 = puVar9 + 2;
  } while (uVar7 != 0);
  if (uVar8 == 0) {
    sVar12 = 0;
  }
  else {
    sVar12 = uVar8 << 3;
    memmove(__dest,pvVar13,sVar12);
  }
  pvVar13 = (void *)((int)__dest + uVar11 * 8 + sVar12);
  iVar1 = *(int *)(param_1 + -0x48) - (int)__src >> 3;
  sVar12 = 0;
  if (iVar1 != 0) {
    sVar12 = iVar1 << 3;
    memmove(pvVar13,__src,sVar12);
  }
  if (*(int *)(param_1 + -0x4c) != 0) {
    _ZdlPv();
  }
  *(void **)(param_1 + -0x4c) = __dest;
  *(size_t *)(param_1 + -0x48) = (int)pvVar13 + sVar12;
  *(int *)(param_1 + -0x44) = (int)__dest + iVar3;
LAB_002121d8:
  if (0 < (int)uVar5) {
    uVar10 = 0;
    while( true ) {
      iVar3 = uVar10 * 8;
      pvStack_2c = __dest;
      uVar4 = _ZN13CMemoryStream7ReadIntEv(param_2);
      *(undefined4 *)((int)pvStack_2c + uVar10 * 8) = uVar4;
      uVar4 = _ZN13CMemoryStream7ReadIntEv(param_2);
      uVar10 = uVar10 + 1;
      *(undefined4 *)((int)__dest + iVar3 + 4) = uVar4;
      if (uVar10 == uVar5) break;
      __dest = *(void **)(param_1 + -0x4c);
    }
  }
  iVar3 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(bool *)(param_1 + -0x40) = iVar3 != 0;
  iVar3 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(bool *)(param_1 + -0x3f) = iVar3 != 0;
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + -0x3c);
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + -0x38);
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + -0x34);
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -0x30) = uVar4;
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -0x2c) = uVar4;
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -0x28) = uVar4;
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -0x24) = uVar4;
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (param_2,param_1 + -0x20);
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -0x1c) = uVar4;
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -0x18) = uVar4;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x14) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x13) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x12) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -0x11) = uVar2;
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -0x10) = uVar4;
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -0xc) = uVar4;
  uVar4 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + -8) = uVar4;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -4) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -3) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -2) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(param_2);
  *(undefined1 *)(param_1 + -1) = uVar2;
  return;
}


