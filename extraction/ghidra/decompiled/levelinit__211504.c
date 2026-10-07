// _ZN19CComponentLevelInitC1ERKS_ @ 00211504

int * _ZN19CComponentLevelInitC1ERKS_
                (int *param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  undefined1 uVar1;
  uint uVar2;
  int *piVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  uint uVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  int extraout_r12;
  bool bVar15;
  
  iVar5 = DAT_002117b0 + 0x211528;
  *param_1 = iVar5;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (param_1 + 1,param_2 + 4,param_3,iVar5,param_4);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (param_1 + 2,param_2 + 8);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (param_1 + 3,param_2 + 0xc);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (param_1 + 4,param_2 + 0x10);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (param_1 + 5,param_2 + 0x14);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (param_1 + 6,param_2 + 0x18);
  *(undefined1 *)(param_1 + 7) = *(undefined1 *)(param_2 + 0x1c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (param_1 + 8,param_2 + 0x20);
  iVar8 = *(int *)(param_2 + 0x28);
  iVar5 = *(int *)(param_2 + 0x24);
  param_1[9] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  iVar5 = iVar8 - iVar5 >> 2;
  uVar2 = iVar5 * -0x11111111;
  uVar9 = uVar2;
  if (iVar5 * 0x11111111 != 0) {
    bVar15 = iVar5 * 0x11111111 == -0x4444444;
    if (0x4444443 < uVar2 && !bVar15) {
      iVar5 = _ZSt17__throw_bad_allocv();
                    /* WARNING: Could not recover jumptable at 0x002117b0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      if (!bVar15) {
        piVar3 = (int *)_Znwj(0xa4);
        _ZN19CComponentLevelInitC1ERKS_(piVar3,iVar5);
        return piVar3;
      }
      piVar3 = (int *)(*(code *)(extraout_r12 + iVar5 * 0x1000))();
      return piVar3;
    }
    uVar2 = _Znwj(iVar5 * 4);
    uVar9 = iVar5 * 4;
  }
  param_1[9] = uVar2;
  param_1[10] = uVar2;
  iVar5 = *(int *)(param_2 + 0x24);
  iVar8 = *(int *)(param_2 + 0x28);
  param_1[0xb] = uVar2 + uVar9;
  for (; iVar5 != iVar8; iVar5 = iVar5 + 0x3c) {
    if (uVar2 != 0) {
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (uVar2,iVar5);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (uVar2 + 4,iVar5 + 4);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (uVar2 + 8,iVar5 + 8);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (uVar2 + 0xc,iVar5 + 0xc);
      *(undefined1 *)(uVar2 + 0x10) = *(undefined1 *)(iVar5 + 0x10);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (uVar2 + 0x14,iVar5 + 0x14);
      *(undefined4 *)(uVar2 + 0x18) = *(undefined4 *)(iVar5 + 0x18);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (uVar2 + 0x1c,iVar5 + 0x1c);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (uVar2 + 0x20,iVar5 + 0x20);
      *(undefined4 *)(uVar2 + 0x24) = *(undefined4 *)(iVar5 + 0x24);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (uVar2 + 0x28,iVar5 + 0x28);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (uVar2 + 0x2c,iVar5 + 0x2c);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (uVar2 + 0x30,iVar5 + 0x30);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (uVar2 + 0x34,iVar5 + 0x34);
      *(undefined1 *)(uVar2 + 0x38) = *(undefined1 *)(iVar5 + 0x38);
    }
    uVar2 = uVar2 + 0x3c;
  }
  uVar1 = *(undefined1 *)(param_2 + 0x30);
  param_1[10] = uVar2;
  *(undefined1 *)(param_1 + 0xc) = uVar1;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (param_1 + 0xd,param_2 + 0x34);
  uVar1 = *(undefined1 *)(param_2 + 0x38);
  iVar12 = *(int *)(param_2 + 0x3c);
  param_1[0x17] = *(int *)(param_2 + 0x5c);
  iVar11 = *(int *)(param_2 + 0x40);
  iVar10 = *(int *)(param_2 + 0x44);
  param_1[0x19] = *(int *)(param_2 + 100);
  iVar7 = *(int *)(param_2 + 0x48);
  iVar14 = *(int *)(param_2 + 0x4c);
  param_1[0x1a] = *(int *)(param_2 + 0x68);
  iVar5 = *(int *)(param_2 + 0x50);
  iVar8 = *(int *)(param_2 + 0x54);
  param_1[0x1b] = *(int *)(param_2 + 0x6c);
  iVar4 = *(int *)(param_2 + 0x58);
  iVar13 = *(int *)(param_2 + 0x60);
  param_1[0x1c] = *(int *)(param_2 + 0x70);
  iVar6 = *(int *)(param_2 + 0x74);
  *(undefined1 *)(param_1 + 0xe) = uVar1;
  param_1[0xf] = iVar12;
  param_1[0x1d] = iVar6;
  iVar6 = *(int *)(param_2 + 0x78);
  param_1[0x10] = iVar11;
  param_1[0x11] = iVar10;
  param_1[0x12] = iVar7;
  param_1[0x13] = iVar14;
  param_1[0x14] = iVar5;
  param_1[0x15] = iVar8;
  param_1[0x16] = iVar4;
  param_1[0x18] = iVar13;
  param_1[0x1e] = iVar6;
  uVar1 = *(undefined1 *)(param_2 + 0xa0);
  iVar10 = *(int *)(param_2 + 0x7c);
  iVar11 = *(int *)(param_2 + 0x80);
  iVar7 = *(int *)(param_2 + 0x84);
  iVar6 = *(int *)(param_2 + 0x88);
  iVar4 = *(int *)(param_2 + 0x8c);
  iVar12 = *(int *)(param_2 + 0x90);
  iVar5 = *(int *)(param_2 + 0x98);
  iVar8 = *(int *)(param_2 + 0x9c);
  param_1[0x25] = *(int *)(param_2 + 0x94);
  param_1[0x1f] = iVar10;
  param_1[0x20] = iVar11;
  param_1[0x21] = iVar7;
  param_1[0x22] = iVar6;
  param_1[0x23] = iVar4;
  param_1[0x24] = iVar12;
  param_1[0x26] = iVar5;
  param_1[0x27] = iVar8;
  *(undefined1 *)(param_1 + 0x28) = uVar1;
  return param_1;
}


