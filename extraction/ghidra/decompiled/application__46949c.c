// _ZN11Application11LoadStringsEPKc.part.1369.constprop.2592 @ 0046949c

void _ZN11Application11LoadStringsEPKc_part_1369_constprop_2592(int param_1)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  undefined4 uVar4;
  int iVar5;
  code *pcVar6;
  int iVar7;
  undefined4 local_74;
  int local_70;
  int local_6c;
  int local_68;
  int local_64;
  int local_60;
  undefined4 local_5c;
  undefined1 auStack_58 [4];
  int local_54;
  undefined1 auStack_50 [24];
  undefined1 auStack_38 [28];
  
  iVar2 = DAT_004697a0;
  iVar7 = DAT_00469798 + 0x4694bc;
  iVar5 = DAT_0046979c + 0x4694c4;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
            (&local_74,iVar7);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,iVar5);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,
             *(undefined4 *)(iVar2 + 0x4694e0 + *(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1) * 4)
            );
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,DAT_004697a4 + 0x469508);
  iVar1 = _ZN11Application11GetInstanceEv();
  piVar3 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 0x28);
  (**(code **)(*piVar3 + 0xc))(&local_70,piVar3,local_74);
  if (local_70 == 0) goto LAB_00469634;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
            (&local_74,iVar7);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,iVar5);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,
             *(undefined4 *)(iVar2 + 0x4694e0 + *(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1) * 4)
            );
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,DAT_004697a8 + 0x469570);
  iVar2 = _ZN11Application11GetInstanceEv();
  piVar3 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 0x28);
  (**(code **)(*piVar3 + 0xc))(&local_6c,piVar3,local_74);
  if (local_6c != 0) {
    uVar4 = *(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + param_1);
    local_64 = local_70;
    if (local_70 == 0) {
LAB_004695d0:
      local_60 = local_6c;
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_6c + 4);
    }
    else {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_70 + 4);
      local_60 = local_6c;
      if (local_6c != 0) goto LAB_004695d0;
    }
    iVar2 = _ZN8CStrings14LoadStringPackEN5boost13intrusive_ptrIN6glitch2io9IReadFileEEES5_
                      (uVar4,&local_64,&local_60);
    if (local_60 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (local_64 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    iVar1 = DAT_004697b0;
    if (iVar2 == 0) {
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
                (&local_74,DAT_004697ac + 0x46965c);
      iVar2 = _ZN11Application11GetInstanceEv();
      piVar3 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 0x28);
      pcVar6 = *(code **)(*piVar3 + 0xc);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (&local_5c,&local_74);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
                (&local_5c,iVar1 + 0x469664);
      (*pcVar6)(&local_68,piVar3,local_5c);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (&local_5c);
      if (local_68 == 0) {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                  (auStack_58,&local_74);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
                  (auStack_58,iVar1 + 0x469664);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (auStack_58);
      }
      else {
        uVar4 = *(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + param_1);
        local_54 = local_68;
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_68 + 4);
        iVar2 = _ZN8CStrings13LoadStringMapEN5boost13intrusive_ptrIN6glitch2io9IReadFileEEE
                          (uVar4,&local_54);
        if (local_54 != 0) {
          _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
        }
        if ((iVar2 == 0) && (*(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1) == 1)) {
          memcpy(auStack_50,(void *)(DAT_004697b4 + 0x469764),0x18);
          memcpy(auStack_38,(void *)(DAT_004697b8 + 0x469778),0x18);
          _ZN8CStrings7ReplaceEPtS0_j
                    (*(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + param_1),auStack_50,auStack_38,
                     0xc);
        }
      }
      if (local_68 != 0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
    }
    if (local_6c != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
  }
  if (local_70 != 0) {
    _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
  }
LAB_00469634:
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_74);
  return;
}


