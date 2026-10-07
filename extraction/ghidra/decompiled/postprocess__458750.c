// _ZN19CPostProcessManagerD1Ev @ 00458750

int _ZN19CPostProcessManagerD1Ev(int param_1)

{
  bool bVar1;
  int iVar2;
  undefined4 *puVar3;
  int iVar4;
  int *piVar5;
  int iVar6;
  int local_20;
  int local_1c;
  
  piVar5 = *(int **)(param_1 + 0x54);
  *(undefined4 *)(param_1 + 0x54) = 0;
  if (piVar5 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar2 = *piVar5;
      bVar1 = (bool)hasExclusiveAccess(piVar5);
    } while (!bVar1);
    *piVar5 = iVar2 + -1;
    DataMemoryBarrier(0xf);
    if (iVar2 + -1 == 0) {
      _ZN6glitch5video14CVertexStreamsD1Ev(piVar5);
      free(piVar5);
    }
  }
  iVar2 = *(int *)(param_1 + 0x58);
  *(undefined4 *)(param_1 + 0x58) = 0;
  if (iVar2 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  puVar3 = *(undefined4 **)(param_1 + 0x14);
  piVar5 = (int *)*puVar3;
  if (piVar5 != (int *)0x0) {
    _ZN6glitch5video15CTextureManager13removeTextureERN5boost13intrusive_ptrINS0_8ITextureEEE
              (*(undefined4 *)(*(int *)(*(int *)(DAT_00458dfc + 0x4587d4) + 0x10) + 0x14c),
               piVar5 + 1);
    local_20 = piVar5[1];
    piVar5[1] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_20);
    iVar2 = piVar5[3];
    piVar5[3] = 0;
    if (iVar2 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    local_1c = piVar5[2];
    piVar5[2] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
    _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(piVar5 + 4);
    if (piVar5[3] != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 2);
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 1);
    if (*piVar5 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZdlPv(piVar5);
    **(undefined4 **)(param_1 + 0x14) = 0;
    puVar3 = *(undefined4 **)(param_1 + 0x14);
  }
  piVar5 = (int *)puVar3[1];
  if (piVar5 != (int *)0x0) {
    _ZN6glitch5video15CTextureManager13removeTextureERN5boost13intrusive_ptrINS0_8ITextureEEE
              (*(undefined4 *)(*(int *)(*(int *)(DAT_00458e00 + 0x458894) + 0x10) + 0x14c),
               piVar5 + 1);
    local_20 = piVar5[1];
    piVar5[1] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_20);
    iVar2 = piVar5[3];
    piVar5[3] = 0;
    if (iVar2 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    local_1c = piVar5[2];
    piVar5[2] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
    _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(piVar5 + 4);
    if (piVar5[3] != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 2);
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 1);
    if (*piVar5 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZdlPv(piVar5);
    *(undefined4 *)(*(int *)(param_1 + 0x14) + 4) = 0;
    puVar3 = *(undefined4 **)(param_1 + 0x14);
  }
  piVar5 = (int *)puVar3[2];
  if (piVar5 != (int *)0x0) {
    _ZN6glitch5video15CTextureManager13removeTextureERN5boost13intrusive_ptrINS0_8ITextureEEE
              (*(undefined4 *)(*(int *)(*(int *)(DAT_00458e04 + 0x458954) + 0x10) + 0x14c),
               piVar5 + 1);
    local_20 = piVar5[1];
    piVar5[1] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_20);
    iVar2 = piVar5[3];
    piVar5[3] = 0;
    if (iVar2 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    local_1c = piVar5[2];
    piVar5[2] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
    _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(piVar5 + 4);
    if (piVar5[3] != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 2);
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 1);
    if (*piVar5 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZdlPv(piVar5);
    *(undefined4 *)(*(int *)(param_1 + 0x14) + 8) = 0;
    puVar3 = *(undefined4 **)(param_1 + 0x14);
  }
  piVar5 = (int *)puVar3[3];
  if (piVar5 != (int *)0x0) {
    _ZN6glitch5video15CTextureManager13removeTextureERN5boost13intrusive_ptrINS0_8ITextureEEE
              (*(undefined4 *)(*(int *)(*(int *)(DAT_00458e08 + 0x458a14) + 0x10) + 0x14c),
               piVar5 + 1);
    local_20 = piVar5[1];
    piVar5[1] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_20);
    iVar2 = piVar5[3];
    piVar5[3] = 0;
    if (iVar2 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    local_1c = piVar5[2];
    piVar5[2] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
    _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(piVar5 + 4);
    if (piVar5[3] != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 2);
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 1);
    if (*piVar5 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZdlPv(piVar5);
    *(undefined4 *)(*(int *)(param_1 + 0x14) + 0xc) = 0;
    puVar3 = *(undefined4 **)(param_1 + 0x14);
  }
  piVar5 = (int *)puVar3[4];
  if (piVar5 != (int *)0x0) {
    _ZN6glitch5video15CTextureManager13removeTextureERN5boost13intrusive_ptrINS0_8ITextureEEE
              (*(undefined4 *)(*(int *)(*(int *)(DAT_00458e0c + 0x458ad4) + 0x10) + 0x14c),
               piVar5 + 1);
    local_20 = piVar5[1];
    piVar5[1] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_20);
    iVar2 = piVar5[3];
    piVar5[3] = 0;
    if (iVar2 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    local_1c = piVar5[2];
    piVar5[2] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
    _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(piVar5 + 4);
    if (piVar5[3] != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 2);
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 1);
    if (*piVar5 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZdlPv(piVar5);
    *(undefined4 *)(*(int *)(param_1 + 0x14) + 0x10) = 0;
    puVar3 = *(undefined4 **)(param_1 + 0x14);
  }
  piVar5 = (int *)puVar3[5];
  if (piVar5 != (int *)0x0) {
    _ZN6glitch5video15CTextureManager13removeTextureERN5boost13intrusive_ptrINS0_8ITextureEEE
              (*(undefined4 *)(*(int *)(*(int *)(DAT_00458e10 + 0x458b94) + 0x10) + 0x14c),
               piVar5 + 1);
    local_20 = piVar5[1];
    piVar5[1] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_20);
    iVar2 = piVar5[3];
    piVar5[3] = 0;
    if (iVar2 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    local_1c = piVar5[2];
    piVar5[2] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
    _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(piVar5 + 4);
    if (piVar5[3] != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 2);
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 1);
    if (*piVar5 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZdlPv(piVar5);
    *(undefined4 *)(*(int *)(param_1 + 0x14) + 0x14) = 0;
    puVar3 = *(undefined4 **)(param_1 + 0x14);
  }
  piVar5 = (int *)puVar3[6];
  if (piVar5 != (int *)0x0) {
    _ZN6glitch5video15CTextureManager13removeTextureERN5boost13intrusive_ptrINS0_8ITextureEEE
              (*(undefined4 *)(*(int *)(*(int *)(DAT_00458e14 + 0x458c54) + 0x10) + 0x14c),
               piVar5 + 1);
    local_20 = piVar5[1];
    piVar5[1] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(&local_20);
    iVar2 = piVar5[3];
    piVar5[3] = 0;
    if (iVar2 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    local_1c = piVar5[2];
    piVar5[2] = 0;
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev();
    _ZN5boost13intrusive_ptrIN6glitch5video9CMaterialEED2Ev(piVar5 + 4);
    if (piVar5[3] != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 2);
    _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(piVar5 + 1);
    if (*piVar5 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    _ZdlPv(piVar5);
    *(undefined4 *)(*(int *)(param_1 + 0x14) + 0x18) = 0;
  }
  iVar4 = *(int *)(param_1 + 8);
  iVar2 = *(int *)(param_1 + 0xc) - iVar4 >> 2;
  if (iVar2 != 0) {
    iVar6 = 0;
    while( true ) {
      piVar5 = *(int **)(iVar4 + iVar6 * 4);
      iVar6 = iVar6 + 1;
      if (piVar5 != (int *)0x0) {
        (**(code **)(*piVar5 + 8))(piVar5);
      }
      if (iVar6 == iVar2) break;
      iVar4 = *(int *)(param_1 + 8);
    }
  }
  if (*(int *)(param_1 + 0x58) != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  piVar5 = *(int **)(param_1 + 0x54);
  if (piVar5 != (int *)0x0) {
    DataMemoryBarrier(0xf);
    do {
      iVar2 = *piVar5;
      bVar1 = (bool)hasExclusiveAccess(piVar5);
    } while (!bVar1);
    *piVar5 = iVar2 + -1;
    DataMemoryBarrier(0xf);
    if (iVar2 + -1 == 0) {
      _ZN6glitch5video14CVertexStreamsD1Ev(piVar5);
      free(piVar5);
    }
  }
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(param_1 + 0x50);
  if (*(int *)(param_1 + 0x4c) != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  _ZNSt8_Rb_treeISbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEESt4pairIKS8_iESt10_Select1stISB_ESt4lessIS8_ESaISB_EE8_M_eraseEPSt13_Rb_tree_nodeISB_E
            (param_1 + 0x20,*(undefined4 *)(param_1 + 0x28));
  if (*(int *)(param_1 + 0x14) != 0) {
    _ZdlPv();
  }
  if (*(int *)(param_1 + 8) != 0) {
    _ZdlPv();
  }
  _ZN5boost13intrusive_ptrIN6glitch5video8ITextureEED2Ev(param_1 + 4);
  return param_1;
}


