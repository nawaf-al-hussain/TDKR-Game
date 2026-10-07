// _ZNK25CComponentBaseGlobalIllum5CloneEv @ 00211e84

int * _ZNK25CComponentBaseGlobalIllum5CloneEv(int param_1)

{
  undefined1 uVar1;
  undefined1 uVar2;
  int *piVar3;
  int iVar4;
  void *pvVar5;
  undefined4 uVar6;
  uint uVar7;
  undefined4 uVar8;
  void *pvVar9;
  int iVar10;
  uint uVar11;
  int extraout_r2;
  int iVar12;
  uint uVar13;
  undefined4 *puVar14;
  undefined4 extraout_r3;
  size_t sVar15;
  undefined4 *__src;
  uint uVar16;
  uint uVar17;
  undefined1 *puVar18;
  bool bVar19;
  undefined8 uVar20;
  undefined1 auStack_48 [4];
  void *pvStack_44;
  int *piStack_3c;
  int iStack_38;
  
  piVar3 = (int *)_Znwj(0x70);
  uVar2 = *(undefined1 *)(param_1 + 4);
  iVar10 = DAT_00211ffc + 0x211eb0;
  iVar4 = *(int *)(param_1 + 8);
  piVar3[3] = *(int *)(param_1 + 0xc);
  iVar12 = *(int *)(param_1 + 0x10);
  *(undefined1 *)(piVar3 + 1) = uVar2;
  piVar3[4] = iVar12;
  piVar3[5] = *(int *)(param_1 + 0x14);
  piVar3[6] = *(int *)(param_1 + 0x18);
  iVar12 = *(int *)(param_1 + 0x1c);
  piVar3[2] = iVar4;
  piVar3[7] = iVar12;
  iVar4 = *(int *)(param_1 + 0x20);
  piVar3[0xb] = 0;
  piVar3[8] = iVar4;
  iVar12 = *(int *)(param_1 + 0x28);
  iVar4 = *(int *)(param_1 + 0x24);
  piVar3[10] = 0;
  *piVar3 = iVar10;
  piVar3[9] = 0;
  uVar16 = iVar12 - iVar4 >> 3;
  if (uVar16 == 0) {
    pvVar5 = (void *)0x0;
    iVar4 = 0;
LAB_00211f28:
    piVar3[9] = (int)pvVar5;
    piVar3[10] = (int)pvVar5;
    pvVar9 = *(void **)(param_1 + 0x24);
    iVar12 = *(int *)(param_1 + 0x28);
    piVar3[0xb] = (int)pvVar5 + iVar4;
    iVar4 = iVar12 - (int)pvVar9 >> 3;
    sVar15 = 0;
    if (iVar4 != 0) {
      sVar15 = iVar4 << 3;
      memmove(pvVar5,pvVar9,sVar15);
    }
    uVar2 = *(undefined1 *)(param_1 + 0x30);
    uVar1 = *(undefined1 *)(param_1 + 0x31);
    piVar3[10] = (int)pvVar5 + sVar15;
    *(undefined1 *)(piVar3 + 0xc) = uVar2;
    *(undefined1 *)((int)piVar3 + 0x31) = uVar1;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (piVar3 + 0xd,param_1 + 0x34);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (piVar3 + 0xe,param_1 + 0x38);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (piVar3 + 0xf,param_1 + 0x3c);
    iVar4 = *(int *)(param_1 + 0x44);
    iVar12 = *(int *)(param_1 + 0x48);
    iVar10 = *(int *)(param_1 + 0x4c);
    piVar3[0x10] = *(int *)(param_1 + 0x40);
    piVar3[0x11] = iVar4;
    piVar3[0x12] = iVar12;
    piVar3[0x13] = iVar10;
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
              (piVar3 + 0x14,param_1 + 0x50);
    iVar4 = *(int *)(param_1 + 0x54);
    iVar12 = *(int *)(param_1 + 0x58);
    piVar3[0x17] = *(int *)(param_1 + 0x5c);
    iVar10 = *(int *)(param_1 + 0x60);
    piVar3[0x15] = iVar4;
    piVar3[0x16] = iVar12;
    piVar3[0x18] = iVar10;
    piVar3[0x19] = *(int *)(param_1 + 100);
    piVar3[0x1a] = *(int *)(param_1 + 0x68);
    piVar3[0x1b] = *(int *)(param_1 + 0x6c);
    return piVar3;
  }
  if (uVar16 < 0x20000000) {
    iVar4 = uVar16 << 3;
    pvVar5 = (void *)_Znwj(iVar4);
    goto LAB_00211f28;
  }
  uVar20 = _ZSt17__throw_bad_allocv();
  uVar8 = (undefined4)((ulonglong)uVar20 >> 0x20);
  iVar4 = (int)uVar20;
  puVar18 = auStack_48;
  piStack_3c = piVar3;
  iStack_38 = param_1;
  iVar12 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(bool *)(iVar4 + 4) = iVar12 != 0;
  uVar6 = _ZN13CMemoryStream7ReadIntEv(uVar8);
  *(undefined4 *)(iVar4 + 8) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0xc) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0x10) = uVar6;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x14) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x15) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x16) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x17) = uVar2;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0x18) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0x1c) = uVar6;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x20) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x21) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x22) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x23) = uVar2;
  uVar7 = _ZN13CMemoryStream7ReadIntEv(uVar8);
  __src = *(undefined4 **)(iVar4 + 0x28);
  pvVar5 = *(void **)(iVar4 + 0x24);
  uVar16 = (int)__src - (int)pvVar5 >> 3;
  if (uVar7 <= uVar16) {
    if (uVar7 < uVar16) {
      *(void **)(iVar4 + 0x28) = (void *)((int)pvVar5 + uVar7 * 8);
    }
    goto LAB_002121d8;
  }
  uVar17 = uVar7 - uVar16;
  if (uVar17 == 0) goto LAB_002121d8;
  uVar13 = uVar17;
  puVar14 = __src;
  if (uVar17 <= (uint)(*(int *)(iVar4 + 0x2c) - (int)__src >> 3)) {
    do {
      uVar13 = uVar13 - 1;
      *puVar14 = 0;
      puVar14[1] = 0;
      puVar14 = puVar14 + 2;
    } while (uVar13 != 0);
    *(undefined4 **)(iVar4 + 0x28) = __src + uVar17 * 2;
    goto LAB_002121d8;
  }
  bVar19 = uVar17 == 0x1fffffff - uVar16;
  if (0x1fffffff - uVar16 <= uVar17 && !bVar19) {
    uVar20 = _ZSt20__throw_length_errorPKc((int)&DAT_002123a8 + DAT_002123a8);
    uVar6 = (undefined4)((ulonglong)uVar20 >> 0x20);
    iVar12 = (int)uVar20;
    if (bVar19) {
      puVar18 = (undefined1 *)(extraout_r2 + (uVar17 >> 0x1a));
    }
    *(int **)(puVar18 + -4) = &DAT_002123a8;
    *(int *)(puVar18 + -8) = iVar4;
    *(undefined4 *)(puVar18 + -0xc) = uVar8;
    *(undefined4 *)(puVar18 + -0x10) = extraout_r3;
    _ZN19CComponentLevelInit4LoadEP13CMemoryStream();
    uVar8 = _ZN13CMemoryStream9ReadFloatEv(uVar6);
    *(undefined4 *)(iVar12 + -0x10) = uVar8;
    _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
              (uVar6,iVar12 + -0xc);
    uVar8 = _ZN13CMemoryStream9ReadFloatEv(uVar6);
    *(undefined4 *)(iVar12 + -8) = uVar8;
    uVar8 = _ZN13CMemoryStream9ReadFloatEv(uVar6);
    *(undefined4 *)(iVar12 + -4) = uVar8;
    _ZN25CComponentBaseGlobalIllum4LoadEP13CMemoryStream(iVar12,uVar6);
    piVar3 = (int *)_ZN13CMemoryStream7ReadIntEv(uVar6);
    *(int **)(iVar12 + 0x70) = piVar3;
    return piVar3;
  }
  if (uVar17 < uVar16) {
    uVar13 = uVar16 * 2;
  }
  else {
    uVar13 = uVar16 + uVar17;
  }
  if (uVar13 < uVar16) {
    iVar12 = -8;
LAB_00212380:
    pvVar5 = (void *)_Znwj(iVar12);
    pvVar9 = *(void **)(iVar4 + 0x24);
    uVar13 = (int)__src - (int)pvVar9 >> 3;
  }
  else {
    uVar11 = 0x1fffffff;
    if (uVar13 < 0x1fffffff) {
      uVar11 = uVar13;
    }
    iVar12 = uVar11 << 3;
    pvVar9 = pvVar5;
    pvVar5 = (void *)0x0;
    uVar13 = uVar16;
    if (uVar11 != 0) goto LAB_00212380;
  }
  uVar11 = uVar17;
  puVar14 = (undefined4 *)((int)pvVar5 + uVar16 * 8);
  do {
    uVar11 = uVar11 - 1;
    *puVar14 = 0;
    puVar14[1] = 0;
    puVar14 = puVar14 + 2;
  } while (uVar11 != 0);
  if (uVar13 == 0) {
    sVar15 = 0;
  }
  else {
    sVar15 = uVar13 << 3;
    memmove(pvVar5,pvVar9,sVar15);
  }
  pvVar9 = (void *)((int)pvVar5 + uVar17 * 8 + sVar15);
  iVar10 = *(int *)(iVar4 + 0x28) - (int)__src >> 3;
  sVar15 = 0;
  if (iVar10 != 0) {
    sVar15 = iVar10 << 3;
    memmove(pvVar9,__src,sVar15);
  }
  if (*(int *)(iVar4 + 0x24) != 0) {
    _ZdlPv();
  }
  *(void **)(iVar4 + 0x24) = pvVar5;
  *(size_t *)(iVar4 + 0x28) = (int)pvVar9 + sVar15;
  *(int *)(iVar4 + 0x2c) = (int)pvVar5 + iVar12;
