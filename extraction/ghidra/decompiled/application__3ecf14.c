// _ZN11Application9GetStringEi @ 003ecf14

int _ZN11Application9GetStringEi(int param_1,int param_2)

{
  int iVar1;
  
  iVar1 = *(int *)((int)&__DT_SYMTAB[0x1df].st_name + param_1);
  return *(int *)(iVar1 + 8) + *(int *)(*(int *)(iVar1 + 0xc) + param_2 * 4) * 2;
}


