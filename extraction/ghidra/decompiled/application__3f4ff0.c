// _ZN11Application12KeepScreenOnEb @ 003f4ff0

void _ZN11Application12KeepScreenOnEb(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  
  iVar1 = _ZN11Application11GetInstanceEv();
  (**(code **)(**(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1) + 0x60))
            (*(int **)(&__DT_SYMTAB[0x1dd].st_info + iVar1),param_2);
  return;
}


