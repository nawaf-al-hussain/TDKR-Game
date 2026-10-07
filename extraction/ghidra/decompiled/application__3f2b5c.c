// _ZN11Application14SaveCheckPointESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEi @ 003f2b5c

void _ZN11Application14SaveCheckPointESbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEi
               (int param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  int *piVar4;
  undefined1 auStack_6c [4];
  char local_68 [8];
  undefined4 local_60;
  undefined4 local_5c;
  undefined3 local_28;
  byte bStack_25;
  int local_24;
  
  piVar4 = *(int **)(DAT_003f2d94 + 0x3f2b7c);
  local_24 = *piVar4;
  _ZN11Application11GetInstanceEv();
  iVar1 = _ZN11Application11GetInstanceEv();
  if (*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) != 0) {
    iVar1 = _ZN11Application11GetInstanceEv();
    if (*(int *)(*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) + 8) +
        *(int *)(*(int *)(*(int *)(&__DT_SYMTAB[0x1de].st_info + iVar1) + 0xc) + 0x1330) * 2 != 0) {
      local_68[0] = '\x01';
      local_68[1] = 0;
      _local_28 = CONCAT13((byte)((uint)_local_28 >> 0x18) & 0xfe,0xffffff);
      _ZN7gameswf6String19encodeUTF8FromWcharEPS0_PKt(local_68);
      iVar1 = _ZN11Application11GetInstanceEv();
      iVar1 = (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1) + 0x48))();
      if (iVar1 < 2) {
        *(undefined1 *)(DAT_003f2db4 + 0x3f2d74) = 0;
      }
      else {
        *(undefined1 *)(DAT_003f2d98 + 0x3f2c20) = 1;
      }
      if (local_68[0] == -1) {
        _ZN7gameswf13free_internalEPvj(local_5c,local_60);
      }
    }
    *(undefined4 *)(DAT_003f2d9c + 0x3f2c40) = 0x447a0000;
  }
  *(undefined1 *)(DAT_003f2da0 + 0x3f2c58) = 1;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2ERKS7_
            (auStack_6c,param_2);
  iVar1 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
  *(undefined4 *)(iVar1 + 0xc) = 0;
  *(undefined4 *)(iVar1 + 8) = 0;
  iVar1 = _ZN6CLevel8GetLevelEv();
  if (param_3 < 0) {
    param_3 = *(int *)(iVar1 + 0xc0);
  }
  if ((iVar1 == 0) ||
     (iVar2 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                        (auStack_6c,DAT_003f2da4 + 0x3f2ca4), iVar2 != 0)) {
    _ZN13CMemoryStream9WriteByteEh(*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),0);
    iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                      (auStack_6c,DAT_003f2db0 + 0x3f2d44);
    uVar3 = *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1);
    if (iVar1 == 0) {
      _ZN13CMemoryStream9WriteByteEh(uVar3);
    }
    else {
      _ZN13CMemoryStream12WriteStringCERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
                (uVar3,auStack_6c);
      _ZN13CMemoryStream8WriteIntEi
                (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),param_3);
    }
  }
  else {
    _ZN13CMemoryStream9WriteByteEh(*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),1);
    _ZN13CMemoryStream12WriteStringCERKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
              (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),
               *(undefined4 *)(DAT_003f2da8 + 0x3f2cc8));
    _ZN13CMemoryStream8WriteIntEi
              (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),param_3);
    _ZN6CLevel4SaveEP13CMemoryStream
              (iVar1,*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  }
  uVar3 = _ZN11Application14EncryptAndSaveEPKciP13CMemoryStream
                    (param_1,DAT_003f2dac + 0x3f2cf8,0xb4,
                     *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (auStack_6c);
  if (local_24 == *piVar4) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail(uVar3);
}


