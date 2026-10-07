// _ZN13CZonesManager13IsMissionZoneEi @ 002cd360

undefined1 _ZN13CZonesManager13IsMissionZoneEi(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int aiStack_1c [4];
  undefined1 local_c;
  undefined1 local_b;
  
  iVar1 = param_1 + 0x20;
  iVar2 = *(int *)(param_1 + 0x24);
  while (iVar2 != 0) {
    if (*(int *)(iVar2 + 0x10) < param_2) {
      iVar2 = *(int *)(iVar2 + 0xc);
    }
    else {
      iVar1 = iVar2;
      iVar2 = *(int *)(iVar2 + 8);
    }
  }
  if ((param_1 + 0x20 == iVar1) || (param_2 < *(int *)(iVar1 + 0x10))) {
    aiStack_1c[1] = 0xffffffff;
    aiStack_1c[2] = 0xffffffff;
    aiStack_1c[3] = 0xffffffff;
    local_c = 0;
    local_b = 0;
    aiStack_1c[0] = param_2;
    iVar1 = _ZNSt8_Rb_treeIiSt4pairIKiN13CZonesManager18LazyObjectFileInfoEESt10_Select1stIS4_ESt4lessIiESaIS4_EE17_M_insert_unique_ESt23_Rb_tree_const_iteratorIS4_ERKS4__constprop_2915
                      (param_1 + 0x1c,iVar1,aiStack_1c);
  }
  return *(undefined1 *)(iVar1 + 0x20);
}