LAB_002121d8:
  if (0 < (int)uVar7) {
    uVar16 = 0;
    while( true ) {
      iVar12 = uVar16 * 8;
      pvStack_44 = pvVar5;
      uVar6 = _ZN13CMemoryStream7ReadIntEv(uVar8);
      *(undefined4 *)((int)pvStack_44 + uVar16 * 8) = uVar6;
      uVar6 = _ZN13CMemoryStream7ReadIntEv(uVar8);
      uVar16 = uVar16 + 1;
      *(undefined4 *)((int)pvVar5 + iVar12 + 4) = uVar6;
      if (uVar16 == uVar7) break;
      pvVar5 = *(void **)(iVar4 + 0x24);
    }
  }
  iVar12 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(bool *)(iVar4 + 0x30) = iVar12 != 0;
  iVar12 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(bool *)(iVar4 + 0x31) = iVar12 != 0;
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (uVar8,iVar4 + 0x34);
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (uVar8,iVar4 + 0x38);
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (uVar8,iVar4 + 0x3c);
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0x40) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0x44) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0x48) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0x4c) = uVar6;
  _ZN13CMemoryStream10ReadStringERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (uVar8,iVar4 + 0x50);
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0x54) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0x58) = uVar6;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x5c) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x5d) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x5e) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x5f) = uVar2;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0x60) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 100) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(uVar8);
  *(undefined4 *)(iVar4 + 0x68) = uVar6;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x6c) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x6d) = uVar2;
  uVar2 = _ZN13CMemoryStream8ReadCharEv(uVar8);
  *(undefined1 *)(iVar4 + 0x6e) = uVar2;
  piVar3 = (int *)_ZN13CMemoryStream8ReadCharEv(uVar8);
  *(char *)(iVar4 + 0x6f) = (char)piVar3;
  return piVar3;
}


