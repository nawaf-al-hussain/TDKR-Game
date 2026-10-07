// _ZN11Application16RequireLoadLevelEPKci @ 003edecc

void _ZN11Application16RequireLoadLevelEPKci(int param_1,undefined4 param_2,undefined4 param_3)

{
  undefined4 uVar1;
  
  uVar1 = _ZN11GS_BaseMenu15GetMissionIndexEPKcb_constprop_2447(param_2);
  *(undefined4 *)(&__DT_SYMTAB[0x1e7].st_info + param_1) = param_3;
  *(undefined4 *)((int)&__DT_SYMTAB[0x1e7].st_size + param_1) = uVar1;
  return;
}


