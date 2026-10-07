// _ZN18CPostProcessEffect9PreRenderEii @ 00455198

void _ZN18CPostProcessEffect9PreRenderEii(int param_1,int param_2,undefined4 param_3)

{
  int iVar1;
  int *piVar2;
  int iVar3;
  byte bVar4;
  int *piVar5;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  
  iVar3 = *(int *)(*(int *)(param_1 + 0x38) + 0x14);
  if (((param_2 < *(int *)(*(int *)(param_1 + 0x38) + 0x18) - iVar3 >> 2) && (-1 < param_2)) &&
     (iVar3 = *(int *)(iVar3 + param_2 * 4), iVar3 != 0)) {
    piVar5 = *(int **)(*(int *)(DAT_004552e0 + 0x4551dc) + 0x10);
    _ZN11Application11GetInstanceEv();
    iVar1 = _ZN11Application11GetInstanceEv();
    piVar2 = *(int **)(*(int *)((int)&__DT_SYMTAB[0x1de].st_name + iVar1) + 8);
    (**(code **)(*piVar2 + 0x70))(piVar2,iVar3);
    local_18 = *(undefined4 *)(iVar3 + 0x18);
    local_14 = *(undefined4 *)(iVar3 + 0x1c);
    local_20 = 0;
    local_1c = 0;
    (**(code **)(**(int **)(piVar5[0x48] + -4) + 0xc))(*(int **)(piVar5[0x48] + -4),&local_20);
    iVar1 = _ZN6CLevel8GetLevelEv();
    if (((iVar1 == 0) || (iVar1 = _ZN6CLevel8GetLevelEv(), *(char *)(iVar1 + 0xa50) == '\0')) &&
       (*(char *)(DAT_004552e4 + 0x4552a4) == '\0')) {
      iVar1 = piVar5[10];
      bVar4 = *(byte *)((int)piVar5 + 0x292);
      piVar5[10] = 0;
      if (iVar1 != 0) {
        bVar4 = bVar4 | 1;
      }
      *(byte *)((int)piVar5 + 0x292) = bVar4;
    }
    else {
      iVar1 = piVar5[10];
      bVar4 = *(byte *)((int)piVar5 + 0x292);
      piVar5[10] = -1;
      if (iVar1 != -1) {
        bVar4 = bVar4 | 1;
      }
      *(byte *)((int)piVar5 + 0x292) = bVar4;
    }
    (**(code **)(*piVar5 + 0x94))(piVar5,param_3);
    *(undefined1 *)(iVar3 + 0x20) = 1;
  }
  return;
}


