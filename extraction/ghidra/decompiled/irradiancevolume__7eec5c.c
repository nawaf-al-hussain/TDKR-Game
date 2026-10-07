// _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEfENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE9push_backERKS5_.part.772.constprop.1306 @ 007eec5c

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void _ZNSt6vectorISt4pairIPN6glitch10irradiance17CIrradianceVolumeEfENS1_4core10SAllocatorIS5_LNS1_6memory13E_MEMORY_HINTE0EEEE9push_backERKS5__part_772_constprop_1306
               (int *param_1,undefined4 *param_2)

{
  uint uVar1;
  undefined4 *puVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 *puVar5;
  undefined4 *puVar6;
  uint uVar7;
  undefined4 *puVar8;
  undefined4 *puVar9;
  undefined4 *puVar10;
  int iVar11;
  undefined4 *puVar12;
  
  puVar8 = (undefined4 *)param_1[1];
  if (puVar8 == (undefined4 *)param_1[2]) {
    uVar1 = (int)puVar8 - *param_1 >> 3;
    if (uVar1 == 0) {
      iVar11 = 8;
    }
    else {
      uVar7 = uVar1 * 2;
      if (uVar7 < uVar1) {
        iVar11 = -8;
      }
      else {
        if (0x1ffffffe < uVar7) {
          uVar7 = 0x1fffffff;
        }
        iVar11 = uVar7 << 3;
      }
    }
    puVar2 = (undefined4 *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(iVar11,0);
    puVar10 = (undefined4 *)*param_1;
    puVar12 = (undefined4 *)param_1[1];
    puVar5 = puVar2 + uVar1 * 2;
    puVar9 = puVar2 + 2;
    if (puVar5 != (undefined4 *)0x0) {
      uVar3 = param_2[1];
      *puVar5 = *param_2;
      puVar5[1] = uVar3;
    }
    puVar5 = puVar10;
    puVar6 = puVar2;
    if (puVar8 != puVar10) {
      do {
        if (puVar6 != (undefined4 *)0x0) {
          uVar3 = puVar5[1];
          *puVar6 = *puVar5;
          puVar6[1] = uVar3;
        }
        puVar5 = puVar5 + 2;
        puVar6 = puVar6 + 2;
      } while (puVar8 != puVar5);
      puVar9 = (undefined4 *)((int)puVar2 + ((int)puVar8 - (int)(puVar10 + 2) & 0xfffffff8U) + 0x10)
      ;
    }
    puVar6 = puVar9;
    puVar5 = puVar8;
    if (puVar8 != puVar12) {
      do {
        if (puVar6 != (undefined4 *)0x0) {
          uVar3 = puVar5[1];
          *puVar6 = *puVar5;
          puVar6[1] = uVar3;
        }
        puVar5 = puVar5 + 2;
        puVar6 = puVar6 + 2;
      } while (puVar5 != puVar12);
      puVar9 = (undefined4 *)((int)puVar9 + ((int)puVar5 - (int)(puVar8 + 2) & 0xfffffff8U) + 8);
    }
    if (puVar10 != (undefined4 *)0x0) {
      _Z10GlitchFreePv(puVar10);
    }
    *param_1 = (int)puVar2;
    param_1[1] = (int)puVar9;
    param_1[2] = (int)puVar2 + iVar11;
    return;
  }
  if (puVar8 != (undefined4 *)0x0) {
    *puVar8 = puVar8[-2];
    puVar8[1] = puVar8[-1];
    uVar4 = param_2[1];
    uVar3 = *param_2;
    param_1[1] = (int)(puVar8 + 2);
    puVar8[1] = uVar4;
    *puVar8 = uVar3;
    return;
  }
  uRam00000000 = *param_2;
  _DAT_00000004 = param_2[1];
  param_1[1] = 8;
  return;
}


