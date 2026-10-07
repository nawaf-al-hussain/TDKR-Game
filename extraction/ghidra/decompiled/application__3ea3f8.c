// _ZN11ApplicationD1Ev @ 003ea3f8

int * _ZN11ApplicationD1Ev(int *param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int *piVar4;
  int iVar5;
  int *piVar6;
  int *piVar7;
  uint uVar8;
  int iVar9;
  int *piVar10;
  uint uVar11;
  
  *param_1 = DAT_003ea6f0 + 0x3ea414;
  _ZN10cSingletonI19cAchievementManagerE12getSingletonEv();
  _ZN10cSingletonI19cAchievementManagerE7ReleaseEv_isra_1389();
  _ZN9CControls5CleanEv();
  _Z22CleanMaterialRenderersv();
  iVar1 = _ZN11Application11GetInstanceEv();
  (**(code **)(**(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8) + 0x9c))();
  iVar1 = param_1[0x47e6];
  if ((uint)(param_1[0x47e7] - iVar1) >> 2 != 0) {
    uVar11 = 0;
    do {
      iVar9 = *(int *)(iVar1 + uVar11 * 4);
      iVar1 = uVar11 * 4;
      iVar2 = *(int *)(iVar9 + 0xc);
      iVar3 = *(int *)(iVar9 + 0x10);
      if ((uint)(iVar3 - iVar2) >> 2 != 0) {
        uVar8 = 0;
        do {
          iVar5 = *(int *)(iVar2 + uVar8 * 4);
          if (iVar5 != 0) {
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                      (iVar5 + 0x14);
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                      (iVar5 + 0x10);
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                      (iVar5 + 0xc);
            _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                      (iVar5 + 8);
            _ZdlPv(iVar5);
            *(undefined4 *)(*(int *)(*(int *)(param_1[0x47e6] + iVar1) + 0xc) + uVar8 * 4) = 0;
            iVar9 = *(int *)(param_1[0x47e6] + iVar1);
            iVar2 = *(int *)(iVar9 + 0xc);
            iVar3 = *(int *)(iVar9 + 0x10);
          }
          uVar8 = uVar8 + 1;
        } while (uVar8 < (uint)(iVar3 - iVar2 >> 2));
      }
      if (iVar2 != 0) {
        _ZdlPv(iVar2);
      }
      uVar11 = uVar11 + 1;
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar9 + 8);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (iVar9 + 4);
      _ZdlPv(iVar9);
      *(undefined4 *)(param_1[0x47e6] + iVar1) = 0;
      iVar1 = param_1[0x47e6];
    } while (uVar11 < (uint)(param_1[0x47e7] - iVar1 >> 2));
  }
  piVar10 = *(int **)(DAT_003ea6f4 + 0x3ea55c);
  iVar1 = *piVar10;
  if (iVar1 != 0) {
    piVar4 = *(int **)(iVar1 + 8);
    piVar6 = *(int **)(iVar1 + 4);
    while (piVar7 = piVar6, piVar6 != piVar4) {
      while( true ) {
        piVar6 = piVar7 + 1;
        iVar2 = *piVar7;
        if (iVar2 == 0) break;
        _ZN13CNavMeshQueryD1Ev(iVar2);
        _ZdlPv(iVar2);
        *piVar7 = 0;
        piVar4 = *(int **)(iVar1 + 8);
        piVar7 = piVar6;
        if (piVar6 == piVar4) goto LAB_003ea5a4;
      }
    }
LAB_003ea5a4:
    iVar2 = *(int *)(iVar1 + 4);
    *(int *)(iVar1 + 0x14) = *(int *)(iVar1 + 0x10);
    *(int *)(iVar1 + 8) = iVar2;
    if (*(int *)(iVar1 + 0x10) != 0) {
      _ZdlPv();
      iVar2 = *(int *)(iVar1 + 4);
    }
    if (iVar2 != 0) {
      _ZdlPv(iVar2);
    }
    _ZdlPv(iVar1);
    *piVar10 = 0;
  }
  if (param_1[0x480a] != 0) {
    _ZdlPv();
    param_1[0x480a] = 0;
  }
  if (*(int *)(DAT_003ea6f8 + 0x3ea610) != 0) {
    *(int *)(DAT_003ea6f8 + 0x3ea610) = 0;
    _ZdlPv();
  }
  if (param_1[0x47c6] != 0) {
    _ZdaPv();
    param_1[0x47c6] = 0;
  }
  _ZN5MPool10DeinitPoolEv();
  piVar10 = (int *)param_1[0x47f9];
  while (piVar10 != param_1 + 0x47f9) {
    piVar10 = (int *)*piVar10;
    _ZdlPv();
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x47ec);
  if (param_1[0x47e6] != 0) {
    _ZdlPv();
  }
  piVar10 = (int *)param_1[0x47be];
  while (param_1 + 0x47be != piVar10) {
    piVar10 = (int *)*piVar10;
    _ZdlPv();
  }
  if (param_1[0x47bd] != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
  _ZN3glf3AppD1Ev(param_1);
  return param_1;
}


