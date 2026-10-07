// _ZN11Application22FormatNumberForCrtLangEdb @ 003eb03c

void _ZN11Application22FormatNumberForCrtLangEdb
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined1 param_5)

{
  uint uVar1;
  
  if (*(uint *)(&__DT_SYMTAB[0x1ef].st_info + param_1) < 10) {
    uVar1 = 1 << (*(uint *)(&__DT_SYMTAB[0x1ef].st_info + param_1) & 0xff);
    if ((uVar1 & 0x1c9) != 0) {
      _Z20FormatNumberInternaldPKcS0_bb
                (param_3,param_4,DAT_003eb140 + 0x3eb0c4,DAT_003eb13c + 0x3eb0bc,param_5,1);
      return;
    }
    if ((uVar1 & 0x34) != 0) {
      _Z20FormatNumberInternaldPKcS0_bb
                (param_3,param_4,DAT_003eb150 + 0x3eb12c,DAT_003eb14c + 0x3eb124,param_5,1);
      return;
    }
    if ((uVar1 & 0x202) != 0) {
      _Z20FormatNumberInternaldPKcS0_bb
                (param_3,param_4,DAT_003eb148 + 0x3eb104,DAT_003eb144 + 0x3eb0fc,param_5,0);
      return;
    }
  }
  _Z20FormatNumberInternaldPKcS0_bb
            (param_3,param_4,DAT_003eb134 + 0x3eb078,DAT_003eb138 + 0x3eb080,param_5,1);
  return;
}


