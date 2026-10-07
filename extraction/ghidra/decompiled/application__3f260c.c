// _ZN11Application17GetSavedLevelNameERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEPiiib @ 003f260c

void _ZN11Application17GetSavedLevelNameERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEEPiiib
               (int param_1,undefined4 param_2,undefined4 *param_3,undefined4 param_4,int param_5,
               char param_6)

{
  int iVar1;
  undefined4 uVar2;
  int *piVar3;
  char acStack_a4 [128];
  int local_24;
  
  piVar3 = *(int **)(DAT_003f26f4 + 0x3f262c);
  local_24 = *piVar3;
  _ZNSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS1_6memory13E_MEMORY_HINTE0EEEE6assignEPKcj
            (param_2,DAT_003f26f8 + 0x3f2638,0);
  *param_3 = 0xffffffff;
  if (param_5 < 0) {
    param_5 = *(int *)((int)&__DT_SYMTAB[0x1ea].st_size + param_1);
  }
  sprintf(acStack_a4,(char *)(DAT_003f26fc + 0x3f2678),param_5);
  iVar1 = _ZN11Application14DecryptAndLoadEPKciP13CMemoryStream
                    (param_1,acStack_a4,0xb4,
                     *(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
  if ((iVar1 != 0) &&
     ((iVar1 = _ZN13CMemoryStream8ReadByteEv
                         (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1)),
      param_6 != '\0' || (iVar1 == 1)))) {
    _ZN13CMemoryStream11ReadStringCERSbIcSt11char_traitsIcEN6glitch4core10SAllocatorIcLNS2_6memory13E_MEMORY_HINTE0EEEE
              (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1),param_2);
    uVar2 = _ZN13CMemoryStream7ReadIntEv
                      (*(undefined4 *)((int)&__DT_SYMTAB[0x1ea].st_value + param_1));
    *param_3 = uVar2;
  }
  if (local_24 == *piVar3) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}


