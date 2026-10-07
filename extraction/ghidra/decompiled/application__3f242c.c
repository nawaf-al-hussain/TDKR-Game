// _ZN11Application20SaveCheckPointInFileEPKcSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS4_6memory13E_MEMORY_HINTE0EEEEi @ 003f242c

/* WARNING: Removing unreachable block (ram,0x003eede8) */

undefined4
_ZN11Application20SaveCheckPointInFileEPKcSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS4_6memory13E_MEMORY_HINTE0EEEEi
          (int param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  char cVar1;
  int iVar2;
  undefined4 uVar3;
  int *piVar4;
  undefined4 *puVar5;
  int *unaff_r4;
  int iVar6;
  undefined4 uStack_1c;
  
  iVar6 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)(iVar6 + 0xc) = 0;
  *(undefined4 *)(iVar6 + 8) = 0;
  iVar6 = _ZN6CLevel8GetLevelEv();
  if (param_4 < 0) {
    param_4 = *(int *)(iVar6 + 0xc0);
  }
  if ((iVar6 == 0) ||
     (iVar2 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                        (param_3,DAT_003f2534 + 0x3f2480), iVar2 != 0)) {
    _ZN13CMemoryStream9WriteByteEh(*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),0);
    iVar6 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                      (param_3,DAT_003f2538 + 0x3f24ac);
    uVar3 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    if (iVar6 == 0) {
      _ZN13CMemoryStream9WriteByteEh(uVar3);
    }
    else {
      _ZN13CMemoryStream12WriteStringCERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (uVar3,param_3);
      _ZN13CMemoryStream8WriteIntEi
                (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),param_4);
    }
  }
  else {
    _ZN13CMemoryStream9WriteByteEh(*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),1);
    _ZN13CMemoryStream12WriteStringCERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
              (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),
               *(undefined4 *)(DAT_003f253c + 0x3f24f4));
    _ZN13CMemoryStream8WriteIntEi
              (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),param_4);
    _ZN6CLevel4SaveEP13CMemoryStream
              (iVar6,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  }
  puVar5 = *(undefined4 **)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  cVar1 = *(char *)(DAT_003eedfc + 0x3eec90);
  uStack_1c = 0xb4;
  *(char *)(DAT_003eee00 + 0x3eeca4) = cVar1;
  if (cVar1 == '\0') {
    iVar6 = _ZN11Application11GetInstanceEv();
    iVar6 = *(int *)((int)&__DT_SYMTAB[0x1df].st_name + iVar6);
    iVar6 = *(int *)(iVar6 + 8) + *(int *)(*(int *)(iVar6 + 0xc) + 0x1330) * 2;
    if (iVar6 == 0) {
      uVar3 = 0;
    }
    else {
      iVar2 = _Znaj(0x100);
      _Z21_ConvertUnicodeToUTF8PcPKt(iVar2,iVar6);
      iVar6 = _ZN11Application11GetInstanceEv();
      (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar6) + 0x5c))
                (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar6),iVar2);
      uVar3 = 0;
      if (iVar2 != 0) {
        _ZdaPv();
        uVar3 = 0;
      }
    }
  }
  else {
    iVar6 = _ZN11Application11GetInstanceEv();
    piVar4 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar6) + 0x28);
    (**(code **)(*piVar4 + 0x14))(&stack0xffffffe8,piVar4,param_2,0,0);
    uVar3 = 0;
    if (unaff_r4 != (int *)0x0) {
      (**(code **)(*unaff_r4 + 0xc))(unaff_r4,&uStack_1c,4);
      _ZN11CEncryption15PrepareForWriteEP13CMemoryStream
                (*(undefined4 *)(DAT_003eee04 + 0x3eed90),puVar5);
      uVar3 = puVar5[2];
      (**(code **)(*unaff_r4 + 0xc))(unaff_r4,&stack0xffffffec,4);
      (**(code **)(*unaff_r4 + 0xc))(unaff_r4,*puVar5,uVar3);
      if (unaff_r4 != (int *)0x0) {
        _ZN6glitch21intrusive_ptr_releaseEPKNS_17IReferenceCountedE();
      }
      uVar3 = 1;
    }
  }
  return uVar3;
}


