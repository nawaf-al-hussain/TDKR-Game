// _ZN11Application21CheckReturnToMainMenuEv @ 003ee3a8

void _ZN11Application21CheckReturnToMainMenuEv(int param_1)

{
  if (*(char *)((int)&__DT_SYMTAB[0x1e8].st_name + param_1) == '\0') {
    return;
  }
  _ZN11GS_BaseMenu16ReturnToMainMenuEb(0);
  *(undefined1 *)((int)&__DT_SYMTAB[0x1e8].st_name + param_1) = 0;
  return;
}


