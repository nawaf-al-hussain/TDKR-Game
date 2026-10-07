// _ZN11Application19ApplyLanguageChangeEi @ 003f6b28

void _ZN11Application19ApplyLanguageChangeEi(int param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  uint uVar3;
  undefined4 uVar4;
  
  iVar2 = DAT_003f6bcc;
  if (*(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1) != param_2) {
    *(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1) = param_2;
    strcpy((char *)(DAT_003f6bd0 + 0x3f6b60),*(char **)(iVar2 + 0x3f6b54 + param_2 * 4));
    iVar2 = *(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1);
    if (-1 < iVar2) {
      _ZN11Application11LoadStringsEPKc_part_1369_constprop_2592(param_1);
      iVar2 = *(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1);
    }
    uVar3 = iVar2 - 6;
    if (uVar3 < 4) {
      uVar4 = *(undefined4 *)(DAT_003f6bd8 + 0x3f6ba0 + uVar3 * 4);
      uVar1 = *(undefined4 *)(DAT_003f6bd4 + 0x3f6b9c + uVar3 * 4);
    }
    else {
      uVar4 = 1000;
      uVar1 = 0;
    }
    _ZN7gameswf21setFontBaselineAdjustEf(uVar1);
    _ZN7gameswf19setFontRatioPercentEi(uVar4);
    if (*(int *)(DAT_003f6bdc + 0x3f6bc0) != 0) {
      *(undefined1 *)(*(int *)(DAT_003f6bdc + 0x3f6bc0) + 4) = 1;
    }
    return;
  }
  return;
}


