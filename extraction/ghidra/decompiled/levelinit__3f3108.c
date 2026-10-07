// _ZN11Application23LoadLevelInitCheckPointEv @ 003f3108

undefined4 _ZN11Application23LoadLevelInitCheckPointEv(int param_1)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  undefined1 auStack_1c [8];
  
  iVar1 = _ZN11Application14DecryptAndLoadEPKciP13CMemoryStream
                    (param_1,DAT_003f31d8 + 0x3f3128,0xb4,
                     *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  if (iVar1 == 0) {
    uVar3 = 0;
  }
  else {
    *(undefined4 *)(*(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1) + 0xc) = 0;
    iVar1 = _ZN6CLevel8GetLevelEv();
    if (iVar1 == 0) {
      uVar3 = 1;
    }
    else {
      iVar2 = _ZN13CMemoryStream8ReadByteEv
                        (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
      if (iVar2 == 1) {
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
                  (auStack_1c,DAT_003f31dc + 0x3f3190);
        _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                  (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),auStack_1c);
        _ZN13CMemoryStream7ReadIntEv(*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
        uVar3 = _ZN6CLevel4LoadEP13CMemoryStream
                          (iVar1,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
        _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
                  (auStack_1c);
      }
      else {
        uVar3 = 0;
      }
    }
  }
  return uVar3;
}


