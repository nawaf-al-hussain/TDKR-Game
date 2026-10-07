// _ZN26CComponentLevelGlobalIllum4LoadEP13CMemoryStream @ 003d1100

/* WARNING: Removing unreachable block (ram,0x0034a2b8) */
/* WARNING: Removing unreachable block (ram,0x0034a2c4) */
/* WARNING: Removing unreachable block (ram,0x0034a2cc) */
/* WARNING: Removing unreachable block (ram,0x0034a2e8) */

void _ZN26CComponentLevelGlobalIllum4LoadEP13CMemoryStream(int param_1,int *param_2)

{
  undefined1 uVar1;
  uint uVar2;
  uint uVar3;
  uint *puVar4;
  int iVar5;
  undefined4 uVar6;
  int iVar7;
  uint *extraout_r3;
  int iVar8;
  undefined4 *puVar9;
  int *piVar10;
  undefined4 *puVar11;
  undefined4 *puVar12;
  int *piVar13;
  uint *puVar14;
  int *piVar15;
  uint *puStack_30;
  uint *apuStack_2c [4];
  
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 4) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  iVar8 = param_2[3];
  iVar7 = *param_2;
  *(undefined4 *)(param_1 + 8) = uVar6;
  uVar1 = *(undefined1 *)(iVar7 + iVar8);
  param_2[3] = iVar8 + 1;
  *(undefined1 *)(param_1 + 0xc) = uVar1;
  uVar1 = *(undefined1 *)(*param_2 + param_2[3]);
  param_2[3] = param_2[3] + 1;
  *(undefined1 *)(param_1 + 0xd) = uVar1;
  uVar1 = *(undefined1 *)(*param_2 + param_2[3]);
  param_2[3] = param_2[3] + 1;
  *(undefined1 *)(param_1 + 0xe) = uVar1;
  uVar1 = *(undefined1 *)(*param_2 + param_2[3]);
  param_2[3] = param_2[3] + 1;
  *(undefined1 *)(param_1 + 0xf) = uVar1;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x10) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x14) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  *(undefined4 *)(param_1 + 0x18) = uVar6;
  uVar6 = _ZN13CMemoryStream9ReadFloatEv(param_2);
  iVar7 = param_1 + 0x20;
  *(undefined4 *)(param_1 + 0x1c) = uVar6;
  iVar8 = DAT_0034a448 + 0x34a0f8;
  if ((char)param_2[0xd] == '\0') {
    piVar15 = *(int **)(iVar8 + DAT_0034a458);
    piVar13 = piVar15 + 3;
    _ZN13CMemoryStream11ReadStringWERSbIwSt11char_traitsIwEN6glitch4core10SAllocatorIwLNS2_6memory13E_MEMORY_HINTE0EEEE
              ();
    piVar10 = piVar13 + *piVar15;
    if (piVar13 == piVar10) {
      puStack_30 = (uint *)(*(int *)(iVar8 + DAT_0034a454) + 0xc);
LAB_0034a28c:
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                (iVar7,&puStack_30);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (&puStack_30);
      return;
    }
    uVar3 = (int)piVar10 - (int)piVar13 >> 2;
    if (uVar3 < 0x3ffffffd) {
      uVar2 = uVar3;
      if (uVar3 != 0 && 0x1000 < uVar3 + 0x1d) {
        uVar2 = (uVar3 + 0x1000) - (uVar3 + 0x1d & 0xfff);
      }
      puVar4 = (uint *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(uVar2 + 0xd,0);
      puStack_30 = puVar4 + 3;
      puVar4[1] = uVar2;
      puVar4[2] = 0;
      puVar14 = puStack_30;
      do {
        piVar15 = piVar13 + 1;
        *(char *)puVar14 = (char)*piVar13;
        puVar14 = (uint *)((int)puVar14 + 1);
        piVar13 = piVar15;
      } while (piVar10 != piVar15);
      if (puVar4 != *(uint **)(iVar8 + DAT_0034a454)) {
        *puVar4 = uVar3;
        puVar4[2] = 0;
        *(undefined1 *)((int)puStack_30 + uVar3) = 0;
      }
      goto LAB_0034a28c;
    }
LAB_0034a428:
    puVar14 = (uint *)_ZSt20__throw_length_errorPKc(DAT_0034a488 + 0x34a434);
    apuStack_2c[0] = extraout_r3;
  }
  else {
    if (*(char *)((int)param_2 + 0x35) == '\0') {
      uVar3 = _ZN13CMemoryStream7ReadIntEv();
      puVar14 = (uint *)(DAT_0034a45c + 0x34a300);
      if (((*puVar14 & 1) == 0) && (iVar5 = __cxa_guard_acquire(puVar14), iVar5 != 0)) {
        iVar5 = DAT_0034a470 + 0x34a3b4;
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_2189
                  (iVar5,DAT_0034a474 + 0x34a3b8);
        __cxa_guard_release(puVar14);
        __aeabi_atexit(iVar5,*(undefined4 *)(iVar8 + DAT_0034a478),
                       *(undefined4 *)(iVar8 + DAT_0034a46c));
      }
      if ((int)uVar3 < 0) {
        iVar8 = DAT_0034a480 + 0x34a3f8;
      }
      else if (uVar3 < (uint)(param_2[8] - param_2[7] >> 2)) {
        iVar8 = param_2[7] + uVar3 * 4;
      }
      else {
        iVar8 = DAT_0034a460 + 0x34a334;
      }
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
                (iVar7,iVar8);
      return;
    }
    uVar3 = _ZN13CMemoryStream7ReadIntEv();
    puVar14 = (uint *)(DAT_0034a44c + 0x34a114);
    if (((*puVar14 & 1) == 0) && (iVar5 = __cxa_guard_acquire(puVar14), iVar5 != 0)) {
      iVar5 = DAT_0034a464 + 0x34a36c;
      _ZNSbIwSt11char_traitsIwEN6glitch4core10SAllocatorIwLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKwRKS6__isra_2197_constprop_2932
                (iVar5);
      __cxa_guard_release(puVar14);
      __aeabi_atexit(iVar5,*(undefined4 *)(iVar8 + DAT_0034a468),
                     *(undefined4 *)(iVar8 + DAT_0034a46c));
    }
    if ((int)uVar3 < 0) {
      puVar11 = (undefined4 *)(DAT_0034a47c + 0x34a3ec);
    }
    else if (uVar3 < (uint)(param_2[0xb] - param_2[10] >> 2)) {
      puVar11 = (undefined4 *)(param_2[10] + uVar3 * 4);
    }
    else {
      puVar11 = (undefined4 *)(DAT_0034a450 + 0x34a148);
    }
    puVar11 = (undefined4 *)*puVar11;
    puVar9 = puVar11 + puVar11[-3];
    if (puVar11 == puVar9) {
      apuStack_2c[0] = (uint *)(*(int *)(iVar8 + DAT_0034a454) + 0xc);
      goto LAB_0034a1cc;
    }
    uVar3 = (int)puVar9 - (int)puVar11;
    piVar15 = (int *)((int)uVar3 >> 2);
    if ((int *)0x3ffffffc < piVar15) {
      _ZSt20__throw_length_errorPKc(DAT_0034a484 + 0x34a428);
      goto LAB_0034a428;
    }
    piVar13 = piVar15;
    if (piVar15 != (int *)0x0 && 0x1000 < (int)piVar15 + 0x1dU) {
      piVar13 = (int *)((int)piVar15 + (0x1000 - ((int)piVar15 + 0x1dU & 0xfff)));
    }
    puVar14 = (uint *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE((int)piVar13 + 0xd,0);
    apuStack_2c[0] = puVar14 + 3;
    puVar14[1] = (uint)piVar13;
    puVar14[2] = 0;
    puVar4 = apuStack_2c[0];
    do {
      puVar12 = puVar11 + 1;
      *(char *)puVar4 = (char)*puVar11;
      puVar4 = (uint *)((int)puVar4 + 1);
      puVar11 = puVar12;
    } while (puVar9 != puVar12);
    if (puVar14 == *(uint **)(iVar8 + DAT_0034a454)) goto LAB_0034a1cc;
  }
  *puVar14 = (uint)piVar15;
  puVar14[2] = 0;
  *(undefined1 *)((int)apuStack_2c[0] + ((int)uVar3 >> 2)) = 0;
LAB_0034a1cc:
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
            (iVar7,apuStack_2c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (apuStack_2c);
  return;
}


