// _ZN15CWeatherManagerD1Ev @ 0041cf00

int _ZN15CWeatherManagerD1Ev(int param_1)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  uint uVar4;
  undefined1 auStack_14 [4];
  
  iVar2 = *(int *)(param_1 + 0xc);
  iVar1 = *(int *)(param_1 + 0x10);
  if ((uint)(iVar1 - iVar2) >> 2 != 0) {
    uVar4 = 0;
    do {
      piVar3 = *(int **)(iVar2 + uVar4 * 4);
      if (piVar3 != (int *)0x0) {
        (**(code **)(*piVar3 + 4))(piVar3);
        *(undefined4 *)(*(int *)(param_1 + 0xc) + uVar4 * 4) = 0;
        iVar2 = *(int *)(param_1 + 0xc);
        iVar1 = *(int *)(param_1 + 0x10);
      }
      uVar4 = uVar4 + 1;
    } while (uVar4 < (uint)(iVar1 - iVar2 >> 2));
  }
  iVar1 = DAT_0041d014;
  *(int *)(param_1 + 0x10) = iVar2;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
            (auStack_14,iVar1 + 0x41cf88);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEaSERKS7_
            (param_1 + 0x18,auStack_14);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_14);
  *(undefined4 *)(param_1 + 0x20) = 0;
  if (*(int **)(param_1 + 0x44) != (int *)0x0) {
    (**(code **)(**(int **)(param_1 + 0x44) + 0x84))();
    piVar3 = *(int **)(param_1 + 0x44);
    if (piVar3 != (int *)0x0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE
                ((int)piVar3 + *(int *)(*piVar3 + -0x10));
    }
  }
  if (*(int *)(param_1 + 0x38) != 0) {
    _ZdlPv();
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x1c);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (param_1 + 0x18);
  if (*(int *)(param_1 + 0xc) != 0) {
    _ZdlPv();
  }
  return param_1;
}


