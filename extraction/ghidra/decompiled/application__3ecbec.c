// _ZN11Application11LoadStringsEPKc @ 003ecbec

void _ZN11Application11LoadStringsEPKc(int param_1,char *param_2)

{
  int iVar1;
  size_t sVar2;
  int iVar3;
  int *piVar4;
  undefined4 uVar5;
  int iVar6;
  code *pcVar7;
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
  
  iVar3 = DAT_003ecef8;
  if (*(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1) < 0) {
    return;
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
            (&local_74);
  iVar6 = DAT_003ecefc + 0x3ecc30;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,iVar3 + 0x3ecc28);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,*(undefined4 *)(iVar6 + *(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1) * 4))
  ;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,DAT_003ecf00 + 0x3ecc5c);
  iVar1 = _ZN11Application11GetInstanceEv();
  piVar4 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 0x28);
  (**(code **)(*piVar4 + 0xc))(&local_70,piVar4,local_74);
  if (local_70 == 0) goto LAB_003ecd90;
  sVar2 = strlen(param_2);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
            (&local_74,param_2,sVar2);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,iVar3 + 0x3ecc28);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,*(undefined4 *)(iVar6 + *(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1) * 4))
  ;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
            (&local_74,DAT_003ecf04 + 0x3ecccc);
  iVar3 = _ZN11Application11GetInstanceEv();
  piVar4 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar3) + 0x28);
  (**(code **)(*piVar4 + 0xc))(&local_6c,piVar4,local_74);
  if (local_6c != 0) {
    uVar5 = *(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + param_1);
    local_64 = local_70;
    if (local_70 == 0) {
LAB_003ecd2c:
      local_60 = local_6c;
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_6c + 4);
    }
    else {
      _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_70 + 4);
      local_60 = local_6c;
      if (local_6c != 0) goto LAB_003ecd2c;
    }
    iVar3 = _ZN8CStrings14LoadStringPackEN5boost13intrusive_ptrIN6glitch2io9IReadFileEEES5_
                      (uVar5,&local_64,&local_60);
    if (local_60 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    if (local_64 != 0) {
      _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
    }
    iVar1 = DAT_003ecf08;
    if (iVar3 == 0) {
      sVar2 = strlen(param_2);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
                (&local_74,param_2,sVar2);
      iVar3 = _ZN11Application11GetInstanceEv();
      piVar4 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar3) + 0x28);
      pcVar7 = *(code **)(*piVar4 + 0xc);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                (&local_5c,&local_74);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
                (&local_5c,iVar1 + 0x3ecdb8);
      (*pcVar7)(&local_68,piVar4,local_5c);
      _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                (&local_5c);
      if (local_68 == 0) {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
                  (auStack_58,&local_74);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6appendEPKc
                  (auStack_58,iVar1 + 0x3ecdb8);
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (auStack_58);
      }
      else {
        uVar5 = *(undefined4 *)(&__DT_SYMTAB[0x1de].st_info + param_1);
        local_54 = local_68;
        _ZN6glitch21intrusive_ptr_add_refEPKNS_21IReferenceCountedBaseE(local_68 + 4);
        iVar3 = _ZN8CStrings13LoadStringMapEN5boost13intrusive_ptrIN6glitch2io9IReadFileEEE
                          (uVar5,&local_54);
        if (local_54 != 0) {
          _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
        }
        if ((iVar3 == 0) && (*(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1) == 1)) {
          memcpy(auStack_50,(void *)(DAT_003ecf0c + 0x3ece98),0x18);
          memcpy(auStack_38,(void *)(DAT_003ecf10 + 0x3eceac),0x18);
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
LAB_003ecd90:
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_74);
  return;
}


