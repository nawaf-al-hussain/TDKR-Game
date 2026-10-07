// _ZN6glitch5scene18SBatchMeshCompilerINS0_10CBatchMeshIvNS0_31SSegmentExtraDataHandlingPolicyIvNS0_25SBatchMeshSegmentInternalEEEEEE11postProcessEv @ 00306088

void _ZN6glitch5scene18SBatchMeshCompilerINS0_10CBatchMeshIvNS0_31SSegmentExtraDataHandlingPolicyIvNS0_25SBatchMeshSegmentInternalEEEEEE11postProcessEv
               (int param_1)

{
  bool bVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  int iVar5;
  int *piVar6;
  int *piVar7;
  undefined4 uVar8;
  undefined4 *puVar9;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined1 local_48;
  undefined1 local_47;
  undefined4 *local_44;
  undefined4 *local_40;
  undefined4 *local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  int local_2c;
  
  local_34 = *(undefined4 *)(param_1 + 0x28);
  piVar6 = *(int **)(DAT_003062bc + 0x3060a8);
  local_2c = *piVar6;
  uVar8 = *(undefined4 *)(param_1 + 0x24);
  local_44 = (undefined4 *)0x0;
  local_40 = (undefined4 *)0x0;
  local_3c = (undefined4 *)0x0;
  local_38 = 1;
  local_30 = 1;
  puVar2 = (undefined4 *)_Z11GlitchAllocjN6glitch6memory13E_MEMORY_HINTE(4,0);
  if (puVar2 != (undefined4 *)0x0) {
    *puVar2 = uVar8;
  }
  puVar4 = local_44;
  puVar9 = puVar2;
  if (local_44 != (undefined4 *)0x0) {
    do {
      if (puVar9 != (undefined4 *)0x0) {
        *puVar9 = *puVar4;
      }
      puVar4 = puVar4 + 1;
      puVar9 = puVar9 + 1;
    } while (puVar4 != (undefined4 *)0x0);
    puVar9 = (undefined4 *)((int)puVar2 + (-(int)(local_44 + 1) & 0xfffffffcU) + 4);
  }
  puVar9 = puVar9 + 1;
  if (local_40 != (undefined4 *)0x0) {
    puVar4 = (undefined4 *)0x0;
    puVar3 = puVar9;
    do {
      if (puVar3 != (undefined4 *)0x0) {
        *puVar3 = *puVar4;
      }
      puVar4 = puVar4 + 1;
      puVar3 = puVar3 + 1;
    } while (local_40 != puVar4);
    puVar9 = (undefined4 *)((int)puVar9 + ((uint)(local_40 + -1) & 0xfffffffc) + 4);
  }
  if (local_44 != (undefined4 *)0x0) {
    _Z10GlitchFreePv();
  }
  local_48 = 0;
  local_3c = puVar2 + 1;
  local_47 = 0;
  local_64 = 0;
  local_60 = 0;
  local_5c = 0;
  local_58 = 0;
  local_54 = 0;
  local_50 = 0;
  local_4c = 0;
  local_44 = puVar2;
  local_40 = puVar9;
  (**(code **)(**(int **)(param_1 + 0x44) + 0x78))
            (*(int **)(param_1 + 0x44),param_1 + 0x18,*(undefined4 *)(param_1 + 0x38),
             *(undefined4 *)(param_1 + 0xc),&local_64);
  puVar4 = *(undefined4 **)(param_1 + 0x1c);
  puVar9 = *(undefined4 **)(param_1 + 0x18);
  for (puVar2 = puVar9; puVar2 != puVar4; puVar2 = puVar2 + 5) {
    if (puVar2[2] != 0) {
      _Z10GlitchFreePv();
    }
    if (puVar2[1] != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    piVar7 = (int *)*puVar2;
    if (piVar7 != (int *)0x0) {
      if (*piVar7 == 2) {
        _ZNK6glitch5video9CMaterial23removeFromRootSceneNodeEv(piVar7);
      }
      DataMemoryBarrier(0xf);
      do {
        iVar5 = *piVar7;
        bVar1 = (bool)hasExclusiveAccess(piVar7);
      } while (!bVar1);
      *piVar7 = iVar5 + -1;
      DataMemoryBarrier(0xf);
      if (iVar5 + -1 == 0) {
        _ZN6glitch5video9CMaterialD1Ev(piVar7);
        _Z10GlitchFreePv(piVar7);
      }
    }
  }
  *(undefined4 **)(param_1 + 0x1c) = puVar9;
  if (local_44 != (undefined4 *)0x0) {
    _Z10GlitchFreePv();
  }
  if (local_2c != *piVar6) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}


