// _ZN13CZonesManager16UpdateZoneOffsetEiii @ 002cd1d8

void _ZN13CZonesManager16UpdateZoneOffsetEiii
               (int param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int local_54 [4];
  undefined1 local_44;
  undefined1 local_43;
  int local_40 [4];
  undefined1 local_30;
  undefined1 local_2f;
  int local_2c [4];
  undefined1 local_1c;
  undefined1 local_1b;
  
  iVar5 = *(int *)(param_1 + 0x24);
  iVar4 = param_1 + 0x20;
  iVar3 = iVar5;
  iVar1 = iVar4;
  while (iVar3 != 0) {
    if (*(int *)(iVar3 + 0x10) < param_2) {
      iVar3 = *(int *)(iVar3 + 0xc);
    }
    else {
      iVar3 = *(int *)(iVar3 + 8);
      iVar1 = iVar3;
    }
  }
  iVar3 = iVar4;
  if ((iVar4 == iVar1) || (iVar2 = iVar5, param_2 < *(int *)(iVar1 + 0x10))) {
    local_44 = 0;
    local_43 = 0;
    local_54[1] = 0xffffffff;
    local_54[2] = 0xffffffff;
    local_54[3] = 0xffffffff;
    local_54[0] = param_2;
    _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4__constprop_2915
              (param_1 + 0x1c,iVar1,local_54);
    iVar5 = *(int *)(param_1 + 0x24);
    iVar2 = iVar5;
  }
  while (iVar2 != 0) {
    if (*(int *)(iVar2 + 0x10) < param_2) {
      iVar2 = *(int *)(iVar2 + 0xc);
    }
    else {
      iVar3 = iVar2;
      iVar2 = *(int *)(iVar2 + 8);
    }
  }
  if ((iVar4 == iVar3) || (param_2 < *(int *)(iVar3 + 0x10))) {
    local_30 = 0;
    local_2f = 0;
    local_40[1] = 0xffffffff;
    local_40[2] = 0xffffffff;
    local_40[3] = 0xffffffff;
    local_40[0] = param_2;
    iVar3 = _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4__constprop_2915
                      (param_1 + 0x1c,iVar3,local_40);
    iVar5 = *(int *)(param_1 + 0x24);
  }
  *(undefined4 *)(iVar3 + 0x1c) = param_4;
  iVar3 = iVar4;
  while (iVar5 != 0) {
    if (*(int *)(iVar5 + 0x10) < param_2) {
      iVar5 = *(int *)(iVar5 + 0xc);
    }
    else {
      iVar3 = iVar5;
      iVar5 = *(int *)(iVar5 + 8);
    }
  }
  if ((iVar4 == iVar3) || (param_2 < *(int *)(iVar3 + 0x10))) {
    local_2c[1] = 0xffffffff;
    local_2c[2] = 0xffffffff;
    local_2c[3] = 0xffffffff;
    local_1c = 0;
    local_1b = 0;
    local_2c[0] = param_2;
    iVar3 = _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4__constprop_2915
                      (param_1 + 0x1c,iVar3,local_2c);
  }
  *(undefined4 *)(iVar3 + 0x18) = param_3;
  return;
}


