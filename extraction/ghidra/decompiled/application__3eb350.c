// _ZN11Application37ChangeSWFFontScaleAccordingToLanguageEv @ 003eb350

void _ZN11Application37ChangeSWFFontScaleAccordingToLanguageEv(int param_1)

{
  undefined4 uVar1;
  uint uVar2;
  undefined4 uVar3;
  
  uVar2 = *(int *)(&__DT_SYMTAB[0x1ef].st_info + param_1) - 6;
  if (uVar2 < 4) {
    uVar3 = *(undefined4 *)(DAT_003eb3a4 + 0x3eb388 + uVar2 * 4);
    uVar1 = *(undefined4 *)(DAT_003eb3a0 + 0x3eb384 + uVar2 * 4);
  }
  else {
    uVar3 = 1000;
    uVar1 = 0;
  }
  _ZN7gameswf21setFontBaselineAdjustEf(uVar1);
  *(undefined4 *)(DAT_0070df08 + 0x70df04) = uVar3;
  return;
}


