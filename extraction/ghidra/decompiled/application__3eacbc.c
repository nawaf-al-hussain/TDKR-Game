// _ZN11Application14PlayTitleMusicEb @ 003eacbc

void _ZN11Application14PlayTitleMusicEb(undefined4 param_1,int param_2)

{
  undefined4 *puVar1;
  undefined1 auStack_30 [40];
  
  if (param_2 == 0) {
    puVar1 = *(undefined4 **)(DAT_003ead40 + 0x3eacd8);
  }
  else {
    puVar1 = *(undefined4 **)(DAT_003ead48 + 0x3ead24);
    _ZN15VoxSoundManager4PlayEPKcNS_6E_LOOPEi
              (auStack_30,*puVar1,DAT_003ead4c + 0x3ead2c,0xffffffff,0);
    _ZN3vox13EmitterHandleD1Ev(auStack_30);
  }
  _ZN15VoxSoundManager9PlayMusicEPKcbbiNS_13E_MUSIC_STATEEb
            (*puVar1,DAT_003ead44 + 0x3eacf4,1,0,0,3,1);
  return;
}


