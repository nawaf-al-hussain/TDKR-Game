// _ZN11Application26FormatNumberForCrtLangCharEdb @ 003eb154

void _ZN11Application26FormatNumberForCrtLangCharEdb
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined1 param_5)

{
  uint uVar1;
  
  if (*(uint *)(&__DT_SYMTAB[0x1ef].st_info + param_1) < 10) {
    uVar1 = 1 << (*(uint *)(&__DT_SYMTAB[0x1ef].st_info + param_1) & 0xff);
    if ((uVar1 & 0x20a) != 0) {
      _Z24FormatNumberInternalChardPKcS0_bb
                (param_3,param_4,DAT_003eb25c + 0x3eb1e0,DAT_003eb258 + 0x3eb1d8,param_5,0);
      return;
    }
    if ((uVar1 & 0x34) != 0) {
      _Z24FormatNumberInternalChardPKcS0_bb
                (param_3,param_4,DAT_003eb26c + 0x3eb248,DAT_003eb268 + 0x3eb240,param_5,1);
      return;
    }
    if ((uVar1 & 0x1c1) != 0) {
      _Z24FormatNumberInternalChardPKcS0_bb
                (param_3,param_4,DAT_003eb264 + 0x3eb220,DAT_003eb260 + 0x3eb218,param_5,1);
      return;
    }
  }
  _Z24FormatNumberInternalChardPKcS0_bb
            (param_3,param_4,DAT_003eb250 + 0x3eb190,DAT_003eb254 + 0x3eb198,param_5,1);
  return;
}


