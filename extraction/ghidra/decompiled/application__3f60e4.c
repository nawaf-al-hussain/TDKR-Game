// _ZN11Application20SafePushRenderTargetERKN5boost13intrusive_ptrIN6glitch5video13IRenderTargetEEE @ 003f60e4

void _ZN11Application20SafePushRenderTargetERKN5boost13intrusive_ptrIN6glitch5video13IRenderTargetEEE
               (undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  int *piVar2;
  
  iVar1 = _ZN11Application11GetInstanceEv();
  piVar2 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
  (**(code **)(*piVar2 + 0x70))(piVar2,param_2);
  return;
}


