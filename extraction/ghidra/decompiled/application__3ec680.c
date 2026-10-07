// _ZN11Application4InitEN5boost13intrusive_ptrIN6glitch7IDeviceEEE @ 003ec680

void _ZN11Application4InitEN5boost13intrusive_ptrIN6glitch7IDeviceEEE(int param_1,int *param_2)

{
  int iVar1;
  int *piVar2;
  code *pcVar3;
  uint *puVar4;
  undefined4 *puVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  undefined4 uVar9;
  int *piVar10;
  uint in_fpscr;
  double dVar11;
  double dVar12;
  double dVar13;
  undefined8 uVar14;
  undefined4 local_34;
  timeval local_30;
  
  puVar4 = (uint *)(DAT_003ecac0 + 0x3ec6a0);
  gettimeofday(&local_30,(__timezone_ptr_t)0x0);
  iVar6 = DAT_003ecac4 + 0x3ec6b4;
  if (((*puVar4 & 1) == 0) && (iVar1 = __cxa_guard_acquire(puVar4), iVar1 != 0)) {
    uVar14 = VectorSignedToFloat(local_30.tv_sec,(byte)(in_fpscr >> 0x16) & 3);
    *(undefined8 *)(DAT_003ecb08 + 0x3ecaa8) = uVar14;
    __cxa_guard_release(puVar4);
  }
  iVar1 = DAT_003ecacc;
  dVar11 = (double)VectorSignedToFloat(local_30.tv_sec,(byte)(in_fpscr >> 0x16) & 3);
  dVar12 = *(double *)(DAT_003ecac8 + 0x3ec6d0);
  iVar8 = DAT_003ecacc + 0x3ec6e4;
  iVar7 = *(int *)(DAT_003ecacc + 0x3ec724);
  *(undefined4 *)((int)&__DT_SYMTAB[0x1df].st_size + param_1) = 0x3c;
  *(undefined4 *)((int)&__DT_SYMTAB[0x1ee].st_size + param_1) = 0;
  *(undefined4 *)(&__DT_SYMTAB[0x1df].st_info + param_1) = 0x41855555;
  dVar13 = (double)VectorSignedToFloat(local_30.tv_usec,(byte)(in_fpscr >> 0x16) & 3);
  *(float *)(&__DT_SYMTAB[0x1ed].st_info + param_1) =
       (float)((dVar13 + (dVar11 - dVar12) * DAT_003ecab0) * DAT_003ecab8);
  if (iVar7 < 1) {
    piVar2 = (int *)(iVar8 + (iVar7 + -1) * 4);
    iVar1 = DAT_003ecb10 + 0x3ecb88;
    uVar9 = **(undefined4 **)(iVar6 + DAT_003ecb14);
    do {
      iVar7 = iVar7 + 1;
      piVar10 = (int *)_Znwj(0x45c);
      _ZN3glf14TaskThreadImplC1Ev();
      *piVar10 = iVar1;
      piVar10[0x116] = 0x100000;
      _ZN3glf6Thread5StartEi(piVar10,uVar9);
      piVar2 = piVar2 + 1;
      *piVar2 = (int)piVar10;
    } while (iVar7 != 1);
    *(undefined4 *)(DAT_003ecb18 + 0x3ecc08) = 1;
  }
  else if (iVar7 != 1) {
    iVar7 = 1;
    uVar9 = *(undefined4 *)(iVar6 + DAT_003ecad0);
    puVar5 = (undefined4 *)(iVar1 + 0x3ec6e8);
    do {
      iVar7 = iVar7 + 1;
      _ZN3glf14TaskThreadImpl4StopEv(*puVar5);
      iVar8 = _Znwj(0xc);
      if (iVar8 != -8) {
        *(undefined4 *)(iVar8 + 8) = *puVar5;
      }
      _ZNSt8__detail15_List_node_base7_M_hookEPS0_(iVar8,uVar9);
      puVar5 = puVar5 + 1;
    } while (iVar7 < *(int *)(iVar1 + 0x3ec724));
    *(undefined4 *)(iVar1 + 0x3ec724) = 1;
  }
  if (*(char *)((int)&__DT_SYMTAB[0x1ec].st_value + param_1) != '\0') {
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
              (&local_34,DAT_003ecb0c + 0x3ecb2c);
    iVar1 = _ZN11Application11GetInstanceEv();
    piVar2 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 0x28);
    (**(code **)(*piVar2 + 0x78))(piVar2,local_34,1,1);
    _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
              (&local_34);
  }
  iVar1 = _ZN11Application11GetInstanceEv();
  piVar2 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 0x28);
  (**(code **)(*piVar2 + 0x20))(piVar2,DAT_003ecad4 + 0x3ec7b8,1,1);
  iVar1 = _ZN11Application11GetInstanceEv();
  piVar2 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 0x28);
  (**(code **)(*piVar2 + 0x20))(piVar2,DAT_003ecad8 + 0x3ec7e0,1,1);
  puVar5 = *(undefined4 **)(iVar6 + DAT_003ecadc);
  _ZN13DeviceOptions7PreLoadEv(*puVar5);
  _ZN13DeviceOptions11LoadProfileEv(*puVar5);
  piVar2 = *(int **)(*param_2 + 8);
  iVar7 = piVar2[0x53];
  iVar1 = _Znwj(0xc);
  _ZN28CCustomTexturePolicySelectorC2EPN6glitch5video15CTextureManagerE(iVar1,iVar7);
  *(int *)((int)&__DT_SYMTAB[0x1e6].st_size + param_1) = iVar1;
  if (iVar1 != 0) {
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar1 + 4);
    _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(iVar1 + 4);
  }
  iVar8 = *(int *)(iVar7 + 0xcc);
  *(int *)(iVar7 + 0xcc) = iVar1;
  if (iVar8 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  if (iVar1 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE(iVar1);
  }
  (**(code **)(*piVar2 + 0x90))(piVar2,2);
  iVar1 = DAT_003ecae0;
  (**(code **)(*piVar2 + 0x90))(piVar2,1,0);
  pcVar3 = *(code **)(*piVar2 + 0x90);
  *(uint *)(piVar2[0x53] + 200) = *(uint *)(piVar2[0x53] + 200) | 0x40;
  *(uint *)(iVar7 + 200) = *(uint *)(iVar7 + 200) | 0x80;
  (*pcVar3)(piVar2,8,1);
  _ZN6glitch4core24setProcessBufferHeapSizeEi(0x40000);
  piVar2 = (int *)_Z11CustomAllocjPKci(0x4c,iVar1 + 0x3ec8c8,0x790);
  iVar7 = DAT_003ecae8;
  piVar10 = (int *)(DAT_003ecaec + 0x3ec924);
  *piVar2 = DAT_003ecae4 + 0x3ec920;
  puVar5 = *(undefined4 **)(iVar6 + iVar7);
  piVar2[0xd] = 0;
  piVar2[2] = (int)(puVar5 + 3);
  iVar7 = DAT_003ecaf0;
  piVar2[0xe] = 0;
  piVar2[4] = 0;
  piVar2[0xf] = 0;
  piVar2[5] = 0;
  piVar2[6] = 0;
  piVar2[7] = 0;
  piVar2[8] = 0;
  piVar2[9] = 0;
  piVar2[10] = 0;
  *(undefined1 *)(piVar2 + 0xb) = 0;
  *(undefined1 *)((int)piVar2 + 0x2d) = 0;
  *(undefined1 *)(piVar2 + 0x10) = 0;
  *(undefined1 *)(piVar2 + 0x11) = 0;
  iVar7 = *(int *)(iVar6 + iVar7);
  uVar9 = *puVar5;
  *piVar10 = (int)piVar2;
  piVar2[0x12] = iVar7 + 0xc;
  _ZNSs9_M_mutateEjjj(piVar2 + 2,0,uVar9,0);
  *(undefined1 *)(piVar2 + 3) = 0;
  *(undefined1 *)(piVar2 + 1) = 0;
  iVar7 = _ZN11Application11GetInstanceEv();
  piVar2 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar7) + 0x28);
  (**(code **)(*piVar2 + 0x78))(piVar2,DAT_003ecaf4 + 0x3ec9bc,1,1);
  *(undefined1 *)(**(int **)(iVar6 + DAT_003ecaf8) + 0x25) = 1;
  iVar7 = _ZN11Application11GetInstanceEv();
  *(undefined4 *)(DAT_003ecafc + 0x3ec9fc) =
       *(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar7) + 0x18);
  piVar10 = *(int **)(iVar6 + DAT_003ecb00);
  iVar6 = *piVar10;
  *(undefined4 *)(iVar6 + 0x38) = 0xffffffff;
  *(undefined4 *)(iVar6 + 0x6c) = 0;
  piVar2 = (int *)_Z11CustomAllocjPKci(0x4c,iVar1 + 0x3ec8c8,0x79b);
  _ZN11gxGameStateC1Ev();
  iVar6 = DAT_003ecb04;
  iVar1 = *piVar10;
  piVar2[4] = 0;
  piVar2[6] = 0;
  *piVar2 = iVar6 + 0x3eca48;
  piVar2[7] = 0;
  piVar2[0xb] = 0;
  piVar2[0xc] = 0;
  piVar2[0xd] = 0;
  piVar2[0xe] = 0;
  piVar2[0xf] = 0;
  piVar2[0x10] = 0;
  piVar2[0x11] = 0;
  piVar2[0x12] = 0;
  _ZN12gxStateStack9PushStateEP11gxGameState(iVar1 + 4,piVar2);
  return;
}


