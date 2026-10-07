// _ZN11Application20ExistsCheckPointSaveEib @ 003f2838

void _ZN11Application20ExistsCheckPointSaveEib(int param_1,int param_2,int param_3)

{
  int iVar1;
  uint uVar2;
  int *piVar3;
  int iVar4;
  char *local_a0;
  char acStack_9c [128];
  int local_1c;
  
  piVar3 = *(int **)(DAT_003f29a0 + 0x3f2858);
  iVar4 = DAT_003f29a4 + 0x3f2860;
  local_1c = *piVar3;
  if (param_2 < 0) {
    param_2 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1);
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEEC2EPKcRKS6__isra_1368
            (&local_a0,iVar4);
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
            (&local_a0,iVar4,0);
  if (param_2 < 0) {
    param_2 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1);
  }
  sprintf(acStack_9c,(char *)(DAT_003f29a8 + 0x3f28a8),param_2);
  iVar4 = _ZN11Application14DecryptAndLoadEPKciP13CMemoryStream
                    (param_1,acStack_9c,0xb4,
                     *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  if ((iVar4 == 0) ||
     ((iVar4 = _ZN13CMemoryStream8ReadByteEv
                         (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1)),
      param_3 == 0 && (iVar4 != 1)))) {
    iVar4 = -1;
  }
  else {
    _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
              (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),&local_a0);
    iVar4 = _ZN13CMemoryStream7ReadIntEv
                      (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  }
  iVar1 = _ZNKSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE7compareEPKc
                    (&local_a0,DAT_003f29ac + 0x3f28e8);
  if (iVar1 == 0) {
    iVar4 = 0;
  }
  else if ((iVar4 < 0) || (*(int *)(DAT_003f29b0 + 0x3f290c) <= iVar4)) {
    iVar4 = 0;
  }
  else {
    uVar2 = strcmp((char *)(iVar4 * 0x114 + DAT_003f29b4 + 0x3f2974),local_a0);
    iVar4 = 1 - uVar2;
    if (1 < uVar2) {
      iVar4 = 0;
    }
  }
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEED2Ev
            (&local_a0);
  if (local_1c != *piVar3) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail(iVar4);
  }
  return;
}


