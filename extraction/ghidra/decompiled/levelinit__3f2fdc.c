// _ZN11Application23SaveLevelInitCheckPointESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEi @ 003f2fdc

undefined4
_ZN11Application23SaveLevelInitCheckPointESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEi
          (int param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  undefined1 auStack_1c [8];
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_1c);
  iVar3 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)(iVar3 + 0xc) = 0;
  *(undefined4 *)(iVar3 + 8) = 0;
  iVar3 = _ZN6CLevel8GetLevelEv();
  if (param_3 < 0) {
    param_3 = *(int *)(iVar3 + 0xc0);
  }
  if ((iVar3 == 0) ||
     (iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                        (auStack_1c,DAT_003f30f8 + 0x3f303c), iVar1 != 0)) {
    _ZN13CMemoryStream9WriteByteEh(*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),0);
    iVar3 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                      (auStack_1c,DAT_003f30fc + 0x3f3060);
    uVar2 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    if (iVar3 == 0) {
      _ZN13CMemoryStream9WriteByteEh(uVar2);
    }
    else {
      _ZN13CMemoryStream12WriteStringCERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (uVar2,auStack_1c);
      _ZN13CMemoryStream8WriteIntEi
                (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),param_3);
    }
  }
  else {
    _ZN13CMemoryStream9WriteByteEh(*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),1);
    _ZN13CMemoryStream12WriteStringCERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
              (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),
               *(undefined4 *)(DAT_003f3100 + 0x3f30a0));
    _ZN13CMemoryStream8WriteIntEi
              (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),param_3);
    _ZN6CLevel4SaveEP13CMemoryStream
              (iVar3,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  }
  uVar2 = _ZN11Application14EncryptAndSaveEPKciP13CMemoryStream
                    (param_1,DAT_003f3104 + 0x3f30d0,0xb4,
                     *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_1c);
  return uVar2;
}


