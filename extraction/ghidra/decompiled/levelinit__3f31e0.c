// _ZN11Application24ResetLevelInitCheckPointESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEi @ 003f31e0

undefined4
_ZN11Application24ResetLevelInitCheckPointESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEi
          (int param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  undefined4 uVar2;
  undefined1 *puVar3;
  int iVar4;
  undefined1 auStack_14 [4];
  
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_14);
  iVar4 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)(iVar4 + 0xc) = 0;
  *(undefined4 *)(iVar4 + 8) = 0;
  _ZN13CMemoryStream9WriteByteEh(iVar4,0);
  iVar4 = _ZN6CLevel8GetLevelEv();
  if (param_3 < 0) {
    param_3 = *(int *)(iVar4 + 0xc0);
  }
  iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                    (auStack_14,DAT_003f32b4 + 0x3f3230);
  if (iVar1 == 0) {
    if (iVar4 == 0) goto LAB_003f327c;
    puVar3 = *(undefined1 **)(DAT_003f32b8 + 0x3f326c);
  }
  else {
    puVar3 = auStack_14;
  }
  _ZN13CMemoryStream12WriteStringCERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
            (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),puVar3);
  _ZN13CMemoryStream8WriteIntEi
            (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),param_3);
LAB_003f327c:
  uVar2 = _ZN11Application14EncryptAndSaveEPKciP13CMemoryStream
                    (param_1,DAT_003f32bc + 0x3f3294,0xb4,
                     *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_14);
  return uVar2;
}


