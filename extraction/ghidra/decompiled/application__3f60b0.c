// _ZN11Application8isFrozenEv @ 003f60b0

void _ZN11Application8isFrozenEv(int param_1)

{
  if (*(char *)((int)&__DT_SYMTAB[0x1f1].st_name + param_1) != '\0') {
    if (*(char *)((int)&__DT_SYMTAB[0x1f1].st_name + param_1 + 1) != '\0') {
      *(undefined1 *)((int)&__DT_SYMTAB[0x1f1].st_name + param_1 + 1) = 0;
    }
    return;
  }
  return;
}


