// _ZN15CWeatherManager11SetFogColorERKN6glitch5video6SColorE @ 0041eb28

bool _ZN15CWeatherManager11SetFogColorERKN6glitch5video6SColorE
               (undefined4 param_1,undefined4 *param_2)

{
  bool bVar1;
  int iVar2;
  int iVar3;
  undefined4 unaff_r4;
  
  iVar2 = _ZN11Application11GetInstanceEv();
  iVar3 = *(int *)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar2) + 8);
  iVar2 = *(int *)(iVar3 + 0x154);
  iVar3 = _ZNK6glitch5video31CGlobalMaterialParameterManager15getParameterDefEt
                    (iVar2,*(undefined2 *)(iVar3 + 0x172),0,param_2,unaff_r4);
  if (iVar3 == 0) {
    return false;
  }
  if (*(char *)(iVar3 + 9) != '\x11') {
    return false;
  }
  bVar1 = *(short *)(iVar3 + 0xc) != 0;
  if (bVar1) {
    *(undefined4 *)(*(int *)(iVar2 + 0x60) + *(int *)(iVar3 + 4)) = *param_2;
  }
  return bVar1;
}


