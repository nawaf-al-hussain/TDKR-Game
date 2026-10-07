// _ZN13CZonesManager13UnloadMissionEi @ 002cd0b8

void _ZN13CZonesManager13UnloadMissionEi(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  int iVar4;
  int iVar5;
  int local_28;
  int local_24 [4];
  undefined1 local_14;
  undefined1 local_13;
  
  iVar4 = *(int *)(param_1 + 0x24);
  iVar5 = param_1 + 0x20;
  iVar1 = iVar4;
  iVar2 = iVar5;
  while (iVar1 != 0) {
    if (*(int *)(iVar1 + 0x10) < param_2) {
      iVar1 = *(int *)(iVar1 + 0xc);
    }
    else {
      iVar1 = *(int *)(iVar1 + 8);
      iVar2 = iVar1;
    }
  }
  iVar1 = iVar5;
  if ((iVar5 != iVar2) && (iVar1 = iVar2, param_2 < *(int *)(iVar2 + 0x10))) {
    iVar1 = iVar5;
  }
  iVar2 = iVar5;
  if (iVar5 != iVar1) {
    while (iVar4 != 0) {
      if (*(int *)(iVar4 + 0x10) < param_2) {
        iVar4 = *(int *)(iVar4 + 0xc);
      }
      else {
        iVar2 = iVar4;
        iVar4 = *(int *)(iVar4 + 8);
      }
    }
    if ((iVar5 == iVar2) || (param_2 < *(int *)(iVar2 + 0x10))) {
      local_24[1] = 0xffffffff;
      local_24[2] = 0xffffffff;
      local_24[3] = 0xffffffff;
      local_14 = 0;
      local_13 = 0;
      local_24[0] = param_2;
      iVar2 = _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4__constprop_2915
                        (param_1 + 0x1c,iVar2,local_24);
    }
    if (*(char *)(iVar2 + 0x20) != '\0') {
      piVar3 = *(int **)(param_1 + 0x44);
      *(undefined1 *)(param_1 + 0x7d) = 1;
      if (piVar3 == *(int **)(param_1 + 0x48)) {
        local_28 = param_2;
        _ZNSt6vectorIiSaIiEE13_M_insert_auxEN9__gnu_cxx17__normal_iteratorIPiS1_EERKi
                  (param_1 + 0x40,piVar3,&local_28);
      }
      else {
        if (piVar3 != (int *)0x0) {
          *piVar3 = param_2;
        }
        *(int **)(param_1 + 0x44) = piVar3 + 1;
      }
    }
  }
  return;
}


